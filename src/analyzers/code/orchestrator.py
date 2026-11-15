from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
import typer

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.base import SKIP_DIRS
from src.analyzers.code.dotnet_structural import analyze_dotnet_structural
from src.analyzers.code.fitness_engine import (
    discover_workspace_packages,
    evaluate_architecture_fitness,
)
from src.analyzers.code.java_structural import analyze_java_structural
from src.analyzers.code.js_ts_structural import analyze_js_ts_structural
from src.analyzers.code.python_ast import analyze_python_with_metrics
from src.analyzers.code.treesitter_engine import (
    MAX_DEAD_CODE_SYMBOLS,
    MAX_FILE_COMPLEXITIES,
    MAX_IMPORT_EDGES,
    is_treesitter_available,
)
from src.analyzers.dependencies import (
    parse_repository_dependencies,
    scan_dependencies_with_osv,
    scan_repository_secrets,
)
from src.analyzers.observability import apply_observability_overlay
from src.analyzers.pipeline.dag_builder import build_workflow_graph_payload
from src.analyzers.pipeline.heuristics import analyze_workflow_anti_patterns
from src.analyzers.pipeline.parser import discover_local_workflows, parse_workflow_yaml
from src.analyzers.scorecard import compute_repository_scorecard
from src.analyzers.traceability import extract_code_to_cloud_traceability
from src.models.artifacts import (
    CodeToCloudEdge,
    DependencyRecord,
    FitnessViolation,
    PipelineWorkflow,
    RepositoryScorecard,
    SecretFinding,
    VulnerabilityRecord,
    WorkspacePackage,
)


@dataclass
class CodeAnalysisResult:
    ecosystem: str
    framework: str
    components: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    modules: list[dict[str, Any]] = field(default_factory=list)
    fitness_violations: list[FitnessViolation] = field(default_factory=list)
    fitness_summary: dict[str, Any] = field(default_factory=dict)
    dependencies: list[DependencyRecord] = field(default_factory=list)
    vulnerabilities: list[VulnerabilityRecord] = field(default_factory=list)
    secrets: list[SecretFinding] = field(default_factory=list)
    workspace_packages: list[WorkspacePackage] = field(default_factory=list)
    code_to_cloud_edges: list[CodeToCloudEdge] = field(default_factory=list)
    pipelines: list[PipelineWorkflow] = field(default_factory=list)
    observability: dict[str, Any] = field(default_factory=dict)
    scorecard: RepositoryScorecard | None = None


def _run_analyzer_for_ecosystem(
    eco: Ecosystem, target_dir: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if eco == Ecosystem.PYTHON:
        return analyze_python_with_metrics(target_dir)
    if eco == Ecosystem.DOTNET:
        return analyze_dotnet_structural(target_dir)
    if eco == Ecosystem.REACT_TS_JS:
        return analyze_js_ts_structural(target_dir)
    if eco == Ecosystem.JAVA_SPRINGBOOT:
        return analyze_java_structural(target_dir)
    return [], {"files_analyzed": 0, "loc": 0, "sloc": 0, "component_count": 0}


def _collect_repo_files_and_contents(repo_dir: Path) -> tuple[list[str], dict[str, str]]:
    all_files: list[str] = []
    manifest_contents: dict[str, str] = {}
    manifest_names = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "pom.xml",
        "build.gradle",
    }

    for f in repo_dir.rglob("*"):
        if not f.is_file():
            continue
        rel_parts = f.relative_to(repo_dir).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        rel_str = str(f.relative_to(repo_dir)).replace("\\", "/")
        all_files.append(rel_str)
        if f.name in manifest_names or f.suffix.lower() == ".csproj":
            with suppress(OSError):
                manifest_contents[rel_str] = f.read_text(encoding="utf-8", errors="replace")[:8192]

    return sorted(all_files), manifest_contents


def _is_test_file_path(rel_path: str) -> bool:
    low = rel_path.replace("\\", "/").lower()
    fname = Path(low).name
    return (
        "/test/" in f"/{low}"
        or "/tests/" in f"/{low}"
        or "/__tests__/" in f"/{low}"
        or ".test." in fname
        or ".spec." in fname
        or "_test." in fname
        or fname.startswith("test_")
    )


def _prefix_rel_path(raw_path: str, prefix: str) -> str:
    cleaned = str(raw_path or "").replace("\\", "/")
    if prefix and cleaned and not cleaned.startswith(prefix):
        return f"{prefix}{cleaned}"
    return cleaned


def _parse_local_pipelines(
    repo_dir: Path,
    pipeline_policy_path: Path | str | None = None,
) -> list[PipelineWorkflow]:
    workflows: list[PipelineWorkflow] = []
    for wf_path, content in discover_local_workflows(repo_dir):
        parsed = parse_workflow_yaml(content)
        if not parsed:
            continue
        wf_payload, dag = build_workflow_graph_payload(wf_path, parsed)
        anti_patterns = analyze_workflow_anti_patterns(
            parsed,
            dag,
            file_source=wf_path,
            raw_yaml=content,
            policy_path=pipeline_policy_path,
        )
        findings_strs = [
            f"[{ap['severity']}] {ap['type']}: {ap['message']}" for ap in anti_patterns
        ]
        raw_jobs = parsed.get("jobs", {}) if isinstance(parsed.get("jobs"), dict) else {}
        workflows.append(
            PipelineWorkflow(
                id=wf_payload["id"],
                path=wf_path,
                name=wf_payload["name"],
                triggers=wf_payload["triggers"],
                jobs=raw_jobs,
                job_nodes=wf_payload["jobs"],
                dag_metrics=wf_payload["dag_metrics"],
                findings=findings_strs,
                anti_patterns=anti_patterns,
                cross_workflow_edges=wf_payload.get("cross_workflow_edges", []),
                blast_radius=wf_payload.get("blast_radius", {}),
            )
        )
    return workflows


def orchestrate_full_analysis(
    repo_dir: Path,
    *,
    policy_path: Path | str | None = None,
    pipeline_policy_path: Path | str | None = None,
    otel_traces: Path | str | None = None,
    coverage_path: Path | str | None = None,
    enable_live_osv: bool = False,
    osv_transport: httpx.BaseTransport | None = None,
    osv_cache_path: Path | None = None,
    pipelines: list[PipelineWorkflow] | None = None,
    include_local_pipelines: bool = True,
) -> CodeAnalysisResult:
    """
    Classify a local repository (including monorepo submodules) and orchestrate
    polyglot AST analysis, architectural fitness, dependency/OSV/secret scanning,
    Code-to-Cloud traceability, observability overlay, and 6-D scorecard computation.
    """
    all_files, manifest_contents = _collect_repo_files_and_contents(repo_dir)
    classification = classify_repository(all_files, file_contents=manifest_contents)

    typer.echo(
        f"Ecosystem {classification.ecosystem.value} ({classification.framework}) detected."
    )

    components: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    agg_metrics: dict[str, Any] = {
        "files_analyzed": 0,
        "loc": 0,
        "sloc": 0,
        "component_count": 0,
    }
    complexity_samples: list[float] = []
    max_cc = 0
    cog_samples: list[float] = []
    max_cog = 0
    weighted_dup_num = 0.0
    weighted_dup_den = 0
    dead_code_count = 0
    used_treesitter = False
    has_ast_run = False

    fc_by_file: dict[str, dict[str, Any]] = {}
    dead_by_key: dict[tuple[str, int, str], dict[str, Any]] = {}
    edge_conf: dict[tuple[str, str], float] = {}

    analyzed_ecos: set[Ecosystem] = set()
    module_summaries: list[dict[str, Any]] = []

    def _accumulate_module(
        mod_comps: list[dict[str, Any]],
        mod_metrics: dict[str, Any],
        prefix: str,
    ) -> None:
        nonlocal max_cc, max_cog, weighted_dup_num, weighted_dup_den
        nonlocal dead_code_count, used_treesitter, has_ast_run

        has_ast_run = True
        for comp in mod_comps:
            comp_copy = dict(comp)
            if prefix:
                comp_copy["file"] = _prefix_rel_path(comp_copy.get("file", ""), prefix)
            key = (comp_copy["name"], comp_copy["type"], comp_copy["file"])
            if key not in seen_keys:
                seen_keys.add(key)
                components.append(comp_copy)

        mod_loc = int(mod_metrics.get("loc", 0))
        agg_metrics["files_analyzed"] += int(mod_metrics.get("files_analyzed", 0))
        agg_metrics["loc"] += mod_loc
        agg_metrics["sloc"] += int(mod_metrics.get("sloc", 0))
        if mod_metrics.get("avg_cyclomatic_complexity", 0) > 0:
            complexity_samples.append(float(mod_metrics["avg_cyclomatic_complexity"]))
        max_cc = max(max_cc, int(mod_metrics.get("max_cyclomatic_complexity", 0)))

        if mod_metrics.get("ast_engine") == "tree-sitter":
            used_treesitter = True
        if mod_metrics.get("avg_cognitive_complexity", 0) > 0:
            cog_samples.append(float(mod_metrics["avg_cognitive_complexity"]))
        max_cog = max(max_cog, int(mod_metrics.get("max_cognitive_complexity", 0)))
        if mod_loc > 0:
            dup_val = float(mod_metrics.get("duplication_pct", 0.0) or 0.0)
            weighted_dup_num += dup_val * mod_loc
            weighted_dup_den += mod_loc
        dead_code_count += int(mod_metrics.get("dead_code_count", 0))

        for fc in mod_metrics.get("file_complexities", []) or []:
            if not isinstance(fc, dict):
                continue
            fc_file = _prefix_rel_path(fc.get("file", ""), prefix)
            if not fc_file:
                continue
            fc_copy = dict(fc)
            fc_copy["file"] = fc_file
            existing = fc_by_file.get(fc_file)
            if existing is None or int(fc_copy.get("cognitive", 0)) > int(
                existing.get("cognitive", 0)
            ):
                fc_by_file[fc_file] = fc_copy

        for sym in mod_metrics.get("dead_code_symbols", []) or []:
            if not isinstance(sym, dict):
                continue
            sym_file = _prefix_rel_path(sym.get("file", ""), prefix)
            sym_line = int(sym.get("line", 0))
            sym_name = str(sym.get("name", ""))
            dkey = (sym_file, sym_line, sym_name)
            if dkey not in dead_by_key:
                dead_by_key[dkey] = {
                    "name": sym_name,
                    "file": sym_file,
                    "line": sym_line,
                }

        for edge in mod_metrics.get("import_edges", []) or []:
            if not isinstance(edge, dict):
                continue
            src_file = _prefix_rel_path(edge.get("source_file", ""), prefix)
            tgt_sym = str(edge.get("target_symbol", ""))
            conf = float(edge.get("confidence", 0.0) or 0.0)
            if not src_file or not tgt_sym:
                continue
            ekey = (src_file, tgt_sym)
            if conf > edge_conf.get(ekey, 0.0):
                edge_conf[ekey] = conf

    if classification.modules:
        for mod in classification.modules:
            mod_dir = repo_dir if mod.path == "." else (repo_dir / mod.path)
            if not mod_dir.exists():
                continue
            module_summaries.append({
                "path": mod.path,
                "ecosystem": mod.ecosystem.value,
                "framework": mod.framework,
                "manifests": mod.manifest_files,
            })
            if mod.path == "." and mod.ecosystem in analyzed_ecos:
                continue
            mod_comps, mod_metrics = _run_analyzer_for_ecosystem(mod.ecosystem, mod_dir)
            analyzed_ecos.add(mod.ecosystem)
            prefix = "" if mod.path == "." else f"{mod.path}/"
            _accumulate_module(mod_comps, mod_metrics, prefix)
    elif classification.ecosystem != Ecosystem.UNKNOWN:
        comps, mod_metrics = _run_analyzer_for_ecosystem(classification.ecosystem, repo_dir)
        _accumulate_module(comps, mod_metrics, "")
    else:
        typer.echo("Unsupported ecosystem for deep architecture scan. Skipping gracefully.")

    agg_metrics["component_count"] = len(components)
    agg_metrics["avg_cyclomatic_complexity"] = (
        round(sum(complexity_samples) / len(complexity_samples), 2)
        if complexity_samples
        else 0.0
    )
    agg_metrics["max_cyclomatic_complexity"] = max_cc
    agg_metrics["ast_engine"] = (
        "tree-sitter"
        if (used_treesitter or (not has_ast_run and is_treesitter_available()))
        else "fallback"
    )
    agg_metrics["avg_cognitive_complexity"] = (
        round(sum(cog_samples) / len(cog_samples), 2) if cog_samples else 0.0
    )
    agg_metrics["max_cognitive_complexity"] = max_cog
    agg_metrics["duplication_pct"] = (
        round(weighted_dup_num / weighted_dup_den, 2) if weighted_dup_den > 0 else 0.0
    )
    agg_metrics["dead_code_count"] = dead_code_count
    agg_metrics["dead_code_symbols"] = sorted(
        dead_by_key.values(),
        key=lambda i: (i["file"], i["line"], i["name"]),
    )[:MAX_DEAD_CODE_SYMBOLS]
    agg_metrics["file_complexities"] = sorted(
        fc_by_file.values(),
        key=lambda i: (
            -int(i.get("cognitive", 0)),
            -int(i.get("cyclomatic", 0)),
            -int(i.get("loc", 0)),
            str(i.get("file", "")),
        ),
    )[:MAX_FILE_COMPLEXITIES]
    agg_metrics["import_edges"] = sorted(
        (
            {"source_file": src, "target_symbol": tgt, "confidence": conf}
            for (src, tgt), conf in edge_conf.items()
        ),
        key=lambda e: (e["source_file"], e["target_symbol"], -e["confidence"]),
    )[:MAX_IMPORT_EDGES]

    test_file_count = sum(1 for rel in all_files if _is_test_file_path(rel))
    if test_file_count > 0:
        agg_metrics["test_file_count"] = test_file_count

    # Horizon 2 Engines (deterministic, offline-safe unless enable_live_osv=True)
    workspace_packages = discover_workspace_packages(repo_dir)
    fitness_violations, fitness_summary = evaluate_architecture_fitness(
        components,
        metrics=agg_metrics,
        policy_path=policy_path,
    )
    dependencies = parse_repository_dependencies(repo_dir)
    vulnerabilities = scan_dependencies_with_osv(
        dependencies,
        repo_dir=repo_dir,
        transport=osv_transport,
        cache_path=osv_cache_path,
        enable_live=enable_live_osv,
    )
    secrets = scan_repository_secrets(repo_dir)

    if pipelines is not None:
        resolved_pipelines = list(pipelines)
    elif include_local_pipelines:
        resolved_pipelines = _parse_local_pipelines(
            repo_dir,
            pipeline_policy_path=pipeline_policy_path,
        )
    else:
        resolved_pipelines = []

    c2c_edges = extract_code_to_cloud_traceability(
        repo_dir,
        modules=module_summaries,
        workspace_packages=workspace_packages,
        pipelines=resolved_pipelines,
    )

    observability = apply_observability_overlay(
        components,
        otel_traces_path=otel_traces,
        coverage_path=coverage_path,
    )
    if observability.get("enabled") and observability.get("coverage_percent") is not None:
        agg_metrics["coverage_percent"] = observability["coverage_percent"]

    scorecard = compute_repository_scorecard(
        metrics=agg_metrics,
        components=components,
        pipelines=resolved_pipelines,
        dependencies=dependencies,
        vulnerabilities=vulnerabilities,
        secrets=secrets,
        fitness_violations=fitness_violations,
        coverage_percent=agg_metrics.get("coverage_percent"),
    )

    return CodeAnalysisResult(
        ecosystem=classification.display_language,
        framework=classification.framework,
        components=components,
        metrics=agg_metrics,
        modules=module_summaries,
        fitness_violations=fitness_violations,
        fitness_summary=fitness_summary,
        dependencies=dependencies,
        vulnerabilities=vulnerabilities,
        secrets=secrets,
        workspace_packages=workspace_packages,
        code_to_cloud_edges=c2c_edges,
        pipelines=resolved_pipelines,
        observability=observability,
        scorecard=scorecard,
    )


def orchestrate_deep_analysis(repo_dir: Path) -> list[dict[str, Any]]:
    """Determines ecosystem and routes to the appropriate structural/AST analyzers."""
    return orchestrate_full_analysis(repo_dir).components
