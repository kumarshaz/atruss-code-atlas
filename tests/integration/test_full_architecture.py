import json
import os
from pathlib import Path

import httpx
import pytest

from src.cli.commands.discover import execute_discovery


def _pets_workshop_mock_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/orgs/github-samples/repos":
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 8001,
                        "name": "pets-workshop",
                        "owner": {"login": "github-samples", "id": 99},
                        "default_branch": "main",
                        "clone_url": "https://github.com/github-samples/pets-workshop.git",
                        "ssh_url": "git@github.com:github-samples/pets-workshop.git",
                        "html_url": "https://github.com/github-samples/pets-workshop",
                        "size": 512,
                        "archived": False,
                        "private": False,
                        "pushed_at": "2026-01-10T00:00:00Z",
                        "language": "TypeScript",
                    },
                    {
                        "id": 8002,
                        "name": "unrelated-repo",
                        "owner": {"login": "github-samples", "id": 99},
                        "default_branch": "main",
                        "clone_url": "https://github.com/github-samples/unrelated-repo.git",
                        "language": "Python",
                    },
                ],
            )
        if request.url.path == "/repos/github-samples/pets-workshop/git/trees/main":
            return httpx.Response(
                200,
                json={
                    "sha": "49000790c260bf6ab84a833f0ece3bc91d2afbe0",
                    "tree": [
                        {"path": "frontend/package.json", "type": "blob"},
                        {"path": "frontend/src/App.tsx", "type": "blob"},
                        {"path": "backend/pyproject.toml", "type": "blob"},
                        {"path": "backend/app.py", "type": "blob"},
                        {"path": ".github/workflows/ci.yml", "type": "blob"},
                        {"path": "backend/Dockerfile", "type": "blob"},
                    ],
                },
            )
        return httpx.Response(404, json={"message": "Not Found"})

    return httpx.MockTransport(handler)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_architecture_integration_against_samples(tmp_path: Path):
    """
    Validates end-to-end discovery targeting `github-samples/pets-workshop`
    via live GH_TOKEN (when ATRUSS_LIVE_GH_TESTS=1) or deterministic httpx.MockTransport offline.
    """
    use_live = os.getenv("ATRUSS_LIVE_GH_TESTS") == "1" and bool(os.getenv("GH_TOKEN"))
    token = os.getenv("GH_TOKEN") if use_live else None
    transport = None if use_live else _pets_workshop_mock_transport()

    base_dir = tmp_path / "exports"
    log_dir = tmp_path / "logs"

    await execute_discovery(
        org="github-samples",
        token=token,
        base_dir=str(base_dir),
        log_dir=str(log_dir),
        include_archived=False,
        max_concurrent=1,
        exclude_repo_names=[],
        exclude_repo_patterns=["^(?!pets-workshop$).*"],
        dry_run=False,
        transport=transport,
    )

    json_path = base_dir / "latest" / "repos" / "repositories.json"
    csv_path = base_dir / "latest" / "repos" / "repositories.csv"

    assert json_path.exists(), "Integration: Discovery JSON envelope missing"
    assert csv_path.exists(), "Integration: Discovery CSV matrix missing"

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    items = payload.get("items", [])
    assert len(items) == 1
    assert items[0]["RepositoryName"] == "pets-workshop"
    assert items[0]["PrimaryLanguage"] != "Unknown"
