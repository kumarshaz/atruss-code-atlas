import pytest
import os
from pathlib import Path
from src.cli.commands.discover import execute_discovery

@pytest.mark.asyncio
async def test_full_architecture_integration_against_samples(tmp_path: Path):
    """
    T018: Upholds Constitution VII by targeting the actual `github-samples/pets-workshop` baseline
    ensuring discovery structures operate effectively without crashing.
    """
    token = os.getenv("GH_TOKEN", "mock_token")
    if token == "mock_token":
        pytest.skip("Skipping active integration hit because GH_TOKEN is not injected in test environment.")
    
    # We will enforce a full extraction against `github-samples`
    # We mock or use dry-run to ensure we don't spam the API with real tokens during CI
    
    base_dir = tmp_path / "exports"
    log_dir = tmp_path / "logs"
    
    # Run the raw async executor against the github-samples org filtering only for pets-workshop
    await execute_discovery(
        org="github-samples",
        token=token,
        base_dir=str(base_dir),
        log_dir=str(log_dir),
        include_archived=False,
        max_concurrent=1,
        exclude_repo_names=[],
        exclude_repo_patterns=["^(?!pets-workshop$).*"], # exclude everything except pets-workshop
        dry_run=False
    )
    
    # The `exports` folder should contain the payloads
    json_path = base_dir / "repos" / "repositories.json"
    csv_path = base_dir / "repos" / "repositories.csv"
    
    assert json_path.exists(), "Integration: Discovery JSON envelope missing"
    assert csv_path.exists(), "Integration: Discovery CSV matrix missing"
