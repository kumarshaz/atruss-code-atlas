# Feature Specification: Portable Output Architecture & Strict Test Harness

**Feature Branch**: `003-portable-test-harness`  
**Created**: 2026-03-20  
**Status**: Draft  
**Input**: Re-architecting output flow for Docs-as-Code (Offline JSON + Markdown) without backend databases, and implementing rigid TDD fixture harnesses targeting real-world public repos like `pets-workshop`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Offline CLI Execution & Immutable Docs-as-Code Output (Priority: P1)

As a developer, I want to run the CLI locally and have it output byte-for-byte deterministic JSON and Markdown files directly to my filesystem, so that I can commit and host them statically in an Astro website without requiring databases.

**Why this priority**: Disconnecting the database and queues enables total portability and allows users to run pipelines natively inside existing CI/CD runners without external deployment architectures.

**Independent Test**: Can be fully tested by executing `repo-analyzer discover` and `analyze-pipeline` locally and asserting that outputs are pure files in `.json` and `.md` formats, with no Redis/PostgreSQL connections initiated.

**Acceptance Scenarios**:
1. **Given** a standard CLI invocation, **When** the analysis completes, **Then** all artifacts are dumped to the specified locally mapped `--output-dir` containing `analysis-result.json` and `report.md`.
2. **Given** a lack of network connection to any databases, **When** the CLI executes against a local git tree, **Then** it must succeed natively generating Markdown without failures.

---

### User Story 2 - Comprehensive Fixture Testing against Real Monorepos (Priority: P1)

As an automation engineer, I want the CLI test harness to run integratively against pinned SHAs of complex public repositories (e.g., `github-samples/pets-workshop`, `dotnet/eShop`, `Azure-Samples/todo-app-java-on-azure`), so that we can validate the pipeline DAG parsers and extraction logic against real-world chaos before shipping.

**Why this priority**: Relying entirely on dummy string comparisons masks real-world AST extraction failures. Using pinned public monorepos enforces the strictest standard of TDD validity.

**Independent Test**: Execute the Pytest integration suite locally. The suite must clone the pinned public repositories and assert the generated topological JSON accurately maps to known structures.

**Acceptance Scenarios**:
1. **Given** the Pytest suite execution, **When** testing the `pets-workshop` fixture, **Then** the engine correctly parses client, server, and content submodules.
2. **Given** the pipeline classifier test, **When** run against `Azure-Samples/todo-app-java-on-azure`, **Then** it successfully extracts Maven goals and Azure deployment bounds inside the DAG.

---

### User Story 3 - Chained Input Sourcing via Variable Lists (Priority: P2)

As a DevOps engineer, I want to pass a generic text file or manifest of target GitHub repositories to the analysis commands so that I can bypass the discovery phase entirely when I already know my targets.

**Why this priority**: Teams often have hardcoded subsets of active repositories they wish to scan explicitly without trusting the discovery bounds of an entire Organization's API page.

**Independent Test**: Create a generic `targets.json` or `.txt`, pass it via CLI args, and verify the pipeline successfully iterates and maps the specific targets.

**Acceptance Scenarios**:
1. **Given** a simple text file listing `org/repo1` and `org/repo2`, **When** provided to `analyze-pipeline --repos-file targets.txt`, **Then** the CLI clones exactly those two targets sequentially and processes them.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST output core analysis results natively as strictly-typed, immutable `.json` strings.
- **FR-002**: System MUST generate Arc42 Markdown `.md` reports natively containing standard ` ```mermaid ` AST DAG strings perfectly ingestible by static site generators.
- **FR-003**: System MUST NOT require active running services (FastAPI, Redis, Postgres) for basic local CLI execution. All extraction runs purely in-memory.
- **FR-004**: System MUST accept repository targets natively from a JSON discovery output `(--from-discovery)` OR a user-provided flat file list array `(--repos-file)`.
- **FR-005**: Test suite MUST execute against explicitly identified public GitHub repositories (including `.NET eShop` and `pets-workshop`) as test subjects by targeting pinned SHAs specifically to avoid continuous integration drift.

### Key Entities

- **PortableArtifact**: The unified filesystem package containing `{repo-hash}-analysis.json` and `{repo-hash}-report.md`.
- **HarnessFixture**: The pinned git signature pointing to exact states of public repo structures.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of integration tests pass natively on a completely clean local machine without requiring a docker-compose background stack (zero backend DBs).
- **SC-002**: Generated `.md` output files render successfully when parsed by standard Astro Content Collections without necessitating complex client-side React rendering hooks.
- **SC-003**: Analysis engines correctly parse `github-samples/pets-workshop` successfully classifying and mapping all submodules dynamically within < 3 minutes under CI workloads.
