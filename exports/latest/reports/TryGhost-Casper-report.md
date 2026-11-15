---
title: Architecture — TryGhost/Casper
description: Arc42 and Pipeline report for TryGhost/Casper
---

# Repository Architecture Analysis: TryGhost/Casper

## Metadata
- **SHA**: `c0cd68e16dbcf682e6fb316a5fab4bffb4c8a920`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 14.66
- **avg_cyclomatic_complexity**: 8.54
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 81.45
- **file_complexities**: 9 entry(ies)
- **files_analyzed**: 9
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 572
- **max_cognitive_complexity**: 1001
- **max_cyclomatic_complexity**: 607
- **sloc**: 428

# Architecture: TryGhost/Casper

## Context
- **Repository**: `TryGhost/Casper`
- **SHA**: `c0cd68e16dbcf682e6fb316a5fab4bffb4c8a920`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Unknown

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
    casper["casper : MODULE"]:::atlasJob
```

## Component Details
- **casper** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (67.72/100)
- **Technical Debt Score**: 32.28
- **Estimated Remediation Effort**: 29.86h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 27.84 | 0.20 | avg_cc=8.54, max_cc=607, duplication=81.45%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=17, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 32.00 | 0.15 | avg_cognitive=14.66, max_cognitive=1001, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `A` | 94.00 | 0.15 | workflows=1, operational_antipatterns=2, parallel_branches=False |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (81.45) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (1001.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (607.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 17 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@tryghost/release-utils` `0.9.4` (npm, `package.json`)
- `@tryghost/theme-translations` `0.0.22` (npm, `package.json`)
- `autoprefixer` `10.6.2` (npm, `package.json`)
- `beeper` `2.1.0` (npm, `package.json`)
- `cssnano` `9.9.0` (npm, `package.json`)
- `gscan` `6.7.0` (npm, `package.json`)
- `gulp` `5.0.1` (npm, `package.json`)
- `gulp-concat` `2.6.1` (npm, `package.json`)
- `gulp-livereload` `4.0.2` (npm, `package.json`)
- `gulp-postcss` `10.0.0` (npm, `package.json`)
- `gulp-uglify` `3.0.2` (npm, `package.json`)
- `gulp-zip` `6.1.0` (npm, `package.json`)
- `inquirer` `14.3.0` (npm, `package.json`)
- `postcss` `8.5.32` (npm, `package.json`)
- `postcss-color-mod-function` `4.1.1` (npm, `package.json`)
- `postcss-easy-import` `4.0.0` (npm, `package.json`)
- `pump` `3.0.4` (npm, `package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_336d9ccc_14ca_4f62_b546_268b94e761fa["336d9ccc-14ca-4f62-b546-268b94e761fa"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_test_yml_required_checks_pass["test.yml#required-checks-pass"]:::atlasJob
        job_test_yml_test["test.yml#test"]:::atlasJob
    end
    mod_336d9ccc_14ca_4f62_b546_268b94e761fa -->|BUILT_BY| job_test_yml_required_checks_pass
    mod_336d9ccc_14ca_4f62_b546_268b94e761fa -->|BUILT_BY| job_test_yml_test
```

- `336d9ccc-14ca-4f62-b546-268b94e761fa` (code_module) --[BUILT_BY]--> `test.yml#required-checks-pass` (ci_job)
- `336d9ccc-14ca-4f62-b546-268b94e761fa` (code_module) --[BUILT_BY]--> `test.yml#test` (ci_job)


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
  subgraph Test_0["Test"]
    direction TB
    0_test["test"]:::atlasJob
    0_required_checks_pass["required-checks-pass"]:::atlasJob
    0_test --> 0_required_checks_pass
  end
```
