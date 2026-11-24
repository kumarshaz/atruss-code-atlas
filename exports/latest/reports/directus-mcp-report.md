---
title: Architecture — directus/mcp
description: Arc42 and Pipeline report for directus/mcp
---

# Repository Architecture Analysis: directus/mcp

## Metadata
- **SHA**: `472ce5b8dd3ddda45dba2a494cc024467a601ff4`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 4.41
- **avg_cyclomatic_complexity**: 4.12
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 63.48
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 36
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: TypeScript
- **import_edges**: 100 entry(ies)
- **loc**: 2312
- **max_cognitive_complexity**: 59
- **max_cyclomatic_complexity**: 32
- **sloc**: 1866

# Architecture: directus/mcp

## Context
- **Repository**: `directus/mcp`
- **SHA**: `472ce5b8dd3ddda45dba2a494cc024467a601ff4`
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
    _directus_content_mcp["@directus/content-mcp : MODULE"]:::atlasJob
```

## Component Details
- **@directus/content-mcp** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (64.65/100)
- **Technical Debt Score**: 35.35
- **Estimated Remediation Effort**: 26.03h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 45.52 | 0.20 | avg_cc=4.12, max_cc=32, duplication=63.48%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=474, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 57.00 | 0.15 | avg_cognitive=4.41, max_cognitive=59, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (63.48) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (59.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (32.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 474 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@directus/eslint-config` `0.1.0` (npm, `package.json`)
- `@directus/eslint-config` `0.1.0` (npm, `pnpm-lock.yaml`)
- `@directus/sdk` `19.1.0` (npm, `package.json`)
- `@directus/sdk` `19.1.0` (npm, `pnpm-lock.yaml`)
- `@directus/tsconfig` `3.0.0` (npm, `package.json`)
- `@directus/tsconfig` `3.0.0` (npm, `pnpm-lock.yaml`)
- `@directus/types` `13.1.0` (npm, `package.json`)
- `@directus/types` `13.1.0` (npm, `pnpm-lock.yaml`)
- `@modelcontextprotocol/sdk` `1.10.2` (npm, `package.json`)
- `@modelcontextprotocol/sdk` `1.10.2` (npm, `pnpm-lock.yaml`)
- `@types/node` `22.15.3` (npm, `package.json`)
- `@types/node` `22.15.3` (npm, `pnpm-lock.yaml`)
- `dotenv` `16.5.0` (npm, `package.json`)
- `dotenv` `16.5.0` (npm, `pnpm-lock.yaml`)
- `eslint` `9.25.1` (npm, `package.json`)
- `eslint` `9.25.1` (npm, `pnpm-lock.yaml`)
- `isomorphic-dompurify` `2.24.0` (npm, `package.json`)
- `isomorphic-dompurify` `2.24.0` (npm, `pnpm-lock.yaml`)
- `marked` `15.0.11` (npm, `package.json`)
- `marked` `15.0.11` (npm, `pnpm-lock.yaml`)
- `typescript` `5.8.3` (npm, `package.json`)
- `typescript` `5.8.3` (npm, `pnpm-lock.yaml`)
- `zod` `3.24.3` (npm, `pnpm-lock.yaml`)
- `zod` `4.0.0-beta.20250424T163858` (npm, `package.json`)
- `zod` `4.0.0-beta.20250424T163858` (npm, `pnpm-lock.yaml`)
- `@asamuzakjp/css-color` `3.1.5` (npm, `pnpm-lock.yaml`)
- `@babel/code-frame` `7.27.1` (npm, `pnpm-lock.yaml`)
- `@babel/helper-string-parser` `7.27.1` (npm, `pnpm-lock.yaml`)
- `@babel/helper-validator-identifier` `7.27.1` (npm, `pnpm-lock.yaml`)
- `@babel/parser` `7.27.1` (npm, `pnpm-lock.yaml`)
- ... (+444 more dependencies)


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
