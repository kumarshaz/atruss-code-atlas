# Implementation Plan: Atruss Code Atlas Unified Specification (001–008 + Horizon 2 Top 10)

**Branch**: `main` | **Date**: 2026-11-14 | **Spec**: [spec.md](./spec.md)
**Input**: Consolidated Master PRD ([`docs/atruss-code-atlas-prd.md`](../../docs/atruss-code-atlas-prd.md)) and Unified Specification ([`docs/atruss-code-atlas-unified-spec.md`](../../docs/atruss-code-atlas-unified-spec.md))

---

## 1. Summary

This unified implementation plan consolidates the architectural foundation delivered across SpecKit iterations `001` through `008` (`FR-001`–`FR-020`) and defines the execution blueprint for the **Top 10 Strategic Product & Architectural Enhancements** (`FR-021`–`FR-030`, `REC-01`–`REC-10`). All deliverables adhere strictly to Constitution v2.1.0 principles and are validated via the 5-Gate Architectural Conformance Validator (`scripts/validate_agent_workflow.py`).

---

## 2. Technical Context

- **Language/Version**: Python 3.11+ (`.venv` CLI & Analyzers), Node.js 20+ / Astro v5 + Starlight (`web/`)
- **Primary Dependencies**: `typer`, `httpx`, `pydantic`, `pyyaml`, `networkx`, `radon`, `rich` (plus Horizon 2 `tree-sitter`, `cytoscape`, `elkjs`)
- **Storage**: Deterministic local filesystem (`exports/{timestamp}/` + `exports/latest/`), externalized policy rules (`manifests/ecosystems.yaml`)
- **Testing**: `pytest`, `pytest-asyncio` (strict 0-skip enforcement via `scripts/validate_agent_workflow.py`)
- **Target Platform**: Cross-platform CLI (Linux, macOS, WSL) + GitHub Pages Static Hosting (`web/astro.config.mjs`)
- **Performance Goals**: `< 60 seconds` per `< 50k LoC` repository (`SC-001`); `< 5 seconds` incremental PR delta (`SC-006`); byte-for-byte SHA-256 deterministic JSON/Markdown outputs.

---

## 3. Constitution Check

*GATE: Must pass before implementation and after every phase via `scripts/validate_agent_workflow.py`.*

- **I. Policy-as-Code & Extensibility**: **PASS** — All ecosystem and classification heuristics are externalized in `manifests/ecosystems.yaml` and loaded via `src/analyzers/classification.py`.
- **II. Single Source of Truth for Reports**: **PASS** — Deterministic `exports/latest/` JSON artifacts drive both Arc42 Markdown generation (`src/core/services/report_generator.py`) and Astro build-time rendering (`scripts/generate-report-stubs.py`).
- **III. Security & Privacy First**: **PASS** — Dual-logger token masking (`src/core/auth.py`) and ephemeral read-only shallow clones (`src/core/utils/git_cloner.py`).
- **IV. Performance & Scalability**: **PASS** — Dual-mode GitHub Trees API inspection (`src/cli/commands/discover.py`) and shallow `--depth 1` cloning.
- **V. Progressive Disclosure**: **PASS** — Reports layer Executive Summary & A–F Scorecard ahead of deep trace matrices and interactive Astro views (`web/src/content/docs/index.mdx`, `web/src/components/PipelineView.astro`).
- **VI. Pipeline Visualization as a First-Class Feature**: **PASS** — Real `src/analyzers/pipeline/parser.py`, `src/analyzers/pipeline/dag_builder.py`, and `src/analyzers/pipeline/heuristics.py` wired into `src/cli/commands/analyze_pipeline.py`.
- **VII. Strict SDD & TDD**: **PASS** — Enforced by the 5-Gate Validator (`scripts/validate_agent_workflow.py`).

---

## 4. Project Structure & Canonical Module Mapping

### 4.1 Documentation & Specifications (`docs/` & `specs/009-unified-atlas-spec/`)

```text
docs/
├── README.md                               # Canonical Documentation & Specification Index
├── atruss-code-atlas-prd-baseline.md      # Preserved v1.0 Baseline PRD (Iterations 001–008)
├── atruss-code-atlas-prd.md               # Consolidated Master PRD v2.0 (Lineage + Top 10 Recommendations)
├── atruss-code-atlas-unified-spec.md      # Unified SpecKit Specification (FR-001 to FR-030)
└── agentic-sdlc-guide.md                   # Agentic SDLC Playbook (SpecKit vs. Antigravity Native)

specs/009-unified-atlas-spec/
├── spec.md                                 # Unified Feature Specification
├── plan.md                                 # Unified Architectural Plan (this file)
├── tasks.md                                # Complete Traceability Task Matrix (T001–T030)
└── checklists/
    └── requirements.md                     # SpecKit Specification Quality Checklist
```

### 4.2 Core Source, Exporters, Web Portal & Verification Harness

```text
manifests/
└── ecosystems.yaml                          # Externalized ecosystem & 27-column discovery classification rules

src/
├── models/
│   ├── artifacts.py                         # PipelineDAG, WorkflowNode, AntiPattern, CodeAnalysis models
│   ├── discovery.py                         # 27-column DiscoveryManifestItem schema
│   └── topology.py                          # Aggregate org-level TopologyNode & WorkflowRun models
├── analyzers/
│   ├── classification.py                    # Loads manifests/ecosystems.yaml & computes 27-col discovery signals
│   ├── pipeline/
│   │   ├── parser.py                        # GitHub Actions / CI workflow YAML parser
│   │   ├── dag_builder.py                   # Job dependency DAG builder & trigger mapper
│   │   └── heuristics.py                    # Pipeline & CI security anti-pattern rule engine
│   └── code/
│       ├── orchestrator.py                  # Polyglot code analyzer router & complexity aggregator
│       ├── python_ast.py                    # Python AST & Radon cyclomatic complexity analyzer
│       ├── dotnet_structural.py             # .NET .csproj, Controllers, Services, DbContext analyzer
│       ├── js_ts_structural.py              # React/Next/Vite/TS package, component & route analyzer
│       └── java_structural.py               # Java Spring Boot Maven/Gradle & annotation analyzer
├── core/
│   ├── auth.py                              # Token masking & credential hygiene
│   ├── services/
│   │   └── report_generator.py              # Arc42 & Mermaid Markdown report synthesizer
│   ├── utils/
│   │   ├── export_manager.py                # Timestamped export directory & exports/latest/ manager
│   │   ├── git_cloner.py                    # Shallow (--depth 1) ephemeral repository cloner
│   │   ├── json_exporter.py                 # Canonical JSON serialization helper
│   │   └── markdown_exporter.py             # Canonical Markdown serialization helper
│   └── exporters/
│       ├── discovery_exporter.py            # Exports repos/repositories.{json,csv,yaml}
│       ├── pipeline_exporter.py             # Exports per-repo pipeline DAGs & aggregate topology
│       └── markdown_exporter.py             # Exports reports/{org}-{repo}-report.md
└── cli/
    └── commands/
        ├── discover.py                      # Organization/user discovery CLI command
        ├── analyze_pipeline.py              # Pipeline DAG & anti-pattern CLI command
        └── analyze_code.py                  # Deep structural code & Arc42 report CLI command

scripts/
├── generate-report-stubs.py                 # Generates Astro Starlight MDX pages from exports/latest/
├── validate_agent_workflow.py               # 5-Gate Architectural Conformance Validator
└── run_public_100_eval.py                   # 100-Repository Public GitHub Benchmark Runner

web/
├── astro.config.mjs                         # Astro v5 + Starlight config with dynamic BASE_PATH
└── src/
    ├── components/
    │   └── PipelineView.astro               # Interactive pipeline DAG & anti-pattern viewer
    ├── pages/
    │   └── index.astro                      # Material Design 3 landing page & multi-repo catalog explorer
    └── styles/
        └── custom.css                       # Material Design 3 color tokens & responsive elevation rules

tests/
├── unit/
│   └── test_cli_inputs.py                   # CLI input & flag validation tests
└── integration/
    ├── test_public_100_eval.py              # 100-repository stratified benchmark verification
    └── test_todo_nodejs_mongo.py            # End-to-end polyglot pipeline & code analysis integration test
```

---

## 5. Phased Roadmap for Horizon 2 Top 10 Recommendations (`FR-021`–`FR-030`)

### 5.1 Wave 1 (v2.1 — Security & Supply-Chain Depth)
- **`REC-02` (`FR-022`) — CI/CD Workflow Security Static Analysis**: Extend `src/analyzers/pipeline/heuristics.py` and `src/analyzers/pipeline/parser.py` to detect `pull_request_target` untrusted checkout/expression injection (`AP-008`), unpinned 3rd-party Actions (`AP-009`), missing or over-privileged `GITHUB_TOKEN` permissions (`AP-010`), insecure `GITHUB_ENV` writes (`AP-011`), artifact poisoning (`AP-012`), public self-hosted runner exposure (`AP-013`), and cache poisoning (`AP-014`).
- **`REC-03` (`FR-023`) — OSV.dev Batch API, SBOM & Reachability**: Extend `src/analyzers/code/orchestrator.py` and `src/models/artifacts.py` to query the OSV.dev `/v1/querybatch` endpoint as primary vulnerability intelligence source, emit CycloneDX v1.5 / SPDX v2.3 SBOMs (`--sbom`), and annotate each CVE with execution-chain reachability (`REACHABLE_FROM_CI`, `REACHABLE_FROM_RUNTIME`, `UNREACHABLE_DORMANT`).
- **`REC-05` (`FR-025`) — Monorepo Workspace Graph & Blast-Radius Centrality**: Extend `manifests/ecosystems.yaml`, `src/analyzers/classification.py`, and `src/analyzers/pipeline/dag_builder.py` to resolve internal workspace packages (`pnpm`, `nx`, `turborepo`, `cargo`, `go.work`, `uv`) and compute PageRank/Betweenness Centrality blast-radius scores (`--blast-radius <node_id>`).

### 5.2 Wave 2 (v2.2 — Polyglot AST & CI/CD PR Governance)
- **`REC-01` (`FR-021`) — Tree-sitter Polyglot AST & Call Graph Resolution**: Enhance `src/analyzers/code/orchestrator.py`, `src/analyzers/code/python_ast.py`, `src/analyzers/code/js_ts_structural.py`, `src/analyzers/code/dotnet_structural.py`, and `src/analyzers/code/java_structural.py` with hybrid Tree-sitter CST resolution and edge confidence scores (`1.0`, `0.8`, `0.5`).
- **`REC-04` (`FR-024`) — Diff-Aware Incremental PR Delta & SARIF Action**: Extend `src/cli/commands/analyze_code.py`, `src/cli/commands/analyze_pipeline.py`, and `src/core/utils/json_exporter.py` to support `--diff <base>..<head>` and `--format sarif` (SARIF v2.1.0 for GitHub Code Scanning).
- **`REC-06` (`FR-026`) — Declarative Architecture Fitness Functions**: Extend `manifests/ecosystems.yaml` and `src/analyzers/code/orchestrator.py` to evaluate declarative architectural boundary rules (`forbidden_edges`, `max_cyclomatic_complexity`, `require_test_gate_before_deploy`) via `--policy`.
- **`REC-08` (`FR-028`) — Runtime Observability Overlay**: Extend `src/analyzers/code/orchestrator.py` to ingest OpenTelemetry trace exports (`--otel-traces`) and coverage reports (`--coverage`) to classify `HOT_PATH`, `COVERED_STATIC`, and `DEAD_UNOBSERVED` nodes.

### 5.3 Wave 3 (v2.3 — Interactive Canvas, MCP Server & Historical Trends)
- **`REC-07` (`FR-027`) — Model Context Protocol (MCP) Server**: Expose structural graph tools (`get_blast_radius`, `trace_entrypoint_chain`, `query_antipatterns`, `get_repo_scorecard`, `check_boundary_violation`) over stdio/SSE from the unified CLI.
- **`REC-09` (`FR-029`) — Interactive WebGL/Canvas Graph Explorer & Code-Jump Drawer**: Upgrade `web/src/components/PipelineView.astro` with Cytoscape.js + ELK.js semantic zoom, search spotlight (`Cmd+K` / `Ctrl+K`), and a synchronized Code-Jump Inspector Drawer.
- **`REC-10` (`FR-030`) — Longitudinal Architecture Drift & Historical Scorecard**: Extend `src/core/utils/export_manager.py` and `scripts/generate-report-stubs.py` to append historical scorecard snapshots to `catalog-history.json` and render drift sparklines in `web/src/components/PipelineView.astro`.
