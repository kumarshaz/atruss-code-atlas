from pathlib import Path
import json
import os
import subprocess
import typer

from src.analyzers.code.orchestrator import orchestrate_deep_analysis
from src.core.utils.git_cloner import GitCloner
from src.models.artifacts import PortableArtifact
from src.core.utils.json_exporter import JSONExporter
from src.core.utils.markdown_exporter import MarkdownExporter

app = typer.Typer()

def _get_git_sha(repo_dir: Path) -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"

def _analyze_repo_code(repo_dir: Path, repo_name: str) -> PortableArtifact:
    sha = _get_git_sha(repo_dir)
    components = orchestrate_deep_analysis(repo_dir)
    
    # We serialize the generic components down natively into the unified portable struct
    return PortableArtifact(
        repository=repo_name,
        sha=sha,
        ecosystem="UNKNOWN",
        metrics={},
        pipelines=[],
        architecture_components=[{"name": c.name, "type": c.type, "dependencies": list(c.dependencies)} for c in components]
    )

@app.command("analyze-code")
def analyze_code(
    repo_path: str | None = typer.Option(None, "--path", help="Local repository path to analyze"),
    output_dir: str | None = typer.Option(None, "--output-dir", help="Directory to save Arc42 markdown"),
    from_discovery: str | None = typer.Option(None, "--from-discovery", help="Path to discovery JSON manifest"),
    repos_file: str | None = typer.Option(None, "--repos-file", help="Path to text document containing line separated repo targets"),
    token: str | None = typer.Option(None, "--token", help="GitHub Personal Access Token for cloning")
):
    """Performs deep architectural code scanning exporting strictly offline artifacts."""
    
    if not repo_path and not from_discovery and not repos_file:
        typer.echo("Error: Must provide either --path, --from-discovery, or --repos-file", err=True)
        raise typer.Exit(1)

    artifacts: list[PortableArtifact] = []

    targets_to_process = []

    if from_discovery:
        if not os.path.exists(from_discovery):
            raise typer.Exit(1)
        with open(from_discovery, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for item in manifest:
            if item.get("clone_url") and item.get("name"):
                targets_to_process.append({"url": item["clone_url"], "name": item["name"]})
                
    elif repos_file:
        if not os.path.exists(repos_file):
            raise typer.Exit(1)
        with open(repos_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        for line in lines:
            targets_to_process.append({"url": f"https://github.com/{line}.git", "name": line})
            
    if targets_to_process:
        typer.echo(f"Loaded {len(targets_to_process)} repositories.")
        for item in targets_to_process:
            clone_url = item["url"]
            name = item["name"]
            typer.echo(f"\nProcessing {name}...")
            with GitCloner.clone_temporarily(clone_url, token) as repo_dir_str:
                if repo_dir_str:
                    artifact = _analyze_repo_code(Path(repo_dir_str), name)
                    artifacts.append(artifact)
    else:
        repo_dir = Path(repo_path) # type: ignore
        artifacts.append(_analyze_repo_code(repo_dir, repo_dir.name))

    if output_dir:
        json_exporter = JSONExporter(output_dir)
        md_exporter = MarkdownExporter(output_dir)
        for art in artifacts:
            json_exporter.export(art)
            md_exporter.export(art)
        typer.echo(f"\nReports saved to {output_dir}")
    else:
        typer.echo("Analysis complete. Provide --output-dir to save portable outputs.")

if __name__ == "__main__":
    app()
