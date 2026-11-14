<!--
Sync Impact Report:
- Version change: 2.0.0 -> 2.1.0
- Modified principles: 
  - VIII. Standardized Node.js Development Environment -> VIII. Standardized WSL Development Environment
- Added sections: None
- Removed sections: None
- Templates requiring updates: 
  - ✅ tasks-template.md (environment checklists must respect WSL limits)
- Follow-up TODOs: None
-->
# Atruss Code Atlas Constitution

## Core Principles

### I. Policy-as-Code & Extensibility
All classification logic is externalized as YAML/JSON manifests—never hardcoded. New ecosystems are addable via manifest extension with zero engine code changes. Plugin manifest schema enforced by governance.

### II. Single Source of Truth for Reports
The canonical JSON report is the single source of truth. HTML and PDF reports must be rendered ONLY from this canonical JSON. Render pipeline reads no other source.

### III. Security & Privacy First
GitHub tokens must never be persisted beyond the session or written to exported artifacts. Clones must use ephemeral temporary directories that are deterministically purged on completion. Dependency vulnerability intelligence must be queried dynamically from authoritative advisory databases (OSV.dev batch API and NIST NVD, with air-gapped cache support) rather than hardcoded.

### IV. Performance & Scalability
Analyses for `< 500k` LoC repositories must complete in `< 3 minutes` (`<= 180s` SLA). The engine must use bounded asynchronous concurrency (`asyncio.Semaphore`) with per-repository timeout circuit breakers and shallow blobless Git clones (`--depth 1 --filter=blob:none --single-branch`).

### V. Auditability
Every report event must be logged, including actor, timestamp, and repo identity, using an append-only tamper-evident audit log.

### VI. Pipeline Visualization as a First-Class Feature
Pipeline visualization is a core feature, not an addon. The DAG must be accurate, interactive, exportable, and fully represent the `.github/workflows/*.yml` definitions including triggers and anti-patterns.

### VII. Strict Test and Specification Driven Development
All features must be specified strictly via SDD methodologies before implementation. Subsequent coding MUST follow Test-Driven Development (TDD) where failing tests are designed first. Test harnesses must explicitly validate complex structures using baseline targets (e.g., `github-samples/pets-workshop` to ensure client, server, and content mono-repo submodule discovery operates seamlessly).

### VIII. Standardized WSL Development Environment
All frontend development, Docs-as-Code generation, and Python tooling MUST be executed within a Windows Subsystem for Linux (WSL) environment to prevent path length issues and cross-platform discrepancies. Node.js versions MUST be managed strictly using `fnm` (Fast Node Manager) pointing to the project's required engine version (>= v22). Python development MUST utilize a virtual environment (`venv`) initiated natively within WSL bash.

## Technology & Architecture Constraints

- **Development Environment**: All execution workloads must run inside WSL. Node.js workloads must execute via `fnm`, avoiding native or nvm bounds. Python workloads must execute via native WSL `venv`.
- **Analysis**: Use ecosystem-appropriate AST and dependency scanners (e.g., Radon, Bandit for Python; Roslyn for .NET; ESLint for JS/TS; PMD, SpotBugs for Java).
- **Orchestration & Storage**: The core engine MUST run strictly as an offline-capable CLI without a database or async broker (No FastAPI, Celery, Redis, PostgreSQL, or S3/MinIO). The strictly typed JSON schema acts as the immutable contract, outputting native self-contained Arc42 Markdown/Mermaid files specifically designed for seamless ingestion by static SSGs like Astro.

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and migration plans. All PRs/reviews must verify compliance with the "Policy-as-Code" and "Single Source of Truth" principles.

**Version**: 2.1.0 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-03-28
