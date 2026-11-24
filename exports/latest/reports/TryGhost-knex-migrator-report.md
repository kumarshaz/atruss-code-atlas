---
title: Architecture — TryGhost/knex-migrator
description: Arc42 and Pipeline report for TryGhost/knex-migrator
---

# Repository Architecture Analysis: TryGhost/knex-migrator

## Metadata
- **SHA**: `cb6c132ff7645f6b57b2e7e376a591e32570ddc5`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.73
- **avg_cyclomatic_complexity**: 2.39
- **component_count**: 1
- **dead_code_count**: 11
- **dead_code_symbols**: 11 entry(ies)
- **duplication_pct**: 85.26
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 80
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: TypeScript
- **import_edges**: 100 entry(ies)
- **loc**: 8052
- **max_cognitive_complexity**: 39
- **max_cyclomatic_complexity**: 33
- **sloc**: 6339
- **test_file_count**: 79

# Architecture: TryGhost/knex-migrator

## Context
- **Repository**: `TryGhost/knex-migrator`
- **SHA**: `cb6c132ff7645f6b57b2e7e376a591e32570ddc5`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: TypeScript

## Building Block View

```mermaid
graph TD;
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
    knex_migrator["knex-migrator : MODULE"]:::atlasJob
```

## Component Details
- **knex-migrator** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (60.25/100)
- **Technical Debt Score**: 39.75
- **Estimated Remediation Effort**: 47.24h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.00 | 0.20 | avg_cc=2.39, max_cc=33, duplication=85.26%, dead_code=11 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=19, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 42.00 | 0.15 | avg_cognitive=1.73, max_cognitive=39, fitness_violations=3, oversized_files=3 |
| Pipeline Health | `F` | 58.00 | 0.15 | workflows=2, operational_antipatterns=8, parallel_branches=True |
| Security | `B` | 80.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=1 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (85.26) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (39.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (33.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 19 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@tryghost/database-info` `2.3.19` (npm, `package.json`)
- `@tryghost/errors` `3.4.5` (npm, `package.json`)
- `@tryghost/logging` `5.4.8` (npm, `package.json`)
- `@tryghost/pro-ship` `1.1.9` (npm, `package.json`)
- `@types/node` `26.6.6` (npm, `package.json`)
- `@vitest/coverage-v8` `5.1.0` (npm, `package.json`)
- `commander` `15.1.0` (npm, `package.json`)
- `debug` `4.4.3` (npm, `package.json`)
- `knex` `3.3.0` (npm, `package.json`)
- `knex2` `2.4.2` (npm, `package.json`)
- `mysql2` `3.24.6` (npm, `package.json`)
- `nconf` `0.13.0` (npm, `package.json`)
- `oxfmt` `0.78.0` (npm, `package.json`)
- `oxlint` `1.93.0` (npm, `package.json`)
- `rimraf` `6.1.4` (npm, `package.json`)
- `semver` `7.8.6` (npm, `package.json`)
- `sinon` `22.1.0` (npm, `package.json`)
- `typescript` `7.0.2` (npm, `package.json`)
- `vitest` `5.1.0` (npm, `package.json`)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
  pipeline_root(["TryGhost/knex-migrator"]):::atlasRoot
  subgraph Publish_0["Publish"]
    direction TB
    0_publish["publish"]:::atlasJob
  end
  pipeline_root --> 0_publish
  subgraph Test_Suite_1["Test Suite"]
    direction TB
    1_lint["lint"]:::atlasJob
    1_test["test"]:::atlasJob
    1_ghost_consumer_smoke["ghost-consumer-smoke"]:::atlasJob
    1_required_checks_pass["required-checks-pass"]:::atlasJob
    1_lint --> 1_required_checks_pass
    1_test --> 1_required_checks_pass
    1_ghost_consumer_smoke --> 1_required_checks_pass
    wf_entry_1(["Trigger: Test Suite"]):::atlasWorkflow
    wf_entry_1 --> 1_lint
    wf_entry_1 --> 1_test
    wf_entry_1 --> 1_ghost_consumer_smoke
  end
  pipeline_root --> wf_entry_1
```
