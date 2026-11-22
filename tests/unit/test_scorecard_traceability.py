from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.analyzers.observability import apply_observability_overlay, parse_otel_traces
from src.analyzers.scorecard import (
    DIMENSION_WEIGHTS,
    compute_repository_scorecard,
    score_to_grade,
)
from src.analyzers.traceability import (
    extract_code_to_cloud_traceability,
    render_code_to_cloud_mermaid,
)
from src.models.artifacts import (
    DependencyRecord,
    FitnessViolation,
    PipelineWorkflow,
    SecretFinding,
    VulnerabilityRecord,
    WorkspacePackage,
)


def test_score_to_grade_boundaries() -> None:
    assert score_to_grade(100.0) == "A"
    assert score_to_grade(90.0) == "A"
    assert score_to_grade(89.99) == "B"
    assert score_to_grade(80.0) == "B"
    assert score_to_grade(79.99) == "C"
    assert score_to_grade(70.0) == "C"
    assert score_to_grade(69.99) == "D"
    assert score_to_grade(60.0) == "D"
    assert score_to_grade(59.99) == "F"
    assert score_to_grade(0.0) == "F"


def test_scorecard_clean_repository_and_weights() -> None:
    weight_sum = sum(w for _, w in DIMENSION_WEIGHTS.values())
    assert weight_sum == pytest.approx(1.0)

    clean_pipeline = PipelineWorkflow(
        id="ci.yml",
        name="CI",
        triggers=["pull_request"],
        jobs={
            "lint": {"runs-on": "ubuntu-latest", "steps": [{"run": "ruff check"}]},
            "test": {"runs-on": "ubuntu-latest", "steps": [{"run": "pytest"}]},
        },
        dag_metrics={"node_count": 2, "edge_count": 0, "max_depth": 0, "is_valid_dag": True},
        anti_patterns=[],
    )
    clean_deps = [
        DependencyRecord(
            name="fastapi",
            version="0.110.0",
            ecosystem="PyPI",
            purl="pkg:pypi/fastapi@0.110.0",
            manifest_file="uv.lock",
            line=10,
            is_direct=True,
        ),
        DependencyRecord(
            name="pydantic",
            version="2.6.0",
            ecosystem="PyPI",
            purl="pkg:pypi/pydantic@2.6.0",
            manifest_file="uv.lock",
            line=20,
            is_direct=True,
        ),
    ]
    metrics = {
        "avg_cyclomatic_complexity": 2.1,
        "max_cyclomatic_complexity": 8,
        "avg_cognitive_complexity": 3.0,
        "max_cognitive_complexity": 10,
        "duplication_pct": 0.0,
        "dead_code_count": 0,
        "file_complexities": [{"file": "src/app.py", "loc": 120}],
    }

    scorecard = compute_repository_scorecard(
        metrics=metrics,
        components=[{"name": "AppService", "type": "SERVICE", "file": "src/app.py"}],
        pipelines=[clean_pipeline],
        dependencies=clean_deps,
        vulnerabilities=[],
        secrets=[],
        fitness_violations=[],
        coverage_percent=94.0,
    )

    assert set(scorecard.dimensions.keys()) == set(DIMENSION_WEIGHTS.keys())
    assert scorecard.overall_grade == "A"
    assert scorecard.overall_score >= 90.0
    assert scorecard.technical_debt_score == pytest.approx(
        round(100.0 - scorecard.overall_score, 2)
    )
    assert scorecard.dimensions["code_quality"].grade == "A"
    assert scorecard.dimensions["security"].grade == "A"
    assert scorecard.dimensions["maintainability"].grade == "A"
    assert scorecard.dimensions["test_coverage"].score == pytest.approx(99.0)
    assert scorecard.dimensions["dependency_health"].grade == "A"
    assert scorecard.dimensions["pipeline_health"].score == 100.0


def test_scorecard_penalized_repository_and_fallbacks() -> None:
    bad_pipeline = PipelineWorkflow(
        id="deploy.yml",
        name="Deploy",
        triggers=["push"],
        jobs={
            "deploy": {"runs-on": "ubuntu-latest", "steps": [{"run": "echo deploy"}]},
        },
        dag_metrics={"node_count": 1, "edge_count": 0, "max_depth": 0, "is_valid_dag": True},
        anti_patterns=[
            {
                "rule_id": "ATRUSS-PIPE-001",
                "type": "NO_TEST_GATE",
                "severity": "CRITICAL",
                "message": "No upstream test job",
            },
            {
                "rule_id": "ATRUSS-PIPE-009",
                "type": "TEMPLATE_INJECTION",
                "severity": "CRITICAL",
                "message": "Untrusted shell interpolation",
            },
        ],
    )
    bad_deps = [
        DependencyRecord(
            name="requests",
            version="2.19.0",
            ecosystem="PyPI",
            purl="pkg:pypi/requests@2.19.0",
            manifest_file="requirements.txt",
            line=1,
            is_direct=True,
            is_outdated=True,
            vulnerability_ids=["GHSA-1234"],
        ),
    ]
    vulns = [
        VulnerabilityRecord(
            id="GHSA-1234",
            package="requests",
            installed_version="2.19.0",
            ecosystem="PyPI",
            purl="pkg:pypi/requests@2.19.0",
            severity="CRITICAL",
            summary="Critical vulnerability",
        ),
    ]
    secrets = [
        SecretFinding(
            rule_id="ATRUSS-SEC-001",
            type="AWS_ACCESS_KEY",
            severity="CRITICAL",
            file_source="config.py",
            start_line=4,
            end_line=4,
            redacted_snippet="AKIA***REDACTED***",
            entropy=4.2,
            message="Hardcoded key",
        )
    ]
    fitness = [
        FitnessViolation(
            rule_id="ATRUSS-ARCH-001",
            type="LAYER_VIOLATION",
            severity="HIGH",
            source_component="ApiController",
            target_component="UserRepo",
            file_source="api.py",
            message="Layer violation",
        )
    ]
    metrics = {
        "avg_cyclomatic_complexity": 10.0,
        "max_cyclomatic_complexity": 32,
        "avg_cognitive_complexity": 14.0,
        "max_cognitive_complexity": 40,
        "duplication_pct": 18.0,
        "dead_code_count": 12,
        "file_complexities": [{"file": "src/god.py", "loc": 900}],
    }

    sc = compute_repository_scorecard(
        metrics=metrics,
        components=[],
        pipelines=[bad_pipeline],
        dependencies=bad_deps,
        vulnerabilities=vulns,
        secrets=secrets,
        fitness_violations=fitness,
        coverage_percent=35.0,
    )

    assert sc.overall_grade == "F"
    assert sc.overall_score < 60.0
    assert sc.technical_debt_score == pytest.approx(round(100.0 - sc.overall_score, 2))
    assert sc.remediation_hours > 15.0
    assert sc.dimensions["security"].grade == "F"
    assert sc.dimensions["dependency_health"].grade == "F"
    assert sc.dimensions["pipeline_health"].score == pytest.approx(80.0)

    expected_overall = round(
        sum(dim.score * dim.weight for dim in sc.dimensions.values()), 2
    )
    assert sc.overall_score == pytest.approx(expected_overall)

    # Fallback defaults when empty
    empty_sc = compute_repository_scorecard()
    assert empty_sc.dimensions["dependency_health"].score == 90.0
    assert empty_sc.dimensions["pipeline_health"].score == 40.0
    assert empty_sc.dimensions["test_coverage"].score == 40.0

    # Test files present without coverage_percent -> 70.0
    test_file_sc = compute_repository_scorecard(
        components=[{"name": "test_app", "type": "FUNCTION", "file": "tests/test_app.py"}]
    )
    assert test_file_sc.dimensions["test_coverage"].score == 70.0


def test_code_to_cloud_traceability_monorepo_and_mermaid(tmp_path: Path) -> None:
    api_dir = tmp_path / "services" / "api"
    api_dir.mkdir(parents=True)
    (api_dir / "pyproject.toml").write_text('[project]\nname = "orders-api"\n', encoding="utf-8")
    (api_dir / "Dockerfile").write_text("FROM python:3.11-slim\nCOPY . /app\n", encoding="utf-8")

    web_dir = tmp_path / "services" / "web"
    web_dir.mkdir(parents=True)
    (web_dir / "package.json").write_text('{"name": "storefront-web"}', encoding="utf-8")

    k8s_dir = tmp_path / "k8s"
    k8s_dir.mkdir()
    (k8s_dir / "api-deployment.yaml").write_text(
        "kind: Deployment\nmetadata:\n  name: orders-api\n",
        encoding="utf-8",
    )

    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "deploy.yml").write_text(
        """
name: Deploy Monorepo
on:
  push:
    branches: [main]
jobs:
  build-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run API tests
        working-directory: services/api
        run: pytest
      - name: Build image
        run: docker build -f services/api/Dockerfile services/api
  deploy-api:
    needs: [build-api]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy k8s
        run: kubectl apply -f k8s/api-deployment.yaml
  deploy-web:
    runs-on: ubuntu-latest
    steps:
      - name: Build web
        working-directory: services/web
        run: npm run build
      - uses: actions/deploy-pages@v4
""",
        encoding="utf-8",
    )

    workspace_pkgs = [
        WorkspacePackage(name="orders-api", path="services/api", ecosystem="python", manager="uv"),
        WorkspacePackage(
            name="storefront-web", path="services/web", ecosystem="react_ts_js", manager="pnpm"
        ),
    ]
    edges = extract_code_to_cloud_traceability(
        tmp_path,
        workspace_packages=workspace_pkgs,
    )
    assert edges

    rels = {(e.source, e.relationship, e.target) for e in edges}
    assert ("services/api", "PACKAGED_BY", "services/api/Dockerfile") in rels
    assert ("services/api", "PACKAGED_BY", "k8s/api-deployment.yaml") in rels
    assert ("services/api", "BUILT_BY", "deploy.yml#build-api") in rels
    assert ("services/api/Dockerfile", "BUILT_BY", "deploy.yml#build-api") in rels
    assert ("k8s/api-deployment.yaml", "DEPLOYED_BY", "deploy.yml#deploy-api") in rels
    assert ("deploy.yml#deploy-api", "DEPLOYS_TO", "production") in rels
    assert ("deploy.yml#deploy-api", "DEPLOYS_TO", "kubernetes") in rels
    assert ("services/web", "DEPLOYED_BY", "deploy.yml#deploy-web") in rels
    assert ("deploy.yml#deploy-web", "DEPLOYS_TO", "github-pages") in rels

    # Determinism check
    edges_repeat = extract_code_to_cloud_traceability(tmp_path, workspace_packages=workspace_pkgs)
    assert [e.model_dump() for e in edges] == [e.model_dump() for e in edges_repeat]

    mermaid = render_code_to_cloud_mermaid(edges)
    assert mermaid.startswith("flowchart LR")
    assert "%% title: Code-to-Cloud Deployment Traceability" in mermaid
    assert 'subgraph code_modules["Code Modules"]' in mermaid
    assert 'subgraph build_artifacts["Build Artifacts / Containers"]' in mermaid
    assert 'subgraph ci_jobs["CI/CD Jobs"]' in mermaid
    assert 'subgraph runtime_envs["Runtime Environments"]' in mermaid
    assert "-->|PACKAGED_BY|" in mermaid
    assert "-->|BUILT_BY|" in mermaid
    assert "-->|DEPLOYS_TO|" in mermaid
    assert render_code_to_cloud_mermaid([]) == ""


def test_observability_overlay_otel_and_coverage_formats(tmp_path: Path) -> None:
    otel_file = tmp_path / "traces.json"
    otel_file.write_text(
        json.dumps({
            "resourceSpans": [
                {
                    "scopeSpans": [
                        {
                            "spans": [
                                {
                                    "name": "POST /orders",
                                    "attributes": [
                                        {
                                            "key": "code.function",
                                            "value": {"stringValue": "create_order"},
                                        },
                                        {
                                            "key": "http.route",
                                            "value": {"stringValue": "/orders"},
                                        },
                                    ],
                                },
                                {
                                    "name": "OrderService.process",
                                    "attributes": {
                                        "code.namespace": "app.services.OrderService",
                                        "code.filepath": "src/services/order_service.py",
                                    },
                                },
                            ]
                        }
                    ]
                }
            ]
        }),
        encoding="utf-8",
    )

    trace_counts = parse_otel_traces(otel_file)
    assert trace_counts["create_order"] == 1
    assert trace_counts["/orders"] == 1
    assert trace_counts["app.services.OrderService"] == 1
    assert trace_counts["src/services/order_service.py"] == 1

    # Jest coverage-summary.json
    jest_cov = tmp_path / "coverage-summary.json"
    jest_cov.write_text(
        json.dumps({
            "total": {"statements": {"pct": 75.0}},
            "src/api/orders.py": {"statements": {"pct": 100}},
            "src/services/billing_service.py": {"statements": {"pct": 80}},
            "src/legacy/unused.py": {"statements": {"pct": 0}},
        }),
        encoding="utf-8",
    )

    components = [
        {"name": "create_order", "type": "API_ROUTE", "file": "src/api/orders.py"},
        {"name": "OrderService", "type": "SERVICE", "file": "src/services/order_service.py"},
        {
            "name": "BillingService",
            "type": "SERVICE",
            "file": "src/services/billing_service.py",
        },
        {"name": "UnusedHelper", "type": "SERVICE", "file": "src/legacy/unused.py"},
    ]

    # Disabled when neither path is passed
    disabled = apply_observability_overlay(components)
    assert disabled == {
        "enabled": False,
        "hot_paths": 0,
        "covered_static": 0,
        "dead_unobserved": 0,
    }

    summary = apply_observability_overlay(
        components,
        otel_traces_path=otel_file,
        coverage_path=jest_cov,
    )
    assert summary["enabled"] is True
    assert summary["runner"] == "jest"
    assert summary["coverage_percent"] == 75.0
    assert summary["hot_paths"] == 2
    assert summary["covered_static"] == 1
    assert summary["dead_unobserved"] == 1
    assert summary["component_statuses"] == {
        "BillingService": "COVERED_STATIC",
        "OrderService": "HOT_PATH",
        "UnusedHelper": "DEAD_UNOBSERVED",
        "create_order": "HOT_PATH",
    }
    assert components[0]["observability_status"] == "HOT_PATH"
    assert components[2]["observability_status"] == "COVERED_STATIC"
    assert components[3]["observability_status"] == "DEAD_UNOBSERVED"

    # LCOV format support
    lcov_file = tmp_path / "lcov.info"
    lcov_file.write_text(
        "SF:src/services/billing_service.py\nLF:10\nLH:8\nend_of_record\n"
        "SF:src/legacy/unused.py\nLF:10\nLH:0\nend_of_record\n",
        encoding="utf-8",
    )
    lcov_summary = apply_observability_overlay(
        [dict(c) for c in components],
        coverage_path=lcov_file,
    )
    assert lcov_summary["runner"] == "lcov"
    assert lcov_summary["coverage_percent"] == 40.0
    assert lcov_summary["component_statuses"]["BillingService"] == "COVERED_STATIC"
    assert lcov_summary["component_statuses"]["UnusedHelper"] == "DEAD_UNOBSERVED"

    # Cobertura XML support
    cob_file = tmp_path / "cobertura.xml"
    cob_file.write_text(
        '<?xml version="1.0" ?>'
        '<coverage line-rate="0.65">'
        "<packages><package><classes>"
        '<class name="Billing" filename="src/services/billing_service.py" line-rate="0.9"/>'
        '<class name="Unused" filename="src/legacy/unused.py" line-rate="0.0"/>'
        "</classes></package></packages>"
        "</coverage>",
        encoding="utf-8",
    )
    cob_summary = apply_observability_overlay(
        [dict(c) for c in components],
        coverage_path=cob_file,
    )
    assert cob_summary["runner"] == "cobertura"
    assert cob_summary["coverage_percent"] == 65.0
    assert cob_summary["component_statuses"]["BillingService"] == "COVERED_STATIC"
    assert cob_summary["component_statuses"]["UnusedHelper"] == "DEAD_UNOBSERVED"
