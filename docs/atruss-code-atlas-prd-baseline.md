# Atruss Code Atlas: Baseline Product Requirements Document (v1.0 Baseline)

**Document ID**: `PRD-ATRUSS-BASELINE-V1`  
**Version**: `1.0.0-Baseline` (Pre-Iteration 2 Consolidation)  
**Date**: 2026-11-14  
**Status**: Baseline Reference (Superseded by [`docs/atruss-code-atlas-prd.md`](./atruss-code-atlas-prd.md))  
**Companion Specifications**: [`docs/atruss-code-atlas-unified-spec.md`](./atruss-code-atlas-unified-spec.md) & [`specs/009-unified-atlas-spec/spec.md`](../specs/009-unified-atlas-spec/spec.md)

---

## 1. Baseline Product Intent & Market Gap

**Product Intent**: Atruss Code Atlas is a passive, offline-capable architectural and CI/CD pipeline observability platform. It ingests GitHub organizations and repositories, performs structural classification, static code boundary extraction, and GitHub Actions workflow DAG analysis, and emits deterministic, portable Docs-as-Code artifacts (`JSON`, `CSV`, `YAML`, and `Arc42 Markdown` with `Mermaid` diagrams) rendered statically via an Astro Starlight web observatory.

### 1.1 Baseline Competitive Differentiation

| Competitor / Tool | Core Strength | Baseline Atruss Code Atlas Advantage |
| :--- | :--- | :--- |
| **SonarQube / SonarCloud** | AST-level code quality, cyclomatic complexity, security gates | Understands GitHub Actions DAGs and detects CI/CD pipeline anti-patterns (missing test gates, missing caches, unmasked secrets). |
| **GitHub Advanced Security (GHAS)** | Native dependency, secret, and CodeQL scanning | Outputs deterministic, portable offline Arc42 Markdown and JSON/CSV/YAML datasets rather than locking data in a SaaS UI. |
| **Spotify Backstage** | Developer portal and service cataloging | Passive zero-agent inspection; requires no repository instrumentation, webhooks, or YAML push agents. |
| **Datadog CI Visibility** | Real-time pipeline telemetry and flakiness tracking | Connects CI/CD workflow topology directly to repository structural architecture (API routes, services, data layers, UI components). |

### 1.2 Baseline Non-Negotiable Constitution (v2.1.0)

1. **I. Policy-as-Code & Extensibility**: All classification logic is externalized as YAML/JSON manifests (`manifests/ecosystems.yaml`)—never hardcoded in engine code.
2. **II. Single Source of Truth for Reports**: The canonical JSON export is the single source of truth; Markdown and Astro HTML views read exclusively from canonical exports.
3. **III. Security & Privacy First**: GitHub tokens are never persisted beyond the execution session and are masked across console and file loggers.
4. **IV. Performance & Scalability**: Repository analysis (`< 500k LoC`) completes in `< 3 minutes` (`180s` circuit breaker).
5. **V. Auditability**: Every export run is timestamped and logged with repository SHA and actor context.
6. **VI. Pipeline Visualization as a First-Class Feature**: GitHub Actions `.github/workflows/*.yml` DAG reconstruction and anti-pattern detection are core capabilities.
7. **VII. Strict Test and Specification Driven Development (SDD/TDD)**: Features follow SpecKit `spec.md -> plan.md -> tasks.md` workflows and test against pinned-SHA public repositories (`github-samples/pets-workshop`, `dotnet/eShop`, `Azure-Samples/todo-nodejs-mongo-terraform`, `hamvocke/spring-testing`).
8. **VIII. Standardized WSL Development Environment**: All Python (`.venv`) and Node.js (`fnm` v22+) workloads execute natively inside WSL/Linux.

---

## 2. Baseline Scope Boundary (Iterations 001–008)

- **In Scope (Baseline)**:
  - GitHub organization & repository ingestion (REST v3 `/orgs/{org}/repos`, `/git/trees/{sha}?recursive=1`, shallow `git clone --depth 1 --filter=blob:none`).
  - 4 Core Ecosystems: **Python**, **.NET**, **React / TypeScript / JavaScript**, and **Java Spring Boot**.
  - 27-column ADO-parity discovery manifest (`repositories.json`, `repositories.csv`, `repositories.yaml`).
  - GitHub Actions workflow DAG reconstruction (`jobs`, `needs:` edges, triggers) and 7 pipeline anti-pattern heuristics.
  - Structural code component extraction and Arc42 Markdown + Mermaid generation.
  - Astro 6 + Starlight + Material Design 3 static web observatory (`web/`) deployed to GitHub Pages.
  - 100-repo popular + stratified random public GitHub benchmark runner (`atruss benchmark`) and 5-Gate Agentic Workflow Validator (`scripts/validate_agent_workflow.py`).
- **Out of Scope in v1.0 Baseline**:
  - GitLab / Bitbucket / Azure DevOps native ingestion, real-time webhooks, IDE plugins, autonomous AI code modification of target repos.

---

## 3. Baseline Functional Requirements Summary

### 3.1 Ingestion & Discovery (`FR-ING-*`)

| ID | Baseline Requirement | Priority | Baseline Status (001–008) |
| :--- | :--- | :---: | :--- |
| **FR-ING-01** | Authenticate via optional Fine-Grained PAT / `GH_TOKEN` / `GITHUB_TOKEN` with dual-logger masking | P0 | Implemented (`001`, `004`) |
| **FR-ING-02** | Discover repositories by GitHub org (`--org`), discovery manifest (`--from-discovery`), flat file (`--repos-file`), or local path (`--path`) | P0 | Implemented (`001`–`006`) |
| **FR-ING-03** | Classify primary ecosystem and framework via externalized `manifests/ecosystems.yaml` | P0 | Implemented (`001`, `006`) |
| **FR-ING-04** | Support monorepos with mixed ecosystems by partitioning independent manifest-root submodules | P1 | Implemented (`001`, `006`) |
| **FR-ING-05** | Capture repository metadata, default branch, release activity, and 27-column ADO-parity signals via `/git/trees?recursive=1` | P0 | Implemented (`004`, `006`) |
| **FR-ING-06** | Index manifests (`requirements.txt`, `pyproject.toml`, `.sln`, `.csproj`, `package.json`, `tsconfig.json`, `pom.xml`, `build.gradle`) | P0 | Implemented (`001`, `006`) |
| **FR-ING-07** | Extract all `.github/workflows/*.yml` files (via API contents or shallow clone) | P0 | Implemented (`001`, `006`) |

### 3.2 Code & Coverage Analysis (`FR-ANA-*`)

| ID | Baseline Requirement | Priority | Baseline Status (001–008) |
| :--- | :--- | :---: | :--- |
| **FR-ANA-01** | Compute LoC / SLoC per module and language | P0 | Implemented (`006`) |
| **FR-ANA-02** | Compute Cyclomatic Complexity per function/method | P0 | Implemented for Python (`radon`), basic structural for others (`006`) |
| **FR-ANA-03** | Compute Cognitive Complexity per class/module | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-ANA-04** | Detect code duplication % via clone detection | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-ANA-05** | Detect dead code (unreachable / unused exports) | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-ANA-06** | Scan dependencies against vulnerability databases (CVE / OSV) | P0 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-ANA-07** | Detect hardcoded secrets via regex + entropy scan | P0 | Implemented for workflows (`006`); full repo scan in v2.0 PRD |
| **FR-ANA-08** | Detect outdated dependencies with upgrade paths | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-ANA-09** | Calculate test coverage % when test artifacts exist (`pytest`, `Jest`, `dotnet test`, `JaCoCo`) | P1 | Implemented (`001`, `coverage_parser.py`) |
| **FR-ANA-10** | Produce composite Technical Debt Score & 6-Dimension A–F Scorecard | P0 | Partial (Org maturity score in `006`; full 6-D scorecard in v2.0 PRD) |

### 3.3 Report Generation & Exporters (`FR-RPT-*`)

| ID | Baseline Requirement | Priority | Baseline Status (001–008) |
| :--- | :--- | :---: | :--- |
| **FR-RPT-01** | Produce canonical JSON, CSV, and YAML in timestamped `exports/{timestamp}/` and `exports/latest/` | P0 | Implemented (`003`, `004`, `006`) |
| **FR-RPT-02** | Render canonical JSON and Arc42 Markdown to static HTML via Astro Starlight + Material Design 3 | P0 | Implemented (`005`, `006`, `007`) |
| **FR-RPT-03** | Export HTML to PDF | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-RPT-04** | Executive Summary scorecard (A–F per dimension) | P0 | Partial (Addressed in v2.0 PRD) |
| **FR-RPT-05** | Dependency Tree with CVE annotations | P0 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-RPT-06** | Module Complexity Heatmap | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-RPT-07** | Findings Table (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`) | P0 | Implemented (`006`, `007`) |
| **FR-RPT-08** | Pipeline Topology section linking to visualization | P0 | Implemented (`004`, `006`, `007`) |
| **FR-RPT-09** | Version-stamp every report with repo SHA + analysis timestamp | P0 | Implemented (`003`, `006`) |

### 3.4 Pipeline Visualization (`FR-VIZ-*`)

| ID | Baseline Requirement | Priority | Baseline Status (001–008) |
| :--- | :--- | :---: | :--- |
| **FR-VIZ-01** | Parse `.github/workflows/*.yml` — extract jobs, steps, triggers, `needs:` | P0 | Implemented (`001`, `006`) |
| **FR-VIZ-02** | Render a DAG (`jobs` = nodes, `needs:` = directed edges) | P0 | Implemented (`001`, `006`, `007`) |
| **FR-VIZ-03** | Each node displays job name, runner, step count (and run status when available) | P0 | Implemented (`006`, `007`) |
| **FR-VIZ-04** | Color-code nodes and severity badges using semantic tokens | P0 | Implemented (`007`) |
| **FR-VIZ-05** | Correctly render parallel vs. sequential job chains | P0 | Implemented (`001`, `006`) |
| **FR-VIZ-06** | Detect all 7 baseline pipeline anti-patterns (`NO_TEST_GATE`, `NO_CACHE`, `NO_ARTIFACT_HANDOFF`, `HARDCODED_SECRET`, `SEQUENTIAL_ONLY`, `UNFILTERED_MAIN_PUSH`, `UNLABELED_SELF_HOSTED`) | P1 | Implemented (`001`, `006`) |
| **FR-VIZ-07** | Interactive zoom/pan on DAG in web UI | P1 | Implemented (`007`) |
| **FR-VIZ-08** | Export DAG as SVG or PNG | P1 | Deferred in Baseline (Addressed in v2.0 PRD) |
| **FR-VIZ-09** | Show trigger conditions (`push`, `pull_request`, `schedule`, `workflow_dispatch`) as metadata | P0 | Implemented (`006`, `007`) |
| **FR-VIZ-10** | Detect `workflow_call` / `workflow_run` cross-workflow dependencies as cross-graph edges | P1 | Partial in topology model (`004`); full cross-graph edges in v2.0 PRD |
