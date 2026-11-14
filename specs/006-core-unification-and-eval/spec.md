# Feature Specification: Core Engine Unification, Policy-as-Code & Agentic Workflow Evaluation

**Feature Branch**: `006-core-unification-and-eval`  
**Created**: 2026-11-12  
**Status**: Approved (Aligned via `/grill-me`)  
**Input**: Deep audit findings from `docs/restart-research-and-strategy-report.md` and interactive design alignment session.

---

## 1. Context & Problem Statement

Between Iterations `003`, `004`, and `005`, critical cross-iteration drift occurred:
1. **Broken CLI & Exporter Contracts**: `004` overwrote `src/cli/commands/analyze_pipeline.py`, removing `--repos-file` and `_analyze_repo_workflows()`, breaking `tests/unit/test_cli_inputs.py` and `tests/integration/test_todo_nodejs_mongo.py`.
2. **Mocked Pipeline Extraction**: `analyze_pipeline.py` contains `# Mock targeting behavior` and never calls `src/analyzers/pipeline/parser.py`, `dag_builder.py`, or `heuristics.py`.
3. **Exporter Split-Brain**: `src/core/utils/` (`003`) and `src/core/exporters/` (`004`) duplicate functionality with incompatible schemas, leaving Astro's `PipelineView.astro` (`005`) unable to find `exports/latest/pipelines/{org}-{repo}-pipeline.json`.
4. **Hardcoded Classification & Incomplete Discovery**: `classification.py` hardcodes ecosystem checks instead of using external YAML manifests (violating Constitution Principle I), and `discover.py` never calls `/git/trees/{sha}?recursive=1` to populate the 27-column discovery fields (`FrameworkType`, `HasDockerfile`, `HasPipeline`, `HasKubernetes`, `DocumentationPriority`).
5. **Single-Language AST & Hollow E2E Tests**: `orchestrator.py` skips `.NET`, `React/TS`, and `Java Spring Boot`, and 5 integration test files consist solely of `pytest.skip(...)`.

---

## 2. Clarifications & Architectural Decisions (from `/grill-me`)

- **Workflow Model**: Retain `.specify/memory/constitution.md` and `specs/00X/` for Docs-as-Code traceability, enforced by an automated **5-Gate Agentic Workflow Validator** (`scripts/validate_agent_workflow.py`).
- **Dual-Mode Ingestion**: Use GitHub REST `/git/trees/{sha}?recursive=1` & contents API by default for fast zero-clone discovery and pipeline analysis, while supporting `--repos-file` and `--path` via shallow `git clone --depth 1` for local/code analysis.
- **Unified YAML Policy-as-Code**: Externalize both the 4 core ecosystems + sub-frameworks AND the 27-column discovery signals (`HasAPI`, `HasService`, `HasFrontend`, `HasDatabase`, `HasDockerfile`, `HasPipeline`, `HasKubernetes`) into `manifests/ecosystems.yaml`.
- **Hybrid Pipeline Output Schema**: Output **both** per-repo `exports/{timestamp}/pipelines/{org}-{repo}-pipeline.json` (with `workflows`, `jobs`, `needs` edges, and `anti_patterns` for Astro `PipelineView.astro`) AND aggregate `exports/{timestamp}/relationships/pipeline_topology.{json,csv,yaml}` for org-wide rollups.
- **4-Ecosystem Structural Code Analysis**: Use Python `ast` + `radon` for Python, and lightweight structural/regex/file-boundary extractors for `.NET`, `React/TS`, and `Java Spring Boot` so all 4 MVP ecosystems generate real Arc42 component diagrams and complexity/LoC metrics without requiring external `.NET` or `Java` SDKs installed.

---

## 3. User Scenarios & Testing *(mandatory)*

### User Story 1 - Declarative Policy-as-Code Discovery & Classification (Priority: P1)

As an engineering leader, I want `atruss discover` to inspect repository file trees via `/git/trees?recursive=1` and classify repositories using external YAML manifests (`manifests/ecosystems.yaml`), so that all 27 discovery columns and 4 ecosystems are accurately populated without hardcoded Python rules.

**Independent Test**: Run `atruss discover --org github-samples` (or against mocked tree payloads and local paths) and verify that `repositories.json`, `repositories.csv`, and `repositories.yaml` accurately report `PrimaryLanguage`, `FrameworkType`, `HasDockerfile`, `HasPipeline`, `HasKubernetes`, and `DocumentationPriority`.

**Acceptance Scenarios**:
1. **Given** `manifests/ecosystems.yaml` defining rules for Python, .NET, React/TS/JS, and Java Spring Boot, **When** `classify_repository()` runs on a file tree (root or nested monorepo paths), **Then** it returns the matching ecosystem, sub-framework, and 27-column boolean flags.
2. **Given** a new framework rule added to `manifests/ecosystems.yaml`, **When** `classify_repository()` runs, **Then** the new framework is detected with zero Python code modifications.

---

### User Story 2 - Unified Dual-Mode Pipeline DAG & Anti-Pattern Analysis (Priority: P1)

As a DevOps engineer, I want `atruss analyze-pipeline` to support both `--from-discovery` (API/clone) and `--repos-file` / `--path` (local/clone), parse real `.github/workflows/*.yml` files using `parser.py`, `dag_builder.py`, and `heuristics.py`, and output both per-repo pipeline JSONs and aggregate topology rollups.

**Independent Test**: Execute `atruss analyze-pipeline` via `--from-discovery` and `--repos-file` against `Azure-Samples/todo-nodejs-mongo-terraform` and `github-samples/pets-workshop`, verifying both `exports/latest/pipelines/{org}-{repo}-pipeline.json` and `exports/latest/relationships/pipeline_topology.json` are generated with zero mock data.

**Acceptance Scenarios**:
1. **Given** a repository with `.github/workflows/*.yml`, **When** `atruss analyze-pipeline` runs, **Then** `pipelines/{org}-{repo}-pipeline.json` is written matching the exact schema expected by `web/src/components/PipelineView.astro` (`workflows[].jobs`, `needs`, `anti_patterns`).
2. **Given** a `--repos-file` list or `--path` local directory, **When** `atruss analyze-pipeline` runs, **Then** `_analyze_repo_workflows()` parses all nested workflows and exports deterministic JSON and Markdown DAGs.

---

### User Story 3 - Multi-Ecosystem Structural Code Analysis & Arc42 Generation (Priority: P1)

As a software architect, I want `atruss analyze-code` to extract architectural components (API endpoints, services, data access layers, UI components) and basic LoC/complexity metrics across all 4 MVP ecosystems (Python, .NET, React/TS/JS, Java Spring Boot), outputting canonical JSON and Arc42 Markdown reports into `exports/latest/reports/`.

**Independent Test**: Run `atruss analyze-code` against fixtures for Python, .NET, React/TS, and Java Spring Boot and verify non-empty `architecture_components` and valid Mermaid component diagrams in `exports/latest/reports/{org}-{repo}-report.md`.

**Acceptance Scenarios**:
1. **Given** a Python, .NET, React/TS, or Java Spring Boot repository, **When** `orchestrate_deep_analysis()` runs, **Then** it extracts controllers/routes, services, and data/repository layers and computes LoC and file complexity metrics.
2. **Given** the extracted components, **When** report export runs, **Then** `{org}-{repo}-report.md` and `{org}-{repo}-analysis.json` are written to `exports/latest/reports/` so Astro's `ArchitectureView.astro` renders them natively.

---

### User Story 4 - 5-Gate Agentic Coding Workflow Validator & Zero-Skip Test Suite (Priority: P1)

As a maintainer using local and remote AI agents, I want an automated validation script (`scripts/validate_agent_workflow.py`) and a 100% active `pytest` suite with zero `pytest.skip()` placeholders, so that no agent task can be marked complete if tests are skipped, mocked, or out of sync with Astro schemas.

**Independent Test**: Run `python scripts/validate_agent_workflow.py --spec specs/006-core-unification-and-eval` and `pytest`, verifying all 5 gates pass and 0 tests are skipped.

**Acceptance Scenarios**:
1. **Given** the repository test suite, **When** `pytest` runs, **Then** all unit and integration tests (`test_cli_inputs.py`, `test_todo_nodejs_mongo.py`, `test_pets_workshop_monorepo.py`, `test_classification_e2e.py`, `test_pipeline_dag_e2e.py`, `test_coverage_e2e.py`, `test_golden_snapshots.py`, `test_performance.py`) execute and pass with 0 skips.
2. **Given** any commit or agent task completion, **When** `scripts/validate_agent_workflow.py` runs, **Then** it verifies Spec-to-Task coverage, AST anti-stub/anti-skip rules, Pytest execution, Python-to-Astro schema parity, and byte-for-byte determinism.

---

## 4. Functional Requirements

- **FR-001**: System MUST externalize all ecosystem, framework, and 27-column discovery classification rules into `manifests/ecosystems.yaml` and load them dynamically in `src/analyzers/classification.py`.
- **FR-002**: `atruss discover` MUST fetch the repository file tree via `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1` (with graceful fallback on empty/truncated trees) and populate all 27 `DiscoveryManifestItem` fields via the YAML classification engine.
- **FR-003**: `atruss analyze-pipeline` MUST support `--from-discovery <json>`, `--repos-file <txt>`, and `--path <dir>`, using dual-mode fetching (GitHub contents/trees API or shallow `git clone --depth 1` via `GitCloner`).
- **FR-004**: `atruss analyze-pipeline` MUST remove all hardcoded mock nodes and wire `src/analyzers/pipeline/parser.py`, `dag_builder.py`, and `heuristics.py` to generate real job nodes, `needs:` edges, triggers, and anti-pattern findings.
- **FR-005**: `atruss analyze-pipeline` MUST output both per-repository `exports/{timestamp}/pipelines/{org}-{repo}-pipeline.json` (matching Astro's `PipelineView.astro`) AND aggregate `exports/{timestamp}/relationships/pipeline_topology.{json,csv,yaml}` (plus symlink/copy to `exports/latest/`).
- **FR-006**: `src/core/utils/` and `src/core/exporters/` MUST be unified so there is a single canonical set of JSON, YAML, CSV, and Arc42 Markdown exporters writing to `exports/{timestamp}/` and `exports/latest/`.
- **FR-007**: `src/analyzers/code/` MUST implement structural extractors for all 4 MVP ecosystems:
  - `python_ast.py` (Python AST + Radon complexity/LoC)
  - `dotnet_structural.py` (`.csproj`, `Controllers`, `Services`, `DbContext`/Repository, Minimal APIs)
  - `js_ts_structural.py` (`package.json`, React/Next/Vite components, Express/Nest/API routes, state stores)
  - `java_structural.py` (`pom.xml`/`build.gradle`, `@RestController`/`@Controller`, `@Service`, `@Repository`/`JpaRepository`)
- **FR-008**: `atruss analyze-code` MUST write `{org}-{repo}-report.md` and `{org}-{repo}-analysis.json` into `exports/{timestamp}/reports/` (and `exports/latest/reports/`) matching `web/src/components/ArchitectureView.astro`.
- **FR-009**: `scripts/validate_agent_workflow.py` MUST enforce the 5-Gate Agentic Evaluation framework (Spec-Plan-Task traceability, AST anti-stub/anti-skip scan, Pytest 0-skip gate, Astro schema contract verification, and SHA-256 determinism check).
- **FR-010**: All `pytest.skip()` placeholders in `tests/integration/` MUST be replaced with real, deterministic tests using local synthetic fixtures for fast offline CI and pinned-SHA repositories for E2E verification.

---

## 5. Success Criteria

- **SC-001**: `pytest` runs 100% of unit and integration tests with **0 failures, 0 errors, and 0 skipped tests**.
- **SC-002**: Modifying `manifests/ecosystems.yaml` adds or updates framework classification with 0 lines of Python changed.
- **SC-003**: Running `atruss discover` → `atruss analyze-pipeline` → `atruss analyze-code` populates `exports/latest/{repos,pipelines,relationships,reports}/` such that `cd web && npm run build` renders Discovery, Pipeline DAGs, and Arc42 Architecture views with zero empty-state fallbacks on analyzed repos.
- **SC-004**: `python scripts/validate_agent_workflow.py --spec specs/006-core-unification-and-eval` exits with code `0` and produces an `A` grade in `exports/latest/agent-eval-report.json`.
