# Feature Specification: Chained Analysis Pipeline

**Feature Branch**: `002-chain-analysis`  
**Created**: 2026-03-20  
**Status**: Draft  
**Input**: User description: "Add ability to output discovery results to JSON and use that JSON as input for pipeline and code analysis phases, automatically cloning the repositories locally before analyzing. In ADO, I would analyze all the repos in a project in discovery phase and then in code analysis, I would clone the repos locally and then run the analysis."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chained Code Analysis (Priority: P1)

As a security or architecture reviewer, I want to feed my organization's repository discovery JSON directly into the deep code analyzer so that I don't have to manually clone 100+ repositories by hand to analyze their architectures.

**Why this priority**: Automating the gap between discovery and analysis is the core value proposition of an at-scale organization analyzer.

**Independent Test**: Can be fully tested by providing a mock JSON array matching the discovery output format, verifying the tool clones the repos, executes the code scanner, and reports results.

**Acceptance Scenarios**:

1. **Given** a valid JSON discovery file and an `--output-dir`, **When** the `analyze-code` command is executed with the `--from-discovery` flag, **Then** all repositories in the JSON are cloned locally, analyzed, and a Markdown architecture report is generated for each.
2. **Given** a repository that fails to clone (e.g., unauthorized), **When** the command iterates to that repository, **Then** the failure is logged and the analysis gracefully skips to the next repository.

---

### User Story 2 - Chained Pipeline Analysis (Priority: P1)

As a DevSecOps engineer, I want to feed my organization's discovery JSON directly into the pipeline analyzer to check GitHub Actions workflows globally across all my repos.

**Why this priority**: Checking anti-patterns at scale is crucial for organization-wide compliance.

**Independent Test**: Can be tested by providing a JSON manifest containing a few public repositories, verifying the DAG builder processes local workflows for all of them.

**Acceptance Scenarios**:

1. **Given** a valid discovery JSON file, **When** `analyze-pipeline` is run with `--from-discovery`, **Then** the tool clones the repos and extracts the workflow DAG logs for each.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `discover` command MUST output the standard JSON array to a file when an `--output` argument is provided.
- **FR-002**: The `analyze-code` and `analyze-pipeline` commands MUST accept a `--from-discovery <file.json>` flag.
- **FR-003**: If `--from-discovery` is provided, the tool MUST iterate through the JSON array, extracting the `clone_url` and `name` of each repository.
- **FR-004**: The tool MUST automatically clone each remote repository to a local workspace using `git clone`.
- **FR-005**: The local clones MUST be located in the Operating System Temporary Directory to ensure isolated runs.
- **FR-006**: The tool MUST keep the cloned repositories locally after analysis completes, deferred to the OS temporary directory lifecycle for garbage collection.
- **FR-007**: The tool MUST utilize existing Git credentials (e.g. `GITHUB_TOKEN` environment variable or local SSH bindings) to execute the remote clones.

### Key Entities

- **DiscoveryManifest**: The JSON array schema containing `[{"name": "repo-a", "clone_url": "https...", "ecosystem": "python"}]` defining the execution bounds.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can execute a full organization discovery and subsequent code analysis entirely through automated chained arguments without manual `git clone` execution.
- **SC-002**: The tool successfully handles multi-repository scaling bounds (e.g. 50+ repositories) without crashing from disk space exhaustion or unhandled exceptions natively.
