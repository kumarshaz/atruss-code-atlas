# Atruss Code Atlas — Material Design 3 Web Portal (`web/`)

Static **Material Design 3 (Astro 6 + Starlight)** architectural intelligence portal for **Atruss Code Atlas**. Renders interactive organization leaderboards, repository discovery matrices, top-down (`flowchart TD`) CI/CD pipeline DAGs with `AP-001`–`AP-007` anti-pattern badges, and expandable Arc42 structural code architecture explorers directly from `../exports/latest/`.

---

## Directory Structure

```text
web/
├── public/                     # Static favicons and assets
├── src/
│   ├── assets/                 # Portal brand icons (atruss-favicon.png)
│   ├── components/             # Material Design 3 Astro components (AtlasSummary, RepoGrid, PipelineView, ArchitectureView, etc.)
│   ├── content/docs/           # Starlight MDX entrypoints (index.mdx, orgs/index.mdx, generated reports/<org>/<repo>.mdx)
│   ├── content.config.ts       # Astro 6 Content Layer collection & frontmatter schema
│   ├── lib/                    # Client-side Mermaid lazy hydration & top-level architecture tree builder
│   ├── styles/                 # Material Design 3 Dark/Light adaptive theme tokens (material-theme.css)
│   └── tests/                  # Node.js schema & UI contract regression tests
├── astro.config.mjs            # Astro + Starlight + astro-mermaid configuration (reads ASTRO_SITE & ASTRO_BASE)
├── package.json                # Scripts & dependencies
└── tsconfig.json               # TypeScript configuration
```

---

## Commands

Run from `web/` (using Node.js v22+):

| Command | Description |
| :--- | :--- |
| `npm ci` | Install locked dependencies |
| `npm run copy-data` | Sync `../exports/latest/` into `src/data/latest/` and generate tabbed `.mdx` report stubs via `../scripts/generate-report-stubs.py` |
| `npm test` | Run M3 component, layout, and `exports/latest/` schema contract tests (`src/tests/AtlasSummary.test.ts` & `src/tests/schema.test.ts`) |
| `npm run dev` | Sync latest discovery/analysis data and launch local dev server (`http://localhost:4321`) |
| `npm run build` | Sync latest data, build static HTML/CSS/JS + Pagefind search index to `dist/` |
| `npm run preview` | Preview production static build locally |

### GitHub Pages Subpath Build

To build with a GitHub Pages base path (as executed in `.github/workflows/deploy-pages.yml`):

```bash
ASTRO_SITE="https://kumarshaz.github.io" ASTRO_BASE="/atruss-code-atlas" npm run build
```
