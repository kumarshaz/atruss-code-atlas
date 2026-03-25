# atruss-code-atlas Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-24

## Active Technologies
- Python 3.10+ + `subprocess` (built-in), `tempfile` (built-in), `json` (built-in) (002-chain-analysis)
- OS Temporary Filesystem (`tempfile.gettempdir()`) (002-chain-analysis)
- Python 3.12+ + Typer (CLI), NetworkX (DAGs), Pytest (Harness) *(Explicitly excluding Celery, Redis, FastAPI, PostgreSQL)* (003-portable-test-harness)
- Native Local Filesystem (Static `.json` and `.md`) (003-portable-test-harness)
- Python 3.11+ + `json` (stdlib), `csv` (stdlib), `pyyaml` (existing), `pydantic` (for models/schemas) (004-structured-output-formats)
- Local Filesystem (`--output-dir`) (004-structured-output-formats)

- Python 3.12 + FastAPI, Celery, Redis, PyYAML, NetworkX, SQLAlchemy, external analyzers (Radon, Bandit) (001-repo-analyzer)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.12: Follow standard conventions

## Recent Changes
- 004-structured-output-formats: Added Python 3.11+ + `json` (stdlib), `csv` (stdlib), `pyyaml` (existing), `pydantic` (for models/schemas)
- 003-portable-test-harness: Added Python 3.12+ + Typer (CLI), NetworkX (DAGs), Pytest (Harness) *(Explicitly excluding Celery, Redis, FastAPI, PostgreSQL)*
- 002-chain-analysis: Added Python 3.10+ + `subprocess` (built-in), `tempfile` (built-in), `json` (built-in)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
