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
- [x] T019 [US3] Implement Material Design 3 token system (`web/src/styles/custom.css`) and dynamic GitHub Pages `BASE_PATH` routing (`web/astro.config.mjs`) (FR-019)
- [x] T020 [US2] Implement 100-Repository Public GitHub Benchmark harness and stratified evaluation report generator in `scripts/run_public_100_eval.py` and `tests/integration/test_public_100_eval.py` (FR-020)

## Phase 3: Horizon 2 Top 10 Strategic Enhancements (v2.1 – v2.3 Backlog)

- [ ] T021 [P] [US4] Implement hybrid Tree-sitter Polyglot AST & Cross-File Call Graph Resolution for Python, JS/TS, Go, Rust, Bash, and HCL with edge confidence scores (`1.0`, `0.8`, `0.5`) in `src/analyzers/code/orchestrator.py` (FR-021, SC-004)
- [ ] T022 [P] [US5] Implement CI/CD Workflow Security Static Analyzer (`AP-008`–`AP-014`: `pull_request_target` injection, unpinned actions, excessive `GITHUB_TOKEN` permissions, insecure `GITHUB_ENV`, artifact poisoning, self-hosted runner exposure, cache poisoning) in `src/analyzers/pipeline/heuristics.py` (FR-022, SC-005)
- [ ] T023 [P] [US6] Upgrade vulnerability engine in `src/analyzers/code/orchestrator.py` to query OSV.dev Batch API (`/v1/querybatch`) as primary source, add CycloneDX v1.5 / SPDX v2.3 SBOM exporter (`--sbom`), and tag CVEs with DAG reachability (`REACHABLE_FROM_CI`, `REACHABLE_FROM_RUNTIME`, `UNREACHABLE_DORMANT`) (FR-023)
- [ ] T024 [P] [US7] Implement Diff-Aware Incremental PR Architecture Delta (`--diff <base>..<head>`) and GitHub Code Scanning SARIF v2.1.0 exporter (`--format sarif`) in `src/cli/commands/analyze_code.py` and `src/core/utils/json_exporter.py` (FR-024, SC-006)
- [ ] T025 [P] [US8] Implement Monorepo Workspace Graph resolver (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `Cargo.toml`, `go.work`, `pyproject.toml`) and PageRank/Betweenness Centrality blast-radius scoring (`--blast-radius <node_id>`) in `src/analyzers/classification.py` and `src/analyzers/pipeline/dag_builder.py` (FR-025)
- [ ] T026 [P] [US9] Implement Declarative Architecture Fitness Functions & Policy-as-Code engine (`--policy <path>`) in `manifests/ecosystems.yaml` and `src/analyzers/code/orchestrator.py` (FR-026, SC-007)
- [ ] T027 [P] [US10] Implement Model Context Protocol (MCP) Server (`atruss mcp serve`, `--transport stdio|sse`) exposing `get_blast_radius`, `trace_entrypoint_chain`, `query_antipatterns`, `get_repo_scorecard`, and `check_boundary_violation` in `src/cli/commands/analyze_code.py` (FR-027, SC-008)
- [ ] T028 [P] [US11] Implement Runtime Observability Overlay ingesting OpenTelemetry trace exports (`--otel-traces`) and coverage reports (`--coverage`) to classify `HOT_PATH`, `COVERED_STATIC`, and `DEAD_UNOBSERVED` nodes in `src/analyzers/code/orchestrator.py` (FR-028)
- [ ] T029 [P] [US12] Implement Interactive WebGL/Canvas Graph Explorer (Cytoscape.js / ELK.js) with semantic zoom, search spotlight (`Cmd+K`), and synchronized Code-Jump Inspector Drawer in `web/src/components/PipelineView.astro` and `web/src/content/docs/index.mdx` (FR-029, SC-009)
- [ ] T030 [P] [US13] Implement Longitudinal Architecture Drift & Historical Scorecard Time-Series tracking (`catalog-history.json`) and trend sparklines in `src/core/utils/export_manager.py` and `web/src/content/docs/index.mdx` (FR-030, SC-010)
