<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Create a Product Requirement specification that combines my idea of code analysis and generating a complete report on code repository and pipeline visualization combining the discussions in the 2 threads I have.

Make the requirements explicit with all the classification logic applicable for github projects. The product should be handle 4 types of programs as MVP:

1. Python
2. Dotnet
3. React/TypeScript/JavaScript
4. Java with Springboot.
It should also visualize the pipelines as discussed in the other thread.

Here is the full **CodeLens PRS v1.0**, synthesized from both discussion threads and anchored to the Architecture Framework (The Spec is the source of truth — all code/reports are disposable derivatives).

***

# Atruss Code Atlas: Intelligent Repository Analysis \& Pipeline Visualization Platform

**PRS Version 1.0.0-MVP | Status: DRAFT**

The canonical Spec file is attached for download.  Below is the full structured specification.

***

## 1. Intent Declaration

**Product Intent:** Atruss Code Atlas ingests any GitHub repository, performs deep structural/quality/dependency analysis, produces a machine-readable + human-readable report, and renders an interactive visual map of CI/CD pipelines — classified per programming ecosystem, scored, and fully regenerable from the Spec.

**Non-Negotiable Constitution (Policy-as-Code):**

- All classification logic is externalized as YAML/JSON manifests — never hardcoded
- The canonical JSON report is the single source of truth; HTML and PDF are derived artifacts
- Pipeline visualization is a first-class feature, not a post-analysis addon
- New ecosystems are addable via manifest extension with zero engine code changes

***

## 2. MVP Scope Boundary

**In Scope:** GitHub ingestion (public + private), 4 ecosystems (Python, .NET, React/TS/JS, Java Spring Boot), canonical JSON report, HTML/PDF render, GitHub Actions DAG visualization, CVE scanning, secrets detection.

**Out of Scope (Post-MVP):** GitLab/Bitbucket, Rust/Go/Ruby, real-time webhooks, AI-generated code remediation, IDE plugins.

***

## 3. Functional Requirements

### Ingestion

| ID | Requirement | Priority |
| :-- | :-- | :-- |
| FR-ING-01 | Authenticate via OAuth App or Fine-Grained PAT | P0 |
| FR-ING-02 | Clone/shallow-fetch by URL or org/repo slug | P0 |
| FR-ING-03 | Detect primary ecosystem via classification engine (§5) | P0 |
| FR-ING-04 | Support monorepos with mixed ecosystems (per-module units) | P1 |
| FR-ING-05 | Capture commit count, contributors, branch topology, last activity | P0 |
| FR-ING-06 | Index all manifests: requirements.txt, .csproj, package.json, pom.xml, build.gradle | P0 |
| FR-ING-07 | Extract all `.github/workflows/*.yml` files | P0 |

### Code Analysis

| ID | Requirement | Priority |
| :-- | :-- | :-- |
| FR-ANA-01 | Compute LoC per module, file, and language | P0 |
| FR-ANA-02 | Compute Cyclomatic Complexity per function/method | P0 |
| FR-ANA-03 | Compute Cognitive Complexity per class/module | P1 |
| FR-ANA-04 | Detect code duplication % via clone detection | P1 |
| FR-ANA-05 | Detect dead code (unreachable / unused exports) | P1 |
| FR-ANA-06 | Scan dependencies against NIST NVD CVE database | P0 |
| FR-ANA-07 | Detect hardcoded secrets via regex + entropy scan | P0 |
| FR-ANA-08 | Detect outdated dependencies with upgrade paths | P1 |
| FR-ANA-09 | Calculate test coverage % when test artifacts exist | P1 |
| FR-ANA-10 | Produce composite Technical Debt Score | P0 |

### Report Generation

| ID | Requirement | Priority |
| :-- | :-- | :-- |
| FR-RPT-01 | Produce canonical JSON conforming to CodeLens Report Schema v1 | P0 |
| FR-RPT-02 | Render JSON to human-readable HTML report | P0 |
| FR-RPT-03 | Export HTML to PDF | P1 |
| FR-RPT-04 | Executive Summary scorecard (A–F per dimension) | P0 |
| FR-RPT-05 | Dependency Tree with CVE annotations | P0 |
| FR-RPT-06 | Module Complexity Heatmap | P1 |
| FR-RPT-07 | Findings Table (CRITICAL / HIGH / MEDIUM / LOW / INFO) | P0 |
| FR-RPT-08 | Pipeline Topology section linking to visualization | P0 |
| FR-RPT-09 | Version-stamp every report with repo SHA + analysis timestamp | P0 |

### Pipeline Visualization

| ID | Requirement | Priority |
| :-- | :-- | :-- |
| FR-VIZ-01 | Parse all `.github/workflows/*.yml` — extract jobs, steps, triggers, `needs:` | P0 |
| FR-VIZ-02 | Render a DAG (jobs = nodes, `needs:` = directed edges) | P0 |
| FR-VIZ-03 | Each node displays: job name, runner, duration, last run pass/fail status | P0 |
| FR-VIZ-04 | Color-code nodes: green (success), red (failure), yellow (in-progress), gray (skipped) | P0 |
| FR-VIZ-05 | Correctly render parallel vs. sequential job chains | P0 |
| FR-VIZ-06 | Detect pipeline anti-patterns (no cache, no test gate, no artifact handoff) | P1 |
| FR-VIZ-07 | Interactive zoom/pan on DAG (web UI) | P1 |
| FR-VIZ-08 | Export DAG as SVG or PNG | P1 |
| FR-VIZ-09 | Show trigger conditions (push, PR, schedule, manual) as node metadata | P0 |
| FR-VIZ-10 | Detect `workflow_call` / `workflow_run` cross-workflow dependencies as cross-graph edges | P1 |


***

## 4. Ecosystem Classification Logic (Policy-as-Code)

The classification engine evaluates signals in a **priority-ordered rule chain**. First matching rule wins. Rules live in external YAML manifests — behavior changes require manifest edits, not code changes.[^1]

### Python

| Signal | Weight | Detection Rule |
| :-- | :-- | :-- |
| `requirements.txt` | HIGH | Exists in root or subdir |
| `pyproject.toml` | HIGH | Contains `[tool.poetry]` or `[build-system]` |
| `setup.py` / `setup.cfg` | HIGH | File exists |
| `Pipfile` | MEDIUM | File exists |
| `*.py` > 30% LoC | MEDIUM | File extension census |
| `__init__.py` in 2+ dirs | LOW | Module structure signal |
| **Sub-classification** |  | Django / FastAPI / Flask / Generic |

### .NET

| Signal | Weight | Detection Rule |
| :-- | :-- | :-- |
| `*.sln` | HIGH | Solution file exists |
| `*.csproj` / `*.fsproj` | HIGH | Project file exists |
| `global.json` | MEDIUM | File exists |
| `*.cs` > 30% LoC | MEDIUM | Extension census |
| **Sub-classification** |  | ASP.NET Core / Blazor / Worker Service / Console App |

### React / TypeScript / JavaScript

| Signal | Weight | Detection Rule |
| :-- | :-- | :-- |
| `package.json` with `react` dep | HIGH | `dependencies` or `devDependencies` contains `"react"` |
| `tsconfig.json` | HIGH | TypeScript project indicator |
| `*.tsx` > 10% LoC | HIGH | Extension census |
| `next.config.*` | HIGH | Next.js detection |
| `vite.config.*` | MEDIUM | Vite bundler |
| **Sub-classification** |  | Next.js / React SPA (Vite) / React SPA (CRA) / Vanilla TS / Vanilla JS |

### Java Spring Boot

| Signal | Weight | Detection Rule |
| :-- | :-- | :-- |
| `pom.xml` | HIGH | Maven build file |
| `build.gradle` / `build.gradle.kts` | HIGH | Gradle build file |
| `src/main/java` directory | HIGH | Standard Maven layout |
| `*.java` > 30% LoC | MEDIUM | Extension census |
| **Sub-classification** |  | Spring Web / Spring Data JPA / Spring Security / Quarkus / Plain Java |

### Monorepo Conflict Resolution

When multiple ecosystems are detected, each manifest-root subdirectory is treated as an **independent module unit** with its own scorecard. The top-level report aggregates with a weighted composite. Tie-break priority order: **Java > .NET > Python > JS/TS**.[^2]

***

## 5. Pipeline DAG — Node \& Edge Schema

### Node (Job)

- `id`: `{workflow_file}#{job_id}`
- `label`, `runner`, `trigger`, `status`, `steps_count`, `artifacts[]`, `cache_keys[]`


### Edge (`needs:` relationship)

- `source` → `target`, `type`: `sequential | conditional`


### Anti-Pattern Detection Rules

| Anti-Pattern | Detection Logic | Severity |
| :-- | :-- | :-- |
| No test gate before deploy | Deploy job has no upstream test job in `needs:` chain | HIGH |
| No dependency caching | Install step present but no `cache` action | MEDIUM |
| No artifact handoff | Build job has no `upload-artifact` step | MEDIUM |
| Hardcoded secrets in YAML | `env:` value matches secret entropy/regex patterns | CRITICAL |
| Fully sequential pipeline | DAG is a linear chain with zero branches | LOW |
| No branch protection filter | Triggers on push to `main` with no branch filter | HIGH |
| Unlabeled self-hosted runner | `runs-on: self-hosted` with no constraint labels | MEDIUM |


***

## 6. Scorecard Dimensions (A–F Grade)

All 6 dimensions are computed for every repository across all 4 ecosystems:[^2]

- **Code Quality** — Complexity, duplication, dead code
- **Security** — CVE count/severity, secrets exposure
- **Maintainability** — Cognitive complexity, module coupling, LoC distribution
- **Test Coverage** — Coverage % where measurable
- **Dependency Health** — Outdated packages, license risk, CVE count
- **Pipeline Health** — Anti-patterns, parallelism, test gating, artifact hygiene

***

## 7. Non-Functional Requirements (The Constitution)

| NFR | Requirement | Enforcement |
| :-- | :-- | :-- |
| NFR-PERF-01 | Analysis < 500k LoC completes in < 3 min | Async job queue with timeout circuit breaker |
| NFR-SEC-01 | GitHub tokens never persisted beyond session | Ephemeral job context; purged on completion |
| NFR-SEC-02 | CVE data sourced from NIST NVD API (not vendored) | Policy at data source config layer |
| NFR-SCALE-01 | 10 concurrent analyses per tenant | Horizontal containerized workers |
| NFR-EXT-01 | New ecosystem via manifest only (no engine code changes) | Plugin manifest schema enforced by governance |
| NFR-AUDIT-01 | Every report event logged: actor, timestamp, repo identity | Append-only tamper-evident audit log |
| NFR-PORTABILITY-01 | HTML/PDF rendered ONLY from canonical JSON | Render pipeline reads no other source |


***

## 8. Technology Recommendations

| Layer | Technology | Rationale |
| :-- | :-- | :-- |
| Ingestion | GitHub REST v3 + GraphQL v4 | Rate-limit aware, fine-grained PAT support [^3] |
| Python Analysis | Radon, Bandit, pip-audit | Mature, CLI-composable |
| .NET Analysis | Roslyn Analyzers, dotnet-outdated, Security Code Scan | First-party Roslyn AST |
| JS/TS Analysis | ESLint, ts-morph, npm audit, Semgrep | AST-level analysis |
| Java Analysis | PMD, SpotBugs, OWASP Dependency-Check | Industry standard |
| Pipeline Parsing | PyYAML + custom DAG builder | GitHub Actions YAML schema |
| DAG Visualization | React Flow or Cytoscape.js | Interactive, export-capable [^1] |
| Report Rendering | Jinja2 (HTML) + WeasyPrint (PDF) | Deterministic; reads only canonical JSON |
| Orchestration | FastAPI + Celery + Redis | Async job queue |
| Storage | PostgreSQL (metadata) + S3/MinIO (reports) | Durable, versioned artifacts |


***

## 9. Acceptance Criteria — Definition of Done (MVP)

- [ ] Ecosystem classification accuracy > 90% across test fixtures for all 4 ecosystems
- [ ] Canonical JSON report passes schema v1 validation for every analysis run
- [ ] GitHub Actions DAG renders correctly with all jobs, edges, and trigger metadata
- [ ] Known CVE dependency flagged at CRITICAL or HIGH severity
- [ ] Hardcoded secrets detected at ≥ 80% recall against known pattern fixtures
- [ ] DAG export to PNG/SVG is functional
- [ ] All 6 scorecard dimensions produce a grade for all 4 ecosystems
- [ ] Report generation time < 3 minutes for repos under 500k LoC
- [ ] HTML report renders correctly in Chrome, Firefox, and Safari

***

> **Architectural Note:** This document is the immutable Spec. Every code artifact, report template, and visualization component is a disposable, regenerable derivative of this declared intent. If intent changes, update this Spec — do not patch the artifacts.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://github.blog/enterprise-software/ci-cd/build-ci-cd-pipeline-github-actions-four-steps/

[^2]: https://www.reddit.com/r/codereview/comments/1j5xhcn/best_aipowered_code_analysis_tool_for_github_repos/

[^3]: https://www.statsig.com/perspectives/building-custom-cicd-pipelines-with-github-actions

[^4]: https://www.qodo.ai/blog/github-ai-code-review/

[^5]: https://www.devtoolsacademy.com/blog/state-of-ai-code-review-tools-2025/

[^6]: https://dev.to/heraldofsolace/the-6-best-ai-code-review-tools-for-pull-requests-in-2025-4n43

[^7]: https://www.augmentcode.com/tools/best-ai-code-review-tools-2025

[^8]: https://github.com/adityap27/code-quality-report-analyzer

[^9]: https://github.com/resources/articles/ai-code-reviews

[^10]: https://www.youtube.com/watch?v=_UNE39gZrV4

[^11]: https://www.softwareseni.com/spec-driven-development-in-2025-the-complete-guide-to-using-ai-to-write-production-code/

[^12]: https://digital.ai/catalyst-blog/github-cicd/

[^13]: https://www.youtube.com/watch?v=5PdEmeopJVQ

[^14]: https://github.com/YerbaPage/Awesome-Repo-Level-Code-Generation

[^15]: https://github.com/github/awesome-copilot/blob/main/instructions/github-actions-ci-cd-best-practices.instructions.md

