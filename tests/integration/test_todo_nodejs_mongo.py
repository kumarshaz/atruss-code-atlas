import os
from src.cli.commands.analyze_pipeline import _analyze_repo_workflows
from tests.utils.fixture_manager import FixtureManager
from pathlib import Path

def test_todo_nodejs_mongo_parsing(tmp_path):
    """Integrates against the todo-nodejs-mongo-terraform public repository mapping complex Terraform CI/CD."""
    repo_url = "https://github.com/Azure-Samples/todo-nodejs-mongo-terraform.git"
    pinned_sha = "96d9c797122d5c1c30af19f22ddbd6bee42e19de"
    
    with FixtureManager.clone_pinned_fixture(repo_url, pinned_sha) as repo_dir:
        # Run the core logic bound natively
        artifact = _analyze_repo_workflows(Path(repo_dir), "todo-nodejs-mongo-terraform")
        
        # Verify the unified artifact natively dumps correctly
        assert artifact.repository == "todo-nodejs-mongo-terraform"
        assert artifact.sha == pinned_sha
        
        # Ensure that recursive pipeline sweeping caught workflows
        pipeline_names = [p.name for p in artifact.pipelines]
        assert len(pipeline_names) > 0
        assert any("terraform" in name.lower() or "azure" in name.lower() for name in pipeline_names)
