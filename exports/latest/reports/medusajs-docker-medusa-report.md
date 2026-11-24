---
title: Architecture — medusajs/docker-medusa
description: Arc42 and Pipeline report for medusajs/docker-medusa
---

# Repository Architecture Analysis: medusajs/docker-medusa

## Metadata
- **SHA**: `1f441e9f5f698e5b6c7f99df3a42fd6aa487a373`
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
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 133
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 122

# Architecture: medusajs/docker-medusa

## Context
- **Repository**: `medusajs/docker-medusa`
- **SHA**: `1f441e9f5f698e5b6c7f99df3a42fd6aa487a373`
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
    docker_compose_override["docker-compose.override : module"]:::atlasJob
    docker_compose_prod["docker-compose.prod : module"]:::atlasJob
    docker_compose["docker-compose : module"]:::atlasJob
```

## Component Details
- **docker-compose.override** (`docker-compose.override.yml`): module
- **docker-compose.prod** (`docker-compose.prod.yml`): module
- **docker-compose** (`docker-compose.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (80.50/100)
- **Technical Debt Score**: 19.50
- **Estimated Remediation Effort**: 4.88h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_7c4d8431_5762_4afb_aef1_c01b387eb837["7c4d8431-5762-4afb-aef1-c01b387eb837"]:::atlasCategory
        mod_admin["admin"]:::atlasCategory
        mod_backend["backend"]:::atlasCategory
        mod_storefront["storefront"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_admin_Dockerfile["admin/Dockerfile"]:::atlasWorkflow
        art_admin_Dockerfile_prod["admin/Dockerfile.prod"]:::atlasWorkflow
        art_backend_Dockerfile["backend/Dockerfile"]:::atlasWorkflow
        art_backend_Dockerfile_prod["backend/Dockerfile.prod"]:::atlasWorkflow
        art_docker_compose_override_yml["docker-compose.override.yml"]:::atlasWorkflow
        art_docker_compose_prod_yml["docker-compose.prod.yml"]:::atlasWorkflow
        art_docker_compose_yml["docker-compose.yml"]:::atlasWorkflow
        art_storefront_Dockerfile["storefront/Dockerfile"]:::atlasWorkflow
        art_storefront_Dockerfile_prod["storefront/Dockerfile.prod"]:::atlasWorkflow
    end
    mod_7c4d8431_5762_4afb_aef1_c01b387eb837 -->|PACKAGED_BY| art_docker_compose_override_yml
    mod_7c4d8431_5762_4afb_aef1_c01b387eb837 -->|PACKAGED_BY| art_docker_compose_prod_yml
    mod_7c4d8431_5762_4afb_aef1_c01b387eb837 -->|PACKAGED_BY| art_docker_compose_yml
    mod_admin -->|PACKAGED_BY| art_admin_Dockerfile
    mod_admin -->|PACKAGED_BY| art_admin_Dockerfile_prod
    mod_admin -->|PACKAGED_BY| art_docker_compose_override_yml
    mod_admin -->|PACKAGED_BY| art_docker_compose_prod_yml
    mod_admin -->|PACKAGED_BY| art_docker_compose_yml
    mod_backend -->|PACKAGED_BY| art_backend_Dockerfile
    mod_backend -->|PACKAGED_BY| art_backend_Dockerfile_prod
    mod_backend -->|PACKAGED_BY| art_docker_compose_override_yml
    mod_backend -->|PACKAGED_BY| art_docker_compose_prod_yml
    mod_backend -->|PACKAGED_BY| art_docker_compose_yml
    mod_storefront -->|PACKAGED_BY| art_docker_compose_override_yml
    mod_storefront -->|PACKAGED_BY| art_docker_compose_prod_yml
    mod_storefront -->|PACKAGED_BY| art_docker_compose_yml
    mod_storefront -->|PACKAGED_BY| art_storefront_Dockerfile
    mod_storefront -->|PACKAGED_BY| art_storefront_Dockerfile_prod
```

- `7c4d8431-5762-4afb-aef1-c01b387eb837` (code_module) --[PACKAGED_BY]--> `docker-compose.override.yml` (container)
- `7c4d8431-5762-4afb-aef1-c01b387eb837` (code_module) --[PACKAGED_BY]--> `docker-compose.prod.yml` (container)
- `7c4d8431-5762-4afb-aef1-c01b387eb837` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `admin` (code_module) --[PACKAGED_BY]--> `admin/Dockerfile` (container)
- `admin` (code_module) --[PACKAGED_BY]--> `admin/Dockerfile.prod` (container)
- `admin` (code_module) --[PACKAGED_BY]--> `docker-compose.override.yml` (container)
- `admin` (code_module) --[PACKAGED_BY]--> `docker-compose.prod.yml` (container)
- `admin` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `backend` (code_module) --[PACKAGED_BY]--> `backend/Dockerfile` (container)
- `backend` (code_module) --[PACKAGED_BY]--> `backend/Dockerfile.prod` (container)
- `backend` (code_module) --[PACKAGED_BY]--> `docker-compose.override.yml` (container)
- `backend` (code_module) --[PACKAGED_BY]--> `docker-compose.prod.yml` (container)
- `backend` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `storefront` (code_module) --[PACKAGED_BY]--> `docker-compose.override.yml` (container)
- `storefront` (code_module) --[PACKAGED_BY]--> `docker-compose.prod.yml` (container)
- `storefront` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `storefront` (code_module) --[PACKAGED_BY]--> `storefront/Dockerfile` (container)
- `storefront` (code_module) --[PACKAGED_BY]--> `storefront/Dockerfile.prod` (container)


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
