# Implementation Plan: Repository Discovery and Deep Analysis

**Branch**: `001-repo-analyzer` | **Date**: 2026-03-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-repo-analyzer/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. 

## Summary

Implement a CLI-driven backend system to discover Git repositories, parse their CI/CD pipelines (DAG generation), extract test coverage metrics, and perform deep static architecture code analysis for supported ecosystems. The technical approach leverages Python 3.12 with FastAPI for orchestration, Celery/Redis for background processing, and PostgreSQL for metadata storage, satisfying performance constraints on repos up to 500k LoC.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: FastAPI, Celery, Redis, PyYAML, NetworkX, SQLAlchemy, external analyzers (Radon, Bandit)  
**Storage**: PostgreSQL (metadata), local filesystem (reports)  
**Testing**: pytest  
**Target Platform**: CLI / Docker Container
**Project Type**: cli
**Performance Goals**: < 2 mins for 100 repo classification; < 3 mins for 500k LoC deep analysis  
**Constraints**: 10 concurrent analyses scale  
**Scale/Scope**: MVP focusing strictly on public git repositories with provider-agnostic core  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Policy-as-Code & Extensibility**: Passed. Manifest-based classification is inherent to the data model.
- **Single Source of Truth**: Passed. Postgres acts as the canonical representation for Arc42 generation.
- **Security & Privacy First**: Passed. Optional PAT auth designed strictly for rate limits; ephemeral.
- **Performance & Scalability**: Passed. Celery + Redis ensures strict concurrency controls (10 limit) to meet the 3-minute SLA circuit breaker.
- **Auditability**: Passed (schema logs).
- **Pipeline Visualization**: Passed. Node/Edge DAG schema defined directly in data-model.md.

## Project Structure

### Documentation (this feature)

```text
specs/001-repo-analyzer/
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entities schema
├── quickstart.md        # Local setup
├── contracts/           # CLI definitions
└── tasks.md             # (To be created via /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── models/
│   └── services/
├── cli/
│   └── commands/
├── analyzers/
│   ├── pipeline/
│   └── code/
└── api/

tests/
├── unit/
└── integration/
```

**Structure Decision**: Selected a modular single-project layout that isolates `cli/` from `analyzers/` and `core/` to ensure the project can migrate to a full web app wrapper (`api/`) later if desired.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-language analysis | Extracting architecture metrics requires AST | Simple regex analysis is incredibly fragile and yields unacceptable false positives. |
