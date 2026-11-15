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
    docker_compose["docker-compose : module"]
    config["config : module"]
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
    subgraph code_modules["Code Modules"]
        mod_bitwarden_lite["bitwarden-lite"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_bitwarden_lite_Dockerfile["bitwarden-lite/Dockerfile"]
        art_bitwarden_lite_docker_compose_yml["bitwarden-lite/docker-compose.yml"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_auto_label_pr_sdlc_yml_label["auto-label-pr-sdlc.yml#label"]
        job_build_bitwarden_lite_workflow_target_yml_build["build-bitwarden-lite-workflow-target.yml#build"]
        job_build_bitwarden_lite_workflow_target_yml_check_run["build-bitwarden-lite-workflow-target.yml#check-run"]
        job_build_bitwarden_lite_yml_build_docker["build-bitwarden-lite.yml#build-docker"]
        job_build_bitwarden_lite_yml_check_event_source["build-bitwarden-lite.yml#check-event-source"]
        job_build_bitwarden_lite_yml_setup["build-bitwarden-lite.yml#setup"]
        job_cleanup_container_images_yml_cleanup_images["cleanup-container-images.yml#cleanup-images"]
        job_enforce_pr_labels_sdlc_yml_enforce_label["enforce-pr-labels-sdlc.yml#enforce-label"]
        job_review_code_yml_review["review-code.yml#review"]
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
  pipeline_root(["bitwarden/self-host (6 workflows)"])
  grp_0_CI___Verification["CI & Verification (4 workflows · 5 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]
  pipeline_root --> grp_1_Automation___Other
  grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 3 jobs)"]
  pipeline_root --> grp_2_Scheduled___Manual
```
