# Phase 0: Research & Architecture Decisions

This file resolves the unknowns inherent in porting the tool strictly towards static outputs while validating via real-world monorepo fixtures.

## 1. Local execution without databases
- **Decision**: Purge any `SQLAlchemy` engine models or Celery job queues completely from the execution chain. Route all aggregated findings via Pydantic straight into native `json.dump()` outputs bound to the local `--output-dir`.
- **Rationale**: Constitution Version 2.0 perfectly isolates the execution context (NFR-POR-01). The file system naturally handles caching natively while guaranteeing the outputs can be uploaded directly to environments like Astro statically.
- **Alternatives considered**: Leaving SQLite in as a single-node metadata cache. Rejected because managing `.sqlite` state pollutes the directory bounds and violates the immutable file constraint mapping.

## 2. Test Harness: Public Pinned Fixtures
- **Decision**: Implement a native pytest fixture inside `tests/integration/` that strictly clones `--depth 1` against specific pinned SHAs for known public repositories (`github-samples/pets-workshop`).
- **Rationale**: Enforces Principle VII validation. If Microsoft changes the `pets-workshop` repository, the local integration bounds won't break since the SHA is immutable, guaranteeing purely deterministic architectural pipeline extraction tests.
- **Alternatives considered**: Mock arrays or local dummy strings. Rejected because they are insufficient for validating real multi-module topology scale.

## 3. Chained File Input Sourcing
- **Decision**: Extend `analyze-pipeline` and `analyze-code` Typer commands to parse `--repos-file` targeting a newline-delimited text string array.
- **Rationale**: DevOps workflows easily stream line separated arrays `cat repos.txt | xargs` or provide explicit text blocks. This simplifies CI/CD injections significantly better than complicated JSON manifest wrappers for targets you already know.
- **Alternatives considered**: JSON-only manifest ingest `(--from-discovery)`. Added `--repos-file` specifically to fulfill US3 fallback capabilities easily for hardcoded manual pipeline spans.
