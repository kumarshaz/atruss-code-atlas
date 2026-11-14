import base64
import csv
import json
from pathlib import Path

import httpx
import pytest

from src.cli.commands.analyze_code import _analyze_repo_code
from src.cli.commands.analyze_pipeline import execute_pipeline_analysis
from src.cli.commands.discover import execute_discovery
from src.core.services.report_generator import generate_arc42_markdown


def _b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tr_con_golden_contracts_discovery_pipeline_and_code(tmp_path: Path):
    """TR-CON E2E: validates full golden schemas across discovery (27-col), Astro pipeline JSON, and Arc42 MD."""
    workflow_yml = (
        "name: CI\n"
        "on:\n"
        "  push:\n"
        "    branches: [main]\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/setup-python@v5\n"
        "        with:\n"
        "          cache: pip\n"
        "      - run: pytest\n"
        "  deploy:\n"
        "    needs: test\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - run: echo deploy\n"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/orgs/acme/repos":
            return httpx.Response(
                200,
                json=[
                    {
                        "id": 42,
                        "name": "pet-api",
                        "owner": {"login": "acme", "id": 7},
                        "default_branch": "main",
                        "clone_url": "https://github.com/acme/pet-api.git",
                        "ssh_url": "git@github.com:acme/pet-api.git",
                        "html_url": "https://github.com/acme/pet-api",
                        "size": 120,
                        "archived": False,
                        "private": False,
                        "pushed_at": "2026-01-15T12:00:00Z",
                        "language": "Python",
                    }
                ],
            )
        if path == "/repos/acme/pet-api/git/trees/main":
            return httpx.Response(
                200,
                json={
                    "sha": "deadbeef1234",
                    "tree": [
                        {"path": "pyproject.toml", "type": "blob"},
                        {"path": "src/main.py", "type": "blob"},
                        {"path": "Dockerfile", "type": "blob"},
                        {"path": ".github/workflows/ci.yml", "type": "blob"},
                    ],
                },
            )
        if path == "/repos/acme/pet-api/contents/.github/workflows/ci.yml":
            return httpx.Response(
                200,
                json={"encoding": "base64", "content": _b64(workflow_yml)},
            )
        return httpx.Response(404, json={"message": "Not Found"})

    transport = httpx.MockTransport(handler)
    exports_dir = tmp_path / "exports"
    logs_dir = tmp_path / "logs"

    await execute_discovery(
        org="acme",
        base_dir=str(exports_dir),
        log_dir=str(logs_dir),
        include_archived=False,
        max_concurrent=2,
        exclude_repo_names=[],
        exclude_repo_patterns=[],
        dry_run=False,
        transport=transport,
    )

    manifest_json = exports_dir / "latest" / "repos" / "repositories.json"
    manifest_csv = exports_dir / "latest" / "repos" / "repositories.csv"
    assert manifest_json.exists()
    assert manifest_csv.exists()

    with open(manifest_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert len(rows[0]) == 27
    assert rows[0]["Organization"] == "acme"
    assert rows[0]["RepositoryName"] == "pet-api"
    assert rows[0]["PrimaryLanguage"] == "Python"
    assert rows[0]["HasDockerfile"] == "True"
    assert rows[0]["HasPipeline"] == "True"

    await execute_pipeline_analysis(
        from_discovery=str(manifest_json),
        output_dir=str(exports_dir),
        transport=transport,
    )

    astro_pipe = exports_dir / "latest" / "pipelines" / "acme-pet-api-pipeline.json"
    assert astro_pipe.exists()
    pipe_data = json.loads(astro_pipe.read_text(encoding="utf-8"))
    assert "analyzed_at" in pipe_data
    assert len(pipe_data["workflows"]) == 1
    wf = pipe_data["workflows"][0]
    assert wf["name"] == "CI"
    assert [j["id"] for j in wf["jobs"]] == ["test", "deploy"]
    assert wf["jobs"][1]["needs"] == ["test"]

    local_repo = tmp_path / "pet-api"
    (local_repo / "src").mkdir(parents=True)
    (local_repo / "pyproject.toml").write_text("[project]\nname='pet-api'\n", encoding="utf-8")
    (local_repo / "src" / "main.py").write_text(
        "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/pets')\ndef list_pets(): return []\n",
        encoding="utf-8",
    )
    code_artifact = _analyze_repo_code(local_repo, "acme/pet-api")
    md = generate_arc42_markdown(
        code_artifact.repository,
        code_artifact.architecture_components,
        metrics=code_artifact.metrics,
        ecosystem=code_artifact.ecosystem,
        framework=str(code_artifact.metrics.get("framework", "Unknown")),
        sha=code_artifact.sha,
        include_frontmatter=True,
    )
    assert md.startswith("---\ntitle: Architecture")
    assert "```mermaid" in md
    assert "list_pets" in md
