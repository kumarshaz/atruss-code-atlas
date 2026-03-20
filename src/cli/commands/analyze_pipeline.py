import json
import os
import subprocess
from pathlib import Path

import typer

from src.analyzers.pipeline.dag_builder import build_workflow_dag, get_dag_metrics
from src.analyzers.pipeline.heuristics import find_missing_caches, find_untested_deployments
from src.analyzers.pipeline.parser import parse_workflow_yaml
from src.core.utils.git_cloner import GitCloner
from src.models.artifacts import PortableArtifact, PipelineWorkflow
from src.core.utils.json_exporter import JSONExporter
from src.core.utils.markdown_exporter import MarkdownExporter

app = typer.Typer()

def _get_git_sha(repo_dir: Path) -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"

def _analyze_repo_workflows(repo_dir: Path, repo_name: str) -> PortableArtifact:
    workflows_dir = repo_dir / ".github" / "workflows"
    sha = _get_git_sha(repo_dir)
    
    artifact = PortableArtifact(
        repository=repo_name,
        sha=sha,
        ecosystem="UNKNOWN",
        metrics={},
        pipelines=[],
        architecture_components=[]
    )
    
    if not workflows_dir.exists() or not workflows_dir.is_dir():
        typer.echo(f"No .github/workflows directory found in {repo_name}.", err=True)
        return artifact

    for yaml_file in workflows_dir.rglob("*.yml"):
        workflow_name = yaml_file.name
        typer.echo(f"  Analyzing {workflow_name}...")
        with open(yaml_file, encoding="utf-8") as f:
            content = f.read()
            
        workflow_data = parse_workflow_yaml(content)
        if not workflow_data:
            continue
            
        dag = build_workflow_dag(workflow_data)
        metrics = get_dag_metrics(dag)
        
        findings = []
        findings.extend(find_untested_deployments(dag))
        findings.extend(find_missing_caches(workflow_data))
        
        pl = PipelineWorkflow(name=workflow_name, jobs=workflow_data.get("jobs", {}), dag_metrics=metrics, findings=findings)
        artifact.pipelines.append(pl)

    return artifact

@app.command("analyze-pipeline")
def analyze_pipeline(
    repo_path: str | None = typer.Option(None, "--repo", help="Local repository path containing code"),
    output_dir: str | None = typer.Option(None, "--output-dir", help="Directory to save explicit CLI reports"),
    from_discovery: str | None = typer.Option(None, "--from-discovery", help="Path to discovery JSON manifest"),
    repos_file: str | None = typer.Option(None, "--repos-file", help="Path to text document containing line separated repo targets"),
    token: str | None = typer.Option(None, "--token", help="GitHub PAT")
):
    """Analyzes CI/CD pipelines natively generating portable Docs-as-Code bounds without database."""
    
    if not repo_path and not from_discovery and not repos_file:
        typer.echo("Error: Must provide either --repo, --from-discovery, or --repos-file", err=True)
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
                    artifact = _analyze_repo_workflows(Path(repo_dir_str), name)
                    artifacts.append(artifact)
    else:
        repo_dir = Path(repo_path) # type: ignore
        artifacts.append(_analyze_repo_workflows(repo_dir, repo_dir.name))

    if output_dir:
        json_exporter = JSONExporter(output_dir)
        md_exporter = MarkdownExporter(output_dir)
        for art in artifacts:
            out_json = json_exporter.export(art)
            out_md = md_exporter.export(art)
            typer.echo(f"\nSaved Portable Assets for {art.repository}\n  -> {out_json}\n  -> {out_md}")
    else:
        typer.echo("Analysis complete. Provide --output-dir to save portable output states natively.")

if __name__ == "__main__":
    app()
