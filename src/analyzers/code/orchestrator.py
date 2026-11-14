from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import typer

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.base import SKIP_DIRS
from src.analyzers.code.dotnet_structural import analyze_dotnet_structural
from src.analyzers.code.java_structural import analyze_java_structural
from src.analyzers.code.js_ts_structural import analyze_js_ts_structural
from src.analyzers.code.python_ast import analyze_python_with_metrics


@dataclass
class CodeAnalysisResult:
    ecosystem: str
    framework: str
    components: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    modules: list[dict[str, Any]] = field(default_factory=list)


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


def orchestrate_full_analysis(repo_dir: Path) -> CodeAnalysisResult:
    """
    Classify a local repository (including monorepo submodules) and route to
    structural AST/code analyzers across all 4 MVP ecosystems.
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

    analyzed_ecos: set[Ecosystem] = set()
    module_summaries: list[dict[str, Any]] = []

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
            for comp in mod_comps:
                comp_copy = dict(comp)
                if prefix and not comp_copy["file"].startswith(prefix):
                    comp_copy["file"] = f"{prefix}{comp_copy['file']}"
                key = (comp_copy["name"], comp_copy["type"], comp_copy["file"])
                if key not in seen_keys:
                    seen_keys.add(key)
                    components.append(comp_copy)

            agg_metrics["files_analyzed"] += int(mod_metrics.get("files_analyzed", 0))
            agg_metrics["loc"] += int(mod_metrics.get("loc", 0))
            agg_metrics["sloc"] += int(mod_metrics.get("sloc", 0))
            if mod_metrics.get("avg_cyclomatic_complexity", 0) > 0:
                complexity_samples.append(float(mod_metrics["avg_cyclomatic_complexity"]))
            max_cc = max(max_cc, int(mod_metrics.get("max_cyclomatic_complexity", 0)))
    elif classification.ecosystem != Ecosystem.UNKNOWN:
        comps, mod_metrics = _run_analyzer_for_ecosystem(classification.ecosystem, repo_dir)
        components.extend(comps)
        agg_metrics["files_analyzed"] = int(mod_metrics.get("files_analyzed", 0))
        agg_metrics["loc"] = int(mod_metrics.get("loc", 0))
        agg_metrics["sloc"] = int(mod_metrics.get("sloc", 0))
        if mod_metrics.get("avg_cyclomatic_complexity", 0) > 0:
            complexity_samples.append(float(mod_metrics["avg_cyclomatic_complexity"]))
        max_cc = int(mod_metrics.get("max_cyclomatic_complexity", 0))
    else:
        typer.echo("Unsupported ecosystem for deep architecture scan. Skipping gracefully.")

    agg_metrics["component_count"] = len(components)
    agg_metrics["avg_cyclomatic_complexity"] = (
        round(sum(complexity_samples) / len(complexity_samples), 2)
        if complexity_samples
        else 0.0
    )
    agg_metrics["max_cyclomatic_complexity"] = max_cc

    return CodeAnalysisResult(
        ecosystem=classification.display_language,
        framework=classification.framework,
        components=components,
        metrics=agg_metrics,
        modules=module_summaries,
    )


def orchestrate_deep_analysis(repo_dir: Path) -> list[dict[str, Any]]:
    """Determines ecosystem and routes to the appropriate structural/AST analyzers."""
    return orchestrate_full_analysis(repo_dir).components
