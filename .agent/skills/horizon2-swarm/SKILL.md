---
name: horizon2-swarm
description: Antigravity-native parallel subagent swarm workflow for implementing, verifying, and shipping Atruss Code Atlas Horizon 2 capabilities (FR-021 to FR-030) cleanly on a feature branch.
---

# Horizon 2 Antigravity Agent Swarm Workflow

Use this skill when extending, hardening, or verifying Atruss Code Atlas v2.0 Horizon 2 capabilities (`FR-021`–`FR-030`) inside `kumarshaz/atruss-code-atlas`.

## Critical Invariants
1. **Repository Isolation**: Never modify sibling reference repositories (e.g. `astruss-code-atlas-dev`). Work on a dedicated feature branch branched from `main` (never push directly to `main`).
2. **Disjoint Parallel Waves (`Workspace: "inherit"`)**: Define and invoke subagents with strictly non-overlapping file write ownership per wave so parallel workers never conflict.
3. **Zero-Stub / Zero-Skip Constitution**: Never leave `TODO` comments in Python `src/` or `tests/`, empty `pass` stubs, or `pytest.skip()` decorators. All external network lookups (`OSV.dev`, GitHub API) must support `httpx.MockTransport` and offline graceful degradation.
4. **Byte-for-Byte Determinism**: Sort keys, graph nodes/edges, findings, and SBOM serials deterministically so Gate 5 SHA-256 checks always match.

## Swarm Execution Topology

1. **Coordinator Foundation**:
   - Declare dependencies (`pyproject.toml`, `requirements.txt`), Pydantic schemas (`src/models/artifacts.py`), and archival export folders (`src/core/utils/export_manager.py`).
2. **Wave A — Parallel Domain Engines**:
   - `pipeline-security-agent`: `manifests/pipeline-rules.yaml`, `src/analyzers/pipeline/{parser,dag_builder,heuristics}.py`, pipeline unit/integration tests (`FR-021`).
   - `polyglot-ast-fitness-agent`: `manifests/architecture-rules.yaml`, `src/analyzers/code/{treesitter_engine,fitness_engine,python_ast,dotnet_structural,js_ts_structural,java_structural}.py`, AST & fitness unit tests (`FR-022`, `FR-023`).
   - `deps-osv-sbom-agent`: `src/analyzers/dependencies/{manifest_parser,osv_client,secret_scanner}.py`, `src/core/exporters/sbom_exporter.py`, dependency/SBOM tests (`FR-024`).
3. **Wave B — Platform Core, CLI & Integration**:
   - `scorecard-traceability-sarif-mcp-agent`: `src/analyzers/{scorecard,traceability,observability,drift}.py`, `src/core/exporters/{sarif_exporter,llms_exporter}.py`, `src/cli/commands/{check,diff,mcp_server}.py`, unit tests (`FR-025`–`FR-029`).
   - Coordinator integration: `src/analyzers/code/orchestrator.py`, `src/core/services/report_generator.py`, `src/core/exporters/markdown_exporter.py`, `src/cli/commands/{analyze_code,analyze_pipeline}.py`, `src/cli/main.py`.
4. **Wave C — Parallel Portal UI, Harnesses & Governance**:
   - `astro-m3-ui-agent`: `web/src/components/{ScorecardHeatmap,CrossRepoTopology,PipelineView,ArchitectureView,RepoTabs}.astro`, `web/src/styles/material-theme.css`, `web/src/content/docs/orgs/index.mdx`, `web/package.json` (`FR-030`).
   - `harness-docs-verifier-agent`: `scripts/{validate_agent_workflow,generate-report-stubs,run_benchmark_loop}.py`, `tests/integration/test_horizon2_e2e.py`, `.github/workflows/tests.yml`, `specs/009-unified-atlas-spec/{plan,tasks}.md`, `docs/agentic-sdlc-guide.md`, `README.md`.

## Mandatory Exit Gates

Run before committing or opening a PR:

```bash
.venv/bin/ruff check src/ tests/ scripts/
.venv/bin/pytest tests/ -v --strict-markers
.venv/bin/python scripts/validate_agent_workflow.py --spec specs/009-unified-atlas-spec
.venv/bin/python scripts/validate_agent_workflow.py --spec specs/006-core-unification-and-eval
cd web && npm test && npm run build && ASTRO_SITE=https://kumarshaz.github.io ASTRO_BASE=/atruss-code-atlas npm run build
```
