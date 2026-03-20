from pathlib import Path

import typer

from src.analyzers.code.orchestrator import orchestrate_deep_analysis
from src.core.services.report_generator import generate_arc42_markdown

app = typer.Typer()

@app.command("analyze-code")
def analyze_code(
    repo_path: str = typer.Option(..., "--path", help="Local repository path to analyze"),
    output_dir: str | None = typer.Option(None, "--output-dir", help="Directory to save Arc42 markdown")
):
    """Performs deep architectural code scanning using abstract syntax trees."""

    repo_dir = Path(repo_path)
    if not repo_dir.exists() or not repo_dir.is_dir():
        typer.echo(f"Directory {repo_path} does not exist.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Starting deep analysis of {repo_dir.name}...")

    components = orchestrate_deep_analysis(repo_dir)

    typer.echo(f"Found {len(components)} architectural components.")

    markdown = generate_arc42_markdown(repo_dir.name, components)

    if output_dir:
        out_path = Path(output_dir) / f"{repo_dir.name}_arc42.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        typer.echo(f"Report saved to: {out_path}")
    else:
        typer.echo("\n--- Arc42 Document ---")
        typer.echo(markdown)

if __name__ == "__main__":
    app()
