# Implementation Plan: Structured Output Formats (GitHub Edition Migration)

**Branch**: `004-structured-output-formats` 
**Input**: Feature specification from `/specs/004-structured-output-formats/spec.md` + Reference ADO Python scripts

## Summary

This iteration vastly expands the structured output requirements to enforce a hierarchical, multi-format archival export mapping directly from ADO parity models. Instead of simply generating flat single-file outputs, the `discover` and `analyze-pipeline` CLI commands will now execute as comprehensive exporters running a strict 8-phase pipeline that dumps timestamped folder trees containing deterministic JSON, CSV, and YAML artifacts.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `httpx`, `asyncio`, `pyyaml`, `pydantic`
**Storage**: Local Filesystem (`exports/{timestamp}/...`)
**Testing**: `pytest`, `pytest-asyncio`, `pytest-httpx`
**Target Platform**: CLI / GitHub Actions Runners
**Project Type**: CLI
**Performance Goals**: Full run under 2 minutes for ~800 entities
**Constraints**: Zero database dependencies, offline-capable docs-as-code extraction, strict GitHub REST API rate limit awareness.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Single Source of Truth**: PASS (Extracts purely from GitHub API and YAML contents).
- **Performance**: PASS (Target <2m using async HTTP).
- **Tests**: PASS (Will rely on robust mocked httpx harnesses).
- **Architecture**: PASS (No databases, standard filesystem exports).

## Project Structure

### Documentation (this feature)

```text
specs/004-structured-output-formats/
├── plan.md              # This file
├── research.md          # Technical decisions for GitHub vs ADO parity
├── data-model.md        # Explicit CSV and JSON models defined by reference
├── quickstart.md        # CLI execution examples
├── contracts/cli.md     # Updated CLI arguments
└── tasks.md             # To be generated
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── auth.py          # Token validation and Bearer management
│   ├── http_client.py   # Async HTTP with Link pagination and rate limits
│   └── exporters/       # JSON, CSV, YAML output generators
├── models/
│   ├── discovery.py     # Repository, Ecosystem discovery models
│   └── topology.py      # Workflow, Run, Environment, RunnerGroup models
├── analyzers/
│   ├── classifiers/     # Activity, orphan, pattern extraction logic
│   └── pipeline/        # YAML parsing, DAG building
└── cli/
    ├── commands/
    │   ├── discover.py
    │   └── analyze_pipeline.py
    └── main.py
```

**Structure Decision**: A single project modular architecture cleanly segregating the generic GitHub async HTTP extraction logic from the core analytical classification rules and the deterministic filesystem exporters based on the 8-phase ADO parity models.
