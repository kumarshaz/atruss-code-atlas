from pathlib import Path

import pytest

from src.cli.commands.analyze_code import _analyze_repo_code
from src.cli.commands.analyze_pipeline import _analyze_repo_workflows
from tests.utils.fixture_manager import FixtureManager


@pytest.mark.integration
@pytest.mark.e2e
def test_pets_workshop_parsing():
    """Clones pinned github-samples/pets-workshop and validates structural ecosystem & pipeline extraction."""
    repo_url = "https://github.com/github-samples/pets-workshop.git"
    pinned_sha = "49000790c260bf6ab84a833f0ece3bc91d2afbe0"

    with FixtureManager.clone_pinned_fixture(repo_url, pinned_sha) as repo_dir:
        repo_path = Path(repo_dir)
        artifact = _analyze_repo_code(repo_path, "pets-workshop")
        pipe_artifact = _analyze_repo_workflows(repo_path, "pets-workshop")

        assert artifact.repository == "pets-workshop"
        assert artifact.sha == pinned_sha
        assert artifact.ecosystem != "Unknown"
        assert len(artifact.architecture_components) > 0
        assert artifact.metrics["files_analyzed"] > 0
        assert pipe_artifact.repository == "pets-workshop"
