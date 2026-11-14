# Research & Technical Decisions: GitHub Edition Orchestration

## Decision 1: Async HTTP vs Sync HTTP
**Decision**: `httpx.AsyncClient` + `asyncio.Semaphore(10)`
**Rationale**: ADO PowerShell implementation handled implicit job parallelization. To hit the < 2 minute performance requirement for 800+ repos while staying within secondary rate limits, a strongly controlled async barrier limits concurrent spikes preventing 403 blocks while vastly outperforming sequential `requests`.

## Decision 2: Pagination Model
**Decision**: RFC 5988 `Link` header tracking via `rel="next"`.
**Rationale**: GitHub does not use the `continuationToken` query concept native to ADO. Native Link header parsing represents the robust canonical standard for GH tree iterations.

## Decision 3: Export Hierarchy vs Flat Files
**Decision**: Directory based generation per run (`exports/{timestamp}/{resource}/...`) vs a single output file.
**Rationale**: The user explicit requirement specifies 8 granular export phases isolating repos, contents, workflows, runners, relationships, and reports into separate sub-domains retaining both CSVs for humans and hierarchical JSONs for visualizers like Astro automatically.

## Decision 4: Pipeline Layer Compression
**Decision**: Compress `Build -> Release` into a single `Workflow` entity.
**Rationale**: ADO utilized separated build systems and release (Classic) pipelines. GitHub Actions inherently merges these into unified YAML definitions, natively dropping a Mermaid subgraph layer and simplifying the data models into `Repo -> Workflow -> Environment -> Runner`.
