---
title: Architecture — home-assistant/docker
description: Arc42 and Pipeline report for home-assistant/docker
---

# Repository Architecture Analysis: home-assistant/docker

## Metadata
- **SHA**: `2b9dfe4d4908e07a3704a0efad09e221ea046f10`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 0
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 0
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Unknown
- **import_edges**: 0 entry(ies)
- **loc**: 0
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 0

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (76.00/100)
- **Technical Debt Score**: 24.00
- **Estimated Remediation Effort**: 19.50h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=3, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 49.00 | 0.15 | workflows=4, operational_antipatterns=9, parallel_branches=True |
| Security | `F` | 52.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=4 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 3 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `Brotli` `1.2.1` (PyPI, `requirements.txt`)
- `mysqlclient` `2.3.0` (PyPI, `requirements.txt`)
- `psycopg2` `2.9.13` (PyPI, `requirements.txt`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod__devcontainer[".devcontainer"]:::atlasCategory
        mod_b0372cf2_d160_41e2_a0e8_2256080e7d36["b0372cf2-d160-41e2-a0e8-2256080e7d36"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__devcontainer_Dockerfile[".devcontainer/Dockerfile"]:::atlasWorkflow
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
    end
    mod__devcontainer -->|PACKAGED_BY| art__devcontainer_Dockerfile
    mod_b0372cf2_d160_41e2_a0e8_2256080e7d36 -->|PACKAGED_BY| art_Dockerfile
```

- `.devcontainer` (code_module) --[PACKAGED_BY]--> `.devcontainer/Dockerfile` (container)
- `b0372cf2-d160-41e2-a0e8-2256080e7d36` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)


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
  pipeline_root(["home-assistant/docker (4 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_1_hadolint["hadolint (1 jobs)"]
      direction TB
      wf_1_hadolint(["Trigger: hadolint"]):::atlasWorkflow
      job_1_golangci["golangci"]:::atlasJob
      wf_1_hadolint --> job_1_golangci
    end
    pipeline_root --> wf_1_hadolint
    subgraph sg_wf_3_Shellcheck["Shellcheck (1 jobs)"]
      direction TB
      wf_3_Shellcheck(["Trigger: Shellcheck"]):::atlasWorkflow
      job_3_shellcheck["shellcheck"]:::atlasJob
      wf_3_Shellcheck --> job_3_shellcheck
    end
    pipeline_root --> wf_3_Shellcheck
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (2 workflows · 4 jobs)"]
    direction TB
    subgraph sg_wf_0_Build_base_images["Build base images (3 jobs)"]
      direction TB
      wf_0_Build_base_images(["Trigger: Build base images"]):::atlasWorkflow
      job_0_init["init"]:::atlasJob
      job_0_build["build"]:::atlasJob
      job_0_manifest["manifest"]:::atlasJob
      wf_0_Build_base_images --> job_0_init
      job_0_init --> job_0_build
      job_0_init --> job_0_manifest
      job_0_build --> job_0_manifest
    end
    pipeline_root --> wf_0_Build_base_images
    subgraph sg_wf_2_Release_Drafter["Release Drafter (1 jobs)"]
      direction TB
      wf_2_Release_Drafter(["Trigger: Release Drafter"]):::atlasWorkflow
      job_2_update_release_draft["update_release_draft"]:::atlasJob
      wf_2_Release_Drafter --> job_2_update_release_draft
    end
    pipeline_root --> wf_2_Release_Drafter
  end
```
