from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

from typer.testing import CliRunner

from src.analyzers.drift import compute_drift_report, render_drift_markdown, resolve_snapshot_dir
from src.cli.commands.check import app as check_app
from src.cli.commands.diff import app as diff_app
from src.cli.commands.mcp_server import AtrussMCPServer
from src.cli.commands.mcp_server import app as mcp_app
from src.core.exporters.llms_exporter import export_llms_context
from src.core.exporters.sarif_exporter import build_sarif_report, export_sarif_report
from src.models.artifacts import (
    DependencyRecord,
    FitnessViolation,
    PipelineWorkflow,
    PortableArtifact,
    RepositoryScorecard,
    ScorecardDimension,
    SecretFinding,
    VulnerabilityRecord,
)

runner = CliRunner()


def _make_sample_snapshot(
    root: Path,
    *,
    security_score: float = 95.0,
    security_grade: str = "A",
    overall_score: float = 92.0,
    overall_grade: str = "A",
    extra_component: bool = False,
    include_antipattern: bool = False,
    include_fitness_violation: bool = False,
) -> Path:
    (root / "repos").mkdir(parents=True, exist_ok=True)
    (root / "pipelines").mkdir(parents=True, exist_ok=True)
    (root / "reports").mkdir(parents=True, exist_ok=True)
    (root / "sbom").mkdir(parents=True, exist_ok=True)
    (root / "relationships").mkdir(parents=True, exist_ok=True)

    (root / "repos" / "repositories.json").write_text(
        json.dumps({
            "count": 1,
            "items": [
                {
                    "Organization": "acme",
                    "RepositoryName": "orders-api",
                    "RepositoryId": "acme/orders-api",
                    "PrimaryLanguage": "Python",
                    "FrameworkType": "FastAPI",
                    "DocumentationPriority": "P1",
                }
            ],
        }),
        encoding="utf-8",
    )

    anti_patterns = []
    if include_antipattern:
        anti_patterns.append({
            "rule_id": "ATRUSS-PIPE-008",
            "type": "UNPINNED_ACTION",
            "severity": "HIGH",
            "file_source": ".github/workflows/ci.yml",
            "start_line": 12,
            "end_line": 12,
            "message": "Unpinned action third-party/setup@v1",
        })

    (root / "pipelines" / "acme-orders-api-pipeline.json").write_text(
        json.dumps({
            "org": "acme",
            "repository": "orders-api",
            "sha": "deadbeef",
            "workflows": [
                {
                    "id": "ci.yml",
                    "name": "CI",
                    "triggers": ["push"],
                    "jobs": [
                        {
                            "id": "test",
                            "name": "Run Tests",
                            "runner": "ubuntu-latest",
                            "steps_count": 3,
                            "needs": [],
                        },
                        {
                            "id": "deploy",
                            "name": "Deploy Prod",
                            "runner": "ubuntu-latest",
                            "steps_count": 2,
                            "needs": ["test"],
                        },
                    ],
                    "anti_patterns": anti_patterns,
                }
            ],
        }),
        encoding="utf-8",
    )

    (root / "relationships" / "pipeline_topology.json").write_text(
        json.dumps({
            "count": 1,
            "items": [
                {
                    "repoName": "orders-api",
                    "workflowName": "CI",
                    "deploymentTargetName": "production",
                }
            ],
        }),
        encoding="utf-8",
    )

    components = [
        {
            "name": "OrdersController",
            "type": "API_ROUTE",
            "file": "src/api.py",
            "ecosystem": "python",
            "dependencies": ["OrdersService"],
        },
        {
            "name": "OrdersService",
            "type": "SERVICE",
            "file": "src/service.py",
            "ecosystem": "python",
            "dependencies": ["OrdersRepo"],
        },
        {
            "name": "OrdersRepo",
            "type": "DATA_ACCESS_LAYER",
            "file": "src/repo.py",
            "ecosystem": "python",
            "dependencies": [],
        },
    ]
    if extra_component:
        components.append({
            "name": "OrdersAudit",
            "type": "SERVICE",
            "file": "src/audit.py",
            "ecosystem": "python",
            "dependencies": [],
        })

    fitness_violations = []
    if include_fitness_violation:
        components[0]["dependencies"] = ["OrdersService", "OrdersRepo"]
        fitness_violations.append({
            "rule_id": "ATRUSS-ARCH-001",
            "type": "LAYER_VIOLATION",
            "severity": "HIGH",
            "source_component": "OrdersController",
            "target_component": "OrdersRepo",
            "file_source": "src/api.py",
            "start_line": 1,
            "end_line": 1,
            "message": "OrdersController bypasses SERVICE to access OrdersRepo",
        })

    debt_score = round(100.0 - overall_score, 2)
    report_payload = {
        "repository": "acme/orders-api",
        "sha": "deadbeef",
        "ecosystem": "Python",
        "metrics": {
            "files_analyzed": 3,
            "loc": 250,
            "sloc": 200,
            "component_count": len(components),
            "avg_cyclomatic_complexity": 2.0,
            "max_cyclomatic_complexity": 5,
            "framework": "FastAPI",
        },
        "pipelines": [],
        "architecture_components": components,
        "fitness_violations": fitness_violations,
        "dependencies": [
            {
                "name": "fastapi",
                "version": "0.110.0",
                "ecosystem": "PyPI",
                "purl": "pkg:pypi/fastapi@0.110.0",
                "manifest_file": "requirements.txt",
                "line": 1,
                "is_direct": True,
            }
        ],
        "vulnerabilities": [],
        "secrets": [],
        "code_to_cloud_edges": [
            {
                "source": "orders-api",
                "source_type": "code_module",
                "target": "ci.yml#deploy",
                "target_type": "ci_job",
                "relationship": "DEPLOYED_BY",
            },
            {
                "source": "ci.yml#deploy",
                "source_type": "ci_job",
                "target": "production",
                "target_type": "environment",
                "relationship": "DEPLOYS_TO",
            },
        ],
        "scorecard": {
            "overall_score": overall_score,
            "overall_grade": overall_grade,
            "technical_debt_score": debt_score,
            "remediation_hours": round(debt_score * 0.25, 2),
            "dimensions": {
                "code_quality": {
                    "name": "Code Quality",
                    "score": 95.0,
                    "grade": "A",
                    "weight": 0.20,
                    "details": "",
                },
                "security": {
                    "name": "Security",
                    "score": security_score,
                    "grade": security_grade,
                    "weight": 0.20,
                    "details": "",
                },
                "maintainability": {
                    "name": "Maintainability",
                    "score": 90.0,
                    "grade": "A",
                    "weight": 0.15,
                    "details": "",
                },
                "test_coverage": {
                    "name": "Test Coverage",
                    "score": 90.0,
                    "grade": "A",
                    "weight": 0.15,
                    "details": "",
                },
                "dependency_health": {
                    "name": "Dependency Health",
                    "score": 90.0,
                    "grade": "A",
                    "weight": 0.15,
                    "details": "",
                },
                "pipeline_health": {
                    "name": "Pipeline Health",
                    "score": 95.0,
                    "grade": "A",
                    "weight": 0.15,
                    "details": "",
                },
            },
        },
    }
    (root / "reports" / "acme-orders-api-analysis.json").write_text(
        json.dumps(report_payload, indent=2),
        encoding="utf-8",
    )

    (root / "sbom" / "acme-orders-api.cdx.json").write_text(
        json.dumps({
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "metadata": {"component": {"name": "acme/orders-api"}},
            "components": [{"name": "fastapi", "version": "0.110.0"}],
            "vulnerabilities": [],
        }),
        encoding="utf-8",
    )
    return root


def test_drift_engine_and_diff_cli(tmp_path: Path) -> None:
    exports_root = tmp_path / "exports_with_latest"
    latest_dir = exports_root / "latest"
    _make_sample_snapshot(latest_dir)
    assert resolve_snapshot_dir(exports_root) == latest_dir
    assert resolve_snapshot_dir(latest_dir) == latest_dir

    t1 = tmp_path / "t1"
    t2 = tmp_path / "t2"
    _make_sample_snapshot(t1)
    _make_sample_snapshot(
        t2,
        security_score=70.0,
        security_grade="C",
        overall_score=78.0,
        overall_grade="C",
        extra_component=True,
        include_antipattern=True,
        include_fitness_violation=True,
    )

    report = compute_drift_report(t1, t2)
    assert report["has_regression"] is True
    assert report["summary"]["added_components_count"] == 1
    assert report["summary"]["new_antipatterns_count"] == 1
    assert report["summary"]["new_fitness_violations_count"] == 1
    assert report["summary"]["regressions_count"] >= 4

    sec_trans = report["scorecard_transitions"]["acme/orders-api"]["dimensions"]["security"]
    assert sec_trans["from"] == "A"
    assert sec_trans["to"] == "C"
    assert sec_trans["delta"] == -25.0

    md = render_drift_markdown(report)
    assert "REGRESSION DETECTED" in md
    assert "acme/orders-api" in md

    # CLI diff --fail-on-regression -> exit 1
    out_exports = tmp_path / "cli_exports"
    out_dir = tmp_path / "standalone_drift"
    res_fail = runner.invoke(
        diff_app,
        [
            "--baseline",
            str(t1),
            "--target",
            str(t2),
            "--exports-dir",
            str(out_exports),
            "--output-dir",
            str(out_dir),
            "--fail-on-regression",
        ],
    )
    assert res_fail.exit_code == 1
    assert (out_dir / "drift_report.json").exists()
    assert (out_dir / "drift_report.md").exists()
    assert (out_exports / "latest" / "drift" / "drift_report.json").exists()

    # Identical snapshots -> NO REGRESSIONS, exit 0
    res_ok = runner.invoke(
        diff_app,
        [
            "--baseline",
            str(t1),
            "--target",
            str(t1),
            "--exports-dir",
            str(out_exports),
            "--fail-on-regression",
        ],
    )
    assert res_ok.exit_code == 0


def test_sarif_exporter_v210_and_check_cli(tmp_path: Path) -> None:
    artifact = PortableArtifact(
        repository="acme/demo",
        sha="abc123",
        ecosystem="Python",
        metrics={"loc": 50},
        pipelines=[
            PipelineWorkflow(
                id="deploy.yml",
                path=".github/workflows/deploy.yml",
                name="Deploy",
                triggers=["push"],
                anti_patterns=[
                    {
                        "rule_id": "ATRUSS-PIPE-008",
                        "type": "UNPINNED_ACTION",
                        "severity": "HIGH",
                        "file_source": ".github/workflows/deploy.yml",
                        "start_line": 14,
                        "end_line": 14,
                        "message": "Action third-party/tool@v1 is unpinned.",
                    }
                ],
            )
        ],
        fitness_violations=[
            FitnessViolation(
                rule_id="ATRUSS-ARCH-001",
                type="LAYER_VIOLATION",
                severity="HIGH",
                source_component="OrdersRoute",
                target_component="OrdersRepo",
                file_source="src/routes.py",
                start_line=5,
                end_line=5,
                message="API_ROUTE bypasses SERVICE.",
            )
        ],
        secrets=[
            SecretFinding(
                rule_id="ATRUSS-SEC-001",
                type="AWS_ACCESS_KEY",
                severity="CRITICAL",
                file_source="src/settings.py",
                start_line=2,
                end_line=2,
                redacted_snippet="AKIA***REDACTED***",
                entropy=4.3,
                message="AWS Access Key detected.",
            )
        ],
        vulnerabilities=[
            VulnerabilityRecord(
                id="GHSA-xxxx-9999",
                package="requests",
                installed_version="2.19.0",
                fixed_version="2.32.0",
                ecosystem="PyPI",
                purl="pkg:pypi/requests@2.19.0",
                manifest_file="requirements.txt",
                line=3,
                severity="MEDIUM",
                summary="Cookie leak",
            )
        ],
        scorecard=RepositoryScorecard(
            overall_score=70.0,
            overall_grade="C",
            technical_debt_score=30.0,
            remediation_hours=10.0,
            dimensions={
                "security": ScorecardDimension(name="Security", score=60.0, grade="D", weight=0.2)
            },
        ),
        dependencies=[
            DependencyRecord(
                name="requests",
                version="2.19.0",
                ecosystem="PyPI",
                purl="pkg:pypi/requests@2.19.0",
                manifest_file="requirements.txt",
                line=3,
            )
        ],
    )

    sarif_1 = build_sarif_report(artifact)
    sarif_2 = build_sarif_report(artifact)
    assert sarif_1 == sarif_2
    assert sarif_1["version"] == "2.1.0"
    run = sarif_1["runs"][0]
    assert run["tool"]["driver"]["name"] == "atruss-code-atlas"
    rule_ids = {r["id"] for r in run["tool"]["driver"]["rules"]}
    assert {"ATRUSS-PIPE-008", "ATRUSS-ARCH-001", "ATRUSS-SEC-001", "GHSA-xxxx-9999"} == rule_ids

    results_by_rule = {r["ruleId"]: r for r in run["results"]}
    assert results_by_rule["ATRUSS-SEC-001"]["level"] == "error"
    assert results_by_rule["ATRUSS-PIPE-008"]["level"] == "error"
    assert results_by_rule["GHSA-xxxx-9999"]["level"] == "warning"
    assert (
        results_by_rule["ATRUSS-ARCH-001"]["locations"][0]["physicalLocation"]["artifactLocation"][
            "uri"
        ]
        == "src/routes.py"
    )

    sarif_file = export_sarif_report(artifact, tmp_path / "demo.sarif.json")
    assert sarif_file.exists()
    sarif_dir_file = export_sarif_report(
        [artifact],
        output_dir=tmp_path / "sarif_dir",
        findings=[
            {
                "rule_id": "ATRUSS-PIPE-009",
                "type": "TEMPLATE_INJECTION",
                "severity": "CRITICAL",
                "file_source": ".github/workflows/deploy.yml",
                "start_line": 22,
                "end_line": 24,
                "message": "Untrusted github.event.issue.title in run step.",
            }
        ],
    )
    assert sarif_dir_file.name == "acme-demo.sarif.json"
    dir_payload = json.loads(sarif_dir_file.read_text(encoding="utf-8"))
    assert len(dir_payload["runs"][0]["results"]) == 5

    # Build real temporary repo for `atruss check`
    bad_repo = tmp_path / "bad_repo"
    (bad_repo / ".github" / "workflows").mkdir(parents=True)
    (bad_repo / "requirements.txt").write_text("fastapi==0.110.0\n", encoding="utf-8")
    (bad_repo / "models.py").write_text(
        "class Base:\n    pass\n\nclass UserModel(Base):\n    pass\n",
        encoding="utf-8",
    )
    (bad_repo / "services.py").write_text("class UserService:\n    pass\n", encoding="utf-8")
    (bad_repo / "routes.py").write_text(
        "from models import UserModel\n\nclass App:\n"
        "    def get(self, p):\n        return lambda f: f\n\n"
        "app = App()\n\n@app.get('/users')\ndef list_users():\n    return UserModel()\n",
        encoding="utf-8",
    )
    fake_aws_key = "AKIA" + "1234567890ABCDEF"
    (bad_repo / "settings.py").write_text(f'AWS_KEY = "{fake_aws_key}"\n', encoding="utf-8")
    (bad_repo / ".github" / "workflows" / "ci.yml").write_text(
        "name: CI\non:\n  pull_request:\n    branches: [main]\npermissions:\n  contents: read\n"
        "jobs:\n  build:\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n"
        "    steps:\n      - uses: third-party/action@v1\n",
        encoding="utf-8",
    )

    sarif_out = tmp_path / "pr.sarif"
    check_exports = tmp_path / "check_exports"
    res_fail = runner.invoke(
        check_app,
        [
            "--path",
            str(bad_repo),
            "--sarif",
            str(sarif_out),
            "--exports-dir",
            str(check_exports),
            "--fail-on",
            "HIGH",
        ],
    )
    assert res_fail.exit_code == 1
    assert sarif_out.exists()
    assert (check_exports / "latest" / "sarif" / "local-bad_repo.sarif.json").exists()
    assert (check_exports / "latest" / "reports" / "local-bad_repo-analysis.json").exists()
    loaded_sarif = json.loads(sarif_out.read_text(encoding="utf-8"))
    found_rules = {r["ruleId"] for r in loaded_sarif["runs"][0]["results"]}
    assert "ATRUSS-PIPE-008" in found_rules
    assert "ATRUSS-ARCH-001" in found_rules
    assert "ATRUSS-SEC-001" in found_rules

    res_none = runner.invoke(
        check_app,
        ["--path", str(bad_repo), "--fail-on", "NONE"],
    )
    assert res_none.exit_code == 0

    clean_repo = tmp_path / "clean_repo"
    clean_repo.mkdir()
    (clean_repo / "app.py").write_text("def greet(name: str) -> str:\n    return name\n")
    res_clean = runner.invoke(check_app, ["--path", str(clean_repo), "--fail-on", "HIGH"])
    assert res_clean.exit_code == 0

    res_bad_flag = runner.invoke(
        check_app,
        ["--path", str(bad_repo), "--fail-on", "INVALID"],
    )
    assert res_bad_flag.exit_code == 2


def test_llms_exporter_determinism(tmp_path: Path) -> None:
    latest_dir = _make_sample_snapshot(tmp_path / "latest")

    llms_1, full_1 = export_llms_context(latest_dir, output_dir=tmp_path / "out1")
    llms_2, full_2 = export_llms_context(latest_dir, output_dir=tmp_path / "out2")

    assert hashlib.sha256(llms_1.read_bytes()).hexdigest() == hashlib.sha256(
        llms_2.read_bytes()
    ).hexdigest()
    assert hashlib.sha256(full_1.read_bytes()).hexdigest() == hashlib.sha256(
        full_2.read_bytes()
    ).hexdigest()

    idx_txt = llms_1.read_text(encoding="utf-8")
    full_txt = full_1.read_text(encoding="utf-8")
    assert "# Atruss Code Atlas" in idx_txt
    assert "acme/orders-api" in idx_txt
    assert "Grade A (92.0/100)" in idx_txt
    assert "## Repository: acme/orders-api" in full_txt
    assert "OrdersController" in full_txt
    assert "Code-to-Cloud Traceability" in full_txt


def test_mcp_server_framing_and_all_10_tools(tmp_path: Path) -> None:
    latest_dir = _make_sample_snapshot(
        tmp_path / "latest",
        include_antipattern=True,
        include_fitness_violation=True,
    )
    server = AtrussMCPServer(latest_dir)

    # 1. Protocol lifecycle + error handling
    init_resp = server.handle_message({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert init_resp is not None
    assert init_resp["result"]["serverInfo"]["name"] == "atruss-code-atlas"

    assert (
        server.handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    )

    tools_resp = server.handle_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert tools_resp is not None
    tool_names = [t["name"] for t in tools_resp["result"]["tools"]]
    expected_tools = [
        "list_repositories",
        "get_repo_architecture",
        "get_pipeline_dag",
        "find_cross_repo_impacts",
        "get_blast_radius",
        "trace_entrypoint_chain",
        "get_security_findings",
        "query_antipatterns",
        "get_repo_scorecard",
        "check_boundary_violation",
    ]
    assert tool_names == expected_tools

    # Unknown method & unknown tool
    err_method = server.handle_message({"jsonrpc": "2.0", "id": 99, "method": "foo/bar"})
    assert err_method is not None and err_method["error"]["code"] == -32601
    err_tool = server.handle_message({
        "jsonrpc": "2.0",
        "id": 100,
        "method": "tools/call",
        "params": {"name": "nonexistent_tool", "arguments": {}},
    })
    assert err_tool is not None and err_tool["error"]["code"] == -32602

    # 2. Verify all 10 tools return structured payloads
    def _call(name: str, args: dict) -> dict:
        resp = server.handle_message({
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {"name": name, "arguments": args},
        })
        assert resp is not None
        return resp["result"]["structuredContent"]

    listed = _call("list_repositories", {"ecosystem": "Python"})
    assert listed["count"] == 1
    assert listed["repositories"][0]["repository"] == "acme/orders-api"

    arch = _call("get_repo_architecture", {"repository": "acme/orders-api"})
    assert arch["found"] is True
    assert len(arch["architecture_components"]) == 3

    missing_arch = _call("get_repo_architecture", {"repository": "missing/repo"})
    assert missing_arch["found"] is False

    pipe = _call("get_pipeline_dag", {"repository": "orders-api"})
    assert pipe["found"] is True
    assert len(pipe["workflows"]) == 1

    impacts = _call("find_cross_repo_impacts", {"target": "fastapi"})
    assert "acme/orders-api" in impacts["dependent_repositories"]

    blast_code = _call(
        "get_blast_radius",
        {"repository": "acme/orders-api", "target_node": "OrdersRepo", "scope": "code"},
    )
    assert blast_code["found"] is True
    assert blast_code["blast_radius_count"] >= 2

    blast_pipe = _call(
        "get_blast_radius",
        {"repository": "acme/orders-api", "target_node": "test", "scope": "pipeline"},
    )
    assert blast_pipe["found"] is True
    assert blast_pipe["blast_radius_count"] == 1

    chains = _call("trace_entrypoint_chain", {"repository": "acme/orders-api"})
    assert chains["entrypoints_count"] == 1
    assert "OrdersRepo" in chains["chains"][0]["reachable_components"]

    sec = _call("get_security_findings", {"severity": "HIGH"})
    assert sec["count"] == 1
    assert sec["findings"][0]["rule_id"] == "ATRUSS-PIPE-008"

    aps = _call("query_antipatterns", {"rule_id": "ATRUSS-ARCH-001"})
    assert aps["count"] == 1
    assert aps["antipatterns"][0]["source"] == "architecture"

    sc = _call("get_repo_scorecard", {"repository": "acme/orders-api"})
    assert sc["found"] is True
    assert sc["scorecard"]["overall_grade"] == "A"

    # Dynamic scorecard fallback when analysis.json has no persisted scorecard
    rep_file = latest_dir / "reports" / "acme-orders-api-analysis.json"
    rep_json = json.loads(rep_file.read_text(encoding="utf-8"))
    rep_json["scorecard"] = None
    rep_file.write_text(json.dumps(rep_json), encoding="utf-8")
    sc_dynamic = _call("get_repo_scorecard", {"repository": "acme/orders-api"})
    assert sc_dynamic["found"] is True
    assert set(sc_dynamic["scorecard"]["dimensions"].keys()) == {
        "code_quality",
        "security",
        "maintainability",
        "test_coverage",
        "dependency_health",
        "pipeline_health",
    }

    boundary = _call(
        "check_boundary_violation",
        {
            "repository": "acme/orders-api",
            "source_component": "BillingController",
            "source_layer": "API_ROUTE",
            "target_component": "OrdersRepo",
            "target_layer": "DATA_ACCESS_LAYER",
        },
    )
    assert boundary["found"] is True
    assert boundary["candidate_violated"] is True
    assert boundary["passed"] is False

    # 3. NDJSON framing via StringIO
    ndjson_in = io.StringIO(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n"
        + json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"
        + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}) + "\n"
        + "{bad-json\n"
    )
    ndjson_out = io.StringIO()
    server.serve_stdio(ndjson_in, ndjson_out)
    out_lines = [json.loads(line) for line in ndjson_out.getvalue().splitlines() if line.strip()]
    assert len(out_lines) == 3
    assert out_lines[0]["id"] == 1
    assert len(out_lines[1]["result"]["tools"]) == 10
    assert out_lines[2]["error"]["code"] == -32700

    # 4. Content-Length framing via BytesIO
    req1 = json.dumps({"jsonrpc": "2.0", "id": 7, "method": "ping"}).encode("utf-8")
    cl_in = io.BytesIO(f"Content-Length: {len(req1)}\r\n\r\n".encode("ascii") + req1)
    cl_out = io.BytesIO()
    server.serve_stdio(cl_in, cl_out)
    raw_cl = cl_out.getvalue().decode("utf-8")
    assert raw_cl.startswith("Content-Length: ")
    _hdr, body = raw_cl.split("\r\n\r\n", 1)
    assert json.loads(body)["id"] == 7

    # 5. CLI transport guard and CLI NDJSON stdin execution
    res_bad = runner.invoke(mcp_app, ["--exports-dir", str(latest_dir), "--transport", "sse"])
    assert res_bad.exit_code == 1

    cli_in = json.dumps({"jsonrpc": "2.0", "id": 42, "method": "ping"}) + "\n"
    res_cli = runner.invoke(mcp_app, ["--exports-dir", str(latest_dir)], input=cli_in)
    assert res_cli.exit_code == 0
    assert json.loads(res_cli.stdout.strip())["id"] == 42
