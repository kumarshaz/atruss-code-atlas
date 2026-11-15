# Tasks: Atruss Code Atlas Unified Specification (001–008 Baseline + Horizon 2 Top 10)

**Input**: Unified SpecKit Specification ([`spec.md`](./spec.md)) and Implementation Plan ([`plan.md`](./plan.md))

## Phase 1: Baseline Foundation & Core Pipeline (Iterations 001–004) — COMPLETED

- [x] T001 [US1] Implement shallow git clone (`--depth 1`) and local path ingestion with read-only target integrity in `src/core/utils/git_cloner.py` and `src/cli/commands/discover.py` (FR-001)
- [x] T002 [US1] Implement multi-ecosystem manifest detector in `src/analyzers/classification.py` (FR-002)
- [x] T003 [US1] Implement manifest and lockfile dependency extraction in `src/analyzers/code/orchestrator.py` (FR-003)
- [x] T004 [US1] Implement CI/CD workflow trigger and job step parser in `src/analyzers/pipeline/parser.py` (FR-004)
- [x] T005 [US1] Implement sanitized Mermaid `graph TD` diagram generator in `src/core/services/report_generator.py` (FR-005)
- [x] T006 [US2] Implement cross-script import and structural call extractor in `src/analyzers/code/python_ast.py` and `src/analyzers/code/js_ts_structural.py` (FR-006)
- [x] T007 [US2] Implement end-to-end `Trigger -> Entrypoint -> Script -> Dependency` DAG builder with circular dependency (`CYCLE_DETECTED`) and dead-code (`ORPHAN_NODE`) detection in `src/analyzers/pipeline/dag_builder.py` (FR-007)
- [x] T008 [US2] Implement structural anti-pattern rule engine (`AP-001` through `AP-007`) with concrete remediation recommendations in `src/analyzers/pipeline/heuristics.py` (FR-008)
- [x] T009 [US2] Implement dependency vulnerability scanner with graceful degradation and local cache fallback in `src/analyzers/code/orchestrator.py` (FR-009)
- [x] T010 [US2] Implement transitive blast-radius impact calculator in `src/analyzers/pipeline/dag_builder.py` (FR-010)
- [x] T011 [US2] Implement 6-Dimension A–F Weighted Health Scorecard (`Dependency Health`, `Security`, `Architecture`, `CI/CD`, `Maintainability`, `Test Coverage`) in `src/core/services/report_generator.py` (FR-011)
- [x] T012 [US1] Implement progressive-disclosure Arc42 + Mermaid Markdown report generator in `src/core/exporters/markdown_exporter.py` and `src/core/services/report_generator.py` (FR-012)
- [x] T013 [US2] Implement schema-validated JSON report exporter in `src/core/exporters/discovery_exporter.py`, `src/core/exporters/pipeline_exporter.py`, and `src/core/utils/json_exporter.py` (FR-013)

## Phase 2: Astro Starlight Portal, Core Unification & 100-Repo Benchmark (Iterations 005–008) — COMPLETED

- [x] T014 [US3] Implement Astro Starlight MDX artifact generator in `scripts/generate-report-stubs.py` (FR-014)
- [x] T015 [US2] Externalize ecosystem and 27-column archetype definitions to `manifests/ecosystems.yaml` with typed loader `src/analyzers/classification.py` (FR-015)
- [x] T016 [US2] Implement 4-ecosystem structural analyzers (`src/analyzers/code/python_ast.py`, `src/analyzers/code/dotnet_structural.py`, `src/analyzers/code/js_ts_structural.py`, `src/analyzers/code/java_structural.py`) orchestrated by `src/analyzers/code/orchestrator.py` (FR-016)
- [x] T017 [US3] Implement multi-repository catalog aggregation and client-side search/filter cards in `scripts/generate-report-stubs.py` and `web/src/content/docs/index.mdx` (FR-017)
- [x] T018 [US2] Implement 5-Gate Architectural Conformance Validator in `scripts/validate_agent_workflow.py` enforcing Spec-to-Task parity, AST Anti-Stub/Anti-Skip Audit, Full Pytest Execution with 0 skipped tests, Python-to-Astro Schema Contract, and SHA-256 Determinism (FR-018, SC-001, SC-002, SC-003)
- [x] T019 [US6] Implement Material Design 3 token system (`web/src/styles/material-theme.css`) and dynamic GitHub Pages `ASTRO_BASE` routing (`web/astro.config.mjs`) (FR-017, FR-018)
- [x] T020 [US7] Implement 100-Repository Public GitHub Benchmark harness and stratified evaluation report generator in `scripts/run_benchmark_loop.py`, `src/cli/commands/benchmark.py`, and `tests/integration/test_benchmark_e2e.py` (FR-019, FR-020, SC-010)

## Phase 3: Horizon 2 Top 10 Strategic Enhancements (`FR-021`–`FR-030`) — COMPLETED

- [x] T021 [P] [US8] Implement CI/CD Workflow Security Static Analyzer (`UNPINNED_ACTION`, `TEMPLATE_INJECTION`, `PWN_REQUEST_RISK`, `EXCESSIVE_PERMISSIONS`, `NO_TIMEOUT`, `ARTIFACT_CREDENTIAL_PERSISTENCE`, `STATIC_CLOUD_CREDENTIALS`) and `workflow_call`/`workflow_run` cross-workflow DAG edges in `manifests/pipeline-rules.yaml`, `src/analyzers/pipeline/parser.py`, `src/analyzers/pipeline/heuristics.py`, `src/analyzers/pipeline/dag_builder.py`, and `tests/unit/test_pipeline_security.py` (FR-021, SC-004)
- [x] T022 [P] [US9] Integrate `tree-sitter` polyglot syntax-tree analysis across Python, C#, TypeScript/JS, and Java computing Cyclomatic Complexity, Cognitive Complexity, AST Clone Duplication %, Dead Code symbols, and import edges in `src/analyzers/code/treesitter_engine.py`, `src/analyzers/code/{python_ast,dotnet_structural,js_ts_structural,java_structural}.py`, and `tests/unit/test_treesitter_engine.py` (FR-022, SC-002)
- [x] T023 [P] [US10] Implement declarative architectural layer fitness rules, cycle detection (`nx.simple_cycles`), monorepo workspace package discovery (`pnpm`/`turbo`/`nx`/`cargo`/`go.work`/`uv`), and PageRank/Betweenness blast radius in `manifests/architecture-rules.yaml`, `src/analyzers/code/fitness_engine.py`, and `tests/unit/test_fitness_engine.py` (FR-023)
- [x] T024 [P] [US11] Implement polyglot lockfile/manifest parser, offline-safe `OSV.dev` `/v1/querybatch` CVE scanner with reachability tagging, redacted secret scanner, and CycloneDX v1.6 SBOM exporter (`exports/latest/sbom/{org}-{repo}.cdx.json`) in `src/analyzers/dependencies/{manifest_parser,osv_client,secret_scanner}.py`, `src/core/exporters/sbom_exporter.py`, and `tests/unit/test_dependencies_osv_sbom.py` (FR-024, SC-008)
- [x] T025 [P] [US12] Implement deterministic 6-Dimension A–F Repository Scorecard (*Code Quality*, *Security*, *Maintainability*, *Test Coverage*, *Dependency Health*, *Pipeline Health*) and Composite Technical Debt Score (`0–100`) in `src/analyzers/scorecard.py`, `src/models/artifacts.py`, and `tests/unit/test_scorecard_traceability.py` (FR-025, SC-008)
- [x] T026 [P] [US12] Implement Arc42 Section 7 Code-to-Cloud Deployment Traceability Graph linking code submodules, `Dockerfile`/K8s/Terraform manifests, CI/CD jobs, and runtime environments plus OpenTelemetry/coverage overlay (`--otel-traces`, `--coverage`) in `src/analyzers/traceability.py`, `src/analyzers/observability.py`, `src/core/services/report_generator.py`, and `tests/unit/test_scorecard_traceability.py` (FR-026, SC-005)
- [x] T027 [P] [US13] Implement longitudinal snapshot drift engine and `atruss diff --baseline <dir1> --target <dir2>` command emitting `exports/latest/drift/drift_report.{json,md}` (`--fail-on-regression`) in `src/analyzers/drift.py`, `src/cli/commands/diff.py`, `src/cli/commands/analyze_code.py`, and `tests/unit/test_drift_sarif_mcp.py` (FR-027)
- [x] T028 [P] [US13] Implement OASIS SARIF v2.1.0 exporter (`exports/latest/sarif/{org}-{repo}.sarif.json`) and offline PR quality gate (`atruss check --sarif --fail-on`) in `src/core/exporters/sarif_exporter.py`, `src/cli/commands/check.py`, `src/cli/commands/analyze_code.py`, `src/cli/commands/analyze_pipeline.py`, and `tests/unit/test_drift_sarif_mcp.py` (FR-028, SC-008)
- [x] T029 [P] [US13] Implement AI agent context exporter (`exports/latest/llms/llms.txt` and `llms-full.txt`) and read-only stdio MCP server (`atruss mcp`) with 10 tools over `exports/latest/` in `src/core/exporters/llms_exporter.py`, `src/cli/commands/mcp_server.py`, `src/cli/main.py`, and `tests/unit/test_drift_sarif_mcp.py` (FR-029, SC-006)
- [x] T030 [P] [US13] Implement client-side SVG/PNG Mermaid exports (`web/src/lib/mermaid-client.ts`, `PipelineView.astro`, `ArchitectureView.astro`), multi-tab Print/PDF styling (`web/src/styles/material-theme.css`, `RepoTabs.astro`), 6-D Scorecard & Complexity Heatmap (`ScorecardHeatmap.astro`, `scripts/generate-report-stubs.py`), Cross-Repo Topology Explorer (`CrossRepoTopology.astro`, `LeaderboardView.astro`, `OrgComparisonTable.astro`), and end-to-end verification in `tests/integration/test_horizon2_e2e.py`, `scripts/validate_agent_workflow.py`, `web/src/tests/AtlasSummary.test.ts`, and `web/src/tests/schema.test.ts` (FR-030, SC-007, SC-009)
