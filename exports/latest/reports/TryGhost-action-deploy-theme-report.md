---
title: Architecture — TryGhost/action-deploy-theme
description: Arc42 and Pipeline report for TryGhost/action-deploy-theme
---

# Repository Architecture Analysis: TryGhost/action-deploy-theme

## Metadata
- **SHA**: `89f9b471c2f4fd894363a9af01d9f92a84ca79c0`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.14
- **avg_cyclomatic_complexity**: 4.29
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 77.67
- **file_complexities**: 8 entry(ies)
- **files_analyzed**: 8
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: TypeScript
- **import_edges**: 40 entry(ies)
- **loc**: 937
- **max_cognitive_complexity**: 17
- **max_cyclomatic_complexity**: 12
- **sloc**: 795
- **test_file_count**: 4

# Architecture: TryGhost/action-deploy-theme

## Context
- **Repository**: `TryGhost/action-deploy-theme`
- **SHA**: `89f9b471c2f4fd894363a9af01d9f92a84ca79c0`
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
    action_deploy_theme["action-deploy-theme : MODULE"]:::atlasJob
```

## Component Details
- **action-deploy-theme** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (86.32/100)
- **Technical Debt Score**: 13.68
- **Estimated Remediation Effort**: 20.95h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 69.84 | 0.20 | avg_cc=4.29, max_cc=12, duplication=77.67%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=13, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 94.00 | 0.15 | avg_cognitive=3.14, max_cognitive=17, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `A` | 100.00 | 0.15 | workflows=3, operational_antipatterns=1, parallel_branches=True |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (77.67) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 13 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@actions/core` `3.0.1` (npm, `package.json`)
- `@actions/exec` `3.0.0` (npm, `package.json`)
- `@tryghost/admin-api` `1.14.14` (npm, `package.json`)
- `@tryghost/pro-ship` `2.0.1` (npm, `package.json`)
- `@types/node` `26.6.6` (npm, `package.json`)
- `@types/slug` `5.0.9` (npm, `package.json`)
- `@vercel/ncc` `0.45.0` (npm, `package.json`)
- `@vitest/coverage-v8` `5.1.0` (npm, `package.json`)
- `oxfmt` `0.78.0` (npm, `package.json`)
- `oxlint` `1.93.0` (npm, `package.json`)
- `slug` `12.0.1` (npm, `package.json`)
- `typescript` `7.0.2` (npm, `package.json`)
- `vitest` `5.1.0` (npm, `package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69["fb8332e4-82f3-43fa-8d5b-310cc9c56f69"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_major_yml_update_major["major.yml#update-major"]:::atlasJob
        job_sync_dist_yml_rebuild_dist["sync-dist.yml#rebuild-dist"]:::atlasJob
        job_sync_dist_yml_sync_dist["sync-dist.yml#sync-dist"]:::atlasJob
        job_test_yml_check_dist["test.yml#check-dist"]:::atlasJob
        job_test_yml_required_checks_pass["test.yml#required-checks-pass"]:::atlasJob
        job_test_yml_test["test.yml#test"]:::atlasJob
        job_test_yml_validate["test.yml#validate"]:::atlasJob
    end
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_major_yml_update_major
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_sync_dist_yml_rebuild_dist
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_sync_dist_yml_sync_dist
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_test_yml_check_dist
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_test_yml_required_checks_pass
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_test_yml_test
    mod_fb8332e4_82f3_43fa_8d5b_310cc9c56f69 -->|BUILT_BY| job_test_yml_validate
```

- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `major.yml#update-major` (ci_job)
- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `sync-dist.yml#rebuild-dist` (ci_job)
- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `sync-dist.yml#sync-dist` (ci_job)
- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `test.yml#check-dist` (ci_job)
- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `test.yml#required-checks-pass` (ci_job)
- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `test.yml#test` (ci_job)
- `fb8332e4-82f3-43fa-8d5b-310cc9c56f69` (code_module) --[BUILT_BY]--> `test.yml#validate` (ci_job)


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
  pipeline_root(["TryGhost/action-deploy-theme"]):::atlasRoot
  subgraph Update_Major_Version_Tag_0["Update Major Version Tag"]
    direction TB
    0_update_major["update-major"]:::atlasJob
  end
  pipeline_root --> 0_update_major
  subgraph Sync_dist_1["Sync dist"]
    direction TB
    1_rebuild_dist["rebuild-dist"]:::atlasJob
    1_sync_dist["sync-dist"]:::atlasJob
    1_rebuild_dist --> 1_sync_dist
  end
  pipeline_root --> 1_rebuild_dist
  subgraph CI_2["CI"]
    direction TB
    2_validate["validate"]:::atlasJob
    2_test["test"]:::atlasJob
    2_check_dist["check-dist"]:::atlasJob
    2_required_checks_pass["required-checks-pass"]:::atlasJob
    2_validate --> 2_required_checks_pass
    2_test --> 2_required_checks_pass
    2_check_dist --> 2_required_checks_pass
    wf_entry_2(["Trigger: CI"]):::atlasWorkflow
    wf_entry_2 --> 2_validate
    wf_entry_2 --> 2_test
    wf_entry_2 --> 2_check_dist
  end
  pipeline_root --> wf_entry_2
```
