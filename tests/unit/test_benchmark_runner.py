import asyncio
import json
import os
import re
import tempfile
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest
from typer.testing import CliRunner

from scripts.curate_corpus import DEFAULT_CORPUS_PATH, validate_corpus_data
from src.cli.commands.benchmark import (
    execute_benchmark,
    load_replay_entries,
    sample_random_repositories,
    select_corpus_entries,
)
from src.cli.main import app
from src.models.benchmark import BenchmarkManifest, CorpusEntry


def test_popular_100_corpus_schema_and_balance():
    """Verify 100-repo catalog passes schema, 25x4 stratification, and SLA limits."""
    assert DEFAULT_CORPUS_PATH.exists()
    data = json.loads(DEFAULT_CORPUS_PATH.read_text(encoding="utf-8"))
    errors = validate_corpus_data(data)
    assert errors == []

    counts = data["ecosystem_counts"]
    assert counts == {
        "python": 25,
        ".net": 25,
        "react_ts_js": 25,
        "java_springboot": 25,
    }
    for repo in data["repositories"]:
        assert repo["estimated_size_mb"] < 250.0
        assert repo["estimated_loc"] < 500000
        assert repo["url"].startswith("https://github.com/")
        assert repo["clone_url"].endswith(".git")


def test_select_corpus_entries_stratified_limit():
    """Verify --limit 12 without --ecosystem selects 3 repos from each of the 4 ecosystems."""
    selected = select_corpus_entries(DEFAULT_CORPUS_PATH, limit=12)
    assert len(selected) == 12
    by_eco: dict[str, int] = {}
    for entry in selected:
        by_eco[entry.ecosystem_key] = by_eco.get(entry.ecosystem_key, 0) + 1
    assert by_eco == {
        "python": 3,
        ".net": 3,
        "react_ts_js": 3,
        "java_springboot": 3,
    }

    py_only = select_corpus_entries(DEFAULT_CORPUS_PATH, ecosystem="python", limit=5)
    assert len(py_only) == 5
    assert all(e.ecosystem_key == "python" for e in py_only)


@pytest.mark.asyncio
async def test_sample_random_repositories_deterministic_seed():
    """Verify Search sampler stratifies star buckets and respects deterministic seed."""
    recorded_queries: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/search/repositories":
            q = request.url.params.get("q", "")
            recorded_queries.append(q)
            lang = "Python"
            if "C#" in q:
                lang = "CSharp"
            elif "TypeScript" in q:
                lang = "TypeScript"
            elif "Java" in q:
                lang = "Java"

            bucket = "mid"
            stars = 2500
            if "100..1000" in q:
                bucket = "low"
                stars = 350
            elif ">10000" in q:
                bucket = "high"
                stars = 25000

            items = [
                {
                    "full_name": f"sample-org/{lang.lower()}-{bucket}-{idx}",
                    "html_url": f"https://github.com/sample-org/{lang.lower()}-{bucket}-{idx}",
                    "clone_url": f"https://github.com/sample-org/{lang.lower()}-{bucket}-{idx}.git",
                    "default_branch": "main",
                    "size": 10240,
                    "stargazers_count": stars,
                    "archived": False,
                    "sha": f"sha_{lang}_{bucket}_{idx}",
                }
                for idx in range(3)
            ]
            return httpx.Response(200, json={"total_count": len(items), "items": items})
        return httpx.Response(404, json={"message": "Not Found"})

    run1 = await sample_random_repositories(
        count=12,
        seed=2026,
        transport=httpx.MockTransport(handler),
    )
    run2 = await sample_random_repositories(
        count=12,
        seed=2026,
        transport=httpx.MockTransport(handler),
    )

    assert len(run1) == 12
    assert [e.full_name for e in run1] == [e.full_name for e in run2]
    assert {e.ecosystem_key for e in run1} == {"python", ".net", "react_ts_js", "java_springboot"}
    assert {e.star_tier for e in run1} == {"100..1000", "1000..10000", ">10000"}
    assert any("stars:100..1000" in q for q in recorded_queries)
    assert any("stars:1000..10000" in q for q in recorded_queries)
    assert any("stars:>10000" in q for q in recorded_queries)


@pytest.mark.asyncio
async def test_execute_benchmark_circuit_breaker_and_anomaly_capture(tmp_path: Path):
    """
    Verify slow/failing repos trigger timeout/failure anomaly isolation without crashing
    healthy repos in the same batch, leaving zero temp dirs behind.
    """
    good_repo = tmp_path / "good-py"
    (good_repo / ".github" / "workflows").mkdir(parents=True)
    (good_repo / "pyproject.toml").write_text("[project]\nname='good-py'\n", encoding="utf-8")
    (good_repo / "app.py").write_text(
        "from fastapi import FastAPI\napp = FastAPI()\n"
        "@app.get('/ok')\ndef ok(): return {'ok': True}\n",
        encoding="utf-8",
    )
    (good_repo / ".github" / "workflows" / "ci.yml").write_text(
        "name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - run: pytest\n",
        encoding="utf-8",
    )

    entries = [
        CorpusEntry(
            org="acme",
            name="good-py",
            full_name="acme/good-py",
            url="https://github.com/acme/good-py",
            clone_url="https://github.com/acme/good-py.git",
            expected_ecosystem="Python",
            ecosystem_key="python",
        ),
        CorpusEntry(
            org="acme",
            name="slow-repo",
            full_name="acme/slow-repo",
            url="https://github.com/acme/slow-repo",
            clone_url="https://github.com/acme/slow-repo.git",
            expected_ecosystem="Python",
            ecosystem_key="python",
        ),
    ]

    async def resolver(entry: CorpusEntry) -> Path | None:
        if entry.name == "good-py":
            return good_repo
        return None

    class _SlowProc:
        returncode = None

        async def communicate(self):
            await asyncio.sleep(2.0)
            return b"", b""

        def kill(self):
            self.returncode = -9

        async def wait(self):
            return -9

    async def slow_create_subprocess(*args, **kwargs):
        return _SlowProc()

    exports_dir = tmp_path / "exports"
    temp_root = Path(tempfile.gettempdir()) / "atruss_code_atlas"
    before_dirs = set(os.listdir(temp_root)) if temp_root.exists() else set()

    with patch(
        "src.core.utils.git_cloner.asyncio.create_subprocess_exec",
        side_effect=slow_create_subprocess,
    ):
        summary, anomalies, latest_dir = await execute_benchmark(
            entries=entries,
            mode="corpus",
            output_dir=str(exports_dir),
            log_dir=str(tmp_path / "logs"),
            max_concurrent=2,
            timeout=0.15,
            local_repo_resolver=resolver,
        )

    after_dirs = set(os.listdir(temp_root)) if temp_root.exists() else set()
    assert after_dirs == before_dirs

    assert summary.total_repos == 2
    assert summary.completed_repos == 1
    assert summary.timeout_repos == 1
    assert any(a.stage == "timeout" and a.repo == "acme/slow-repo" for a in anomalies)

    assert (latest_dir / "benchmark_summary.json").exists()
    assert (latest_dir / "benchmark_summary.md").exists()
    assert (latest_dir / "anomalies.json").exists()
    assert (latest_dir / "benchmark_manifest.json").exists()
    assert (latest_dir / "repos" / "repositories.json").exists()
    assert (latest_dir / "pipelines" / "acme-good-py-pipeline.json").exists()
    assert (latest_dir / "reports" / "acme-good-py-report.md").exists()
    assert (latest_dir / "reports" / "acme-good-py-analysis.json").exists()

    # Verify --replay works against both benchmark_manifest.json and anomalies.json
    manifest_entries, _ = load_replay_entries(latest_dir / "benchmark_manifest.json")
    assert len(manifest_entries) == 2

    anomaly_entries, _ = load_replay_entries(latest_dir / "anomalies.json")
    assert [e.full_name for e in anomaly_entries] == ["acme/slow-repo"]

    # Validate BenchmarkManifest Pydantic round-trip
    manifest = BenchmarkManifest.model_validate_json(
        (latest_dir / "benchmark_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest.total_entries == 2


def test_benchmark_cli_registered():
    """Verify `atruss benchmark --help` is wired in the root CLI app."""
    runner = CliRunner()
    res = runner.invoke(
        app,
        ["benchmark", "--help"],
        env={"NO_COLOR": "1", "TERM": "dumb", "COLUMNS": "120"},
    )
    assert res.exit_code == 0
    plain_stdout = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", res.stdout)
    assert "--corpus" in plain_stdout
    assert "--random-sample" in plain_stdout
    assert "--replay" in plain_stdout


@pytest.mark.asyncio
async def test_github_client_search_rate_limit_scales_threshold():
    """Verify unauthenticated Search API (limit=10, remaining=9) does not stall for 60s."""
    from src.core.http_client import GitHubClient

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={
                "x-ratelimit-limit": "10",
                "x-ratelimit-remaining": "9",
                "x-ratelimit-reset": "9999999999",
            },
            json={"items": []},
        )

    async with GitHubClient(transport=httpx.MockTransport(handler)) as client:
        data = await asyncio.wait_for(client.get("/search/repositories"), timeout=2.0)
        assert data == {"items": []}
