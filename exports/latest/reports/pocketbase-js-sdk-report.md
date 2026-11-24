---
title: Architecture — pocketbase/js-sdk
description: Arc42 and Pipeline report for pocketbase/js-sdk
---

# Repository Architecture Analysis: pocketbase/js-sdk

## Metadata
- **SHA**: `b190b362c7dbb279f2e17b29d3463fda7c158dfd`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.57
- **avg_cyclomatic_complexity**: 3.44
- **component_count**: 19
- **dead_code_count**: 5
- **dead_code_symbols**: 5 entry(ies)
- **duplication_pct**: 70.43
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 47
- **fitness_passed**: False
- **fitness_violation_count**: 11
- **framework**: React (Vite)
- **import_edges**: 100 entry(ies)
- **loc**: 9266
- **max_cognitive_complexity**: 59
- **max_cyclomatic_complexity**: 29
- **sloc**: 6662
- **test_file_count**: 19

# Architecture: pocketbase/js-sdk

## Context
- **Repository**: `pocketbase/js-sdk`
- **SHA**: `b190b362c7dbb279f2e17b29d3463fda7c158dfd`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: React (Vite)

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
    pocketbase["pocketbase : MODULE"]:::atlasJob
    Client["Client : SERVICE"]:::atlasJob
    BackupService["BackupService : SERVICE"]:::atlasJob
    BaseService["BaseService : SERVICE"]:::atlasJob
    BatchService["BatchService : SERVICE"]:::atlasJob
    SubBatchService["SubBatchService : SERVICE"]:::atlasJob
    CollectionService["CollectionService : SERVICE"]:::atlasJob
    CronService["CronService : SERVICE"]:::atlasJob
    CrudService["CrudService : SERVICE"]:::atlasJob
    FileService["FileService : SERVICE"]:::atlasJob
    HealthService["HealthService : SERVICE"]:::atlasJob
    LogService["LogService : SERVICE"]:::atlasJob
    RealtimeService["RealtimeService : SERVICE"]:::atlasJob
    RecordService["RecordService : SERVICE"]:::atlasJob
    SQLService["SQLService : SERVICE"]:::atlasJob
    SettingsService["SettingsService : SERVICE"]:::atlasJob
    AsyncAuthStore["AsyncAuthStore : SERVICE"]:::atlasJob
    BaseAuthStore["BaseAuthStore : SERVICE"]:::atlasJob
    LocalAuthStore["LocalAuthStore : SERVICE"]:::atlasJob
    repo_root(["pocketbase/js-sdk"]):::atlasRoot
    repo_root --> AsyncAuthStore
    repo_root --> BackupService
    repo_root --> BaseAuthStore
    repo_root --> BaseService
    repo_root --> BatchService
    repo_root --> Client
    repo_root --> CollectionService
    repo_root --> CronService
    repo_root --> CrudService
    repo_root --> FileService
    repo_root --> HealthService
    repo_root --> LocalAuthStore
    repo_root --> LogService
    repo_root --> RealtimeService
    repo_root --> RecordService
    repo_root --> SQLService
    repo_root --> SettingsService
    repo_root --> SubBatchService
    repo_root --> pocketbase
```

## Component Details
- **pocketbase** (`package.json`): MODULE
- **Client** (`src/Client.ts`): SERVICE
- **BackupService** (`src/services/BackupService.ts`): SERVICE
- **BaseService** (`src/services/BaseService.ts`): SERVICE
- **BatchService** (`src/services/BatchService.ts`): SERVICE
- **SubBatchService** (`src/services/BatchService.ts`): SERVICE
- **CollectionService** (`src/services/CollectionService.ts`): SERVICE
- **CronService** (`src/services/CronService.ts`): SERVICE
- **CrudService** (`src/services/CrudService.ts`): SERVICE
- **FileService** (`src/services/FileService.ts`): SERVICE
- **HealthService** (`src/services/HealthService.ts`): SERVICE
- **LogService** (`src/services/LogService.ts`): SERVICE
- **RealtimeService** (`src/services/RealtimeService.ts`): SERVICE
- **RecordService** (`src/services/RecordService.ts`): SERVICE
- **SQLService** (`src/services/SQLService.ts`): SERVICE
- **SettingsService** (`src/services/SettingsService.ts`): SERVICE
- **AsyncAuthStore** (`src/stores/AsyncAuthStore.ts`): SERVICE
- **BaseAuthStore** (`src/stores/BaseAuthStore.ts`): SERVICE
- **LocalAuthStore** (`src/stores/LocalAuthStore.ts`): SERVICE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (57.70/100)
- **Technical Debt Score**: 42.30
- **Estimated Remediation Effort**: 57.91h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 42.24 | 0.20 | avg_cc=3.44, max_cc=29, duplication=70.43%, dead_code=5 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=6, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 0.00 | 0.15 | avg_cognitive=3.57, max_cognitive=59, fitness_violations=11, oversized_files=5 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BackupService -> BaseService -> Client -> BackupService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BaseService -> Client -> CollectionService -> CrudService -> BaseService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BaseService -> Client -> CronService -> BaseService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BaseService -> Client -> FileService -> BaseService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BaseService -> Client -> HealthService -> BaseService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BaseService -> Client -> LogService -> BaseService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (BaseService -> Client -> RealtimeService -> BaseService)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Client -> RecordService -> Client)
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (70.43) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (59.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (29.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 6 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@rollup/plugin-terser` `0.4.3` (npm, `package.json`)
- `prettier` `3.2.4` (npm, `package.json`)
- `rollup` `4.0.0` (npm, `package.json`)
- `rollup-plugin-ts` `3.0.0` (npm, `package.json`)
- `typescript` `5.1.6` (npm, `package.json`)
- `vitest` `2.0.0` (npm, `package.json`)


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
  NoWorkflows[No Workflows Detected]:::atlasMore
```
