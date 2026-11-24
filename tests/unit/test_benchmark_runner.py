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
    """Verify curated production corpus passes schema, multi-ecosystem coverage, and URL checks."""
    assert DEFAULT_CORPUS_PATH.exists()
    data = json.loads(DEFAULT_CORPUS_PATH.read_text(encoding="utf-8"))
    errors = validate_corpus_data(data)
    assert errors == []

    counts = data["ecosystem_counts"]
    assert data["total"] >= 100
    for key in ("python", ".net", "react_ts_js", "java_springboot", "go", "rust"):
        assert counts.get(key, 0) >= 1
    for repo in data["repositories"]:
        assert repo["estimated_size_mb"] > 0.0
        assert repo["estimated_loc"] > 0
        assert repo["url"].startswith("https://github.com/")
        assert repo["clone_url"].endswith(".git")


def test_select_corpus_entries_stratified_limit():
    """Verify --limit 12 without --ecosystem selects stratified entries across ecosystems."""
    selected = select_corpus_entries(DEFAULT_CORPUS_PATH, limit=12)
    assert len(selected) == 12
    by_eco: dict[str, int] = {}
    for entry in selected:
        by_eco[entry.ecosystem_key] = by_eco.get(entry.ecosystem_key, 0) + 1
    for key in ("python", ".net", "react_ts_js", "java_springboot"):
        assert by_eco.get(key, 0) >= 1

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
    assert "--checkpoint-dir" in plain_stdout
    assert "--resume" in plain_stdout
    assert "--isolated" in plain_stdout
    assert "--live-osv" in plain_stdout
    assert "--diff-baseline" in plain_stdout
    assert "--diff-previous" in plain_stdout


@pytest.mark.asyncio
async def test_benchmark_checkpoint_and_resume(tmp_path: Path):
    """Verify per-repo checkpointing writes JSON files and skips re-analysis on resume."""
    repo_dir = tmp_path / "py_app"
    repo_dir.mkdir()
    (repo_dir / "requirements.txt").write_text("fastapi==0.110.0\n", encoding="utf-8")
    (repo_dir / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n")

    entries = [
        CorpusEntry(
            org="acme",
            name="py-app",
            full_name="acme/py-app",
            url="https://github.com/acme/py-app",
            clone_url="https://github.com/acme/py-app.git",
            ecosystem_key="python",
            expected_ecosystem="Python",
            star_tier="1000..10000",
        )
    ]

    calls = 0

    def resolver(_entry: CorpusEntry) -> Path:
        nonlocal calls
        calls += 1
        return repo_dir

    ckpt_dir = tmp_path / "checkpoints"
    summary1, _, _ = await execute_benchmark(
        entries=entries,
        mode="corpus",
        output_dir=str(tmp_path / "exports1"),
        log_dir=str(tmp_path / "logs"),
        checkpoint_dir=ckpt_dir,
        resume=True,
        local_repo_resolver=resolver,
    )
    assert calls == 1
    assert summary1.completed_repos == 1
    assert len(list(ckpt_dir.glob("*.json"))) == 1

    # Second run with resume=True should load from checkpoint without calling resolver
    summary2, _, latest_dir2 = await execute_benchmark(
        entries=entries,
        mode="corpus",
        output_dir=str(tmp_path / "exports2"),
        log_dir=str(tmp_path / "logs"),
        checkpoint_dir=ckpt_dir,
        resume=True,
        local_repo_resolver=resolver,
    )
    assert calls == 1
    assert summary2.completed_repos == 1
    assert (latest_dir2 / "reports" / "acme-py-app-analysis.json").exists()


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


def test_daily_repos_manifest_schema_and_live_head_tracking():
    """Verify manifests/daily-repos.json validates via CorpusEntry and omits pinned_sha."""
    daily_path = Path("manifests/daily-repos.json")
    assert daily_path.exists()
    data = json.loads(daily_path.read_text(encoding="utf-8"))
    entries = select_corpus_entries(daily_path)
    assert len(entries) == data["total"] == len(data["repositories"]) >= 1
    assert len({e.full_name for e in entries}) == len(entries)
    assert all(e.pinned_sha is None for e in entries)
    for e in entries:
        assert e.url.startswith("https://github.com/")
        assert e.clone_url.endswith(".git")


@pytest.mark.asyncio
async def test_execute_benchmark_live_osv_org_summary_and_diff_previous(tmp_path: Path):
    """
    Verify execute_benchmark wires live OSV into analysis/SBOM/SARIF/orgs-summary.json
    and generates drift_report.{json,md} when diff_previous=True.
    """
    repo_dir = tmp_path / "vuln-py"
    (repo_dir / ".github" / "workflows").mkdir(parents=True)
    (repo_dir / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")
    (repo_dir / "app.py").write_text(
        "def ping(ok):\n    return 1 if ok else 0\n",
        encoding="utf-8",
    )
    (repo_dir / ".github" / "workflows" / "ci.yml").write_text(
        "name: CI\non:\n  push:\n    branches: [main]\n"
        "permissions:\n  contents: read\n"
        "jobs:\n  test:\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n"
        "    steps:\n      - run: pytest\n",
        encoding="utf-8",
    )

    entries = [
        CorpusEntry(
            org="acme",
            name="vuln-py",
            full_name="acme/vuln-py",
            url="https://github.com/acme/vuln-py",
            clone_url="https://github.com/acme/vuln-py.git",
            ecosystem_key="python",
            expected_ecosystem="Python",
            pinned_sha=None,
        )
    ]

    def osv_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/querybatch":
            return httpx.Response(
                200,
                json={
                    "results": [
                        {
                            "vulns": [
                                {
                                    "id": "GHSA-test-requests-001",
                                    "aliases": ["CVE-2026-99999"],
                                    "summary": "Mocked test advisory for benchmark live OSV wiring",
                                    "database_specific": {"severity": "HIGH"},
                                }
                            ]
                        }
                    ]
                },
            )
        return httpx.Response(404, json={})

    exports_root = tmp_path / "exports"

    # First offline run populates baseline exports/latest and orgs-summary.json
    _, _, latest1 = await execute_benchmark(
        entries=entries,
        mode="corpus",
        output_dir=str(exports_root),
        log_dir=str(tmp_path / "logs"),
        local_repo_resolver=lambda _e: repo_dir,
        enable_live_osv=False,
    )
    orgs1 = json.loads((latest1 / "orgs-summary.json").read_text(encoding="utf-8"))
    assert len(orgs1) == 1
    assert orgs1[0]["org"] == "acme"
    assert orgs1[0]["open_cves"] == 0

    # Second run enables live OSV + diff_previous and compares against first run
    _, _, latest2 = await execute_benchmark(
        entries=entries,
        mode="corpus",
        output_dir=str(exports_root),
        log_dir=str(tmp_path / "logs"),
        local_repo_resolver=lambda _e: repo_dir,
        enable_live_osv=True,
        osv_transport=httpx.MockTransport(osv_handler),
        diff_previous=True,
    )

    analysis = json.loads(
        (latest2 / "reports" / "acme-vuln-py-analysis.json").read_text(encoding="utf-8")
    )
    assert len(analysis["vulnerabilities"]) == 1
    assert analysis["vulnerabilities"][0]["id"] == "GHSA-test-requests-001"

    sbom = json.loads((latest2 / "sbom" / "acme-vuln-py.cdx.json").read_text(encoding="utf-8"))
    assert len(sbom.get("vulnerabilities", [])) == 1

    sarif = json.loads(
        (latest2 / "sarif" / "acme-vuln-py.sarif.json").read_text(encoding="utf-8")
    )
    assert any(
        "GHSA-test-requests-001" in res.get("message", {}).get("text", "")
        for run in sarif["runs"]
        for res in run.get("results", [])
    )

    orgs2 = json.loads((latest2 / "orgs-summary.json").read_text(encoding="utf-8"))
    assert orgs2[0]["open_cves"] == 1

    drift_json_path = latest2 / "drift" / "drift_report.json"
    drift_md_path = latest2 / "drift" / "drift_report.md"
    assert drift_json_path.exists()
    assert drift_md_path.exists()
    drift_data = json.loads(drift_json_path.read_text(encoding="utf-8"))
    assert drift_data["has_regression"] is True
    assert drift_data["summary"]["new_vulnerabilities_count"] == 1


@pytest.mark.asyncio
async def test_benchmark_subprocess_worker_propagates_live_osv_and_cache(tmp_path: Path):
    """Verify --isolated subprocess worker receives enable_live_osv and reads osv_cache_path."""
    from src.analyzers.dependencies.manifest_parser import build_purl
    from src.cli.commands.benchmark import _run_single_repo_subprocess

    cache_file = tmp_path / "osv_cache.json"
    purl = build_purl("pypi", "requests", "2.31.0")
    cache_file.write_text(
        json.dumps(
            {
                purl: [
                    {
                        "id": "GHSA-cache-isolated-01",
                        "aliases": [],
                        "summary": "Cached advisory verified inside subprocess worker",
                        "database_specific": {"severity": "CRITICAL"},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    repo_dir = tmp_path / "sub-repo"
    repo_dir.mkdir()
    (repo_dir / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")
    (repo_dir / "app.py").write_text("def hello(): return 'hi'\n", encoding="utf-8")

    entry = CorpusEntry(
        org="acme",
        name="sub-repo",
        full_name="acme/sub-repo",
        url=repo_dir.as_uri(),
        clone_url=repo_dir.as_uri(),
        ecosystem_key="python",
        expected_ecosystem="Python",
    )

    # Create local git commit so GitCloner clones cleanly in subprocess
    import subprocess

    subprocess.run(["git", "init", "-b", "main"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=repo_dir, check=True, capture_output=True
    )
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, check=True, capture_output=True)

    outcome = await _run_single_repo_subprocess(
        entry,
        semaphore=asyncio.Semaphore(1),
        timeout=30.0,
        token=None,
        analyzed_date="2026-11-18",
        enable_live_osv=True,
        osv_cache_path=cache_file,
    )
    art = outcome["code_artifact"]
    assert art is not None
    assert len(art.vulnerabilities) == 1
    assert art.vulnerabilities[0].id == "GHSA-cache-isolated-01"


def test_benchmark_cli_corpus_file_isolated_diff_previous(tmp_path: Path):
    """Verify `atruss benchmark --corpus-file --isolated --diff-previous` E2E CLI flags."""
    import subprocess

    repo_dir = tmp_path / "cli-repo"
    repo_dir.mkdir()
    (repo_dir / "pyproject.toml").write_text("[project]\nname='cli-repo'\n", encoding="utf-8")
    (repo_dir / "app.py").write_text("def run(x):\n    return 1 if x else 0\n", encoding="utf-8")
    subprocess.run(["git", "init", "-b", "main"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=repo_dir, check=True, capture_output=True
    )
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo_dir, check=True, capture_output=True)

    corpus_file = tmp_path / "daily.json"
    corpus_file.write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "org": "acme",
                        "name": "cli-repo",
                        "full_name": "acme/cli-repo",
                        "url": repo_dir.as_uri(),
                        "clone_url": repo_dir.as_uri(),
                        "ecosystem_key": "python",
                        "expected_ecosystem": "Python",
                        "pinned_ref": "main",
                        "pinned_sha": None,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    exports_dir = tmp_path / "exports"
    logs_dir = tmp_path / "logs"
    runner = CliRunner()

    first = runner.invoke(
        app,
        [
            "benchmark",
            "--corpus-file",
            str(corpus_file),
            "--output-dir",
            str(exports_dir),
            "--log-path",
            str(logs_dir),
            "--isolated",
            "--no-resume",
            "--no-live-osv",
            "--diff-previous",
        ],
    )
    assert first.exit_code == 0, first.stdout
    assert (exports_dir / "latest" / "orgs-summary.json").exists()
    assert not (exports_dir / "latest" / "drift" / "drift_report.json").exists()

    second = runner.invoke(
        app,
        [
            "benchmark",
            "--corpus-file",
            str(corpus_file),
            "--output-dir",
            str(exports_dir),
            "--log-path",
            str(logs_dir),
            "--isolated",
            "--no-resume",
            "--no-live-osv",
            "--diff-previous",
        ],
    )
    assert second.exit_code == 0, second.stdout
    assert (exports_dir / "latest" / "orgs-summary.json").exists()
    assert (exports_dir / "latest" / "drift" / "drift_report.json").exists()
    assert (exports_dir / "latest" / "drift" / "drift_report.md").exists()

    drift_data = json.loads(
        (exports_dir / "latest" / "drift" / "drift_report.json").read_text(encoding="utf-8")
    )
    assert "atruss_bench_prev_" not in drift_data["summary"]["baseline_dir"]
    assert drift_data["summary"]["baseline_dir"].endswith("latest (previous)")
    assert drift_data["summary"]["target_dir"].endswith("/latest")


@pytest.mark.asyncio
async def test_execute_benchmark_merge_latest_preserves_existing_repos(tmp_path: Path):
    """
    Verify `--merge-latest` (`clean_latest=False`) preserves untouched repos across
    repositories.json, reports, sbom, sarif, pipelines, topology, orgs-summary, and
    catalog-history while updating target repos cleanly with zero ghost removals in drift.
    """
    import subprocess

    def _make_git_repo(name: str, pkg_spec: str) -> Path:
        rdir = tmp_path / name
        (rdir / ".github" / "workflows").mkdir(parents=True)
        (rdir / "requirements.txt").write_text(pkg_spec, encoding="utf-8")
        (rdir / "app.py").write_text("def ok(x):\n    return 1 if x else 0\n", encoding="utf-8")
        (rdir / ".github" / "workflows" / "ci.yml").write_text(
            "name: CI\non:\n  push:\n    branches: [main]\n"
            "permissions:\n  contents: read\n"
            "jobs:\n  test:\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n"
            "    steps:\n      - run: pytest\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-b", "main"], cwd=rdir, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=rdir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"], cwd=rdir, check=True, capture_output=True
        )
        subprocess.run(["git", "add", "."], cwd=rdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=rdir, check=True, capture_output=True)
        return rdir

    repo_a_dir = _make_git_repo("alpha", "flask==3.0.0\n")
    repo_b_dir = _make_git_repo("beta", "requests==2.31.0\n")

    entry_a = CorpusEntry(
        org="org-a",
        name="alpha",
        full_name="org-a/alpha",
        url=repo_a_dir.as_uri(),
        clone_url=repo_a_dir.as_uri(),
        ecosystem_key="python",
        expected_ecosystem="Python",
    )
    entry_b = CorpusEntry(
        org="org-b",
        name="beta",
        full_name="org-b/beta",
        url=repo_b_dir.as_uri(),
        clone_url=repo_b_dir.as_uri(),
        ecosystem_key="python",
        expected_ecosystem="Python",
    )

    exports_dir = tmp_path / "exports"
    logs_dir = tmp_path / "logs"

    # Initial full export populates both org-a/alpha and org-b/beta
    _, _, latest1 = await execute_benchmark(
        entries=[entry_a, entry_b],
        mode="corpus",
        output_dir=str(exports_dir),
        log_dir=str(logs_dir),
        local_repo_resolver=lambda e: repo_a_dir if e.name == "alpha" else repo_b_dir,
        clean_latest=True,
    )
    first_pipe_b = json.loads((latest1 / "pipelines" / "org-b-beta-pipeline.json").read_text())

    # Merge-refresh ONLY org-b/beta with an injected OSV advisory
    def osv_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/querybatch":
            return httpx.Response(
                200,
                json={
                    "results": [
                        {
                            "vulns": [
                                {
                                    "id": "GHSA-merge-beta-01",
                                    "summary": "CVE found during incremental daily refresh",
                                    "database_specific": {"severity": "HIGH"},
                                }
                            ]
                        }
                    ]
                },
            )
        return httpx.Response(404, json={})

    _, _, latest2 = await execute_benchmark(
        entries=[entry_b],
        mode="corpus",
        output_dir=str(exports_dir),
        log_dir=str(logs_dir),
        local_repo_resolver=lambda _e: repo_b_dir,
        clean_latest=False,
        enable_live_osv=True,
        osv_transport=httpx.MockTransport(osv_handler),
        diff_previous=True,
    )

    # Untouched org-a/alpha remains intact across discovery, reports, SBOM, SARIF, and topology
    repos_payload = json.loads(
        (latest2 / "repos" / "repositories.json").read_text(encoding="utf-8")
    )
    assert repos_payload["count"] == 2
    assert {item["RepositoryId"] for item in repos_payload["items"]} == {
        "org-a/alpha",
        "org-b/beta",
    }
    assert (latest2 / "reports" / "org-a-alpha-analysis.json").exists()
    assert (latest2 / "sbom" / "org-a-alpha.cdx.json").exists()
    assert (latest2 / "sarif" / "org-a-alpha.sarif.json").exists()

    topo_json = json.loads(
        (latest2 / "relationships" / "pipeline_topology.json").read_text(encoding="utf-8")
    )
    assert {item["repoName"] for item in topo_json["items"]} == {"alpha", "beta"}

    # Unchanged workflow SHA preserves analyzed_at in merge mode
    second_pipe_b = json.loads((latest2 / "pipelines" / "org-b-beta-pipeline.json").read_text())
    assert second_pipe_b["analyzed_at"] == first_pipe_b["analyzed_at"]

    # Updated org-b/beta advisory reflected in orgs-summary, portfolio catalog-history, and drift
    orgs = json.loads((latest2 / "orgs-summary.json").read_text(encoding="utf-8"))
    by_org = {o["org"]: o for o in orgs}
    assert set(by_org.keys()) == {"org-a", "org-b"}
    assert by_org["org-b"]["open_cves"] == 1

    history = json.loads((latest2 / "catalog-history.json").read_text(encoding="utf-8"))
    assert history["snapshots"][-1]["repo_count"] == 2

    drift = json.loads((latest2 / "drift" / "drift_report.json").read_text(encoding="utf-8"))
    assert drift["summary"]["removed_repos_count"] == 0
    assert drift["summary"]["new_vulnerabilities_count"] == 1


def test_semantic_export_change_detector_filters_timestamp_noise(tmp_path: Path):
    """Verify scripts/has_semantic_export_changes.py ignores volatile timestamps only."""
    import subprocess

    from scripts.has_semantic_export_changes import has_semantic_export_changes

    repo = tmp_path / "repo"
    (repo / "exports" / "latest" / "repos").mkdir(parents=True)
    (repo / "exports" / "latest" / "drift").mkdir(parents=True)
    (repo / "exports" / "latest" / "repos" / "repositories.json").write_text(
        json.dumps(
            {
                "count": 1,
                "items": [
                    {
                        "Organization": "acme",
                        "RepositoryName": "app",
                        "LastUpdate": "2026-11-22T00:00:00Z",
                        "AnalyzedDate": "2026-11-22",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (repo / "exports" / "latest" / "benchmark_summary.json").write_text(
        json.dumps({"run_id": "2026-11-22_00-00-00"}), encoding="utf-8"
    )
    (repo / "exports" / "latest" / "drift" / "drift_report.json").write_text(
        json.dumps(
            {
                "summary": {
                    "baseline_dir": "exports/latest (previous)",
                    "new_vulnerabilities_count": 0,
                }
            }
        ),
        encoding="utf-8",
    )

    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo, check=True, capture_output=True)

    # Touch only volatile timestamps and zero-change drift report
    (repo / "exports" / "latest" / "repos" / "repositories.json").write_text(
        json.dumps(
            {
                "count": 1,
                "items": [
                    {
                        "Organization": "acme",
                        "RepositoryName": "app",
                        "LastUpdate": "2026-11-23T06:00:00Z",
                        "AnalyzedDate": "2026-11-23",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (repo / "exports" / "latest" / "benchmark_summary.json").write_text(
        json.dumps({"run_id": "2026-11-23_06-00-00"}), encoding="utf-8"
    )
    subprocess.run(
        ["git", "add", "-A", "exports/latest/"], cwd=repo, check=True, capture_output=True
    )
    assert has_semantic_export_changes(repo) is False

    # Introducing a new CVE in drift report triggers semantic change detection
    (repo / "exports" / "latest" / "drift" / "drift_report.json").write_text(
        json.dumps(
            {
                "summary": {
                    "baseline_dir": "exports/latest (previous)",
                    "new_vulnerabilities_count": 1,
                }
            }
        ),
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", "-A", "exports/latest/"], cwd=repo, check=True, capture_output=True
    )
    assert has_semantic_export_changes(repo) is True


def test_osv_cache_save_merges_concurrent_writes(tmp_path: Path):
    """Verify OSVBatchClient.save_cache preserves keys written by sibling workers."""
    from src.analyzers.dependencies.osv_client import OSVBatchClient

    cache_file = tmp_path / "shared_osv.json"
    c1 = OSVBatchClient(cache_path=cache_file)
    c2 = OSVBatchClient(cache_path=cache_file)

    c1.save_cache({"pkg:pypi/flask@3.0.0": [{"id": "GHSA-a"}]})
    c2.save_cache({"pkg:pypi/requests@2.31.0": [{"id": "GHSA-b"}]})

    loaded = json.loads(cache_file.read_text(encoding="utf-8"))
    assert set(loaded.keys()) == {"pkg:pypi/flask@3.0.0", "pkg:pypi/requests@2.31.0"}


@pytest.mark.asyncio
async def test_merge_latest_preserves_colliding_repo_name_topology(tmp_path: Path):
    """Verify refreshing `org-b/shared` keeps `org-a/shared` workflows in pipeline_topology."""
    import subprocess

    def _make_repo(dirname: str, wf_name: str) -> Path:
        rdir = tmp_path / dirname
        (rdir / ".github" / "workflows").mkdir(parents=True)
        (rdir / "app.py").write_text("def ok(): return 1\n", encoding="utf-8")
        (rdir / ".github" / "workflows" / "ci.yml").write_text(
            f"name: {wf_name}\non:\n  push:\n    branches: [main]\n"
            "permissions:\n  contents: read\n"
            "jobs:\n  test:\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n"
            "    steps:\n      - run: pytest\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-b", "main"], cwd=rdir, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=rdir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"], cwd=rdir, check=True, capture_output=True
        )
        subprocess.run(["git", "add", "."], cwd=rdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=rdir, check=True, capture_output=True)
        return rdir

    repo_a = _make_repo("a_shared", "AlphaWorkflow")
    repo_b = _make_repo("b_shared", "BetaWorkflow")
    entry_a = CorpusEntry(
        org="org-a",
        name="shared",
        full_name="org-a/shared",
        url=repo_a.as_uri(),
        clone_url=repo_a.as_uri(),
        ecosystem_key="python",
        expected_ecosystem="Python",
    )
    entry_b = CorpusEntry(
        org="org-b",
        name="shared",
        full_name="org-b/shared",
        url=repo_b.as_uri(),
        clone_url=repo_b.as_uri(),
        ecosystem_key="python",
        expected_ecosystem="Python",
    )

    exports_dir = tmp_path / "exports"
    logs_dir = tmp_path / "logs"

    await execute_benchmark(
        entries=[entry_a, entry_b],
        mode="corpus",
        output_dir=str(exports_dir),
        log_dir=str(logs_dir),
        local_repo_resolver=lambda e: repo_a if e.org == "org-a" else repo_b,
        clean_latest=True,
    )

    _, _, latest2 = await execute_benchmark(
        entries=[entry_b],
        mode="corpus",
        output_dir=str(exports_dir),
        log_dir=str(logs_dir),
        local_repo_resolver=lambda _e: repo_b,
        clean_latest=False,
    )

    topo = json.loads((latest2 / "relationships" / "pipeline_topology.json").read_text())
    wf_names = {item["workflowName"] for item in topo["items"]}
    assert {"AlphaWorkflow", "BetaWorkflow"}.issubset(wf_names)

