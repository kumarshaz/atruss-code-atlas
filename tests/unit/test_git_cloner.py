import os
from unittest.mock import patch

import pytest

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
    """Test git cloner yields isolated temp path and executes shallow blobless clone."""
    mock_run.return_value = None
    captured_dir: str | None = None
    with GitCloner.clone_temporarily("https://github.com/test", "token") as repo_dir:
        assert repo_dir is not None
        assert "atruss_code_atlas" in repo_dir
        assert os.path.exists(repo_dir)
        captured_dir = repo_dir

    assert captured_dir is not None
    assert not os.path.exists(captured_dir)
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert "--depth" in cmd
    assert "--filter=blob:none" in cmd
    assert "--single-branch" in cmd


@patch("subprocess.run")
def test_clone_temporarily_cleans_up_on_error(mock_run):
    """Ensure temporary directory is wiped even if analysis raises inside context."""
    mock_run.return_value = None
    captured_dir: str | None = None
    with (
        pytest.raises(RuntimeError, match="boom"),
        GitCloner.clone_temporarily("https://github.com/test") as repo_dir,
    ):
        captured_dir = repo_dir
        assert captured_dir is not None and os.path.exists(captured_dir)
        raise RuntimeError("boom")

    assert captured_dir is not None
    assert not os.path.exists(captured_dir)
