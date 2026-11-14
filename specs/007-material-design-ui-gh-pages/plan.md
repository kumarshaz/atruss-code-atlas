# Implementation Plan: Material Design 3 UI Overhaul & GitHub Pages Deployment

**Branch**: `007-material-design-ui-gh-pages` | **Date**: 2026-11-12 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/007-material-design-ui-gh-pages/spec.md`

---

## 1. Summary

Transform the Astro Starlight frontend (`web/`) into a Google **Material Design 3 (Material You)** engineering observatory and configure automated static deployment to **GitHub Pages**. This retains Starlight's fast static Docs-as-Code routing and search while replacing generic styles with M3 tonal surface hierarchy, Material Symbols icons, interactive M3 Filter Chips on the repository grid, M3 Tabs on each repository report page, and base-path-safe routing for GitHub Pages.

---

## 2. Technical Context

- **Framework**: Astro 6 + `@astrojs/starlight` + `astro-mermaid`
- **Node Environment**: Node.js v22 via `fnm` in WSL (`source ~/.bashrc && fnm use 22`)
- **Design System**: Material Design 3 (`--md-sys-color-*`, `--md-sys-shape-*`, `@material/web`, Google Fonts `Roboto Flex`, `JetBrains Mono`, `Material Symbols Outlined`)
- **Deployment Target**: GitHub Pages (`actions/deploy-pages@v4`)
- **Constraints**: Zero client-side JSON fetching (all data bound at build time from `exports/latest/`); sub-30s build time.

---

## 3. Constitution Check

- **II. Single Source of Truth**: **PASS**. Astro components read exclusively from `exports/latest/` copied at build time.
- **VI. Pipeline Visualization as a First-Class Feature**: **PASS**. Pipeline DAGs are featured in a dedicated M3 Tab with interactive zoom/pan and M3 severity chips.
- **VIII. Standardized WSL Development Environment**: **PASS**. Uses Node v22 via `fnm` inside WSL.

---

## 4. Project Structure & Target Modifications

```text
.github/
└── workflows/
    └── deploy-pages.yml                         # [NEW] GitHub Actions workflow for GitHub Pages deployment

scripts/
└── generate-report-stubs.py                     # [MODIFY] Wrap DiscoveryTable, PipelineView, and ArchitectureView in M3 Tabs layout

web/
├── astro.config.mjs                             # [MODIFY] Add site, base, customCss ('./src/styles/material-theme.css'), and Google Fonts head links
├── package.json                                 # [MODIFY] Add @material/web (or M3 styling/test scripts)
└── src/
    ├── styles/
    │   └── material-theme.css                   # [NEW] Full M3 Dark & Light tonal token system + Starlight variable bridge + M3 utility classes
    ├── components/
    │   ├── AtlasSummary.astro                   # [MODIFY] M3 Hero Banner + Surface Container layout
    │   ├── OrgHealthStrip.astro                 # [MODIFY] M3 Tonal KPI Cards with Material Symbols icons
    │   ├── LanguageChart.astro                  # [MODIFY] M3 Elevated Card + M3 tonal progress/donut bars
    │   ├── RiskFlags.astro                      # [MODIFY] M3 Error/Tertiary Container alert cards
    │   ├── RepoGrid.astro                       # [MODIFY] Add M3 Filter Chip bar (Ecosystem, Priority, Pipeline/Risk) + instant search input
    │   ├── RepoCard.astro                       # [MODIFY] M3 Outlined/Elevated interactive card + BASE_URL-safe href + M3 Assist/Suggestion badges
    │   ├── DiscoveryTable.astro                 # [MODIFY] M3 Data Table + 27-column structured attribute chips
    │   ├── PipelineView.astro                   # [MODIFY] M3 DAG canvas with zoom/pan controls + M3 AntiPattern chips
    │   ├── ArchitectureView.astro               # [MODIFY] M3 Arc42 surface container + component summary chips
    │   ├── AntiPatternBadge.astro               # [MODIFY] M3 semantic severity chips (CRITICAL/HIGH/MEDIUM/LOW)
    │   ├── EmptyStatePrompt.astro               # [MODIFY] M3 surface-variant empty state card with copyable CLI command
    │   └── OrgComparisonTable.astro             # [MODIFY] M3 Data Table + Maturity Score progress bar
    └── content/
        └── docs/
            ├── index.mdx                        # [MODIFY] Clean M3 splash layout + BASE_URL-safe hero action links
            └── orgs/
                └── index.mdx                    # [MODIFY] M3 Organization Benchmarks view
```

---

## 5. Material Design 3 Token Palette Specification

### Dark Scheme (Default Observatory Mode)
- `--md-sys-color-background`: `#0F141A`
- `--md-sys-color-surface`: `#0F141A`
- `--md-sys-color-surface-container-lowest`: `#0A0E14`
- `--md-sys-color-surface-container-low`: `#171C22`
- `--md-sys-color-surface-container`: `#1B2026`
- `--md-sys-color-surface-container-high`: `#252A31`
- `--md-sys-color-surface-container-highest`: `#30353C`
- `--md-sys-color-primary`: `#A3C9FF`
- `--md-sys-color-on-primary`: `#00315C`
- `--md-sys-color-primary-container`: `#004882`
- `--md-sys-color-on-primary-container`: `#D3E4FF`
- `--md-sys-color-secondary`: `#BBC7DB`
- `--md-sys-color-tertiary`: `#FFB3AA`
- `--md-sys-color-error`: `#FFB4AB`
- `--md-sys-color-error-container`: `#93000A`
- `--md-sys-color-outline`: `#8D9199`
- `--md-sys-color-outline-variant`: `#43474E`
- `--md-sys-shape-corner-medium`: `12px`
- `--md-sys-shape-corner-large`: `16px`
- `--md-sys-shape-corner-extra-large`: `24px`
