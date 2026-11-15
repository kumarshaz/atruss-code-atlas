---
title: Architecture — supabase/supabase-grafana
description: Arc42 and Pipeline report for supabase/supabase-grafana
---

# Repository Architecture Analysis: supabase/supabase-grafana

## Metadata
- **SHA**: `04469b485b758e3a28bdea5239f540a4c3604603`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 5
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 5
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 84
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 70

# Architecture: supabase/supabase-grafana

## Context
- **Repository**: `supabase/supabase-grafana`
- **SHA**: `04469b485b758e3a28bdea5239f540a4c3604603`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Docker Compose

## Building Block View

```mermaid
graph TD;
    docker_compose["docker-compose : module"]
    dependabot["dependabot : module"]
    dashboard["dashboard : module"]
    datasource["datasource : module"]
    prometheus["prometheus : module"]
    repo_root(["supabase/supabase-grafana"])
    repo_root --> dashboard
    repo_root --> datasource
    repo_root --> dependabot
    repo_root --> docker_compose
    repo_root --> prometheus
```

## Component Details
- **docker-compose** (`docker-compose.yml`): module
- **dependabot** (`.github/dependabot.yml`): module
- **dashboard** (`grafana/dashboard.yml`): module
- **datasource** (`grafana/datasource.yml`): module
- **prometheus** (`prometheus/prometheus.yml`): module

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
        mod_4e43a12c_56f9_4f58_8d59_77a473b0ecce["4e43a12c-56f9-4f58-8d59-77a473b0ecce"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]
        art_docker_compose_yml["docker-compose.yml"]
    end
    mod_4e43a12c_56f9_4f58_8d59_77a473b0ecce -->|PACKAGED_BY| art_Dockerfile
    mod_4e43a12c_56f9_4f58_8d59_77a473b0ecce -->|PACKAGED_BY| art_docker_compose_yml
```

- `4e43a12c-56f9-4f58-8d59-77a473b0ecce` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `4e43a12c-56f9-4f58-8d59-77a473b0ecce` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
