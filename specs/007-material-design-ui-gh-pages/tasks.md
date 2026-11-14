# Tasks: Material Design 3 UI Overhaul & GitHub Pages Deployment

**Input**: Design documents from `/specs/007-material-design-ui-gh-pages/`  
**Prerequisites**: `plan.md`, `spec.md`, `006-core-unification-and-eval`

---

## Phase 1: Material Design 3 Token System & Astro Configuration (US1, US4)

**Goal**: Establish the M3 token stylesheet, typography/icon fonts, and GitHub Pages `site`/`base` configuration in `web/astro.config.mjs`.

- [x] T001 [P] [US1] Create `web/src/styles/material-theme.css` defining M3 Dark & Light tonal palettes (`--md-sys-color-*`), elevation rules, shape radii (`12px`–`24px`), M3 card/chip/tab classes, and Starlight `--sl-color-*` variable mappings (`FR-001`).
- [x] T002 [US1] Update `web/astro.config.mjs` to load `./src/styles/material-theme.css`, inject Google Fonts (`Roboto Flex`, `JetBrains Mono`, `Material Symbols Outlined`), and configure `site` and `base` from `ASTRO_SITE` / `ASTRO_BASE` environment variables (`FR-001`, `FR-005`).

---

## Phase 2: M3 Landing Command Center & Interactive Filter Chips (US2)

**Goal**: Upgrade all Layer 1 dashboard components to M3 surfaces and add client-side M3 Filter Chips + search to `RepoGrid.astro`.

- [x] T003 [P] [US2] Refactor `web/src/components/AtlasSummary.astro` and `web/src/content/docs/index.mdx` to use M3 Hero layout, tonal surface containers, and `import.meta.env.BASE_URL`-safe action links (`FR-002`, `FR-005`).
- [x] T004 [P] [US2] Refactor `web/src/components/OrgHealthStrip.astro` into M3 Tonal KPI cards with Material Symbols (`folder_managed`, `account_tree`, `deployed_code`, `schedule`) (`FR-002`).
- [x] T005 [P] [US2] Refactor `web/src/components/LanguageChart.astro` and `web/src/components/RiskFlags.astro` into M3 Elevated/Alert container cards with M3 tonal colors (`FR-002`).
- [x] T006 [US2] Upgrade `web/src/components/RepoGrid.astro` and `web/src/components/RepoCard.astro` with an interactive **M3 Filter Chip bar** (`All`, `Python`, `.NET`, `JavaScript/TypeScript`, `Java`, `Has Pipeline`, `Has Docker`, `High Risk`), live text search filter, M3 state layers, and `import.meta.env.BASE_URL`-safe card links (`FR-002`, `FR-003`, `FR-005`).

---

## Phase 3: M3 Tabbed Repository Detail View & Pan/Zoom DAGs (US3)

**Goal**: Upgrade Layer 2 repository detail pages to use an M3 Header Card and M3 Primary Tabs (`Discovery Overview`, `Pipeline Topology DAG`, `Arc42 Code Architecture`).

- [x] T007 [P] [US3] Refactor `web/src/components/DiscoveryTable.astro`, `AntiPatternBadge.astro`, and `EmptyStatePrompt.astro` to use M3 Data Tables, semantic M3 severity chips, and copyable M3 command prompts (`FR-004`).
- [x] T008 [P] [US3] Upgrade `web/src/components/PipelineView.astro` and `web/src/components/ArchitectureView.astro` with M3 surface containers, Mermaid theme synchronization, and interactive zoom/reset controls (`FR-004`).
- [x] T009 [US3] Update `scripts/generate-report-stubs.py` (and corresponding unit tests in `tests/unit/test_generate_stubs.py`) to generate an M3 Tabbed interface wrapping `DiscoveryTable`, `PipelineView`, and `ArchitectureView` on each `/reports/{org}/{repo}/` page (`FR-004`).
- [x] T010 [P] [US3] Refactor `web/src/components/OrgComparisonTable.astro` and `web/src/content/docs/orgs/index.mdx` to use M3 Data Table and tonal maturity score bars (`FR-002`).

---

## Phase 4: GitHub Pages CI/CD Workflow & Build Verification (US4)

**Goal**: Automate static site deployment to GitHub Pages and verify subpath build integrity.

- [x] T011 [P] [US4] Create `.github/workflows/deploy-pages.yml` configuring Node v22, Python 3.12, `npm run copy-data`, `npm run build` (with `ASTRO_BASE` and `ASTRO_SITE`), `actions/upload-pages-artifact@v3`, and `actions/deploy-pages@v4` (`FR-006`).
- [x] T012 [US4] Execute `npm run build` inside `web/` (both default `/` and `ASTRO_BASE=/atruss-code-atlas`) and verify `< 30s` build time, 0 schema errors, and 100% valid internal links (`SC-001`, `SC-003`).
