# Feature Specification: Material Design 3 UI Overhaul & GitHub Pages Deployment

**Feature Branch**: `007-material-design-ui-gh-pages`  
**Created**: 2026-11-12  
**Status**: Approved (Aligned via `/grill-me`)  
**Input**: User requirement for a Google Material Design 3 (Material You) UI instead of a generic UI, hosted statically on GitHub Pages.

---

## 1. Context & Problem Statement

The current Astro Starlight web application (`web/`) uses default Starlight styling with ad-hoc inline CSS rules (`--sl-color-*` variables and hardcoded hex colors). In addition:
1. It lacks a cohesive **Material Design 3 (M3)** design system (tonal surface elevation containers, semantic status tokens, Material Symbols iconography, and interactive M3 chips/tabs/cards).
2. Internal links in `RepoCard.astro` (`/reports/${org}/${repo}`) and `index.mdx` do not prepend `import.meta.env.BASE_URL`, which causes `404` broken links when hosted on a project subpath on **GitHub Pages** (`https://<user>.github.io/atruss-code-atlas/`).
3. There is no automated `.github/workflows/deploy-pages.yml` pipeline to build the Astro site from `exports/latest/` and publish it to GitHub Pages.

---

## 2. Clarifications & Architectural Decisions (from `/grill-me`)

- **UI Architecture**: Retain `@astrojs/starlight` for its zero-JS Docs-as-Code sidebar, search (Pagefind), and MDX routing, while applying a comprehensive **Material Design 3 Theme Override (`web/src/styles/material-theme.css`)** and upgrading all dashboard and report views with M3 components (`@material/web` / M3 CSS specifications).
- **Static Build-Time Portability**: Keep 100% build-time data resolution from `exports/latest/`. Use lightweight client-side interactivity only for instant M3 filter chips (`<md-filter-chip>`), M3 tab switching (`<md-tabs>`), and Mermaid diagram pan/zoom.
- **GitHub Pages Data Strategy**: Commit curated `exports/latest/` artifacts to the repository so every push to `main` builds and deploys to GitHub Pages in `< 60 seconds`, while supporting on-demand/scheduled benchmark workflows to commit updated exports.

---

## 3. User Scenarios & Testing *(mandatory)*

### User Story 1 - Material Design 3 Tonal Theme & App Shell (Priority: P1)

As a user navigating Atruss Code Atlas, I want the entire interface to follow Google Material Design 3 specifications—including M3 Dark/Light tonal surface hierarchies (`--md-sys-color-*`), `Roboto Flex` & `Roboto Mono` typography, and `Material Symbols Outlined` icons—so the observatory feels like a first-class Google Material product.

**Independent Test**: Build the Astro site (`npm run build`) and verify that `material-theme.css` is loaded across all pages, mapping all Starlight `--sl-color-*` variables to `--md-sys-color-*` tonal tokens in both Dark and Light modes.

**Acceptance Scenarios**:
1. **Given** any page in the Astro app, **When** rendered in Dark or Light mode, **Then** background surfaces use M3 tonal elevation (`surface`, `surface-container-low`, `surface-container`, `surface-container-high`) with rounded M3 geometry (`12px`–`24px` radii) and state layers.
2. **Given** status indicators and badges, **When** rendered, **Then** they use semantic M3 container pairs (`primary-container` / `on-primary-container`, `error-container` / `on-error-container`, `tertiary-container` / `on-tertiary-container`).

---

### User Story 2 - Interactive M3 Atlas Command Center (`/` & `/orgs/`) (Priority: P1)

As an engineering leader viewing the root dashboard (`/`), I want M3 Elevated/Filled KPI cards, a build-time SVG ecosystem distribution chart, M3 Risk Alert banners, and an interactive Repository Grid with **M3 Filter Chips** (by Ecosystem, Priority Tier, and Pipeline/Docker status) and instant search.

**Independent Test**: Load the root `/` page, click M3 filter chips (e.g., `Python`, `.NET`, `Tier 1`, `Has Pipeline`, `Risk: Missing CI`), and verify the repository cards filter instantaneously and link cleanly to their detail views.

**Acceptance Scenarios**:
1. **Given** a multi-ecosystem dataset in `exports/latest/repos/repositories.json`, **When** the landing page loads, **Then** `OrgHealthStrip`, `LanguageChart`, `RiskFlags`, and `RepoGrid` render inside M3 `surface-container` cards with Material Symbols icons.
2. **Given** the M3 Filter Chip bar above `RepoGrid`, **When** a user toggles one or more ecosystem or risk chips, **Then** matching `RepoCard` items filter smoothly without page reloads.

---

### User Story 3 - Tabbed M3 Repository Detail View (`/reports/{org}/{repo}/`) (Priority: P1)

As a software architect or DevOps engineer inspecting a specific repository, I want a structured M3 detail view with **M3 Primary Tabs** switching cleanly between **Tab 1: Discovery & 27-Column Metadata**, **Tab 2: Pipeline Topology DAG & Anti-Patterns**, and **Tab 3: Arc42 Code Architecture**, with interactive zoom/pan on Mermaid diagrams.

**Independent Test**: Navigate from a `RepoCard` on `/` to `/reports/github-samples/pets-workshop/` and verify all three M3 tabs switch cleanly and render their respective Discovery table, Pipeline Mermaid DAG + Anti-Pattern chips, and Arc42 Markdown diagram.

**Acceptance Scenarios**:
1. **Given** a generated repository report page, **When** viewing the page, **Then** an M3 Header Card displays repository metadata (Org, Repo, SHA/Last Updated, Ecosystem chip, Priority chip, GitHub action button) above an M3 3-tab bar.
2. **Given** a complex Mermaid DAG in `PipelineView.astro` or `ArchitectureView.astro`, **When** rendered, **Then** the user can zoom/pan or expand the diagram in an M3 surface container.

---

### User Story 4 - Automated GitHub Pages Deployment Pipeline (Priority: P1)

As the project owner, I want a GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) and base-URL-safe routing so that the Material Design 3 UI is automatically built and hosted on GitHub Pages.

**Independent Test**: Build the Astro site with `ASTRO_BASE=/atruss-code-atlas npm run build` and verify that all generated internal links, assets, and report routes resolve with the `/atruss-code-atlas/` prefix and zero broken links.

**Acceptance Scenarios**:
1. **Given** `ASTRO_BASE=/atruss-code-atlas`, **When** `npm run build` executes in `web/`, **Then** all links in `RepoCard.astro`, `index.mdx`, `OrgComparisonTable.astro`, and sidebar navigation include the base path properly.
2. **Given** a push to `main` or manual workflow dispatch, **When** `.github/workflows/deploy-pages.yml` runs, **Then** it executes `npm run copy-data && npm run build` and deploys `web/dist` to GitHub Pages.

---

## 4. Functional Requirements

- **FR-001**: Create `web/src/styles/material-theme.css` implementing Google Material Design 3 color tokens (`--md-sys-color-*` for dark and light themes), elevation tokens (`--md-sys-elevation-*`), shape tokens (`--md-sys-shape-corner-*`), and typography scales (`Roboto Flex`, `Roboto Mono`, `Material Symbols Outlined`), wired into `web/astro.config.mjs`.
- **FR-002**: Install `@material/web` (or lightweight M3 web component/CSS primitives) in `web/package.json` and refactor `AtlasSummary.astro`, `OrgHealthStrip.astro`, `LanguageChart.astro`, `RiskFlags.astro`, `RepoGrid.astro`, and `RepoCard.astro` to follow Material Design 3 specifications.
- **FR-003**: Add interactive M3 Filter Chips (`All`, `Python`, `.NET`, `React/TS`, `Java`, `Has Pipeline`, `Docker`, `High Risk`) and a search bar to `RepoGrid.astro`.
- **FR-004**: Update `scripts/generate-report-stubs.py` and the Layer 2 components (`DiscoveryTable.astro`, `PipelineView.astro`, `ArchitectureView.astro`, `AntiPatternBadge.astro`, `EmptyStatePrompt.astro`) to render inside an M3 Tabbed Container (`Discovery Overview` | `CI/CD Pipeline DAG` | `Arc42 Code Architecture`).
- **FR-005**: Update `web/astro.config.mjs` to support configurable `site` and `base` via environment variables (`ASTRO_SITE`, `ASTRO_BASE`) and update all internal `href` attributes across `web/src/` to respect `import.meta.env.BASE_URL`.
- **FR-006**: Create `.github/workflows/deploy-pages.yml` using `actions/upload-pages-artifact@v3` and `actions/deploy-pages@v4` to publish the static site to GitHub Pages on push to `main` or `workflow_dispatch`.

---

## 5. Success Criteria

- **SC-001**: `cd web && npm run build` completes in `< 30 seconds` with zero TypeScript, Zod schema, or Astro build errors.
- **SC-002**: 100% of UI surfaces, cards, chips, tabs, and badges utilize Material Design 3 `--md-sys-color-*` and `--md-sys-shape-*` tokens rather than raw hardcoded colors.
- **SC-003**: Building with `ASTRO_BASE=/atruss-code-atlas` produces 0 broken internal links between `/`, `/orgs/`, and `/reports/{org}/{repo}/`.
- **SC-004**: `.github/workflows/deploy-pages.yml` validates cleanly and packages `web/dist` for GitHub Pages deployment.
