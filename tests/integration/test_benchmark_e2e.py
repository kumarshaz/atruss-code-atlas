import asyncio
import json
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from typer.testing import CliRunner

from src.cli.commands.benchmark import sample_random_repositories
from src.cli.main import app


def _init_git_repo(repo_dir: Path, files: dict[str, str]) -> str:
    """Create a real git repository on disk with an initial commit and return its HEAD SHA."""
    repo_dir.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        target = repo_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    subprocess.run(["git", "init", "-b", "main"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "atruss@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Atruss"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, check=True, capture_output=True)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_dir, text=True).strip()
    return sha


@pytest.mark.integration
def test_benchmark_cli_corpus_and_broken_yaml_resilience(tmp_path: Path):
    """
    E2E benchmark slice test verifying 4-ecosystem corpus execution via `atruss benchmark`,
    malformed workflow resilience, Astro export creation, and deterministic `--replay`.
    """
    repos_root = tmp_path / "remotes"
    py_repo = repos_root / "acme" / "py-svc"
    ts_repo = repos_root / "acme" / "web-ui"

    py_sha = _init_git_repo(
        py_repo,
        {
            "pyproject.toml": "[project]\nname='py-svc'\n",
            "src/api.py": (
                "from fastapi import APIRouter\n"
                "router = APIRouter()\n"
                "@router.get('/v1')\n"
                "def v1(): return {}\n"
            ),
            ".github/workflows/ci.yml": (
                "name: Py CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
                "    steps:\n      - uses: actions/setup-python@v5\n"
                "        with:\n          cache: pip\n"
                "      - run: pytest\n"
            ),
            # Deliberately malformed workflow file alongside valid workflow
            ".github/workflows/broken.yml": "jobs:\n  bad: [unterminated\n",
        },
    )
    ts_sha = _init_git_repo(
        ts_repo,
        {
            "package.json": '{"name": "web-ui", "dependencies": {"react": "^18.0.0"}}\n',
            "src/App.tsx": "export function App() { return null; }\n",
            ".github/workflows/web.yml": (
                "name: Web CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n"
                "    steps:\n      - run: npm ci && npm test\n"
            ),
        },
    )

    corpus_file = tmp_path / "mini_corpus.json"
    corpus_file.write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "org": "acme",
                        "name": "py-svc",
                        "full_name": "acme/py-svc",
                        "url": py_repo.as_uri(),
                        "clone_url": py_repo.as_uri(),
                        "expected_ecosystem": "Python",
                        "ecosystem_key": "python",
                        "pinned_ref": "main",
                        "pinned_sha": py_sha,
                    },
                    {
                        "org": "acme",
                        "name": "web-ui",
                        "full_name": "acme/web-ui",
                        "url": ts_repo.as_uri(),
                        "clone_url": ts_repo.as_uri(),
                        "expected_ecosystem": "JavaScript/TypeScript",
                        "ecosystem_key": "react_ts_js",
                        "pinned_ref": "main",
                        "pinned_sha": ts_sha,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    exports_dir = tmp_path / "exports"
    runner = CliRunner()
    res = runner.invoke(
        app,
        [
            "benchmark",
            "--corpus",
            str(corpus_file),
            "--output-dir",
            str(exports_dir),
            "--log-path",
            str(tmp_path / "logs"),
            "--max-concurrent",
            "2",
        ],
    )
    assert res.exit_code == 0, res.output

    latest = exports_dir / "latest"
    summary = json.loads((latest / "benchmark_summary.json").read_text(encoding="utf-8"))
    assert summary["total_repos"] == 2
    assert summary["completed_repos"] == 2
    assert summary["classification_accuracy_pct"] == 100.0
    assert (latest / "pipelines" / "acme-py-svc-pipeline.json").exists()
    assert (latest / "pipelines" / "acme-web-ui-pipeline.json").exists()
    assert (latest / "reports" / "acme-py-svc-report.md").exists()
    assert (latest / "reports" / "acme-web-ui-report.md").exists()

    # Deterministic replay via benchmark_manifest.json
    replay_exports = tmp_path / "replay_exports"
    res2 = runner.invoke(
        app,
        [
            "benchmark",
            "--replay",
            str(latest / "benchmark_manifest.json"),
            "--output-dir",
            str(replay_exports),
            "--log-path",
            str(tmp_path / "logs"),
        ],
    )
    assert res2.exit_code == 0, res2.output
    replay_summary = json.loads(
        (replay_exports / "latest" / "benchmark_summary.json").read_text(encoding="utf-8")
    )
    assert replay_summary["total_repos"] == 2
    assert [r["resolved_sha"] for r in replay_summary["results"]] == [py_sha, ts_sha]


@pytest.mark.integration
def test_random_sample_replay_cli_e2e(tmp_path: Path):
    """Test `--random-sample` via mocked GitHub Search API followed by CLI `--replay`."""
    local_repo = tmp_path / "remotes" / "randorg" / "demo-api"
    sha = _init_git_repo(
        local_repo,
        {
            "pom.xml": "<project><artifactId>demo</artifactId></project>\n",
            "src/main/java/App.java": "@SpringBootApplication\npublic class App {}\n",
        },
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/search/repositories":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "full_name": "randorg/demo-api",
                            "html_url": "https://github.com/randorg/demo-api",
                            "clone_url": local_repo.as_uri(),
                            "default_branch": "main",
                            "size": 512,
                            "stargazers_count": 1500,
                            "archived": False,
                            "sha": sha,
                        }
                    ]
                },
            )
        return httpx.Response(404)

    sampled = asyncio.run(
        sample_random_repositories(
            count=1,
            seed=7,
            ecosystem="java_springboot",
            transport=httpx.MockTransport(handler),
        )
    )
    assert len(sampled) == 1

    exports_dir = tmp_path / "exports"
    runner = CliRunner()
    with patch(
        "src.cli.commands.benchmark.sample_random_repositories",
        new=AsyncMock(return_value=sampled),
    ):
        res = runner.invoke(
            app,
            [
                "benchmark",
                "--random-sample",
                "1",
                "--seed",
                "7",
                "--output-dir",
                str(exports_dir),
                "--log-path",
                str(tmp_path / "logs"),
            ],
        )
    assert res.exit_code == 0, res.output
    manifest_file = exports_dir / "latest" / "benchmark_manifest.json"
    assert manifest_file.exists()
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest_data["seed"] == 7
    assert manifest_data["entries"][0]["pinned_sha"] == sha
