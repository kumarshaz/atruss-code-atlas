# Implementation Plan: Full Astro UI Extension (Phases A-D)

**Branch**: `006-ui-data-integration` | **Date**: 2026-03-29 | **Spec**: [spec.md](./spec.md)

## Summary

Transform the scaffolded Astro Starlight dashboard into a fully data-driven organizational observatory. A Python script auto-generates per-repository Markdown stub files from the CLI's `repositories.json` discovery output, driving the Starlight sidebar automatically. Successive Phase B–D expansions add CI/CD pipeline DAG visualization, Arc42 code architecture reports, and a multi-org maturity leaderboard — all rendered at build-time with zero client-side JSON fetching.

---

## Technical Context

**Language/Version**: Python 3.11+ (stub generator), Node.js v22 via `fnm` (Astro build)  
**Primary Dependencies**: Astro v6, `@astrojs/starlight` v0.38+, `astro-mermaid` v2 (already installed)  
**Storage**: Flat JSON/YAML/Markdown files under `exports/latest/` (no database)  
**Testing**: `pytest` for Python stub generator; Astro build success as integration gate  
**Target Platform**: Static site deployed from WSL; `npm run dev` local preview  
**Project Type**: Static site generator (Docs-as-Code) + Python CLI extension  
**Performance Goals**: Python stub generator processes 100 repos in < 5 seconds; Astro build < 60 seconds  
**Constraints**: Zero client-side data fetching; all computation at build time; WSL-native execution only  
**Scale/Scope**: Supporting up to 500 repos across 10 orgs per export; 4 UI component phases

---

## Constitution Check

*GATE: Must pass before Phase 0 research.*

| Principle | Status | Notes |
|---|---|---|
| **I. Policy-as-Code** | ✅ | Frontmatter schema extension in `content.config.ts` acts as the contract |
| **II. Single Source of Truth** | ✅ | All UI reads exclusively from `exports/latest/` JSON/Markdown files |
| **III. Security & Privacy** | ✅ | No API calls at runtime; tokens never persisted in UI layer |
| **IV. Performance & Scalability** | ✅ | Build-time rendering; no per-request compute |
| **V. Auditability** | ✅ | Discovery JSON provides timestamped scan provenance |
| **VI. Pipeline Visualization First-Class** | ✅ | Phase B explicitly implements `PipelineView.astro` with Mermaid DAG |
| **VII. SDD/TDD** | ✅ | Stub generator gets pytest unit tests; Astro build is the integration test |
| **VIII. WSL Dev Environment** | ✅ | All npm/node commands run via `fnm` in WSL; Python via `venv` |

---

## Gap Analysis: Handcrafted Plan vs Spec

Cross-referencing `docs/astro-ui-extension-plan-after-005.md` against `spec.md`:

| Item | In Handcrafted Plan | In Spec FR | Plan Coverage |
|---|---|---|---|
| OrgHealthStrip, LanguageChart, RepoGrid, RepoCard | ✅ Section 5 | ✅ FR-004 | Phase A |
| **RiskFlags component** | ✅ Section 5 | ⚠️ Implicit only in FR-004 | Phase A (explicit below) |
| **DiscoveryTable component** | ✅ Section 5 | ❌ Missing from spec FRs | Phase A (explicit below) |
| `generate-report-stubs.py` | ✅ Section 6 | ✅ FR-001 | Phase A |
| Extend `docsSchema` (Zod) | ✅ Section 10 | ✅ FR-002 | Phase A |
| `copy-data` extended to call stub gen | ✅ Section 7 | ✅ FR-001 flow | Phase A |
| Favicon update | ✅ Section 5 | ✅ FR-003 | Phase A |
| PipelineView + anti-patterns | ✅ Section 5 | ✅ FR-005 | Phase B |
| Pipeline JSON schema definition | ✅ Section 7B | ⚠️ Assumed, not explicit | Phase B prerequisite |
| ArchitectureView + Arc42 | ✅ Section 5 | ✅ FR-006 | Phase C |
| /orgs/ leaderboard | ✅ Section 3 Layer 3 | ✅ FR-007 | Phase D |
| Maturity score formula | ✅ Section 3 Layer 3 | ✅ US4 references it | Phase D |
| Org-grouped sidebar via autogenerate | ✅ Section 4 | ✅ US1 + FR-001 | Phase A |

**Gaps resolved in this plan**: `RiskFlags`, `DiscoveryTable`, and the Pipeline JSON schema contract are made explicit.

---

## Project Structure

### Documentation (this feature)

```text
specs/006-ui-data-integration/
├── plan.md              ← This file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── contracts/           ← Phase 1 output (pipeline JSON schema)
└── tasks.md             ← Phase 2 output (/speckit.tasks)
```

### Source Code Layout

```text
# Python CLI extension
scripts/
└── generate-report-stubs.py     ← NEW: reads repositories.json → emits per-repo .md stubs

tests/unit/
└── test_generate_stubs.py       ← NEW: pytest unit tests for stub generator

# Astro web application
web/
├── astro.config.mjs             ← MODIFY: add favicon config
├── package.json                 ← MODIFY: extend copy-data to invoke stub generator
├── public/
│   └── favicon.svg              ← MODIFY or NEW: replace with atruss favicon
└── src/
    ├── content.config.ts        ← MODIFY: extend docsSchema with custom frontmatter keys
    ├── assets/
    │   └── atruss-favicon.png   ← EXISTS: already present, source asset
    ├── components/
    │   ├── AtlasSummary.astro   ← MODIFY: decompose into sub-components
    │   ├── OrgHealthStrip.astro ← NEW: scan metadata KPIs
    │   ├── LanguageChart.astro  ← NEW: build-time SVG language distribution
    │   ├── RiskFlags.astro      ← NEW: repos with HasDockerfile+no pipeline
    │   ├── RepoGrid.astro       ← NEW: filterable grid container
    │   ├── RepoCard.astro       ← NEW: single repo card with language badge + link
    │   ├── DiscoveryTable.astro ← NEW: structured field table for repo detail Tab 1
    │   ├── PipelineView.astro   ← NEW: Mermaid DAG + anti-patterns Tab 2 (Phase B)
    │   └── ArchitectureView.astro ← NEW: Arc42 Markdown embed Tab 3 (Phase C)
    └── content/docs/
        ├── index.mdx            ← MODIFY: wire real components replacing placeholder
        └── reports/             ← AUTO-GENERATED by stub generator per build
            └── {org}/
                └── {repo}.md   ← AUTO-GENERATED stubs with frontmatter
```

---

## Phase 0: Research

### R-001 — Favicon Configuration in Starlight

**Decision**: Starlight supports custom favicons via the `favicon` config key in `astro.config.mjs`. It expects a path relative to `public/`. The `atruss-favicon.png` must be copied to `web/public/` and referenced in config.

**Implementation**:
```js
starlight({
  favicon: { href: '/favicon.png', type: 'image/png' },
})
```

**Alternative Considered**: Replacing `public/favicon.svg`. Rejected — PNG is already the branded asset at `src/assets/atruss-favicon.png`, so we place a copy in `public/`.

---

### R-002 — Astro `docsSchema` Extension for Custom Frontmatter

**Decision**: Use `docsSchema({ extend: z.object({...}) })` pattern. This safely merges custom fields into Starlight's strict Zod validation.

**Required keys**:
```typescript
extend: z.object({
  org: z.string().optional(),
  repo_name: z.string().optional(),
  language: z.string().optional(),
  framework: z.string().optional(),
  has_pipeline: z.boolean().optional(),
  has_docker: z.boolean().optional(),
  has_kubernetes: z.boolean().optional(),
  has_api: z.boolean().optional(),
  doc_priority: z.string().optional(),
  last_updated: z.string().optional(),
  github_url: z.string().url().optional(),
})
```

---

### R-003 — Stub Generator: Build-Time Python Invocation from npm

**Decision**: Extend `copy-data` script in `web/package.json` to invoke the stub generator via `python3` after the raw export files are copied. The stub generator reads `src/content/docs/reports/repos/repositories.json` (already copied by the first step) and writes per-repo MDX stubs.

**Invocation chain (updated `copy-data`)**:
```bash
mkdir -p src/content/docs/reports/ &&
cp -R ../exports/latest/* src/content/docs/reports/ 2>/dev/null &&
cd .. && python3 scripts/generate-report-stubs.py \
  --discovery exports/latest/repos/repositories.json \
  --output web/src/content/docs/reports/
```

---

### R-004 — Pipeline JSON Schema Contract (Phase B Prerequisite)

**Decision**: Define the schema now so Phase B implementation has a stable contract. The schema follows an adjacency-list model:

```json
{
  "repo_name": "pets-workshop",
  "org": "github-samples",
  "workflows": [
    {
      "name": "ci.yml",
      "trigger": ["push", "pull_request"],
      "jobs": [
        { "id": "build", "name": "Build", "needs": [] },
        { "id": "test", "name": "Test", "needs": ["build"] },
        { "id": "deploy", "name": "Deploy", "needs": ["test"] }
      ],
      "anti_patterns": [
        { "type": "NO_TEST_GATE", "severity": "HIGH", "message": "Deploy runs without a test gate" }
      ]
    }
  ]
}
```

Schema file: `specs/006-ui-data-integration/contracts/pipeline-output.schema.json`

---

### R-005 — Maturity Score Formula (Phase D)

**Decision**: Use a weighted formula per org:

```
score = (repos_with_pipeline / total_repos) × 60
      + (repos_without_antipatterns / repos_with_pipeline) × 40
```

Result is a 0–100 integer. Orgs with 0 pipeline repos receive score of 0. Rendered as a sorted leaderboard table at `/orgs/`.

---

## Phase 1: Design & Data Model

See [data-model.md](./data-model.md) for full entity definitions.

### Key Entity Summary

| Entity | Source File | Key Fields |
|---|---|---|
| **DiscoveryRepository** | `repos/repositories.json` | `Organization`, `RepositoryName`, `PrimaryLanguage`, `HasPipeline`, `HasDockerfile`, `DocumentationPriority` |
| **RepoStub** | Generated `.md` in `reports/{org}/` | Frontmatter projection of DiscoveryRepository |
| **PipelineWorkflow** | `pipelines/{repo}-pipeline.json` | `workflows[]`, `jobs[]`, `anti_patterns[]` |
| **ArchitectureReport** | `reports/{repo}-report.md` | Arc42 Markdown with embedded Mermaid |
| **OrgMaturityScore** | Computed from DiscoveryRepository[] | `org`, `total`, `with_pipeline`, `score` |

---

## Implementation Phases (Task Summary)

### Phase A — Real Data Integration

| Task | Component | Type |
|---|---|---|
| A1 | `generate-report-stubs.py` | Python NEW |
| A2 | `test_generate_stubs.py` | Python test NEW |
| A3 | Extend `content.config.ts` docsSchema | Astro MODIFY |
| A4 | Add favicon to `public/` + config | Astro MODIFY |
| A5 | `OrgHealthStrip.astro` | Astro NEW |
| A6 | `LanguageChart.astro` (SVG, build-time) | Astro NEW |
| A7 | `RiskFlags.astro` | Astro NEW |
| A8 | `RepoGrid.astro` + `RepoCard.astro` | Astro NEW |
| A9 | `DiscoveryTable.astro` | Astro NEW |
| A10 | Refactor `AtlasSummary.astro` | Astro MODIFY |
| A11 | Update `index.mdx` to wire real components | Astro MODIFY |
| A12 | Update `copy-data` in `package.json` | npm MODIFY |

### Phase B — Pipeline Topology Tab

| Task | Component | Type |
|---|---|---|
| B1 | Define `pipeline-output.schema.json` | Contract NEW |
| B2 | `PipelineView.astro` with Mermaid DAG | Astro NEW |
| B3 | Anti-pattern badge renderer | Astro NEW |
| B4 | Empty-state component for missing pipeline data | Astro NEW |
| B5 | Wire PipelineView into repo stub MDX template | Astro MODIFY |

### Phase C — Architecture Report Tab

| Task | Component | Type |
|---|---|---|
| C1 | `ArchitectureView.astro` embedding Arc42 Markdown | Astro NEW |
| C2 | Empty-state component for missing architecture data | Astro NEW |
| C3 | Wire ArchitectureView into repo stub MDX template | Astro MODIFY |

### Phase D — Org Maturity Leaderboard (Stretch)

| Task | Component | Type |
|---|---|---|
| D1 | `/orgs/index.mdx` comparison page | Astro NEW |
| D2 | `OrgComparisonTable.astro` sorted leaderboard | Astro NEW |
| D3 | Maturity score computation at build time | Astro logic NEW |

---

## Verification Plan

| Criterion | How to Verify |
|---|---|
| SC-001: Build succeeds with real data | `npm run build` exits 0; no Astro/Zod errors |
| SC-002: Stub generator runs fast | `time python3 scripts/generate-report-stubs.py ...` < 5s for 100 repos |
| SC-003: Empty states resilient | Run only `atruss discover`; verify Phase B/C tabs render empty-state prompt |
| SC-004: Favicon resolves | Load `http://localhost:4321` and verify browser tab shows Atruss favicon |
| Coverage: All handcrafted plan items | All 13 items in gap table above have ✅ Phase assignment |
