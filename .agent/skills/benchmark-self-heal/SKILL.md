---
name: benchmark-self-heal
description: Autonomous self-healing benchmark and anomaly-triage workflow for Atruss Code Atlas. Executes `atruss benchmark` against the 100 Popular GitHub Projects corpus or stratified random GitHub samples, inspects `anomalies.json`, generates regression tests before patching analyzers, verifies via the 5-Gate Validator, replays failed repositories, and rebuilds the Material Design 3 Astro UI. Suitable for local `/goal` loops or Google AI Pro Remote Agents.
compatibility: Requires Python 3.10+, git 2.25+ (blobless clone support), Node 20+, and `.venv` with `atruss` dependencies installed.
metadata:
  track: 008-public-github-100-benchmark
  sla_crash_free_pct: "98.0"
  sla_classification_pct: "90.0"
  sla_timeout_seconds: "180"
---

# Benchmark Self-Healing Agent Skill

Use this skill to harden `atruss-code-atlas` against real-world public GitHub repositories either locally (via `/goal` or `/schedule`) or via **Google AI Pro Remote Agents**.

## Operating Rules

1. **Strict TDD First**: Never patch `src/analyzers/` or `manifests/ecosystems.yaml` before writing a failing unit test in `tests/unit/` reproducing the exact anomaly from `exports/latest/anomalies.json`.
2. **Disk & Rate-Limit Safety**: Keep `--max-concurrent 4` (or lower) and `--timeout 180`. Shallow blobless clones (`--depth 1 --filter=blob:none --single-branch`) are deleted automatically on context exit. Prefer `--corpus popular-100` when `GH_TOKEN` is absent (clones use git protocol, consuming zero GitHub REST API quota).
3. **Preserve 0-Skip Gate**: Never use `pytest.skip` or stub placeholders; all fixes must pass `scripts/validate_agent_workflow.py` (`Grade: A`).

## Step-by-Step Self-Healing Loop

### Step 1: Run a Stratified Benchmark Batch
Choose a deterministic popular slice or a stratified random sample:

```bash
# Stratified popular corpus slice (3 per ecosystem = 12 repos, or all 100)
.venv/bin/python -m src.cli.main benchmark --corpus popular-100 --limit 12

# Full 100 popular GitHub repositories
.venv/bin/python -m src.cli.main benchmark --corpus popular-100 --max-concurrent 4 --timeout 180

# Stratified random GitHub sampling across star buckets (100..1000, 1000..10000, >10000)
.venv/bin/python -m src.cli.main benchmark --random-sample 12 --seed 2026

# Or use the automated batch orchestrator
.venv/bin/python scripts/run_benchmark_loop.py --corpus popular-100 --limit 20 --rebuild-web
```

### Step 2: Inspect Scorecard & Anomaly Ledger
Review the structured outputs generated under `exports/latest/`:
- `exports/latest/benchmark_summary.json` & `benchmark_summary.md`
- `exports/latest/anomalies.json`
- `exports/latest/benchmark_manifest.json` (pinned commit SHAs for exact reproduction)

Check thresholds:
- **Crash-Free Completion (`crash_free_rate_pct`)**: Target `>= 98.0%` (`SC-003`)
- **Classification Accuracy (`classification_accuracy_pct`)**: Target `>= 90.0%` (`SC-003`)
- **SLA Compliance (`<= 180s` per repo)**: Target `100%` (`NFR-PERF-01`)

### Step 3: Triage Anomalies & Apply Test-First Fix
For each item in `exports/latest/anomalies.json`:
1. **`stage == "classification"`**: Check the repository's manifest layout (e.g., monorepo subdir `pom.xml`, `*.csproj`, `package.json`, `pyproject.toml`) and update pattern scoring or weights in `manifests/ecosystems.yaml` / `src/analyzers/classification.py`. Add a fixture tree test in `tests/unit/test_classification.py`.
2. **`stage == "analyze-pipeline"`**: Inspect the traceback against `.github/workflows/*.yml` edge cases (e.g., matrix expressions, `workflow_call`, non-string scalars) and add a unit test in `tests/unit/test_dag_builder.py` before fixing `src/analyzers/pipeline/`.
3. **`stage == "analyze-code"`**: Inspect the traceback or encoding/AST failure, add a unit test in `tests/unit/test_arc42_generator.py`, and fix the corresponding analyzer in `src/analyzers/code/`.
4. **`stage == "timeout"`**: Identify non-source vendor/asset directories causing slow traversals and add them to `SKIP_DIRS` in `src/analyzers/code/base.py`.

### Step 4: Verify Gates & Replay Failed Repositories
```bash
# Re-run previously failing / anomalous repositories cleanly
.venv/bin/python -m src.cli.main benchmark --replay exports/latest/anomalies.json

# Run full pytest suite and 5-Gate Validator
.venv/bin/pytest tests/ -v --strict-markers
.venv/bin/python scripts/validate_agent_workflow.py --spec specs/008-public-github-100-benchmark
```

### Step 5: Rebuild Material Design 3 Astro Dashboard
```bash
cd web && npm run build
```
Verify `0` Astro content schema errors, `0` Mermaid syntax errors, and clean rendering across Overview (`/`), Benchmark Organization Leaderboard (`/orgs/`), and Repository Tabs (`/reports/<org>/<repo>/`).
