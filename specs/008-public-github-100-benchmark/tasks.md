# Tasks: 100 Popular + Randomized Public GitHub Benchmark & Self-Healing Agent Loop

**Input**: Design documents from `/specs/008-public-github-100-benchmark/`  
**Prerequisites**: `plan.md`, `spec.md`, `006-core-unification-and-eval`

---

## Phase 1: 100 Popular GitHub Projects Corpus & Models (US1)

**Goal**: Define the Pydantic benchmark models and curate the 100 popular GitHub repositories catalog (`25 Python`, `25 .NET`, `25 React/TS/JS`, `25 Java Spring Boot`).

- [x] T001 [P] [US1] Create `src/models/benchmark.py` defining `CorpusEntry`, `BenchmarkRepoResult`, `AnomalyRecord`, `BenchmarkManifest`, and `BenchmarkSummary` Pydantic models (`FR-001`, `FR-004`).
- [x] T002 [P] [US1] Create `tests/fixtures/popular_100_corpus.json` and `scripts/curate_corpus.py` containing 100 stratified popular public repositories (`< 250MB` / `< 500k LoC`) including golden PRD fixtures (`dotnet/eShop`, `github-samples/pets-workshop`, `Azure-Samples/todo-nodejs-mongo-terraform`, `hamvocke/spring-testing`) (`FR-001`, `SC-001`).
- [x] T003 [US1] Write unit tests in `tests/unit/test_benchmark_runner.py` validating `popular_100_corpus.json` schema, 25-per-ecosystem balance, and size/SLA constraints (`SC-001`).

---

## Phase 2: Stratified Random Sampler & Fault-Isolated `atruss benchmark` CLI (US1, US2, US3)

**Goal**: Implement `atruss benchmark` supporting `--corpus popular-100`, `--random-sample N --seed S`, and `--replay`, with shallow blobless clones, 180s timeouts, and `anomalies.json` generation.

- [x] T004 [P] [US3] Upgrade `src/core/utils/git_cloner.py` to use `--depth 1 --filter=blob:none --single-branch` and guarantee immediate temporary directory deletion on context exit (`FR-003`, `SC-002`).
- [x] T005 [US2] Implement the stratified random GitHub sampler in `src/cli/commands/benchmark.py` querying `/search/repositories` across ecosystems and star tiers (`100..1000`, `1000..10000`, `>10000`) with deterministic `--seed` and saving `exports/latest/benchmark_manifest.json` (`FR-002`).
- [x] T006 [US1, US3] Implement the core async batch execution engine in `src/cli/commands/benchmark.py` with `asyncio.wait_for(..., timeout=180.0)`, running discovery + pipeline DAG + code AST per repo, exporting Astro-compatible artifacts into `exports/latest/`, and logging any errors or misclassifications to `exports/latest/anomalies.json` and `benchmark_summary.{json,md}` (`FR-002`, `FR-003`, `FR-004`).
- [x] T007 [US1] Register the `benchmark` command in `src/cli/main.py` and write unit/integration tests in `tests/unit/test_benchmark_runner.py` and `tests/integration/test_benchmark_e2e.py` covering `--corpus`, `--random-sample`, `--replay`, and circuit-breaker anomaly capture (`FR-002`, `SC-003`).

---

## Phase 3: Autonomous Self-Healing Skill & Local/Remote Agent Execution (US3)

**Goal**: Package the self-healing benchmark loop so it can be triggered locally or on a Google AI Pro Remote Agent.

- [x] T008 [P] [US3] Create `.agent/skills/benchmark-self-heal/SKILL.md` and `scripts/run_benchmark_loop.py` defining the step-by-step autonomous loop: run `atruss benchmark` → inspect `anomalies.json` → generate failing unit test → patch `src/analyzers/` or `manifests/ecosystems.yaml` → verify via `scripts/validate_agent_workflow.py` → re-run failed repos via `--replay` → rebuild Astro UI (`FR-005`).
- [x] T009 [US3] Execute an initial live benchmark slice (`atruss benchmark --corpus popular-100 --limit 12` across all 4 ecosystems) to populate `exports/latest/` with rich real-world multi-org data and verify that `cd web && npm run build` renders all benchmarked repositories cleanly (`SC-003`, `SC-004`).
