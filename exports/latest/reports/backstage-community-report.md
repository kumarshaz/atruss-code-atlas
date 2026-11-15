---
title: Architecture — backstage/community
description: Arc42 and Pipeline report for backstage/community
---

# Repository Architecture Analysis: backstage/community

## Metadata
- **SHA**: `03225ddb3fa61f75577d748fb362dccf6fb81905`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 7.5
- **avg_cyclomatic_complexity**: 4.67
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 46.78
- **file_complexities**: 1 entry(ies)
- **files_analyzed**: 1
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: Unknown
- **import_edges**: 5 entry(ies)
- **loc**: 177
- **max_cognitive_complexity**: 22
- **max_cyclomatic_complexity**: 10
- **sloc**: 138

# Architecture: backstage/community

## Context
- **Repository**: `backstage/community`
- **SHA**: `03225ddb3fa61f75577d748fb362dccf6fb81905`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    team_sync["team-sync : MODULE"]
```

## Component Details
- **team-sync** (`github-teams/package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (70.94/100)
- **Technical Debt Score**: 29.06
- **Estimated Remediation Effort**: 18.12h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 68.32 | 0.20 | avg_cc=4.67, max_cc=10, duplication=46.78%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=2, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `B` | 83.50 | 0.15 | avg_cognitive=7.50, max_cognitive=22, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (46.78) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 2 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@octokit/rest` `18.0.0` (npm, `github-teams/package.json`)
- `js-yaml` `4.3.2` (npm, `github-teams/package.json`)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
