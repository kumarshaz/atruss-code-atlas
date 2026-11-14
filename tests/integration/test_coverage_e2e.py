from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.analyzers.coverage_parser import analyze_coverage_report
from src.cli.commands.analyze_coverage import app as coverage_app


@pytest.mark.integration
def test_tr_ana_coverage_extraction_and_cli_e2e(tmp_path: Path):
    """TR-ANA E2E: validates pytest-cov summary, JaCoCo XML, unknown fallback, and CLI invocation."""
    pytest_txt = tmp_path / "pytest_cov.txt"
    pytest_txt.write_text(
        "Name                 Stmts   Miss  Cover\n"
        "----------------------------------------\n"
        "src/app.py             100     12    88%\n"
        "TOTAL                  100     12    88%\n",
        encoding="utf-8",
    )

    py_metrics = analyze_coverage_report(pytest_txt)
    assert py_metrics["runner"] == "pytest-cov"
    assert py_metrics["coverage_percent"] == 88.0

    jacoco_xml = tmp_path / "jacoco.xml"
    jacoco_xml.write_text(
        '<?xml version="1.0" ?>'
        "<report name='core'>"
        '<counter type="INSTRUCTION" missed="10" covered="90"/>'
        "</report>",
        encoding="utf-8",
    )

    java_metrics = analyze_coverage_report(jacoco_xml)
    assert java_metrics["runner"] == "jacoco"
    assert java_metrics["coverage_percent"] == 90.0

    unknown_txt = tmp_path / "empty.txt"
    unknown_txt.write_text("no coverage data", encoding="utf-8")
    assert analyze_coverage_report(unknown_txt)["runner"] == "unknown"

    runner = CliRunner()
    res = runner.invoke(
        coverage_app,
        ["--report", str(pytest_txt)],
    )
    assert res.exit_code == 0, res.output
    assert "88.0" in res.output
