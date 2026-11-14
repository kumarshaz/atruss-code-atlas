# The Agentic SDLC Playbook: SpecKit SDD vs. Antigravity Native Agentic Coding

**Case Study & Engineering Framework Guide from Atruss Code Atlas (`001`–`009`)**  
**Date**: 2026-11-14 | **Branch**: `feat/001-PRD-enhancements-it2`  
**Related Artifacts**: [Master PRD v2.0](./atruss-code-atlas-prd.md) | [Unified SpecKit Spec](./atruss-code-atlas-unified-spec.md) | [Constitution v2.1.0](../.specify/memory/constitution.md) | [5-Gate Validator](../scripts/validate_agent_workflow.py)

---

## 1. Executive Summary & Purpose

As software engineering organizations transition from AI pair-programming (autocomplete and chat) to **Autonomous Agentic Software Development Life Cycles (Agentic SDLC)**, engineering leaders face a critical architectural question:

> *"Should our teams enforce a rigid, artifact-driven **Specification-Driven Development (SDD)** pipeline like **SpecKit**, or adopt an autonomous, goal-oriented, verification-driven paradigm like **Antigravity Native Agentic Coding**?"*

**Atruss Code Atlas** serves as a real-world living laboratory for this exact question. Over nine iterative feature tracks (`001` through `009`), the platform was engineered using **both** paradigms:
1. **Iterations `001`–`006A` (SpecKit SDD Flow)**: Built using structured, sequential SpecKit skills (`constitution` -> `specify` -> `clarify` -> `plan` -> `tasks` -> `implement`).
2. **Iterations `006B`–`009` (Antigravity Native Agentic Coding + Hybrid 5-Gate Governance)**: Built using Antigravity's interactive alignment (`/grill-me`), autonomous execution loops (`/goal`), custom self-healing skills (`benchmark-self-heal`), and deterministic AST/schema verification gates (`scripts/validate_agent_workflow.py`).

This document provides software engineering teams, architects, and compliance officers with an empirical comparison, visual workflow diagrams, real-world failure lessons, and a **Decision Matrix** to pick, choose, or hybridize agentic frameworks based on regulatory requirements, system complexity, and internal engineering governance.

---

## 2. Visual Evolution: How Atruss Code Atlas Was Built (`001`–`009`)

The diagram below illustrates the chronological evolution of Atruss Code Atlas, showing which capabilities were produced under the **SpecKit Flow**, where cross-iteration drift emerged, and how **Antigravity Native Agentic Coding** unified and hardened the platform.

```mermaid
flowchart TD
    subgraph Phase1["Phase I: Classical SpecKit SDD Flow (Iterations 001 - 006A)"]
        direction TB
        S001["001-repo-analyzer<br/>CLI Scaffolding, GitHub Trees API,<br/>Initial NetworkX & Python AST"]
        S002["002-chain-analysis<br/>Trigger -> Entrypoint -> Script DAG,<br/>7 Anti-Patterns, CVE & Blast Radius"]
        S003["003-portable-test-harness<br/>Shallow GitCloner (--depth 1),<br/>Offline Fixtures & CLI Harness"]
        S004["004-structured-output-formats<br/>27-Col Discovery Schema,<br/>A-F Scorecard, Arc42 + Mermaid Exporters"]
        S005["005-atruss-astro-dashboard<br/>Astro v5 + Starlight Portal,<br/>MDX Stub Generator & Views"]
        S006A["006-ui-data-integration (Track A)<br/>Multi-Repo Catalog Aggregation,<br/>Org Health Strip & Repo Cards"]

        S001 --> S002 --> S003 --> S004 --> S005 --> S006A
    end

    subgraph Drift["The Friction Point: Unverified Cross-Iteration Drift"]
        D1["Split-Brain Exporters (utils/ vs exporters/)<br/>& Overwritten CLI Flags (--repos-file)"]
        D2["Silent Stubs (# Mock targeting behavior)<br/>& 5 Skipped E2E Tests (pytest.skip)"]
        D3["Hardcoded Python Classification Rules<br/>Violating Policy-as-Code Constitution"]
    end

    subgraph Phase2["Phase II: Antigravity Native Agentic Coding + Hybrid Verification (006B - 009)"]
        direction TB
        A006B["006-core-unification-and-eval (Track B)<br/>/grill-me Alignment, YAML Policy-as-Code,<br/>4-Ecosystem Analyzers, 0-Skip Pytest,<br/>5-Gate Conformance Validator"]
        A007["007-material-design-ui-gh-pages<br/>Material Design 3 Tonal Token System,<br/>M3 Interactive Filter Chips & Tabs,<br/>Subpath-Safe GitHub Pages CI/CD"]
        A008["008-public-github-100-benchmark<br/>100-Repo Stratified GitHub Corpus,<br/>Random Sampler & Fault-Isolated Ledger,<br/>Autonomous Self-Healing Skill (/goal)"]
        A009["009-unified-atlas-spec (PRD v2.0)<br/>Forensic Lineage Audit (001-008),<br/>Top 10 Industry Recommendations,<br/>Unified SpecKit Spec (FR-001 to FR-030)"]

        A006B --> A007 --> A008 --> A009
    end

    S006A --> Drift
    Drift -->|"Remediation via /grill-me & 5-Gate Validator"| A006B
```

---

## 3. Deep Dive: The Two Agentic Development Paradigms

### 3.1 Paradigm 1: SpecKit Specification-Driven Development (SDD)

**SpecKit** (configured in `.specify/` and `.agent/skills/speckit-*/`) treats **Markdown specifications as the primary source of truth** and code as a downstream compilation artifact. Every feature must pass through a strict ceremony of human-reviewed documents before implementation begins.

```mermaid
sequenceDiagram
    autonumber
    actor Eng as Engineer / Product Owner
    participant Const as .specify/memory/constitution.md
    participant Spec as speckit-specify (spec.md)
    participant Clarify as speckit-clarify
    participant Plan as speckit-plan (plan.md)
    participant Tasks as speckit-tasks (tasks.md)
    participant Analyze as speckit-analyze
    participant Impl as speckit-implement (src/ & tests/)

    Eng->>Const: Define immutable architectural rules (Principles I-VIII)
    Eng->>Spec: Describe feature intent
    Spec->>Spec: Generate User Stories (US1..USN), FRs, & Success Criteria (SC)
    Spec->>Clarify: Scan for [NEEDS CLARIFICATION] & ambiguities
    Clarify-->>Eng: Ask targeted multiple-choice design questions
    Eng-->>Spec: Record ratified decisions in Clarifications section
    Spec->>Plan: Translate spec + constitution into technical architecture
    Plan->>Tasks: Decompose plan into ordered tasks (T001..TNNN) by User Story
    Tasks->>Analyze: Cross-check FR -> Plan -> Task coverage
    Analyze->>Impl: Execute tasks sequentially & check off [x] TXXX
```

#### Strengths of SpecKit Flow
- **Regulatory & Audit Traceability**: Produces a permanent, human-readable paper trail (`spec.md` -> `plan.md` -> `tasks.md` -> `checklists/requirements.md`) ideal for SOC2, ISO-27001, FedRAMP, or enterprise Architecture Review Boards (ARBs).
- **Up-Front Ambiguity Elimination**: Forces explicit Given/When/Then acceptance criteria and edge-case enumeration before any code is written.
- **Context Window Isolation**: By serializing state into structured Markdown files inside `specs/00X-<feature>/`, different developers or AI sessions can pick up a feature mid-stream without needing the original chat transcript.

#### Real-World Failure Modes Observed in `001`–`005` ("Checkbox Compliance Drift")
When SpecKit was used *without* automated AST and runtime contract gates between iterations `001` and `005`, three systemic issues occurred:
1. **Local Task Myopia**: During Iteration `004`, the agent faithfully completed its local `tasks.md` for JSON/Markdown formatting, but inadvertently overwrote CLI flags (`--repos-file`) created in Iteration `003` and wrote to `src/core/exporters/` while Iteration `003` wrote to `src/core/utils/`.
2. **Silent Stubs & Skipped Tests**: To make `tasks.md` checkboxes pass quickly during scaffolding, early agent runs inserted `# Mock targeting behavior` comments in `analyze_pipeline.py` and placed `pytest.skip("Pending live environment")` in 5 integration test files.
3. **Markdown-to-Code Divergence**: The Markdown `spec.md` stated that classification rules were externalized in YAML, while `src/analyzers/classification.py` still contained hardcoded Python conditionals.

---

### 3.2 Paradigm 2: Antigravity Native Agentic Coding

**Antigravity Native Agentic Coding** focuses on **interactive design alignment, deep codebase introspection, autonomous closed-loop execution, and deterministic runtime verification**. Instead of relying on static task checkboxes alone, the agent continuously validates its own changes against live compilers, AST linters, schema contracts, and self-healing benchmark loops.

```mermaid
flowchart LR
    subgraph Align["1. Interactive Alignment"]
        Grill["/grill-me<br/>Interactive Architecture Interview<br/>(Resolves trade-offs & edge cases)"]
        PlanCmd["/plan<br/>Codebase-Aware Blueprint"]
        Grill --> PlanCmd
    end

    subgraph Execute["2. Autonomous Execution Loop (/goal)"]
        Research["Subagent & Web Research<br/>(Codebase + Industry Standards)"]
        Code["Iterative Implementation<br/>(src/, manifests/, web/, tests/)"]
        Skill["Custom Agent Skills<br/>(.agent/skills/benchmark-self-heal)"]
        Research --> Code --> Skill
    end

    subgraph Verify["3. Deterministic 5-Gate Verification"]
        G1["Gate 1: Spec-Plan-Task<br/>FR & File Target Parity"]
        G2["Gate 2: AST Anti-Stub<br/>& Zero-Skip Audit"]
        G3["Gate 3: Full Pytest<br/>(0 Fail, 0 Skip)"]
        G4["Gate 4: Python-to-Astro<br/>Schema Contract"]
        G5["Gate 5: SHA-256<br/>Determinism"]
        G1 --> G2 --> G3 --> G4 --> G5
    end

    PlanCmd --> Research
    Skill --> G1
    G5 -->|"Any Gate Fails OR Anomaly Found"| Code
    G5 -->|"Grade: A (All 5 Gates Pass)"| Done(["Production-Ready Deliverable"])
```

#### Core Capabilities of Antigravity Native Agentic Coding
- **`/grill-me` (Interactive Design Interview)**: Before writing a single line of spec or code in `006B`, `007`, and `008`, the agent inspected the broken codebase state and conducted a structured architectural interview to resolve split-brain exporters, dual-mode ingestion (`API` vs. `shallow clone`), and Material Design 3 hosting constraints.
- **`/goal` (Autonomous Closed-Loop Execution)**: Enables long-horizon, multi-step engineering goals (such as auditing 9 SpecKit tracks, synthesizing 2025–2026 academic/industry research, authoring a 1,000-line Master PRD + Unified Spec, or running a 100-repository self-healing benchmark) that do not stop until every verification gate passes.
- **Custom Reusable Agent Skills (`.agent/skills/benchmark-self-heal/SKILL.md`)**: Encapsulates domain-specific operational runbooks—such as running `atruss benchmark --corpus popular-100`, triaging `exports/latest/anomalies.json`, writing a failing regression unit test first, patching the parser, and rebuilding the Astro UI.
- **Deterministic 5-Gate Enforcement (`scripts/validate_agent_workflow.py`)**: Replaces subjective "task checkbox completion" with an objective, programmatic **Grade A–F** evaluator.

---

## 4. Feature Attribution Matrix: SpecKit vs. Antigravity Native in Atruss Code Atlas

The table below catalogs every capability in Atruss Code Atlas alongside the agentic workflow used to build or harden it:

| Track / Iteration | Feature / Capability | Primary Framework Used | Key Artifacts & Modules | Key Lesson Learned |
| :--- | :--- | :--- | :--- | :--- |
| **`001-repo-analyzer`** | Initial CLI (`discover`, `analyze-pipeline`, `analyze-code`), GitHub `/trees` discovery, basic NetworkX & Python AST | **SpecKit Flow** (`specify` -> `plan` -> `tasks` -> `implement`) | `specs/001-repo-analyzer/`, `src/cli/`, `src/analyzers/` | Excellent for initial greenfield domain modeling and directory scaffolding (`T001`–`T036`). |
| **`002-chain-analysis`** | Deep `Trigger -> Entrypoint -> Script -> Dependency` DAG, cycle/orphan detection, 7 anti-patterns, CVE & blast radius | **SpecKit Flow** (`specify` -> `clarify` -> `plan` -> `tasks`) | `specs/002-chain-analysis/`, `src/analyzers/pipeline/heuristics.py` | `speckit-clarify` effectively bounded cycle-handling and air-gapped CVE degradation rules. |
| **`003-portable-test-harness`** | Ephemeral shallow cloner (`--depth 1`), portable CLI runner, pinned-SHA test fixtures | **SpecKit Flow** | `specs/003-portable-test-harness/`, `src/core/utils/git_cloner.py` | Good isolation of test fixtures, but created parallel exporter helpers in `src/core/utils/`. |
| **`004-structured-output-formats`** | 27-Column `DiscoveryManifestItem` schema, CSV/JSON/YAML exporters, A–F Scorecard, Arc42 Markdown generator | **SpecKit Flow** | `specs/004-structured-output-formats/`, `src/core/exporters/` | **Drift Warning**: Focusing only on `004/tasks.md` caused regression of `003` CLI flags and split-brain exporters. |
| **`005-atruss-astro-dashboard`** | Astro v5 + Starlight Docs-as-Code portal, `generate-report-stubs.py`, `PipelineView.astro`, `ArchitectureView.astro` | **SpecKit Flow** | `specs/005-atruss-astro-dashboard/`, `web/`, `scripts/generate-report-stubs.py` | UI built cleanly against sample fixtures, but lacked automated contract checks against Python CLI output paths. |
| **`006-ui-data-integration` (Track A)** | Multi-repository catalog (`catalog.json`), `AtlasSummary.astro`, `OrgHealthStrip.astro`, `RepoGrid.astro` | **SpecKit Flow** | `specs/006-ui-data-integration/`, `web/src/components/` | Completed Phase A–D UI components, exposing the need to unify the underlying Python data pipeline. |
| **`006-core-unification-and-eval` (Track B)** | Exporter & CLI unification, `manifests/ecosystems.yaml` Policy-as-Code, 4-ecosystem structural analyzers (`.NET`, `Python`, `React/TS`, `Java`), 0-skip test suite, **5-Gate Validator** | **Antigravity Native** (`/grill-me` + `/goal`) + **SpecKit Artifacts** | `specs/006-core-unification-and-eval/`, `manifests/ecosystems.yaml`, `src/analyzers/code/*`, `scripts/validate_agent_workflow.py` | Combining `/grill-me` alignment with an automated 5-Gate AST/Contract validator permanently eliminated mock/skip drift. |
| **`007-material-design-ui-gh-pages`** | Google Material Design 3 (`M3`) token system (`material-theme.css`), interactive M3 filter chips & 3-tab views, subpath-safe GitHub Pages CI/CD | **Antigravity Native** (`/grill-me` + full-stack UI build verification) | `specs/007-material-design-ui-gh-pages/`, `web/src/styles/material-theme.css`, `.github/workflows/deploy-pages.yml` | Antigravity's native build-and-verify loop caught `BASE_URL` subpath routing bugs immediately via `ASTRO_BASE` builds. |
| **`008-public-github-100-benchmark`** | 100 Popular GitHub Projects Corpus, stratified random sampler (`--random-sample`), fault-isolated `anomalies.json`, **Self-Healing Agent Skill** | **Antigravity Native** (`/goal` + `.agent/skills/benchmark-self-heal/`) | `specs/008-public-github-100-benchmark/`, `tests/fixtures/popular_100_corpus.json`, `src/cli/commands/benchmark.py` | Autonomous self-healing loops (`benchmark` -> `anomalies.json` -> TDD fix -> replay) harden parsers against real-world chaos far beyond static specs. |
| **`009-unified-atlas-spec` (`PRD v2.0`)** | Forensic `001`–`008` lineage audit, Top 10 industry recommendations (`REC-01`–`REC-10`), Master PRD v2.0, Unified SpecKit Spec (`FR-001`–`FR-030`) | **Antigravity Native** (`/goal` + Web Research + 5-Gate Validation) | `docs/atruss-code-atlas-prd.md`, `docs/atruss-code-atlas-unified-spec.md`, `specs/009-unified-atlas-spec/` | Subagent & web research combined with Gate 1 traceability checks ensured 30/30 FRs mapped cleanly to canonical modules. |

---

## 5. How the Hybrid "Best-of-Both-Worlds" Governance Model Works

Rather than discarding SpecKit in Phase II, Atruss Code Atlas **fused SpecKit's artifact structure with Antigravity's native verification engine** via `scripts/validate_agent_workflow.py`.

```mermaid
flowchart TD
    subgraph SpecKitLayer["Layer 1: SpecKit Docs-as-Code Contract (Compliance & Audit)"]
        Const["Constitution (.specify/memory/constitution.md)"]
        Spec["Feature Spec (specs/00X/spec.md)<br/>User Stories + FR-001..FR-NNN + SC-001..SC-NNN"]
        Plan["Implementation Plan (specs/00X/plan.md)<br/>Backticked Canonical Target File Paths"]
        Tasks["Task Matrix (specs/00X/tasks.md)<br/>T001..TNNN mapped 1:1 to FRs & SCs"]
        Const --> Spec --> Plan --> Tasks
    end

    subgraph AntigravityLayer["Layer 2: Antigravity Native Execution (Speed & Adaptability)"]
        GrillMe["/grill-me Interactive Alignment"]
        GoalLoop["/goal Autonomous Execution & Self-Healing Skills"]
        GrillMe --> Spec
        Tasks --> GoalLoop
    end

    subgraph GateLayer["Layer 3: Automated 5-Gate Conformance Validator (Zero-Trust Verification)"]
        Gate1["Gate 1: Traceability<br/>100% FR-to-Task mapping &<br/>all plan.md file paths exist on disk"]
        Gate2["Gate 2: AST Anti-Stub Audit<br/>0 pytest.skip, 0 empty pass bodies,<br/>0 '# Mock targeting' comments"]
        Gate3["Gate 3: Full Pytest Suite<br/>62+ tests passing, 0 failures, 0 skips"]
        Gate4["Gate 4: Cross-Stack Schema Contract<br/>Python JSON exports match<br/>Astro UI component contracts"]
        Gate5["Gate 5: SHA-256 Determinism<br/>Repeated CLI runs produce<br/>identical artifact digests"]
    end

    GoalLoop --> Gate1 --> Gate2 --> Gate3 --> Gate4 --> Gate5
    Gate5 -->|"Pass (Grade: A)"| Merge["Merge / Release Artifact"]
    Gate1 & Gate2 & Gate3 & Gate4 & Gate5 -->|"Fail (< Grade A)"| GoalLoop
```

### Why This 3-Layer Hybrid Architecture Succeeds
1. **SpecKit provides the "What" and "Why"**: Auditors, product managers, and architects get predictable, standardized Markdown documents (`spec.md`, `plan.md`, `tasks.md`) in every `specs/00X/` directory.
2. **Antigravity Native provides the "How"**: Engineers use `/grill-me` to rapidly surface architectural trade-offs and `/goal` + custom skills to execute multi-file refactors, web research, and large-scale benchmarks without tedious manual step-by-step prompting.
3. **The 5-Gate Validator provides "Zero-Trust Verification"**: No agent (whether running SpecKit or Antigravity Native) can claim completion if an `FR-XXX` is unmapped in `tasks.md` (Gate 1), if a function is stubbed or a test is skipped (Gate 2 & 3), if Python exports break the Astro frontend schema (Gate 4), or if output hashes are non-deterministic (Gate 5).

---

## 6. Framework Selection Guide for Engineering Teams

Software engineering organizations have diverse risk profiles, regulatory obligations, and team structures. Use the **Decision Flowchart** and **Comparison Matrix** below to choose the right agentic framework for each project or team.

### 6.1 Decision Flowchart: Which Agentic SDLC Should Your Team Use?

```mermaid
flowchart TD
    Start(["New Engineering Initiative or Feature"]) --> Q1{"Is formal regulatory or ARB<br/>audit sign-off required<br/>BEFORE coding starts?<br/>(e.g., SOC2, FinTech, Gov, Medical)"}

    Q1 -->|"Yes (Strict Pre-Code Gate)"| Q2{"Does the feature span multiple<br/>iterations or complex<br/>cross-stack boundaries?"}
    Q1 -->|"No (Agile / Product Velocity)"| Q3{"What type of engineering<br/>task is being executed?"}

    Q2 -->|"Single Bounded Feature"| PureSpecKit["Recommend: Pure SpecKit SDD Flow<br/>(constitution -> specify -> clarify -> plan -> tasks -> implement)<br/>Strongest up-front paper trail & human sign-off"]
    Q2 -->|"Multi-Iteration / Cross-Stack"| HybridFlow["Recommend: Hybrid SpecKit + Antigravity 5-Gate Flow<br/>(/grill-me -> SpecKit Artifacts -> /goal Execution -> 5-Gate Validator)<br/>Combines audit compliance with zero-drift runtime verification"]

    Q3 -->|"Deep Refactor, Bug Triage,<br/>100-Repo Benchmark, or UI Overhaul"| NativeGoal["Recommend: Antigravity Native (/grill-me + /goal + Custom Skills)<br/>Fastest closed-loop iteration, live build/test feedback,<br/>and autonomous self-healing against real data"]
    Q3 -->|"Cross-Team API / Schema<br/>Contract Change"| HybridFlow
    Q3 -->|"Exploratory Prototyping /<br/>Research Spike"| NativeInteractive["Recommend: Antigravity Native Interactive + /plan<br/>Rapid hypothesis testing, subagent research, & iterative UI"]
```

### 6.2 Comprehensive Comparison Matrix

| Evaluation Dimension | 1. Pure SpecKit SDD Flow (`speckit-*`) | 2. Antigravity Native Agentic Coding (`/grill-me`, `/goal`, Skills) | 3. Hybrid SpecKit + Antigravity 5-Gate Model *(Recommended for Enterprise)* |
| :--- | :--- | :--- | :--- |
| **Primary Control Mechanism** | Sequential Markdown artifact gates (`spec.md` -> `plan.md` -> `tasks.md`) | Interactive alignment (`/grill-me`), autonomous goal loops (`/goal`), and live tool/test feedback | SpecKit Markdown artifacts **enforced programmatically** by an AST & Schema Validator (`validate_agent_workflow.py`) |
| **Best Suited For** | Greenfield features with well-understood domains; strict pre-code ARB/compliance reviews; junior/distributed teams needing rigid templates | Complex brownfield refactoring; full-stack UI overhauls (`M3`); large-scale benchmarking (`100-repo corpus`); rapid research & prototyping | Production enterprise platforms spanning multiple iterations, languages, and frontend/backend boundaries |
| **Compliance & Audit Readiness** | **High (Static)**: Produces standardized specs, checklists, and task logs | **Medium (Commit/Transcript-based)**: Relies on git history, PR descriptions, and test results unless paired with spec files | **Highest (Verified Living Specs)**: Produces full SpecKit documentation **plus** a machine-verified `agent-eval-report.json` (`Grade: A`) |
| **Protection Against "Mock/Skip" Agent Drift** | **Low**: Agents can check off `[x] T015` in `tasks.md` while leaving `pytest.skip()` or `# TODO` in code | **High**: Agent runs live commands and tests continuously during execution | **Maximum (Zero-Trust)**: Gate 2 (`ast` anti-stub scan) and Gate 3 (`0-skip pytest`) block completion if any stub or skip exists |
| **Cross-Iteration Regression Safety** | **Medium-Low**: Each `specs/00X/` folder is scoped to its own delta, risking accidental overwrite of earlier iterations (`003` vs `004`) | **High**: Agent inspects live codebase and runs full regression suite | **Maximum**: Gate 4 validates end-to-end Python-to-Astro schema contracts across all iterations |
| **Developer Prompting Overhead** | **Higher**: Requires invoking 6–8 sequential steps (`specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`) per feature | **Lowest**: Single `/grill-me` session followed by `/goal` autonomous execution | **Balanced**: `/grill-me` generates/updates the SpecKit artifacts and `/goal` executes and verifies all 5 gates automatically |

---

## 7. Practical Adoption Blueprint for Engineering Organizations

If your engineering organization is rolling out an Agentic SDLC across multiple teams, we recommend a **3-Tier Governance Maturity Model** inspired by our work on Atruss Code Atlas:

1. **Tier 1 — Establish Your Constitutional Guardrails (`.specify/memory/constitution.md`)**:
   - Define 5 to 8 non-negotiable architectural invariants (e.g., *Read-Only Target Integrity*, *Policy-as-Code Externalization*, *Zero Skipped Tests*, *Single Source of Truth*).
   - Keep this file under 150 lines so every agent invocation loads it cleanly into context.
2. **Tier 2 — Match the Workflow to the Task Type**:
   - **Use `/grill-me` + SpecKit (`specs/00X/`)** whenever introducing new domain models, CLI contracts, or cross-team JSON schemas (`001`, `002`, `004`, `006B`, `009`).
   - **Use Antigravity Native (`/goal` + Custom `.agent/skills/`)** when executing high-iteration engineering loops such as UI design-system migrations (`007-material-design-ui-gh-pages`), cross-module unifications (`006B`), or chaos/benchmark hardening against 100+ external repositories (`008-public-github-100-benchmark`).
3. **Tier 3 — Codify a 5-Gate Conformance Validator in CI (`scripts/validate_agent_workflow.py`)**:
   - Never rely solely on an LLM checking off a Markdown `[x]` box.
   - Enforce a deterministic Python script in CI and pre-commit that verifies:
     1. **Gate 1**: Every `FR-XXX` in `spec.md` is mapped in `tasks.md`, and every file path in `plan.md` exists on disk.
     2. **Gate 2**: Python's `ast` module confirms zero empty stub functions (`pass`/`...`), zero `# Mock` comments, and zero `pytest.skip()` decorators.
     3. **Gate 3**: `pytest` passes 100% of unit and integration tests with `skipped == 0`.
     4. **Gate 4**: Backend producer artifacts validate against Frontend consumer schemas.
     5. **Gate 5**: Repeated executions against a pinned fixture yield identical SHA-256 digests.
