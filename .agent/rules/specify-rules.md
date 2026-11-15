# Atruss Code Atlas Development Guidelines

Synced with Constitution v2.1.0 & Unified Specification (`009-unified-atlas-spec`)

## Active Technologies
- **Core Engine**: Python 3.10+ (Typer CLI), `httpx` (Async REST + Rate-Limit Backoff + OSV Batch), NetworkX (Pipeline, Code & C2C DAGs), Tree-sitter (Polyglot CST complexity, clones, dead code), Pydantic v2 (Contracts), Pytest (0-Skip Test Harness)
- **UI / Intelligence Portal**: Astro 5+ / Starlight (Material Design 3 Docs-as-Code SSG), Node.js v22 (managed by `fnm`)
- **Rendering**: Mermaid (`astro-mermaid` + client lazy hydration + SVG/PNG export & Print/PDF styling), Arc42 Markdown + Section 7 Traceability
- **Data Layers**: Local Filesystem (`exports/latest/` CSV, JSON, YAML, Markdown, CycloneDX v1.6 SBOM, OASIS SARIF v2.1.0, `llms.txt`, `catalog-history.json`) — *100% offline-capable*
- **Excluded Technologies**: Celery, Redis, FastAPI, PostgreSQL, S3/MinIO

## Project Structure

```text
docs/          # Master PRD v2.0, Baseline PRD v1.0, Unified Spec, and Agentic SDLC Playbook
manifests/     # Policy-as-Code rules (ecosystems.yaml, architecture-rules.yaml, pipeline-rules.yaml)
src/           # Core CLI (incl. check, diff, mcp), Tree-sitter & fitness analyzers, OSV/SBOM/SARIF/llms exporters
scripts/       # 5-Gate Workflow Validator, 100-repo benchmark orchestrator, MDX stub generator
specs/         # SpecKit feature lineage (001 through 009-unified-atlas-spec)
tests/         # Unit and offline/live integration test suites (strict 0-skip enforcement)
web/           # Material Design 3 Astro Starlight static portal (4-tab reports, heatmaps, cross-repo topology)
exports/       # Canonical latest telemetry, SBOMs, SARIF, llms.txt & reports (exports/latest/)
```

## Canonical Commands

- **Lint & Unit Tests**: `.venv/bin/ruff check src/ tests/ scripts/ && .venv/bin/pytest tests/unit/ -v --strict-markers`
- **Full Test Suite**: `.venv/bin/pytest tests/ -v --strict-markers`
- **PR Quality Gate & Drift Diff & MCP Server**: `atruss check --sarif out.sarif.json --fail-on HIGH`, `atruss diff --baseline exports/t1 --target exports/latest`, `atruss mcp --exports-dir exports/latest`
- **5-Gate Agentic Workflow Validator**:
  - `.venv/bin/python scripts/validate_agent_workflow.py --spec specs/009-unified-atlas-spec`
  - `.venv/bin/python scripts/validate_agent_workflow.py --spec specs/006-core-unification-and-eval --output /tmp/eval-006.json`
- **Self-Healing 100-Repo Benchmark**: `.venv/bin/python scripts/run_benchmark_loop.py --corpus popular-100 --limit 12 --validate`
- **Astro Web Portal (Test & Build)**: `cd web && npm test && npm run build && ASTRO_SITE=https://kumarshaz.github.io ASTRO_BASE=/atruss-code-atlas npm run build`

## Code Style & Development Environment

- **Execution Environment**: Windows Subsystem for Linux (WSL) or Linux CI (`ubuntu-latest`).
- **Python**: Dependencies isolated within `.venv` at the repository root.
- **Node.js**: Managed via `fnm` pointing to Node.js v22+ (see `.agent/rules/headless-shell.md` for non-interactive shell invocations).
- **Agentic Workflow Skill**: `.agent/skills/horizon2-swarm/SKILL.md` defines Antigravity-native parallel disjoint wave execution + Grade `A` exit gates.
- **Architectural Tenets**:
  1. Policy-as-Code (`manifests/ecosystems.yaml`, `manifests/architecture-rules.yaml`, `manifests/pipeline-rules.yaml`)
  2. Single Source of Truth (`exports/latest/` JSON/YAML/CSV/MD/SBOM/SARIF/llms contracts)
  3. Strict Spec-Driven & Test-Driven Development enforced by the 5-Gate Validator (`Grade: A`, `0` skipped tests, `0` AST stubs/TODOs, 8-artifact determinism)
