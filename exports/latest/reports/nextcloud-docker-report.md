---
title: Architecture — nextcloud/docker
description: Arc42 and Pipeline report for nextcloud/docker
---

# Repository Architecture Analysis: nextcloud/docker

## Metadata
- **SHA**: `18bc14cc9d4d8516fd8cd19034f9493ace636f13`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 8
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 8
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 730
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 530

# Architecture: nextcloud/docker

## Context
- **Repository**: `nextcloud/docker`
- **SHA**: `18bc14cc9d4d8516fd8cd19034f9493ace636f13`
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
    compose["compose : module"]:::atlasJob
```

## Component Details
- **compose** (`.examples/docker-compose/insecure/mariadb/apache/compose.yaml`): module
- **compose** (`.examples/docker-compose/insecure/mariadb/fpm/compose.yaml`): module
- **compose** (`.examples/docker-compose/insecure/postgres/apache/compose.yaml`): module
- **compose** (`.examples/docker-compose/insecure/postgres/fpm/compose.yaml`): module
- **compose** (`.examples/docker-compose/with-nginx-proxy/mariadb/apache/compose.yaml`): module
- **compose** (`.examples/docker-compose/with-nginx-proxy/mariadb/fpm/compose.yaml`): module
- **compose** (`.examples/docker-compose/with-nginx-proxy/postgres/apache/compose.yaml`): module
- **compose** (`.examples/docker-compose/with-nginx-proxy/postgres/fpm/compose.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (86.95/100)
- **Technical Debt Score**: 13.05
- **Estimated Remediation Effort**: 8.76h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `B` | 85.00 | 0.15 | workflows=2, operational_antipatterns=5, parallel_branches=False |
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
        mod__examples_docker_compose_insecure_mariadb_apache[".examples/docker-compose/insecure/mariadb/apache"]:::atlasCategory
        mod__examples_docker_compose_insecure_mariadb_fpm[".examples/docker-compose/insecure/mariadb/fpm"]:::atlasCategory
        mod__examples_docker_compose_insecure_postgres_apache[".examples/docker-compose/insecure/postgres/apache"]:::atlasCategory
        mod__examples_docker_compose_insecure_postgres_fpm[".examples/docker-compose/insecure/postgres/fpm"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_mariadb_apache[".examples/docker-compose/with-nginx-proxy/mariadb/apache"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy[".examples/docker-compose/with-nginx-proxy/mariadb/apache/proxy"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm[".examples/docker-compose/with-nginx-proxy/mariadb/fpm"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy[".examples/docker-compose/with-nginx-proxy/mariadb/fpm/proxy"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_postgres_apache[".examples/docker-compose/with-nginx-proxy/postgres/apache"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy[".examples/docker-compose/with-nginx-proxy/postgres/apache/proxy"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_postgres_fpm[".examples/docker-compose/with-nginx-proxy/postgres/fpm"]:::atlasCategory
        mod__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy[".examples/docker-compose/with-nginx-proxy/postgres/fpm/proxy"]:::atlasCategory
        mod__examples_dockerfiles_cron_apache[".examples/dockerfiles/cron/apache"]:::atlasCategory
        mod__examples_dockerfiles_cron_fpm[".examples/dockerfiles/cron/fpm"]:::atlasCategory
        mod__examples_dockerfiles_cron_fpm_alpine[".examples/dockerfiles/cron/fpm-alpine"]:::atlasCategory
        mod__examples_dockerfiles_full_apache[".examples/dockerfiles/full/apache"]:::atlasCategory
        mod__examples_dockerfiles_full_fpm[".examples/dockerfiles/full/fpm"]:::atlasCategory
        mod__examples_dockerfiles_full_fpm_alpine[".examples/dockerfiles/full/fpm-alpine"]:::atlasCategory
        mod__examples_dockerfiles_imap_apache[".examples/dockerfiles/imap/apache"]:::atlasCategory
        mod__examples_dockerfiles_imap_fpm[".examples/dockerfiles/imap/fpm"]:::atlasCategory
        mod__examples_dockerfiles_imap_fpm_alpine[".examples/dockerfiles/imap/fpm-alpine"]:::atlasCategory
        mod__examples_dockerfiles_smb_apache[".examples/dockerfiles/smb/apache"]:::atlasCategory
        mod__examples_dockerfiles_smb_fpm[".examples/dockerfiles/smb/fpm"]:::atlasCategory
        mod__examples_dockerfiles_smb_fpm_alpine[".examples/dockerfiles/smb/fpm-alpine"]:::atlasCategory
        mod_32_apache["32/apache"]:::atlasCategory
        mod_32_fpm["32/fpm"]:::atlasCategory
        mod_32_fpm_alpine["32/fpm-alpine"]:::atlasCategory
        mod_33_apache["33/apache"]:::atlasCategory
        mod_33_fpm["33/fpm"]:::atlasCategory
        mod_33_fpm_alpine["33/fpm-alpine"]:::atlasCategory
        mod_34_apache["34/apache"]:::atlasCategory
        mod_34_fpm["34/fpm"]:::atlasCategory
        mod_34_fpm_alpine["34/fpm-alpine"]:::atlasCategory
        mod_35_apache["35/apache"]:::atlasCategory
        mod_35_fpm["35/fpm"]:::atlasCategory
        mod_35_fpm_alpine["35/fpm-alpine"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy_Dockerfile[".examples/docker-compose/with-nginx-proxy/mariadb/apache/proxy/Dockerfile"]:::atlasWorkflow
        art__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy_Dockerfile[".examples/docker-compose/with-nginx-proxy/mariadb/fpm/proxy/Dockerfile"]:::atlasWorkflow
        art__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy_Dockerfile[".examples/docker-compose/with-nginx-proxy/postgres/apache/proxy/Dockerfile"]:::atlasWorkflow
        art__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy_Dockerfile[".examples/docker-compose/with-nginx-proxy/postgres/fpm/proxy/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_cron_apache_Dockerfile[".examples/dockerfiles/cron/apache/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_cron_fpm_alpine_Dockerfile[".examples/dockerfiles/cron/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_cron_fpm_Dockerfile[".examples/dockerfiles/cron/fpm/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_full_apache_Dockerfile[".examples/dockerfiles/full/apache/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_full_fpm_alpine_Dockerfile[".examples/dockerfiles/full/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_full_fpm_Dockerfile[".examples/dockerfiles/full/fpm/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_imap_apache_Dockerfile[".examples/dockerfiles/imap/apache/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_imap_fpm_alpine_Dockerfile[".examples/dockerfiles/imap/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_imap_fpm_Dockerfile[".examples/dockerfiles/imap/fpm/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_smb_apache_Dockerfile[".examples/dockerfiles/smb/apache/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_smb_fpm_alpine_Dockerfile[".examples/dockerfiles/smb/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art__examples_dockerfiles_smb_fpm_Dockerfile[".examples/dockerfiles/smb/fpm/Dockerfile"]:::atlasWorkflow
        art_32_apache_Dockerfile["32/apache/Dockerfile"]:::atlasWorkflow
        art_32_fpm_alpine_Dockerfile["32/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art_32_fpm_Dockerfile["32/fpm/Dockerfile"]:::atlasWorkflow
        art_33_apache_Dockerfile["33/apache/Dockerfile"]:::atlasWorkflow
        art_33_fpm_alpine_Dockerfile["33/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art_33_fpm_Dockerfile["33/fpm/Dockerfile"]:::atlasWorkflow
        art_34_apache_Dockerfile["34/apache/Dockerfile"]:::atlasWorkflow
        art_34_fpm_alpine_Dockerfile["34/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art_34_fpm_Dockerfile["34/fpm/Dockerfile"]:::atlasWorkflow
        art_35_apache_Dockerfile["35/apache/Dockerfile"]:::atlasWorkflow
        art_35_fpm_alpine_Dockerfile["35/fpm-alpine/Dockerfile"]:::atlasWorkflow
        art_35_fpm_Dockerfile["35/fpm/Dockerfile"]:::atlasWorkflow
    end
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_mariadb_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_docker_compose_insecure_postgres_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_mariadb_fpm_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_apache_proxy_Dockerfile
    mod__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy -->|PACKAGED_BY| art__examples_docker_compose_with_nginx_proxy_postgres_fpm_proxy_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_dockerfiles_cron_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_cron_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_dockerfiles_full_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_full_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_dockerfiles_imap_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_imap_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod__examples_dockerfiles_smb_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod__examples_dockerfiles_smb_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod_32_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_32_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_32_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod_33_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_33_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_33_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod_34_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_34_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_34_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art__examples_dockerfiles_cron_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art__examples_dockerfiles_full_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art__examples_dockerfiles_imap_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art__examples_dockerfiles_smb_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art_32_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art_33_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art_34_apache_Dockerfile
    mod_35_apache -->|PACKAGED_BY| art_35_apache_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_32_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_33_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_34_fpm_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
    mod_35_fpm -->|PACKAGED_BY| art_35_fpm_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_cron_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_full_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_imap_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art__examples_dockerfiles_smb_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art_32_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art_33_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art_34_fpm_alpine_Dockerfile
    mod_35_fpm_alpine -->|PACKAGED_BY| art_35_fpm_alpine_Dockerfile
```

- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/cron/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/full/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/imap/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/smb/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `32/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `33/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `34/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/apache` (code_module) --[PACKAGED_BY]--> `35/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/cron/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/cron/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/full/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/full/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/imap/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/imap/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/smb/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/smb/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `32/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `32/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `33/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `33/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `34/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `34/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `35/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/mariadb/fpm` (code_module) --[PACKAGED_BY]--> `35/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/cron/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/full/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/imap/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/smb/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `32/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `33/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `34/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/apache` (code_module) --[PACKAGED_BY]--> `35/apache/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/cron/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/cron/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/full/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/full/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/imap/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/imap/fpm/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/smb/fpm-alpine/Dockerfile` (container)
- `.examples/docker-compose/insecure/postgres/fpm` (code_module) --[PACKAGED_BY]--> `.examples/dockerfiles/smb/fpm/Dockerfile` (container)


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
  pipeline_root(["nextcloud/docker"]):::atlasRoot
  subgraph Images_0["Images"]
    direction TB
    0_init["init"]:::atlasJob
    0_test["test"]:::atlasJob
    0_init --> 0_test
    0_summary["summary"]:::atlasJob
    0_test --> 0_summary
  end
  pipeline_root --> 0_init
  subgraph update_sh_1["update.sh"]
    direction TB
    1_run_update_sh["run_update_sh"]:::atlasJob
  end
  pipeline_root --> 1_run_update_sh
```
