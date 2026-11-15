---
title: Architecture — home-assistant/builder
description: Arc42 and Pipeline report for home-assistant/builder
---

# Repository Architecture Analysis: home-assistant/builder

## Metadata
- **SHA**: `9b2658ea6ddfd83d528e5d8e37393893bf5e92d7`
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
- **framework**: Container
- **import_edges**: 0 entry(ies)
- **loc**: 14
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 14
- **test_file_count**: 2

# Architecture: home-assistant/builder

## Context
- **Repository**: `home-assistant/builder`
- **SHA**: `9b2658ea6ddfd83d528e5d8e37393893bf5e92d7`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Container

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
    config["config : module"]:::atlasJob
```

## Component Details
- **config** (`.github/tests/app/config.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (79.60/100)
- **Technical Debt Score**: 20.40
- **Estimated Remediation Effort**: 17.60h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 20.00 | 0.15 | workflows=3, operational_antipatterns=12, parallel_branches=True |
| Security | `B` | 88.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=1 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod__github_tests_app[".github/tests/app"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__github_tests_app_Dockerfile[".github/tests/app/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_release_drafter_yml_update_release_draft["release-drafter.yml#update_release_draft"]:::atlasJob
        job_test_actions_yml_app["test-actions.yml#app"]:::atlasJob
        job_test_actions_yml_check_publish["test-actions.yml#check_publish"]:::atlasJob
        job_test_actions_yml_skip_existing["test-actions.yml#skip_existing"]:::atlasJob
        job_test_build_app_yml_build["test-build-app.yml#build"]:::atlasJob
        job_test_build_app_yml_manifest["test-build-app.yml#manifest"]:::atlasJob
        job_test_build_app_yml_prepare["test-build-app.yml#prepare"]:::atlasJob
    end
    mod__github_tests_app -->|BUILT_BY| job_test_actions_yml_app
    mod__github_tests_app -->|BUILT_BY| job_test_actions_yml_skip_existing
    mod__github_tests_app -->|BUILT_BY| job_test_build_app_yml_build
    mod__github_tests_app -->|BUILT_BY| job_test_build_app_yml_prepare
    mod__github_tests_app -->|DEPLOYED_BY| job_release_drafter_yml_update_release_draft
    mod__github_tests_app -->|DEPLOYED_BY| job_test_actions_yml_check_publish
    mod__github_tests_app -->|DEPLOYED_BY| job_test_build_app_yml_manifest
    mod__github_tests_app -->|PACKAGED_BY| art__github_tests_app_Dockerfile
    art__github_tests_app_Dockerfile -->|BUILT_BY| job_test_actions_yml_skip_existing
    art__github_tests_app_Dockerfile -->|DEPLOYED_BY| job_release_drafter_yml_update_release_draft
    art__github_tests_app_Dockerfile -->|DEPLOYED_BY| job_test_actions_yml_check_publish
    art__github_tests_app_Dockerfile -->|DEPLOYED_BY| job_test_build_app_yml_manifest
```

- `.github/tests/app` (code_module) --[BUILT_BY]--> `test-actions.yml#app` (ci_job)
- `.github/tests/app` (code_module) --[BUILT_BY]--> `test-actions.yml#skip_existing` (ci_job)
- `.github/tests/app` (code_module) --[BUILT_BY]--> `test-build-app.yml#build` (ci_job)
- `.github/tests/app` (code_module) --[BUILT_BY]--> `test-build-app.yml#prepare` (ci_job)
- `.github/tests/app` (code_module) --[DEPLOYED_BY]--> `release-drafter.yml#update_release_draft` (ci_job)
- `.github/tests/app` (code_module) --[DEPLOYED_BY]--> `test-actions.yml#check_publish` (ci_job)
- `.github/tests/app` (code_module) --[DEPLOYED_BY]--> `test-build-app.yml#manifest` (ci_job)
- `.github/tests/app` (code_module) --[PACKAGED_BY]--> `.github/tests/app/Dockerfile` (container)
- `.github/tests/app/Dockerfile` (container) --[BUILT_BY]--> `test-actions.yml#skip_existing` (ci_job)
- `.github/tests/app/Dockerfile` (container) --[DEPLOYED_BY]--> `release-drafter.yml#update_release_draft` (ci_job)
- `.github/tests/app/Dockerfile` (container) --[DEPLOYED_BY]--> `test-actions.yml#check_publish` (ci_job)
- `.github/tests/app/Dockerfile` (container) --[DEPLOYED_BY]--> `test-build-app.yml#manifest` (ci_job)


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
  pipeline_root(["home-assistant/builder"]):::atlasRoot
  subgraph Release_Drafter_0["Release Drafter"]
    direction TB
    0_update_release_draft["update_release_draft"]:::atlasJob
  end
  pipeline_root --> 0_update_release_draft
  subgraph Test_actions_1["Test actions"]
    direction TB
    1_check_publish["check_publish"]:::atlasJob
    1_app["app"]:::atlasJob
    1_check_publish --> 1_app
    1_skip_existing["skip_existing"]:::atlasJob
    1_check_publish --> 1_skip_existing
    1_app --> 1_skip_existing
  end
  pipeline_root --> 1_check_publish
  subgraph Build_test_app_2["Build test app"]
    direction TB
    2_prepare["prepare"]:::atlasJob
    2_build["build"]:::atlasJob
    2_prepare --> 2_build
    2_manifest["manifest"]:::atlasJob
    2_prepare --> 2_manifest
    2_build --> 2_manifest
  end
  pipeline_root --> 2_prepare
```
