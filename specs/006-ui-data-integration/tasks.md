# Tasks: Full Astro UI Extension (Feature 006)

**Branch**: `006-ui-data-integration`  
**Input**: `specs/006-ui-data-integration/` (spec.md, plan.md, data-model.md, contracts/)  
**Total Tasks**: 39 | **Phases**: 7 (Setup → Foundation → US1 → US2 → US3 → US4 → Polish)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on each other)
- **[Story]**: User story this task belongs to
- Paths are relative to project root unless noted

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the project environment and directory structure before any implementation begins.

- [x] T001 Verify `astro-mermaid` (v2+) and `mermaid` (v11+) are listed in `web/package.json` dependencies — both are pre-installed; do **not** run `npm install` unless versions are missing
- [x] T002 [P] Create `scripts/` directory at project root for the Python CLI extension scripts
- [x] T003 [P] Create `specs/006-ui-data-integration/contracts/` directory and confirm `pipeline-output.schema.json` exists
- [x] T004 Run `mkdir -p web/public/` then copy `web/src/assets/atruss-favicon.png` to `web/public/favicon.png` for Starlight favicon serving

**Checkpoint**: Environment ready — all directories exist, favicon source in `public/`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before any user story work begins. These tasks wire up the data pipeline and schema contracts that all components depend on.

**⚠️ CRITICAL**: No component work in Phase 3+ can begin until this phase is complete.

- [x] T005 Extend `docsSchema` in `web/src/content.config.ts` to accept custom frontmatter keys (`org`, `repo_name`, `language`, `framework`, `has_pipeline`, `has_docker`, `has_kubernetes`, `has_api`, `doc_priority`, `last_updated`, `github_url`) using `docsSchema({ extend: z.object({...}) })`
- [x] T006 Update `web/astro.config.mjs` to configure the Starlight `favicon` key pointing to `/favicon.png`
- [x] T007 Write `scripts/generate-report-stubs.py` — reads `exports/latest/repos/repositories.json`, groups repos by `Organization`, and emits `/web/src/content/docs/reports/{org}/{repo_name}.md` stubs with full frontmatter mapping from `DiscoveryRepository` fields (as defined in `specs/006-ui-data-integration/data-model.md`)
- [x] T008 Write `tests/unit/test_generate_stubs.py` — pytest tests verifying the stub generator: (a) creates correct directory structure, (b) emits valid frontmatter, (c) handles missing/empty `repositories.json` gracefully
- [x] T009 Update `copy-data` script in `web/package.json` to invoke `../.venv/bin/python3 ../scripts/generate-report-stubs.py --discovery ../exports/latest/repos/repositories.json --output src/content/docs/reports/` after the raw file copy step — use `.venv/bin/python3` (not bare `python3`) to comply with **Constitution §VIII** WSL venv requirement
- [x] T022 Create `web/src/components/EmptyStatePrompt.astro` — **shared component used by both US2 and US3**; accepts `phase` (string e.g. `"Pipeline"`) and `command` (string e.g. `"atruss analyze-pipeline"`) props; renders a neutral styled card with an instructional CLI prompt ⚠️ Placed here in Foundation (not Phase 4) because it blocks both US2 and US3 independently
- [x] T010 Verify `npm run copy-data` in `web/` runs without errors end-to-end (copies files → invokes stub generator → generates stubs)

**Checkpoint**: Foundation ready — `npm run dev` launches, stubs appear in sidebar, favicon resolves.

---

## Phase 3: User Story 1 — Central Repository Discovery & Routing (Priority: P1) 🎯 MVP

**Goal**: Replace the static placeholder in `index.mdx` with real data-driven components that read `repositories.json` and render an org health strip, language chart, risk flag panel, and filterable repo grid. Each repo card deep-links to its generated stub page.

**Independent Test**: Run `npm run dev`, navigate to `http://localhost:4321`. Verify: (a) `OrgHealthStrip` shows correct repo count from `repositories.json`, (b) `LanguageChart` renders accurate language breakdown, (c) `RepoGrid` shows all repos with correct language badges, (d) clicking a card navigates to the correct `/reports/{org}/{repo}/` page, (e) that detail page shows a `DiscoveryTable` with all repository properties.

- [x] T011 [P] [US1] Create `web/src/components/OrgHealthStrip.astro` — accepts `repos` array prop, renders total repo count, scan date (from `LastUpdate`), repos-with-pipeline count, and repos-with-docker count as KPI badges
- [x] T012 [P] [US1] Create `web/src/components/LanguageChart.astro` — accepts `repos` array prop, computes language frequency map from `TechnologyStack`, renders as a build-time SVG bar chart (no client-side JS)
- [x] T013 [P] [US1] Create `web/src/components/RiskFlags.astro` — accepts `repos` array prop, filters for `HasDockerfile: true AND HasPipeline: false`, renders a highlighted warning list of at-risk repository names with links
- [x] T014 [P] [US1] Create `web/src/components/RepoCard.astro` — accepts a single repo object as prop, renders repo name, org, language badge (color-coded by language), `doc_priority` badge, and a `href` deep-link to `/reports/{org}/{repo_name}/`
- [x] T015 [US1] Create `web/src/components/RepoGrid.astro` — accepts `repos` array, renders a responsive grid of `RepoCard` components sorted by `DocumentationPriority` (P1 first)
- [x] T016 [US1] Create `web/src/components/DiscoveryTable.astro` — accepts a single repo's frontmatter props, renders a structured two-column table of all discovery fields (language, framework, has_api, has_pipeline, has_docker, has_kubernetes, doc_priority, last_updated, github_url)
- [x] T017 [US1] Refactor `web/src/components/AtlasSummary.astro` — replace its internal static markup by importing and composing `OrgHealthStrip`, `LanguageChart`, `RiskFlags`, and `RepoGrid`; load `repositories.json` via `Astro.glob()` or direct import at the top
- [x] T018 [US1] Update `web/src/content/docs/index.mdx` — replace placeholder content with `<AtlasSummary />` component import (data flows from this single entry point)
- [x] T019 [US1] Verify `web/astro.config.mjs` sidebar uses `autogenerate: { directory: 'reports' }` and confirm org-grouped sub-dropdowns appear in the browser at `http://localhost:4321` after T010 stubs are generated — no code change needed if already configured

**Checkpoint**: US1 fully functional. `npm run dev` shows live org data, repo cards navigate correctly to stub detail pages with working `DiscoveryTable`.

---

## Phase 4: User Story 2 — CI/CD Pipeline Observability (Priority: P1)

**Goal**: Add a "Pipeline" tab to each repository detail page that reads pipeline JSON output and renders a Mermaid DAG of CI jobs plus anti-pattern severity badges. Shows a graceful empty state when pipeline analysis has not been run.

**Prerequisites**: T022 (`EmptyStatePrompt.astro`) completed in Phase 2 Foundation.

**Independent Test**: Run `npm run dev`. Navigate to a repo detail page for a repo that has pipeline JSON in `exports/latest/pipelines/`. Verify: (a) Pipeline tab shows a Mermaid DAG with correct job nodes and edges, (b) anti-patterns render as color-coded badges (HIGH=red, MEDIUM=yellow, LOW=blue), (c) navigate to a repo without pipeline JSON — verify the empty state prompt renders without JS errors.

- [x] T020 [P] [US2] Create `web/src/components/PipelineView.astro` — accepts `repo_name` and `org` props; attempts to load `exports/latest/pipelines/{org}-{repo_name}-pipeline.json` via `Astro.glob()`; if found, transforms the `jobs[]` adjacency list into a Mermaid `graph TD` string and emits a mermaid block; if not found, renders `<EmptyStatePrompt phase="Pipeline" command="atruss analyze-pipeline" />` (T022, already created in Foundation)
- [x] T021 [P] [US2] Create `web/src/components/AntiPatternBadge.astro` — accepts `type`, `severity`, `message` props; renders a styled badge with severity-appropriate colour (HIGH=destructive red, MEDIUM=caution amber, LOW=info blue) and tooltip message
- [x] T038 [US2] Integrate `AntiPatternBadge` into `PipelineView.astro` — below the Mermaid DAG block, iterate over `anti_patterns[]` from the pipeline JSON and render one `<AntiPatternBadge />` per finding (depends on T020 + T021)
- [x] T039 [US2] Verify `atruss analyze-pipeline` emits pipeline JSON named `{org}-{repo_name}-pipeline.json` under `exports/latest/pipelines/` — confirm naming convention matches what T020 `PipelineView.astro` expects; if naming differs, update T020's glob pattern to match actual CLI output
- [x] T023 [US2] Update the stub template in `scripts/generate-report-stubs.py` to emit the `<PipelineView />` MDX component import and usage in the generated `{repo}.md` files (Phase B section)
- [x] T024 [US2] Review `web/src/content.config.ts` Zod schema extension and confirm all pipeline-related frontmatter keys are covered; add new optional keys (e.g., `workflow_count`, `has_antipatterns`) to the `docsSchema` extension if additional data surfaces during T020 implementation

**Checkpoint**: US2 fully functional. Pipeline DAG renders for repos with output; empty state renders for repos without. Empty state does not break the Astro build.

---

## Phase 5: User Story 3 — Architectural Arc42 Boundary Visualization (Priority: P2)

**Goal**: Add an "Architecture" tab to each repository detail page that embeds the Arc42 Markdown report (with Mermaid component boundary diagrams) generated by `atruss analyze-code`. Shows a graceful empty state when code analysis has not been run.

**Independent Test**: Run `npm run dev`. Navigate to a repo detail page for a repo that has `exports/latest/reports/{repo}-report.md`. Verify: (a) Architecture tab renders the full embedded Arc42 Markdown content, (b) Mermaid diagrams within the report render as SVGs (via `astro-mermaid`), (c) navigate to a repo without a report — verify the empty state prompt renders without errors.

- [x] T025 [P] [US3] Create `web/src/components/ArchitectureView.astro` — accepts `repo_name` and `org` props; attempts to load `exports/latest/reports/{repo_name}-report.md` via `Astro.glob()`; if found, uses Astro's `<Content />` slot to render the Markdown; if not found, renders `<EmptyStatePrompt phase="Architecture" command="atruss analyze-code" />`
- [x] T026 [US3] Update the stub template in `scripts/generate-report-stubs.py` to emit the `<ArchitectureView />` MDX component import and usage in the generated `{repo}.md` files (Phase C section)

**Checkpoint**: US3 fully functional. Arc42 content renders for analyzed repos; empty state renders gracefully for unanalyzed repos.

---

## Phase 6: User Story 4 — Multi-Organization Comparison Leaderboard (Priority: P3)

**Goal**: Implement a dedicated `/orgs/` page that aggregates all org data from `repositories.json`, computes a CI/CD maturity score per org using the formula from `plan.md R-005`, and renders a sorted leaderboard table.

**Independent Test**: Run `npm run dev`. Navigate to `http://localhost:4321/orgs/`. Verify: (a) Each org in the discovery JSON appears as a row in the table, (b) maturity score is computed and displayed as a 0–100 integer, (c) table is sorted descending by score, (d) page renders with zero client-side JS data fetching.

- [x] T027 [P] [US4] Create `web/src/components/OrgComparisonTable.astro` — accepts an array of `OrgMaturityScore` objects; renders a sorted HTML table with columns: Org Name, Total Repos, Repos With Pipeline, Pipeline Coverage %, Maturity Score; rows sorted by score descending
- [x] T028 [US4] Create `web/src/content/docs/orgs/index.mdx` — imports `OrgHealthStrip` and `OrgComparisonTable`; loads `repositories.json` at build time; computes `OrgMaturityScore[]` using the formula: `score = pipeline_coverage_pct × 60 + (repos_without_antipatterns / repos_with_pipeline) × 40`; apply guards: if `repos_with_pipeline = 0` then `score = 0`; if pipeline JSON is absent, omit second term and use `score = pipeline_coverage_pct × 60` only — document degraded-mode behaviour in a code comment
- [x] T029 [US4] Update `web/astro.config.mjs` sidebar to add an `Org Comparison` entry linking to `/orgs/`

**Checkpoint**: US4 functional. `/orgs/` page renders with correct per-org scores. Adding a new org's discovery JSON automatically reflects in the leaderboard on next build.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Consistency, accessibility, and documentation improvements across all phases.

- [x] T030 [P] Run `pytest tests/unit/test_generate_stubs.py` — confirm all assertions pass including the timing assertion (100 repos generated in < 5 seconds) verifying SC-002
- [ ] T031 [P] Run standalone `npm run build` in `web/` (without the full pipeline) and confirm Astro build exits 0 with no Zod schema errors, no Starlight slug errors, and no broken component imports
- [x] T032 [P] Verify `http://localhost:4321` browser tab shows the Atruss favicon (not the default Starlight rocket)
- [x] T033 [P] Add language colour mapping constant to `web/src/components/RepoCard.astro` covering: Python (blue), TypeScript (blue-violet), JavaScript (yellow), Go (cyan), Java (orange), unknown (grey)
- [x] T034 [P] Add `aria-label` attributes to all SVG chart elements in `LanguageChart.astro` for accessibility
- [x] T035 Update `README.md` to document the new `generate-report-stubs.py` workflow and the `npm run dev` / `npm run build` pipeline
- [x] T036 Update `docs/astro-ui-extension-plan-after-005.md` Phase A checkbox items to mark them complete
- [ ] T037 [P] Run full end-to-end pipeline smoke test: `atruss discover --org {org}` → `../.venv/bin/python3 scripts/generate-report-stubs.py ...` → `npm run build` — all three stages must complete without errors and produce a deployable static site in `web/dist/`

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Can Parallelize? |
|---|---|---|
| Phase 1: Setup | Nothing | ✅ All T001–T004 parallel |
| Phase 2: Foundation | Phase 1 complete | T005–T009 sequential; T022 after T009; T010 verifies all |
| Phase 3: US1 | Phase 2 complete | T011–T014 fully parallel; T015–T019 sequential |
| Phase 4: US2 | Phase 2 complete (incl. T022 EmptyStatePrompt) | T020–T021 parallel; T038, T039, T023, T024 after |
| Phase 5: US3 | Phase 2 complete (T022 already in Foundation) | T025 parallel with T026 |
| Phase 6: US4 | Phase 3 complete (RepoCard, data loading) | T027 parallel with T028 |
| Phase 7: Polish | All desired stories complete | Most tasks parallel |

### User Story Dependencies

- **US1 (P1)**: Only depends on Phase 2 foundation — can start immediately after T010
- **US2 (P1)**: Depends on `EmptyStatePrompt` from T022 — T022 should be pulled forward
- **US3 (P2)**: Depends on `EmptyStatePrompt` from T022 — same as US2
- **US4 (P3)**: Depends on US1 completion (`RepoGrid` loading pattern reused)

### Critical Path (Single Developer)

```
T001→T004 → T005→T010 → T011→T019 → T020→T024 → T025→T026 → T027→T029 → T030→T037
(Setup)      (Foundation) (US1/MVP)   (US2)        (US3)        (US4)        (Polish)
```

---

## Parallel Execution Examples

### Phase 3: US1 — Launch together after T010

```bash
# These 4 tasks share no files — run in parallel:
"Create OrgHealthStrip.astro"   # T011
"Create LanguageChart.astro"    # T012
"Create RiskFlags.astro"        # T013
"Create RepoCard.astro"         # T014

# Then sequentially:
T015 (RepoGrid, uses RepoCard) → T016 (DiscoveryTable) → T017 (AtlasSummary refactor) → T018 (index.mdx)
```

### Phase 4: US2 — Launch together after T010

```bash
# T020 and T021 and T022 share no files:
"Create PipelineView.astro"     # T020
"Create AntiPatternBadge.astro" # T021
"Create EmptyStatePrompt.astro" # T022
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundation (T005–T010) — **blocks everything**
3. Complete Phase 3: US1 (T011–T019)
4. **STOP and VALIDATE**: `npm run dev` renders live org data with real `repositories.json`
5. Demonstrate/commit MVP before moving to US2

### Incremental Delivery

1. Setup + Foundation → Stubs auto-generate, sidebar populates, favicon works
2. US1 → Full landing page with org health, language chart, risk signals, repo grid
3. US2 → Repo detail pages gain Pipeline DAG tab
4. US3 → Repo detail pages gain Architecture tab
5. US4 → `/orgs/` maturity leaderboard active

---

## Notes

- `[P]` tasks = different files, no blocking dependencies on each other within the phase
- All Astro components must remain SSG-safe: no client-side `fetch()`, no reactive stores
- The `EmptyStatePrompt` component (T022) is a shared dependency for US2 AND US3 — consider pulling it forward to the Foundation phase if implementing US2 and US3 in parallel
- Commit after each checkpoint to preserve a working state
- `npm run build` is the definitive integration test — a successful build = no schema violations, no slug errors, no broken imports

