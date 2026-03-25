# Tasks: Structured Output Formats

**Input**: Design documents from `/specs/004-structured-output-formats/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Tests**: Required per Constitution VII (Strict Test DD). Failing tests must be written first.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base classes for exporters.

- [ ] T001 Create `BaseExporter` interface/abstract class in `src/atruss/core/exporters/base_exporter.py`
- [ ] T002 Initialize empty structural implementations for `json_exporter.py`, `csv_exporter.py`, and `yaml_exporter.py` in `src/atruss/core/exporters/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Foundational schemas must be confirmed decoupleable before implementing concrete exporters.

- [ ] T003 Confirm `DiscoveryManifestItem` and `PipelineDAG` (Nodes/Edges) Pydantic models in `src/atruss/core/models/` map neatly to dictionaries (ensuring no circular references or unhandled complex types block generic JSON/YAML serialization)

**Checkpoint**: Models are ready for seamless structural serialization. Exporters can now be built.

---

## Phase 3: User Story 1 - Structured Repo Discovery Output (Priority: P1)

**Goal**: Enable repository discovery to output its results in structural formats (CSV, JSON, and YAML) via `--format` flag.

**Independent Test**: Running the discover CLI with `--format csv`, `--format json`, and `--format yaml` independently produces strictly formatted data matching the discovery schemas.

### Tests for User Story 1 (MANDATORY per TDD) ⚠️

- [ ] T004 [P] [US1] Write failing unit test for `CSVExporter` processing discovery models in `tests/unit/exporters/test_csv_exporter.py`
- [ ] T005 [P] [US1] Write failing unit test for `YAMLExporter` processing discovery models in `tests/unit/exporters/test_yaml_exporter.py`
- [ ] T006 [P] [US1] Write failing unit test for `JSONExporter` processing discovery models in `tests/unit/exporters/test_json_exporter.py`
- [ ] T007 [P] [US1] Write failing integration test for `python -m atruss.cli discover` output formatting in `tests/integration/test_structured_exports.py`

### Implementation for User Story 1

- [ ] T008 [P] [US1] Implement `CSVExporter.export_discovery()` mapping the manifest items to CSV rows in `src/atruss/core/exporters/csv_exporter.py` 
- [ ] T009 [P] [US1] Implement `YAMLExporter` converting the model dict to YAML via `pyyaml` in `src/atruss/core/exporters/yaml_exporter.py`
- [ ] T010 [P] [US1] Implement `JSONExporter` natively converting the model dict to JSON in `src/atruss/core/exporters/json_exporter.py`
- [ ] T011 [US1] Update `discover.py` CLI parser to accept `--format` flag
- [ ] T012 [US1] Integrate exporters into the `discover` command execution flow in `src/atruss/cli/discover.py`

**Checkpoint**: At this point, the repository discovery command correctly dumps CSV, JSON, and YAML structured data.

---

## Phase 4: User Story 2 - Structured Pipeline Visualization Output (Priority: P1)

**Goal**: Enable pipeline visualization DAGs to be exported as structured formats (CSV, JSON, YAML) so DevOps can programmatically analyze dependencies instead of purely rendering visual diagrams.

**Independent Test**: Running the `analyze-pipeline` CLI with `--format csv`, `--format json`, and `--format yaml` independently produces DAG node/edge structures serialized to the respective format.

### Tests for User Story 2 (MANDATORY per TDD) ⚠️

- [ ] T013 [P] [US2] Write failing unit test for flattening the PipelineDAG into CSV nodes/edges in `tests/unit/exporters/test_csv_exporter.py`
- [ ] T014 [P] [US2] Write failing unit tests for PipelineDAG YAML export in `tests/unit/exporters/test_yaml_exporter.py`
- [ ] T015 [P] [US2] Write failing unit tests for PipelineDAG JSON serialization in `tests/unit/exporters/test_json_exporter.py`
- [ ] T016 [P] [US2] Write failing integration test for `python -m atruss.cli analyze-pipeline` CLI formatting in `tests/integration/test_structured_exports.py`

### Implementation for User Story 2

- [ ] T017 [P] [US2] Implement `CSVExporter.export_pipeline()` flattening the DAG into node lists in `src/atruss/core/exporters/csv_exporter.py`
- [ ] T018 [P] [US2] Integrate the `PipelineDAG` model dumping into the generic `YAMLExporter` in `src/atruss/core/exporters/yaml_exporter.py`
- [ ] T019 [P] [US2] Ensure standard `JSONExporter` correctly handles the PipelineDAG in `src/atruss/core/exporters/json_exporter.py`
- [ ] T020 [US2] Update `analyze_pipeline.py` CLI parser to accept the `--format` flag
- [ ] T021 [US2] Connect `analyze_pipeline` command flow to the exporters in `src/atruss/cli/analyze_pipeline.py`

**Checkpoint**: Both Discovery and Pipeline commands now output strictly structured CSV/JSON/YAML data fully independently.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T022 [P] Update `docs/` or `README.md` to reflect the new `[json, yaml, csv]` structural output features and quickstart examples
- [ ] T023 Run `flake8` / `ruff` formatting and code cleanup across exporter changes
- [ ] T024 Validate CI pipeline executes the integration tests in `test_structured_exports.py` successfully

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: Start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1.
- **User Stories (Phase 3 & 4)**: Depend on Phase 2 completion. Can be parallelized.
- **Polish (Final Phase)**: Depends on User Stories completion.

### Parallel Opportunities
- Exporter tests (T004-T007 and T013-T016) can run entirely in parallel.
- Concrete Exporter logic (T008-T010 and T017-T019) can be developed independently in parallel.
- US1 (`discover` CLI updates) and US2 (`analyze-pipeline` CLI updates) can be worked on concurrently by two engineers without stepping on each other.

---

## Implementation Strategy

### MVP First
- Deliver Phase 1, Phase 2, and Phase 3 (US1: Discovery Export). 
- Validate that the single `discover` command can output perfectly formatted CSV.
- Add Phase 4 (Pipeline Export) leveraging the patterns defined in US1.
