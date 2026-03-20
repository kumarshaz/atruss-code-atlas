from unittest.mock import patch
from src.core.utils.git_cloner import GitCloner

def test_inject_credentials_with_token():
    url = "https://github.com/org/repo.git"
    token = "ghp_12345"
    secure_url = GitCloner._inject_credentials(url, token)
    assert secure_url == "https://x-access-token:ghp_12345@github.com/org/repo.git"

def test_inject_credentials_without_token():
    url = "https://github.com/org/repo.git"
    secure_url = GitCloner._inject_credentials(url, None)
    assert secure_url == "https://github.com/org/repo.git"

def test_inject_credentials_already_has_credentials():
    url = "https://user:pass@github.com/org/repo.git"
    token = "ghp_12345"
    secure_url = GitCloner._inject_credentials(url, token)
    assert secure_url == url

@patch("subprocess.run")
def test_clone_temporarily_yields_dir(mock_run):
    """Test git cloner yields isolated temp path and executes clone natively."""
    mock_run.return_value = None
    with GitCloner.clone_temporarily("https://github.com/test", "token") as repo_dir:
        assert repo_dir is not None
        assert "atruss_code_atlas" in repo_dir
    mock_run.assert_called_once()
