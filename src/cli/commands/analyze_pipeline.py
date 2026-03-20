import json
from pathlib import Path

import typer

from src.analyzers.pipeline.dag_builder import build_workflow_dag, get_dag_metrics
from src.analyzers.pipeline.heuristics import find_missing_caches, find_untested_deployments
from src.analyzers.pipeline.parser import parse_workflow_yaml

app = typer.Typer()

@app.command("analyze-pipeline")
def analyze_pipeline(
    repo_path: str = typer.Option(..., "--repo", help="Local repository path containing code"),
    output_dir: str | None = typer.Option(None, "--output-dir", help="Directory to save report JSON")
):
    """Analyzes CI/CD pipelines (GitHub Actions) for anti-patterns and builds a DAG."""

    repo_dir = Path(repo_path)
    workflows_dir = repo_dir / ".github" / "workflows"

    if not workflows_dir.exists() or not workflows_dir.is_dir():
        typer.echo(f"No .github/workflows directory found in {repo_path}.", err=True)
        return

    all_findings = []
    all_metrics = {}

    for yaml_file in workflows_dir.glob("*.yml"):
        workflow_name = yaml_file.name
        typer.echo(f"Analyzing {workflow_name}...")

        with open(yaml_file, encoding="utf-8") as f:
            content = f.read()

        workflow_data = parse_workflow_yaml(content)
        if not workflow_data:
            typer.echo(f"Failed to parse {workflow_name} or it is empty.")
            continue

        dag = build_workflow_dag(workflow_data)
        metrics = get_dag_metrics(dag)
        all_metrics[workflow_name] = metrics

        findings = []
        findings.extend(find_untested_deployments(dag))
        findings.extend(find_missing_caches(workflow_data))

        if findings:
            all_findings.append({
                "workflow": workflow_name,
                "findings": findings
            })
            for issue in findings:
                typer.echo(f"  - {issue}", err=True)

    report = {
        "repository": repo_path,
        "metrics": all_metrics,
        "anti_patterns": all_findings
    }

    if output_dir:
        out_path = Path(output_dir) / "pipeline_report.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        typer.echo(f"\nReport saved to: {out_path}")
    else:
        typer.echo("\n--- Pipeline Analysis Report ---")
        typer.echo(json.dumps(report, indent=2))

if __name__ == "__main__":
    app()
