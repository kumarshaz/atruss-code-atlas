import asyncio
import json
from pathlib import Path
import typer

from src.core.http_client import GitHubClient
from src.core.auth import setup_secure_logging
from src.core.utils.export_manager import ExportManager
from src.core.exporters.pipeline_exporter import TopologyArchiver
from src.core.exporters.markdown_exporter import MarkdownArchiver
from src.models.topology import TopologyNode, WorkflowRun

app = typer.Typer()

async def execute_pipeline_analysis(
    from_discovery: str,
    output_dir: str,
    token: str
):
    log_path = Path(output_dir) / "logs" / "pipeline_analysis.log"
    logger = setup_secure_logging(log_path, token)
    
    logger.info(f"Starting pipeline analysis via discovery payload: {from_discovery}")
    
    with open(from_discovery, "r", encoding="utf-8") as f:
        discovery_payload = json.load(f)
        
    repos = discovery_payload.get("items", [])
    if not repos:
        logger.warning("Empty discovery payload detected. Proceeding with zero-length bindings.")
        
    nodes = []
    runs = []
    
    async with GitHubClient(token=token, logger=logger) as client:
        # Phase 2 -> 8 structural extraction
        for repo in repos:
            org = repo.get("Organization")
            repo_name = repo.get("RepositoryName")
            repo_id = repo.get("RepositoryId")
            
            try:
                workflows = await client.get_paginated(f"/repos/{org}/{repo_name}/actions/workflows")
            except Exception as e:
                logger.error(f"Failed pulling workflows for {repo_name}: {e}")
                workflows = []
                
            for w in workflows:
                w_id = w["id"]
                w_name = w["name"]
                
                # Mock targeting behavior (typically obtained from parsing workflow YAML syntax trees)
                node = TopologyNode(
                    repoId=repo_id,
                    repoName=repo_name,
                    workflowId=w_id,
                    workflowName=w_name,
                    environmentNames=["production"],
                    deploymentTargetId=1,
                    deploymentTargetType="environment",
                    deploymentTargetName="production",
                    linkageMethod="workflow-environment",
                    resourceNames=["kubernetes_cluster"]
                )
                nodes.append(node)
                
                runs.append(WorkflowRun(
                    repo_name=repo_name,
                    workflow_name=w_name,
                    target_env="production",
                    resource="kubernetes_cluster"
                ))
    
    # Write exports into topology map natively
    manager = ExportManager(base_dir=output_dir)
    archiver = TopologyArchiver(manager)
    archiver.export(nodes, runs)
    
    md_archiver = MarkdownArchiver(manager)
    md_archiver.export(nodes, runs)
    
    logger.info(f"Completed mapping topologies natively to {manager.base_path}")


@app.command("analyze-pipeline")
def analyze_pipeline(
    from_discovery: str = typer.Option(..., "--from-discovery", help="Path to discovery JSON"),
    output_dir: str = typer.Option("exports", "--output-dir", help="Base exports directory"),
    token: str = typer.Option(..., "--token", envvar="GH_TOKEN", help="GitHub Personal Access Token")
):
    """
    Crawls pipeline bounds translating the discovered repositories natively to DAG arrays and Arc42 graphs.
    """
    asyncio.run(
        execute_pipeline_analysis(
            from_discovery=from_discovery,
            output_dir=output_dir,
            token=token
        )
    )
