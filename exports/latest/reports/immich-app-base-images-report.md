---
title: Architecture — immich-app/base-images
description: Arc42 and Pipeline report for immich-app/base-images
---

# Repository Architecture Analysis: immich-app/base-images

## Metadata
- **SHA**: `1e95d65c6d4c34906b78eb064e06644515d24e6e`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 2
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 2
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 42
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 39

# Architecture: immich-app/base-images

## Context
- **Repository**: `immich-app/base-images`
- **SHA**: `1e95d65c6d4c34906b78eb064e06644515d24e6e`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Docker Compose

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
    docker_compose["docker-compose : module"]:::atlasJob
    versions["versions : module"]:::atlasJob
```

## Component Details
- **docker-compose** (`postgres/docker-compose.yml`): module
- **versions** (`postgres/versions.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (82.75/100)
- **Technical Debt Score**: 17.25
- **Estimated Remediation Effort**: 14.81h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 57.00 | 0.15 | workflows=6, operational_antipatterns=13, parallel_branches=True |
| Security | `C` | 76.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=2 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_postgres["postgres"]:::atlasCategory
        mod_server["server"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_postgres_Dockerfile["postgres/Dockerfile"]:::atlasWorkflow
        art_postgres_docker_compose_yml["postgres/docker-compose.yml"]:::atlasWorkflow
        art_server_Dockerfile["server/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_build_postgres_yml_build_and_push["build-postgres.yml#build_and_push"]:::atlasJob
    end
    mod_postgres -->|BUILT_BY| job_build_postgres_yml_build_and_push
    mod_postgres -->|PACKAGED_BY| art_postgres_Dockerfile
    mod_postgres -->|PACKAGED_BY| art_postgres_docker_compose_yml
    mod_postgres -->|PACKAGED_BY| art_server_Dockerfile
    mod_server -->|PACKAGED_BY| art_server_Dockerfile
    art_postgres_Dockerfile -->|BUILT_BY| job_build_postgres_yml_build_and_push
    art_postgres_docker_compose_yml -->|BUILT_BY| job_build_postgres_yml_build_and_push
```

- `postgres` (code_module) --[BUILT_BY]--> `build-postgres.yml#build_and_push` (ci_job)
- `postgres` (code_module) --[PACKAGED_BY]--> `postgres/Dockerfile` (container)
- `postgres` (code_module) --[PACKAGED_BY]--> `postgres/docker-compose.yml` (container)
- `postgres` (code_module) --[PACKAGED_BY]--> `server/Dockerfile` (container)
- `server` (code_module) --[PACKAGED_BY]--> `server/Dockerfile` (container)
- `postgres/Dockerfile` (container) --[BUILT_BY]--> `build-postgres.yml#build_and_push` (ci_job)
- `postgres/docker-compose.yml` (container) --[BUILT_BY]--> `build-postgres.yml#build_and_push` (ci_job)


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
  pipeline_root(["immich-app/base-images (6 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (3 workflows · 5 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_1_Build_and_Push_Server_Base_Images["Build and Push Server Base Images (3 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_1_Build_and_Push_Server_Base_Images
  job_1_pre_job["pre-job"]:::atlasJob
  job_1_build_and_push["build_and_push"]:::atlasJob
  job_1_success_check["success-check"]:::atlasJob
  wf_1_Build_and_Push_Server_Base_Images --> job_1_pre_job
  job_1_pre_job --> job_1_build_and_push
  job_1_build_and_push --> job_1_success_check
  wf_2_PR_Conventional_Commit["PR Conventional Commit (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_2_PR_Conventional_Commit
  job_2_validate_pr_title["validate-pr-title"]:::atlasJob
  wf_2_PR_Conventional_Commit --> job_2_validate_pr_title
  wf_3_Zizmor["Zizmor (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_3_Zizmor
  job_3_zizmor["zizmor"]:::atlasJob
  wf_3_Zizmor --> job_3_zizmor
  grp_1_Scheduled___Manual["Scheduled & Manual (2 workflows · 5 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Scheduled___Manual
  wf_0_Build_and_Push_Postgres_Images["Build and Push Postgres Images (4 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_0_Build_and_Push_Postgres_Images
  job_0_pre_job["pre-job"]:::atlasJob
  job_0_matrix["matrix"]:::atlasJob
  job_0_build_and_push["build_and_push"]:::atlasJob
  wf_0_Build_and_Push_Postgres_Images --> job_0_pre_job
  job_0_pre_job --> job_0_matrix
  job_0_pre_job --> job_0_build_and_push
  job_0_matrix --> job_0_build_and_push
  wf_5_Test["Test (1 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_5_Test
  job_5_shellcheck["shellcheck"]:::atlasJob
  wf_5_Test --> job_5_shellcheck
  grp_2_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Release___Deploy
  wf_4_Git_tag["Git tag (1 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_4_Git_tag
  job_4_set_tag["set_tag"]:::atlasJob
  wf_4_Git_tag --> job_4_set_tag
```
