---
title: Architecture — github-samples/pets-workshop
description: Arc42 and Pipeline report for github-samples/pets-workshop
---

# Repository Architecture Analysis: github-samples/pets-workshop

## Metadata
- **SHA**: `d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.94
- **avg_cyclomatic_complexity**: 1.89
- **component_count**: 6
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 68.88
- **file_complexities**: 15 entry(ies)
- **files_analyzed**: 15
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: Astro
- **import_edges**: 75 entry(ies)
- **loc**: 880
- **max_cognitive_complexity**: 11
- **max_cyclomatic_complexity**: 9
- **sloc**: 653
- **test_file_count**: 5

# Architecture: github-samples/pets-workshop

## Context
- **Repository**: `github-samples/pets-workshop`
- **SHA**: `d2437a6f3dbb1fe4bd5e97790ccc12c42cbfc03a`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Astro

## Building Block View

```mermaid
graph TD;
    %% title: Building Block View — github-samples/pets-workshop
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
    dog_shelter["dog-shelter : MODULE"]:::atlasJob
    get_dogs["get_dogs : API_ROUTE"]:::atlasJob
    get_dog["get_dog : API_ROUTE"]:::atlasJob
    BaseModel["BaseModel : DATA_ACCESS_LAYER"]:::atlasJob
    Breed["Breed : DATA_ACCESS_LAYER"]:::atlasJob
    Dog["Dog : DATA_ACCESS_LAYER"]:::atlasJob
    repo_root(["github-samples/pets-workshop"]):::atlasRoot
    repo_root --> dog_shelter
    Breed --> BaseModel
    Dog --> BaseModel
    get_dog --> Breed
    get_dog --> Dog
    get_dogs --> Breed
    get_dogs --> Dog
```

## Component Details
- **dog-shelter** (`app/client/package.json`): MODULE
- **get_dogs** (`app/server/app.py`): API_ROUTE (deps: Breed, Dog)
- **get_dog** (`app/server/app.py`): API_ROUTE (deps: Breed, Dog)
- **BaseModel** (`app/server/models/base.py`): DATA_ACCESS_LAYER
- **Breed** (`app/server/models/breed.py`): DATA_ACCESS_LAYER (deps: BaseModel)
- **Dog** (`app/server/models/dog.py`): DATA_ACCESS_LAYER (deps: BaseModel)

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (60.29/100)
- **Technical Debt Score**: 39.71
- **Estimated Remediation Effort**: 110.20h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `C` | 75.00 | 0.20 | avg_cc=1.89, max_cc=9, duplication=68.88%, dead_code=0 |
| Dependency Health | `A` | 97.91 | 0.15 | dependencies=407, outdated=0, vulnerable=17, has_lockfile=True |
| Maintainability | `A` | 94.00 | 0.15 | avg_cognitive=0.94, max_cognitive=11, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=85, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (68.88) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 407 | **Vulnerabilities**: 85 | **Secrets**: 0

### Known Vulnerabilities (OSV)
- **[MEDIUM] `GHSA-26w7-cxv4-gfx2`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-26w7-cxv4-gfx2`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-2883-xcg3-v3hh`** `js-yaml` `4.1.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-28wg-ghj8-5hjv`** `nanoid` `3.3.11` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-2p49-hgcm-8545`** `svgo` `4.0.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-2pvr-wf23-7pc7`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-2pvr-wf23-7pc7`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-2v37-7h3g-55p8`** `nanoid` `3.3.11` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-376h-93r7-7g6f`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-376h-93r7-7g6f`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-38fc-9xqv-7f7q`** `sqlalchemy` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-4g3v-8h47-v7g6`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-4g3v-8h47-v7g6`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-4grg-w6v8-c28g`** `flask` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-4q55-j62x-fr9h`** `devalue` `5.7.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-4vpr-x523-8j87`** `svgo` `4.0.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-52cp-r559-cp3m`** `js-yaml` `4.1.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-562c-5r94-xh97`** `flask` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-587h-7wmj-h5pm`** `vite` `7.3.2` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-5p4m-2wfm-xmqj`** `js-yaml` `4.1.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-5wv5-4vpf-pj6m`** `flask` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-68fv-2mgg-jv7q`** `source-map-js` `1.2.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-68rp-wp8r-4726`** `flask` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-698v-4r3x-3vcv`** `vite` `7.3.2` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-6g55-p6wh-862q`** `postcss` `8.5.6` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-77vg-94rm-hx3p`** `devalue` `5.7.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-7pw4-f3q4-r2p2`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-7pw4-f3q4-r2p2`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-7w5x-hrqm-74c2`** `smol-toml` `1.6.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-887w-45rq-vxgf`** `sqlalchemy` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-8hv8-536x-4wqp`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-8hv8-536x-4wqp`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-98hj-9722-w3j8`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-98hj-9722-w3j8`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-9jrq-w75r-8gcw`** `vite` `7.3.2` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-9rgm-9g3h-6x36`** `devalue` `5.7.1` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-c57f-mm3j-27q9`** `@astrojs/node` `10.0.4` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-c57f-mm3j-27q9`** `@astrojs/node` `10.0.4` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-f48w-9m4c-m7f5`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-f48w-9m4c-m7f5`** `astro` `6.1.6` (fixed: `none`, REACHABLE_FROM_RUNTIME)

### Inventory Sample
- `flask` `*` (PyPI, `app/server/requirements.txt`)
- `flask_sqlalchemy` `*` (PyPI, `app/server/requirements.txt`)
- `sqlalchemy` `*` (PyPI, `app/server/requirements.txt`)
- `@astrojs/node` `10.0.4` (npm, `app/client/package-lock.json`)
- `@astrojs/node` `10.0.4` (npm, `app/client/package.json`)
- `@playwright/test` `1.59.1` (npm, `app/client/package-lock.json`)
- `@playwright/test` `1.59.1` (npm, `app/client/package.json`)
- `@tailwindcss/vite` `4.2.2` (npm, `app/client/package-lock.json`)
- `@tailwindcss/vite` `4.2.2` (npm, `app/client/package.json`)
- `@types/node` `25.6.0` (npm, `app/client/package-lock.json`)
- `@types/node` `25.6.0` (npm, `app/client/package.json`)
- `astro` `6.1.6` (npm, `app/client/package-lock.json`)
- `astro` `6.1.6` (npm, `app/client/package.json`)
- `cross-env` `10.1.0` (npm, `app/client/package-lock.json`)
- `cross-env` `10.1.0` (npm, `app/client/package.json`)
- `esbuild-wasm` `0.28.0` (npm, `app/client/package-lock.json`)
- `esbuild-wasm` `0.28.0` (npm, `app/client/package.json`)
- `tailwindcss` `4.2.2` (npm, `app/client/package-lock.json`)
- `tailwindcss` `4.2.2` (npm, `app/client/package.json`)
- `typescript` `6.0.2` (npm, `app/client/package-lock.json`)
- `typescript` `6.0.2` (npm, `app/client/package.json`)
- `@astrojs/compiler` `3.0.1` (npm, `app/client/package-lock.json`)
- `@astrojs/internal-helpers` `0.8.0` (npm, `app/client/package-lock.json`)
- `@astrojs/markdown-remark` `7.1.0` (npm, `app/client/package-lock.json`)
- `@astrojs/prism` `4.0.1` (npm, `app/client/package-lock.json`)
- `@astrojs/telemetry` `3.3.0` (npm, `app/client/package-lock.json`)
- `@babel/helper-string-parser` `7.27.1` (npm, `app/client/package-lock.json`)
- `@babel/helper-validator-identifier` `7.28.5` (npm, `app/client/package-lock.json`)
- `@babel/parser` `7.29.2` (npm, `app/client/package-lock.json`)
- `@babel/types` `7.29.0` (npm, `app/client/package-lock.json`)
- ... (+377 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    %% title: Code-to-Cloud Deployment Traceability
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_app_client["app/client"]:::atlasCategory
        mod_app_server["app/server"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_app_client_Dockerfile["app/client/Dockerfile"]:::atlasWorkflow
    end
    mod_app_client -->|PACKAGED_BY| art_app_client_Dockerfile
    mod_app_server -->|PACKAGED_BY| art_app_client_Dockerfile
```

- `app/client` (code_module) --[PACKAGED_BY]--> `app/client/Dockerfile` (container)
- `app/server` (code_module) --[PACKAGED_BY]--> `app/client/Dockerfile` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  %% title: CI/CD Pipeline Topology — github-samples/pets-workshop
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
  NoWorkflows[No Workflows Detected]:::atlasMore
```
