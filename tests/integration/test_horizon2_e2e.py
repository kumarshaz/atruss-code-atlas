from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import httpx
import pytest
from typer.testing import CliRunner

from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.cli.commands.analyze_code import app as analyze_code_app
from src.cli.commands.analyze_pipeline import app as pipeline_app
from src.cli.commands.check import app as check_app
from src.cli.commands.diff import app as diff_app
from src.cli.commands.mcp_server import AtrussMCPServer
from src.core.exporters.llms_exporter import build_llms_full_txt, build_llms_txt
from src.core.exporters.sarif_exporter import build_sarif_report
from src.core.exporters.sbom_exporter import build_cyclonedx_sbom
from src.core.services.report_generator import generate_arc42_markdown
from src.models.artifacts import PortableArtifact


def _build_synthetic_secret_token() -> str:
    # Concatenated dynamically so static secret scanners do not confuse test fixtures for live keys.
    return "sk" + "-" + "aB9kL2" * 4


def _seed_horizon2_fixture_repo(repo_dir: Path, *, include_risks: bool = True) -> None:
    (repo_dir / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (repo_dir / "api").mkdir(parents=True, exist_ok=True)
    (repo_dir / "data").mkdir(parents=True, exist_ok=True)
    (repo_dir / "infra").mkdir(parents=True, exist_ok=True)

    (repo_dir / "pyproject.toml").write_text(
        "[project]\nname = 'horizon2-e2e'\nversion = '0.1.0'\n",
        encoding="utf-8",
    )
    (repo_dir / "requirements.txt").write_text(
        "fastapi==0.109.0\nrequests==2.31.0\n",
        encoding="utf-8",
    )
    (repo_dir / "Dockerfile").write_text(
        "FROM python:3.12-slim\nCOPY . /app\nCMD [\"uvicorn\", \"api.routes:app\"]\n",
        encoding="utf-8",
    )
    (repo_dir / "infra" / "deployment.yaml").write_text(
        "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: horizon2-api\n",
        encoding="utf-8",
    )

    (repo_dir / "data" / "__init__.py").write_text("", encoding="utf-8")
    (repo_dir / "data" / "repository.py").write_text(
        "class Base:\n"
        "    pass\n\n"
        "class RecordModel(Base):\n"
        "    name: str = 'item'\n\n"
        "def fetch_records(limit: int = 10) -> list[str]:\n"
        "    if limit > 0:\n"
        "        return [f'item-{i}' for i in range(limit)]\n"
        "    return []\n",
        encoding="utf-8",
    )

    (repo_dir / "api" / "__init__.py").write_text("", encoding="utf-8")
    (repo_dir / "api" / "service.py").write_text(
        "class RecordService:\n"
        "    def list_items(self) -> list[str]:\n"
        "        return ['ok']\n",
        encoding="utf-8",
    )
    if include_risks:
        token_val = _build_synthetic_secret_token()
        (repo_dir / "api" / "routes.py").write_text(
            "from fastapi import FastAPI\n"
            "from data.repository import RecordModel, fetch_records\n\n"
            "app = FastAPI()\n"
            f'STRIPE_API_SECRET = "{token_val}"\n\n'
            "@app.get('/records')\n"
            "def get_records():\n"
            "    _ = RecordModel()\n"
            "    return fetch_records(5)\n\n"
            "def _unused_helper_alpha(x: int) -> int:\n"
            "    return x + 1\n",
            encoding="utf-8",
        )
        reusable_wf = (
            "name: Reusable Deploy\n"
            "on:\n"
            "  workflow_call:\n"
            "jobs:\n"
            "  publish:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: echo publishing\n"
        )
        risky_ci = (
            "name: Risky Pipeline\n"
            "on: pull_request_target\n"
            "permissions: write-all\n"
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "        with:\n"
            "          ref: ${{ github.event.pull_request.head.sha }}\n"
            "      - run: echo ${{ github.event.pull_request.title }}\n"
            "      - uses: actions/upload-artifact@v4\n"
            "  call_reusable:\n"
            "    needs: build\n"
            "    uses: ./.github/workflows/reusable.yml\n"
        )
        (repo_dir / ".github" / "workflows" / "reusable.yml").write_text(
            reusable_wf, encoding="utf-8"
        )
        (repo_dir / ".github" / "workflows" / "ci.yml").write_text(
            risky_ci, encoding="utf-8"
        )
    else:
        (repo_dir / "api" / "routes.py").write_text(
            "from fastapi import FastAPI\n"
            "from api.service import RecordService\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/health')\n"
            "def health():\n"
            "    return {'status': RecordService().list_items()}\n",
            encoding="utf-8",
        )
        clean_ci = (
            "name: Clean CI\n"
            "on:\n"
            "  pull_request:\n"
            "    branches: [main]\n"
            "permissions:\n"
            "  contents: read\n"
            "jobs:\n"
            "  test:\n"
            "    runs-on: ubuntu-latest\n"
            "    timeout-minutes: 15\n"
            "    steps:\n"
            "      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683\n"
            "        with:\n"
            "          persist-credentials: false\n"
            "      - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b\n"
            "        with:\n"
            "          cache: pip\n"
            "      - run: pip install -r requirements.txt && pytest\n"
        )
        (repo_dir / ".github" / "workflows" / "ci.yml").write_text(
            clean_ci, encoding="utf-8"
        )


@pytest.mark.integration
def test_horizon2_analyze_code_sbom_sarif_llms_and_coverage_e2e(tmp_path: Path):
    """FR-021..FR-029 E2E: CLI analyze-code + analyze-pipeline + SARIF + CycloneDX + llms.txt."""
    repo_dir = tmp_path / "horizon2-e2e"
    _seed_horizon2_fixture_repo(repo_dir, include_risks=True)

    lcov_path = tmp_path / "lcov.info"
    lcov_path.write_text(
        f"SF:{repo_dir / 'api' / 'routes.py'}\n"
        "LF:10\n"
        "LH:8\n"
        "end_of_record\n",
        encoding="utf-8",
    )

    exports_dir = tmp_path / "exports"
    runner = CliRunner()

    pipe_res = runner.invoke(
        pipeline_app,
        [
            "--path",
            str(repo_dir),
            "--output-dir",
            str(exports_dir),
            "--format",
            "sarif",
            "--blast-radius",
            "build",
        ],
    )
    assert pipe_res.exit_code == 0, pipe_res.output

    code_res = runner.invoke(
        analyze_code_app,
        [
            "--path",
            str(repo_dir),
            "--exports-dir",
            str(exports_dir),
            "--sbom",
            "--format",
            "sarif",
            "--blast-radius",
            "get_records",
            "--coverage",
            str(lcov_path),
        ],
    )
    assert code_res.exit_code == 0, code_res.output

    latest = exports_dir / "latest"
    analysis_path = latest / "reports" / "local-horizon2-e2e-analysis.json"
    report_md_path = latest / "reports" / "local-horizon2-e2e-report.md"
    sbom_path = latest / "sbom" / "local-horizon2-e2e.cdx.json"
    sarif_path = latest / "sarif" / "local-horizon2-e2e.sarif.json"
    llms_txt = latest / "llms" / "llms.txt"
    llms_full_txt = latest / "llms" / "llms-full.txt"
    history_path = latest / "catalog-history.json"

    for artifact_file in (
        analysis_path,
        report_md_path,
        sbom_path,
        sarif_path,
        llms_txt,
        llms_full_txt,
        history_path,
    ):
        assert artifact_file.exists(), f"Missing expected Horizon 2 artifact: {artifact_file}"

    analysis_json = json.loads(analysis_path.read_text(encoding="utf-8"))
    assert analysis_json["scorecard"]["overall_grade"] in {"A", "B", "C", "D", "F"}
    assert len(analysis_json["scorecard"]["dimensions"]) == 6
    assert any(d["name"] == "fastapi" for d in analysis_json["dependencies"])
    assert any(v["rule_id"].startswith("ATRUSS-ARCH-") for v in analysis_json["fitness_violations"])
    assert len(analysis_json["secrets"]) >= 1
    assert len(analysis_json["code_to_cloud_edges"]) >= 1

    md_text = report_md_path.read_text(encoding="utf-8")
    assert "## Section 7: Code-to-Cloud Deployment Traceability" in md_text
    assert "```mermaid" in md_text

    sbom_json = json.loads(sbom_path.read_text(encoding="utf-8"))
    assert sbom_json["bomFormat"] == "CycloneDX"
    assert sbom_json["specVersion"] == "1.6"

    sarif_json = json.loads(sarif_path.read_text(encoding="utf-8"))
    assert sarif_json["version"] == "2.1.0"
    assert len(sarif_json["runs"][0]["results"]) > 0

    history_json = json.loads(history_path.read_text(encoding="utf-8"))
    assert len(history_json["snapshots"]) >= 1
    assert "horizon2-e2e" in llms_txt.read_text(encoding="utf-8")
    assert "6-Dimension Scorecard" in llms_full_txt.read_text(encoding="utf-8")


@pytest.mark.integration
def test_horizon2_offline_mocked_osv_batch_vulnerability_enrichment(tmp_path: Path):
    """FR-024 E2E: Verifies offline-safe mocked OSV.dev /v1/querybatch CVE matching & SBOM."""
    repo_dir = tmp_path / "osv-e2e"
    _seed_horizon2_fixture_repo(repo_dir, include_risks=False)

    def osv_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/querybatch":
            payload = json.loads(request.content.decode("utf-8"))
            results = []
            for q in payload.get("queries", []):
                pkg_meta = q.get("package", {})
                pkg_str = f"{pkg_meta.get('name', '')} {pkg_meta.get('purl', '')}".lower()
                if "requests" in pkg_str:
                    results.append({
                        "vulns": [
                            {
                                "id": "GHSA-9hjg-9r4m-mvj7",
                                "summary": "Requests credential leak on cross-host redirect",
                                "database_specific": {"severity": "HIGH"},
                                "affected": [
                                    {
                                        "ranges": [
                                            {
                                                "events": [
                                                    {"introduced": "0"},
                                                    {"fixed": "2.32.0"},
                                                ]
                                            }
                                        ]
                                    }
                                ],
                            }
                        ]
                    })
                else:
                    results.append({})
            return httpx.Response(200, json={"results": results})
        return httpx.Response(404)

    result = orchestrate_full_analysis(
        repo_dir,
        enable_live_osv=True,
        osv_transport=httpx.MockTransport(osv_handler),
        osv_cache_path=tmp_path / "osv-cache.json",
    )
    assert len(result.vulnerabilities) == 1
    assert result.vulnerabilities[0].id == "GHSA-9hjg-9r4m-mvj7"
    assert result.vulnerabilities[0].fixed_version == "2.32.0"

    sbom = build_cyclonedx_sbom(
        "local/osv-e2e",
        "mocksha01",
        result.dependencies,
        result.vulnerabilities,
    )
    assert sbom["vulnerabilities"][0]["id"] == "GHSA-9hjg-9r4m-mvj7"


@pytest.mark.integration
def test_horizon2_check_and_diff_gates_and_mcp_stdio(tmp_path: Path):
    """FR-027/028/029 E2E: Verifies atruss check --sarif, atruss diff regressions, and MCP."""
    runner = CliRunner()

    clean_repo = tmp_path / "clean-repo"
    _seed_horizon2_fixture_repo(clean_repo, include_risks=False)
    baseline_exports = tmp_path / "baseline-exports"
    res_base = runner.invoke(
        analyze_code_app,
        ["--path", str(clean_repo), "--exports-dir", str(baseline_exports)],
    )
    assert res_base.exit_code == 0, res_base.output

    clean_check = runner.invoke(
        check_app,
        [
            "--path",
            str(clean_repo),
            "--fail-on",
            "CRITICAL",
            "--exports-dir",
            str(baseline_exports),
        ],
    )
    assert clean_check.exit_code == 0, clean_check.output

    risky_repo = tmp_path / "risky-repo"
    _seed_horizon2_fixture_repo(risky_repo, include_risks=True)
    target_exports = tmp_path / "target-exports"
    res_tgt = runner.invoke(
        analyze_code_app,
        ["--path", str(risky_repo), "--exports-dir", str(target_exports)],
    )
    assert res_tgt.exit_code == 0, res_tgt.output

    sarif_out = tmp_path / "check.sarif.json"
    risky_check = runner.invoke(
        check_app,
        [
            "--path",
            str(risky_repo),
            "--sarif",
            str(sarif_out),
            "--fail-on",
            "HIGH",
            "--exports-dir",
            str(target_exports),
        ],
    )
    assert risky_check.exit_code == 1
    assert sarif_out.exists()
    assert json.loads(sarif_out.read_text(encoding="utf-8"))["version"] == "2.1.0"

    # Normalize report repository keys so diff compares baseline vs target on the same logical repo
    base_rep_dir = baseline_exports / "latest" / "reports"
    tgt_rep_dir = target_exports / "latest" / "reports"
    base_data = json.loads((base_rep_dir / "local-clean-repo-analysis.json").read_text())
    tgt_data = json.loads((tgt_rep_dir / "local-risky-repo-analysis.json").read_text())
    base_data["repository"] = "org/shared-svc"
    tgt_data["repository"] = "org/shared-svc"
    (base_rep_dir / "local-clean-repo-analysis.json").write_text(json.dumps(base_data))
    (tgt_rep_dir / "local-risky-repo-analysis.json").write_text(json.dumps(tgt_data))

    diff_res = runner.invoke(
        diff_app,
        [
            "--baseline",
            str(baseline_exports / "latest"),
            "--target",
            str(target_exports / "latest"),
            "--exports-dir",
            str(target_exports),
            "--fail-on-regression",
        ],
    )
    assert diff_res.exit_code == 1
    drift_json = target_exports / "latest" / "drift" / "drift_report.json"
    assert drift_json.exists()
    drift_payload = json.loads(drift_json.read_text(encoding="utf-8"))
    assert drift_payload["has_regression"] is True
    assert "org/shared-svc" in drift_payload["scorecard_transitions"]

    # MCP server over Content-Length AND newline-delimited JSON-RPC stdio
    server = AtrussMCPServer(target_exports / "latest")
    tools = server.handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert tools is not None
    assert len(tools["result"]["tools"]) == 10

    scorecard_res = server.call_tool("get_repo_scorecard", {"repository": "org/shared-svc"})
    assert scorecard_res["found"] is True

    req_list = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    req_call = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "list_repositories", "arguments": {}},
    })
    framed_in = io.BytesIO(
        f"Content-Length: {len(req_list)}\r\n\r\n{req_list}{req_call}\n".encode()
    )
    framed_out = io.BytesIO()
    server.serve_stdio(stdin=framed_in, stdout=framed_out)
    out_bytes = framed_out.getvalue().decode("utf-8")
    assert "Content-Length:" in out_bytes
    assert "org/shared-svc" in out_bytes


@pytest.mark.integration
def test_horizon2_sha256_determinism_e2e(tmp_path: Path):
    """SC-008: Repeated full Horizon 2 runs produce byte-identical SHA-256 outputs."""
    repo_dir = tmp_path / "det-h2"
    _seed_horizon2_fixture_repo(repo_dir, include_risks=True)

    digests: list[dict[str, str]] = []
    for idx in range(2):
        res = orchestrate_full_analysis(repo_dir)
        portable = PortableArtifact(
            repository="local/det-h2",
            sha="fixedsha123",
            ecosystem=res.ecosystem,
            metrics=res.metrics,
            pipelines=res.pipelines,
            architecture_components=res.components,
            scorecard=res.scorecard,
            dependencies=res.dependencies,
            vulnerabilities=res.vulnerabilities,
            secrets=res.secrets,
            fitness_violations=res.fitness_violations,
            code_to_cloud_edges=res.code_to_cloud_edges,
            workspace_packages=res.workspace_packages,
            observability=res.observability,
        )
        sbom = build_cyclonedx_sbom(
            "local/det-h2", "fixedsha123", res.dependencies, res.vulnerabilities
        )
        sarif = build_sarif_report(portable, repo_name="local/det-h2")
        md = generate_arc42_markdown(
            "local/det-h2",
            res.components,
            metrics=res.metrics,
            ecosystem=res.ecosystem,
            framework=res.framework,
            sha="fixedsha123",
            scorecard=res.scorecard,
            dependencies=res.dependencies,
            vulnerabilities=res.vulnerabilities,
            fitness_violations=res.fitness_violations,
            code_to_cloud_edges=res.code_to_cloud_edges,
            workspace_packages=res.workspace_packages,
        )
        det_latest = tmp_path / f"latest_{idx}"
        (det_latest / "reports").mkdir(parents=True, exist_ok=True)
        (det_latest / "sbom").mkdir(parents=True, exist_ok=True)
        (det_latest / "reports" / "local-det-h2-analysis.json").write_text(
            portable.model_dump_json(indent=2), encoding="utf-8"
        )
        (det_latest / "sbom" / "local-det-h2.cdx.json").write_text(
            json.dumps(sbom, indent=2), encoding="utf-8"
        )
        llms_short = build_llms_txt(det_latest)
        llms_full = build_llms_full_txt(det_latest)

        digests.append({
            key: hashlib.sha256(val.encode("utf-8")).hexdigest()
            for key, val in {
                "artifact": portable.model_dump_json(indent=2),
                "sbom": json.dumps(sbom, sort_keys=True),
                "sarif": json.dumps(sarif, sort_keys=True),
                "md": md,
                "llms": llms_short,
                "llms_full": llms_full,
            }.items()
        })

    assert digests[0] == digests[1]
