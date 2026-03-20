from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from src.cli.commands.analyze_pipeline import app

runner = CliRunner()

@patch("src.cli.commands.analyze_pipeline.GitCloner.clone_temporarily")
@patch("src.cli.commands.analyze_pipeline._analyze_repo_workflows")
def test_cli_repos_file_parsing(mock_analyze, mock_clone, tmp_path):
    """Unit contract test ensuring --repos-file arrays are parsed without relying on network cloning."""
    repos_file = tmp_path / "targets.txt"
    repos_file.write_text("org/repo1\norg/repo2")
    
    # Mock the cloner to just return a dummy directory string
    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = str(tmp_path)
    mock_clone.return_value = mock_ctx
    
    # Mock the analyzer to return a valid artifact
    from src.models.artifacts import PortableArtifact
    mock_analyze.return_value = PortableArtifact(
        repository="dummy", sha="abc", ecosystem="UNKNOWN", metrics={}, pipelines=[], architecture_components=[]
    )
    
    result = runner.invoke(app, [
        "--repos-file", str(repos_file)
    ])
    
    assert result.exit_code == 0
    assert "Loaded 2 repositories." in result.stdout
    assert "Processing org/repo1" in result.stdout
    assert "Processing org/repo2" in result.stdout
    
    # Ensure clone was called exactly 2 times
    assert mock_clone.call_count == 2
