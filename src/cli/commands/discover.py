import asyncio
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import typer

from src.analyzers.classification import classify_repository
from src.core.auth import setup_secure_logging, validate_token
from src.core.exporters.discovery_exporter import DiscoveryArchiver
from src.core.http_client import GitHubClient
from src.core.utils.export_manager import ExportManager
from src.models.discovery import DiscoveryManifestItem

app = typer.Typer()


async def _analyze_discovered_repo(
    client: GitHubClient,
    org: str,
    repo: dict[str, Any],
    analyzed_date: str,
    logger: Any,
) -> DiscoveryManifestItem:
    name = repo["name"]
    owner = repo.get("owner", {}).get("login") or org
    default_branch = repo.get("default_branch") or "main"

    file_paths: list[str] = []
    truncated = False
    try:
        if hasattr(client, "get_repo_tree_with_status"):
            file_paths, _, truncated = await client.get_repo_tree_with_status(
                owner, name, ref=default_branch
            )
        else:
            file_paths, _ = await client.get_repo_tree(owner, name, ref=default_branch)
            truncated = bool(getattr(client, "last_tree_truncated", False))
    except Exception as exc:
        logger.debug(f"Could not fetch git tree for {owner}/{name}: {exc}")

    fallback_lang = repo.get("language") or "Unknown"
    if truncated:
        logger.warning(
            f"Tree truncated for {owner}/{name}; falling back gracefully using "
            f"{len(file_paths)} partial paths and GitHub language='{fallback_lang}'."
        )
    cls_result = classify_repository(file_paths, fallback_language=fallback_lang)

    primary_language = (
        cls_result.display_language
        if cls_result.display_language != "Unknown"
        else fallback_lang
    )

    return DiscoveryManifestItem(
        Organization=org,
        Project=org,
        ProjectId=str(repo.get("owner", {}).get("id", "")),
        RepositoryName=name,
        RepositoryId=str(repo.get("id", "")),
        DefaultBranch=default_branch,
        CloneUrl=repo.get("clone_url", ""),
        SshUrl=repo.get("ssh_url", ""),
        WebUrl=repo.get("html_url", ""),
        Size=repo.get("size", 0),
        IsDisabled=repo.get("archived", False),
        IsPrivate=repo.get("private", False),
        LastUpdate=repo.get("updated_at") or repo.get("pushed_at") or "",
        PrimaryLanguage=primary_language,
        FrameworkType=cls_result.framework,
        AllFrameworks="; ".join(cls_result.all_frameworks),
        DeployableTypes="; ".join(cls_result.deployable_types),
        HasAPI=cls_result.signals.get("HasAPI", False),
        HasService=cls_result.signals.get("HasService", False),
        HasFrontend=cls_result.signals.get("HasFrontend", False),
        HasDatabase=cls_result.signals.get("HasDatabase", False),
        TechnologyStack=cls_result.technology_stack,
        HasDockerfile=cls_result.signals.get("HasDockerfile", False),
        HasPipeline=cls_result.signals.get("HasPipeline", False),
        HasKubernetes=cls_result.signals.get("HasKubernetes", False),
        DocumentationPriority=cls_result.documentation_priority,
        AnalyzedDate=analyzed_date,
    )


async def execute_discovery(
    org: str,
    base_dir: str,
    log_dir: str,
    include_archived: bool,
    max_concurrent: int,
    exclude_repo_names: list[str],
    exclude_repo_patterns: list[str],
    dry_run: bool,
    token: str | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
):
    log_path = Path(log_dir) / "discovery.log"
    logger = setup_secure_logging(log_path, token)

    logger.info(f"Starting discovery for org: {org}")
    if dry_run:
        logger.info("DRY RUN ENABLED - No exports will be written")

    async with GitHubClient(
        token=token, max_concurrent=max_concurrent, logger=logger, transport=transport
    ) as client:
        if transport is None:
            await validate_token(client, org, logger)

        logger.info("Fetching repository list...")
        try:
            repos = await client.get_paginated(f"/orgs/{org}/repos")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                logger.info(f"Org '{org}' not found; falling back to /users/{org}/repos")
                repos = await client.get_paginated(f"/users/{org}/repos")
            else:
                raise

        filtered_repos: list[dict[str, Any]] = []
        for r in repos:
            name = r["name"]
            if not include_archived and r.get("archived", False):
                logger.debug(f"Skipping archived repo: {name}")
                continue
            if name in exclude_repo_names:
                logger.debug(f"Skipping explicitly excluded repo: {name}")
                continue
            if any(re.search(pat, name) for pat in exclude_repo_patterns):
                logger.debug(f"Skipping repo {name} matching exclusion regex")
                continue
            filtered_repos.append(r)

        filtered_repos.sort(key=lambda r: r["name"].lower())
        analyzed_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        tasks = [
            _analyze_discovered_repo(client, org, r, analyzed_date, logger)
            for r in filtered_repos
        ]
        processed_items: list[DiscoveryManifestItem] = list(await asyncio.gather(*tasks))

        logger.info(f"Validated {len(processed_items)} repositories matching filter criteria.")

        if not dry_run:
            manager = ExportManager(base_dir=base_dir)
            archiver = DiscoveryArchiver(manager)
            archiver.export(processed_items)
            manager.publish_to_latest(modules=["repos"])
            logger.info(
                f"Successfully exported strictly formatted datasets to: {manager.base_path}"
            )


@app.command("discover")
def discover(
    org: str = typer.Option(..., "--org", help="GitHub organization or user name"),
    token: str | None = typer.Option(
        None,
        "--token",
        envvar="GH_TOKEN",
        help="GitHub Personal Access Token (Optional)",
    ),
    output_path: str = typer.Option(
        "exports",
        "--output-path",
        help="Directory to save the exports",
    ),
    log_path: str = typer.Option(
        "logs",
        "--log-path",
        help="Directory to save secure execution logs",
    ),
    include_archived: bool = typer.Option(
        False,
        "--include-archived",
        help="Include archived repositories",
    ),
    max_concurrent: int = typer.Option(
        10,
        "--max-concurrent",
        help="Max concurrent connections",
    ),
    exclude_names: str = typer.Option(
        "",
        "--exclude-repo-names",
        help="Comma-separated repo names to exclude",
    ),
    exclude_patterns: str = typer.Option(
        "",
        "--exclude-repo-patterns",
        help="Comma-separated regex patterns to exclude",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate without writing files"),
):
    """
    Extract multi-phase repository discovery datasets deterministically.
    """
    names_list = [n.strip() for n in exclude_names.split(",") if n.strip()]
    patterns_list = [p.strip() for p in exclude_patterns.split(",") if p.strip()]

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
            dry_run=dry_run,
        )
    )
