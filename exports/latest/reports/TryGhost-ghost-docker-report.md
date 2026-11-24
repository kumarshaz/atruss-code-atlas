---
title: Architecture — TryGhost/ghost-docker
description: Arc42 and Pipeline report for TryGhost/ghost-docker
---

# Repository Architecture Analysis: TryGhost/ghost-docker

## Metadata
- **SHA**: `74e0df94c51ff45b5fcf6194be9ed18d7e147757`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 6
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 6
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 397
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 354

# Architecture: TryGhost/ghost-docker

## Context
- **Repository**: `TryGhost/ghost-docker`
- **SHA**: `74e0df94c51ff45b5fcf6194be9ed18d7e147757`
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
    compose_ipv6["compose.ipv6 : module"]:::atlasJob
    compose["compose : module"]:::atlasJob
    next_docker_beta["next-docker-beta : module"]:::atlasJob
    launcher["launcher : module"]:::atlasJob
    release["release : module"]:::atlasJob
    shellcheck["shellcheck : module"]:::atlasJob
    repo_root(["TryGhost/ghost-docker"]):::atlasRoot
    repo_root --> compose
    repo_root --> compose_ipv6
    repo_root --> launcher
    repo_root --> next_docker_beta
    repo_root --> release
    repo_root --> shellcheck
```

## Component Details
- **compose.ipv6** (`compose.ipv6.yml`): module
- **compose** (`compose.yml`): module
- **next-docker-beta** (`.github/ISSUE_TEMPLATE/next-docker-beta.yml`): module
- **launcher** (`.github/workflows/launcher.yml`): module
- **release** (`.github/workflows/release.yml`): module
- **shellcheck** (`.github/workflows/shellcheck.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (89.65/100)
- **Technical Debt Score**: 10.35
- **Estimated Remediation Effort**: 6.09h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `C` | 71.00 | 0.15 | workflows=3, operational_antipatterns=4, parallel_branches=False |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_tinybird["tinybird"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_tinybird_Dockerfile["tinybird/Dockerfile"]:::atlasWorkflow
    end
    mod_tinybird -->|PACKAGED_BY| art_tinybird_Dockerfile
```

- `tinybird` (code_module) --[PACKAGED_BY]--> `tinybird/Dockerfile` (container)


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
  pipeline_root(["TryGhost/ghost-docker"]):::atlasRoot
  subgraph Served_launcher_0["Served launcher"]
    direction TB
    0_refuse["refuse"]:::atlasJob
  end
  pipeline_root --> 0_refuse
  subgraph Release_1["Release"]
    direction TB
    1_refuse["refuse"]:::atlasJob
  end
  pipeline_root --> 1_refuse
  subgraph ShellCheck_2["ShellCheck"]
    direction TB
    2_shellcheck["shellcheck"]:::atlasJob
  end
  pipeline_root --> 2_shellcheck
```
