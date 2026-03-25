
# Atruss Code Atlas: Product Requirement Specification (v1.0-Core)

## 1. The Market Gap & Value Proposition
Enterprises are suffering from architectural drift and pipeline fragmentation. Developers are acting as "Master Blacksmiths," hand-crafting CI/CD workflows and hiding domain logic in undocumented repositories. 

**The Gap:** Existing tools lock data behind proprietary SaaS UIs (GHAS, Sonar) or require heavy, active instrumentation (Backstage). Nothing passively reads a repository and its CI/CD workflows to output a deterministic, portable, Docs-as-Code artifact (Arc42 + Mermaid DAGs).

**The Atruss Code Atlas Value Proposition:** Passive, offline-capable architectural and pipeline observability. It tells you exactly *what* is being built (structural architecture) and *how* it gets to production (pipeline topology) without requiring a single agent or webhook.



###  Market Gap Analysis: Why Build Atruss Code Atlas?

If a stakeholder asks, *"Why aren't we just using SonarQube?"*, you need a bulletproof answer. Here is the technical market gap.

| Competitor / Tool | Core Strength | The Missing Link (The Atruss Code Atlas Gap) |
| :--- | :--- | :--- |
| **SonarQube / SonarCloud** | Deep AST-level code quality, cyclomatic complexity, and security gates. | **Blind to CI/CD pipelines.** It doesn't understand the GitHub Actions DAG, nor does it detect pipeline anti-patterns (e.g., missing cache, missing test gates). |
| **GitHub Advanced Security (GHAS)** | Native dependency scanning, secret scanning, and code scanning (CodeQL). | **Zero portability.** Data is locked in the GitHub UI. It cannot generate deterministic, offline Arc42 Markdown documentation. |
| **Backstage (Spotify)** | Excellent developer portal and service cataloging. | **Requires heavy active integration.** Services must push data to it. Atruss Code Atlas is *passive*—it ingests, analyzes, and reports without altering the target repo. |
| **Datadog CI Visibility** | Real-time telemetry on pipeline execution times and flakiness. | **No architectural context.** It knows a job failed, but it doesn't know if the project is a .NET Worker Service using CQRS or a React SPA. |

**The Atruss Code Atlas Differentiator:** Atruss Code Atlas is the only tool bridging **Structural Architecture** (detecting patterns like DDD, CQRS, Hexagonal Ports & Adapters) with **Pipeline Topology** (Action DAGs) and outputting it as an **immutable, portable artifact** (JSON + Markdown/Mermaid).

---

## 2. Target Architecture (Hexagonal / Ports & Adapters)
To ensure the Python engine remains a rigid skeleton that can support future expansions (like an Astro-based UI or an enterprise API), the system must enforce strict boundaries.

* **Core Domain (The "Lego" Logic):** The immutable rules of classification. This handles AST parsing, DAG reconstruction, pattern matching (e.g., detecting CQRS, DDD, or Hexagonal patterns in the target repo), and pipeline anti-pattern detection. It has zero knowledge of GitHub or Astro.
* **Inbound Ports (The Interfaces):** * `CLIAdapter`: For local developer execution and CI/CD runner integration.
    * `FastAPIAdapter` (Future): For orchestrating asynchronous scanning at an enterprise level.
* **Outbound Adapters (The "Modular Joints"):**
    * `GitHubRESTClient` / `GitHubGraphQLClient`: Fetches the raw state.
    * `JSONExporter` / `MarkdownExporter`: Generates the deterministic canonical output and the Arc42/Mermaid files.

## 3. Core Functional Requirements (The "Lego Slices")

### Slice 1: Ecosystem Ingestion & Classification
The system must automatically classify and parse the "Big Four" ecosystems.
* **.NET (C# 10+):** Deep inspection via Roslyn/AST. Must detect project types (WebApi, Worker Service, UI), data access patterns, and internal NuGet feed usage.
* **React/TypeScript:** AST-level analysis via ESLint/ts-morph. Must detect state management, component hierarchies, and strict linting/formatting standards.
* **Python:** Framework detection (FastAPI, Django), dependency analysis, and quality indicators (pytest, ruff).
* **Java Spring Boot:** Maven/Gradle parsing, Spring Web/Data JPA detection, and test coverage mapping.

### Slice 2: Pipeline Topology (DAG) Reconstruction
* Parse all `.github/workflows/*.yml`.
* Map `jobs` and `needs` into a Directed Acyclic Graph (DAG).
* Detect pipeline anti-patterns (e.g., no test gate before deploy, missing artifact handoffs).
* Output the DAG as a standard `graph LR` Mermaid string.

### Slice 3: The Portable Output Engine (Docs-as-Code)
* **Canonical Source of Truth:** A strictly typed `analysis-result.json`.
* **Visual Artifacts:** Auto-generate Arc42 Markdown files with embedded Mermaid diagrams representing Context, Deployment, and Pipeline Topology.
* **Astro Readiness:** The Markdown output must be entirely self-contained so it can be ingested natively by Astro Content Collections for a static, zero-JS visualizer.

## 4. Non-Functional Requirements (The Constitution)

| NFR | Directive | Business Alignment |
| :--- | :--- | :--- |
| **NFR-DET-01** | **Strict Determinism:** Running CodeLens twice on the same Git SHA must produce byte-for-byte identical JSON and Markdown. | Ensures auditability and prevents noise in Git-backed Docs-as-Code workflows. |
| **NFR-POR-01** | **Total Portability:** The core engine must run locally without a database. All outputs must be static files. | Allows teams to run it offline, in air-gapped environments, or locally before a PR. |
| **NFR-PERF-01** | **Execution Speed:** Analysis of a repository under 500k LoC must complete in under 3 minutes. | Ensures it can be embedded directly into standard CI/CD pipelines without bottlenecking deployments. |
| **NFR-EXT-01** | **Schema First:** The JSON schema is the contract. Any Astro UI or PDF generator must read *only* from the JSON, never from the Python engine memory. | Enforces decoupling; allows the UI to be rewritten or replaced ("plastic surgery") without touching the core engine. |


### 2. The Astro Visualizer Architecture (Portability First)

You want portability via Markdown and embedded Mermaid. Astro is an excellent choice for this because it is a Static Site Generator (SSG) that ships zero JavaScript by default. 

**Red Flag:** Do not build a heavy React/Vite SPA inside Astro to parse the `analysis-result.json` on the client side. That defeats the purpose of "Docs-as-Code" portability.

**The "Lego" Approach for Astro:**
1. **The Python Engine (The Generator):** Your Python tool runs the analysis and outputs two things into an `./output` folder:
    * `analysis-result.json` (The raw facts).
    * `report.md` (The Arc42 document with standard ` ```mermaid ` blocks).
2. **Astro Content Collections (The Consumer):** Astro reads the `./output` folder directly at build time using its native Content Collections API.
3. **Mermaid Rendering:** * Do not use generic React wrappers for Mermaid. 
    * Use a rehype plugin (like `rehype-mermaid`) in your `astro.config.mjs` to render the SVG *at build time* on the server, or inject the lightweight `mermaid.js` script globally and let it parse `<pre class="mermaid">` tags on load.
4. **Static Output:** Run `astro build`. The output is pure HTML/CSS/SVG. You can host this on GitHub Pages, S3, or an on-prem Nginx server. 

---

