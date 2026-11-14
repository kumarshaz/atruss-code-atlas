import pytest
from typer.testing import CliRunner
from src.cli.main import app

runner = CliRunner()

def test_atruss_version():
    """Verify that the CLI command is named atruss and returns the correct version."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "atruss version" in result.stdout

def test_atruss_app_name():
    """Verify the app name is strictly atruss."""
    assert app.info.name == "atruss"
