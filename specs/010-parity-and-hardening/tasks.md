# Tasks: Post-Release Parity, Polyglot Depth & Benchmark SLA Hardening

**Input**: Design documents from `/specs/010-parity-and-hardening/`  
**Prerequisites**: [`plan.md`](./plan.md) (required), [`spec.md`](./spec.md) (required), [`checklists/requirements.md`](./checklists/requirements.md)  
**Note**: Spec `010` is a **pending specification** authored after the `2026-11-15` documentation/implementation audit; all tasks remain unchecked (`[ ]`) until implemented via TDD.

---

## Phase 1: Environment Sync & Superior Baseline Ratification Setup

**Goal**: Align local `[dev]` runtime dependencies and rule docs ahead of TDD cycles while locking preserved capabilities (`10 ecosystems / 372 repos`, `4 UI tabs`, `15 filter chips`, `Astro 6 + Mermaid v12 ELK`, `orgs-summary.json`, `reports/{org}/{repo}.mdx`, `pipeline_architecture.md`).

- [ ] T001 Sync Python `[dev]` dependencies (`uv pip install -e ".[dev]"`) verifying `tree-sitter*` grammar wheels and resolve `.agent/rules/specify-rules.md` (`Astro 5+` -> `Astro 6+`) (`FR-005`, `FR-009`, `SC-005`, `SC-008`)
- [ ] T002 [P] Audit [`tests/unit/test_multi_ecosystem_support.py`](../../tests/unit/test_multi_ecosystem_support.py) and `web/src/tests/` assertions to lock regression guards around 10 ecosystems, 4 UI tabs (`RepoTabs.astro`), 15 filter chips (`RepoGrid.astro`), and `24`/`20` pagination (`FR-009`, `SC-007`)

---

## Phase 2: User Story 1 - Dependency Freshness, NVD/CVSS Enrichment & `atruss check` Parity (Priority: P1) 🎯 MVP

**Goal**: Populate `is_outdated`/`latest_version`, support optional CVSS/NVD enrichment alongside `OSV.dev`, and enable `atruss check` to evaluate cached/opt-in live advisories cleanly (`FR-001`, `FR-002`, `FR-003`, `SC-001`).

**Independent Test**: Run `pytest tests/unit/test_dependencies_osv_sbom.py tests/unit/test_drift_sarif_mcp.py` with mocked `httpx.MockTransport` registry and advisory responses verifying `is_outdated`, CVSS fields, and non-empty `vulnerabilities` in `atruss check --sarif`.

### Tests for User Story 1 (Write First — Fail Before Implementation)

- [ ] T003 [P] [US1] Add failing unit tests in `tests/unit/test_dependencies_osv_sbom.py` for cached/mocked registry outdated version detection (`DependencyRecord.is_outdated`, `latest_version`) and optional NVD CVSS normalization (`FR-001`, `FR-002`, `SC-001`)
- [ ] T004 [P] [US1] Add failing unit tests in `tests/unit/test_drift_sarif_mcp.py` verifying `atruss check` evaluates offline cached OSV advisories (and opt-in `--live-osv` / `--check-outdated`) rather than hardcoding `vulnerabilities=[]` (`FR-003`, `SC-001`)

### Implementation for User Story 1

- [ ] T005 [US1] Implement cached and opt-in registry freshness lookup (PyPI, npm, NuGet, Maven, Go, Cargo, RubyGems, Packagist, Hex) populating `DependencyRecord.is_outdated` and `latest_version` in `src/analyzers/dependencies/manifest_parser.py` while keeping offline defaults deterministic (`FR-001`)
- [ ] T006 [US1] Implement optional NVD/CVSS enrichment helper with cache and `httpx.MockTransport` support in `src/analyzers/dependencies/osv_client.py` (`FR-002`)
- [ ] T007 [US1] Update `src/cli/commands/check.py` to load offline cached OSV advisories and support `--live-osv` / `--check-outdated` flags feeding SARIF v2.1.0 and `scorecard.py` (`FR-003`, `SC-001`)

---

## Phase 3: User Story 2 - Polyglot CST/AST Depth Across Go, Rust, Ruby, PHP & Elixir (Priority: P1)

**Goal**: Upgrade Go, Rust, Ruby, PHP, and Elixir from `_run_generic_structural()` LOC-only fallback to CST complexity, clone duplication, dead-code, and import-edge telemetry while preserving `infra_devops` structural/IaC extraction (`FR-004`, `FR-005`, `SC-002`).

**Independent Test**: Run `pytest tests/unit/test_treesitter_engine.py tests/unit/test_multi_ecosystem_support.py` across Go, Rust, Ruby, PHP, Elixir, and `infra_devops` fixtures verifying non-fallback CST metrics and preserved fallback/IaC behavior.

### Tests for User Story 2 (Write First — Fail Before Implementation)

- [ ] T008 [P] [US2] Add failing unit tests in `tests/unit/test_treesitter_engine.py` asserting cyclomatic complexity, cognitive complexity, clones, dead code, and import edges across Go, Rust, Ruby, PHP, and Elixir fixtures (`FR-004`, `SC-002`)
- [ ] T009 [P] [US2] Add regression checks in `tests/unit/test_multi_ecosystem_support.py` ensuring `infra_devops` keeps specialized Dockerfile/Helm/Terraform structural extraction and missing-grammar fallback remains safe (`FR-004`, `FR-005`)

### Implementation for User Story 2

- [ ] T010 [US2] Declare required polyglot grammar bindings in `pyproject.toml` and `requirements.txt` (`FR-005`)
- [ ] T011 [US2] Extend grammar registration, AST decision-point traversal, clone tokenization, dead-code extraction, and import-edge resolution for Go, Rust, Ruby, PHP, and Elixir in `src/analyzers/code/treesitter_engine.py` (`FR-004`)
- [ ] T012 [US2] Wire Go, Rust, Ruby, PHP, and Elixir CST analysis in `src/analyzers/code/orchestrator.py` while keeping `_run_generic_structural` fallback when grammar wheels are absent and specialized `infra_devops` extraction intact (`FR-004`, `FR-005`, `SC-002`)

---

## Phase 4: User Story 3 - 372-Repo Corpus Tooling Sync, Random Sampler & Benchmark SLA Recovery (Priority: P1)

**Goal**: Sync `scripts/curate_corpus.py` to all 372 repos / 10 ecosystems, expand `ECOSYSTEM_SEARCH_LANG` in `atruss benchmark --random-sample`, and fix the 52 monorepo timeouts and classification mismatches (`FR-006`, `FR-007`, `FR-008`, `SC-003`, `SC-004`).

**Independent Test**: Run `python scripts/curate_corpus.py --validate`, `pytest tests/unit/test_benchmark_runner.py tests/integration/test_benchmark_e2e.py`, and replay `exports/latest/anomalies.json` under `--isolated --timeout 180` confirming `>= 98%` crash-free completion and `>= 90%` classification accuracy.

### Tests for User Story 3 (Write First — Fail Before Implementation)

- [ ] T013 [P] [US3] Add failing tests in `tests/unit/test_benchmark_runner.py` validating `scripts/curate_corpus.py` 372-repo / 10-ecosystem integrity (no truncation to 100) and `ECOSYSTEM_SEARCH_LANG` coverage across expanded ecosystems (`FR-006`, `FR-007`, `SC-003`)
- [ ] T014 [P] [US3] Add anomaly-reproduction and monorepo bounded-scan tests in `tests/integration/test_benchmark_e2e.py` and `tests/unit/test_classification.py` targeting `Container / Helm / IaC` and multi-language tie-breakers from `exports/latest/anomalies.json` (`FR-008`, `SC-004`)

### Implementation for User Story 3

- [ ] T015 [US3] Synchronize `CURATED_CATALOG` and validation logic in `scripts/curate_corpus.py` with the 372-repository, 10-ecosystem dataset in `tests/fixtures/popular_100_corpus.json` (`FR-006`, `SC-003`)
- [ ] T016 [US3] Expand `ECOSYSTEM_SEARCH_LANG` and implement bounded monorepo scan optimizations in `src/cli/commands/benchmark.py` and `src/analyzers/code/orchestrator.py` (with shallow blobless protections in `src/core/utils/git_cloner.py`) to eliminate the 52 timeout bottlenecks (`FR-007`, `FR-008`, `SC-004`)
- [ ] T017 [US3] Refine `Container / Helm / IaC` and multi-language detection signals and tie-breakers declaratively in `manifests/ecosystems.yaml` and verify via `atruss benchmark --replay exports/latest/anomalies.json --isolated --timeout 180` (`FR-008`, `SC-004`)

---

## Phase 5: User Story 4 - Ratified Portal Architecture, Build SLA Calibration & Docs Alignment (Priority: P2)

**Goal**: Lock ratified UI/export contracts, optimize/calibrate 323+ page Astro builds within `<= 65s`, and finalize developer/validator consistency (`FR-009`, `FR-010`, `SC-005`, `SC-006`, `SC-007`, `SC-008`).

**Independent Test**: Run `web` `npm test`, `npm run build` (`/` and `ASTRO_BASE=/atruss-code-atlas`), and `scripts/validate_agent_workflow.py --spec specs/010-parity-and-hardening` confirming `Grade: A` and `<= 65s` static builds.

- [ ] T018 [US4] Measure and optionally optimize `scripts/generate-report-stubs.py` and Pagefind indexing in `web/package.json` / `web/astro.config.mjs` keeping `<= 65s` static builds across 323+ HTML pages under both `/` and `ASTRO_BASE=/atruss-code-atlas` (`FR-009`, `SC-006`)
- [ ] T019 [P] [US4] Update cross-references in `docs/` (`atruss-code-atlas-prd.md`, `metrics-methodology.md`, `README.md`) once Spec `010` features land to reflect 100% live status (`FR-009`, `FR-010`, `SC-008`)

---

## Phase 6: Final Cross-Cutting Verification & Release Readiness

- [ ] T020 Run full verification suite after all edits (`ruff check src/ tests/ scripts/`, `pytest tests/ -v --strict-markers`, `cd web && npm test && npm run build && ASTRO_SITE=https://kumarshaz.github.io ASTRO_BASE=/atruss-code-atlas npm run build`, and `.venv/bin/python scripts/validate_agent_workflow.py --spec specs/010-parity-and-hardening`) confirming Grade `A`, 0 skipped tests, and 0 missing targets (`FR-010`, `SC-005`, `SC-006`, `SC-007`)

---

## Dependencies & Execution Order

- **Phase 1 (`T001`–`T002`)** establishes synced `[dev]` wheels and regression locks before TDD runs.
- **US1 (`T003`–`T007`)**, **US2 (`T008`–`T012`)**, and **US3 (`T013`–`T017`)** have disjoint primary file ownership (`dependencies/` + `check.py` vs `code/treesitter_engine.py` vs `curate_corpus.py` + `benchmark.py` + `manifests/ecosystems.yaml`), enabling parallel agent execution waves (only coordinating edits to `orchestrator.py` cleanly between `T012` and `T016`).
- **US4 (`T018`–`T019`)** and **Phase 6 (`T020`)** finalize portal timing, doc sync, and 5-Gate Grade `A` sign-off.
