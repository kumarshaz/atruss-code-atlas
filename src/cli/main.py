import typer

from src.cli.commands.analyze_code import app as code_app
from src.cli.commands.analyze_coverage import app as coverage_app
from src.cli.commands.analyze_pipeline import app as pipeline_app
from src.cli.commands.benchmark import app as benchmark_app
from src.cli.commands.check import app as check_app
from src.cli.commands.diff import app as diff_app
from src.cli.commands.discover import app as discover_app
from src.cli.commands.mcp_server import app as mcp_app

app = typer.Typer(
    name="atruss",
    help="Repository Discovery and Deep Analysis Tool",
    add_completion=False,
)

app.add_typer(discover_app)
app.add_typer(pipeline_app)
app.add_typer(code_app)
app.add_typer(coverage_app)
app.add_typer(benchmark_app)
app.add_typer(check_app)
app.add_typer(diff_app)
app.add_typer(mcp_app)


@app.command()
def version():
    """Print the version of the application."""
    typer.echo("atruss version 0.1.0")


if __name__ == "__main__":
    app()
