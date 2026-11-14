import json
from pathlib import Path

import httpx
import pytest
from typer.testing import CliRunner

from src.cli.commands.analyze_code import app as analyze_code_app
from src.cli.commands.analyze_pipeline import execute_pipeline_analysis
from src.cli.commands.discover import execute_discovery


@pytest.mark.integration
@pytest.mark.asyncio
async def test_discover_and_export_lifecycle_latest_merge(tmp_path: Path):
    """Validates discover -> analyze-pipeline -> analyze-code merges all modules into exports/latest/."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/orgs/demo/repos":
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 101,
                        "name": "atlas-svc",
                        "owner": {"login": "demo", "id": 9},
                        "default_branch": "main",
                        "clone_url": "https://github.com/demo/atlas-svc.git",
                        "ssh_url": "git@github.com:demo/atlas-svc.git",
                        "html_url": "https://github.com/demo/atlas-svc",
                        "language": "Python",
                    }
                ],
            )
        if request.url.path == "/repos/demo/atlas-svc/git/trees/main":
            return httpx.Response(
                200,
                json={
                    "sha": "abc000",
                    "tree": [
                        {"path": "pyproject.toml", "type": "blob"},
                        {"path": ".github/workflows/ci.yml", "type": "blob"},
                    ],
                },
            )
        return httpx.Response(404, json={"message": "Not Found"})

    exports_dir = tmp_path / "exports"
    logs_dir = tmp_path / "logs"

    await execute_discovery(
        org="demo",
        base_dir=str(exports_dir),
        log_dir=str(logs_dir),
        include_archived=False,
        max_concurrent=1,
        exclude_repo_names=[],
        exclude_repo_patterns=[],
        dry_run=False,
        transport=httpx.MockTransport(handler),
    )

    await execute_pipeline_analysis(
        from_discovery=str(exports_dir / "latest" / "repos" / "repositories.json"),
        output_dir=str(exports_dir),
        transport=httpx.MockTransport(handler),
    )

    local_repo = tmp_path / "atlas-svc"
    local_repo.mkdir()
    (local_repo / "pyproject.toml").write_text("[project]\nname='atlas-svc'\n", encoding="utf-8")
    (local_repo / "svc.py").write_text(
        "class InventoryService:\n    def count(self): return 1\n",
        encoding="utf-8",
    )

    runner = CliRunner()
    res = runner.invoke(
        analyze_code_app,
        ["--path", str(local_repo), "--exports-dir", str(exports_dir)],
    )
    assert res.exit_code == 0, res.output

    latest = exports_dir / "latest"
    assert (latest / "repos" / "repositories.json").exists()
    assert (latest / "repos" / "repositories.csv").exists()
    assert (latest / "repos" / "repositories.yaml").exists()
    assert (latest / "pipelines" / "demo-atlas-svc-pipeline.json").exists()
    assert (latest / "relationships" / "pipeline_topology.json").exists()
    assert (latest / "reports" / "local-atlas-svc-report.md").exists()
    analysis = json.loads((latest / "reports" / "local-atlas-svc-analysis.json").read_text(encoding="utf-8"))
    assert analysis["ecosystem"] == "Python"
