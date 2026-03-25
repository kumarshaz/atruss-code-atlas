# Tasks: Chained Analysis Pipeline

**Input**: Design documents from `/specs/002-chain-analysis/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

*(No external dependency setup required as everything maps to Python standard libraries)*

- [x] T001 Initialize `src/core/utils/git_cloner.py` structural boundaries.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Implement `GitCloner` orchestrator in `src/core/utils/git_cloner.py` handling `subprocess.run` executions mapped to `tempfile.gettempdir()`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chained Code Analysis (Priority: P1) 🎯 MVP

**Goal**: Feed organizational discovery JSON into deep code analyzer orchestrating auto-clones.

**Independent Test**: Can be tested locally by discovering a sample org to JSON, and passing it to `analyze-code` observing the generation of architecture markers.

### Implementation for User Story 1

- [x] T003 [P] [US1] Implement `--output` JSON export logic mapping `DiscoveryManifest` in `src/cli/commands/discover.py`.
- [x] T004 [US1] Add `--from-discovery` manifest reading logic to `src/cli/commands/analyze_code.py`.
- [x] T005 [US1] Orchestrate local clones by mapping `GitCloner` outputs into the AST architecture generator inside `analyze_code.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Chained Pipeline Analysis (Priority: P1)

**Goal**: Feed organizational discovery JSON into the pipeline analyzer to trigger DAG workflow checks across repositories automatically.

**Independent Test**: Can be tested by running `analyze-pipeline` using the generated output JSON from User Story 1.

### Implementation for User Story 2

- [x] T006 [P] [US2] Add `--from-discovery` manifest reading logic to `src/cli/commands/analyze_pipeline.py`.
- [x] T007 [US2] Orchestrate local clones by mapping `GitCloner` outputs into the networkX DAG builder inside `analyze_pipeline.py`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T008 [P] Add unit test mapping limiting `GitCloner` path bounds logically in `tests/unit/test_git_cloner.py`.
- [x] T009 [P] Update `README.md` with Chaining quickstart documentation workflows.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 and User Story 2 can be worked on in parallel after Phase 2 since they target different CLI modules (`analyze_code` vs `analyze_pipeline`).
- **Polish (Final Phase)**: Depends on all desired user stories being complete
