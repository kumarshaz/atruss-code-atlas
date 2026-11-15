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
    docker_compose["docker-compose : module"]
    versions["versions : module"]
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
    subgraph code_modules["Code Modules"]
        mod_postgres["postgres"]
        mod_server["server"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_postgres_Dockerfile["postgres/Dockerfile"]
        art_postgres_docker_compose_yml["postgres/docker-compose.yml"]
        art_server_Dockerfile["server/Dockerfile"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_build_postgres_yml_build_and_push["build-postgres.yml#build_and_push"]
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
  pipeline_root(["immich-app/base-images (6 workflows)"])
  grp_0_CI___Verification["CI & Verification (3 workflows · 5 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Scheduled___Manual["Scheduled & Manual (2 workflows · 5 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  grp_2_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]
  pipeline_root --> grp_2_Release___Deploy
```
