---
title: Architecture — langfuse/langfuse-cli
description: Arc42 and Pipeline report for langfuse/langfuse-cli
---

# Repository Architecture Analysis: langfuse/langfuse-cli

## Metadata
- **SHA**: `46d3bce82e695cdf1dc05c89f9f9822e4260d065`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 6.58
- **avg_cyclomatic_complexity**: 6.05
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 65.53
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 60
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: TypeScript
- **import_edges**: 100 entry(ies)
- **loc**: 11059
- **max_cognitive_complexity**: 128
- **max_cyclomatic_complexity**: 72
- **sloc**: 10138
- **test_file_count**: 19

# Architecture: langfuse/langfuse-cli

## Context
- **Repository**: `langfuse/langfuse-cli`
- **SHA**: `46d3bce82e695cdf1dc05c89f9f9822e4260d065`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: TypeScript

## Building Block View

```mermaid
graph TD;
    _langfuse_cli["@langfuse/cli : MODULE"]
```

## Component Details
- **@langfuse/cli** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (41.65/100)
- **Technical Debt Score**: 58.35
- **Estimated Remediation Effort**: 61.19h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 37.80 | 0.20 | avg_cc=6.05, max_cc=72, duplication=65.53%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=9, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 37.26 | 0.15 | avg_cognitive=6.58, max_cognitive=128, fitness_violations=3, oversized_files=3 |
| Pipeline Health | `F` | 35.00 | 0.15 | workflows=4, operational_antipatterns=10, parallel_branches=False |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=8 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (65.53) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (128.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (72.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 9 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@apidevtools/swagger-parser` `12.1.0` (npm, `package.json`)
- `@types/bun` `1.4.4` (npm, `package.json`)
- `@types/semver` `7.8.0` (npm, `package.json`)
- `ajv` `8.17.1` (npm, `package.json`)
- `ajv-formats` `3.0.1` (npm, `package.json`)
- `semver` `7.8.6` (npm, `package.json`)
- `typescript` `7.0.2` (npm, `package.json`)
- `yaml` `2.9.1` (npm, `package.json`)
- `zod` `4.6.7` (npm, `package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_348a47bb_7e01_46c8_8577_53d321087830["348a47bb-7e01-46c8-8577-53d321087830"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_beta_release_yml_beta_version["beta-release.yml#beta-version"]
        job_beta_release_yml_preparation["beta-release.yml#preparation"]
        job_beta_release_yml_publish["beta-release.yml#publish"]
        job_ci_yml_conformance["ci.yml#conformance"]
        job_release_yml_publish["release.yml#publish"]
        job_zizmor_yml_zizmor["zizmor.yml#zizmor"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_npm_publish["npm-publish"]
        env_npm_publish_beta["npm-publish-beta"]
    end
    job_beta_release_yml_publish -->|DEPLOYS_TO| env_npm_publish_beta
    job_release_yml_publish -->|DEPLOYS_TO| env_npm_publish
    mod_348a47bb_7e01_46c8_8577_53d321087830 -->|BUILT_BY| job_beta_release_yml_beta_version
    mod_348a47bb_7e01_46c8_8577_53d321087830 -->|BUILT_BY| job_ci_yml_conformance
    mod_348a47bb_7e01_46c8_8577_53d321087830 -->|BUILT_BY| job_zizmor_yml_zizmor
    mod_348a47bb_7e01_46c8_8577_53d321087830 -->|DEPLOYED_BY| job_beta_release_yml_preparation
    mod_348a47bb_7e01_46c8_8577_53d321087830 -->|DEPLOYED_BY| job_beta_release_yml_publish
    mod_348a47bb_7e01_46c8_8577_53d321087830 -->|DEPLOYED_BY| job_release_yml_publish
```

- `beta-release.yml#publish` (ci_job) --[DEPLOYS_TO]--> `npm-publish-beta` (environment)
- `release.yml#publish` (ci_job) --[DEPLOYS_TO]--> `npm-publish` (environment)
- `348a47bb-7e01-46c8-8577-53d321087830` (code_module) --[BUILT_BY]--> `beta-release.yml#beta-version` (ci_job)
- `348a47bb-7e01-46c8-8577-53d321087830` (code_module) --[BUILT_BY]--> `ci.yml#conformance` (ci_job)
- `348a47bb-7e01-46c8-8577-53d321087830` (code_module) --[BUILT_BY]--> `zizmor.yml#zizmor` (ci_job)
- `348a47bb-7e01-46c8-8577-53d321087830` (code_module) --[DEPLOYED_BY]--> `beta-release.yml#preparation` (ci_job)
- `348a47bb-7e01-46c8-8577-53d321087830` (code_module) --[DEPLOYED_BY]--> `beta-release.yml#publish` (ci_job)
- `348a47bb-7e01-46c8-8577-53d321087830` (code_module) --[DEPLOYED_BY]--> `release.yml#publish` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["langfuse/langfuse-cli (4 workflows)"])
  grp_0_Release___Deploy["Release & Deploy (2 workflows · 4 jobs)"]
  pipeline_root --> grp_0_Release___Deploy
  wf_0_Beta_release["Beta release (3 jobs)"]
  grp_0_Release___Deploy --> wf_0_Beta_release
  wf_2_Release["Release (1 jobs)"]
  grp_0_Release___Deploy --> wf_2_Release
  grp_1_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  wf_1_CI["CI (1 jobs)"]
  grp_1_Scheduled___Manual --> wf_1_CI
  wf_3_Check_GitHub_Actions["Check GitHub Actions (1 jobs)"]
  grp_1_Scheduled___Manual --> wf_3_Check_GitHub_Actions
```
