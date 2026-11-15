---
title: Architecture — zulip/zulip-desktop
description: Arc42 and Pipeline report for zulip/zulip-desktop
---

# Repository Architecture Analysis: zulip/zulip-desktop

## Metadata
- **SHA**: `308ea3b248badd4664d533afe08427022563536e`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.0
- **avg_cyclomatic_complexity**: 2.25
- **component_count**: 1
- **dead_code_count**: 4
- **dead_code_symbols**: 4 entry(ies)
- **duplication_pct**: 61.75
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 64
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: TypeScript
- **import_edges**: 100 entry(ies)
- **loc**: 7813
- **max_cognitive_complexity**: 69
- **max_cyclomatic_complexity**: 28
- **sloc**: 6719
- **test_file_count**: 4

# Architecture: zulip/zulip-desktop

## Context
- **Repository**: `zulip/zulip-desktop`
- **SHA**: `308ea3b248badd4664d533afe08427022563536e`
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
    zulip["zulip : MODULE"]:::atlasJob
```

## Component Details
- **zulip** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (67.60/100)
- **Technical Debt Score**: 32.40
- **Estimated Remediation Effort**: 37.45h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 47.50 | 0.20 | avg_cc=2.25, max_cc=28, duplication=61.75%, dead_code=4 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=40, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 42.00 | 0.15 | avg_cognitive=3.00, max_cognitive=69, fitness_violations=3, oversized_files=3 |
| Pipeline Health | `F` | 57.00 | 0.15 | workflows=4, operational_antipatterns=8, parallel_branches=True |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (61.75) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (69.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (28.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 40 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@electron/remote` `2.0.8` (npm, `package.json`)
- `@sentry/core` `11.8.0` (npm, `package.json`)
- `@sentry/electron` `8.3.0` (npm, `package.json`)
- `@types/auto-launch` `5.0.2` (npm, `package.json`)
- `@types/backoff` `2.5.2` (npm, `package.json`)
- `@types/i18n` `0.13.1` (npm, `package.json`)
- `@types/minimalistic-assert` `1.0.3` (npm, `package.json`)
- `@types/node` `24.13.2` (npm, `package.json`)
- `@types/p-fifo` `1.0.2` (npm, `package.json`)
- `@types/semver` `7.5.8` (npm, `package.json`)
- `@types/yaireo__tagify` `4.3.2` (npm, `package.json`)
- `@typescript/native` `latest` (npm, `package.json`)
- `@yaireo/tagify` `4.5.0` (npm, `package.json`)
- `adm-zip` `0.6.1` (npm, `package.json`)
- `auto-launch` `5.0.5` (npm, `package.json`)
- `backoff` `2.5.0` (npm, `package.json`)
- `electron` `45.1.0` (npm, `package.json`)
- `electron-builder` `26.18.0` (npm, `package.json`)
- `electron-log` `5.0.3` (npm, `package.json`)
- `electron-updater` `6.3.4` (npm, `package.json`)
- `electron-vite` `6.0.0` (npm, `package.json`)
- `electron-window-state` `5.0.3` (npm, `package.json`)
- `escape-goat` `4.0.0` (npm, `package.json`)
- `gatemaker` `1.0.0` (npm, `package.json`)
- `htmlhint` `1.1.2` (npm, `package.json`)
- `i18n` `0.15.1` (npm, `package.json`)
- `i18next-cli` `1.2.1` (npm, `package.json`)
- `minimalistic-assert` `1.0.1` (npm, `package.json`)
- `node-json-db` `1.3.0` (npm, `package.json`)
- `p-fifo` `1.0.0` (npm, `package.json`)
- ... (+10 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_22d00534_2786_4782_b2dd_5c2a3693dc83["22d00534-2786-4782-b2dd-5c2a3693dc83"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_codeql_yml_analyze["codeql.yml#analyze"]:::atlasJob
        job_node_js_yml_build["node.js.yml#build"]:::atlasJob
        job_release_yml_linux["release.yml#linux"]:::atlasJob
        job_release_yml_macos["release.yml#macos"]:::atlasJob
        job_release_yml_prepare["release.yml#prepare"]:::atlasJob
        job_release_yml_windows["release.yml#windows"]:::atlasJob
        job_zizmor_yml_zizmor["zizmor.yml#zizmor"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_azure["azure"]:::atlasTarget
        env_release_macos["release-macos"]:::atlasTarget
        env_release_windows["release-windows"]:::atlasTarget
    end
    job_release_yml_macos -->|DEPLOYS_TO| env_release_macos
    job_release_yml_windows -->|DEPLOYS_TO| env_azure
    job_release_yml_windows -->|DEPLOYS_TO| env_release_windows
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|BUILT_BY| job_codeql_yml_analyze
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|BUILT_BY| job_node_js_yml_build
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|BUILT_BY| job_release_yml_linux
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|BUILT_BY| job_release_yml_prepare
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|BUILT_BY| job_zizmor_yml_zizmor
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|DEPLOYED_BY| job_release_yml_macos
    mod_22d00534_2786_4782_b2dd_5c2a3693dc83 -->|DEPLOYED_BY| job_release_yml_windows
```

- `release.yml#macos` (ci_job) --[DEPLOYS_TO]--> `release-macos` (environment)
- `release.yml#windows` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `release.yml#windows` (ci_job) --[DEPLOYS_TO]--> `release-windows` (environment)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[BUILT_BY]--> `codeql.yml#analyze` (ci_job)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[BUILT_BY]--> `node.js.yml#build` (ci_job)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[BUILT_BY]--> `release.yml#linux` (ci_job)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[BUILT_BY]--> `release.yml#prepare` (ci_job)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[BUILT_BY]--> `zizmor.yml#zizmor` (ci_job)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[DEPLOYED_BY]--> `release.yml#macos` (ci_job)
- `22d00534-2786-4782-b2dd-5c2a3693dc83` (code_module) --[DEPLOYED_BY]--> `release.yml#windows` (ci_job)


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
  pipeline_root(["zulip/zulip-desktop (4 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_0_CodeQL_Advanced["CodeQL Advanced (1 jobs)"]
      direction TB
      wf_0_CodeQL_Advanced(["Trigger: CodeQL Advanced"]):::atlasWorkflow
      job_0_analyze["analyze"]:::atlasJob
      wf_0_CodeQL_Advanced --> job_0_analyze
    end
    pipeline_root --> wf_0_CodeQL_Advanced
    subgraph sg_wf_3_GitHub_Actions_Security_Analysis_with_zizmor["GitHub Actions Security Analysis with zizmor (1 jobs)"]
      direction TB
      wf_3_GitHub_Actions_Security_Analysis_with_zizmor(["Trigger: GitHub Actions Security Analysis with zizmor"]):::atlasWorkflow
      job_3_zizmor["zizmor"]:::atlasJob
      wf_3_GitHub_Actions_Security_Analysis_with_zizmor --> job_3_zizmor
    end
    pipeline_root --> wf_3_GitHub_Actions_Security_Analysis_with_zizmor
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_1_Node_js_CI["Node.js CI (1 jobs)"]
      direction TB
      wf_1_Node_js_CI(["Trigger: Node.js CI"]):::atlasWorkflow
      job_1_build["build"]:::atlasJob
      wf_1_Node_js_CI --> job_1_build
    end
    pipeline_root --> wf_1_Node_js_CI
  end
  subgraph sg_grp_2_Release___Deploy["Release & Deploy (1 workflows · 4 jobs)"]
    direction TB
    subgraph sg_wf_2_Release["Release (4 jobs)"]
      direction TB
      wf_2_Release(["Trigger: Release"]):::atlasWorkflow
      job_2_prepare["prepare"]:::atlasJob
      job_2_linux["linux"]:::atlasJob
      job_2_macos["macos"]:::atlasJob
      wf_2_Release --> job_2_prepare
      job_2_prepare --> job_2_linux
      job_2_prepare --> job_2_macos
    end
    pipeline_root --> wf_2_Release
  end
```
