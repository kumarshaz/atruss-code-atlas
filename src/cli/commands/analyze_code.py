import json
import os
import subprocess
from pathlib import Path

import typer

from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.core.utils.export_manager import ExportManager
from src.core.utils.git_cloner import GitCloner
from src.core.utils.json_exporter import JSONExporter
from src.core.utils.markdown_exporter import MarkdownExporter
from src.models.artifacts import PortableArtifact

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


def _analyze_repo_code(repo_dir: Path, repo_name: str) -> PortableArtifact:
    sha = _get_git_sha(repo_dir)
    analysis = orchestrate_full_analysis(repo_dir)

    return PortableArtifact(
        repository=repo_name,
        sha=sha,
        ecosystem=analysis.ecosystem,
        metrics={**analysis.metrics, "framework": analysis.framework},
        pipelines=[],
        architecture_components=analysis.components,
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
    repo_path: str | None = typer.Option(None, "--path", help="Local repository path to analyze"),
    output_dir: str | None = typer.Option(
        None, "--output-dir", help="Directory to save standalone JSON/Markdown reports"
    ),
    exports_dir: str = typer.Option(
        "exports", "--exports-dir", help="Archival exports base directory (for Astro UI)"
    ),
    from_discovery: str | None = typer.Option(
        None, "--from-discovery", help="Path to discovery JSON manifest"
    ),
    repos_file: str | None = typer.Option(
        None, "--repos-file", help="Path to text document containing line-separated repo targets"
    ),
    token: str | None = typer.Option(
        None, "--token", envvar="GH_TOKEN", help="GitHub Personal Access Token for cloning"
    ),
):
    """Performs deep architectural code scanning exporting strictly offline artifacts."""
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
                    artifact = _analyze_repo_code(Path(repo_dir_str), item["name"])
                    processed.append((item["org"], item["repo"], artifact))
    else:
        local_dir = Path(repo_path)  # type: ignore[arg-type]
        if not local_dir.exists():
            typer.echo(f"Error: Local path not found: {repo_path}", err=True)
            raise typer.Exit(1)
        artifact = _analyze_repo_code(local_dir, local_dir.name)
        processed.append(("local", local_dir.name, artifact))

    # Always export into archival exports/{timestamp}/reports/ and sync exports/latest/ for Astro
    manager = ExportManager(base_dir=exports_dir)
    reports_dir = str(manager.base_path / "reports")
    archival_md = MarkdownExporter(reports_dir)
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
    manager.publish_to_latest(modules=["reports"])

    if output_dir:
        json_exporter = JSONExporter(output_dir)
        md_exporter = MarkdownExporter(output_dir)
        for _org, _repo, art in processed:
            json_exporter.export(art)
            md_exporter.export(art, include_frontmatter=True)
        typer.echo(f"\nReports saved to {output_dir}")
    else:
        typer.echo(f"Analysis complete. Archival reports saved to {manager.base_path / 'reports'}")


if __name__ == "__main__":
    app()
