---
description: "Task list template for feature implementation"
---

# Tasks: Portable Output Architecture & Strict Test Harness

**Input**: Design documents from `/specs/003-portable-test-harness/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are MANDATORY per Constitution VII (TDD). Write failing tests before implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Remove FastAPI, Celery, Redis, and SQLAlchemy dependencies from `pyproject.toml`.
- [x] T002 Purge DB migrations, `src/core/database.py`, and `src/core/worker.py` completely to satisfy offline portability requirements.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create `PortableArtifact` and `HarnessFixture` Pydantic models mapping the JSON schema in `src/models/artifacts.py`.
- [x] T004 Create foundational Pytest fixture wrapper that explicitly clones pinned SHAs using purely native temporary directories in `tests/utils/fixture_manager.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Offline CLI Execution & Immutable Docs-as-Code Output (Priority: P1) 🎯 MVP

**Goal**: Output byte-for-byte deterministic JSON and Markdown files directly to the filesystem natively, disconnecting all database logic.

**Independent Test**: Can be fully tested by executing `repo-analyzer discover` and `analyze-pipeline` locally to assert outputs are written as pure `.json`/`.md` arrays mapped to `--output-dir`.

### Tests for User Story 1 (MANDATORY per TDD) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T005 [P] [US1] Integration test targeting offline static file generation bounding schemas mapped directly into temporary output directories in `tests/integration/test_offline_generation.py`.

### Implementation for User Story 1

- [x] T006 [P] [US1] Build native `JSONExporter` logic writing extracted pipeline/architectural bounds locally in `src/core/utils/json_exporter.py`.
- [x] T007 [P] [US1] Build native `MarkdownExporter` stringifying Arc42 strings with ````mermaid```` sequences locally in `src/core/utils/markdown_exporter.py`.
- [x] T008 [US1] Refactor `analyze-pipeline` CLI in `src/cli/commands/analyze_pipeline.py` deleting all DB persistence routes and hooking native Exporters.
- [x] T009 [US1] Refactor `analyze-code` CLI in `src/cli/commands/analyze_code.py` deleting DB dependencies hooking purely native Exporters.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Comprehensive Fixture Testing against Real Monorepos (Priority: P1)

**Goal**: Execute test harnesses against specific, real-world public repositories to aggressively validate pipeline topology logic natively.

**Independent Test**: Execute the Pytest suite where integration fixtures isolate `github-samples/pets-workshop` and assert known module DAG extractions.

### Tests for User Story 2 (MANDATORY per TDD) ⚠️

- [x] T010 [P] [US2] Integration test targeting the pinned `pets-workshop` SHA guaranteeing client, server, and content sub-workflow parsings in `tests/integration/test_pets_workshop_monorepo.py`.
- [x] T011 [P] [US2] Integration test targeting the pinned `Azure-Samples/todo-nodejs-mongo-terraform` parsing workflows natively in `tests/integration/test_todo_nodejs_mongo.py`.

### Implementation for User Story 2

- [x] T012 [P] [US2] Expand pipeline DAG traversal recursive sweep mapping explicitly across all `.github/workflows` nested directories in `src/analyzers/pipeline/parser.py`.
- [x] T013 [US2] Run test suite natively generating the `analysis-result.json` snapshots and locking them against regression.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Chained Input Sourcing via Variable Lists (Priority: P2)

**Goal**: Extend analysis commands to explicitly ingest newline-delimited text arrays `(--repos-file)` dynamically bypassing initial discovery pipelines.

**Independent Test**: Pass a `.txt` mapping of two dummy targets into `--repos-file` bounds and verify iterators run across both targets perfectly.

### Tests for User Story 3 (MANDATORY per TDD) ⚠️

- [x] T014 [P] [US3] Contract tests verifying iteration behavior over flat text strings natively in `tests/unit/test_cli_inputs.py`.
- [x] T015 [P] [US3] Integration test verifying multiple pipelines cloned consecutively based on target lists in `tests/integration/test_array_sourcing.py`.

### Implementation for User Story 3

- [x] T016 [P] [US3] Parse and validate `--repos-file` string variables wrapping Typer input arguments in `src/cli/commands/analyze_pipeline.py`.
- [x] T017 [US3] Expand CLI loop to iterate extracted repository arrays running native git clones sequentially in `src/cli/commands/analyze_pipeline.py`.
- [x] T018 [US3] Ensure identical `--repos-file` iteration array logic applied synchronously within `src/cli/commands/analyze_code.py`.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T019 [P] Update `README.md` natively reflecting strict Docs-as-Code `--output-dir` behaviors and replacing database setup steps.
- [x] T020 Run entire isolated Pytest matrix validating all integrations map to immutable filesystem footprints without 401 unauthenticated locking against GitHub organically.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Blocks all development until databases codebases are systematically purged.
- **Foundational (Phase 2)**: Depends on Phase 1 - BLOCKS all user stories.
- **User Stories (Phase 3+)**: US1 and US2 run in parallel post foundation. US3 chains after US1 output sequences are confirmed locally.
- **Polish (Final Phase)**: Blocks on completion of US3 iterating arrays.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration

### Parallel Opportunities

- Export JSON mapping (T006) and Markdown mapping (T007) run fully in parallel.
- All integration tests against `pets-workshop` (T010) and `todo-java-azure` (T011) run in parallel bounding separate git fixtures dynamically.

## Implementation Strategy

### Incremental Delivery Sequence
1. Foundation -> Exporters implemented natively ensuring all Typer outputs hook to OS paths.
2. Integration Fixtures -> Hook explicit GitHub payloads ensuring extraction topologies map identically without regressions.
3. Input Expanders -> Add flat-file arrays mapping iterating architectures dynamically natively.
