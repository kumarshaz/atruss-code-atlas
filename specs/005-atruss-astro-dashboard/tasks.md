---
description: "Task list for Atruss Astro Dashboard feature implementation"
---

# Tasks: Atruss Astro Dashboard

**Input**: Design documents from `/specs/005-atruss-astro-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Install `fnm` and configure Node.js environment via WSL bash (MUST explicitly use `v22` per Constitution)
- [x] T002 Update `README.md` with WSL `fnm` installation and setup instructions specifying Node.js `v22`
- [x] T003 Initialize Astro project in `web/` directory with Starlight template

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Setup pre-build script in `web/package.json` to copy Python CLI JSON/YAML/Markdown exports into Astro `web/src/content/docs/reports/`
- [x] T005 Generate standard test-fixture samples from the Python CLI into the `/exports` folder

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Brand Realignment (Priority: P1) 🎯 MVP

**Goal**: The CLI entrypoint and documentation to be named `atruss` rather than `repo-analyzer`.

**Independent Test**: Can be independently tested by installing the package in a fresh environment and successfully executing `atruss --help` without reference to the old name.

### Tests for User Story 1 ⚠️

- [x] T006 [TestFirst] [US1] Create failing tests in `tests/` verifying `atruss` execution and import paths

### Implementation for User Story 1

- [x] T007 [P] [US1] Rename package name, CLI entrypoints, and script names in `pyproject.toml` from `repo-analyzer` to `atruss`
- [x] T008 [P] [US1] Update CLI app instantiation to `atruss` in `src/cli/main.py`
- [x] T009 [US1] Update test suite imports and asserts in `tests/` to reflect new `atruss` naming
- [x] T010 [US1] Ensure `0 instances` of `repo-analyzer` exist in code via cross-repository find and replace

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Astro Starlight Web Scaffolding (Priority: P1)

**Goal**: Navigate the generated Markdown outputs through an Astro Starlight web application so that the documentation is highly readable, searchable, and responsive.

**Independent Test**: Can be fully tested by building the Astro app (`npm run build`) and verifying that it serves Starlight documentation pages populated by a sample of generated Markdown.

### Tests for User Story 2 ⚠️

- [x] T011 [TestFirst] [US2] Create failing component tests for Astro markdown rendering and schema validation

### Implementation for User Story 2

- [x] T012 [P] [US2] Configure `web/astro.config.mjs` for Starlight, set dark-mode focused aesthetic
- [x] T013 [P] [US2] Setup Astro Content Collections to parse markdown docs in `web/src/content.config.ts`
- [x] T014 [US2] Define strict Zod schemas inside `web/src/content.config.ts` to validate JSON/YAML data structure
- [x] T015 [US2] Place sample CLI markdown outputs in `web/src/content/docs/reports/` and run dev server to verify rendering

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Summary Dashboard View (Priority: P2)

**Goal**: A high-level summary dashboard that ingests the JSON/YAML data from the Discovery, Pipeline, and Code scans, to see the aggregate system landscape at a glance.

**Independent Test**: Can be tested by visiting the root landing page of the Astro application and verifying that the summary statistics match the input JSON/YAML datasets.

### Tests for User Story 3 ⚠️

- [x] T016 [TestFirst] [US3] Create failing tests verifying `AtlasSummary.astro` receives and formats code analysis JSON correctly

### Implementation for User Story 3

- [x] T017 [P] [US3] Develop `AtlasSummary.astro` component to parse explicit `outputs/` YAML/JSON datasets
- [x] T018 [P] [US3] Override the default Starlight `index.mdx` entry point to load `AtlasSummary.astro`
- [x] T019 [P] [US3] Polish CSS/UI elements focusing on vibrant dynamic dashboard aesthetic matching the `atruss` vision
- [x] T020 [P] [US3] Verify deeply-linked URL paths connecting summary tiles directly into the detailed `.md` reports

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T021 Implement fallback UI in `AtlasSummary.astro` for edge case where JSON/YAML parsing fails or data is missing
- [x] T022 Document Astro specific usage steps (Data Sync -> Build) in the primary GitHub repository `README.md`
- [x] T023 Confirm Astro application builds under 30 seconds for test fixtures

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### Parallel Example: User Story 3

```bash
# Launch component and index overridden concurrently:
Task: "Create web/src/components/AtlasSummary.astro to digest data"
Task: "Override default landing page with custom summary structure in web/src/content/docs/index.mdx"
```
