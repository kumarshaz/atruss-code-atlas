import os
from pathlib import Path
from typer.testing import CliRunner
from src.cli.commands.analyze_pipeline import app

runner = CliRunner()

def test_array_sourcing_success(tmp_path):
    """Test passing --repos-file parsing flat text arrays sequentially."""
    repos_file = tmp_path / "targets.txt"
    repos_file.write_text("github-samples/pets-workshop\nAzure-Samples/todo-nodejs-mongo-terraform")

    # Note: actually running the full typre execution to completion will take ~10secs for 2 clones.
    # We will trigger the Typer CLI ensuring the repos file is picked up and output-dir is dumped natively.
    out_dir = tmp_path / "reports"
    
    result = runner.invoke(app, [
        "--repos-file", str(repos_file),
        "--output-dir", str(out_dir)
    ])
    
    assert result.exit_code == 0
    assert "Loaded 2 repositories" in result.stdout
    assert "Processing github-samples/pets-workshop..." in result.stdout
    assert "Processing Azure-Samples/todo-nodejs-mongo-terraform..." in result.stdout
    
    # Assert artifacts dumped statically into the output dir
    files = list(out_dir.glob("*.json"))
    assert len(files) == 2
