---
title: Architecture — bitwarden/self-host
description: Arc42 and Pipeline report for bitwarden/self-host
---

# Repository Architecture Analysis: bitwarden/self-host

## Metadata
- **SHA**: `03e222b23f5fe89e8cd4036976044c859324fb44`
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
- **loc**: 98
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 40

# Architecture: bitwarden/self-host

## Context
- **Repository**: `bitwarden/self-host`
- **SHA**: `03e222b23f5fe89e8cd4036976044c859324fb44`
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
    config["config : module"]:::atlasJob
```

## Component Details
- **docker-compose** (`bitwarden-lite/docker-compose.yml`): module
- **config** (`bitwarden-lite/hbs/config.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (80.35/100)
- **Technical Debt Score**: 19.65
- **Estimated Remediation Effort**: 15.41h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `C` | 73.00 | 0.15 | workflows=6, operational_antipatterns=9, parallel_branches=False |
| Security | `F` | 52.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=4 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_bitwarden_lite["bitwarden-lite"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_bitwarden_lite_Dockerfile["bitwarden-lite/Dockerfile"]:::atlasWorkflow
        art_bitwarden_lite_docker_compose_yml["bitwarden-lite/docker-compose.yml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_auto_label_pr_sdlc_yml_label["auto-label-pr-sdlc.yml#label"]:::atlasJob
        job_build_bitwarden_lite_workflow_target_yml_build["build-bitwarden-lite-workflow-target.yml#build"]:::atlasJob
        job_build_bitwarden_lite_workflow_target_yml_check_run["build-bitwarden-lite-workflow-target.yml#check-run"]:::atlasJob
        job_build_bitwarden_lite_yml_build_docker["build-bitwarden-lite.yml#build-docker"]:::atlasJob
        job_build_bitwarden_lite_yml_check_event_source["build-bitwarden-lite.yml#check-event-source"]:::atlasJob
        job_build_bitwarden_lite_yml_setup["build-bitwarden-lite.yml#setup"]:::atlasJob
        job_cleanup_container_images_yml_cleanup_images["cleanup-container-images.yml#cleanup-images"]:::atlasJob
        job_enforce_pr_labels_sdlc_yml_enforce_label["enforce-pr-labels-sdlc.yml#enforce-label"]:::atlasJob
        job_review_code_yml_review["review-code.yml#review"]:::atlasJob
    end
    mod_bitwarden_lite -->|BUILT_BY| job_auto_label_pr_sdlc_yml_label
    mod_bitwarden_lite -->|BUILT_BY| job_build_bitwarden_lite_workflow_target_yml_build
    mod_bitwarden_lite -->|BUILT_BY| job_build_bitwarden_lite_workflow_target_yml_check_run
    mod_bitwarden_lite -->|BUILT_BY| job_build_bitwarden_lite_yml_check_event_source
    mod_bitwarden_lite -->|BUILT_BY| job_build_bitwarden_lite_yml_setup
    mod_bitwarden_lite -->|BUILT_BY| job_cleanup_container_images_yml_cleanup_images
    mod_bitwarden_lite -->|BUILT_BY| job_enforce_pr_labels_sdlc_yml_enforce_label
    mod_bitwarden_lite -->|BUILT_BY| job_review_code_yml_review
    mod_bitwarden_lite -->|PACKAGED_BY| art_bitwarden_lite_Dockerfile
    mod_bitwarden_lite -->|PACKAGED_BY| art_bitwarden_lite_docker_compose_yml
    art_bitwarden_lite_Dockerfile -->|BUILT_BY| job_build_bitwarden_lite_yml_build_docker
```

- `bitwarden-lite` (code_module) --[BUILT_BY]--> `auto-label-pr-sdlc.yml#label` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `build-bitwarden-lite-workflow-target.yml#build` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `build-bitwarden-lite-workflow-target.yml#check-run` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `build-bitwarden-lite.yml#check-event-source` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `build-bitwarden-lite.yml#setup` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `cleanup-container-images.yml#cleanup-images` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `enforce-pr-labels-sdlc.yml#enforce-label` (ci_job)
- `bitwarden-lite` (code_module) --[BUILT_BY]--> `review-code.yml#review` (ci_job)
- `bitwarden-lite` (code_module) --[PACKAGED_BY]--> `bitwarden-lite/Dockerfile` (container)
- `bitwarden-lite` (code_module) --[PACKAGED_BY]--> `bitwarden-lite/docker-compose.yml` (container)
- `bitwarden-lite/Dockerfile` (container) --[BUILT_BY]--> `build-bitwarden-lite.yml#build-docker` (ci_job)


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
  pipeline_root(["bitwarden/self-host (6 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (4 workflows · 5 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_0_Label_PR["Label PR (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_0_Label_PR
  job_0_label["label"]:::atlasJob
  wf_0_Label_PR --> job_0_label
  wf_1_Build_Bitwarden_lite__fork_PR_["Build Bitwarden lite (fork PR) (2 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_1_Build_Bitwarden_lite__fork_PR_
  job_1_check_run["check-run"]:::atlasJob
  job_1_build["build"]:::atlasJob
  wf_1_Build_Bitwarden_lite__fork_PR_ --> job_1_check_run
  job_1_check_run --> job_1_build
  wf_4_SDLC___Enforce_PR_labels["SDLC / Enforce PR labels (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_4_SDLC___Enforce_PR_labels
  job_4_enforce_label["enforce-label"]:::atlasJob
  wf_4_SDLC___Enforce_PR_labels --> job_4_enforce_label
  wf_5_Code_Review["Code Review (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_5_Code_Review
  job_5_review["review"]:::atlasJob
  wf_5_Code_Review --> job_5_review
  grp_1_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Automation___Other
  wf_3_Cleanup_Container_Images["Cleanup Container Images (1 jobs)"]:::atlasWorkflow
  grp_1_Automation___Other --> wf_3_Cleanup_Container_Images
  job_3_cleanup_images["cleanup-images"]:::atlasJob
  wf_3_Cleanup_Container_Images --> job_3_cleanup_images
  grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 3 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Scheduled___Manual
  wf_2_Build_Bitwarden_lite["Build Bitwarden lite (3 jobs)"]:::atlasWorkflow
  grp_2_Scheduled___Manual --> wf_2_Build_Bitwarden_lite
  job_2_check_event_source["check-event-source"]:::atlasJob
  job_2_setup["setup"]:::atlasJob
  job_2_build_docker["build-docker"]:::atlasJob
  wf_2_Build_Bitwarden_lite --> job_2_check_event_source
  job_2_check_event_source --> job_2_setup
  job_2_setup --> job_2_build_docker
```
