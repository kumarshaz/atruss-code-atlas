# Atruss Code Atlas — Material Design 3 Web Portal (`web/`)

Static **Material Design 3 (Astro 6 + Starlight + Mermaid v12 + `@mermaid-js/layout-elk`)** architectural intelligence portal for **Atruss Code Atlas**. Renders interactive organization leaderboards (from `orgs-summary.json` with 20-row pagination), repository discovery matrices (15 ecosystem/risk filter chips + 24-card pagination), cross-repo workflow/dependency topologies, 6-Dimension A–F Scorecard heatmaps, top-down (`flowchart TD`) CI/CD pipeline DAGs with `AP-001`–`AP-014` anti-pattern badges, client-side SVG/PNG export + Print/PDF formatting, and expandable Arc42 structural code architecture explorers directly from `../exports/latest/`.

---

## Directory Structure

```text
web/
├── public/                     # Static favicons (favicon.png, favicon.ico), social card (og-default.png), and copied llms.txt / llms-full.txt
├── src/
│   ├── assets/                 # Portal brand logo (atruss-logo.png)
│   ├── components/             # Material Design 3 Astro components (BaseHead, AtlasSummary, LeaderboardView, ScorecardHeatmap, CrossRepoTopology, RepoTabs, RepoGrid, PipelineView, ArchitectureView, etc.)
│   ├── content/docs/           # Starlight MDX entrypoints (index.mdx, orgs/index.mdx, generated reports/<org>/<repo>.mdx)
│   ├── content.config.ts       # Astro 6 Content Layer collection & frontmatter schema
│   ├── lib/                    # Client-side Mermaid v12 ELK hydration (mermaid-client.ts) & architecture tree builder (architecture-tree.ts)
│   ├── styles/                 # Material Design 3 Dark/Light adaptive theme tokens & @media print rules (material-theme.css)
│   └── tests/                  # Node.js schema & UI contract regression tests
├── astro.config.mjs            # Astro 6 + Starlight + astro-mermaid configuration (reads ASTRO_SITE & ASTRO_BASE)
├── package.json                # Scripts & dependencies (astro ^6.0.1, starlight ^0.38.2, mermaid ^12.3.0, @mermaid-js/layout-elk)
└── tsconfig.json               # TypeScript configuration
```

---

## Commands

Run from `web/` (using Node.js v22+):

| Command | Description |
| :--- | :--- |
| `npm ci` | Install locked dependencies |
| `npm run copy-data` | Pre-compute `../exports/latest/orgs-summary.json` via `../scripts/generate-org-summary.py`, sync `../exports/latest/` into `src/data/latest/`, copy `llms*.txt` into `public/`, and generate 4-tab `.mdx` report stubs via `../scripts/generate-report-stubs.py` |
| `npm test` | Run M3 component, layout, and `exports/latest/` schema contract tests (`src/tests/AtlasSummary.test.ts` & `src/tests/schema.test.ts`) |
| `npm run dev` | Sync latest discovery/analysis data and launch local dev server (`http://localhost:4321`) |
| `npm run build` | Sync latest data, build static HTML/CSS/JS + Pagefind search index to `dist/` |
| `npm run preview` | Preview production static build locally |

### Custom Domain & Environment Overrides

By default, `astro.config.mjs` (and `.github/workflows/deploy-pages.yml`) builds for `https://atruss.shashinkumar.com` at the root base `/`. To override `site` or build under a subpath (as also verified in `.github/workflows/tests.yml`):

```bash
ASTRO_SITE="https://kumarshaz.github.io" ASTRO_BASE="/atruss-code-atlas" npm run build
```
