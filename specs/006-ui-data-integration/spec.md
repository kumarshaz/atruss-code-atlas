# Feature Specification: Full Astro UI Extension (Phases A-D)

**Feature Branch**: `006-ui-data-integration`  
**Created**: 2026-03-29  
**Status**: Draft  
**Input**: User description: "include all the phases from docs/astro-ui-extension-plan-after-005.md also make sure the favicon is updated with a version of web/src/assets/atruss-favicon.png"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Central Repository Discovery & Routing (Priority: P1)
As an engineering leader, I want a central dashboard that reads repository discovery data and generates a fully navigable grid and sidebar structure, so I can instantly observe the language distribution, overall risk (missing pipelines), and drill down into specific codebases.

**Why this priority**: Acts as the skeleton (Phase A) required to hook up all subsequent architectural data tabs.
**Independent Test**: Dashboard renders using `repositories.json` to generate an `OrgHealthStrip`, `LanguageChart`, and `RepoGrid`. The python stub generator correctly creates `reports/{org}/{repo}.md` files, powering the Starlight sidebar automatically.

**Acceptance Scenarios**:
1. **Given** a discovery output file, **When** the Astro build runs, **Then** a Python script auto-generates Markdown shell pages for each repository containing the correct frontmatter.
2. **Given** the generated Starlight sidebar, **When** I click into a specific repository, **Then** I see the Repository Details page populated with a "Discovery" tab laying out its properties.
3. **Given** the site renders, **When** I check the browser tab, **Then** the application favicon matches the Atruss Code Atlas branding (`atruss-favicon.png`).

---

### User Story 2 - CI/CD Pipeline Observability (Priority: P1)
As a DevSecOps engineer, I want to open a repository's detail page and switch to the "Pipeline" tab to view a visual flowchart of its deployment execution steps and identify missing quality gates.

**Why this priority**: Implements Phase B. Pipeline visualization is a core differentiator from competitors like SonarQube.
**Independent Test**: Load a repository that has valid `analyze-pipeline` JSON output and verify the frontend correctly translates the adjacency list into a visual Mermaid DAG block.

**Acceptance Scenarios**:
1. **Given** a repository with pipeline output available, **When** I view its "Pipeline" tab, **Then** I see a Mermaid DAG mapping the CI/CD execution flow.
2. **Given** a repository with pipeline anti-patterns, **When** I view the "Pipeline" tab, **Then** I see warning badges highlighting risks like "Deploying without Test Gates".
3. **Given** a repository where pipeline analysis hasn't run yet, **When** I view the tab, **Then** I see a graceful "Not yet analyzed" empty state prompt.

---

### User Story 3 - Architectural Arc42 Boundary Visualization (Priority: P2)
As a software architect, I want to open a repository's detail page and switch to the "Architecture" tab to view embedded Arc42 documentation detailing database endpoints and domain boundaries, so I don't have to manually reverse-engineer undocumented services.

**Why this priority**: Implements Phase C. It closes the observability loop, allowing offline code intelligence without requiring active plugins.
**Independent Test**: Load a repository that has `analyze-code` Arc42 output and verify starlight correctly parses the embedded Mermaid graphs inside the Markdown.

**Acceptance Scenarios**:
1. **Given** a repository with code analysis output, **When** I view its "Architecture" tab, **Then** I see the full Arc42 Markdown documentation rendered efficiently.
2. **Given** a repository lacking code analysis output, **When** I view the tab, **Then** I see a graceful "Not yet analyzed" empty-state prompt.

---

### User Story 4 - Multi-Organization Comparison (Priority: P3)
As an enterprise executive, I want a dedicated comparison page that ranks multiple GitHub organizations based on their CI/CD maturity metrics, so I can target structural modernization efforts at the poorest-performing divisions.

**Why this priority**: Implements Phase D stretch goal for cross-portfolio metric aggregation.
**Independent Test**: Navigate to the `/orgs/` route and verify the maturity leaderboard accurately reflects computed percentages relative to pipeline usage.

**Acceptance Scenarios**:
1. **Given** discovery data encompassing multiple organizations, **When** I view the `/orgs/` page, **Then** I see a leaderboard separating and scoring organizations based on pipeline prevalence and anti-pattern density.

---

### Edge Cases

- **Missing Output Phases**: A repository discovered in Phase A might never undergo Phase B or C analysis. The UI must aggressively rely on polite empty states rather than throwing `undefined data` React/Astro errors.
- **Malformed Pipeline JSON**: The `PipelineView` component needs safe fallbacks so an incomplete adjacency list does not break the entire web app build phase.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST process `exports/latest/repos/repositories.json` prior to Astro build via `generate-report-stubs.py` to emit dynamic Starlight Markdown shell files with custom frontmatter.
- **FR-002**: Astro `docsSchema` MUST be updated (extended) to legally pass through injected architectural domain keys without failing the strictly typed build.
- **FR-003**: System MUST update the Starlight application favicon payload to utilize `web/src/assets/atruss-favicon.png`.
- **FR-004**: System MUST render Phase A dashboard components: `OrgHealthStrip`, `LanguageChart`, and `RepoGrid`.
- **FR-005**: System MUST implement `PipelineView.astro` parsing custom JSON Pipeline payloads to generate graphical Mermaid outputs.
- **FR-006**: System MUST implement `ArchitectureView.astro` serving static Arc42 output blocks directly into the DOM layout.
- **FR-007**: System MUST provide a dedicated `/orgs/` comparison leaderboard generating composite maturity ratings against multi-org JSON extractions.

### Key Entities 

- **Discovery Payload**: The Phase A org-wide repository schema array.
- **Pipeline List Schema**: The Phase B workflow representation mapping steps to structural edges.
- **Architectural Hexagonal Manifest**: The Phase C generated Arc42 Markdown payload.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `npm run dev` successfully renders all three nested tab components simultaneously without any client-side JSON request overhead.
- **SC-002**: A brand-new repository passed through the 3-stage python CLI instantly flows fully into the Starlight output upon running `npm run build`.
- **SC-003**: Empty states are 100% resilient; running just the `discover` phase does not break the Phase B and C UI tabs during rendering operations.
- **SC-004**: The Starlight `/favicon.ico` seamlessly resolves the targeted custom `atruss-favicon.png`.

## Assumptions

- We are maintaining the offline, static build model strictly enforced in the previous iteration.
- JSON output formats for the Pipeline Analysis engine will strictly emulate ADO-friendly directed graphs to maintain frontend compatibility.
