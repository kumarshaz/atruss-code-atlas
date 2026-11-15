---
title: Architecture — n8n-io/self-hosted-ai-starter-kit
description: Arc42 and Pipeline report for n8n-io/self-hosted-ai-starter-kit
---

# Repository Architecture Analysis: n8n-io/self-hosted-ai-starter-kit

## Metadata
- **SHA**: `662bd8892476b41d9084417a569cc84013354674`
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
- **loc**: 156
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 142

# Architecture: n8n-io/self-hosted-ai-starter-kit

## Context
- **Repository**: `n8n-io/self-hosted-ai-starter-kit`
- **SHA**: `662bd8892476b41d9084417a569cc84013354674`
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
        mod_ed5441f4_17bb_4bc4_9c63_c45a317a3ab1["ed5441f4-17bb-4bc4-9c63-c45a317a3ab1"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_docker_compose_yml["docker-compose.yml"]
    end
    mod_ed5441f4_17bb_4bc4_9c63_c45a317a3ab1 -->|PACKAGED_BY| art_docker_compose_yml
```

- `ed5441f4-17bb-4bc4-9c63-c45a317a3ab1` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
