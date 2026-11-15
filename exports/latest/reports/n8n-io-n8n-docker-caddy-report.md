---
title: Architecture — n8n-io/n8n-docker-caddy
description: Arc42 and Pipeline report for n8n-io/n8n-docker-caddy
---

# Repository Architecture Analysis: n8n-io/n8n-docker-caddy

## Metadata
- **SHA**: `2f93c081f0249edb42ce821aed451704d8095cf8`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 1
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 35
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 32

# Architecture: n8n-io/n8n-docker-caddy

## Context
- **Repository**: `n8n-io/n8n-docker-caddy`
- **SHA**: `2f93c081f0249edb42ce821aed451704d8095cf8`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Docker Compose

## Building Block View

```mermaid
graph TD;
    docker_compose["docker-compose : module"]
```

## Component Details
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
    subgraph code_modules["Code Modules"]
        mod_a9809ccf_304e_47b5_9eaf_88950db94721["a9809ccf-304e-47b5-9eaf-88950db94721"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_docker_compose_yml["docker-compose.yml"]
    end
    mod_a9809ccf_304e_47b5_9eaf_88950db94721 -->|PACKAGED_BY| art_docker_compose_yml
```

- `a9809ccf-304e-47b5-9eaf-88950db94721` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
