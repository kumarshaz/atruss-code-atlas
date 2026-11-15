from __future__ import annotations

import json
from pathlib import Path

import typer

from src.analyzers.drift import compute_drift_report, render_drift_markdown
from src.core.utils.export_manager import ExportManager

app = typer.Typer()


_BASELINE_OPT = typer.Option(
    ..., "--baseline", help="Baseline archival export snapshot directory"
)
_TARGET_OPT = typer.Option(
    ..., "--target", help="Target archival export snapshot directory"
)
_OUTPUT_DIR_OPT = typer.Option(
    None, "--output-dir", help="Optional directory to write drift_report.{json,md}"
)
_EXPORTS_DIR_OPT = typer.Option(
    "exports", "--exports-dir", help="Archival exports base directory"
)
_FAIL_ON_REG_OPT = typer.Option(
    False,
    "--fail-on-regression",
    help="Exit with status code 1 if architectural, pipeline, or scorecard regressions occur",
)


@app.command("diff")
def diff(
    baseline: Path = _BASELINE_OPT,
    target: Path = _TARGET_OPT,
    output_dir: Path | None = _OUTPUT_DIR_OPT,
    exports_dir: str = _EXPORTS_DIR_OPT,
    fail_on_regression: bool = _FAIL_ON_REG_OPT,
) -> None:
    """
    Compare two archival export snapshots (baseline vs. target) and emit
    drift_report.json and drift_report.md (FR-027).
    """
    if not baseline.exists():
        typer.echo(f"Error: Baseline directory not found: {baseline}", err=True)
        raise typer.Exit(1)
    if not target.exists():
        typer.echo(f"Error: Target directory not found: {target}", err=True)
        raise typer.Exit(1)

    report = compute_drift_report(baseline, target)
    md_text = render_drift_markdown(report)
    json_text = json.dumps(report, indent=2) + "\n"

    manager = ExportManager(base_dir=exports_dir)
    json_arch = manager.get_path("drift", "drift_report.json")
    md_arch = manager.get_path("drift", "drift_report.md")
    json_arch.write_text(json_text, encoding="utf-8")
    md_arch.write_text(md_text, encoding="utf-8")
    manager.publish_to_latest(modules=["drift"])

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "drift_report.json").write_text(json_text, encoding="utf-8")
        (output_dir / "drift_report.md").write_text(md_text, encoding="utf-8")

    summary = report["summary"]
    typer.echo(
        f"Drift diff completed: regressions={summary['regressions_count']}, "
        f"new_antipatterns={summary['new_antipatterns_count']}, "
        f"new_fitness_violations={summary['new_fitness_violations_count']}."
    )

    if fail_on_regression and report["has_regression"]:
        typer.echo("Drift gate failed: architectural or scorecard regressions detected.", err=True)
        raise typer.Exit(1)
