# Atruss Code Atlas — Documentation & Specification Index

Welcome to the canonical documentation hub for **Atruss Code Atlas**. This directory houses the authoritative product requirements, unified SpecKit specifications, and agentic engineering governance guides for the platform.

---

## Document Lineage & Architecture Map

```mermaid
flowchart LR
    accTitle: Atruss Code Atlas Documentation and Specification Lineage
    accDescr: Diagram connecting the Baseline PRD v1.0, Master PRD v2.0, Unified SpecKit Specification (009), Plan/Tasks, Agentic SDLC Playbook, Research Plan, Metrics Methodology, and the 372-repository 10-ecosystem portal build pipeline.
    Baseline["Baseline PRD v1.0<br/>(atruss-code-atlas-prd-baseline.md)<br/>Iterations 001 - 008 Foundation"]
    MasterPRD["Consolidated Master PRD v2.0<br/>(atruss-code-atlas-prd.md)<br/>001-008 Lineage + Top 10 Roadmap (REC-01..10)"]
    UnifiedSpec["Unified SpecKit Specification<br/>(atruss-code-atlas-unified-spec.md &<br/>specs/009-unified-atlas-spec/spec.md)<br/>US1-US13 | FR-001..FR-030 | SC-001..SC-010"]
    PlanTasks["Unified Plan, Tasks & 5-Gate Validator<br/>(specs/009-unified-atlas-spec/{plan,tasks}.md)<br/>T001-T020 [x] Baseline | T021-T030 [x] Horizon 2"]
    SDLCGuide["Agentic SDLC Playbook<br/>(agentic-sdlc-guide.md)<br/>QRSPI · SDD · Harness Engineering · Swarm"]
    ResearchPlan["SDLC Research & Update Plan<br/>(agentic-sdlc-research-and-update-plan.md)<br/>RPI -> QRSPI · Guides & Sensors"]
    Metrics["Metrics & Scoring Methodology<br/>(metrics-methodology.md)<br/>6-D A-F Formulas · Maturity · Complexity · AP-001..014"]
    NativeFlows["10-Ecosystem Corpus & Astro 6 Portal<br/>(372-Repo Corpus · orgs-summary.json<br/>Mermaid v12 ELK · GitHub Actions CI/CD)"]

    Baseline -->|"Evolution & Top 10 Enhancements"| MasterPRD
    MasterPRD -->|"Executable Requirements Translation"| UnifiedSpec
    UnifiedSpec -->|"1:1 FR & Module Traceability"| PlanTasks
    MasterPRD -->|"Transparent Math & Rule Contracts"| Metrics
    SDLCGuide -.->|"Governs & Validates"| PlanTasks
    ResearchPlan -.->|"Upgrades & Tracks"| SDLCGuide
    PlanTasks -->|"Parallel Subagent Swarms"| NativeFlows
```

---

## 1. Core Product & Specification Documents (`docs/`)

| Document | Objective & Scope | Target Audience |
| :--- | :--- | :--- |
| **[`atruss-code-atlas-prd-baseline.md`](./atruss-code-atlas-prd-baseline.md)**<br/>*(Baseline PRD v1.0)* | Preserves the clean **v1.0 Baseline Product Requirements Document** representing the foundational capabilities delivered across Iterations `001` through `008` (27-column discovery, structural code analysis, pipeline DAG extraction, `AP-001`–`AP-007` heuristics, 6-Dimension A–F Scorecard, Material Design 3 Astro Starlight portal, and 100-repo benchmark). | Product Managers, Architects, Auditors establishing baseline vs. v2.0 delta |
| **[`atruss-code-atlas-prd.md`](./atruss-code-atlas-prd.md)**<br/>*(Consolidated Master PRD v2.0)* | The **authoritative single-source-of-truth Master PRD (v2.0)**. Consolidates:<br/>1. Executive vision, market gap analysis, and **Constitution v2.1.0** principles.<br/>2. Forensic specification lineage audit across all `001`–`008` `Spec -> Plan -> Task` tracks.<br/>3. **Top 10 Strategic Industry & Forum Recommendations (`REC-01`–`REC-10`)** across Backend, Code Structure, and Frontend.<br/>4. Complete Functional Requirements catalog, **14-Rule Anti-Pattern Matrix (`AP-001`–`AP-014`)**, **6-Dimension A–F Scorecard** mathematical formulas, NFRs, and the **v2.1–v2.3 Delivery Architecture**. | Executives, Product Owners, Principal Architects, Tech Leads, DevOps & Security Leads |
| **[`atruss-code-atlas-unified-spec.md`](./atruss-code-atlas-unified-spec.md)**<br/>*(Unified SpecKit Specification)* | Collates every requirement from the Baseline PRD and Master PRD v2.0 into a strict, executable **SpecKit-style Feature Specification**:<br/>- **13 Prioritized User Stories (`US1`–`US13`)** with independent test criteria and Given/When/Then acceptance scenarios.<br/>- **Boundary & Edge Case Specifications** (cyclic graphs, dynamic imports, air-gapped OSV/NVD lookups, `>500`-node topologies).<br/>- **30 Testable Functional Requirements**: `FR-001`–`FR-020` (Delivered Baseline `001`–`008`) and `FR-021`–`FR-030` (Delivered Horizon 2 Top 10 Enhancements).<br/>- **Key Domain Entities** and **10 Measurable Success Criteria (`SC-001`–`SC-010`)**. | Software Engineers, QA/SDETs, AI Coding Agents, Compliance Reviewers |
| **[`agentic-sdlc-guide.md`](./agentic-sdlc-guide.md)**<br/>*(Agentic SDLC Playbook)* | Educational engineering playbook and empirical case study detailing how Atruss Code Atlas was built using **SpecKit Specification-Driven Development (`001`–`006A`)**, **Antigravity Native Agentic Coding & Parallel Swarms (`006B`–`009` + Horizon 2)**, the **`RPI -> QRSPI`** (*Question-Research-Spec-Plan-Implement*) evolution, **Harness Engineering** (*Feed-Forward Guides + Feedback Sensors*), and **Cross-Ecosystem Education**.<br/>Includes embedded **Mermaid diagrams**, a feature-by-feature attribution matrix, the **3-Layer Hybrid 5-Gate Governance Model**, and an **Enterprise Decision Flowchart**. | VP of Engineering, Engineering Managers, Staff Engineers, AI Platform & Governance Teams |
| **[`agentic-sdlc-research-and-update-plan.md`](./agentic-sdlc-research-and-update-plan.md)**<br/>*(Agentic SDLC Research & Update Plan)* | Synthesizes industry best practices from **QRSPI** (Alex Kim), **Harness Engineering** (Martin Fowler / Birgitta Böckeler — Guides vs. Sensors), **Specification-Driven Development** (Thoughtworks / SpecKit), and **Multi-Agent Swarm Governance**, mapping them to concrete documentation and harness tracks across `README.md`, `docs/`, and `.github/workflows/`. | AI Platform Engineers, Technical Writers, Governance & DevEx Leads |
| **[`metrics-methodology.md`](./metrics-methodology.md)**<br/>*(Metrics & Scoring Methodology)* | Transparent reference for how every metric in Atruss Code Atlas is derived: **6-Dimension A–F Scorecard** weights & exact deduction formulas, **Remediation Hours**, **Engineering Maturity Leaderboard (60/40)** index, `tree-sitter` **Cyclomatic/Cognitive Complexity**, **AST Clone Duplication**, **PageRank Blast Radius**, and **14-Rule CI/CD** & **Architecture Fitness** policies. | Engineering Leaders, Architects, Auditors, Platform Teams |

---

## 2. Unified SpecKit Execution Package (`specs/009-unified-atlas-spec/`)

To maintain 100% programmatic conformance with the **5-Gate Agentic Workflow Validator** ([`../scripts/validate_agent_workflow.py`](../scripts/validate_agent_workflow.py)), the unified specification is paired with its structured SpecKit execution artifacts in [`../specs/009-unified-atlas-spec/`](../specs/009-unified-atlas-spec/):

| Artifact | Objective & Scope | Verification Gate |
| :--- | :--- | :--- |
| **[`../specs/009-unified-atlas-spec/spec.md`](../specs/009-unified-atlas-spec/spec.md)** | Canonical SpecKit copy of the Unified Specification (`US1`–`US13`, `FR-001`–`FR-030`, `SC-001`–`SC-010`). | **Gate 1**: Extracts all `FR-\d+` and `SC-\d+` identifiers to enforce 100% task coverage. |
| **[`../specs/009-unified-atlas-spec/plan.md`](../specs/009-unified-atlas-spec/plan.md)** | **Unified Implementation Plan**. Maps constitutional guardrails, canonical repository module paths (`manifests/`, `src/`, `scripts/`, `web/`, `tests/`), and the 3-Wave Antigravity Swarm delivery architecture for `REC-01`–`REC-10`. | **Gate 1**: Verifies every concrete backticked file path exists on disk (`missing_targets = 0`). |
| **[`../specs/009-unified-atlas-spec/tasks.md`](../specs/009-unified-atlas-spec/tasks.md)** | **Unified Task Traceability Matrix (`T001`–`T030`)**.<br/>- **Phase 1 & 2 (`T001`–`T020` `[x]`)**: Completed baseline tasks mapped to `FR-001`–`FR-020` (`001`–`008`).<br/>- **Phase 3 (`T021`–`T030` `[x]`)**: Completed Horizon 2 enhancement tasks mapped 1:1 to `FR-021`–`FR-030` (`REC-01`–`REC-10`) on branch `002-horizon2-unified-atlas`. | **Gate 1**: Verifies 30/30 `FR`s and 10/10 `SC`s are mapped to checked tasks `T001`–`T030`. |
| **[`../specs/009-unified-atlas-spec/checklists/requirements.md`](../specs/009-unified-atlas-spec/checklists/requirements.md)** | **SpecKit Specification Quality Checklist**. Confirms zero unresolved ambiguities, complete acceptance scenarios, and full requirement-to-task readiness. | SpecKit Quality & Readiness Gate |

---

## 3. Next-Iteration SpecKit Package (`specs/010-parity-and-hardening/` — Draft)

Tracks remaining post-release gaps (`is_outdated` freshness, NVD/CVSS & `atruss check` OSV parity, Go/Rust/Ruby/PHP/Elixir AST depth, `curate_corpus.py` 372-repo sync, expanded `--random-sample`, and monorepo benchmark SLA recovery) while formally ratifying superior code evolutions (10-ecosystem structural/manifest coverage, 4 UI tabs, 15 filter chips + pagination, Astro 6 + Mermaid v12 ELK, `orgs-summary.json`, `reports/{org}/{repo}.mdx`, and `pipeline_architecture.md`):

- [`../specs/010-parity-and-hardening/spec.md`](../specs/010-parity-and-hardening/spec.md) (`US1`–`US4`, `FR-001`–`FR-010`, `SC-001`–`SC-008`)
- [`../specs/010-parity-and-hardening/plan.md`](../specs/010-parity-and-hardening/plan.md) · [`../specs/010-parity-and-hardening/tasks.md`](../specs/010-parity-and-hardening/tasks.md) (`T001`–`T020` `[ ]`) · [`../specs/010-parity-and-hardening/checklists/requirements.md`](../specs/010-parity-and-hardening/checklists/requirements.md)

---

## 4. Recommended Reading Order by Role

1. **New Stakeholders & Engineering Leaders**: Start with the root [`../README.md`](../README.md) (*What's In It For You* by persona), then read [`agentic-sdlc-guide.md`](./agentic-sdlc-guide.md), [`agentic-sdlc-research-and-update-plan.md`](./agentic-sdlc-research-and-update-plan.md), and Sections 1–4 of [`atruss-code-atlas-prd.md`](./atruss-code-atlas-prd.md).
2. **Product Managers & System Architects**: Read [`atruss-code-atlas-prd-baseline.md`](./atruss-code-atlas-prd-baseline.md) for the v1.0 foundation, followed by [`atruss-code-atlas-prd.md`](./atruss-code-atlas-prd.md) for the `001`–`008` lineage audit and Top 10 strategic enhancements (`REC-01`–`REC-10`).
3. **Contributors & AI Coding Agents Implementing Horizon 2 (`v2.1`–`v2.3`)**: Load [`atruss-code-atlas-unified-spec.md`](./atruss-code-atlas-unified-spec.md) alongside [`../specs/009-unified-atlas-spec/plan.md`](../specs/009-unified-atlas-spec/plan.md) and [`../specs/009-unified-atlas-spec/tasks.md`](../specs/009-unified-atlas-spec/tasks.md), and validate all changes using:
   ```bash
   python scripts/validate_agent_workflow.py --spec specs/009-unified-atlas-spec
   ```

---

## 5. Multi-Repo & 10-Ecosystem Delivery via Antigravity Subagents & GitHub Native Flows

The expanded **372-repository production corpus** across **10 ecosystems** (`Python`, `.NET`, `JavaScript/TypeScript`, `Java`, `Go`, `Rust`, `Ruby`, `PHP`, `Elixir`, and `Container / Helm / IaC`—with `tree-sitter` CST metrics across Python/.NET/TS/JS/Java and structural/IaC extraction across the remaining ecosystems) and **multi-repository project topologies** (split backend/client/deployment/helm/operator repos) were delivered using Antigravity's native subagent orchestration (`invoke_subagent`) paired with GitHub-native CI/CD workflows, precomputed organization rollups ([`scripts/generate-org-summary.py`](../scripts/generate-org-summary.py) -> `exports/latest/orgs-summary.json`), and the Astro 6 + Mermaid v12 (`@mermaid-js/layout-elk`) web portal ([`web/README.md`](../web/README.md)):

1. **Parallel Domain Subagent Swarms**:
   - **AST & Fitness Swarm**: Extended [`manifests/ecosystems.yaml`](../manifests/ecosystems.yaml) and [`src/analyzers/code/`](../src/analyzers/code/) for 10-ecosystem structural parsing, cyclomatic complexity, and architectural fitness rules (`AP-001`–`AP-014`).
   - **Supply-Chain & Traceability Swarm**: Delivered offline-capable CycloneDX v1.6 SBOMs, OSV CVE matching, 6-Dimension A–F Scorecards, Code-to-Cloud traceability, and OASIS SARIF v2.1.0 outputs.
   - **Multi-Repo Corpus & UI Swarm**: Curated the 372-repo multi-repo corpus ([`tests/fixtures/popular_100_corpus.json`](../tests/fixtures/popular_100_corpus.json)), built subprocess-isolated checkpointed benchmarking (`atruss benchmark --isolated --checkpoint-dir ... --resume`), and wired [`web/src/components/CrossRepoTopology.astro`](../web/src/components/CrossRepoTopology.astro) + [`web/src/components/PipelineView.astro`](../web/src/components/PipelineView.astro).
2. **GitHub-Native Verification & Deployment Flows**:
   - **CI Gate ([`.github/workflows/tests.yml`](../.github/workflows/tests.yml))**: Runs `ruff check`, `pytest tests/unit/`, Astro Portal tests & dual builds (`npm test && npm run build`), `pytest tests/integration/`, and the **5-Gate Agentic Workflow Validator** (`validate_agent_workflow.py`) on every push and PR.
   - **Portal Publishing ([`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml))**: Synchronizes `exports/latest/` via `npm run copy-data`, compiles the static Material Design 3 Astro Starlight site, and deploys directly to GitHub Pages.
