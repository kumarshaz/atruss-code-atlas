import json
import os
import subprocess
from pathlib import Path

import httpx
import typer

from src.analyzers.code.fitness_engine import (
    _build_component_graph,
    compute_component_blast_radius,
)
from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.analyzers.drift import compute_drift_report, render_drift_markdown
from src.core.exporters.llms_exporter import export_llms_context
from src.core.exporters.sarif_exporter import export_sarif_report
from src.core.exporters.sbom_exporter import export_cyclonedx_sbom
from src.core.utils.export_manager import ExportManager
from src.core.utils.git_cloner import GitCloner
from src.core.utils.json_exporter import JSONExporter
from src.core.utils.markdown_exporter import MarkdownExporter
from src.models.artifacts import PortableArtifact

app = typer.Typer()

_REPO_PATH_OPT = typer.Option(None, "--path", help="Local repository path to analyze")
_OUTPUT_DIR_OPT = typer.Option(
    None, "--output-dir", help="Directory to save standalone JSON/Markdown reports"
)
_EXPORTS_DIR_OPT = typer.Option(
    "exports", "--exports-dir", help="Archival exports base directory (for Astro UI)"
)
_FROM_DISCOVERY_OPT = typer.Option(
    None, "--from-discovery", help="Path to discovery JSON manifest"
)
_REPOS_FILE_OPT = typer.Option(
    None, "--repos-file", help="Path to text document containing line-separated repo targets"
)
_TOKEN_OPT = typer.Option(
    None, "--token", envvar="GH_TOKEN", help="GitHub Personal Access Token for cloning"
)
_SBOM_OPT = typer.Option(
    True,
    "--sbom/--no-sbom",
    help="Export deterministic CycloneDX v1.6 JSON SBOM alongside code analysis",
)
_POLICY_OPT = typer.Option(
    None, "--policy", help="Custom architecture-rules.yaml policy manifest path"
)
_PIPELINE_POLICY_OPT = typer.Option(
    None, "--pipeline-policy", help="Custom pipeline-rules.yaml policy manifest path"
)
_FORMAT_OPT = typer.Option(
    "json", "--format", help="Primary output format: json, markdown, or sarif"
)
_DIFF_OPT = typer.Option(
    None, "--diff", help="Baseline archival snapshot directory to compute drift_report.{json,md}"
)
_BLAST_RADIUS_OPT = typer.Option(
    None, "--blast-radius", help="Target component name for blast-radius & centrality analysis"
)
_OTEL_TRACES_OPT = typer.Option(
    None,
    "--otel-traces",
    help="Optional OpenTelemetry JSON traces export path for hot-path overlay",
)
_COVERAGE_OPT = typer.Option(
    None, "--coverage", help="Optional Cobertura XML or LCOV path for coverage overlay"
)
_LIVE_OSV_OPT = typer.Option(
    False, "--live-osv", help="Enable live OSV.dev API queries (offline-safe cache by default)"
)


def _get_git_sha(repo_dir: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


def _analyze_repo_code(
    repo_dir: Path,
    repo_name: str,
    *,
    policy_path: Path | str | None = None,
    pipeline_policy_path: Path | str | None = None,
    otel_traces: Path | str | None = None,
    coverage_path: Path | str | None = None,
    enable_live_osv: bool = False,
    osv_transport: httpx.BaseTransport | None = None,
    osv_cache_path: Path | None = None,
) -> PortableArtifact:
    sha = _get_git_sha(repo_dir)
    analysis = orchestrate_full_analysis(
        repo_dir,
        policy_path=policy_path,
        pipeline_policy_path=pipeline_policy_path,
        otel_traces=otel_traces,
        coverage_path=coverage_path,
        enable_live_osv=enable_live_osv,
        osv_transport=osv_transport,
        osv_cache_path=osv_cache_path,
    )

    merged_metrics = {
        **analysis.metrics,
        "framework": analysis.framework,
        "fitness_passed": analysis.fitness_summary.get("passed", True),
        "fitness_violation_count": analysis.fitness_summary.get("violation_count", 0),
    }

    return PortableArtifact(
        repository=repo_name,
        sha=sha,
        ecosystem=analysis.ecosystem,
        metrics=merged_metrics,
        pipelines=analysis.pipelines,
        architecture_components=analysis.components,
        scorecard=analysis.scorecard,
        dependencies=analysis.dependencies,
        vulnerabilities=analysis.vulnerabilities,
        secrets=analysis.secrets,
        fitness_violations=analysis.fitness_violations,
        code_to_cloud_edges=analysis.code_to_cloud_edges,
        workspace_packages=analysis.workspace_packages,
        observability=analysis.observability,
    )


def _load_targets_from_discovery(from_discovery: str) -> list[dict[str, str]]:
    with open(from_discovery, encoding="utf-8") as f:
        payload = json.load(f)

    items = payload.get("items", []) if isinstance(payload, dict) else payload
    targets: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        org = item.get("Organization") or ""
        name = item.get("RepositoryName") or item.get("name") or ""
        clone_url = item.get("CloneUrl") or item.get("clone_url") or ""
        if "/" in name and not org:
            org, name = name.split("/", 1)
        if not clone_url and org and name:
            clone_url = f"https://github.com/{org}/{name}.git"
        if clone_url and name:
            full_name = f"{org}/{name}" if org else name
            targets.append({
                "url": clone_url,
                "name": full_name,
                "org": org or "local",
                "repo": name,
            })
    return targets


@app.command("analyze-code")
def analyze_code(
    repo_path: str | None = _REPO_PATH_OPT,
    output_dir: str | None = _OUTPUT_DIR_OPT,
    exports_dir: str = _EXPORTS_DIR_OPT,
    from_discovery: str | None = _FROM_DISCOVERY_OPT,
    repos_file: str | None = _REPOS_FILE_OPT,
    token: str | None = _TOKEN_OPT,
    sbom: bool = _SBOM_OPT,
    policy: Path | None = _POLICY_OPT,
    pipeline_policy: Path | None = _PIPELINE_POLICY_OPT,
    output_format: str = _FORMAT_OPT,
    diff_baseline: str | None = _DIFF_OPT,
    blast_radius: str | None = _BLAST_RADIUS_OPT,
    otel_traces: Path | None = _OTEL_TRACES_OPT,
    coverage: Path | None = _COVERAGE_OPT,
    live_osv: bool = _LIVE_OSV_OPT,
):
    """Performs deep architectural code scanning exporting strictly offline artifacts."""
    fmt = output_format.strip().lower()
    if fmt not in {"json", "markdown", "sarif"}:
        typer.echo(
            f"Error: Invalid --format '{output_format}'. Expected json, markdown, or sarif.",
            err=True,
        )
        raise typer.Exit(2)

    if diff_baseline and not Path(diff_baseline).exists():
        typer.echo(f"Error: Baseline directory not found: {diff_baseline}", err=True)
        raise typer.Exit(1)

    if not repo_path and not from_discovery and not repos_file:
        typer.echo(
            "Error: Must provide either --path, --from-discovery, or --repos-file",
            err=True,
        )
        raise typer.Exit(1)

    targets_to_process: list[dict[str, str]] = []

    if from_discovery:
        if not os.path.exists(from_discovery):
            typer.echo(f"Error: Discovery file not found: {from_discovery}", err=True)
            raise typer.Exit(1)
        targets_to_process = _load_targets_from_discovery(from_discovery)

    elif repos_file:
        if not os.path.exists(repos_file):
            typer.echo(f"Error: Repos file not found: {repos_file}", err=True)
            raise typer.Exit(1)
        with open(repos_file, encoding="utf-8") as f:
            lines = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]
        for line in lines:
            if line.startswith("http://") or line.startswith("https://"):
                parts = line.rstrip("/").removesuffix(".git").split("/")[-2:]
                org, repo = parts[0], parts[1]
                clone_url = line
            elif "/" in line:
                org, repo = line.split("/", 1)
                clone_url = f"https://github.com/{line}.git"
            else:
                org, repo = "local", line
                clone_url = f"https://github.com/{line}.git"
            targets_to_process.append({
                "url": clone_url,
                "name": f"{org}/{repo}",
                "org": org,
                "repo": repo,
            })

    processed: list[tuple[str, str, PortableArtifact]] = []

    if targets_to_process:
        typer.echo(f"Loaded {len(targets_to_process)} repositories.")
        for item in targets_to_process:
            typer.echo(f"\nProcessing {item['name']}...")
            with GitCloner.clone_temporarily(item["url"], token) as repo_dir_str:
                if repo_dir_str:
                    artifact = _analyze_repo_code(
                        Path(repo_dir_str),
                        item["name"],
                        policy_path=policy,
                        pipeline_policy_path=pipeline_policy,
                        otel_traces=otel_traces,
                        coverage_path=coverage,
                        enable_live_osv=live_osv,
                    )
                    processed.append((item["org"], item["repo"], artifact))
    else:
        local_dir = Path(repo_path).resolve()  # type: ignore[arg-type]
        if not local_dir.exists():
            typer.echo(f"Error: Local path not found: {repo_path}", err=True)
            raise typer.Exit(1)
        artifact = _analyze_repo_code(
            local_dir,
            local_dir.name,
            policy_path=policy,
            pipeline_policy_path=pipeline_policy,
            otel_traces=otel_traces,
            coverage_path=coverage,
            enable_live_osv=live_osv,
        )
        processed.append(("local", local_dir.name, artifact))

    if blast_radius:
        for _org, _repo, art in processed:
            graph = _build_component_graph(art.architecture_components, metrics=art.metrics)
            blast_res = compute_component_blast_radius(graph, target_node=blast_radius)
            art.metrics["blast_radius"] = blast_res
            typer.echo(json.dumps({"repository": art.repository, **blast_res}, indent=2))

    # Always export into archival exports/{timestamp}/{reports,sbom,sarif}/ and sync latest/
    manager = ExportManager(base_dir=exports_dir)
    reports_dir = str(manager.base_path / "reports")
    archival_md = MarkdownExporter(reports_dir)
    published_modules = ["reports"]

    for org, repo, art in processed:
        safe_prefix = f"{org}-{repo}"
        (manager.base_path / "reports" / f"{safe_prefix}-analysis.json").write_text(
            art.model_dump_json(indent=2), encoding="utf-8"
        )
        archival_md.export(
            art,
            filename=f"{safe_prefix}-report.md",
            include_frontmatter=True,
        )
        if sbom:
            sbom_path = manager.get_path("sbom", f"{safe_prefix}.cdx.json")
            export_cyclonedx_sbom(
                art.repository,
                art.sha,
                art.dependencies,
                art.vulnerabilities,
                output_path=sbom_path,
            )
            if "sbom" not in published_modules:
                published_modules.append("sbom")
        if fmt == "sarif":
            sarif_path = manager.get_path("sarif", f"{safe_prefix}.sarif.json")
            export_sarif_report(art, output_path=sarif_path, repo_name=art.repository)
            if "sarif" not in published_modules:
                published_modules.append("sarif")

    latest_dir = manager.publish_to_latest(modules=published_modules)

    drift_json_text: str | None = None
    drift_md_text: str | None = None
    if diff_baseline:
        drift_report = compute_drift_report(Path(diff_baseline), latest_dir)
        drift_json_text = json.dumps(drift_report, indent=2) + "\n"
        drift_md_text = render_drift_markdown(drift_report)
        manager.get_path("drift", "drift_report.json").write_text(
            drift_json_text, encoding="utf-8"
        )
        manager.get_path("drift", "drift_report.md").write_text(drift_md_text, encoding="utf-8")
        manager.publish_to_latest(modules=["drift"])

    export_llms_context(latest_dir, output_dir=manager.base_path / "llms")
    manager.publish_to_latest(modules=["llms"])

    scored = [art for _, _, art in processed if art.scorecard is not None]
    avg_score = (
        round(
            sum(art.scorecard.overall_score for art in scored if art.scorecard) / len(scored),
            2,
        )
        if scored
        else 0.0
    )
    repos_summary = {
        art.repository: {
            "overall_score": art.scorecard.overall_score if art.scorecard else 0.0,
            "overall_grade": art.scorecard.overall_grade if art.scorecard else "N/A",
            "technical_debt_score": art.scorecard.technical_debt_score if art.scorecard else 0.0,
            "vulnerabilities_count": len(art.vulnerabilities),
            "fitness_violations_count": len(art.fitness_violations),
            "secrets_count": len(art.secrets),
        }
        for _org, _repo, art in processed
    }
    manager.append_catalog_history({
        "command": "analyze-code",
        "repo_count": len(processed),
        "average_overall_score": avg_score,
        "total_vulnerabilities": sum(len(art.vulnerabilities) for _, _, art in processed),
        "total_fitness_violations": sum(len(art.fitness_violations) for _, _, art in processed),
        "total_secrets": sum(len(art.secrets) for _, _, art in processed),
        "repos": repos_summary,
    })

    if output_dir:
        out_path = Path(output_dir)
        json_exporter = JSONExporter(output_dir)
        md_exporter = MarkdownExporter(output_dir)
        for _org, _repo, art in processed:
            json_exporter.export(art)
            md_exporter.export(art, include_frontmatter=True)
            if fmt == "sarif":
                export_sarif_report(art, output_dir=out_path, repo_name=art.repository)
        if drift_json_text is not None and drift_md_text is not None:
            out_path.mkdir(parents=True, exist_ok=True)
            (out_path / "drift_report.json").write_text(drift_json_text, encoding="utf-8")
            (out_path / "drift_report.md").write_text(drift_md_text, encoding="utf-8")
        typer.echo(f"\nReports saved to {output_dir}")
    else:
        typer.echo(f"Analysis complete. Archival reports saved to {manager.base_path / 'reports'}")


if __name__ == "__main__":
    app()
