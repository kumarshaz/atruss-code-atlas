from pathlib import Path

import networkx as nx
import pytest

from src.analyzers.code.fitness_engine import (
    compute_component_blast_radius,
    discover_workspace_packages,
    evaluate_architecture_fitness,
    load_architecture_rules,
)


def test_load_default_and_custom_architecture_rules(tmp_path: Path):
    rules = load_architecture_rules()
    assert rules["version"] == "1.0"
    assert rules["forbid_circular_dependencies"] is True
    assert rules["require_test_gate_before_deploy"] is True
    assert rules["thresholds"]["max_cyclomatic_complexity"] == 20
    assert rules["thresholds"]["max_cognitive_complexity"] == 25
    assert rules["thresholds"]["max_duplication_pct"] == 15.0
    rule_ids = {r["rule_id"] for r in rules["layer_rules"]}
    assert {"ATRUSS-ARCH-001", "ATRUSS-ARCH-002", "ATRUSS-ARCH-003"}.issubset(rule_ids)

    custom_policy = tmp_path / "custom-rules.yaml"
    custom_policy.write_text(
        'version: "2.0"\n'
        "forbid_circular_dependencies: false\n"
        "thresholds:\n"
        "  max_cyclomatic_complexity: 5\n"
        "layer_rules: []\n",
        encoding="utf-8",
    )
    loaded_custom = load_architecture_rules(custom_policy)
    assert loaded_custom["version"] == "2.0"
    assert loaded_custom["thresholds"]["max_cyclomatic_complexity"] == 5

    with pytest.raises(FileNotFoundError):
        load_architecture_rules(tmp_path / "nonexistent-rules.yaml")


def test_layer_violations_arch_001_002_003():
    # ATRUSS-ARCH-001 triggers only when SERVICE exists in repo
    components_no_service = [
        {
            "name": "PetController",
            "type": "API_ROUTE",
            "file": "api.py",
            "dependencies": ["PetRepo"],
        },
        {
            "name": "PetRepo",
            "type": "DATA_ACCESS_LAYER",
            "file": "repo.py",
            "dependencies": [],
        },
    ]
    v_no_svc, s_no_svc = evaluate_architecture_fitness(components_no_service)
    assert v_no_svc == []
    assert s_no_svc["passed"] is True

    # Adding a SERVICE layer activates ATRUSS-ARCH-001 + tests ARCH-002 and ARCH-003
    components_violating = [
        {
            "name": "PetController",
            "type": "API_ROUTE",
            "file": "api.py",
            "dependencies": ["PetRepo"],
        },
        {
            "name": "PetCard",
            "type": "UI_COMPONENT",
            "file": "PetCard.tsx",
            "dependencies": ["PetRepo"],
        },
        {
            "name": "PetOrder",
            "type": "DOMAIN",
            "file": "domain.py",
            "dependencies": ["S3Adapter"],
        },
        {
            "name": "PetService",
            "type": "SERVICE",
            "file": "svc.py",
            "dependencies": ["PetRepo"],
        },
        {
            "name": "PetRepo",
            "type": "DATA_ACCESS_LAYER",
            "file": "repo.py",
            "dependencies": [],
        },
        {
            "name": "S3Adapter",
            "type": "INFRASTRUCTURE",
            "file": "infra.py",
            "dependencies": [],
        },
    ]
    violations, summary = evaluate_architecture_fitness(components_violating)
    assert summary["passed"] is False
    by_rule = {v.rule_id: v for v in violations}
    assert by_rule["ATRUSS-ARCH-001"].type == "LAYER_VIOLATION"
    assert by_rule["ATRUSS-ARCH-001"].severity == "HIGH"
    assert by_rule["ATRUSS-ARCH-001"].source_component == "PetController"
    assert by_rule["ATRUSS-ARCH-001"].target_component == "PetRepo"

    assert by_rule["ATRUSS-ARCH-002"].type == "LAYER_VIOLATION"
    assert by_rule["ATRUSS-ARCH-002"].severity == "HIGH"
    assert by_rule["ATRUSS-ARCH-002"].source_component == "PetCard"

    assert by_rule["ATRUSS-ARCH-003"].type == "LAYER_VIOLATION"
    assert by_rule["ATRUSS-ARCH-003"].severity == "MEDIUM"
    assert by_rule["ATRUSS-ARCH-003"].source_component == "PetOrder"


def test_circular_dependency_detection_arch_004(tmp_path: Path):
    components = [
        {
            "name": "AlphaService",
            "type": "SERVICE",
            "file": "a.py",
            "dependencies": ["BetaService"],
        },
        {
            "name": "BetaService",
            "type": "SERVICE",
            "file": "b.py",
            "dependencies": ["GammaService"],
        },
        {
            "name": "GammaService",
            "type": "SERVICE",
            "file": "c.py",
            "dependencies": ["AlphaService"],
        },
    ]
    violations, summary = evaluate_architecture_fitness(components)
    assert summary["passed"] is False
    assert summary["cycle_count"] == 1
    assert len(violations) == 1
    v = violations[0]
    assert v.rule_id == "ATRUSS-ARCH-004"
    assert v.type == "CIRCULAR_DEPENDENCY"
    assert v.severity == "HIGH"
    assert "AlphaService -> BetaService -> GammaService -> AlphaService" in v.message

    # Custom policy disabling circular dependency check
    permissive = tmp_path / "permissive.yaml"
    permissive.write_text(
        'version: "1.0"\nforbid_circular_dependencies: false\nlayer_rules: []\n',
        encoding="utf-8",
    )
    v2, s2 = evaluate_architecture_fitness(components, policy_path=permissive)
    assert v2 == []
    assert s2["passed"] is True


def test_complexity_and_duplication_threshold_violations_arch_005():
    components = [
        {"name": "HeavyService", "type": "SERVICE", "file": "heavy.py", "dependencies": []},
    ]
    bad_metrics = {
        "max_cyclomatic_complexity": 24,
        "max_cognitive_complexity": 30,
        "duplication_pct": 22.5,
        "file_complexities": [
            {"file": "heavy.py", "loc": 200, "cyclomatic": 24, "cognitive": 30}
        ],
    }
    violations, summary = evaluate_architecture_fitness(components, metrics=bad_metrics)
    assert summary["passed"] is False
    assert len(violations) == 3
    assert all(v.rule_id == "ATRUSS-ARCH-005" for v in violations)
    assert all(v.type == "COMPLEXITY_THRESHOLD" for v in violations)
    assert all(v.severity == "MEDIUM" for v in violations)
    assert all(v.file_source == "heavy.py" for v in violations)
    assert {v.target_component for v in violations} == {
        "max_cyclomatic_complexity",
        "max_cognitive_complexity",
        "duplication_pct",
    }

    clean_metrics = {
        "max_cyclomatic_complexity": 10,
        "max_cognitive_complexity": 12,
        "duplication_pct": 5.0,
    }
    v_clean, s_clean = evaluate_architecture_fitness(components, metrics=clean_metrics)
    assert v_clean == []
    assert s_clean["passed"] is True


def test_pure_python_blast_radius_pagerank_and_betweenness():
    G = nx.DiGraph()
    G.add_edges_from([
        ("WebUI", "OrderAPI"),
        ("MobileUI", "OrderAPI"),
        ("OrderAPI", "AuthService"),
        ("OrderAPI", "OrderService"),
        ("OrderService", "UserRepo"),
        ("AuthService", "UserRepo"),
    ])

    overall = compute_component_blast_radius(G)
    assert overall["node_count"] == 6
    assert overall["edge_count"] == 6
    pr = overall["pagerank"]
    assert pytest.approx(sum(pr.values()), rel=1e-4) == 1.0
    # UserRepo is the sink of all transitive dependencies, so it holds highest PageRank
    assert pr["UserRepo"] > pr["WebUI"]
    # OrderAPI / AuthService / OrderService act as bridges with positive betweenness
    assert overall["betweenness_centrality"]["OrderAPI"] > 0.0

    targeted = compute_component_blast_radius(G, target_node="UserRepo")
    assert targeted["target_found"] is True
    assert targeted["blast_radius_count"] == 5
    assert targeted["impacted_nodes"] == [
        "AuthService",
        "MobileUI",
        "OrderAPI",
        "OrderService",
        "WebUI",
    ]
    assert targeted["direct_dependents"] == ["AuthService", "OrderService"]
    assert targeted["blast_radius_pct"] == 100.0

    missing = compute_component_blast_radius(G, target_node="NonExistent")
    assert missing["target_found"] is False
    assert missing["blast_radius_count"] == 0
    assert missing["impacted_nodes"] == []

    empty_res = compute_component_blast_radius(nx.DiGraph())
    assert empty_res["node_count"] == 0
    assert empty_res["pagerank"] == {}


def test_discover_workspace_packages_pnpm_and_npm_and_turbo_and_nx(tmp_path: Path):
    # 1. pnpm-workspace.yaml
    pnpm_repo = tmp_path / "pnpm_ws"
    (pnpm_repo / "packages" / "core").mkdir(parents=True)
    (pnpm_repo / "packages" / "ignored").mkdir(parents=True)
    (pnpm_repo / "apps" / "web").mkdir(parents=True)
    (pnpm_repo / "pnpm-workspace.yaml").write_text(
        "packages:\n  - 'packages/*'\n  - 'apps/*'\n  - '!packages/ignored'\n",
        encoding="utf-8",
    )
    (pnpm_repo / "packages" / "core" / "package.json").write_text(
        '{"name": "@acme/core"}', encoding="utf-8"
    )
    (pnpm_repo / "packages" / "ignored" / "package.json").write_text(
        '{"name": "@acme/ignored"}', encoding="utf-8"
    )
    (pnpm_repo / "apps" / "web" / "package.json").write_text(
        '{"name": "@acme/web", "dependencies": {"@acme/core": "workspace:*", "react": "^18"}}',
        encoding="utf-8",
    )
    pnpm_pkgs = discover_workspace_packages(pnpm_repo)
    assert [(p.name, p.path, p.manager, p.internal_dependencies) for p in pnpm_pkgs] == [
        ("@acme/web", "apps/web", "pnpm", ["@acme/core"]),
        ("@acme/core", "packages/core", "pnpm", []),
    ]

    # 2. package.json workspaces (object form)
    npm_repo = tmp_path / "npm_ws"
    (npm_repo / "libs" / "utils").mkdir(parents=True)
    (npm_repo / "services" / "api").mkdir(parents=True)
    (npm_repo / "package.json").write_text(
        '{"name": "root", "workspaces": {"packages": ["libs/*", "services/*"]}}',
        encoding="utf-8",
    )
    (npm_repo / "libs" / "utils" / "package.json").write_text(
        '{"name": "utils-pkg"}', encoding="utf-8"
    )
    (npm_repo / "services" / "api" / "package.json").write_text(
        '{"name": "api-pkg", "dependencies": {"utils-pkg": "1.0.0"}}',
        encoding="utf-8",
    )
    npm_pkgs = discover_workspace_packages(npm_repo)
    assert [(p.name, p.manager, p.internal_dependencies) for p in npm_pkgs] == [
        ("utils-pkg", "npm", []),
        ("api-pkg", "npm", ["utils-pkg"]),
    ]

    # 3. turbo.json standalone
    turbo_repo = tmp_path / "turbo_ws"
    (turbo_repo / "apps" / "portal").mkdir(parents=True)
    (turbo_repo / "packages" / "ui").mkdir(parents=True)
    (turbo_repo / "turbo.json").write_text('{"tasks": {"build": {}}}', encoding="utf-8")
    (turbo_repo / "packages" / "ui" / "package.json").write_text(
        '{"name": "@t/ui"}', encoding="utf-8"
    )
    (turbo_repo / "apps" / "portal" / "package.json").write_text(
        '{"name": "@t/portal", "dependencies": {"@t/ui": "*"}}', encoding="utf-8"
    )
    turbo_pkgs = discover_workspace_packages(turbo_repo)
    assert [(p.name, p.manager, p.internal_dependencies) for p in turbo_pkgs] == [
        ("@t/portal", "turborepo", ["@t/ui"]),
        ("@t/ui", "turborepo", []),
    ]

    # 4. nx.json + project.json
    nx_repo = tmp_path / "nx_ws"
    (nx_repo / "apps" / "store").mkdir(parents=True)
    (nx_repo / "libs" / "shared").mkdir(parents=True)
    (nx_repo / "nx.json").write_text(
        '{"workspaceLayout": {"appsDir": "apps", "libsDir": "libs"}}',
        encoding="utf-8",
    )
    (nx_repo / "libs" / "shared" / "project.json").write_text(
        '{"name": "shared-lib"}', encoding="utf-8"
    )
    (nx_repo / "apps" / "store" / "project.json").write_text(
        '{"name": "store-app", "implicitDependencies": ["shared-lib", "!ignored"]}',
        encoding="utf-8",
    )
    nx_pkgs = discover_workspace_packages(nx_repo)
    assert [(p.name, p.manager, p.internal_dependencies) for p in nx_pkgs] == [
        ("store-app", "nx", ["shared-lib"]),
        ("shared-lib", "nx", []),
    ]


def test_discover_workspace_packages_cargo_go_and_uv(tmp_path: Path):
    # 5. Cargo.toml [workspace]
    cargo_repo = tmp_path / "cargo_ws"
    (cargo_repo / "crates" / "core").mkdir(parents=True)
    (cargo_repo / "crates" / "cli").mkdir(parents=True)
    (cargo_repo / "crates" / "skipme").mkdir(parents=True)
    (cargo_repo / "Cargo.toml").write_text(
        '[workspace]\nmembers = ["crates/*"]\nexclude = ["crates/skipme"]\n',
        encoding="utf-8",
    )
    (cargo_repo / "crates" / "core" / "Cargo.toml").write_text(
        '[package]\nname = "atlas-core"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    (cargo_repo / "crates" / "skipme" / "Cargo.toml").write_text(
        '[package]\nname = "atlas-skip"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    (cargo_repo / "crates" / "cli" / "Cargo.toml").write_text(
        '[package]\nname = "atlas-cli"\nversion = "0.1.0"\n'
        '[dependencies]\natlas-core = { path = "../core" }\nserde = "1.0"\n',
        encoding="utf-8",
    )
    cargo_pkgs = discover_workspace_packages(cargo_repo)
    assert [(p.name, p.ecosystem, p.manager, p.internal_dependencies) for p in cargo_pkgs] == [
        ("atlas-cli", "rust", "cargo", ["atlas-core"]),
        ("atlas-core", "rust", "cargo", []),
    ]

    # 6. go.work
    go_repo = tmp_path / "go_ws"
    (go_repo / "libs" / "common").mkdir(parents=True)
    (go_repo / "services" / "billing").mkdir(parents=True)
    (go_repo / "go.work").write_text(
        "go 1.22\n\n"
        "use (\n"
        "    ./libs/common // shared lib\n"
        ")\n"
        "use ./services/billing\n",
        encoding="utf-8",
    )
    (go_repo / "libs" / "common" / "go.mod").write_text(
        "module github.com/acme/common\n\ngo 1.22\n",
        encoding="utf-8",
    )
    (go_repo / "services" / "billing" / "go.mod").write_text(
        "module github.com/acme/billing\n\n"
        "require (\n"
        "    github.com/acme/common v0.0.0\n"
        "    github.com/stretchr/testify v1.9.0\n"
        ")\n",
        encoding="utf-8",
    )
    go_pkgs = discover_workspace_packages(go_repo)
    assert [(p.name, p.ecosystem, p.manager, p.internal_dependencies) for p in go_pkgs] == [
        ("github.com/acme/common", "go", "go", []),
        ("github.com/acme/billing", "go", "go", ["github.com/acme/common"]),
    ]

    # 7. pyproject.toml [tool.uv.workspace]
    uv_repo = tmp_path / "uv_ws"
    (uv_repo / "packages" / "core_lib").mkdir(parents=True)
    (uv_repo / "services" / "api").mkdir(parents=True)
    (uv_repo / "pyproject.toml").write_text(
        '[project]\nname = "uv-root"\nversion = "0.1.0"\n'
        '[tool.uv.workspace]\nmembers = ["packages/*", "services/*"]\n',
        encoding="utf-8",
    )
    (uv_repo / "packages" / "core_lib" / "pyproject.toml").write_text(
        '[project]\nname = "acme-core"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    (uv_repo / "services" / "api" / "pyproject.toml").write_text(
        '[project]\nname = "acme-api"\nversion = "0.1.0"\n'
        'dependencies = ["acme_core>=0.1.0", "fastapi>=0.110"]\n',
        encoding="utf-8",
    )
    uv_pkgs = discover_workspace_packages(uv_repo)
    assert [(p.name, p.ecosystem, p.manager, p.internal_dependencies) for p in uv_pkgs] == [
        ("acme-core", "python", "uv", []),
        ("acme-api", "python", "uv", ["acme-core"]),
    ]


def test_fitness_engine_bridges_import_edges_and_is_deterministic():
    components = [
        {"name": "RouteHandler", "type": "API_ROUTE", "file": "routes.py", "dependencies": []},
        {"name": "BizService", "type": "SERVICE", "file": "service.py", "dependencies": []},
        {"name": "DbModel", "type": "DATA_ACCESS_LAYER", "file": "models.py", "dependencies": []},
    ]
    metrics = {
        "import_edges": [
            {"source_file": "routes.py", "target_symbol": "DbModel", "confidence": 1.0}
        ]
    }
    v1, s1 = evaluate_architecture_fitness(components, metrics=metrics)
    v2, s2 = evaluate_architecture_fitness(components, metrics=metrics)
    assert v1 == v2
    assert s1 == s2
    assert len(v1) == 1
    assert v1[0].rule_id == "ATRUSS-ARCH-001"
    assert v1[0].source_component == "RouteHandler"
    assert v1[0].target_component == "DbModel"
