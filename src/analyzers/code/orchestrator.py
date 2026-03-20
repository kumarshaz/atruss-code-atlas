from pathlib import Path

import typer

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.python_ast import analyze_python_ast


def orchestrate_deep_analysis(repo_dir: Path):
    """Determines ecosystem and routes to the appropriate AST parser, or gracefully skips."""

    all_files = []
    for f in repo_dir.rglob("*"):
        if f.is_file() and ".git" not in f.parts and "node_modules" not in f.parts and ".venv" not in f.parts:
            all_files.append(str(f.relative_to(repo_dir)))

    classification = classify_repository(all_files[:1000])

    if classification.ecosystem == Ecosystem.PYTHON:
        typer.echo("Python ecosystem detected. Running Python AST analysis...")
        return analyze_python_ast(repo_dir)
    elif classification.ecosystem in [Ecosystem.DOTNET, Ecosystem.JAVA_SPRINGBOOT, Ecosystem.REACT_TS_JS]:
        typer.echo(f"Ecosystem {classification.ecosystem.value} detected.")
        typer.echo("Graceful Skip: Strict AST mapping for this ecosystem is scheduled for a future release.")
        return []
    else:
        typer.echo("Unsupported ecosystem for deep architecture scan. Skipping gracefully.")
        return []
