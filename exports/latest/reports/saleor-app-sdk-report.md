---
title: Architecture — saleor/app-sdk
description: Arc42 and Pipeline report for saleor/app-sdk
---

# Repository Architecture Analysis: saleor/app-sdk

## Metadata
- **SHA**: `1db77f862352aa95aa807f00d83921c06051b5ba`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.07
- **avg_cyclomatic_complexity**: 1.96
- **component_count**: 7
- **dead_code_count**: 6
- **dead_code_symbols**: 6 entry(ies)
- **duplication_pct**: 80.96
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 187
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Next.js
- **import_edges**: 100 entry(ies)
- **loc**: 17702
- **max_cognitive_complexity**: 29
- **max_cyclomatic_complexity**: 16
- **sloc**: 13588
- **test_file_count**: 66

# Architecture: saleor/app-sdk

## Context
- **Repository**: `saleor/app-sdk`
- **SHA**: `1db77f862352aa95aa807f00d83921c06051b5ba`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Next.js

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
    _saleor_app_sdk["@saleor/app-sdk : MODULE"]:::atlasJob
    DynamoAPLRepository["DynamoAPLRepository : DATA_ACCESS_LAYER"]:::atlasJob
    MemoryAPLRepository["MemoryAPLRepository : DATA_ACCESS_LAYER"]:::atlasJob
    AppContext["AppContext : UI_COMPONENT"]:::atlasJob
    AppBridgeProvider["AppBridgeProvider : UI_COMPONENT"]:::atlasJob
    ProductDetailsWidgetPage["ProductDetailsWidgetPage : UI_COMPONENT"]:::atlasJob
    RoutePropagator["RoutePropagator : UI_COMPONENT"]:::atlasJob
    repo_root(["saleor/app-sdk"]):::atlasRoot
    repo_root --> _saleor_app_sdk
    DynamoAPLRepository --> MemoryAPLRepository
    MemoryAPLRepository --> DynamoAPLRepository
    ProductDetailsWidgetPage --> AppBridgeProvider
    ProductDetailsWidgetPage --> AppContext
    RoutePropagator --> AppBridgeProvider
    RoutePropagator --> AppContext
    linkStyle 1 stroke:#ba1a1a,stroke-width:2px,stroke-dasharray: 5 5
```

## Component Details
- **@saleor/app-sdk** (`package.json`): MODULE
- **DynamoAPLRepository** (`src/APL/dynamodb/dynamo-apl-repository.ts`): DATA_ACCESS_LAYER (deps: MemoryAPLRepository)
- **MemoryAPLRepository** (`src/APL/dynamodb/memory-apl-repository.ts`): DATA_ACCESS_LAYER (deps: DynamoAPLRepository)
- **AppContext** (`src/app-bridge/app-bridge-provider.tsx`): UI_COMPONENT
- **AppBridgeProvider** (`src/app-bridge/app-bridge-provider.tsx`): UI_COMPONENT
- **ProductDetailsWidgetPage** (`src/app-bridge/use-widget-auto-resize.ts`): UI_COMPONENT (deps: AppBridgeProvider, AppContext)
- **RoutePropagator** (`src/app-bridge/next/route-propagator.tsx`): UI_COMPONENT (deps: AppBridgeProvider, AppContext)

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (65.97/100)
- **Technical Debt Score**: 34.03
- **Estimated Remediation Effort**: 43.70h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 61.50 | 0.20 | avg_cc=1.96, max_cc=16, duplication=80.96%, dead_code=6 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=904, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `D` | 62.50 | 0.15 | avg_cognitive=1.07, max_cognitive=29, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `D` | 64.00 | 0.15 | workflows=3, operational_antipatterns=7, parallel_branches=True |
| Security | `F` | 46.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=3 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (DynamoAPLRepository -> MemoryAPLRepository -> DynamoAPLRepository)
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (80.96) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (29.0) exceeds policy threshold (25.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 904 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `src/app-bridge/use-dashboard-token.test.ts:12` (`const VALID_TOKEN = "eyJh***REDACTED***";`)

### Inventory Sample
- `@aws-sdk/client-dynamodb` `3.848.0` (npm, `package.json`)
- `@aws-sdk/client-dynamodb` `3.848.0` (npm, `pnpm-lock.yaml`)
- `@aws-sdk/lib-dynamodb` `3.850.0` (npm, `package.json`)
- `@aws-sdk/lib-dynamodb` `3.850.0` (npm, `pnpm-lock.yaml`)
- `@aws-sdk/util-dynamodb` `3.848.0` (npm, `package.json`)
- `@aws-sdk/util-dynamodb` `3.848.0` (npm, `pnpm-lock.yaml`)
- `@changesets/cli` `2.28.1` (npm, `package.json`)
- `@changesets/cli` `2.28.1` (npm, `pnpm-lock.yaml`)
- `@opentelemetry/api` `1.9.0` (npm, `package.json`)
- `@opentelemetry/api` `1.9.0` (npm, `pnpm-lock.yaml`)
- `@opentelemetry/semantic-conventions` `1.30.0` (npm, `package.json`)
- `@opentelemetry/semantic-conventions` `1.30.0` (npm, `pnpm-lock.yaml`)
- `@testing-library/dom` `10.4.0` (npm, `package.json`)
- `@testing-library/dom` `10.4.0` (npm, `pnpm-lock.yaml`)
- `@testing-library/react` `16.2.0` (npm, `package.json`)
- `@testing-library/react` `16.2.0` (npm, `pnpm-lock.yaml`)
- `@types/aws-lambda` `8.10.147` (npm, `package.json`)
- `@types/aws-lambda` `8.10.147` (npm, `pnpm-lock.yaml`)
- `@types/debug` `4.1.12` (npm, `package.json`)
- `@types/debug` `4.1.12` (npm, `pnpm-lock.yaml`)
- `@types/node` `12.20.55` (npm, `pnpm-lock.yaml`)
- `@types/node` `22.19.6` (npm, `package.json`)
- `@types/node` `22.19.6` (npm, `pnpm-lock.yaml`)
- `@types/react` `19.0.10` (npm, `package.json`)
- `@types/react` `19.0.10` (npm, `pnpm-lock.yaml`)
- `@types/react-dom` `19.0.4` (npm, `package.json`)
- `@types/react-dom` `19.0.4` (npm, `pnpm-lock.yaml`)
- `@typescript-eslint/eslint-plugin` `5.36.1` (npm, `package.json`)
- `@typescript-eslint/eslint-plugin` `5.36.1` (npm, `pnpm-lock.yaml`)
- `@typescript-eslint/parser` `5.36.1` (npm, `package.json`)
- ... (+874 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_4e591fe9_cb12_4f6a_950a_d386f78fe746["4e591fe9-cb12-4f6a-950a-d386f78fe746"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_assign_pr_yml_assign_creator["assign-pr.yml#assign_creator"]:::atlasJob
        job_main_yml_build["main.yml#build"]:::atlasJob
        job_main_yml_lint["main.yml#lint"]:::atlasJob
        job_main_yml_test["main.yml#test"]:::atlasJob
        job_prepare_release_yml_release["prepare-release.yml#release"]:::atlasJob
    end
    mod_4e591fe9_cb12_4f6a_950a_d386f78fe746 -->|BUILT_BY| job_assign_pr_yml_assign_creator
    mod_4e591fe9_cb12_4f6a_950a_d386f78fe746 -->|BUILT_BY| job_main_yml_build
    mod_4e591fe9_cb12_4f6a_950a_d386f78fe746 -->|BUILT_BY| job_main_yml_lint
    mod_4e591fe9_cb12_4f6a_950a_d386f78fe746 -->|BUILT_BY| job_main_yml_test
    mod_4e591fe9_cb12_4f6a_950a_d386f78fe746 -->|DEPLOYED_BY| job_prepare_release_yml_release
```

- `4e591fe9-cb12-4f6a-950a-d386f78fe746` (code_module) --[BUILT_BY]--> `assign-pr.yml#assign_creator` (ci_job)
- `4e591fe9-cb12-4f6a-950a-d386f78fe746` (code_module) --[BUILT_BY]--> `main.yml#build` (ci_job)
- `4e591fe9-cb12-4f6a-950a-d386f78fe746` (code_module) --[BUILT_BY]--> `main.yml#lint` (ci_job)
- `4e591fe9-cb12-4f6a-950a-d386f78fe746` (code_module) --[BUILT_BY]--> `main.yml#test` (ci_job)
- `4e591fe9-cb12-4f6a-950a-d386f78fe746` (code_module) --[DEPLOYED_BY]--> `prepare-release.yml#release` (ci_job)


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
  pipeline_root(["saleor/app-sdk"]):::atlasRoot
  subgraph Assign_PR_to_creator_0["Assign PR to creator"]
    direction TB
    0_assign_creator["assign_creator"]:::atlasJob
  end
  pipeline_root --> 0_assign_creator
  subgraph QA_1["QA"]
    direction TB
    1_lint["lint"]:::atlasJob
    1_test["test"]:::atlasJob
    1_build["build"]:::atlasJob
    wf_entry_1(["Trigger: QA"]):::atlasWorkflow
    wf_entry_1 --> 1_lint
    wf_entry_1 --> 1_test
    wf_entry_1 --> 1_build
  end
  pipeline_root --> wf_entry_1
  subgraph Open_release_2["Open release"]
    direction TB
    2_release["release"]:::atlasJob
  end
  pipeline_root --> 2_release
```
