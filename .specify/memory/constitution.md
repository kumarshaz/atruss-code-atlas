<!--
Sync Impact Report:
- Version change: 1.1.0 -> 2.0.0
- Modified principles: 
  - [PROJECT_NAME] -> Atruss Code Atlas
  - [PRINCIPLE_1_NAME] -> I. Policy-as-Code & Extensibility
  - [PRINCIPLE_2_NAME] -> II. Single Source of Truth for Reports
  - [PRINCIPLE_3_NAME] -> III. Security & Privacy First
  - [PRINCIPLE_4_NAME] -> IV. Performance & Scalability
  - [PRINCIPLE_5_NAME] -> V. Auditability
  - Added VI. Pipeline Visualization as a First-Class Feature
  - Added VII. Strict Test and Specification Driven Development
- Added sections: Technology & Architecture Constraints
- Removed sections: Orchestration & Storage (FastAPI, Postgres, Redis dependencies explicitly banned)
- Templates requiring updates: 
  - ✅ plan-template.md (general updates not needed as it defers to constitution)
  - ✅ spec-template.md (general updates not needed as it handles custom constraints well)
  - ✅ tasks-template.md (updated to make TDD testing mandatory rather than optional)
- Follow-up TODOs: None
-->
# Atruss Code Atlas Constitution

## Core Principles

### I. Policy-as-Code & Extensibility
All classification logic is externalized as YAML/JSON manifests—never hardcoded. New ecosystems are addable via manifest extension with zero engine code changes. Plugin manifest schema enforced by governance.

### II. Single Source of Truth for Reports
The canonical JSON report is the single source of truth. HTML and PDF reports must be rendered ONLY from this canonical JSON. Render pipeline reads no other source.

### III. Security & Privacy First
GitHub tokens must never be persisted beyond the session. They must use ephemeral job context that is purged on completion. CVE data must be sourced from NIST NVD API (not vendored).

### IV. Performance & Scalability
Analyses for < 500k LoC repositories must complete in < 3 minutes. The system must use an async job queue with a timeout circuit breaker and support 10 concurrent analyses per tenant via horizontal containerized workers.

### V. Auditability
Every report event must be logged, including actor, timestamp, and repo identity, using an append-only tamper-evident audit log.

### VI. Pipeline Visualization as a First-Class Feature
Pipeline visualization is a core feature, not an addon. The DAG must be accurate, interactive, exportable, and fully represent the `.github/workflows/*.yml` definitions including triggers and anti-patterns.

### VII. Strict Test and Specification Driven Development
All features must be specified strictly via SDD methodologies before implementation. Subsequent coding MUST follow Test-Driven Development (TDD) where failing tests are designed first. Test harnesses must explicitly validate complex structures using baseline targets (e.g., `github-samples/pets-workshop` to ensure client, server, and content mono-repo submodule discovery operates seamlessly).

## Technology & Architecture Constraints

- **Ingestion**: Use GitHub REST v3 + GraphQL v4.
- **Analysis**: Use ecosystem-appropriate AST and dependency scanners (e.g., Radon, Bandit for Python; Roslyn for .NET; ESLint for JS/TS; PMD, SpotBugs for Java).
- **Orchestration & Storage**: The core engine MUST run strictly as an offline-capable CLI without a database or async broker (No FastAPI, Celery, Redis, PostgreSQL, or S3/MinIO). The strictly typed JSON schema acts as the immutable contract, outputting native self-contained Arc42 Markdown/Mermaid files specifically designed for seamless ingestion by static SSGs like Astro.

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and migration plans. All PRs/reviews must verify compliance with the "Policy-as-Code" and "Single Source of Truth" principles.

**Version**: 2.0.0 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-03-20
