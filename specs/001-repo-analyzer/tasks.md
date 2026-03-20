---
description: "Task list template for feature implementation"
---

# Tasks: Repository Discovery and Deep Analysis

**Input**: Design documents from `specs/001-repo-analyzer/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included natively where complex algorithmic validation (DAG building, AST generation) is necessary to ensure safety. 

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Create project directories (src/core, src/cli, src/analyzers, tests/)
- [x] T002 Initialize Python 3.12 project with pyproject.toml and requirements.txt (fastapi, celery, redis, sqlalchemy, typer, pyyaml, networkx)
- [x] T003 [P] Configure ruff and pytest in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [x] T004 Setup SQLAlchemy database connection module and base models in `src/core/database.py`
- [x] T005 Initialize Alembic for schema migrations
- [x] T006 [P] Configure Celery app and Redis integration in `src/core/worker.py`
- [x] T007 [P] Create base Typer/Click CLI application wrapper in `src/cli/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Discover and Classify Repositories (Priority: P1) 🎯 MVP

**Goal**: Authenticate to GitHub (optional PAT), discover repositories, and classify their ecosystem using YAML/JSON manifests.

**Independent Test**: Can be fully tested by providing a target GitHub organization and verifying that it returns a classified repository inventory list.

### Tests for User Story 1
- [x] T008 [P] [US1] Unit test for manifest classification engine in `tests/unit/test_classification.py`

### Implementation for User Story 1
- [x] T009 [P] [US1] Create `GitRepository` SQLAlchemy model in `src/core/models/repository.py` and generate Alembic migration
- [x] T010 [US1] Implement ecosystem classification engine in `src/analyzers/classification.py`
- [x] T011 [US1] Implement GitHub API client for org scanning in `src/core/services/github_api.py` (with optional PAT auth)
- [x] T012 [US1] Implement `repo-analyzer discover` command in `src/cli/commands/discover.py`

**Checkpoint**: At this point, User Story 1 (Discovery) should be fully functional and testable independently via CLI.

---

## Phase 4: User Story 2 - Analyze CI/CD Pipelines (Priority: P1)

**Goal**: Parse `.github/workflows`, build a NetworkX DAG, and detect anti-patterns (e.g. missing test gates).

**Independent Test**: Provide local workflow YAML files and verify the DAG structure and exact anti-pattern findings json.

### Tests for User Story 2
- [x] T013 [P] [US2] Unit tests for NetworkX DAG cycle detection and heuristics in `tests/unit/test_dag_builder.py`

### Implementation for User Story 2
- [x] T014 [P] [US2] Create models (`PipelineWorkflow`, `PipelineJob`, `JobDependency`, `AntiPatternFinding`) in `src/core/models/pipeline.py` and generate Alembic migrations
- [x] T015 [US2] Implement workflow YAML parser service in `src/analyzers/pipeline/parser.py`
- [x] T016 [US2] Implement DAG builder using NetworkX in `src/analyzers/pipeline/dag_builder.py`
- [x] T017 [US2] Implement core anti-pattern heuristics (no tests, hardcoded secrets) in `src/analyzers/pipeline/heuristics.py`
- [x] T018 [US2] Implement `repo-analyzer analyze-pipeline` command in `src/cli/commands/analyze_pipeline.py`

**Checkpoint**: At this point, User Story 2 should work completely independent of deep code analysis.

---

## Phase 5: User Story 3 - Deep Local Code Analysis (Priority: P2)

**Goal**: Perform static architecture analysis (AST) and generate Arc42 Markdown documentation + Mermaid diagrams. Skip unsupported ecosystems.

**Independent Test**: Run against a local Python sample project and verify output markdown file and Mermaid topology.

### Tests for User Story 3
- [x] T019 [P] [US3] Unit tests for Arc42 generation from mock architecture data in `tests/unit/test_arc42_generator.py`

### Implementation for User Story 3
- [x] T020 [P] [US3] Create `ArchitectureComponent` model in `src/core/models/architecture.py` and generate Alembic migration
- [x] T021 [US3] Implement dynamic ecosystem check and graceful skip logic in `src/analyzers/code/orchestrator.py`
- [x] T022 [US3] Implement Python AST Wrapper (Radon/Bandit interfaces) in `src/analyzers/code/python_ast.py`
- [x] T023 [US3] Implement Arc42 markdown and Mermaid diagram Generator in `src/core/services/report_generator.py`
- [x] T024 [US3] Implement `repo-analyzer analyze-code` command in `src/cli/commands/analyze_code.py`

**Checkpoint**: All US3 implementations complete.

---

## Phase 6: User Story 4 - Extract Test Coverage (Priority: P2)

**Goal**: Extract test coverage metrics from CI/CD pipeline run logs and artifacts for supported testing tools.

**Independent Test**: Mock workflow run logs containing known coverage summaries and verify accurate extraction parsing.

### Tests for User Story 4
- [x] T025 [P] [US4] Unit tests for log parsing and coverage extraction regexes in `tests/unit/test_coverage_extractor.py`

### Implementation for User Story 4
- [x] T026 [US4] Implement GitHub API fetching logic for workflow run logs in `src/core/services/github_api.py`
- [x] T027 [US4] Implement regex/AST-based coverage extraction for common tools (pytest, Jest, dotnet test) in `src/analyzers/pipeline/coverage.py`
- [x] T028 [US4] Update pipeline DB models (`PipelineWorkflow`) to store coverage metric in `src/core/models/pipeline.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: E2E Integration Testing & Golden Snapshots

**Purpose**: Strict E2E compliance validation against pinned public repos ensuring accurate classifications and parsed DAG outputs.

- [x] T029 [P] Implement end-to-end integration test scaffolding (cloning public fixture repos) in `tests/integration/conftest.py`
- [x] T030 [P] Implement `TR-CLS` Classification E2E tests for Python, .NET, React/TypeScript, and Java Spring Boot in `tests/integration/test_classification_e2e.py`
- [x] T031 [P] Implement `TR-ANA-PY/DOTNET/TS/JAVA` Coverage Extraction E2E tests for pytest, dotnet test, Jest, and Jacoco in `tests/integration/test_coverage_e2e.py`
- [x] T032 [P] Implement `TR-DAG` Pipeline DAG E2E tests (Basic, OS Matrix, Parallel, branching, anti-patterns) in `tests/integration/test_pipeline_dag_e2e.py`
- [x] T033 Implement `TR-CON` Golden Master JSON snapshot regressions (DAG + Reports matching CodeLens schema) in `tests/integration/test_golden_snapshots.py`
- [x] T034 Implement `TR-PERF` Performance test bounds (< 3 minutes SLA on medium repos) in `tests/integration/test_performance.py`

---

## Phase 8: Polish & CI Matrix

**Purpose**: Finalize the developer experience and continuous integration pipelines.

- [x] T035 [P] Update `docs/` and README.md with final command usage flags
- [x] T036 Write multi-job GitHub Actions CI workflow matrix (`unit-tests`, `integration-python`, `integration-dotnet`, `integration-js`, `integration-java`, `golden-report`, `performance-smoke`) in `.github/workflows/tests.yml`

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies - starts immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion - BLOCKS all.
- **User Stories (Phase 3+)**: Can run sequentially or perfectly in parallel (different data models, different sub-module packages).

### Parallel Opportunities
- Models in US1, US2, and US3 (`T009`, `T014`, `T020`) can be written in parallel by 3 developers right after `T004` (SQLAlchemy setup).
- Unit tests (`T008`, `T013`, `T019`) can be written in parallel before implementation logic.

### Implementation Strategy
1. **MVP First Delivery**: Complete Phase 1 & 2 infrastructure, then execute Phase 3 (US1 - Discovery). This immediately validates the GitHub API auth scopes and the database.
2. **Incremental Delivery**: Deliver Phase 4 (Pipelines) as isolated PR. Then deliver Phase 5 (AST Deep Scan) as the final isolated PR.
