import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import httpx
import typer

from src.analyzers.pipeline.dag_builder import build_workflow_graph_payload
from src.analyzers.pipeline.heuristics import analyze_workflow_anti_patterns
from src.analyzers.pipeline.parser import discover_local_workflows, parse_workflow_yaml
from src.core.auth import setup_secure_logging
from src.core.exporters.markdown_exporter import MarkdownArchiver
from src.core.exporters.pipeline_exporter import TopologyArchiver
from src.core.http_client import GitHubClient
from src.core.utils.export_manager import ExportManager
from src.core.utils.git_cloner import GitCloner
from src.core.utils.json_exporter import JSONExporter
from src.core.utils.markdown_exporter import MarkdownExporter
from src.models.artifacts import PipelineWorkflow, PortableArtifact
from src.models.topology import TopologyNode, WorkflowRun

app = typer.Typer()


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


def _infer_resource_from_workflow(wf_data: dict[str, Any], job_data: dict[str, Any]) -> str:
    steps = job_data.get("steps", []) if isinstance(job_data.get("steps"), list) else []
    uses_text = " ".join(
        f"{s.get('uses', '')} {s.get('run', '')}" for s in steps if isinstance(s, dict)
    ).lower()
    if "deploy-pages" in uses_text or "upload-pages-artifact" in uses_text:
        return "github-pages"
    if "kubernetes" in uses_text or "kubectl" in uses_text or "helm" in uses_text:
        return "kubernetes-cluster"
    if "azure" in uses_text:
        return "azure-cloud"
    if "aws" in uses_text:
        return "aws-cloud"
    if "docker" in uses_text:
        return "container-registry"
    return "ci-runner"


def _analyze_workflows_from_contents(
    repo_name: str,
    sha: str,
    workflow_entries: list[tuple[str, str]],
) -> tuple[list[PipelineWorkflow], list[dict[str, Any]], list[TopologyNode], list[WorkflowRun]]:
    """
    Parse workflow YAML strings into PortableArtifact workflows, Astro pipeline dicts,
    and aggregate TopologyNode / WorkflowRun entries.
    """
    artifact_workflows: list[PipelineWorkflow] = []
    astro_workflows: list[dict[str, Any]] = []
    topo_nodes: list[TopologyNode] = []
    wf_runs: list[WorkflowRun] = []

    short_repo = repo_name.split("/")[-1]

    for idx, (wf_path, content) in enumerate(workflow_entries, start=1):
        parsed = parse_workflow_yaml(content)
        if not parsed:
            continue

        wf_payload, dag = build_workflow_graph_payload(wf_path, parsed)
        anti_patterns = analyze_workflow_anti_patterns(parsed, dag)
        findings_strs = [
            f"[{ap['severity']}] {ap['type']}: {ap['message']}" for ap in anti_patterns
        ]

        raw_jobs = parsed.get("jobs", {}) if isinstance(parsed.get("jobs"), dict) else {}

        artifact_workflows.append(
            PipelineWorkflow(
                id=wf_payload["id"],
                name=wf_payload["name"],
                triggers=wf_payload["triggers"],
                jobs=raw_jobs,
                job_nodes=wf_payload["jobs"],
                dag_metrics=wf_payload["dag_metrics"],
                findings=findings_strs,
                anti_patterns=anti_patterns,
            )
        )

        astro_workflows.append(
            {
                "id": wf_payload["id"],
                "name": wf_payload["name"],
                "triggers": wf_payload["triggers"],
                "jobs": [
                    {
                        "id": j["id"],
                        "name": j["name"],
                        "runner": j["runner"],
                        "steps_count": j["steps_count"],
                        "needs": j["needs"],
                    }
                    for j in wf_payload["jobs"]
                ],
                "anti_patterns": anti_patterns,
            }
        )

        # Extract real environment & deployment resource targets from parsed jobs
        envs: list[str] = []
        resources: list[str] = []
        for jdetail in wf_payload["jobs"]:
            if jdetail.get("environment") and jdetail["environment"] not in envs:
                envs.append(jdetail["environment"])
            raw_j = raw_jobs.get(jdetail["id"], {})
            if isinstance(raw_j, dict):
                res = _infer_resource_from_workflow(parsed, raw_j)
                if res not in resources:
                    resources.append(res)

        primary_env = envs[0] if envs else "ci"
        primary_res = resources[0] if resources else "ci-runner"

        topo_nodes.append(
            TopologyNode(
                repoId=short_repo,
                repoName=short_repo,
                workflowId=idx,
                workflowName=wf_payload["name"],
                environmentNames=envs,
                deploymentTargetId=idx,
                deploymentTargetType="environment" if envs else "workflow",
                deploymentTargetName=primary_env,
                linkageMethod="workflow-environment" if envs else "workflow-job",
                resourceNames=resources,
            )
        )

        wf_runs.append(
            WorkflowRun(
                repo_name=short_repo,
                workflow_name=wf_payload["name"],
                target_env=primary_env,
                resource=primary_res,
            )
        )

    return artifact_workflows, astro_workflows, topo_nodes, wf_runs


def _analyze_repo_workflows(
    repo_dir: Path, repo_name: str, org: str | None = None
) -> PortableArtifact:
    """
    Analyze all `.github/workflows/*.{yml,yaml}` files inside a cloned or local repository.
    Returns a PortableArtifact containing parsed jobs, DAG metrics, and anti-patterns.
    """
    sha = _get_git_sha(repo_dir)
    workflow_entries = discover_local_workflows(repo_dir)
    artifact_wfs, _, _, _ = _analyze_workflows_from_contents(repo_name, sha, workflow_entries)

    return PortableArtifact(
        repository=repo_name,
        sha=sha,
        ecosystem="GITHUB_ACTIONS",
        metrics={"workflow_count": len(artifact_wfs)},
        pipelines=artifact_wfs,
        architecture_components=[],
    )


def _normalize_discovery_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        raw_items = payload
    elif isinstance(payload, dict):
        raw_items = payload.get("items", [])
    else:
        return []

    normalized: list[dict[str, Any]] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        repo_name = item.get("RepositoryName") or item.get("name") or ""
        org = item.get("Organization") or ""
        if "/" in repo_name and not org:
            org, repo_name = repo_name.split("/", 1)
        clone_url = item.get("CloneUrl") or item.get("clone_url") or (
            f"https://github.com/{org}/{repo_name}.git" if org and repo_name else ""
        )
        normalized.append(
            {
                "org": org or "local",
                "name": repo_name,
                "full_name": f"{org}/{repo_name}" if org else repo_name,
                "clone_url": clone_url,
                "default_branch": item.get("DefaultBranch") or "main",
            }
        )
    return normalized


async def _fetch_repo_workflows_api(
    client: GitHubClient,
    org: str,
    repo_name: str,
    default_branch: str,
    logger: Any,
) -> tuple[list[tuple[str, str]], str]:
    """Fetch `.github/workflows/*.yml` contents via GitHub Trees + Contents API (zero clone)."""
    try:
        paths, sha = await client.get_repo_tree(org, repo_name, ref=default_branch)
    except Exception as exc:
        logger.warning(f"API tree fetch failed for {org}/{repo_name}: {exc}")
        return [], "unknown"

    wf_paths = sorted(
        p for p in paths
        if ".github/workflows/" in f"/{p}" and (p.endswith(".yml") or p.endswith(".yaml"))
    )
    entries: list[tuple[str, str]] = []
    for wf_path in wf_paths:
        try:
            text = await client.get_file_text(org, repo_name, wf_path, ref=default_branch)
            if text:
                entries.append((wf_path, text))
        except Exception as exc:
            logger.debug(f"Could not fetch workflow {wf_path} for {org}/{repo_name}: {exc}")
    return entries, sha


async def execute_pipeline_analysis(
    from_discovery: str,
    output_dir: str,
    token: str | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
    use_clone: bool = False,
) -> ExportManager:
    log_path = Path(output_dir) / "logs" / "pipeline_analysis.log"
    logger = setup_secure_logging(log_path, token)
    logger.info(f"Starting pipeline analysis via discovery payload: {from_discovery}")

    with open(from_discovery, encoding="utf-8") as f:
        discovery_payload = json.load(f)

    repos = _normalize_discovery_items(discovery_payload)
    if not repos:
        logger.warning("Empty discovery payload detected. Proceeding with zero-length bindings.")

    manager = ExportManager(base_dir=output_dir)
    archiver = TopologyArchiver(manager)
    all_nodes: list[TopologyNode] = []
    all_runs: list[WorkflowRun] = []

    async with GitHubClient(token=token, logger=logger, transport=transport) as client:
        for repo in repos:
            org = repo["org"]
            repo_name = repo["name"]
            default_branch = repo["default_branch"]

            wf_entries: list[tuple[str, str]] = []
            sha = "unknown"

            if not use_clone:
                wf_entries, sha = await _fetch_repo_workflows_api(
                    client, org, repo_name, default_branch, logger
                )

            if not wf_entries and (use_clone or transport is None) and repo["clone_url"]:
                with GitCloner.clone_temporarily(repo["clone_url"], token) as cloned_dir:
                    if cloned_dir:
                        cloned_path = Path(cloned_dir)
                        sha = _get_git_sha(cloned_path)
                        wf_entries = discover_local_workflows(cloned_path)

            _, astro_wfs, nodes, runs = _analyze_workflows_from_contents(
                repo["full_name"], sha, wf_entries
            )
            archiver.export_repo_pipeline(org=org, repo=repo_name, sha=sha, workflows=astro_wfs)
            all_nodes.extend(nodes)
            all_runs.extend(runs)

    archiver.export(all_nodes, all_runs)
    md_archiver = MarkdownArchiver(manager)
    md_archiver.export(all_nodes, all_runs)
    manager.publish_to_latest(modules=["pipelines", "relationships", "reports"])

    logger.info(f"Completed mapping topologies natively to {manager.base_path}")
    return manager


@app.command("analyze-pipeline")
def analyze_pipeline(
    from_discovery: str | None = typer.Option(
        None, "--from-discovery", help="Path to discovery JSON"
    ),
    repos_file: str | None = typer.Option(
        None, "--repos-file", help="Path to text file containing newline-separated org/repo targets"
    ),
    repo_path: str | None = typer.Option(
        None, "--path", help="Local repository path to analyze"
    ),
    output_dir: str | None = typer.Option(
        None, "--output-dir", help="Directory to save outputs (defaults to 'exports')"
    ),
    token: str | None = typer.Option(
        None, "--token", envvar="GH_TOKEN", help="GitHub Personal Access Token (Optional)"
    ),
    use_clone: bool = typer.Option(
        False, "--clone", help="Force shallow git clone instead of GitHub API tree fetch"
    ),
):
    """
    Analyze GitHub Actions workflows into DAGs, anti-patterns,
    per-repo Astro JSONs, and aggregate topology exports.
    """
    if not from_discovery and not repos_file and not repo_path:
        typer.echo(
            "Error: Must provide --from-discovery, --repos-file, or --path",
            err=True,
        )
        raise typer.Exit(1)

    if from_discovery:
        if not os.path.exists(from_discovery):
            typer.echo(f"Error: Discovery file not found: {from_discovery}", err=True)
            raise typer.Exit(1)
        target_out = output_dir or "exports"
        asyncio.run(
            execute_pipeline_analysis(
                from_discovery=from_discovery,
                output_dir=target_out,
                token=token,
                use_clone=use_clone,
            )
        )
        return

    artifacts: list[PortableArtifact] = []
    all_nodes: list[TopologyNode] = []
    all_runs: list[WorkflowRun] = []

    resolved_export_dir = output_dir or "exports"
    manager = ExportManager(base_dir=resolved_export_dir)
    archiver = TopologyArchiver(manager)

    if repos_file:
        if not os.path.exists(repos_file):
            typer.echo(f"Error: Repos file not found: {repos_file}", err=True)
            raise typer.Exit(1)
        with open(repos_file, encoding="utf-8") as f:
            lines = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]

        typer.echo(f"Loaded {len(lines)} repositories.")
        for line in lines:
            if line.startswith("http://") or line.startswith("https://"):
                clone_url = line
                name = line.rstrip("/").removesuffix(".git").split("/")[-2:]
                repo_label = "/".join(name)
            else:
                clone_url = f"https://github.com/{line}.git"
                repo_label = line

            typer.echo(f"Processing {repo_label}...")
            with GitCloner.clone_temporarily(clone_url, token) as cloned_dir:
                if cloned_dir:
                    cloned_path = Path(cloned_dir)
                    artifact = _analyze_repo_workflows(cloned_path, repo_label)
                    artifacts.append(artifact)

                    org_part, short_name = (
                        repo_label.split("/", 1) if "/" in repo_label else ("local", repo_label)
                    )
                    wf_entries = discover_local_workflows(cloned_path)
                    _, astro_wfs, nodes, runs = _analyze_workflows_from_contents(
                        repo_label, artifact.sha, wf_entries
                    )
                    archiver.export_repo_pipeline(
                        org=org_part, repo=short_name, sha=artifact.sha, workflows=astro_wfs
                    )
                    all_nodes.extend(nodes)
                    all_runs.extend(runs)

    elif repo_path:
        local_dir = Path(repo_path)
        if not local_dir.exists():
            typer.echo(f"Error: Local path not found: {repo_path}", err=True)
            raise typer.Exit(1)
        repo_label = local_dir.name
        artifact = _analyze_repo_workflows(local_dir, repo_label)
        artifacts.append(artifact)

        wf_entries = discover_local_workflows(local_dir)
        _, astro_wfs, nodes, runs = _analyze_workflows_from_contents(
            repo_label, artifact.sha, wf_entries
        )
        archiver.export_repo_pipeline(
            org="local", repo=repo_label, sha=artifact.sha, workflows=astro_wfs
        )
        all_nodes.extend(nodes)
        all_runs.extend(runs)

    archiver.export(all_nodes, all_runs)
    MarkdownArchiver(manager).export(all_nodes, all_runs)
    manager.publish_to_latest(modules=["pipelines", "relationships", "reports"])

    if output_dir:
        json_exporter = JSONExporter(output_dir)
        md_exporter = MarkdownExporter(output_dir)
        for art in artifacts:
            json_exporter.export(art)
            md_exporter.export(art)
        typer.echo(f"Reports saved to {output_dir}")
