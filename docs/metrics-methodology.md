# Metrics & Scoring Methodology

**How Atruss Code Atlas derives every score, grade, complexity metric, and maturity index.**

Atruss Code Atlas is built on **deterministic, zero-agent static analysis**. Every number surfaced in the Web Portal, Arc42 Markdown reports, SARIF outputs, and MCP responses is computed reproducibly from source ASTs, CI/CD workflow YAML, dependency manifests, and declarative policy-as-code rules—without opaque heuristics or LLM guesswork.

---

## 1. Scoring Philosophy

1. **Deterministic & Reproducible**: Identical repository snapshots always produce byte-identical scores and grades (`0–100` clamped to `[0.0, 100.0]`, rounded to 2 decimal places).
2. **Baseline-of-100 Deduction Model**: Each dimension starts from a clean baseline (`100.0`) and applies bounded, severity-weighted deductions for verifiable findings (or explicit structural baselines when telemetry like coverage reports is absent).
3. **Policy-as-Code Transparency**: Security, pipeline, and architecture fitness thresholds live in versioned YAML manifests ([`manifests/pipeline-rules.yaml`](../manifests/pipeline-rules.yaml), [`manifests/architecture-rules.yaml`](../manifests/architecture-rules.yaml)) and pure Python scoring functions ([`src/analyzers/scorecard.py`](../src/analyzers/scorecard.py)).
4. **Actionable Remediation**: Every score pairs with exact file/line evidence and a deterministic `remediation_hours` estimate so teams can prioritize engineering effort.

---

## 2. 6-Dimension A–F Repository Scorecard

Implemented in [`compute_repository_scorecard()`](../src/analyzers/scorecard.py#L246-L494).

### Letter Grade Scale

| Grade | Score Range | Interpretation |
| :---: | :---: | :--- |
| **A** | `90.0 – 100.0` | Exemplary engineering hygiene, low debt, strong CI/CD & security posture |
| **B** | `80.0 – 89.99` | Healthy production posture with minor localized findings |
| **C** | `70.0 – 79.99` | Moderate technical debt or missing guardrails requiring planned cleanup |
| **D** | `60.0 – 69.99` | Elevated architectural, security, or pipeline risk |
| **F** | `< 60.0` | Critical debt, unmitigated vulnerabilities, or missing core delivery gates |

### Weighted Composite Formula

$$\text{overall\_score} = \sum_{d=1}^{6} (\text{score}_d \times \text{weight}_d)$$

$$\text{technical\_debt\_score} = 100.0 - \text{overall\_score}$$

| Dimension | Weight | Primary Signals | Exact Calculation (`100 - penalty`, clamped `[0, 100]`) |
| :--- | :---: | :--- | :--- |
| **Code Quality** | **20%** | Cyclomatic Complexity, AST Clone Duplication %, Dead Code | Deductions:<br>• `avg_cc > 3.0`: `min(30, (avg_cc - 3.0) * 4.0)`<br>• `max_cc > 15.0`: `min(25, (max_cc - 15.0) * 1.5)`<br>• `duplication_pct > 0`: `min(25, duplication_pct * 1.5)`<br>• `dead_code_count > 0`: `min(20, dead_code_count * 2.0)` |
| **Security** | **20%** | OSV Vulnerabilities, Secret Findings, Pipeline Security Anti-Patterns (`AP-004`, `AP-008`–`AP-014`) | Severity-weighted deductions:<br>• **OSV Vulns**: `CRITICAL -25`, `HIGH -15`, `MEDIUM -7`, `LOW -2`<br>• **Secrets**: `CRITICAL -25`, `HIGH -18`, `MEDIUM -10`, `LOW -5`<br>• **Pipeline Security**: `CRITICAL -20`, `HIGH -12`, `MEDIUM -6`, `LOW -2` |
| **Maintainability** | **15%** | Cognitive Complexity, Architecture Fitness Violations, Oversized Files (`> 500` LOC) | Deductions:<br>• `avg_cognitive > 5.0`: `min(25, (avg_cognitive - 5.0) * 3.0)`<br>• `max_cognitive > 20.0`: `min(25, (max_cognitive - 20.0) * 1.5)`<br>• **Fitness Violations**: `CRITICAL -18`, `HIGH -12`, `MEDIUM -6`, `LOW -2`<br>• **Oversized Files**: `min(20, oversized_files * 5.0)` |
| **Test Coverage** | **15%** | Coverage Report %, CI Test Jobs, Detected Test Files | • **When coverage `%` is present**: `coverage_pct + (5.0 if ci_test_job else 0.0)`<br>• **When coverage `%` is unavailable**: `70.0` if CI test job or test files are detected; otherwise `40.0` |
| **Dependency Health** | **15%** | Lockfile Presence, Outdated Ratio, Vulnerable Dependency Ratio | • **No manifests/deps parsed**: `90.0` (minus `min(60, vulns * 15)` if external vulns exist)<br>• **With manifests**: `-15.0` if manifest exists without a lockfile; `-(outdated_count / total) * 35.0`; `-(vulnerable_count / total) * 50.0` |
| **Pipeline Health** | **15%** | Operational CI/CD Anti-Patterns, Parallel Branching | • **0 workflows**: `40.0`<br>• **With workflows**: `100.0 - op_penalties + (5.0 if parallel_branches else 0.0)` where operational anti-pattern penalties are `CRITICAL -20`, `HIGH -12`, `MEDIUM -6`, `LOW -3` |

### Deterministic Remediation Hours

`remediation_hours` estimates engineering effort by summing fixed severity effort weights plus structural cleanup baselines:
- **OSV Vulnerabilities**: `CRITICAL 4.0h`, `HIGH 2.0h`, `MEDIUM 1.0h`, `LOW 0.5h`
- **Secret Findings**: `2.0h` per finding
- **Architecture Fitness Violations**: `CRITICAL 4.0h`, `HIGH 2.5h`, `MEDIUM 1.5h`, `LOW 0.5h`
- **Pipeline Anti-Patterns**: `CRITICAL 2.0h`, `HIGH 1.5h`, `MEDIUM 1.0h`, `LOW 0.5h`
- **Structural Cleanup**: `(dead_code_count * 0.25h) + (duplication_pct / 5.0h) + (oversized_files * 1.5h) + (technical_debt_score * 0.25h)`

---

## 3. Engineering Maturity Leaderboard Index

The **Organization Maturity Score (`0 – 100`)** on the Executive Leaderboard ([`web/src/components/LeaderboardView.astro`](../web/src/components/LeaderboardView.astro), pre-computed into `exports/latest/orgs-summary.json` by [`scripts/generate-org-summary.py`](../scripts/generate-org-summary.py)) measures how consistently an organization automates and governs its delivery pipelines:

$$\text{maturity\_score} = (0.60 \times \text{pipeline\_coverage\_pct}) + \left(0.40 \times \frac{\text{clean\_pipelined\_repos}}{\text{evaluated\_pipelined\_repos}} \times 100\right)$$

- **60% CI/CD Pipeline Adoption**: Percentage of the organization's repositories with at least one parsed CI/CD workflow.
- **40% Clean Anti-Pattern Compliance**: Percentage of evaluated pipelined repositories that have **zero** CI/CD operational or security anti-patterns. If an organization has `0` pipelined repositories, its maturity score is `0`.
- **Complementary Columns**:
  - **6-D Scorecard**: Mean `overall_score` and corresponding `A–F` grade across analyzed repositories in the organization.
  - **Security & Fitness**: Total open OSV CVEs and architectural fitness rule violations aggregated across the organization.

---

## 4. Structural Code, Complexity & Graph Metrics

Implemented in [`src/analyzers/code/treesitter_engine.py`](../src/analyzers/code/treesitter_engine.py) using `tree-sitter` Concrete Syntax Trees for **Python, C# (.NET), TypeScript/TSX, JavaScript, and Java** (with line/module structural fallbacks in [`src/analyzers/code/orchestrator.py`](../src/analyzers/code/orchestrator.py) for Go, Rust, Ruby, PHP, Elixir, and Container/Helm/IaC):

- **Cyclomatic Complexity (CC)**: Starts at `1` per function/method and increments for every decision branch (`if`, `elif`, `for`, `while`, `case`, `catch`, ternary `?:`, and boolean short-circuit operators `&&` / `||` / `and` / `or`).
- **Cognitive Complexity**: Increments for control-flow breaks and adds a **nesting-depth penalty** (`+depth`) for nested branches, capturing human readability overhead rather than pure path count.
- **AST Clone Duplication %**: Normalizes identifiers, string literals, and numeric constants across sliding token windows (`CLONE_MIN_TOKENS = 15`) and hashes windows to detect Type-1 and Type-2 structural clones without false positives from variable renames.
- **Dead Code Count**: Identifies unreferenced private/internal functions and symbols across the repository's internal call/import graph.
- **Blast Radius (PageRank & Betweenness Centrality)**: Builds a directed dependency graph across internal modules and CI/CD jobs using `networkx`, surfacing high-centrality "hub" components where a change or failure cascades furthest.

---

## 5. CI/CD Pipeline & Architecture Fitness Rules

- **14-Rule CI/CD Policy Engine ([`manifests/pipeline-rules.yaml`](../manifests/pipeline-rules.yaml))**:
  - **Operational (`AP-001`–`AP-007`)**: `NO_TEST_GATE`, `NO_CACHE`, `NO_ARTIFACT_HANDOFF`, `SEQUENTIAL_ONLY`, `UNFILTERED_MAIN_PUSH`, `UNLABELED_SELF_HOSTED` (plus `HARDCODED_SECRET`).
  - **Supply-Chain Security (`AP-008`–`AP-014`)**: `UNPINNED_ACTION`, `TEMPLATE_INJECTION`, `PWN_REQUEST_RISK`, `EXCESSIVE_PERMISSIONS`, `NO_TIMEOUT` (`ATRUSS-PIPE-012`), `ARTIFACT_CREDENTIAL_PERSISTENCE`, `STATIC_CLOUD_CREDENTIALS`.
- **Architecture Fitness Functions ([`manifests/architecture-rules.yaml`](../manifests/architecture-rules.yaml))**: Evaluates declarative layer-dependency rules (`ATRUSS-ARCH-001`–`ATRUSS-ARCH-005`) against internal import edges and detects circular module cycles (`nx.simple_cycles`).
- **Supply-Chain & SBOM**: Parses lockfiles and manifests across 9 dependency ecosystems (`Python`, `.NET`, `JavaScript/TypeScript`, `Java`, `Go`, `Rust`, `Ruby`, `PHP`, `Elixir`)—while `infra_devops` covers Docker, Helm, Kubernetes, and Terraform assets without package lockfiles—to emit offline-capable **CycloneDX v1.6** SBOMs and match package PURLs/versions against cached or opt-in live **OSV** advisories. *(Note: `DependencyRecord.is_outdated` defaults to `False` in offline scans because registry-latest version lookup is not yet populated in `src/analyzers/dependencies/`.)*
