from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import typer

from src.analyzers.code.fitness_engine import (
    discover_workspace_packages,
    evaluate_architecture_fitness,
)
from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.analyzers.dependencies import parse_repository_dependencies, scan_repository_secrets
from src.analyzers.pipeline.dag_builder import build_workflow_graph_payload
from src.analyzers.pipeline.heuristics import analyze_workflow_anti_patterns
from src.analyzers.pipeline.parser import discover_local_workflows, parse_workflow_yaml
from src.analyzers.scorecard import compute_repository_scorecard
from src.analyzers.traceability import extract_code_to_cloud_traceability
from src.core.exporters.sarif_exporter import build_sarif_report, export_sarif_report
from src.core.utils.export_manager import ExportManager
from src.models.artifacts import PipelineWorkflow, PortableArtifact

app = typer.Typer()

_SEVERITY_RANK: dict[str, int] = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
    "NONE": 99,
}


def _get_git_sha(repo_dir: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _run_local_check(
    target_dir: Path,
    policy: Path | None = None,
    pipeline_policy: Path | None = None,
) -> tuple[PortableArtifact, list[str]]:
    sha = _get_git_sha(target_dir)
    analysis = orchestrate_full_analysis(target_dir)

    fitness_violations, fitness_summary = evaluate_architecture_fitness(
        analysis.components,
        metrics=analysis.metrics,
        policy_path=policy,
    )
    workspace_packages = discover_workspace_packages(target_dir)

    pipeline_workflows: list[PipelineWorkflow] = []
    severities: list[str] = []

    for wf_path, content in discover_local_workflows(target_dir):
        parsed = parse_workflow_yaml(content)
        if not parsed:
            continue
        wf_payload, dag = build_workflow_graph_payload(wf_path, parsed)
        anti_patterns = analyze_workflow_anti_patterns(
            parsed,
            dag,
            file_source=wf_path,
            raw_yaml=content,
            policy_path=pipeline_policy,
        )
        for ap in anti_patterns:
            severities.append(str(ap.get("severity", "MEDIUM")).upper())
        findings_strs = [
            f"[{ap['severity']}] {ap['type']}: {ap['message']}" for ap in anti_patterns
        ]
        raw_jobs = parsed.get("jobs", {}) if isinstance(parsed.get("jobs"), dict) else {}
        pipeline_workflows.append(
            PipelineWorkflow(
                id=wf_payload["id"],
                path=wf_path,
                name=wf_payload["name"],
                triggers=wf_payload["triggers"],
                jobs=raw_jobs,
                job_nodes=wf_payload["jobs"],
                dag_metrics=wf_payload["dag_metrics"],
                cross_workflow_edges=wf_payload.get("cross_workflow_edges", []),
                blast_radius=wf_payload.get("blast_radius", {}),
                findings=findings_strs,
                anti_patterns=anti_patterns,
            )
        )

    dependencies = parse_repository_dependencies(target_dir)
    secrets = scan_repository_secrets(target_dir)

    for fv in fitness_violations:
        severities.append(str(fv.severity).upper())
    for sec in secrets:
        severities.append(str(sec.severity).upper())

    merged_metrics: dict[str, Any] = {
        **analysis.metrics,
        "framework": analysis.framework,
        "fitness_passed": fitness_summary.get("passed", True),
        "fitness_violation_count": fitness_summary.get("violation_count", 0),
    }

    scorecard = compute_repository_scorecard(
        metrics=merged_metrics,
        components=analysis.components,
        pipelines=pipeline_workflows,
        dependencies=dependencies,
        vulnerabilities=[],
        secrets=secrets,
        fitness_violations=fitness_violations,
    )
    c2c_edges = extract_code_to_cloud_traceability(
        target_dir,
        modules=analysis.modules,
        workspace_packages=workspace_packages,
        pipelines=pipeline_workflows,
    )

    artifact = PortableArtifact(
        repository=target_dir.name,
        sha=sha,
        ecosystem=analysis.ecosystem,
        metrics=merged_metrics,
        pipelines=pipeline_workflows,
        architecture_components=analysis.components,
        scorecard=scorecard,
        dependencies=dependencies,
        vulnerabilities=[],
        secrets=secrets,
        fitness_violations=fitness_violations,
        code_to_cloud_edges=c2c_edges,
        workspace_packages=workspace_packages,
    )
    return artifact, severities


_REPO_PATH_OPT = typer.Option(".", "--path", help="Local repository path to check")
_SARIF_OPT = typer.Option(
    None, "--sarif", help="Path to write OASIS SARIF v2.1.0 report"
)
_FAIL_ON_OPT = typer.Option(
    "HIGH",
    "--fail-on",
    help="Minimum finding severity threshold to fail (CRITICAL|HIGH|MEDIUM|LOW|NONE)",
)
_POLICY_OPT = typer.Option(
    None, "--policy", help="Custom architecture-rules.yaml policy path"
)
_PIPELINE_POLICY_OPT = typer.Option(
    None, "--pipeline-policy", help="Custom pipeline-rules.yaml policy path"
)
_EXPORTS_DIR_OPT = typer.Option(
    None, "--exports-dir", help="Optional archival exports base directory"
)


@app.command("check")
def check(
    repo_path: str = _REPO_PATH_OPT,
    sarif_path: Path | None = _SARIF_OPT,
    fail_on: str = _FAIL_ON_OPT,
    policy: Path | None = _POLICY_OPT,
    pipeline_policy: Path | None = _PIPELINE_POLICY_OPT,
    exports_dir: Path | None = _EXPORTS_DIR_OPT,
) -> None:
    """
    Run offline PR quality gate checks (pipeline security, architecture fitness, secrets)
    and emit OASIS SARIF v2.1.0 findings (FR-028).
    """
    threshold_key = fail_on.strip().upper()
    if threshold_key not in _SEVERITY_RANK:
        typer.echo(
            f"Error: Invalid --fail-on value '{fail_on}'. "
            "Expected CRITICAL, HIGH, MEDIUM, LOW, or NONE.",
            err=True,
        )
        raise typer.Exit(2)

    target_dir = Path(repo_path).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        typer.echo(f"Error: Repository path not found: {repo_path}", err=True)
        raise typer.Exit(1)

    artifact, severities = _run_local_check(
        target_dir,
        policy=policy,
        pipeline_policy=pipeline_policy,
    )
    sarif_payload = build_sarif_report(artifact, repo_name=artifact.repository)
    total_results = len(sarif_payload["runs"][0]["results"])

    if sarif_path is not None:
        written = export_sarif_report(
            artifact,
            output_path=sarif_path,
            repo_name=artifact.repository,
        )
        typer.echo(f"SARIF v2.1.0 report written to {written}")

    if exports_dir is not None:
        manager = ExportManager(base_dir=str(exports_dir))
        sarif_out = manager.get_path("sarif", f"local-{artifact.repository}.sarif.json")
        export_sarif_report(artifact, output_path=sarif_out, repo_name=artifact.repository)
        rep_out = manager.get_path("reports", f"local-{artifact.repository}-analysis.json")
        rep_out.write_text(artifact.model_dump_json(indent=2), encoding="utf-8")
        manager.publish_to_latest(modules=["sarif", "reports"])

    grade = artifact.scorecard.overall_grade if artifact.scorecard else "?"
    score = artifact.scorecard.overall_score if artifact.scorecard else 0.0
    typer.echo(
        f"Check completed for {artifact.repository}: {total_results} finding(s), "
        f"Scorecard {grade} ({score:.2f}/100)."
    )

    if threshold_key != "NONE":
        threshold_rank = _SEVERITY_RANK[threshold_key]
        breaches = [s for s in severities if _SEVERITY_RANK.get(s, 0) >= threshold_rank]
        if breaches:
            typer.echo(
                f"Gate failed: {len(breaches)} finding(s) at or above severity {threshold_key}.",
                err=True,
            )
            raise typer.Exit(1)
