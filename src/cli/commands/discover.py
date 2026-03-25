import asyncio
import re
from pathlib import Path
from typing import Optional

import typer

from src.core.http_client import GitHubClient
from src.core.auth import validate_token, setup_secure_logging
from src.core.utils.export_manager import ExportManager
from src.core.exporters.discovery_exporter import DiscoveryArchiver
from src.models.discovery import DiscoveryManifestItem

app = typer.Typer()

async def execute_discovery(
    org: str,
    base_dir: str,
    log_dir: str,
    include_archived: bool,
    max_concurrent: int,
    exclude_repo_names: list[str],
    exclude_repo_patterns: list[str],
    dry_run: bool,
    token: Optional[str] = None
):
    log_path = Path(log_dir) / "discovery.log"
    logger = setup_secure_logging(log_path, token)
    
    logger.info(f"Starting discovery for org: {org}")
    if dry_run:
        logger.info("DRY RUN ENABLED - No exports will be written")

    async with GitHubClient(token=token, max_concurrent=max_concurrent, logger=logger) as client:
        await validate_token(client, org, logger)
        
        logger.info("Fetching repository list...")
        repos = await client.get_paginated(f"/orgs/{org}/repos")
        
        # Filtering
        processed_items = []
        for r in repos:
            name = r["name"]
            if not include_archived and r.get("archived", False):
                logger.debug(f"Skipping archived repo: {name}")
                continue
                
            if name in exclude_repo_names:
                logger.debug(f"Skipping explicitly excluded repo: {name}")
                continue
                
            skip_pattern = False
            for pat in exclude_repo_patterns:
                if re.match(pat, name):
                    logger.debug(f"Skipping repo {name} matching regex: {pat}")
                    skip_pattern = True
                    break
            if skip_pattern:
                continue
                
            item = DiscoveryManifestItem(
                Organization=org,
                Project=org,
                ProjectId=str(r.get("owner", {}).get("id", "")),
                RepositoryName=name,
                RepositoryId=str(r.get("id", "")),
                DefaultBranch=r.get("default_branch", "main"),
                CloneUrl=r.get("clone_url", ""),
                SshUrl=r.get("ssh_url", ""),
                WebUrl=r.get("html_url", ""),
                Size=r.get("size", 0),
                IsDisabled=r.get("archived", False),
                IsPrivate=r.get("private", False),
                LastUpdate=r.get("updated_at", ""),
                PrimaryLanguage=r.get("language") or "Unknown",
                FrameworkType="Unknown",
                AllFrameworks="",
                DeployableTypes="",
                HasAPI=False,
                HasService=False,
                HasFrontend=False,
                HasDatabase=False,
                TechnologyStack=r.get("language") or "Unknown",
                HasDockerfile=False,
                HasPipeline=False,
                HasKubernetes=False,
                DocumentationPriority="P3",
                AnalyzedDate=""
            )
            processed_items.append(item)
            
        logger.info(f"Validated {len(processed_items)} repositories matching filter criteria.")
        
        if not dry_run:
            manager = ExportManager(base_dir=base_dir)
            archiver = DiscoveryArchiver(manager)
            archiver.export(processed_items)
            logger.info(f"Successfully exported strictly formatted datasets to: {manager.base_path}")


@app.command("discover")
def discover(
    org: str = typer.Option(..., "--org", help="GitHub organization name"),
    token: Optional[str] = typer.Option(None, "--token", envvar="GH_TOKEN", help="GitHub Personal Access Token (Optional for public)"),
    output_path: str = typer.Option("exports", "--output-path", help="Directory to save the exports"),
    log_path: str = typer.Option("logs", "--log-path", help="Directory to save secure execution logs"),
    include_archived: bool = typer.Option(False, "--include-archived", help="Include archived repositories"),
    max_concurrent: int = typer.Option(10, "--max-concurrent", help="Max concurrent connections"),
    exclude_names: str = typer.Option("", "--exclude-repo-names", help="Comma separated list of repo names to exclude"),
    exclude_patterns: str = typer.Option("", "--exclude-repo-patterns", help="Comma separated list of regex patterns to exclude"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate without writing files")
):
    """
    Perform a multi-phase structural parity extraction of GitHub repositories into deterministic datasets.
    """
    names_list = [n.strip() for n in exclude_names.split(",")] if exclude_names else []
    patterns_list = [p.strip() for p in exclude_patterns.split(",")] if exclude_patterns else []
    
    asyncio.run(
        execute_discovery(
            org=org,
            token=token,
            base_dir=output_path,
            log_dir=log_path,
            include_archived=include_archived,
            max_concurrent=max_concurrent,
            exclude_repo_names=names_list,
            exclude_repo_patterns=patterns_list,
            dry_run=dry_run
        )
    )
