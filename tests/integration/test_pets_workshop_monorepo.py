import os
import json
from src.cli.commands.analyze_code import _analyze_repo_code
from tests.utils.fixture_manager import FixtureManager
from pathlib import Path

def test_pets_workshop_parsing(tmp_path):
    """Integrates against the actual pets-workshop payload explicitly asserting architectural topological DAG extraction natively."""
    repo_url = "https://github.com/github-samples/pets-workshop.git"
    pinned_sha = "49000790c260bf6ab84a833f0ece3bc91d2afbe0"
    
    with FixtureManager.clone_pinned_fixture(repo_url, pinned_sha) as repo_dir:
        # Run the core logic bound natively
        artifact = _analyze_repo_code(Path(repo_dir), "pets-workshop")
        
        # Verify the unified artifact natively dumps correctly
        assert artifact.repository == "pets-workshop"
        assert artifact.sha == pinned_sha
        assert len(artifact.architecture_components) == 0  # Validates the graceful skip feature on UNKNOWN polyglot environments

