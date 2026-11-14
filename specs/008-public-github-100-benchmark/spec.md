# Feature Specification: 100 Popular + Randomized Public GitHub Benchmark & Self-Healing Agent Loop

**Feature Branch**: `008-public-github-100-benchmark`  
**Created**: 2026-11-12  
**Status**: Approved (Aligned via `/grill-me`)  
**Input**: User requirement to create a task on local machine or Google AI Pro Remote Agents to iterate through coding and validation against 100 popular public GitHub projects plus randomized sample GitHub projects.

---

## 1. Context & Problem Statement

Testing Atruss Code Atlas against only 1 or 2 sample repositories hides edge cases found in real-world engineering organizations (e.g., complex matrix workflows, `workflow_call` reusable pipelines, monorepo subdirectory manifests, non-UTF8 files, or unusual `.csproj`/`pom.xml`/`package.json` layouts).

To harden the platform to production grade, we need:
1. A curated, deterministic **100 Popular GitHub Projects Corpus** (`tests/fixtures/popular_100_corpus.json`) stratified across the 4 MVP ecosystems (Python, .NET, React/TS/JS, Java Spring Boot) and capped at `< 500k LoC` / `< 250MB` so all 100 respect the 3-minute SLA.
2. A **Dynamic Stratified Random Sampler** (`--random-sample N --seed S`) that queries the GitHub Search API for diverse repositories across star-count buckets and records the exact seed and commit SHAs for deterministic replay.
3. A fault-isolated **`atruss benchmark` CLI command** and an **Autonomous Self-Healing Agent Loop** (executable locally via background task/`/goal` or in the cloud via **Google AI Pro Remote Agents**) that logs any parser/classification anomalies to `anomalies.json`, writes a regression unit test, fixes the analyzer, and re-runs until pass rate reaches `>= 98%`.

---

## 2. Clarifications & Architectural Decisions (from `/grill-me`)

- **Corpus Curation Strategy**: Combine the PRD's pinned golden fixtures (`dotnet/eShop`, `github-samples/pets-workshop`, `Azure-Samples/todo-nodejs-mongo-terraform`, `hamvocke/spring-testing`, etc.) with top-starred GitHub repositories across Python (25), .NET (25), React/TS/JS (25), and Java Spring Boot (25) capped at `< 250MB` / `< 500k LoC`.
- **Self-Healing Iteration Policy**: When running `atruss benchmark`, any exception, timeout, or schema/classification failure is recorded to `exports/{timestamp}/anomalies.json` without crashing the batch. In autonomous agent mode, the agent inspects `anomalies.json`, creates a unit test reproducing the edge case, patches `src/analyzers/`, and re-evaluates the failed repositories until `>= 98%` pass rate is achieved.
- **Disk & Rate-Limit Safety**: Use shallow/blobless clones (`git clone --depth 1 --filter=blob:none --single-branch`) inside an auto-purging temporary directory context manager and enforce a `180s` per-repo timeout circuit breaker (`NFR-PERF-01`).

---

## 3. User Scenarios & Testing *(mandatory)*

### User Story 1 - Curated 100 Popular GitHub Projects Corpus (Priority: P1)

As an automation engineer, I want a version-controlled catalog of 100 popular public GitHub repositories (`tests/fixtures/popular_100_corpus.json`) spanning Python, .NET, React/TS/JS, and Java Spring Boot with pinned SHAs and expected ecosystem labels, so I can benchmark classification and extraction accuracy deterministically.

**Independent Test**: Run `python scripts/curate_corpus.py --validate` to verify that `tests/fixtures/popular_100_corpus.json` contains exactly 100 repositories (25 per ecosystem), valid GitHub URLs, pinned SHAs/branches, and expected classification metadata.

**Acceptance Scenarios**:
1. **Given** `tests/fixtures/popular_100_corpus.json`, **When** validated by `pytest`, **Then** it contains 25 Python, 25 .NET, 25 React/TS/JS, and 25 Java Spring Boot repositories (including the golden PRD fixtures), all under the 250MB size cap.
2. **Given** `--limit N` or `--ecosystem <name>`, **When** running `atruss benchmark --corpus popular-100`, **Then** the runner executes discovery, pipeline DAG analysis, and structural code analysis across the selected slice and outputs `exports/latest/` artifacts ready for the Astro UI.

---

### User Story 2 - Dynamic Stratified Random GitHub Sampler (Priority: P1)

As a chaos-testing engineer, I want `atruss benchmark --random-sample <N> --seed <int>` to dynamically sample random public GitHub repositories across star tiers (`100..1000`, `1000..10000`, `>10000`) and languages, saving the resolved SHAs to `benchmark_manifest.json` so any discovered bug is 100% reproducible.

**Independent Test**: Run `atruss benchmark --random-sample 4 --seed 42` and verify that it queries GitHub Search API (or deterministic mock in offline unit tests), resolves the exact commit SHAs, analyzes all 4 repos, and writes `exports/latest/benchmark_manifest.json`.

**Acceptance Scenarios**:
1. **Given** `--random-sample 12 --seed 2026`, **When** `atruss benchmark` runs, **Then** it samples 3 repositories per ecosystem across star buckets and writes `benchmark_manifest.json` containing the seed, repo URLs, and exact HEAD SHAs.
2. **Given** a previously generated `benchmark_manifest.json`, **When** `atruss benchmark --replay benchmark_manifest.json` runs, **Then** it re-runs the exact same repositories and SHAs deterministically.

---

### User Story 3 - Fault-Isolated Execution, Anomaly Ledger & Self-Healing Agent Task (Priority: P1)

As a developer running Atruss Code Atlas locally or on a **Google AI Pro Remote Agent**, I want `atruss benchmark` to isolate per-repo failures into `anomalies.json` and provide a repeatable agent task workflow that automatically writes regression tests and fixes parser bugs until the benchmark achieves `>= 98%` success.

**Independent Test**: Feed a repository with a deliberately malformed `.github/workflows/broken.yml` or unusual manifest into `atruss benchmark`, verify that the batch continues without crashing, records the failure in `anomalies.json`, and generates a complete `benchmark_summary.md` scorecard.

**Acceptance Scenarios**:
1. **Given** a batch of repositories where one repo times out (`> 180s`) or has invalid YAML syntax, **When** `atruss benchmark` executes, **Then** the circuit breaker catches the error, logs the stack trace and SHA to `anomalies.json`, cleans up the temporary clone directory, and proceeds to the next repo.
2. **Given** a completed benchmark run, **When** the run finishes, **Then** all discovered repositories, pipeline DAGs, and Arc42 reports are exported into `exports/latest/` so the Material Design 3 Astro site immediately visualizes all 100+ projects.

---

## 4. Functional Requirements

- **FR-001**: Create `tests/fixtures/popular_100_corpus.json` and helper script `scripts/curate_corpus.py` containing 100 stratified popular public GitHub repositories (25 Python, 25 .NET, 25 React/TS/JS, 25 Java Spring Boot, `< 250MB` each) with expected ecosystem and pipeline flags.
- **FR-002**: Implement `src/cli/commands/benchmark.py` (`atruss benchmark`) supporting:
  - `--corpus popular-100` (with optional `--limit <N>` and `--ecosystem <eco>`)
  - `--random-sample <N>` and `--seed <int>` (stratified GitHub `/search/repositories` sampler)
  - `--replay <manifest.json>` (deterministic replay of a previous random sample)
  - `--max-concurrent <int>` (default `4`) and `--timeout <seconds>` (default `180`)
- **FR-003**: `atruss benchmark` MUST execute the full 3-stage pipeline (`discover` classification → `analyze-pipeline` DAG + anti-patterns → `analyze-code` Arc42 components) per repository using shallow clones (`--depth 1 --filter=blob:none`) that are immediately deleted upon per-repo completion.
- **FR-004**: `atruss benchmark` MUST write:
  - Standard Astro-ready exports in `exports/latest/{repos,pipelines,relationships,reports}/`
  - `exports/latest/benchmark_summary.json` and `exports/latest/benchmark_summary.md` (classification accuracy %, pipeline parse success %, average runtime per repo, SLA compliance %)
  - `exports/latest/anomalies.json` (detailed structured log of any repo failures, timeouts, or classification mismatches)
- **FR-005**: Provide an Antigravity Skill / Automation script (`.agent/skills/benchmark-self-heal/SKILL.md` and `scripts/run_benchmark_loop.py`) so either a local background task or a **Google AI Pro Remote Agent** can execute the batch, triage `anomalies.json`, add regression tests, and rebuild the Astro UI.

---

## 5. Success Criteria

- **SC-001**: `tests/fixtures/popular_100_corpus.json` passes schema validation with 100 unique, active public repositories (25 per MVP ecosystem).
- **SC-002**: `atruss benchmark` processes repositories with zero temp-disk accumulation (temp directory size returns to baseline after every repo).
- **SC-003**: Ecosystem classification accuracy across the benchmark corpus reaches `>= 90%` (satisfying PRD §9 MVP Definition of Done) and pipeline/code extraction achieves `>= 98%` crash-free completion.
- **SC-004**: All benchmarked repositories render cleanly in the Material Design 3 Astro dashboard (`web/`) and Organization Leaderboard (`/orgs/`).
