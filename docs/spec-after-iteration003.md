# Atruss Code Atlas: Combined Product Specification (Post-Iteration 003)

**Version**: 1.0  
**Date**: 2026-03-20  
**Status**: Complete (Iterations 001–003)

---

## 1. The Market Gap & Value Proposition

Enterprises are suffering from architectural drift and pipeline fragmentation. Developers are acting as "Master Blacksmiths," hand-crafting CI/CD workflows and hiding domain logic in undocumented repositories.

**The Gap:** Existing tools lock data behind proprietary SaaS UIs (GHAS, Sonar) or require heavy, active instrumentation (Backstage). Nothing passively reads a repository and its CI/CD workflows to output a deterministic, portable, Docs-as-Code artifact (Arc42 + Mermaid DAGs).

**The Atruss Code Atlas Value Proposition:** Passive, offline-capable architectural and pipeline observability. It tells you exactly *what* is being built (structural architecture) and *how* it gets to production (pipeline topology) without requiring a single agent or webhook.

### Competitive Differentiation

| Competitor | Core Strength | Atruss Code Atlas Gap |
| :--- | :--- | :--- |
| **SonarQube** | Deep AST-level code quality and security gates. | **Blind to CI/CD pipelines.** Cannot detect pipeline anti-patterns (missing cache, test gates). |
| **GitHub Advanced Security (GHAS)** | Native dependency/secret/code scanning. | **Zero portability.** Data locked in GitHub UI. No offline Arc42 generation. |
| **Backstage (Spotify)** | Developer portal and service cataloging. | **Heavy active integration.** Services must push data. Atruss is *passive*. |
| **Datadog CI Visibility** | Real-time pipeline telemetry. | **No architectural context.** Knows a job failed, not if it's DDD or a React SPA. |

**Differentiator:** Atruss Code Atlas is the only tool bridging **Structural Architecture** (DDD, CQRS, Hexagonal patterns) with **Pipeline Topology** (Action DAGs) and outputting it as an **immutable, portable artifact** (JSON + Markdown/Mermaid).

---

## 2. Target Architecture (Hexagonal / Ports & Adapters)

The Python engine enforces strict boundaries to support future expansions (Astro-based UI, enterprise API):

* **Core Domain:** Immutable classification rules. Handles AST parsing, DAG reconstruction, pattern matching, and pipeline anti-pattern detection. Zero knowledge of external systems.
* **Inbound Ports:**
  * `CLIAdapter`: Local developer execution and CI/CD runner integration.
  * `FastAPIAdapter` *(Future)*: Enterprise-level asynchronous scanning orchestration.
* **Outbound Adapters:**
  * `GitHubRESTClient` / `GitHubGraphQLClient`: Fetches raw repository state.
  * `JSONExporter` / `MarkdownExporter`: Generates deterministic canonical output and Arc42/Mermaid files.

---

## 3. Feature Summary by Iteration

### Iteration 001: Repository Discovery & Deep Analysis

> **Scope:** Core CLI, ecosystem classification, pipeline DAG extraction, deep code analysis, and coverage extraction.

### Iteration 002: Chained Analysis Pipeline

> **Scope:** Automated cloning from discovery JSON, eliminating manual `git clone` steps at organizational scale.

### Iteration 003: Portable Output Architecture & Strict Test Harness

> **Scope:** Removal of all backend services (FastAPI, Celery, Redis, PostgreSQL). Pure offline JSON + Markdown file output. TDD test harness using pinned public GitHub repositories. `--repos-file` array input support.

---

## 4. User Stories (Combined)

### US-001: Discover and Classify Repositories *(P1 — Iteration 001)*

As an engineering leader, I want to scan a GitHub organization to discover all repositories and classify each by its primary ecosystem, framework, and deployment patterns, so I maintain visibility over our technology landscape.

**Acceptance Criteria:**
1. All accessible repositories are listed with detected ecosystem and framework.
2. Monorepos are separated into independent module units based on manifest resolution rules.

---

### US-002: Analyze CI/CD Pipelines *(P1 — Iteration 001)*

As a DevOps engineer, I want to analyze `.github/workflows` to construct a visual DAG of the deployment process, so I can identify workflows, missing test gates, and pipeline anti-patterns.

**Acceptance Criteria:**
1. A visual DAG is generated matching the structure defined by `needs:` directives.
2. A "No test gate before deploy" anti-pattern flag is raised when applicable.

---

### US-003: Deep Local Code Analysis *(P2 — Iteration 001)*

As a software architect, I want to execute deep analysis on a cloned repository to extract architecture patterns, API endpoints, and data access layers, and auto-generate Arc42 Markdown with Mermaid diagrams.

**Acceptance Criteria:**
1. Key architectural boundaries and API endpoints are identified.
2. Arc42 compliant Markdown is produced with a Mermaid diagram of data and control flow.

---

### US-004: Extract Test Coverage *(P2 — Iteration 001)*

As an engineering manager, I want to automatically extract the test coverage percentage from CI/CD pipeline artifacts, so I can track testing health alongside the pipeline DAG.

**Acceptance Criteria:**
1. Coverage metric is accurately extracted (±2% tolerance) from pytest/Jest/dotnet test/Jacoco run logs or artifacts.

---

### US-005: Chained Code Analysis *(P1 — Iteration 002)*

As a security reviewer, I want to feed discovery JSON directly into the deep code analyzer so I don't have to manually clone 100+ repositories to analyze their architectures.

**Acceptance Criteria:**
1. All repositories in the JSON are cloned locally, analyzed, and a Markdown architecture report is generated for each.
2. Clone failures are logged and the analysis gracefully skips to the next repository.

---

### US-006: Chained Pipeline Analysis *(P1 — Iteration 002)*

As a DevSecOps engineer, I want to feed discovery JSON directly into the pipeline analyzer to check GitHub Actions workflows globally across all repos.

**Acceptance Criteria:**
1. The tool clones repos and extracts the workflow DAG for each entry in the discovery manifest.

---

### US-007: Offline CLI Execution & Immutable Docs-as-Code Output *(P1 — Iteration 003)*

As a developer, I want to run the CLI locally and have it output byte-for-byte deterministic JSON and Markdown files directly to my filesystem, so I can commit and host them statically without databases.

**Acceptance Criteria:**
1. All artifacts are dumped to `--output-dir` containing `analysis-result.json` and `report.md`.
2. The CLI succeeds natively generating Markdown without Redis/PostgreSQL connections.

---

### US-008: Comprehensive Fixture Testing against Real Monorepos *(P1 — Iteration 003)*

As an automation engineer, I want the test harness to run against pinned SHAs of complex public repositories (e.g., `github-samples/pets-workshop`, `Azure-Samples/todo-nodejs-mongo-terraform`), so we validate extraction logic against real-world chaos.

**Acceptance Criteria:**
1. `pets-workshop` fixture correctly parses client, server, and content submodules.
2. `todo-nodejs-mongo-terraform` correctly extracts pipeline and deployment bounds inside the DAG.

---

### US-009: Chained Input Sourcing via Variable Lists *(P2 — Iteration 003)*

As a DevOps engineer, I want to pass a generic text file of target repositories to analysis commands, so I can bypass discovery entirely when I already know my targets.

**Acceptance Criteria:**
1. CLI clones exactly the targets listed in `--repos-file targets.txt` sequentially and processes them.

---

## 5. Consolidated Functional Requirements

| ID | Requirement | Iteration |
| :--- | :--- | :---: |
| **FR-001** | CLI to discover and list repositories for a GitHub org, user, or topic filter. | 001 |
| **FR-002** | Classify each repository's language, framework, and deployment patterns via extensible manifests. | 001 |
| **FR-003** | Optional PAT authentication (GITHUB_TOKEN) for GitHub API rate limits; operate unauthenticated for small public scans. | 001 |
| **FR-004** | Parse `.github/workflows/*.yml` to extract job definitions, steps, triggers, and dependencies. | 001 |
| **FR-005** | Construct and visualize a Directed Acyclic Graph (DAG) for pipeline workflows. | 001 |
| **FR-006** | Flag CI/CD anti-patterns: untested deployments, missing caching, unmasked secrets. | 001 |
| **FR-007** | Deep static code analysis on cloned local codebases to extract architecture components for supported ecosystems. Gracefully skip unsupported ecosystems. | 001 |
| **FR-008** | Generate Arc42 standard documentation with embedded Mermaid syntax diagrams. | 001 |
| **FR-009** | Extract and calculate test coverage percentage from pipeline artifacts. | 001 |
| **FR-010** | `discover` command outputs JSON array to file when `--output` is provided. | 002 |
| **FR-011** | `analyze-code` and `analyze-pipeline` accept `--from-discovery <file.json>` flag. | 002 |
| **FR-012** | Iterate through discovery JSON array, extracting `clone_url` and `name` per repository. | 002 |
| **FR-013** | Automatically clone each remote repository to the OS temporary directory for isolated runs. | 002 |
| **FR-014** | Utilize existing Git credentials (GITHUB_TOKEN or SSH) for remote clones. | 002 |
| **FR-015** | Output analysis results natively as strictly-typed, immutable `.json` files. | 003 |
| **FR-016** | Generate Arc42 Markdown `.md` reports with standard mermaid blocks ingestible by static site generators. | 003 |
| **FR-017** | Must NOT require active running services (FastAPI, Redis, Postgres) for basic CLI execution. | 003 |
| **FR-018** | Accept repository targets from `--from-discovery` OR `--repos-file` (flat text list). | 003 |
| **FR-019** | Test suite must execute against pinned SHA public GitHub repositories to avoid CI drift. | 003 |

---

## 6. Key Entities (Domain Model)

| Entity | Description | Introduced |
| :--- | :--- | :---: |
| **GitRepository** | Provider-agnostic Git repository metadata: primary ecosystem, commit health, module structure. | 001 |
| **PipelineWorkflow** | Formalized CI/CD execution pipeline grouping Jobs and their `needs:` dependency edges. | 001 |
| **ArchitectureComponent** | Discovered code structure: API ingest points, data access boundaries. | 001 |
| **AntiPatternFinding** | Identified risk within a workflow/architecture: severity and nature of infraction. | 001 |
| **DiscoveryManifest** | JSON array schema: `[{"name": "...", "clone_url": "...", "ecosystem": "..."}]`. | 002 |
| **PortableArtifact** | Unified filesystem package: `{repo-hash}-analysis.json` + `{repo-hash}-report.md`. | 003 |
| **HarnessFixture** | Pinned git signature pointing to exact states of public repo structures for TDD. | 003 |

---

## 7. Non-Functional Requirements

| ID | Directive | Business Alignment |
| :--- | :--- | :--- |
| **NFR-DET-01** | **Strict Determinism:** Running twice on the same Git SHA must produce byte-for-byte identical JSON and Markdown. | Auditability; prevents noise in Docs-as-Code workflows. |
| **NFR-POR-01** | **Total Portability:** Core engine runs locally without a database. All outputs are static files. | Offline-capable, air-gapped, or pre-PR local execution. |
| **NFR-PERF-01** | **Execution Speed:** Analysis of a repo under 500k LoC must complete in under 3 minutes. | Embeddable directly into CI/CD pipelines without bottlenecking. |
| **NFR-EXT-01** | **Schema First:** JSON schema is the contract. Any UI must read only from JSON, never from engine memory. | Decoupling; UI can be rewritten without touching the core engine. |

---

## 8. Success Criteria (Combined)

| ID | Criteria | Iteration |
| :--- | :--- | :---: |
| **SC-001** | Discover and classify up to 100 repositories in under 2 minutes. | 001 |
| **SC-002** | Pipeline DAGs correctly visualize 100% of defined sequential and parallel jobs. | 001 |
| **SC-003** | Deep analysis on repos under 500k LoC produces Arc42 docs in under 3 minutes. | 001 |
| **SC-004** | Pipeline anti-patterns produce fewer than 5% false positives. | 001 |
| **SC-005** | Test coverage extraction is accurate within ±2% tolerance. | 001 |
| **SC-006** | Full org discovery → code analysis runs without manual `git clone`. | 002 |
| **SC-007** | Tool handles 50+ repository scaling without disk exhaustion or unhandled exceptions. | 002 |
| **SC-008** | 100% of integration tests pass on a clean machine without docker-compose. | 003 |
| **SC-009** | Generated `.md` renders successfully in Astro Content Collections. | 003 |
| **SC-010** | `pets-workshop` correctly parsed with all submodules in under 3 minutes. | 003 |

---

## 9. Astro Visualizer Architecture (Future)

The output is designed for Astro Static Site Generation:
1. **Python Engine (Generator):** Outputs `analysis-result.json` and `report.md` with embedded mermaid blocks.
2. **Astro Content Collections (Consumer):** Reads the output folder directly at build time.
3. **Mermaid Rendering:** Use `rehype-mermaid` at build time or inject lightweight `mermaid.js` globally.
4. **Static Output:** `astro build` produces pure HTML/CSS/SVG deployable on GitHub Pages, S3, or on-prem Nginx.

> **Red Flag:** Do not build a heavy React/Vite SPA inside Astro to parse `analysis-result.json` on the client side. That defeats the purpose of Docs-as-Code portability.
