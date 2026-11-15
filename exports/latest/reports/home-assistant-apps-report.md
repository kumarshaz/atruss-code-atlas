---
title: Architecture — home-assistant/apps
description: Arc42 and Pipeline report for home-assistant/apps
---

# Repository Architecture Analysis: home-assistant/apps

## Metadata
- **SHA**: `c0f85bb9935683b4cdc0e9a871ed1853e1c69821`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 3
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 3
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Container
- **import_edges**: 0 entry(ies)
- **loc**: 99
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 99

# Architecture: home-assistant/apps

## Context
- **Repository**: `home-assistant/apps`
- **SHA**: `c0f85bb9935683b4cdc0e9a871ed1853e1c69821`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Container

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
    build["build : module"]:::atlasJob
    config["config : module"]:::atlasJob
    en["en : module"]:::atlasJob
```

## Component Details
- **build** (`assist_microphone/build.yaml`): module
- **config** (`assist_microphone/config.yaml`): module
- **en** (`assist_microphone/translations/en.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (78.45/100)
- **Technical Debt Score**: 21.55
- **Estimated Remediation Effort**: 14.39h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `B` | 87.00 | 0.15 | workflows=4, operational_antipatterns=6, parallel_branches=True |
| Security | `F` | 32.00 | 0.20 | vulnerabilities=0, secrets=3, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 0 | **Vulnerabilities**: 0 | **Secrets**: 3

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `git_pull/DOCS.md:58` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `letsencrypt/DOCS.md:1494` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[HIGH] `ATRUSS-SEC-005`** at `mosquitto/DOCS.md:69` (`password: "PBKD***REDACTED***"`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_assist_microphone["assist_microphone"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_assist_microphone_Dockerfile["assist_microphone/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_lint_yml_hadolint["lint.yml#hadolint"]:::atlasJob
        job_lint_yml_shellcheck["lint.yml#shellcheck"]:::atlasJob
        job_lint_yml_yamllint["lint.yml#yamllint"]:::atlasJob
        job_repository_updater_yaml_update["repository-updater.yaml#update"]:::atlasJob
        job_restrict_task_creation_yml_check_authorization["restrict-task-creation.yml#check-authorization"]:::atlasJob
        job_stale_yml_stale["stale.yml#stale"]:::atlasJob
    end
    mod_assist_microphone -->|BUILT_BY| job_lint_yml_hadolint
    mod_assist_microphone -->|BUILT_BY| job_lint_yml_shellcheck
    mod_assist_microphone -->|BUILT_BY| job_lint_yml_yamllint
    mod_assist_microphone -->|BUILT_BY| job_repository_updater_yaml_update
    mod_assist_microphone -->|BUILT_BY| job_restrict_task_creation_yml_check_authorization
    mod_assist_microphone -->|BUILT_BY| job_stale_yml_stale
    mod_assist_microphone -->|PACKAGED_BY| art_assist_microphone_Dockerfile
```

- `assist_microphone` (code_module) --[BUILT_BY]--> `lint.yml#hadolint` (ci_job)
- `assist_microphone` (code_module) --[BUILT_BY]--> `lint.yml#shellcheck` (ci_job)
- `assist_microphone` (code_module) --[BUILT_BY]--> `lint.yml#yamllint` (ci_job)
- `assist_microphone` (code_module) --[BUILT_BY]--> `repository-updater.yaml#update` (ci_job)
- `assist_microphone` (code_module) --[BUILT_BY]--> `restrict-task-creation.yml#check-authorization` (ci_job)
- `assist_microphone` (code_module) --[BUILT_BY]--> `stale.yml#stale` (ci_job)
- `assist_microphone` (code_module) --[PACKAGED_BY]--> `assist_microphone/Dockerfile` (container)


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
  pipeline_root(["home-assistant/apps (4 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Automation___Other["Automation & Other (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_1_Repository_updater["Repository updater (1 jobs)"]
      direction TB
      wf_1_Repository_updater(["Trigger: Repository updater"]):::atlasWorkflow
      job_1_update["update"]:::atlasJob
      wf_1_Repository_updater --> job_1_update
    end
    pipeline_root --> wf_1_Repository_updater
    subgraph sg_wf_2_Restrict_task_creation["Restrict task creation (1 jobs)"]
      direction TB
      wf_2_Restrict_task_creation(["Trigger: Restrict task creation"]):::atlasWorkflow
      job_2_check_authorization["check-authorization"]:::atlasJob
      wf_2_Restrict_task_creation --> job_2_check_authorization
    end
    pipeline_root --> wf_2_Restrict_task_creation
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (1 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_0_Lint["Lint (3 jobs)"]
      direction TB
      wf_0_Lint(["Trigger: Lint"]):::atlasWorkflow
      job_0_hadolint["hadolint"]:::atlasJob
      job_0_yamllint["yamllint"]:::atlasJob
      job_0_shellcheck["shellcheck"]:::atlasJob
      wf_0_Lint --> job_0_hadolint
      wf_0_Lint --> job_0_yamllint
      wf_0_Lint --> job_0_shellcheck
    end
    pipeline_root --> wf_0_Lint
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_3_Stale["Stale (1 jobs)"]
      direction TB
      wf_3_Stale(["Trigger: Stale"]):::atlasWorkflow
      job_3_stale["stale"]:::atlasJob
      wf_3_Stale --> job_3_stale
    end
    pipeline_root --> wf_3_Stale
  end
```
