from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from src.cli.commands.analyze_pipeline import app

runner = CliRunner()

@patch("src.cli.commands.analyze_pipeline.GitCloner.clone_temporarily")
@patch("src.cli.commands.analyze_pipeline._analyze_repo_workflows")
def test_cli_repos_file_parsing(mock_analyze, mock_clone, tmp_path):
    """Unit contract test ensuring --repos-file arrays parse without network cloning."""
    repos_file = tmp_path / "targets.txt"
    repos_file.write_text("org/repo1\norg/repo2")

    # Mock the cloner to just return a dummy directory string
    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = str(tmp_path)
    mock_clone.return_value = mock_ctx

    # Mock the analyzer to return a valid artifact
    from src.models.artifacts import PortableArtifact

    mock_analyze.return_value = PortableArtifact(
        repository="dummy",
        sha="abc",
        ecosystem="UNKNOWN",
        metrics={},
        pipelines=[],
        architecture_components=[],
    )

    out_dir = tmp_path / "exports"
    result = runner.invoke(app, [
        "--repos-file", str(repos_file),
        "--output-dir", str(out_dir),
    ])

    assert result.exit_code == 0
    assert "Loaded 2 repositories." in result.stdout
    assert "Processing org/repo1" in result.stdout
    assert "Processing org/repo2" in result.stdout

    # Ensure clone was called exactly 2 times
    assert mock_clone.call_count == 2


def test_cli_dot_path_resolves_repo_name(tmp_path, monkeypatch):
    """Ensure `--path .` resolves directory basename cleanly instead of empty `local-` slugs."""
    from src.cli.commands.analyze_code import app as code_app

    repo_dir = tmp_path / "sample-dot-repo"
    (repo_dir / ".github" / "workflows").mkdir(parents=True)
    (repo_dir / "pyproject.toml").write_text(
        "[project]\nname='sample-dot-repo'\n", encoding="utf-8"
    )
    (repo_dir / "app.py").write_text("def hello():\n    return 'ok'\n", encoding="utf-8")
    (repo_dir / ".github" / "workflows" / "ci.yml").write_text(
        "name: Dot CI\non: [push]\npermissions:\n  contents: read\njobs:\n"
        "  test:\n    runs-on: ubuntu-latest\n    timeout-minutes: 5\n"
        "    steps:\n      - run: pytest\n",
        encoding="utf-8",
    )

    exports_dir = tmp_path / "exports"
    monkeypatch.chdir(repo_dir)

    res_code = runner.invoke(
        code_app,
        ["--path", ".", "--exports-dir", str(exports_dir), "--no-sbom"],
    )
    assert res_code.exit_code == 0, res_code.output
    res_pipe = runner.invoke(app, ["--path", ".", "--output-dir", str(exports_dir)])
    assert res_pipe.exit_code == 0, res_pipe.output

    latest = exports_dir / "latest"
    assert (latest / "reports" / "local-sample-dot-repo-analysis.json").exists()
    assert (latest / "reports" / "local-sample-dot-repo-report.md").exists()
    assert (latest / "pipelines" / "local-sample-dot-repo-pipeline.json").exists()
    assert not (latest / "reports" / "local--analysis.json").exists()
    assert not (latest / "pipelines" / "local--pipeline.json").exists()

