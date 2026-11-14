# Atruss Code Atlas Development Guidelines

Synced with Constitution v2.1.0 & Unified Specification (`009-unified-atlas-spec`)

## Active Technologies
- **Core Engine**: Python 3.10+ (Typer CLI), `httpx` (Async REST + Rate-Limit Backoff), NetworkX (Pipeline & Dependency DAGs), Pydantic v2 (Contracts), Pytest (0-Skip Test Harness)
- **UI / Intelligence Portal**: Astro 6 + Starlight (Material Design 3 Docs-as-Code SSG), Node.js v22 (managed by `fnm`)
- **Rendering**: Mermaid (`astro-mermaid` + client lazy hydration), Arc42 Markdown
- **Data Layers**: Local Filesystem (`exports/latest/` CSV, JSON, YAML, and Markdown artifacts) — *100% offline-capable*
- **Excluded Technologies**: Celery, Redis, FastAPI, PostgreSQL, S3/MinIO

## Project Structure

```text
docs/          # Master PRD v2.0, Baseline PRD v1.0, Unified Spec, and Agentic SDLC Playbook
manifests/     # Policy-as-Code classification rules (ecosystems.yaml)
src/           # Core CLI, 4-ecosystem structural code analyzers, pipeline DAG engine, exporters
scripts/       # 5-Gate Workflow Validator, 100-repo benchmark orchestrator, MDX stub generator
specs/         # SpecKit feature lineage (001 through 009-unified-atlas-spec)
tests/         # Unit and offline/live integration test suites (strict 0-skip enforcement)
web/           # Material Design 3 Astro Starlight static portal
exports/       # Canonical latest telemetry & reports (exports/latest/)
```

## Canonical Commands

- **Lint & Unit Tests**: `.venv/bin/ruff check src/ scripts/ && .venv/bin/pytest tests/unit/ -v --strict-markers`
- **Full Test Suite**: `.venv/bin/pytest tests/ -v --strict-markers`
- **5-Gate Agentic Workflow Validator**:
  - `.venv/bin/python scripts/validate_agent_workflow.py --spec specs/009-unified-atlas-spec`
  - `.venv/bin/python scripts/validate_agent_workflow.py --spec specs/006-core-unification-and-eval`
- **Self-Healing 100-Repo Benchmark**: `.venv/bin/python scripts/run_benchmark_loop.py --corpus popular-100 --limit 12 --validate`
- **Astro Web Portal (Test & Build)**: `cd web && npm test && npm run build`

## Code Style & Development Environment

- **Execution Environment**: Windows Subsystem for Linux (WSL) or Linux CI (`ubuntu-latest`).
- **Python**: Dependencies isolated within `.venv` at the repository root.
- **Node.js**: Managed via `fnm` pointing to Node.js v22+ (see `.agent/rules/headless-shell.md` for non-interactive shell invocations).
- **Architectural Tenets**:
  1. Policy-as-Code (`manifests/ecosystems.yaml`)
  2. Single Source of Truth (`exports/latest/` JSON/YAML/CSV/MD contracts)
  3. Strict Spec-Driven & Test-Driven Development enforced by the 5-Gate Validator (`Grade: A`, `0` skipped tests, `0` AST stubs/TODOs)
