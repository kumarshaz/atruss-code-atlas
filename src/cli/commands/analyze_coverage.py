import json
from pathlib import Path

import typer

from src.analyzers.coverage_parser import analyze_coverage_report

app = typer.Typer()

@app.command("analyze-coverage")
def analyze_coverage(
    report_path: str = typer.Option(..., "--report", help="Path to the test coverage report artifact")
):
    """Extracts code coverage metrics from test runner artifacts."""

    path = Path(report_path)
    if not path.exists() or not path.is_file():
        typer.echo(f"Report file {report_path} not found.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Analyzing coverage artifact: {path.name}...")

    try:
        metrics = analyze_coverage_report(path)
        typer.echo("\n--- Coverage Summary ---")
        typer.echo(json.dumps(metrics, indent=2))
    except Exception as e:
        typer.echo(f"Error parsing coverage report: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
