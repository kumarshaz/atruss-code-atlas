# Phase 0: Research & Technology Decisions

## Language & Core Framework
- **Decision**: Python 3.12+ with FastAPI.
- **Rationale**: The PRD recommends Python tools (Radon, Bandit) alongside FastAPI and Celery. Python provides the best ecosystem for AST parsing and machine learning/orchestration bindings if needed later.
- **Alternatives considered**: Node.js, Go. Rejected because Python has superior native AST tooling (e.g., Radon) required for code analysis.

## Pipeline Parsing
- **Decision**: PyYAML + custom DAG builder using NetworkX.
- **Rationale**: GitHub Actions workflows are standard YAML. PyYAML is robust. NetworkX is the standard Python package for modeling directed acyclic graphs (DAGs) and detecting cycles or topological sorts.
- **Alternatives considered**: Custom recursive DAG parser. Rejected as NetworkX handles graph traversals and cycle detection natively.

## Local Architecture Analysis
- **Decision**: Multi-tool composition (Radon/Bandit for Python, ESLint/ts-morph output parsing for JS, PMD/SpotBugs output parsing for Java, Roslyn output for .NET).
- **Rationale**: Re-using established AST ecosystem tools is far more reliable and faster than writing native AST parsers for 4 distinct languages natively in Python.

## Storage
- **Decision**: PostgreSQL for metadata and analysis runs; JSON/S3 for canonical reports.
- **Rationale**: Relational DB perfectly models the GitRepository -> PipelineWorkflow relationships. Canonical reports might get large, so object storage is better.

## Task Queue / Orchestration
- **Decision**: Celery + Redis.
- **Rationale**: Deep analysis of 500k LoC repositories requires resilient asynchronous background job processing to meet the NFR performance goals (< 3 mins).
