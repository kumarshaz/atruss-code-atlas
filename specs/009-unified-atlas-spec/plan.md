# Implementation Plan: Atruss Code Atlas Unified Specification (001–008 + Horizon 2 Top 10)

**Branch**: `002-horizon2-unified-atlas` | **Date**: 2026-11-14 | **Spec**: [spec.md](./spec.md)
**Input**: Consolidated Master PRD ([`docs/atruss-code-atlas-prd.md`](../../docs/atruss-code-atlas-prd.md)) and Unified Specification ([`docs/atruss-code-atlas-unified-spec.md`](../../docs/atruss-code-atlas-unified-spec.md))

---

## 1. Summary

This unified implementation plan consolidates the architectural foundation delivered across SpecKit iterations `001` through `008` (`FR-001`–`FR-020`) and delivers the **Top 10 Strategic Horizon 2 Enhancements** (`FR-021`–`FR-030`, `REC-01`–`REC-10`) on branch `002-horizon2-unified-atlas` using Antigravity's parallel subagent swarm workflow (`.agent/skills/horizon2-swarm/`). All deliverables adhere strictly to Constitution v2.1.0 principles and are validated via the 5-Gate Architectural Conformance Validator (`scripts/validate_agent_workflow.py`).

---

## 2. Technical Context

- **Language/Version**: Python 3.11+ (`.venv` CLI & Analyzers), Node.js 22+ / Astro v5 + Starlight (`web/`)
- **Primary Dependencies**: `typer`, `httpx`, `pydantic`, `pyyaml`, `networkx`, `radon`, `rich`, `tree-sitter`, `tree-sitter-language-pack`
- **Storage**: Deterministic local filesystem (`exports/{timestamp}/` + `exports/latest/`), externalized policy rules (`manifests/ecosystems.yaml`, `manifests/architecture-rules.yaml`, `manifests/pipeline-rules.yaml`)
- **Testing**: `pytest`, `pytest-asyncio`, Node `tsx` test runner (strict 0-skip enforcement via `scripts/validate_agent_workflow.py`)
- **Target Platform**: Cross-platform CLI (Linux, macOS, WSL) + GitHub Pages Static Hosting (`web/astro.config.mjs`)
- **Performance Goals**: `< 180 seconds` per repo deep analysis (`SC-002`); fast offline delta & gate checks (`atruss diff`, `atruss check`); byte-for-byte SHA-256 deterministic JSON/Markdown/CycloneDX/SARIF/llms.txt outputs (`SC-008`).

---

## 3. Constitution Check

*GATE: Must pass before implementation and after every phase via `scripts/validate_agent_workflow.py`.*

- **I. Policy-as-Code & Extensibility**: **PASS** — Ecosystem classification (`manifests/ecosystems.yaml`), architectural fitness layers/thresholds (`manifests/architecture-rules.yaml`), and CI/CD security rules (`manifests/pipeline-rules.yaml`) are loaded dynamically.
- **II. Single Source of Truth for Reports**: **PASS** — Deterministic `exports/latest/` JSON, Markdown, CycloneDX v1.6 SBOM, SARIF v2.1.0, and `llms.txt` artifacts drive both CLI gates and Astro build-time rendering (`scripts/generate-report-stubs.py`).
- **III. Security & Privacy First**: **PASS** — Dual-logger token masking (`src/core/auth.py`), ephemeral read-only shallow clones (`src/core/utils/git_cloner.py`), redacted secret scanning (`src/analyzers/dependencies/secret_scanner.py`), and offline-safe OSV queries (`src/analyzers/dependencies/osv_client.py`).
- **IV. Performance & Scalability**: **PASS** — Dual-mode GitHub Trees API inspection (`src/cli/commands/discover.py`), shallow `--depth 1` cloning, and batched OSV queries (`/v1/querybatch`).
- **V. Progressive Disclosure**: **PASS** — Reports layer 6-Dimension A–F Scorecard & Executive Summary ahead of fitness violations, vulnerabilities, Section 7 Code-to-Cloud traceability, and interactive Astro M3 views (`web/src/content/docs/index.mdx`, `web/src/components/PipelineView.astro`, `web/src/components/ScorecardHeatmap.astro`).
- **VI. Pipeline Visualization as a First-Class Feature**: **PASS** — Real `src/analyzers/pipeline/parser.py`, `src/analyzers/pipeline/dag_builder.py`, and `src/analyzers/pipeline/heuristics.py` wired into `src/cli/commands/analyze_pipeline.py` and `web/src/components/CrossRepoTopology.astro`.
- **VII. Strict SDD & TDD**: **PASS** — Enforced by the 5-Gate Validator (`scripts/validate_agent_workflow.py`) across both `specs/006-core-unification-and-eval` and `specs/009-unified-atlas-spec`.

---

## 4. Project Structure & Canonical Module Mapping

### 4.1 Documentation & Specifications (`docs/` & `specs/009-unified-atlas-spec/`)

```text
docs/
├── README.md                               # Canonical Documentation & Specification Index
├── atruss-code-atlas-prd-baseline.md      # Preserved v1.0 Baseline PRD (Iterations 001–008)
├── atruss-code-atlas-prd.md               # Consolidated Master PRD v2.0 (Lineage + Top 10 Recommendations)
├── atruss-code-atlas-unified-spec.md      # Unified SpecKit Specification (FR-001 to FR-030)
└── agentic-sdlc-guide.md                   # Agentic SDLC Playbook (SpecKit vs. Antigravity Native Swarm + 5-Gate Governance)

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
├── ecosystems.yaml                          # Externalized ecosystem & 27-column discovery classification rules
├── architecture-rules.yaml                  # Declarative layer boundary, complexity & duplication fitness rules
└── pipeline-rules.yaml                      # 14-rule CI/CD reliability & supply-chain security policy catalog

src/
├── models/
│   ├── artifacts.py                         # PipelineDAG, CodeToCloudEdge, Scorecard, SBOM/Secret/Fitness models
│   ├── discovery.py                         # 27-column DiscoveryManifestItem schema
│   ├── topology.py                          # Aggregate org-level TopologyNode & WorkflowRun models
│   └── benchmark.py                         # 100-repo benchmark manifest & anomaly models
├── analyzers/
│   ├── classification.py                    # Loads manifests/ecosystems.yaml & computes 27-col discovery signals
│   ├── scorecard.py                         # Deterministic 6-Dimension A-F Scorecard & technical debt calculator
│   ├── traceability.py                      # Arc42 Section 7 Code-to-Cloud deployment traceability graph builder
│   ├── observability.py                     # OpenTelemetry span & LCOV/Cobertura/Jest coverage overlay engine
│   ├── drift.py                             # Longitudinal snapshot drift & regression analyzer
│   ├── coverage_parser.py                   # Multi-runner coverage parser (pytest, Jest, dotnet, JaCoCo)
│   ├── pipeline/
│   │   ├── parser.py                        # GitHub Actions / CI workflow YAML parser + line-number index
│   │   ├── dag_builder.py                   # Job & cross-workflow (workflow_call/run) DAG builder & blast radius
│   │   └── heuristics.py                    # 14-rule CI/CD reliability & supply-chain security rule engine
│   ├── dependencies/
│   │   ├── manifest_parser.py               # Polyglot lockfile & dependency manifest parser + PURL generator
│   │   ├── osv_client.py                    # Offline-safe OSV.dev /v1/querybatch matcher & reachability tagger
│   │   └── secret_scanner.py                # High-entropy & pattern secret detector with strict redaction
│   └── code/
│       ├── orchestrator.py                  # Polyglot code, fitness, supply-chain, scorecard & C2C coordinator
│       ├── treesitter_engine.py             # Hybrid Tree-sitter complexity, clone & dead-code analyzer
│       ├── fitness_engine.py                # Layer boundary, cycle (nx.simple_cycles) & workspace graph engine
│       ├── python_ast.py                    # Python AST, Radon complexity & Tree-sitter metrics analyzer
│       ├── dotnet_structural.py             # .NET .csproj, Controllers, Services, DbContext analyzer
│       ├── js_ts_structural.py              # React/Next/Vite/TS package, component & route analyzer
│       └── java_structural.py               # Java Spring Boot Maven/Gradle & annotation analyzer
├── core/
│   ├── auth.py                              # Token masking & credential hygiene
│   ├── services/
│   │   └── report_generator.py              # Arc42, Horizon 2 sections & Mermaid Markdown report synthesizer
│   ├── utils/
│   │   ├── export_manager.py                # Timestamped exports/{ts}/, exports/latest/ & catalog-history manager
│   │   ├── git_cloner.py                    # Shallow (--depth 1) ephemeral repository cloner
│   │   ├── json_exporter.py                 # Canonical JSON serialization helper
│   │   └── markdown_exporter.py             # Canonical Markdown serialization helper
│   └── exporters/
│       ├── discovery_exporter.py            # Exports repos/repositories.{json,csv,yaml}
│       ├── pipeline_exporter.py             # Exports per-repo pipeline DAGs & aggregate topology
│       ├── markdown_exporter.py             # Exports reports/{org}-{repo}-report.md
│       ├── sbom_exporter.py                 # Exports CycloneDX v1.6 JSON SBOMs (sbom/*.cdx.json)
│       ├── sarif_exporter.py                # Exports OASIS SARIF v2.1.0 findings (sarif/*.sarif.json)
│       └── llms_exporter.py                 # Exports AI agent context (llms/llms.txt & llms-full.txt)
└── cli/
    ├── main.py                              # Root Typer CLI registering all Atruss commands
    └── commands/
        ├── discover.py                      # Organization/user discovery CLI command
        ├── analyze_pipeline.py              # Pipeline DAG, security rules & SARIF/cross-workflow CLI command
        ├── analyze_code.py                  # Deep structural code, SBOM, SARIF, diff & OTel CLI command
        ├── analyze_coverage.py              # Test coverage analysis CLI command
        ├── benchmark.py                     # 100-repo corpus benchmark CLI command
        ├── check.py                         # Offline PR quality gate (`atruss check --sarif --fail-on`)
        ├── diff.py                          # Snapshot architectural drift CLI (`atruss diff`)
        └── mcp_server.py                    # Read-only stdio MCP server (`atruss mcp`) with 10 tools

scripts/
├── curate_corpus.py                         # Curates tests/fixtures/popular_100_corpus.json
├── generate-report-stubs.py                 # Generates Astro Starlight MDX pages with M3 tabs & ScorecardHeatmap
├── validate_agent_workflow.py               # 5-Gate Architectural Conformance Validator
└── run_benchmark_loop.py                    # 100-Repository Public GitHub Benchmark Runner

web/
├── astro.config.mjs                         # Astro v5 + Starlight config with dynamic ASTRO_BASE
├── package.json                             # Copies exports/latest & llms*.txt, builds Starlight static portal
└── src/
    ├── content/docs/
    │   ├── index.mdx                        # Material Design 3 landing page & multi-repo catalog explorer
    │   └── orgs/index.mdx                   # Organization comparison, leaderboard & CrossRepoTopology explorer
    ├── components/
    │   ├── ArchitectureView.astro           # Arc42 architecture viewer with Horizon 2 chips & SVG/PNG export
    │   ├── CrossRepoTopology.astro          # Interactive cross-repo workflow/service Mermaid explorer
    │   ├── LeaderboardView.astro            # Org & repo leaderboard including 6-D scorecards & risk counts
    │   ├── OrgComparisonTable.astro         # Multi-org comparison table with CVE & fitness columns
    │   ├── PipelineView.astro               # Interactive pipeline DAG, cross-workflow edges & SVG/PNG export
    │   ├── RepoTabs.astro                   # 4-tab M3 layout with Print / Save PDF export
    │   └── ScorecardHeatmap.astro           # 6-D Scorecard, complexity heatmap, secrets, CVEs & C2C viewer
    ├── lib/
    │   └── mermaid-client.ts                # Lazy Mermaid hydration plus client-side SVG/PNG export utilities
    ├── styles/
    │   └── material-theme.css               # Material Design 3 tonal color tokens & @media print PDF styling
    └── tests/
        ├── AtlasSummary.test.ts             # Component contract tests for M3 Horizon 2 views & exports
        └── schema.test.ts                   # Schema validation for discovery, pipeline & Horizon 2 artifacts

tests/
├── unit/
│   ├── test_cli_inputs.py                   # CLI input & flag validation tests
│   ├── test_pipeline_security.py            # CI/CD supply-chain rules (ATRUSS-PIPE-008..014) & cross-DAG tests
│   ├── test_treesitter_engine.py            # Polyglot CST complexity, clones, dead-code & import edge tests
│   ├── test_fitness_engine.py               # Architecture rules, cycles, blast radius & workspace tests
│   ├── test_dependencies_osv_sbom.py        # Lockfiles, offline OSV batch, secret scanner & CycloneDX tests
│   ├── test_scorecard_traceability.py       # 6-D Scorecard, Code-to-Cloud traceability & OTel overlay tests
│   └── test_drift_sarif_mcp.py              # Drift diff, OASIS SARIF v2.1.0, llms.txt & MCP server tests
└── integration/
    ├── test_benchmark_e2e.py                # Stratified benchmark verification
    ├── test_horizon2_e2e.py                 # Full Horizon 2 E2E CLI, OSV mock, SARIF/diff/MCP & SHA-256 tests
    └── test_todo_nodejs_mongo.py            # End-to-end polyglot pipeline & code analysis integration test
```

---

## 5. Horizon 2 Delivery Architecture (`FR-021`–`FR-030`, Implemented on `002-horizon2-unified-atlas`)

### 5.1 Wave A — Pipeline Supply-Chain Security, Polyglot Tree-sitter & Supply Chain
- **`REC-01` (`FR-021`) — CI/CD Supply-Chain Security & Cross-Workflow DAGs**: `manifests/pipeline-rules.yaml`, `src/analyzers/pipeline/parser.py`, `src/analyzers/pipeline/heuristics.py`, and `src/analyzers/pipeline/dag_builder.py` detect all 7 security anti-patterns (`UNPINNED_ACTION`, `TEMPLATE_INJECTION`, `PWN_REQUEST_RISK`, `EXCESSIVE_PERMISSIONS`, `NO_TIMEOUT`, `ARTIFACT_CREDENTIAL_PERSISTENCE`, `STATIC_CLOUD_CREDENTIALS`) and resolve `workflow_call` / `workflow_run` cross-workflow edges.
- **`REC-02` (`FR-022`) — Tree-sitter Polyglot AST & Complexity Metrics**: `src/analyzers/code/treesitter_engine.py` integrates `tree-sitter` across Python, C#, TypeScript/JS, and Java (with safe AST/regex fallbacks) to compute Cyclomatic Complexity, Cognitive Complexity, AST Clone Duplication %, Dead Code symbols, and import edges consumed across all four structural analyzers.
- **`REC-03` (`FR-023`) — Declarative Architecture Fitness Functions & Workspace Graph**: `manifests/architecture-rules.yaml` and `src/analyzers/code/fitness_engine.py` evaluate layer boundary violations, circular dependencies (`nx.simple_cycles`), workspace packages (`pnpm`, `turbo`, `nx`, `cargo`, `go.work`, `uv`), and PageRank/Betweenness blast radius (`--blast-radius`).
- **`REC-04` (`FR-024`) — Supply-Chain Lockfiles, OSV.dev Batch, Secret Scanning & CycloneDX v1.6 SBOM**: `src/analyzers/dependencies/{manifest_parser,osv_client,secret_scanner}.py` and `src/core/exporters/sbom_exporter.py` parse manifests/lockfiles, match CVEs against `/v1/querybatch` (offline-safe by default), redact secrets, and export deterministic `sbom/{org}-{repo}.cdx.json`.

### 5.2 Wave B — Scorecard, Code-to-Cloud, Drift Diff, SARIF Gate & MCP Server
- **`REC-05` (`FR-025`) — 6-Dimension A–F Scorecard & Technical Debt Score**: `src/analyzers/scorecard.py` computes deterministic A–F grades across *Code Quality*, *Security*, *Maintainability*, *Test Coverage*, *Dependency Health*, and *Pipeline Health* plus composite `technical_debt_score` (`0–100`) and remediation hours inside `PortableArtifact`.
- **`REC-06` (`FR-026`) — Arc42 Section 7 Code-to-Cloud Traceability & Observability Overlay**: `src/analyzers/traceability.py`, `src/analyzers/observability.py`, and `src/core/services/report_generator.py` link code submodules to `Dockerfile`/Kubernetes/Terraform manifests, CI/CD jobs, and runtime environments while supporting `--otel-traces` and `--coverage`.
- **`REC-07` (`FR-027`) — Snapshot Drift Engine (`atruss diff`)**: `src/analyzers/drift.py`, `src/cli/commands/diff.py`, and `src/cli/commands/analyze_code.py` (`--diff`) compare snapshots across inventory, DAG jobs, fitness violations, vulnerabilities, and scorecards to emit `drift_report.{json,md}`.
- **`REC-08` (`FR-028`) — OASIS SARIF v2.1.0 & PR Quality Gate (`atruss check --sarif`)**: `src/core/exporters/sarif_exporter.py` and `src/cli/commands/check.py` emit schema-valid SARIF v2.1.0 (`sarif/*.sarif.json`) and enforce `--fail-on` severity thresholds offline.
- **`REC-09` (`FR-029`) — `llms.txt` Context Exporters & Stdio MCP Server (`atruss mcp`)**: `src/core/exporters/llms_exporter.py` generates `llms/llms.txt` and `llms/llms-full.txt`, and `src/cli/commands/mcp_server.py` exposes 10 read-only tools over JSON-RPC stdio against `exports/latest/`.

### 5.3 Wave C — Material Design 3 UI, Harnesses & Governance (`REC-10` / `FR-030`)
- **`REC-10` (`FR-030`) — Astro M3 Exports, Print/PDF, Scorecard Heatmap & Cross-Repo Topology**: `web/src/lib/mermaid-client.ts`, `web/src/components/{ScorecardHeatmap,CrossRepoTopology,RepoTabs,PipelineView,ArchitectureView,LeaderboardView,OrgComparisonTable}.astro`, `web/src/styles/material-theme.css`, `scripts/generate-report-stubs.py`, and `web/package.json` deliver SVG/PNG downloads, Print/PDF export, 6-D heatmaps, and org-wide cross-repo topology views verified by `scripts/validate_agent_workflow.py`.
