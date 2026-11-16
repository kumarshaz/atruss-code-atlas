# Feature Specification: Post-Release Parity, Polyglot Depth & Benchmark SLA Hardening

**Feature Branch / Spec ID**: `010-parity-and-hardening` *(authored on `docs/sync-docs-and-specs`)*  
**Created**: 2026-11-15  
**Status**: Draft — Next-Iteration Specification  
**Input**: Implementation audit against Consolidated Master PRD v2.1 ([`docs/atruss-code-atlas-prd.md`](../../docs/atruss-code-atlas-prd.md)) and Specs `007`–`009` ([`specs/009-unified-atlas-spec/spec.md`](../009-unified-atlas-spec/spec.md)), remediating genuine implementation gaps while **preserving and ratifying every area where current code already exceeds legacy specifications**.

---

## Clarifications & Architectural Decisions

- **Ratification Principle (Do Not Downgrade Superior Code)**: Several areas in `origin/main` surpass older Iteration `007`–`009` specification wording and MUST be **ratified as the canonical baseline rather than rolled back**:
  1. **10-Ecosystem Multi-File Coverage Instead of 4 Languages Only**: Code already classifies and analyzes **10 ecosystems** (`Python`, `.NET`, `JavaScript/TypeScript`, `Java`, `Go`, `Rust`, `Ruby`, `PHP`, `Elixir`, `Container / Helm / IaC`) via [`manifests/ecosystems.yaml`](../../manifests/ecosystems.yaml), [`src/analyzers/code/orchestrator.py`](../../src/analyzers/code/orchestrator.py) (`_run_generic_structural`), [`src/analyzers/dependencies/manifest_parser.py`](../../src/analyzers/dependencies/manifest_parser.py) (9 dependency ecosystems), and [`tests/fixtures/popular_100_corpus.json`](../../tests/fixtures/popular_100_corpus.json) (expanded to **372 repositories**). Spec `010` expands AST depth onto those ecosystems instead of reverting to 4 languages or 100 repos.
  2. **4-Tab M3 Repository Detail View Instead of 3 Tabs**: [`RepoTabs.astro`](../../web/src/components/RepoTabs.astro) implements **4 M3 Primary Tabs** (`Discovery Overview`, `CI/CD Pipeline DAG`, `Arc42 Code Architecture`, `6-D Scorecard & Security`) with `ScorecardHeatmap.astro`, SVG/PNG export, and Print/PDF support. Spec `010` retains all 4 tabs.
  3. **15 Filter Chips, Pagination & CSS M3 Tokens**: [`RepoGrid.astro`](../../web/src/components/RepoGrid.astro) implements **15 M3 filter chips** across all 10 ecosystems + `24`-card pagination, [`OrgComparisonTable.astro`](../../web/src/components/OrgComparisonTable.astro) implements `20`-row pagination backed by `exports/latest/orgs-summary.json` (`scripts/generate-org-summary.py`), and `web/src/styles/material-theme.css` uses pure `.m3-*` CSS classes and `--md-sys-*` tokens on **Astro 6 + Starlight + Mermaid v12 ELK (`@mermaid-js/layout-elk`)** rather than `<md-*>` DOM custom elements.
  4. **Canonical Paths & Benchmark Fault Isolation**: Retain nested stub routing `web/src/content/docs/reports/{org}/{repo}.mdx`, aggregate pipeline report `exports/latest/reports/pipeline_architecture.md`, and `atruss benchmark` controls (`--isolated`, `--checkpoint-dir`, `--resume`, `--replay`, `--timeout`).
- **Scope Boundary for Spec `010`**: Close the remaining genuine gaps identified in PRD Section 9:
  1. Populate `DependencyRecord.is_outdated` and `latest_version`, add opt-in/cached NIST NVD or normalized CVSS enrichment alongside `OSV.dev`, and support cached/opt-in live OSV checks in `atruss check` instead of hardcoding `vulnerabilities=[]`.
  2. Extend CST/structural complexity, clone, dead-code, and import-edge analysis (`tree-sitter` / equivalent parsers) to **Go, Rust, Ruby, PHP, and Elixir** while keeping `infra_devops` structural/IaC extraction and offline fallback intact.
  3. Reconcile `scripts/curate_corpus.py` with the 372-repo corpus, expand `ECOSYSTEM_SEARCH_LANG` in `atruss benchmark --random-sample`, and fix the 52 monorepo timeouts and classification mismatches (`320/372 = 86.02%` crash-free, `273/320 = 85.31%` accuracy) to meet `>= 98%` crash-free and `>= 90%` classification targets.
  4. Calibrate or optimize the 323+ page Astro static build SLA (currently `~55s–58s` with Pagefind indexing) and align developer environment sync + `.agent/rules/specify-rules.md` (`Astro 6+`).

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dependency Freshness, NVD/CVSS Enrichment & `atruss check` Vulnerability Parity (Priority: P1)

As a security engineer and tech lead, I want `atruss analyze-code` and `atruss check` to flag outdated packages (`is_outdated`, `latest_version`), enrich advisories consistently with normalized CVSS ratings (OSV.dev primary + optional NVD/cached metadata), and inspect cached or live vulnerability intelligence during PR gating instead of passing an empty vulnerability list, so that Dependency Health scores and CI PR gates reflect real supply-chain risk even offline.

**Why this priority**: Currently [`DependencyRecord.is_outdated`](../../src/models/artifacts.py#L56-L57) is always `False`, NVD enrichment referenced in Constitution Principle III is absent, and [`src/cli/commands/check.py`](../../src/cli/commands/check.py#L121) passes `vulnerabilities=[]`, leaving part of the Dependency Health and Security Scorecard blind in PR checks.

**Independent Test**: Run offline `httpx.MockTransport` and unit fixture tests against Python, JS/TS, Go, and Rust manifests checking populated `is_outdated` / `latest_version`, normalized CVSS metadata, and non-empty `vulnerabilities` surfaced in `atruss check --sarif`.

**Acceptance Scenarios**:

1. **Given** repository manifests across supported dependency ecosystems and an opt-in registry client or cached index, **When** dependency analysis executes, **Then** outdated dependencies populate `is_outdated=True` and `latest_version` deterministically while remaining `False`/`None` without network failure when offline/uncached.
2. **Given** cached OSV/NVD advisory fixtures or `--live-osv` / `--live-nvd` flags, **When** `atruss check --path <repo> --sarif out.sarif.json` runs, **Then** matching known vulnerabilities and CVSS severities flow into both the SARIF report and the 6-D Scorecard instead of hardcoded `vulnerabilities=[]`.

---

### User Story 2 - Polyglot CST/AST Depth Across Go, Rust, Ruby, PHP & Elixir (Priority: P1)

As a software architect analyzing diverse microservices beyond Python, .NET, Java, and TypeScript/JS, I want Go, Rust, Ruby, PHP, and Elixir repositories to produce real syntax-tree complexity (`avg_cyclomatic_complexity`, `max_cyclomatic_complexity`, `avg_cognitive_complexity`, `duplication_pct`, `dead_code_count`, and internal `import_edges`) while retaining specialized structural/IaC extraction for Container/Helm/IaC and safe fallback when optional grammar binaries are absent.

**Why this priority**: Today 10 ecosystems are discovered and cataloged via [`manifests/ecosystems.yaml`](../../manifests/ecosystems.yaml) and [`src/analyzers/code/orchestrator.py`](../../src/analyzers/code/orchestrator.py), yet Go (51 corpus repos), Rust (15), PHP (14), Ruby (8), and Elixir (6) only receive generic LOC counts (`_run_generic_structural`).

**Independent Test**: Run `orchestrate_full_analysis()` and `tests/unit/test_treesitter_engine.py` + `tests/unit/test_multi_ecosystem_support.py` against fixture repositories in Go, Rust, Ruby, PHP, Elixir, and Container/Helm/IaC and verify AST engine metrics (`ast_engine`, cognitive complexity, import edges) without regressing fallback handling or `.venv` `[dev]` installs.

**Acceptance Scenarios**:

1. **Given** Go, Rust, Ruby, PHP, and Elixir fixture repositories with nested control flow, duplicated blocks, and internal imports, **When** code analysis runs with `[dev]` grammars installed, **Then** each repo emits populated cyclomatic/cognitive complexity, clone duplication, dead-code, and import-edge telemetry.
2. **Given** an `infra_devops` repository containing Dockerfiles, Helm charts, and Terraform HCL, **When** code analysis runs, **Then** structural/IaC component extraction continues working cleanly without forcing imperative-language AST errors.

---

### User Story 3 - 372-Repo Corpus Tooling Sync, Expanded Random Sampler & Benchmark SLA Recovery (Priority: P1)

As a platform maintainer, I want `scripts/curate_corpus.py` synchronized with the expanded 372-repository / 10-ecosystem corpus (never silently truncating back to 100 entries), `atruss benchmark --random-sample` capable of sampling across all searchable code ecosystems, and monorepo bottlenecks/misclassifications resolved so benchmark runs meet `>= 98%` crash-free completion and `>= 90%` classification accuracy at `--timeout 180`.

**Why this priority**: Latest snapshot [`exports/latest/benchmark_summary.md`](../../exports/latest/benchmark_summary.md) (`Run ID: 2026-11-15_05-24-40`, `--timeout 60`) hit **52 timeouts (`86.02%` crash-free)** on monorepos and **`85.31%` classification accuracy** (with `Container / Helm / IaC` at `32/54` and `Java` at `20/30`), while `scripts/curate_corpus.py --write` would overwrite the 372-repo file down to 100 repos.

**Independent Test**: Run `python scripts/curate_corpus.py --validate` verifying all 372 repos / 10 ecosystems pass without truncation, test mocked `--random-sample` selection across >4 ecosystems, and replay `exports/latest/anomalies.json` verifying timeout/classification fixes on problematic fixtures.

**Acceptance Scenarios**:

1. **Given** `tests/fixtures/popular_100_corpus.json` with 372 entries across 10 ecosystems, **When** `scripts/curate_corpus.py --validate` (or `--write`) runs, **Then** it preserves and validates all 372 stratified entries cleanly.
2. **Given** `atruss benchmark --random-sample 20 --seed 2026` (mocked or live), **When** language queries are constructed, **Then** `ECOSYSTEM_SEARCH_LANG` samples across all configured searchable ecosystems rather than only 4 languages.
3. **Given** large monorepos previously timing out (`n8n`, `supabase`, `home-assistant/core`, etc.) and misclassified `Container / Helm / IaC` / multi-language repos, **When** bounded tree scanning / file caps and [`manifests/ecosystems.yaml`](../../manifests/ecosystems.yaml) rules run at `--timeout 180`, **Then** crash-free completion reaches `>= 98%` and classification accuracy reaches `>= 90%`.

---

### User Story 4 - Ratified Superior Portal Architecture, Build Performance & Doc/Env Hygiene (Priority: P2)

As an engineering portal maintainer and agentic contributor, I want existing superior code features formally ratified as standard contracts (4 M3 tabs, 15 chips + pagination, CSS `.m3-*` styling, Astro 6 + Mermaid v12 ELK, `orgs-summary.json`, `reports/{org}/{repo}.mdx`, `pipeline_architecture.md`), realistic multi-hundred-page Astro build SLA targets/optimizations (`< 65s` with Pagefind at 323+ pages or faster incremental generation), and consistent `.venv` + agent rules so every verification gate achieves `Grade: A`.

**Why this priority**: Resolves minor documentation/environment mismatches before ongoing releases without undoing the UX improvements already shipped on `main`.

**Independent Test**: Verify `ruff check`, `pytest` (`0` failures, `0` skips), `validate_agent_workflow.py --spec specs/010-parity-and-hardening` (`Grade: A`), and dual Astro builds (`/`, `ASTRO_BASE=/atruss-code-atlas`) succeed cleanly within target thresholds.

**Acceptance Scenarios**:

1. **Given** `.venv` synced with `pyproject.toml` `[dev]` extras, **When** `scripts/validate_agent_workflow.py` executes, **Then** all 5 gates pass (`Grade: A`, `0` skipped tests, `0` failures).
2. **Given** 323+ generated `.mdx` repository pages in `web/`, **When** `npm run copy-data && npm run build` executes (both `/` and `ASTRO_BASE=/atruss-code-atlas`), **Then** all 4 M3 tabs, 15 chips, pagination controls, and Pagefind search complete within the calibrated SLA with zero broken links.

---

### Edge Cases

- **Offline Execution Without Package Registries or NVD**: When offline or rate-limited during `analyze-code` or `check`, outdated version checks and NVD lookups MUST fail closed-gracefully (`is_outdated=False`, `latest_version=None`, cached OSV results if available) without crashing the CLI or breaking Gate 5 SHA-256 determinism.
- **Uninstalled Optional Grammar Wheels**: If a target ecosystem grammar wheel is unavailable at runtime, `treesitter_engine.py` / `orchestrator.py` MUST degrade cleanly to deterministic fallback metrics with `"ast_engine": "fallback"` while CI `[dev]` environments enforce full CST parity.
- **Massive Monorepos Under `--timeout 180`**: Repos with tens of thousands of vendor/generated files MUST respect bounded directory pruning and per-file byte/line caps so clone-plus-analysis fits comfortably inside the 180-second circuit breaker without starving smaller concurrent tasks.
- **Corpus Size Growth (`>= 372` Repos)**: Portal stub generation and Astro Pagefind indexing MUST handle 372+ repos cleanly without memory exhaustion or regression in `ScorecardHeatmap` / `RepoGrid` pagination.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Target Remediation & Hardening Requirements (`FR-001`–`FR-010`)
- **FR-001**: System MUST populate `DependencyRecord.is_outdated` and `DependencyRecord.latest_version` (`src/models/artifacts.py`) via cached or opt-in package registry metadata queries (supporting the 9 dependency ecosystems parsed in `src/analyzers/dependencies/manifest_parser.py`) while remaining deterministic (`False`/`None`) when offline.
- **FR-002**: `src/analyzers/dependencies/osv_client.py` MUST support optional CVSS v3/v4 enrichment (NIST NVD cache / opt-in `--live-nvd` alongside primary `OSV.dev` `/v1/querybatch`) with full offline `httpx.MockTransport` unit test coverage.
- **FR-003**: `atruss check` (`src/cli/commands/check.py`) MUST evaluate offline cached OSV advisories (and optional `--live-osv` / `--check-outdated` flags) rather than hardcoding `vulnerabilities=[]`, propagating dependency/vulnerability severities into SARIF v2.1.0 outputs and quality gate pass/fail decisions.
- **FR-004**: `src/analyzers/code/treesitter_engine.py` and `src/analyzers/code/orchestrator.py` MUST expand CST/AST complexity, clone duplication, dead-code, and import-edge extraction to **Go, Rust, Ruby, PHP, and Elixir** alongside Python, C#, JS/TS, and Java, while preserving `infra_devops` structural/IaC extraction and `"fallback"` safety.
- **FR-005**: `pyproject.toml`, `requirements.txt`, and `tests/unit/test_treesitter_engine.py` / `tests/unit/test_multi_ecosystem_support.py` MUST declare and verify all enabled language grammar dependencies and pass with `0` failures and `0` skips under synced `[dev]` environments.
- **FR-006**: `scripts/curate_corpus.py` MUST synchronize `CURATED_CATALOG` with all **372 repositories across 10 ecosystems** in `tests/fixtures/popular_100_corpus.json` and support safe schema/count validation without downgrading the corpus to 100 entries.
- **FR-007**: `src/cli/commands/benchmark.py` (`ECOSYSTEM_SEARCH_LANG`) MUST support stratified `--random-sample` discovery across all searchable programming ecosystems configured in `manifests/ecosystems.yaml`.
- **FR-008**: Benchmark pipeline & [`manifests/ecosystems.yaml`](../../manifests/ecosystems.yaml) rules MUST optimize oversized monorepo traversal (resolving the 52 timeouts recorded in `2026-11-15_05-24-40` at `--timeout 60`) and refine `Container / Helm / IaC` & multi-language classification tie-breakers to achieve `>= 98%` crash-free completion and `>= 90%` accuracy at `--timeout 180`.
- **FR-009**: Spec & Governance alignment MUST ratify existing superior behaviors (`4`-tab `RepoTabs.astro`, `15` M3 filter chips + `24`/`20` pagination, CSS `.m3-*` classes, `Astro 6 + Mermaid v12 ELK`, `orgs-summary.json`, `reports/{org}/{repo}.mdx`, `reports/pipeline_architecture.md`, and `atruss benchmark --isolated/--checkpoint-dir/--resume`), update `.agent/rules/specify-rules.md` (`Astro 6+`), and recalibrate portal build targets (`< 65s` across 323+ pages with Pagefind, or faster via build optimization).
- **FR-010**: Comprehensive unit, contract, and integration tests MUST cover `FR-001`–`FR-009` in `tests/` and `web/src/tests/`, passing `ruff check`, `pytest --strict-markers`, Astro `npm test` + dual static builds, and `scripts/validate_agent_workflow.py --spec specs/010-parity-and-hardening` at `Grade: A`.

### Preserved Code Capabilities (Ratified Baseline — Do Not Regress)

| Area | Legacy Spec Text (`007`–`009`) | Superior Existing Implementation | Spec `010` Disposition |
| :--- | :--- | :--- | :--- |
| **Multi-Language & Corpus Scope** | 4 languages / 100-repo corpus (`curate_corpus.py`) | **10 ecosystems / 372 repos** via `manifests/ecosystems.yaml`, `orchestrator.py`, `manifest_parser.py`, `tests/fixtures/popular_100_corpus.json` | **Preserve & Expand** AST/sampler parity (`FR-004`..`008`); never revert to 4 langs / 100 repos |
| **Repository Detail Tabs** | 3 M3 Primary Tabs | **4 M3 Primary Tabs** (`Discovery`, `Pipeline`, `Arc42`, `6-D Scorecard & Security`) in `RepoTabs.astro` + `ScorecardHeatmap.astro` | **Ratify 4 Tabs** (`FR-009`) |
| **Catalog Chips & Pagination** | 8 filter chips, unpaginated list | **15 M3 filter chips** across 10 ecosystems + **24-card grid / 20-org table pagination** | **Ratify UX** (`FR-009`) |
| **Portal Stack & Branding** | Astro v5 + `<md-*>` DOM elements | **Astro 6 + Starlight + Mermaid v12 ELK**, `.m3-*` CSS tokens, `atruss-logo.png`, `orgs-summary.json` | **Ratify Stack** (`FR-009`) |
| **Report Paths & Benchmark Flags** | `{org}/{repo}.md`, `pipeline_topology.md`, basic batch runner | `reports/{org}/{repo}.mdx`, `reports/pipeline_architecture.md`, `--isolated`, `--checkpoint-dir`, `--resume`, `--replay` | **Ratify Paths & Flags** (`FR-008`, `FR-009`) |

### Key Entities

- **OutdatedDependencyMetadata**: Extended `DependencyRecord` attribution (`is_outdated`, `latest_version`, source timestamp/cache hit) used by `Scorecard` and `SARIF` exports.
- **AdvisoryEnrichmentRecord**: Unified `OSV.dev` + optional NIST NVD CVSS severity metadata consumed identically by `analyze-code` and `check`.
- **PolyglotLanguageAdapter**: Declarative language grammar & structural fallback mapping bridging `manifests/ecosystems.yaml`, `treesitter_engine.py`, and `orchestrator.py`.
- **CorpusManifestCatalog**: Synchronized 372-repository / 10-ecosystem benchmark fixture and curation script contract.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (Dependency & Gate Parity)**: Outdated dependency detection populates `is_outdated` / `latest_version` accurately on mocked/live registry fixtures while staying deterministic (`SHA-256` identical) offline, and `atruss check` surfaces cached/live CVEs without hardcoding `vulnerabilities=[]`.
- **SC-002 (Expanded Polyglot CST Metrics)**: Go, Rust, Ruby, PHP, and Elixir test fixtures produce non-fallback AST complexity, duplication, dead-code, and import-edge metrics when `[dev]` grammars are installed, while `infra_devops` continues structural/IaC extraction without errors.
- **SC-003 (Corpus Tooling Parity)**: `scripts/curate_corpus.py --validate` validates all **372 repositories across 10 ecosystems** with zero data loss, and `--random-sample` supports all searchable programming ecosystems.
- **SC-004 (Benchmark SLA & Accuracy Recovery)**: Re-running the 372-repo corpus benchmark under `--isolated --timeout 180` achieves **`>= 98%` crash-free completion** and **`>= 90%` classification accuracy** (resolving the `86.02%` / `85.31%` gap in `2026-11-15_05-24-40`).
- **SC-005 (Zero-Skip Suite & Grade `A` Validator)**: `pytest tests/ -v --strict-markers` passes `100%` of tests (`0` failures, `0` skips) and `scripts/validate_agent_workflow.py --spec specs/010-parity-and-hardening` achieves **`Grade: A`** (5/5 gates).
- **SC-006 (Portal Quality & Build Calibration)**: All 4 M3 tabs, 15 filter chips, and `24`/`20` pagination pass `npm test`, and both `npm run build` (`/`) and `ASTRO_BASE=/atruss-code-atlas npm run build` complete cleanly in **`<= 65s`** for `323+` HTML pages with zero broken internal links.
- **SC-007 (Zero Regression on Superior Code)**: All existing capabilities verified in `test_multi_ecosystem_support.py`, `ScorecardHeatmap.astro`, `RepoTabs.astro`, `RepoGrid.astro`, `generate-org-summary.py`, and Mermaid v12 ELK remain intact or enhanced.
- **SC-008 (Spec & Rule Consistency)**: Documentation, Spec `010`, and `.agent/rules/specify-rules.md` agree on `Astro 6+`, `reports/{org}/{repo}.mdx`, and `pipeline_architecture.md`.

---

## Assumptions

- Outdated registry checks (`PyPI`, `npm`, `NuGet`, `crates.io`, etc.) and optional NIST NVD queries MUST remain opt-in or cache-backed so CI and air-gapped runs stay deterministic (`NFR-DET-01`, `NFR-POR-01`).
- Tree-sitter language grammar wheels installed via `pyproject.toml` `[dev]` / runtime dependencies support Linux/WSL Python 3.11+ without native compilation failures.
- No database (PostgreSQL), broker (Redis/Celery), or backend API server (FastAPI) is introduced, preserving Constitution Principle Portability.
