---
title: Architecture — nextcloud/vm
description: Arc42 and Pipeline report for nextcloud/vm
---

# Repository Architecture Analysis: nextcloud/vm

## Metadata
- **SHA**: `775ae1418ad212bbc7729874453d5c4a34f1210b`
- **Primary Ecosystem**: PHP

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
- **framework**: Unknown
- **import_edges**: 0 entry(ies)
- **loc**: 39
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 37
- **test_file_count**: 2

# Architecture: nextcloud/vm

## Context
- **Repository**: `nextcloud/vm`
- **SHA**: `775ae1418ad212bbc7729874453d5c4a34f1210b`
- **Ecosystem**: PHP
- **Framework**: Unknown

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
```

## Component Details
- **docker-compose** (`migrate/docker/docker-compose.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (72.85/100)
- **Technical Debt Score**: 27.15
- **Estimated Remediation Effort**: 21.79h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `B` | 87.00 | 0.15 | workflows=6, operational_antipatterns=6, parallel_branches=True |
| Security | `F` | 4.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=8 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_migrate_docker["migrate/docker"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_migrate_docker_docker_compose_yml["migrate/docker/docker-compose.yml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_check_code_with_shellcheck_yml_shellcheck["check-code-with-shellcheck.yml#shellcheck"]:::atlasJob
        job_dependabot_auto_merge_yml_automerge["dependabot-auto-merge.yml#automerge"]:::atlasJob
        job_install_smoke_test_yml_install["install-smoke-test.yml#install"]:::atlasJob
        job_reviewdog_yml_misspell["reviewdog.yml#misspell"]:::atlasJob
        job_reviewdog_yml_shellcheck["reviewdog.yml#shellcheck"]:::atlasJob
        job_update_copyright_year_yml_update_copyright["update-copyright-year.yml#update-copyright"]:::atlasJob
        job_update_wireguard_major_version_yml_update_wireguard["update-wireguard-major-version.yml#update-wireguard"]:::atlasJob
    end
    mod_migrate_docker -->|BUILT_BY| job_check_code_with_shellcheck_yml_shellcheck
    mod_migrate_docker -->|BUILT_BY| job_dependabot_auto_merge_yml_automerge
    mod_migrate_docker -->|BUILT_BY| job_install_smoke_test_yml_install
    mod_migrate_docker -->|BUILT_BY| job_reviewdog_yml_misspell
    mod_migrate_docker -->|BUILT_BY| job_reviewdog_yml_shellcheck
    mod_migrate_docker -->|BUILT_BY| job_update_copyright_year_yml_update_copyright
    mod_migrate_docker -->|BUILT_BY| job_update_wireguard_major_version_yml_update_wireguard
    mod_migrate_docker -->|PACKAGED_BY| art_migrate_docker_docker_compose_yml
```

- `migrate/docker` (code_module) --[BUILT_BY]--> `check-code-with-shellcheck.yml#shellcheck` (ci_job)
- `migrate/docker` (code_module) --[BUILT_BY]--> `dependabot-auto-merge.yml#automerge` (ci_job)
- `migrate/docker` (code_module) --[BUILT_BY]--> `install-smoke-test.yml#install` (ci_job)
- `migrate/docker` (code_module) --[BUILT_BY]--> `reviewdog.yml#misspell` (ci_job)
- `migrate/docker` (code_module) --[BUILT_BY]--> `reviewdog.yml#shellcheck` (ci_job)
- `migrate/docker` (code_module) --[BUILT_BY]--> `update-copyright-year.yml#update-copyright` (ci_job)
- `migrate/docker` (code_module) --[BUILT_BY]--> `update-wireguard-major-version.yml#update-wireguard` (ci_job)
- `migrate/docker` (code_module) --[PACKAGED_BY]--> `migrate/docker/docker-compose.yml` (container)


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
  pipeline_root(["nextcloud/vm (6 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Scheduled___Manual["Scheduled & Manual (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_2_install_smoke_test["install-smoke-test (1 jobs)"]
      direction TB
      wf_2_install_smoke_test(["Trigger: install-smoke-test"]):::atlasWorkflow
      job_2_install["install"]:::atlasJob
      wf_2_install_smoke_test --> job_2_install
    end
    pipeline_root --> wf_2_install_smoke_test
    subgraph sg_wf_4_Update_Copyright_Year["Update Copyright Year (1 jobs)"]
      direction TB
      wf_4_Update_Copyright_Year(["Trigger: Update Copyright Year"]):::atlasWorkflow
      job_4_update_copyright["update-copyright"]:::atlasJob
      wf_4_Update_Copyright_Year --> job_4_update_copyright
    end
    pipeline_root --> wf_4_Update_Copyright_Year
    subgraph sg_wf_5_Update_WireGuard_Major_Version["Update WireGuard Major Version (1 jobs)"]
      direction TB
      wf_5_Update_WireGuard_Major_Version(["Trigger: Update WireGuard Major Version"]):::atlasWorkflow
      job_5_update_wireguard["update-wireguard"]:::atlasJob
      wf_5_Update_WireGuard_Major_Version --> job_5_update_wireguard
    end
    pipeline_root --> wf_5_Update_WireGuard_Major_Version
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (2 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_0_check_code_with_shellcheck["check-code-with-shellcheck (1 jobs)"]
      direction TB
      wf_0_check_code_with_shellcheck(["Trigger: check-code-with-shellcheck"]):::atlasWorkflow
      job_0_shellcheck["shellcheck"]:::atlasJob
      wf_0_check_code_with_shellcheck --> job_0_shellcheck
    end
    pipeline_root --> wf_0_check_code_with_shellcheck
    subgraph sg_wf_3_reviewdog["reviewdog (2 jobs)"]
      direction TB
      wf_3_reviewdog(["Trigger: reviewdog"]):::atlasWorkflow
      job_3_shellcheck["shellcheck"]:::atlasJob
      job_3_misspell["misspell"]:::atlasJob
      wf_3_reviewdog --> job_3_shellcheck
      wf_3_reviewdog --> job_3_misspell
    end
    pipeline_root --> wf_3_reviewdog
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_1_Dependabot_auto_merge["Dependabot auto-merge (1 jobs)"]
      direction TB
      wf_1_Dependabot_auto_merge(["Trigger: Dependabot auto-merge"]):::atlasWorkflow
      job_1_automerge["automerge"]:::atlasJob
      wf_1_Dependabot_auto_merge --> job_1_automerge
    end
    pipeline_root --> wf_1_Dependabot_auto_merge
  end
```
