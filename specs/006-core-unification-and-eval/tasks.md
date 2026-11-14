# Tasks: Core Engine Unification, Policy-as-Code & Agentic Workflow Evaluation

**Input**: Design documents from `/specs/006-core-unification-and-eval/`  
**Prerequisites**: `plan.md`, `spec.md`  
**Verification Rule**: Every task MUST be verified by running `pytest` and `scripts/validate_agent_workflow.py` with 0 skipped tests before marking complete.

---

## Phase 1: Policy-as-Code YAML Manifests & Discovery Tree Analysis (US1)

**Goal**: Externalize all classification rules into `manifests/ecosystems.yaml` and upgrade `discover.py` to analyze recursive Git trees (`/git/trees/{sha}?recursive=1`).

- [x] T001 [P] [US1] Create `manifests/ecosystems.yaml` defining priority-ordered detection rules for Python, .NET, React/TS/JS, Java Spring Boot, sub-frameworks, and the 27-column discovery signals (`HasAPI`, `HasService`, `HasFrontend`, `HasDatabase`, `HasDockerfile`, `HasPipeline`, `HasKubernetes`, `DocumentationPriority`).
- [x] T002 [US1] Write unit tests in `tests/unit/test_classification.py` testing root and nested monorepo file trees against `manifests/ecosystems.yaml`, including dynamic rule loading (`FR-001`).
- [x] T003 [US1] Refactor `src/analyzers/classification.py` to load `manifests/ecosystems.yaml` dynamically and return both `ClassificationResult` (ecosystem + framework) and the 27-column discovery dictionary (`FR-001`).
- [x] T004 [US1] Update `src/cli/commands/discover.py` to fetch `/repos/{owner}/{repo}/git/trees/{sha}?recursive=1` (with fallback on empty/truncated repos) and populate all 27 fields of `DiscoveryManifestItem` using `classification.py` (`FR-002`).
- [x] T005 [US1] Update `src/core/utils/export_manager.py` so every export run writes to `exports/{timestamp}/` and automatically syncs/updates `exports/latest/` (`FR-005`, `FR-006`).

---

## Phase 2: Pipeline Analyzer Unification & Dual-Schema Export (US2)

**Goal**: Restore `--repos-file` and `_analyze_repo_workflows`, wire real `parser.py` + `dag_builder.py` + `heuristics.py`, and output both per-repo `pipelines/{org}-{repo}-pipeline.json` and aggregate `relationships/pipeline_topology.{json,csv,yaml}`.

- [x] T006 [P] [US2] Expand `src/analyzers/pipeline/parser.py`, `dag_builder.py`, and `heuristics.py` to parse workflow YAML triggers, job `needs:` edges, runner types, step counts, and all 7 PRD anti-patterns (`NO_TEST_GATE`, `NO_CACHE`, `NO_ARTIFACT_HANDOFF`, `HARDCODED_SECRET`, `SEQUENTIAL_ONLY`, `UNFILTERED_MAIN_PUSH`, `UNLABELED_SELF_HOSTED`) (`FR-004`).
- [x] T007 [P] [US2] Update `src/core/exporters/pipeline_exporter.py` to export **both** per-repo `pipelines/{org}-{repo}-pipeline.json` (matching `PipelineView.astro`) AND aggregate `relationships/pipeline_topology.{json,csv,yaml}` (`FR-005`).
- [x] T008 [US2] Refactor `src/cli/commands/analyze_pipeline.py` to support `--from-discovery`, `--repos-file`, and `--path`, restore `_analyze_repo_workflows()`, remove `# Mock targeting behavior`, and support dual-mode API workflow fetch + shallow `GitCloner` fallback (`FR-003`, `FR-004`).
- [x] T009 [US2] Verify and fix `tests/unit/test_cli_inputs.py` and `tests/integration/test_todo_nodejs_mongo.py` so both pass natively (`FR-003`, `SC-001`).

---

## Phase 3: 4-Ecosystem Structural Code Analysis & Arc42 Reports (US3)

**Goal**: Extract architectural components and LoC/complexity metrics across Python, .NET, React/TS/JS, and Java Spring Boot, outputting Arc42 Markdown and JSON to `exports/latest/reports/`.

- [x] T010 [P] [US3] Write unit tests for `.NET`, `React/TS/JS`, `Java Spring Boot`, and `Python` structural analyzers in `tests/unit/test_arc42_generator.py` (`FR-007`).
- [x] T011 [P] [US3] Enhance `src/analyzers/code/python_ast.py` with LoC and Radon cyclomatic complexity calculation (`FR-007`).
- [x] T012 [P] [US3] Implement `src/analyzers/code/dotnet_structural.py` to extract `.csproj` modules, ASP.NET Controllers/Minimal APIs, Worker Services, and EF Core `DbContext`/Repositories (`FR-007`).
- [x] T013 [P] [US3] Implement `src/analyzers/code/js_ts_structural.py` to extract `package.json` dependencies, React/Next/Vite UI components, and Node/Express/API routes (`FR-007`).
- [x] T014 [P] [US3] Implement `src/analyzers/code/java_structural.py` to extract `pom.xml`/`build.gradle` modules, `@RestController`, `@Service`, and `@Repository` boundaries (`FR-007`).
- [x] T015 [US3] Update `src/analyzers/code/orchestrator.py` and `src/cli/commands/analyze_code.py` to route all 4 ecosystems (plus monorepo submodules) and export `{org}-{repo}-report.md` and `{org}-{repo}-analysis.json` into `exports/latest/reports/` matching `ArchitectureView.astro` (`FR-008`).

---

## Phase 4: Zero-Skip E2E Test Harness & 5-Gate Agentic Workflow Validator (US4)

**Goal**: Eliminate all `pytest.skip()` placeholders, register pytest markers, and implement `scripts/validate_agent_workflow.py`.

- [x] T016 [P] [US4] Register custom pytest markers (`integration`, `e2e`, `benchmark`) in `pyproject.toml` to eliminate `PytestUnknownMarkWarning` (`SC-001`).
- [x] T017 [P] [US4] Replace `pytest.skip` in `tests/integration/test_classification_e2e.py`, `test_coverage_e2e.py`, `test_pipeline_dag_e2e.py`, `test_golden_snapshots.py`, and `test_performance.py` with real, deterministic tests against multi-ecosystem fixtures (`FR-010`).
- [x] T018 [P] [US4] Implement full discovery-to-export assertions in `tests/integration/test_structured_exports.py` and `tests/integration/test_full_architecture.py` (using deterministic mocked HTTP transport when `GH_TOKEN` is absent so it never skips) (`FR-010`).
- [x] T019 [US4] Implement `scripts/validate_agent_workflow.py` enforcing Gate 1 (Spec-Plan-Task traceability), Gate 2 (AST anti-stub/anti-skip scan), Gate 3 (Pytest 0-skip execution), Gate 4 (Python-to-Astro schema contract check), and Gate 5 (SHA-256 determinism check), outputting `exports/latest/agent-eval-report.json` (`FR-009`, `SC-004`).
- [x] T020 [US4] Update `.github/workflows/tests.yml` to run the full unit + integration test suite and `python scripts/validate_agent_workflow.py` (`SC-001`, `SC-004`).
