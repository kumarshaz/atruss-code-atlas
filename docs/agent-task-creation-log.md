# Agent Decision Making: Task Creation Log

## Context
**Feature**: 001-repo-analyzer
**Input Sources**: `spec.md`, `plan.md`, `data-model.md`, `contracts/cli.md`

## Phase 1: Setup
**Decision**: Standardize on Python project fundamentals.
**Why**: The PRD and plan explicitly specify Python 3.12, pytest, and standard tooling. Getting the `requirements.txt` and `pyproject.toml` established ensures all subsequent phases have a working environment without dependency hell.
**Tasks Created**: Project init, linter config.

## Phase 2: Foundational Elements
**Decision**: Database ORM (SQLAlchemy) and Queue (Celery) must precede any User Story.
**Why**: All three User Stories rely either heavily on database persistence (`discovery` saves to DB, `pipeline analysis` saves findings, `deep analysis` saves architecture components) or Celery task offloading to meet the strict 3-minute SLA (FR-004 style constraints). If we start user stories before configuring Alembic/SQLAlchemy or Celery/Redis, we will end up with spaghetti code that can't be gracefully tested. 
**Tasks Created**: SQLAlchemy base setup, Alembic init, Celery worker scaffolding.

## Phase 3: User Story 1 (Discover and Classify)
**Decision**: Split the core algorithm (manifest classification) from the network logic (GitHub API) and the interface (CLI).
**Why**: This allows testability. The `manifest-based classification` engine is a strict requirement for Policy-as-Code. By isolating it as a pure function task, we can parallelize unit tests for it without needing a live GitHub API token.
**Tasks Created**: DB Migrations for `GitRepository`, GitHub API client (handling optional PAT auth), classification engine, and finally the `repo-analyzer discover` CLI command.

## Phase 4: User Story 2 (Analyze Pipelines)
**Decision**: Isolate the YAML parser, the DAG Graph engine (NetworkX), and the Anti-pattern heuristics.
**Why**: Parsing `.github/workflows` to JSON is straightforward, but traversing it as a graph to determine dependencies (`needs:`) requires NetworkX. Defining these as three separate tasks allows one developer to write anti-pattern heuristics (like "missing test gate") while another implements the NetworkX edge creation.
**Tasks Created**: DB Migrations for `Pipeline*` entities, YAML Parser Service, NetworkX DAG Builder, Anti-pattern detection, and the CLI command. Included parallel test tasks.

## Phase 5: User Story 3 (Deep Analysis)
**Decision**: Build the Arc42 generator sequentially *after* the AST wrapper.
**Why**: You cannot generate a documentation diagram if the extraction engine doesn't reliably output structured Data Access Layer and API route JSON. The AST wrapper (Radon/Bandit) is the hard prerequisite here. We also added an explicit task for the graceful-skip logic to handle C++/Ruby/Go codebases per the MVP constraint.
**Tasks Created**: DB Migrations for `ArchitectureComponent`, Python AST wrapper logic, graceful skip logic, Arc42/Mermaid Document Generator, and the CLI command.

## Phase 6: Polish
**Decision**: Docs and CI.
**Why**: The standard wrapper for MVP delivery. Ensuring a `quickstart.md` works and the project itself runs CI tests.
