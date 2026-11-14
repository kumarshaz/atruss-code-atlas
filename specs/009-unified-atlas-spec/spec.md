# Feature Specification: Atruss Code Atlas — Unified Platform Specification (Iterations 001–008 & Horizon 2 Enhancements)

**Feature Branch**: `feat/001-PRD-enhancements-it2`  
**Created**: 2026-11-14  
**Status**: Approved — Unified Canonical Specification  
**Input**: Consolidated Master PRD v2.0 ([`docs/atruss-code-atlas-prd.md`](./atruss-code-atlas-prd.md)), Baseline PRD v1.0 ([`docs/atruss-code-atlas-prd-baseline.md`](./atruss-code-atlas-prd-baseline.md)), and SpecKit Lineage (`specs/001-repo-analyzer` through `specs/008-public-github-100-benchmark`)

---

## Clarifications & Architectural Decisions

### Consolidated Lineage Clarifications (`001`–`008` + Iteration 2 PRD Consolidation)
- **Q1 (Execution & Persistence Model — `001`, `003`)**: Should Atruss Code Atlas rely on a backend database (PostgreSQL) and task queue (Celery/Redis) or operate as a stateless CLI?  
  → **A**: **100% Stateless Offline-Capable CLI**. All extraction runs in-memory and writes deterministic static artifacts (`JSON`, `CSV`, `YAML`, `Markdown`) to `exports/{timestamp}/` and `exports/latest/`.
- **Q2 (Ingestion Strategy — `002`, `004`, `006-core`, `008`)**: Should repository discovery and pipeline analysis require cloning every repository locally?  
  → **A**: **Dual-Mode Ingestion**. Discovery and remote pipeline analysis use GitHub REST API recursive trees (`/git/trees/{sha}?recursive=1`) and `/contents/` endpoints for zero-clone speed, while deep code analysis and `--repos-file` / `benchmark` workflows use shallow blobless clones (`git clone --depth 1 --filter=blob:none --single-branch`) inside auto-purging temporary directories.
- **Q3 (Policy-as-Code — `001`, `006-core`, Rec #3)**: Where do ecosystem detection rules, 27-column discovery signals, and architectural layer rules live?  
  → **A**: Externalized in declarative YAML manifests (`manifests/ecosystems.yaml` and `manifests/architecture-rules.yaml`). Zero hardcoded ecosystem heuristics in Python engine code.
- **Q4 (Pipeline Schema & UI Bridge — `004`, `005`, `006-ui`, `006-core`)**: How does the Astro Starlight UI consume Python CLI outputs without client-side runtime API fetches?  
  → **A**: **Build-Time Data Synchronization + Dual Pipeline Schema**. ` analyze-pipeline` outputs both per-repo `exports/latest/pipelines/{org}-{repo}-pipeline.json` (for `PipelineView.astro`) and aggregate `exports/latest/relationships/pipeline_topology.{json,csv,yaml}`. `npm run copy-data` copies `exports/latest/` and invokes `scripts/generate-report-stubs.py` prior to `astro build`.
- **Q5 (Vulnerability Intelligence — Baseline `FR-ANA-06` vs. Rec #4)**: Should dependency vulnerability scanning rely solely on the NIST NVD CPE API?  
  → **A**: Use **Google's `OSV.dev` Batch API (`https://api.osv.dev/v1/querybatch`)** as the primary package-native vulnerability engine (supporting PyPI, npm, NuGet, and Maven PURLs without API key rate-limit bottlenecks), supplemented by optional NVD CVSS enrichment and CycloneDX v1.6 SBOM export.

---

## User Scenarios & Testing *(mandatory)*

### Part I: Baseline Platform User Stories (Implemented in Iterations `001`–`008`)

### User Story 1 - Declarative Policy-as-Code Discovery & 27-Column Classification (Priority: P1)

As an engineering leader, I want to scan a GitHub organization (`atruss discover --org <org>`) to discover all accessible repositories, inspect their recursive file trees, and classify each repository across the 27-column ADO-parity schema using external YAML manifests (`manifests/ecosystems.yaml`), so that I have an accurate, machine-readable inventory of our technology landscape.

**Why this priority**: Organization-wide discovery is the foundational entry point for all downstream pipeline, architectural, and portfolio analyses.

**Lineage**: `001-repo-analyzer` (US1), `004-structured-output-formats` (US1), `006-core-unification-and-eval` (US1).

**Independent Test**: Run `atruss discover --org github-samples` (or against deterministic mocked HTTP tree payloads) and verify that `exports/latest/repos/repositories.{json,csv,yaml}` contain all 27 required columns populated via `manifests/ecosystems.yaml`.

**Acceptance Scenarios**:

1. **Given** a target GitHub organization and `manifests/ecosystems.yaml`, **When** `atruss discover --org <org>` runs, **Then** it fetches `/git/trees/{sha}?recursive=1` per repository and outputs `repositories.json`, `repositories.csv` (UTF-8-SIG BOM), and `repositories.yaml` with all 27 discovery fields.
2. **Given** a multi-ecosystem monorepo (e.g., `github-samples/pets-workshop`), **When** `classify_repository()` executes, **Then** each manifest-anchored subdirectory is isolated as an independent `ModuleUnit` and tie-broken by priority (`Java > .NET > Python > JS/TS`).
3. **Given** a newly added framework rule in `manifests/ecosystems.yaml`, **When** discovery runs, **Then** the new framework is detected with zero Python code changes.

---

### User Story 2 - Dual-Mode Chained & Variable-List Ingestion (Priority: P1)

As a DevSecOps engineer, I want to feed either an organization discovery manifest (`--from-discovery`), a newline-delimited repository list (`--repos-file`), or a local directory (`--path`) into `atruss analyze-pipeline` and `atruss analyze-code`, so that I can automate analysis at organizational scale or target specific repositories on demand.

**Why this priority**: Eliminates manual `git clone` scripting when scanning 50–100+ repositories while allowing targeted local runs before a pull request.

**Lineage**: `002-chain-analysis` (US1, US2), `003-portable-test-harness` (US3), `006-core-unification-and-eval` (US2).

**Independent Test**: Pass a `repositories.json` manifest via `--from-discovery` and a `targets.txt` list via `--repos-file` to both `analyze-pipeline` and `analyze-code`, verifying that all valid repositories are processed and unreachable repositories fail gracefully without aborting the batch.

**Acceptance Scenarios**:

1. **Given** a valid `repositories.json` file or `targets.txt` list, **When** `atruss analyze-pipeline` or `atruss analyze-code` executes, **Then** each repository is fetched (via API or shallow `git clone --depth 1 --filter=blob:none`) into an isolated temporary workspace and analyzed sequentially.
2. **Given** a repository that fails to clone or authenticate, **When** the batch iterates over that target, **Then** the error is logged with masked credentials and execution continues to the remaining repositories.

---

### User Story 3 - CI/CD Pipeline DAG Reconstruction & Operational Anti-Pattern Detection (Priority: P1)

As a DevOps engineer, I want `atruss analyze-pipeline` to parse `.github/workflows/*.yml` files, construct a NetworkX Directed Acyclic Graph (DAG) of jobs and `needs:` dependencies, and flag operational anti-patterns, so that I can visualize deployment topologies and remediate risky workflows.

**Why this priority**: Pipeline transparency is a core differentiator of Atruss Code Atlas over code-only scanners like SonarQube.

**Lineage**: `001-repo-analyzer` (US2), `004-structured-output-formats` (US2), `006-core-unification-and-eval` (US2).

**Independent Test**: Run `atruss analyze-pipeline` against repositories containing complex GitHub Actions workflows and verify that `exports/latest/pipelines/{org}-{repo}-pipeline.json` and `exports/latest/relationships/pipeline_topology.{json,csv,yaml}` accurately capture all jobs, `needs:` edges, triggers, and 7 baseline anti-patterns.

**Acceptance Scenarios**:

1. **Given** a repository with `.github/workflows/*.yml`, **When** `atruss analyze-pipeline` runs, **Then** it generates a validated DAG where jobs are nodes and `needs:` relationships are directed edges, accurately distinguishing sequential chains from parallel branches.
2. **Given** workflows exhibiting any of the 7 baseline anti-patterns (`NO_TEST_GATE`, `NO_CACHE`, `NO_ARTIFACT_HANDOFF`, `HARDCODED_SECRET`, `SEQUENTIAL_ONLY`, `UNFILTERED_MAIN_PUSH`, `UNLABELED_SELF_HOSTED`), **When** heuristics run, **Then** each infraction is emitted with its exact `type`, `severity`, and actionable `message`.

---

### User Story 4 - 4-Ecosystem Structural Code Analysis & Arc42 Report Generation (Priority: P1)

As a software architect, I want `atruss analyze-code` to extract architectural boundaries (`API_ROUTE`, `SERVICE`, `DATA_ACCESS_LAYER`, `UI_COMPONENT`, `MODULE`) and compute LoC and complexity metrics across Python, .NET, React/TypeScript/JavaScript, and Java Spring Boot repositories, outputting canonical JSON and self-contained Arc42 Markdown with Mermaid diagrams.

**Why this priority**: Reverse-engineers living architectural documentation directly from source code without manual diagram maintenance.

**Lineage**: `001-repo-analyzer` (US3), `003-portable-test-harness` (US1), `006-core-unification-and-eval` (US3).

**Independent Test**: Run `atruss analyze-code` against fixtures for Python, .NET, React/TS, and Java Spring Boot and verify that `exports/latest/reports/{org}-{repo}-analysis.json` and `{org}-{repo}-report.md` contain non-empty `architecture_components`, accurate metrics, YAML frontmatter, and valid Mermaid diagrams.

**Acceptance Scenarios**:

1. **Given** a local or cloned repository in any of the 4 MVP ecosystems, **When** `atruss analyze-code` executes, **Then** `orchestrate_full_analysis()` routes the codebase (including monorepo submodules) to the ecosystem analyzer and extracts API routes, services, data access layers, and UI components.
2. **Given** extracted components and metrics, **When** report export runs, **Then** `{org}-{repo}-report.md` is written with Starlight-compatible YAML frontmatter and embedded Arc42 Mermaid diagrams.

---

### User Story 5 - CI/CD Test Coverage Extraction (Priority: P2)

As an engineering manager, I want `atruss analyze-coverage` to extract test coverage percentages from CI/CD test logs and XML/JSON artifacts (`pytest`, `Jest`, `dotnet test`, `JaCoCo`), so that I can track testing health alongside pipeline topology.

**Why this priority**: Provides empirical verification of test effectiveness beyond merely checking whether a test job exists in the workflow DAG.

**Lineage**: `001-repo-analyzer` (US4).

**Independent Test**: Feed sample `pytest`, `Jest`, `dotnet test` Cobertura, and `JaCoCo` XML/log outputs into `atruss analyze-coverage` and verify extracted percentages match within `±2%` tolerance.

**Acceptance Scenarios**:

1. **Given** workflow logs or coverage XML artifacts from supported test runners, **When** `extract_coverage()` executes, **Then** it returns the normalized coverage percentage within `±2%` of the native tool's summary.

---

### User Story 6 - Material Design 3 Astro Observatory & GitHub Pages Deployment (Priority: P1)

As a consumer of architectural and pipeline intelligence, I want to explore all discovered organizations, repositories, pipeline DAGs, and Arc42 architecture reports through a static **Google Material Design 3 (M3)** Astro Starlight web application (`web/`) deployed automatically to GitHub Pages.

**Why this priority**: Transforms raw JSON/CSV/Markdown exports into an interactive, zero-backend engineering observatory accessible to executives, architects, and developers.

**Lineage**: `005-atruss-astro-dashboard` (US1–US3), `006-ui-data-integration` (US1–US4), `007-material-design-ui-gh-pages` (US1–US4).

**Independent Test**: Run `npm run copy-data && ASTRO_BASE=/atruss-code-atlas npm run build` inside `web/` and verify that the site builds in `< 30 seconds` with zero schema errors, rendering Layer 1 (`/`), Layer 2 (`/reports/{org}/{repo}/`), and Layer 3 (`/orgs/`) with M3 tonal tokens and `BASE_URL`-safe links.

**Acceptance Scenarios**:

1. **Given** exported datasets in `exports/latest/`, **When** the root Command Center (`/`) loads, **Then** `OrgHealthStrip`, `LanguageChart`, `RiskFlags`, and `RepoGrid` render inside M3 tonal surface containers with interactive M3 Filter Chips (`All`, `Python`, `.NET`, `JavaScript/TypeScript`, `Java`, `Has Pipeline`, `Has Docker`, `High Risk`) and instant search.
2. **Given** a repository detail page (`/reports/{org}/{repo}/`), **When** the user switches between the 3 M3 Primary Tabs (`Discovery Overview`, `CI/CD Pipeline DAG`, `Arc42 Code Architecture`), **Then** each view renders its data (or a resilient `EmptyStatePrompt` if unanalyzed) with interactive zoom/pan/reset on Mermaid diagrams.
3. **Given** multi-organization discovery data, **When** navigating to `/orgs/`, **Then** `OrgComparisonTable` and `LeaderboardView` rank organizations by their computed `OrgMaturityScore` (`0–100`).

---

### User Story 7 - 100-Repo Public GitHub Benchmark, Random Sampler & Self-Healing Agent Loop (Priority: P1)

As a platform maintainer running locally or on a Google AI Pro Remote Agent, I want `atruss benchmark` to validate discovery, pipeline DAG reconstruction, and code analysis across a curated corpus of **100 popular public GitHub repositories** (`--corpus popular-100`) and **stratified random samples** (`--random-sample N --seed S`), isolating any failures into `anomalies.json` for test-first self-healing.

**Why this priority**: Guarantees production-grade resilience and `>= 90%` classification accuracy across real-world repository layouts without disk exhaustion or unhandled crashes.

**Lineage**: `003-portable-test-harness` (US2), `008-public-github-100-benchmark` (US1–US3).

**Independent Test**: Run `atruss benchmark --corpus popular-100 --limit 12` and `atruss benchmark --random-sample 4 --seed 42`, verifying that `benchmark_manifest.json`, `benchmark_summary.{json,md}`, and `anomalies.json` are generated and temporary clone directories are purged after every repo.

**Acceptance Scenarios**:

1. **Given** `tests/fixtures/popular_100_corpus.json` (25 Python, 25 .NET, 25 React/TS/JS, 25 Java Spring Boot repos `< 250MB`), **When** `atruss benchmark` executes, **Then** it enforces a `180s` per-repo circuit breaker, cleans up shallow clones immediately, and achieves `>= 90%` classification accuracy and `>= 98%` crash-free completion.
2. **Given** any anomaly recorded in `exports/latest/anomalies.json`, **When** the self-healing workflow (`scripts/run_benchmark_loop.py`) runs, **Then** it replays failed targets via `--replay` and verifies all 5 governance gates via `scripts/validate_agent_workflow.py`.

---

### Part II: Horizon 2 Strategic Enhancement User Stories (Top 10 Industry Recommendations)

### User Story 8 - Advanced CI/CD Supply-Chain Security & Cross-Workflow DAGs (Priority: P1 — Rec #1)

As a DevSecOps engineer, I want the pipeline analyzer to detect supply-chain security vulnerabilities (`UNPINNED_ACTION`, `TEMPLATE_INJECTION`, `PWN_REQUEST_RISK`, `EXCESSIVE_PERMISSIONS`, `NO_TIMEOUT`, `ARTIFACT_CREDENTIAL_PERSISTENCE`, `STATIC_CLOUD_CREDENTIALS`) and link reusable workflows (`workflow_call` / `workflow_run`) as cross-workflow edges.

**Why this priority**: Addresses the #1 real-world CI/CD attack vector identified in 2025–2026 industry incidents (`tj-actions` tag hijacking, script injection, and pwn requests) and fulfills `FR-VIZ-10`.

**Independent Test**: Run `atruss analyze-pipeline` on workflow fixtures containing unpinned third-party actions, `${{ github.event.issue.title }}` inside `run:`, `pull_request_target` checkouts, and `uses: ./.github/workflows/reusable.yml`, verifying all 7 new finding types and `cross_workflow` edges are emitted.

**Acceptance Scenarios**:

1. **Given** a workflow using mutable third-party tags (`uses: third-party/action@v2`) or interpolating untrusted event fields in `run:`, **When** `analyze_workflow_anti_patterns()` runs, **Then** it flags `UNPINNED_ACTION` (`HIGH`) and `TEMPLATE_INJECTION` (`CRITICAL`).
2. **Given** a caller workflow invoking a reusable workflow via `uses: ./.github/workflows/build.yml`, **When** `dag_builder.py` constructs the topology, **Then** a directed `cross_workflow` edge links the caller job to the reusable workflow DAG.

---

### User Story 9 - Universal Polyglot `tree-sitter` AST, Cognitive Complexity & Dead-Code Analysis (Priority: P1 — Rec #2)

As a software architect, I want `atruss analyze-code` to parse Python, C#, TypeScript/TSX, and Java via `tree-sitter` syntax trees to compute Cyclomatic Complexity, Cognitive Complexity, AST Clone Duplication %, and Dead Code % uniformly without requiring external language SDKs.

**Why this priority**: Replaces regex approximations in `.NET`, `TS/JS`, and `Java` with true syntax-tree precision and completes original PRD requirements `FR-ANA-02`, `FR-ANA-03`, `FR-ANA-04`, and `FR-ANA-05`.

**Independent Test**: Run `orchestrate_full_analysis()` on C#, TypeScript, Java, and Python fixtures containing nested control flow, duplicated methods, and unused internal functions, verifying accurate `avg_cognitive_complexity`, `duplication_pct`, and `dead_code_count` metrics.

**Acceptance Scenarios**:

1. **Given** a `.NET`, `React/TS`, `Java`, or `Python` repository, **When** `analyze-code` executes, **Then** it computes function-level Cyclomatic Complexity and class/module-level Cognitive Complexity from the syntax tree.
2. **Given** duplicated AST blocks or unreferenced internal symbols, **When** `analyze-code` completes, **Then** `metrics` includes `duplication_pct` and `dead_code_symbols`.

---

### User Story 10 - Declarative Architectural Fitness Functions & Layer Violation Detection (Priority: P1 — Rec #3)

As a principal architect, I want to define architectural layer rules in `manifests/architecture-rules.yaml` (e.g., forbidding `UI_COMPONENT` or `API_ROUTE` from importing `DATA_ACCESS_LAYER` directly, or forbidding circular module dependencies) so that `atruss analyze-code` automatically flags architectural erosion.

**Why this priority**: Transforms static architecture diagrams into enforceable governance gates (ArchUnit / NetArchTest parity in a language-agnostic CLI).

**Independent Test**: Run `atruss analyze-code` on a repository where a Controller directly imports a Database Repository bypassing the Service layer or where Module A and Module B import each other, verifying that `ARCHITECTURE` fitness violations are recorded and highlighted in the Arc42 Mermaid diagram.

**Acceptance Scenarios**:

1. **Given** `manifests/architecture-rules.yaml` prohibiting direct `API_ROUTE -> DATA_ACCESS_LAYER` imports when a `SERVICE` layer is present, **When** `fitness_engine.py` evaluates the import graph, **Then** any violating import is emitted as an `AntiPatternFinding(entity_type="ARCHITECTURE")` and styled as a red dashed edge in the Mermaid diagram.
2. **Given** a circular dependency between internal modules, **When** `nx.simple_cycles` detects a cycle, **Then** a `CIRCULAR_DEPENDENCY` (`HIGH`) finding is recorded.

---

### User Story 11 - Lockfile Dependency Graph, `OSV.dev` Vulnerability Scanning & CycloneDX SBOM (Priority: P1 — Rec #4)

As an application security engineer, I want `atruss` to parse repository manifests and lockfiles, query Google's `OSV.dev` batch API for known vulnerabilities and upgrade paths, scan source files for high-entropy secrets, and export a CycloneDX v1.6 JSON SBOM.

**Why this priority**: Fulfills original PRD requirements `FR-ANA-06`, `FR-ANA-07`, `FR-ANA-08`, and `FR-RPT-05` using modern, rate-limit-resilient open-source vulnerability intelligence.

**Independent Test**: Run `atruss analyze-code` against a fixture with known vulnerable dependencies in `requirements.txt` / `package-lock.json` (using mocked or live `api.osv.dev/v1/querybatch`), verifying CVE annotations in `{org}-{repo}-analysis.json` and valid CycloneDX output in `exports/latest/sbom/{org}-{repo}.cdx.json`.

**Acceptance Scenarios**:

1. **Given** dependency manifests/lockfiles across Python, .NET, JS/TS, or Java, **When** dependency analysis runs, **Then** it batch-queries `OSV.dev` by package PURL and annotates vulnerable packages with CVE/GHSA IDs, severity, and fixed versions.
2. **Given** completed dependency analysis, **When** exporters run, **Then** `exports/latest/sbom/{org}-{repo}.cdx.json` is written conforming to CycloneDX v1.6.

---

### User Story 12 - 6-Dimension A–F Executive Scorecard & Code-to-Cloud Traceability (Priority: P1 — Recs #5 & #6)

As an engineering VP or architect, I want every analyzed repository to receive a deterministic **6-Dimension A–F Scorecard** (*Code Quality*, *Security*, *Maintainability*, *Test Coverage*, *Dependency Health*, *Pipeline Health*), a **Composite Technical Debt Score (`0–100`)**, and an **Arc42 Section 7 Code-to-Cloud Deployment Traceability Graph** linking code submodules to Dockerfiles, CI/CD jobs, and runtime environments.

**Why this priority**: Completes the executive scoring vision in PRD §6 (`FR-RPT-04`, `FR-ANA-10`) and unifies the code architecture and pipeline topology graphs into a single end-to-end view.

**Independent Test**: Run `atruss analyze-code` and `atruss analyze-pipeline` on a multi-service repository and verify that `{org}-{repo}-analysis.json` contains all 6 graded dimensions (`A`–`F`), `technical_debt_score`, and `code_to_cloud_edges`.

**Acceptance Scenarios**:

1. **Given** extracted code, coverage, dependency, and pipeline metrics, **When** `scorecard.py` executes, **Then** it computes `0–100` scores and `A`–`F` grades for all 6 dimensions plus the composite `technical_debt_score`.
2. **Given** a repository with code modules, `Dockerfile` / `k8s` manifests, and deployment workflows, **When** report generation runs, **Then** Section 7 of `{org}-{repo}-report.md` renders a `Code Module -> Container/Artifact -> Workflow Job -> Environment` Mermaid diagram.

---

### User Story 13 - Temporal Drift Diffing (`atruss diff`), SARIF PR Gate (`atruss check --sarif`) & AI/MCP Context (`atruss mcp`) (Priority: P2 — Recs #7, #8, #9, #10)

As a platform engineer or AI agent user, I want to compare two export snapshots for architectural drift (`atruss diff`), export findings as OASIS SARIF v2.1.0 (`atruss check --sarif`), expose architectural context to AI coding agents (`llms.txt` and `atruss mcp`), and export diagrams/reports as SVG, PNG, or PDF directly from the Material Design 3 UI.

**Why this priority**: Embeds Atruss Code Atlas into daily PR workflows, Architecture Review Boards, and AI coding assistant toolchains.

**Independent Test**: Run `atruss diff --baseline <t1> --target <t2>`, `atruss check --sarif`, and verify generated `drift_report.json`, `{org}-{repo}.sarif.json`, `llms.txt`, and M3 UI export controls.

**Acceptance Scenarios**:

1. **Given** two timestamped export directories `exports/t1` and `exports/t2`, **When** `atruss diff` runs, **Then** it emits `drift_report.{json,md}` highlighting added/removed components, new anti-patterns, and scorecard grade changes.
2. **Given** analysis findings, **When** `sarif_exporter.py` runs, **Then** it produces a valid SARIF v2.1.0 JSON file with file and line locations.
3. **Given** the Astro M3 repository detail view, **When** the user clicks `Export SVG`, `Export PNG`, or `Print / Save PDF`, **Then** the browser downloads the vector/raster diagram or renders a multi-tab print layout.

---

### Edge Cases

- **Unsupported or Empty Repository**: When a repository has zero files or belongs to an ecosystem not yet in `manifests/ecosystems.yaml`, discovery classifies `PrimaryLanguage` as `"Unknown"` (`Tier 4 - Unclassified`), `analyze-code` gracefully skips AST extraction without raising an exception, and `analyze-pipeline` still parses `.github/workflows/*.yml` if present.
- **Truncated GitHub Git Trees (`truncated: true`)**: When a massive repository exceeds GitHub's recursive tree item limit, `discover.py` logs a warning and falls back to top-level manifest inspection or shallow clone when deep analysis is requested.
- **GitHub API Primary (`429`) & Secondary (`403`) Rate Limits**: `GitHubClient` proactively inspects `X-RateLimit-Remaining < 50` to sleep until `X-RateLimit-Reset` and retries secondary `403` rate-limit responses using `Retry-After` backoff while immediately propagating fatal `401`/`403` scope errors.
- **Partial Pipeline Execution in Astro UI**: When a user runs only `atruss discover` without running `analyze-pipeline` or `analyze-code`, `PipelineView.astro` and `ArchitectureView.astro` render `EmptyStatePrompt.astro` with copyable CLI instructions rather than failing the Astro build.
- **Hung or Pathological Repository During Benchmark**: If any repository exceeds `180 seconds` during `atruss benchmark`, `asyncio.wait_for` triggers a circuit breaker, records a `timeout` entry in `anomalies.json`, purges the temporary clone directory, and proceeds to the next repository.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Baseline Implemented Requirements (`001`–`008`)
- **FR-001**: System MUST provide the `atruss` CLI (`discover`, `analyze-pipeline`, `analyze-code`, `analyze-coverage`, `benchmark`, `version`) with zero database or message-broker dependencies (`001`, `003`, `005`, `008`).
- **FR-002**: System MUST authenticate to GitHub via optional `--token`, `GH_TOKEN`, or `GITHUB_TOKEN` with `MaskingFormatter` log redaction, and support unauthenticated public scans (`001`, `004`).
- **FR-003**: System MUST paginate GitHub REST endpoints via RFC 5988 `Link: rel="next"` headers with `asyncio.Semaphore(10)` concurrency, proactive `X-RateLimit-Remaining` throttling, and secondary rate-limit retry backoff (`004`).
- **FR-004**: System MUST externalize all ecosystem, framework, and 27-column discovery signal rules into `manifests/ecosystems.yaml` and load them dynamically in `src/analyzers/classification.py` (`001`, `006-core`).
- **FR-005**: `atruss discover` MUST inspect repository file trees via `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1` and populate all 27 `DiscoveryManifestItem` fields, supporting `--include-archived`, `--exclude-repo-names`, `--exclude-repo-patterns`, and `--dry-run` (`004`, `006-core`).
- **FR-006**: System MUST detect multi-ecosystem monorepos by isolating manifest-root subdirectories into independent `ModuleUnit` records resolved by priority (`Java > .NET > Python > JS/TS`) (`001`, `006-core`).
- **FR-007**: `atruss analyze-pipeline` and `atruss analyze-code` MUST accept targets via `--from-discovery <json>`, `--repos-file <txt>`, or `--path <dir>` (`002`, `003`, `006-core`).
- **FR-008**: `GitCloner` MUST execute shallow blobless clones (`git clone --depth 1 --filter=blob:none --single-branch`) inside temporary directories that are automatically deleted upon context exit (`002`, `006-core`, `008`).
- **FR-009**: `atruss analyze-pipeline` MUST parse `.github/workflows/*.{yml,yaml}` files using `parser.py` and `dag_builder.py` (`NetworkX`) to extract triggers, jobs, runners, step counts, and `needs:` directed edges (`001`, `006-core`).
- **FR-010**: `atruss analyze-pipeline` MUST evaluate all 7 baseline anti-patterns (`NO_TEST_GATE`, `NO_CACHE`, `NO_ARTIFACT_HANDOFF`, `HARDCODED_SECRET`, `SEQUENTIAL_ONLY`, `UNFILTERED_MAIN_PUSH`, `UNLABELED_SELF_HOSTED`) in `src/analyzers/pipeline/heuristics.py` (`001`, `006-core`).
- **FR-011**: `atruss analyze-pipeline` MUST export both per-repository `exports/latest/pipelines/{org}-{repo}-pipeline.json` (matching `PipelineView.astro`) and aggregate `exports/latest/relationships/pipeline_topology.{json,csv,yaml}` + `reports/pipeline_topology.md` (`004`, `006-core`).
- **FR-012**: `src/analyzers/code/` MUST extract structural architecture components (`API_ROUTE`, `SERVICE`, `DATA_ACCESS_LAYER`, `UI_COMPONENT`, `MODULE`) and compute `files_analyzed`, `loc`, `sloc`, and cyclomatic complexity across Python (`python_ast.py`), .NET (`dotnet_structural.py`), React/TS/JS (`js_ts_structural.py`), and Java Spring Boot (`java_structural.py`) (`001`, `006-core`).
- **FR-013**: `atruss analyze-code` MUST export `{org}-{repo}-analysis.json` (`PortableArtifact`) and self-contained Arc42 Markdown `{org}-{repo}-report.md` (with Starlight frontmatter and Mermaid component diagrams) into `exports/latest/reports/` (`001`, `003`, `006-core`).
- **FR-014**: `atruss analyze-coverage` (`src/analyzers/coverage_parser.py`) MUST extract test coverage percentages (`±2%` tolerance) from `pytest`, `Jest`, `dotnet test`, and `JaCoCo` artifacts/logs (`001`).
- **FR-015**: `ExportManager` (`src/core/utils/export_manager.py`) MUST write all exports to timestamped `exports/{timestamp}/` folders and automatically synchronize `exports/latest/` (`004`, `006-core`).
- **FR-016**: `scripts/generate-report-stubs.py` MUST read `exports/latest/repos/repositories.json` and emit per-repository Starlight Markdown stubs (`web/src/content/docs/reports/{org}/{repo}.md`) validated by Zod `docsSchema` in `web/src/content.config.ts` (`005`, `006-ui`).
- **FR-017**: The Astro web application (`web/`) MUST implement Google Material Design 3 (`web/src/styles/material-theme.css`) across Layer 1 (`AtlasSummary`, `OrgHealthStrip`, `LanguageChart`, `RiskFlags`, `RepoGrid` with M3 Filter Chips & search, `RepoCard`), Layer 2 (`RepoTabs`, `DiscoveryTable`, `PipelineView`, `AntiPatternBadge`, `ArchitectureView`, `EmptyStatePrompt`), and Layer 3 (`/orgs/` `OrgComparisonTable`, `LeaderboardView`) (`005`, `006-ui`, `007`).
- **FR-018**: `web/` MUST support `ASTRO_SITE` and `ASTRO_BASE` subpath routing via `import.meta.env.BASE_URL` and automated deployment via `.github/workflows/deploy-pages.yml` (`007`).
- **FR-019**: `atruss benchmark` (`src/cli/commands/benchmark.py`) MUST support `--corpus popular-100` (`tests/fixtures/popular_100_corpus.json`), `--random-sample <N> --seed <int>`, and `--replay <manifest.json>`, enforcing a `180s` per-repo circuit breaker and emitting `benchmark_manifest.json`, `benchmark_summary.{json,md}`, and `anomalies.json` (`008`).
- **FR-020**: `scripts/validate_agent_workflow.py` MUST enforce all 5 governance gates (Gate 1: Spec-Plan-Task Traceability, Gate 2: AST Anti-Stub/Anti-Skip Audit, Gate 3: Pytest 0-Skip Execution, Gate 4: Python-to-Astro Schema Contract Verification, Gate 5: SHA-256 Determinism Check) and emit `exports/latest/agent-eval-report.json` (`006-core`).

#### Horizon 2 Enhancement Requirements (Top 10 Industry Recommendations)
- **FR-021 (Rec #1)**: `src/analyzers/pipeline/heuristics.py` and `dag_builder.py` MUST detect the 7 CI/CD supply-chain security anti-patterns (`UNPINNED_ACTION`, `TEMPLATE_INJECTION`, `PWN_REQUEST_RISK`, `EXCESSIVE_PERMISSIONS`, `NO_TIMEOUT`, `ARTIFACT_CREDENTIAL_PERSISTENCE`, `STATIC_CLOUD_CREDENTIALS`) and resolve `workflow_call` / `workflow_run` cross-workflow edges.
- **FR-022 (Rec #2)**: `src/analyzers/code/` MUST integrate `tree-sitter` polyglot syntax-tree analysis across Python, C#, TypeScript/JS, and Java to compute Cyclomatic Complexity, Cognitive Complexity, AST Clone Duplication %, and Dead Code symbols.
- **FR-023 (Rec #3)**: System MUST evaluate declarative architectural layer rules from `manifests/architecture-rules.yaml` against the internal file import graph to detect forbidden layer bypasses and circular dependencies (`nx.simple_cycles`).
- **FR-024 (Rec #4)**: System MUST parse repository lockfiles/manifests, batch-query `https://api.osv.dev/v1/querybatch` for CVE/GHSA vulnerabilities and upgrade paths, scan source files for high-entropy secrets, and export CycloneDX v1.6 SBOMs (`exports/latest/sbom/{org}-{repo}.cdx.json`).
- **FR-025 (Rec #5)**: System MUST compute a deterministic **6-Dimension A–F Repository Scorecard** (*Code Quality*, *Security*, *Maintainability*, *Test Coverage*, *Dependency Health*, *Pipeline Health*) and **Composite Technical Debt Score (`0–100`)** inside `PortableArtifact`.
- **FR-026 (Rec #6)**: System MUST correlate code submodules, `Dockerfile`/Kubernetes/Terraform manifests, and GitHub Actions jobs to generate an **Arc42 Section 7 Code-to-Cloud Deployment Traceability Graph**.
- **FR-027 (Rec #7)**: System MUST provide an `atruss diff --baseline <dir1> --target <dir2>` command emitting `exports/latest/drift/drift_report.{json,md}` to track architectural, pipeline, and scorecard drift across snapshots.
- **FR-028 (Rec #8)**: System MUST export pipeline, secret, vulnerability, and architectural findings in **OASIS SARIF v2.1.0** format (`exports/latest/sarif/{org}-{repo}.sarif.json`) and provide `atruss check --sarif` for PR quality gating.
- **FR-029 (Rec #9)**: System MUST generate AI agent context files (`exports/latest/llms/llms.txt` and `llms-full.txt`) and provide a read-only stdio **Model Context Protocol server (`atruss mcp`)** querying `exports/latest/`.
- **FR-030 (Rec #10)**: The Astro M3 UI (`web/`) MUST provide client-side SVG/PNG diagram download buttons, a multi-tab Print/PDF stylesheet, an M3 Module Complexity & 6-Dimension Scorecard Heatmap (`ScorecardHeatmap.astro`), and a Cross-Repository Topology Explorer on `/orgs/`.

### Key Entities

- **DiscoveryManifestItem**: 27-column repository discovery record exported to `repos/repositories.{json,csv,yaml}`.
- **PortableArtifact**: Canonical per-repository analysis envelope (`reports/{org}-{repo}-analysis.json`) containing `repository`, `sha`, `ecosystem`, `metrics`, `pipelines`, `architecture_components`, `scorecard`, and `dependencies`.
- **PipelineWorkflow & TopologyNode**: Per-workflow DAG structure (`id`, `name`, `triggers`, `jobs`, `job_nodes`, `dag_metrics`, `anti_patterns`) and org-level deployment linkage record (`relationships/pipeline_topology.json`).
- **ArchitectureComponent & FitnessViolation**: Discovered code boundary (`API_ROUTE`, `SERVICE`, `DATA_ACCESS_LAYER`, `UI_COMPONENT`, `MODULE`) and architectural layer/cycle infraction.
- **RepositoryScorecard & OrgMaturityScore**: 6-dimension A–F repository grade breakdown (`0–100` + `technical_debt_score`) and organization-wide CI/CD maturity score (`0–100`).
- **DriftDeltaReport**: Temporal comparison payload detailing added/removed components, anti-pattern deltas, and scorecard grade transitions between two snapshots.
- **CorpusEntry, BenchmarkSummary & AnomalyRecord**: Stratified 100-repo benchmark catalog item, aggregate benchmark run scorecard, and fault-isolated failure record.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (Discovery Speed)**: Organization discovery and 27-column classification of up to 100 repositories completes in `< 2 minutes`.
- **SC-002 (Deep Analysis SLA)**: Pipeline DAG and deep structural code analysis for any repository under `500k LoC` (`< 250MB`) completes in `< 3 minutes` (`180s` hard timeout).
- **SC-003 (Classification Accuracy)**: Ecosystem classification accuracy across the 100-repository benchmark corpus (`tests/fixtures/popular_100_corpus.json`) achieves `>= 90%`.
- **SC-004 (Pipeline DAG Fidelity)**: Pipeline DAG reconstruction visualizes `100%` of defined jobs, `needs:` edges, and triggers, with `< 5%` false-positive rate on anti-pattern rules.
- **SC-005 (Coverage Accuracy)**: Test coverage extraction matches native test runner reports within `±2%` tolerance.
- **SC-006 (Zero-Skip Test Suite)**: `pytest tests/ --strict-markers` executes 100% of unit and integration tests with `0 failures`, `0 errors`, and `0 skipped` tests.
- **SC-007 (5-Gate Agentic Governance)**: `python3 scripts/validate_agent_workflow.py` passes all 5 gates and outputs Grade `A` in `exports/latest/agent-eval-report.json`.
- **SC-008 (Byte-for-Byte Determinism)**: Repeated executions against the same repository SHA produce identical SHA-256 digests across components, metrics, pipeline DAGs, and Arc42 Markdown reports.
- **SC-009 (Static UI Build Performance)**: `cd web && npm run build` completes in `< 30 seconds` with zero Zod schema errors and zero broken internal links under both `/` and `ASTRO_BASE=/atruss-code-atlas`.
- **SC-010 (Benchmark Crash-Free Resilience)**: `atruss benchmark` achieves `>= 98%` crash-free completion across popular and randomized public GitHub repositories with zero temporary disk accumulation.

---

## Assumptions

- Target repositories are hosted on GitHub (public or private with optional PAT authentication) or available as local Git directories.
- All development, CLI execution, testing, and Astro static builds run inside a Linux / WSL environment with Python 3.11+ (`.venv`) and Node.js v22+ (`fnm`).
- The core engine and static web UI remain strictly database-free and broker-free in accordance with Constitution v2.1.0.
