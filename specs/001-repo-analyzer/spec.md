# Feature Specification: Repository Discovery and Deep Analysis

**Feature Branch**: `001-repo-analyzer`  
**Created**: 2026-03-20  
**Status**: Draft  
**Input**: User description: "Discover all repositories across a GitHub organization... Analyze CI/CD pipelines... Deep-analyze local code..." based on Atruss Code Atlas PRD.

## Clarifications

### Session 2026-03-20
- Q: What is the primary user interface for triggering the discovery and analysis in the MVP? → A: Command Line Interface (CLI)
- Q: Should we keep the authentication requirement for the MVP? → A: Keep optional PAT auth for rate limits
- Q: Should we design the MVP's data model to abstract away GitHub from the start? → A: Abstract data models now
- Q: How should the system handle repositories that don't match the 4 supported ecosystems? → A: Analyze pipelines only, skip code

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Discover and Classify Repositories (Priority: P1)

As an engineering leader, I want to scan a GitHub organization or user to discover all available repositories, and accurately classify each by its primary ecosystem, framework, and deployment patterns, so that I can maintain visibility over our technology landscape.

**Why this priority**: Organization-wide visibility is the primary entry point for large-scale analysis. It establishes the foundational inventory that all other analyses build upon.

**Independent Test**: Can be fully tested by providing a target GitHub organization and verifying that it returns a complete repository inventory list, where each entry is correctly classified by ecosystem without relying on deep static code analysis.

**Acceptance Scenarios**:

1. **Given** a valid GitHub organization target, **When** the discovery scan runs, **Then** all accessible repositories are listed with their detected primary ecosystem and framework.
2. **Given** a monorepo containing multiple ecosystems, **When** the classification logic runs, **Then** the repository is separated into independent module units based on defined manifest resolution rules.

---

### User Story 2 - Analyze CI/CD Pipelines (Priority: P1)

As a DevOps engineer, I want to analyze the `.github/workflows` found within a repository to construct a visual representation (DAG) of the deployment process, so that I can visually identify deployment workflows, missing test gates, and pipeline anti-patterns.

**Why this priority**: Pipeline transparency is crucial for security and software delivery performance. Parsing the CI/CD pipeline surfaces immediate risks (like missing caching or skipped tests) without downloading the entire codebase.

**Independent Test**: Can be fully tested using only `.github/workflows/*.yml` artifact files from a repository to verify that all nodes, jobs, and execution chains (sequential/parallel) are correctly visualized in a DAG.

**Acceptance Scenarios**:

1. **Given** a repository with GitHub Actions workflows, **When** the pipeline analyzer runs, **Then** a visual DAG is generated matching the structure defined by the `needs:` directives.
2. **Given** a deployment workflow missing an upstream test job, **When** the pipeline analyzer runs, **Then** a "No test gate before deploy" anti-pattern flag is raised.

---

### User Story 3 - Deep Local Code Analysis (Priority: P2)

As a software architect, I want to execute a deep analysis on a cloned local repository to extract architecture patterns, API endpoints, data access layers, and security configurations, so that I can automatically generate Arc42 software documentation featuring Mermaid diagrams.

**Why this priority**: Architectural documentation drastically reduces the context-gathering time for developers, bringing value via reverse-engineered architecture diagrams.

**Independent Test**: Can be verified by running the analyzer against a local directory containing a supported project (e.g., Python, .NET, React, JS/Java) and validating that Arc42 structured markdown and correct Mermaid diagrams are generated.

**Acceptance Scenarios**:

1. **Given** a cloned local repository, **When** deep architectural analysis is run, **Then** key architectural boundaries and API endpoints are identified.
2. **Given** the extracted telemetry, **When** report generation executes, **Then** an Arc42 compliant markdown document is produced containing a Mermaid architectural diagram of the data and control flow.

---

### User Story 4 - Extract Test Coverage (Priority: P2)

As an engineering manager, I want to automatically extract the test coverage percentage from a repository's CI/CD pipeline artifacts, so that I can track testing health alongside the pipeline DAG without manually downloading reports.

**Why this priority**: Test coverage is a lagging indicator of quality compared to DAG structure (presence of tests), but highly requested. Since it relies on artifact parsing, it belongs after DAG generation.

**Independent Test**: Provide pipeline mock output containing a pytest/Jest coverage summary and verify the system extracts the correct percentage with ±2% tolerance.

**Acceptance Scenarios**:

1. **Given** a repository where a CI pipeline has run with standard test coverage (pytest/Jest/dotnet test/Jacoco), **When** the pipeline analyzer runs, **Then** the coverage metric is accurately extracted from the latest run log or artifact.

### Edge Cases

- What happens when a repository codebase belongs to an unsupported programming ecosystem? → System will gracefully skip deep code analysis but MUST still parse and visualize CI/CD pipelines (e.g., `.github/workflows`).
- How does the system handle GitHub API rate-limiting errors when discovering repositories across a massive GitHub organization?
- How does the DAG renderer handle overly complex pipelines with dozens of heavily interconnected parallel jobs?
- What happens when analyzing an extremely large localized repository with >500k lines of code?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Command Line Interface (CLI) to discover and list repositories for a specified GitHub organization, user, or topic filter.
- **FR-002**: System MUST classify each discovered repository's language, framework, and deployment patterns via extensible YAML/JSON manifests.
- **FR-003**: System SHOULD support optional Fine-Grained Personal Access Token authentication to handle GitHub API rate limits during large discovery scans, but MUST operate without authentication for small public scans.
- **FR-004**: System MUST parse workflow files located in `.github/workflows/*.yml` to extract job definitions, steps, deployment triggers, and step dependencies.
- **FR-005**: System MUST construct and visualize a Directed Acyclic Graph (DAG) for pipeline workflows.
- **FR-006**: System MUST flag CI/CD pipeline anti-patterns, specifically targeting untested deployments, lack of caching, and unmasked secrets.
- **FR-007**: System MUST perform deep static code analysis on cloned local codebases to extract architecture components (API routes, data layers) for supported ecosystems. For unsupported ecosystems, the system MUST gracefully skip deep analysis and only perform pipeline visualization.
- **FR-008**: System MUST generate automated technical documentation following the Arc42 standard, incorporating embedded Mermaid syntax diagrams for architectural visualization.
- **FR-009**: System MUST extract and calculate test coverage percentage when pipeline test artifacts/logs (e.g., from pytest, Jest, dotnet test, Jacoco) are present.

### Key Entities

- **GitRepository**: Represents the high-level metadata of a provider-agnostic Git repository (e.g., GitHub, BitBucket, ADO), indicating its calculated primary ecosystem, commit health, and module structure.
- **PipelineWorkflow**: Represents a formalized CI/CD execution pipeline, logically grouping its internal `Jobs` and their dependency (`needs:`) edge relationships.
- **ArchitectureComponent**: Represents a discovered code structure, highlighting boundary interactions such as API ingest points or persistent data access boundaries.
- **AntiPatternFinding**: Represents an identified risk within a workflow or architectural boundary, detailing the severity and nature of the infraction.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully discover and classify an organization containing up to 100 repositories in under 2 minutes.
- **SC-002**: Pipeline DAG renderings correctly visualize 100% of defined sequential and parallel jobs located within the workflow configurations.
- **SC-003**: Deep architectural local analysis is correctly executed on repositories under 500k LoC and produces completed Arc42 documentation in under 3 minutes.
- **SC-004**: System-identified pipeline anti-patterns achieve an accuracy rate producing fewer than 5% false positives across a standardized test repository suite.
- **SC-005**: Test coverage extraction is accurate within a ±2% tolerance compared to the native tool's reported output.
