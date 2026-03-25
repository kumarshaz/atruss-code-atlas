# Tasks: Structured Output Formats (GitHub Parity Edition)

**Input**: Design documents from `/specs/004-structured-output-formats/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md

**Tests**: Tests are MANDATORY per Constitution VII (TDD). Write failing tests before implementation tasks.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure accommodating the massive async transition.

- [x] T001 Strip legacy Git cloner dependencies to strictly enforce online-only `GET /git/trees` payload extractions.
- [x] T002 Implement `GitHubClient` HTTP async client accommodating Link-Header `rel="next"` pagination and proactive `X-RateLimit-Remaining` threshold checks in `src/core/http_client.py`.
- [x] T003 [P] Implement `validate_token` logic enforcing Bearer token authentication alongside strict dual-logger token masking preventing ephemeral leakages in `src/core/auth.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create deterministic archival filesystem manager to handle `exports/{timestamp}/` folder bounds in `src/core/utils/export_manager.py`.
- [x] T005 [P] Create `DiscoveryManifestItem` and `TopologyNode` explicit domain models mirroring the 27-column relaxed CSV payload structure in `src/models/discovery.py`.
- [x] T006 [P] Create cross-referenced DAG entity models for environments, workflows, and runner associations in `src/models/topology.py`.

---

## Phase 3: User Story 1 - Structured Repo Discovery Output (Priority: P1) 🎯 MVP

**Goal**: Achieve the primary automated repository discovery generating `repositories.json`, `repositories.csv`, and `yaml-contents.json`.

**Independent Test**: Running `repo-analyzer discover --org X` generates exactly 3 archival datasets retaining valid CSV/JSON headers.

### Tests for User Story 1 (MANDATORY per TDD) ⚠️

- [x] T007 [P] [US1] Write unit tests mapping exact GitHub REST payloads down to dynamic CSV and JSON columns in `tests/unit/exporters/test_discovery_exporter.py`.
- [x] T007b [US1] Write unit tests enforcing graceful structural empty `{}` or `[]` dumps for zero-repository organizations matching edge case constraints.

### Implementation for User Story 1

- [x] T008 [P] [US1] Implement `DiscoveryArchiver` extracting CSV/JSON representations in `src/core/exporters/discovery_exporter.py`.
- [x] T009 [US1] Refactor `discover.py` CLI command bypassing prior flat tables and substituting the new comprehensive `github-repo-discovery.py` reference 8-phase logic.
- [x] T010 [US1] Wire exclusion patterns and dynamic column mappers natively to stdout logs.

---

## Phase 4: User Story 2 - Structured Pipeline Visualization Output (Priority: P1)

**Goal**: Transform internal pipeline analysis engines to collapse the classic Pipeline topology into the 3-layer Mermaid/CSV GitHub actions workflows outputs.

**Independent Test**: Run `analyze-pipeline` generating the strict relationships JSON and visual Mermaid models without missing associations.

### Tests for User Story 2 (MANDATORY per TDD) ⚠️

- [x] T011 [P] [US2] Write unit tests ensuring DAG edges natively map to the exact JSON envelope in `tests/unit/exporters/test_pipeline_exporter.py`.

### Implementation for User Story 2

- [x] T012 [P] [US2] Implement `TopologyArchiver` extracting CSV/JSON pipeline hierarchy and relationships mapping in `src/core/exporters/pipeline_exporter.py`.
- [x] T013 [P] [US2] Update Mermaid rendering templates enforcing the strict 3-subgraph model (Workflows, Targets, Resources) in `src/core/exporters/markdown_exporter.py`.
- [x] T014 [US2] Overhaul `analyze_pipeline.py` CLI traversing the outputs from discovery and executing the full run context bindings mapped to the explicit topological models.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T015 [P] Documentation updates in `quickstart.md` and `README.md`.
- [x] T016 Code cleanup and `ruff` / `mypy` linting compliance checks across the async transition.
- [ ] T017 Execute integration end-to-end tests validating full structural mappings by pointing extraction explicitly against the `github-samples/pets-workshop` baseline to uphold Constitution VII compliance (`tests/integration/test_full_architecture.py`).

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup & Foundational**: Must be strictly accomplished first. Async architecture will block sync methods cleanly.
- **User Story 1 & 2**: Can be worked concurrently once exporters architectures are stubbed out. US2 relies on US1 inputs inherently when invoked via CLI, so US1 is prioritized.

## Implementation Strategy

1. Transition the HTTP clients strictly relying on async requests.
2. Formulate explicit file managers ensuring the `exports/` folder targets are deterministic.
3. Test exporter formats against GitHub mocked payloads.
4. Execute `discover`.
5. Execute `analyze-pipeline`. 
