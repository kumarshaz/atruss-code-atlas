---
title: Architecture — langfuse/langfuse-k8s
description: Arc42 and Pipeline report for langfuse/langfuse-k8s
---

# Repository Architecture Analysis: langfuse/langfuse-k8s

## Metadata
- **SHA**: `a2d42cd4db1b50bbcca800e2d3b870a09a17d7a0`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 67
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 67
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Helm Chart
- **import_edges**: 0 entry(ies)
- **loc**: 7678
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 6653
- **test_file_count**: 36

# Architecture: langfuse/langfuse-k8s

## Context
- **Repository**: `langfuse/langfuse-k8s`
- **SHA**: `a2d42cd4db1b50bbcca800e2d3b870a09a17d7a0`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Helm Chart

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
    repo_root(["langfuse/langfuse-k8s (67 components)"]):::atlasRoot
    dir_0_charts_langfuse_tests["charts/langfuse/tests (36)"]:::atlasCategory
    repo_root --> dir_0_charts_langfuse_tests
    sub_0_0__module_root_["(module root) (27)"]:::atlasWorkflow
    dir_0_charts_langfuse_tests --> sub_0_0__module_root_
    sub_0_1_values["values (9)"]:::atlasWorkflow
    dir_0_charts_langfuse_tests --> sub_0_1_values
    dir_1_charts_langfuse_templates["charts/langfuse/templates (27)"]:::atlasCategory
    repo_root --> dir_1_charts_langfuse_templates
    sub_1_0__module_root_["(module root) (7)"]:::atlasWorkflow
    dir_1_charts_langfuse_templates --> sub_1_0__module_root_
    sub_1_1_web["web (6)"]:::atlasWorkflow
    dir_1_charts_langfuse_templates --> sub_1_1_web
    sub_1_2_gateway["gateway (5)"]:::atlasWorkflow
    dir_1_charts_langfuse_templates --> sub_1_2_gateway
    sub_1_more["+3 more submodules (9)"]:::atlasMore
    dir_1_charts_langfuse_templates --> sub_1_more
    dir_2_charts_langfuse["charts/langfuse (4)"]:::atlasCategory
    repo_root --> dir_2_charts_langfuse
```

## Component Details

Showing top 60 representative components out of 67 across 3 module group(s):

- **Module `charts/langfuse/tests`** (36 components — module: 36)
- **Module `charts/langfuse/templates`** (27 components — module: 27)
- **Module `charts/langfuse`** (4 components — module: 4)

- **Chart** (`charts/langfuse/Chart.yaml`): module
- **ai_features_test** (`charts/langfuse/tests/ai_features_test.yaml`): module
- **auth-providers_test** (`charts/langfuse/tests/auth-providers_test.yaml`): module
- **basic_test** (`charts/langfuse/tests/basic_test.yaml`): module
- **bundled-store-auth_test** (`charts/langfuse/tests/bundled-store-auth_test.yaml`): module
- **clickhouse-cluster_test** (`charts/langfuse/tests/clickhouse-cluster_test.yaml`): module
- **clickhouse-crd-preflight_test** (`charts/langfuse/tests/clickhouse-crd-preflight_test.yaml`): module
- **clickhouse-image-tag_test** (`charts/langfuse/tests/clickhouse-image-tag_test.yaml`): module
- **clickhouse-logger_test** (`charts/langfuse/tests/clickhouse-logger_test.yaml`): module
- **clickhouse-pull-secrets_test** (`charts/langfuse/tests/clickhouse-pull-secrets_test.yaml`): module
- **clickhouse-resources_test** (`charts/langfuse/tests/clickhouse-resources_test.yaml`): module
- **cluster** (`charts/langfuse/templates/clickhouse/cluster.yaml`): module
- **deployment** (`charts/langfuse/templates/gateway/deployment.yaml`): module
- **deployment** (`charts/langfuse/templates/web/deployment.yaml`): module
- **deployment** (`charts/langfuse/templates/worker/deployment.yaml`): module
- **deployment-replicas_test** (`charts/langfuse/tests/deployment-replicas_test.yaml`): module
- **downward-api-base** (`charts/langfuse/tests/values/downward-api-base.yaml`): module
- **downward-api-examples** (`charts/langfuse/tests/values/downward-api-examples.yaml`): module
- **downward-api_test** (`charts/langfuse/tests/downward-api_test.yaml`): module
- **extra-all-containers** (`charts/langfuse/tests/values/extra-all-containers.yaml`): module
- **extra-all-env** (`charts/langfuse/tests/values/extra-all-env.yaml`): module
- **extra-containers_test** (`charts/langfuse/tests/extra-containers_test.yaml`): module
- **extra-env_test** (`charts/langfuse/tests/extra-env_test.yaml`): module
- **extra-manifests** (`charts/langfuse/templates/extra-manifests.yaml`): module
- **extra-web-containers** (`charts/langfuse/tests/values/extra-web-containers.yaml`): module
- **extra-worker-containers** (`charts/langfuse/tests/values/extra-worker-containers.yaml`): module
- **gateway_test** (`charts/langfuse/tests/gateway_test.yaml`): module
- **hpa** (`charts/langfuse/templates/gateway/hpa.yaml`): module
- **hpa** (`charts/langfuse/templates/web/hpa.yaml`): module
- **hpa** (`charts/langfuse/templates/worker/hpa.yaml`): module
- **hpa-annotations** (`charts/langfuse/tests/values/hpa-annotations.yaml`): module
- **hpa_test** (`charts/langfuse/tests/hpa_test.yaml`): module
- **ingress** (`charts/langfuse/templates/gateway/ingress.yaml`): module
- **ingress** (`charts/langfuse/templates/ingress.yaml`): module
- **ingress_test** (`charts/langfuse/tests/ingress_test.yaml`): module
- **keeper** (`charts/langfuse/templates/clickhouse/keeper.yaml`): module
- **langfuse-app-secret** (`charts/langfuse/templates/langfuse-app-secret.yaml`): module
- **langfuse-app-secret_test** (`charts/langfuse/tests/langfuse-app-secret_test.yaml`): module
- **minimal-installation_test** (`charts/langfuse/tests/minimal-installation_test.yaml`): module
- **pdb** (`charts/langfuse/templates/gateway/pdb.yaml`): module
- **pdb** (`charts/langfuse/templates/web/pdb.yaml`): module
- **pdb** (`charts/langfuse/templates/worker/pdb.yaml`): module
- **pdb** (`charts/langfuse/tests/values/pdb.yaml`): module
- **postgresql-secret** (`charts/langfuse/templates/postgresql-secret.yaml`): module
- **priority-class_test** (`charts/langfuse/tests/priority-class_test.yaml`): module
- **redis-cluster_test** (`charts/langfuse/tests/redis-cluster_test.yaml`): module
- **redis-secret** (`charts/langfuse/templates/redis-secret.yaml`): module
- **release-name_test** (`charts/langfuse/tests/release-name_test.yaml`): module
- **s3-force-path-style_test** (`charts/langfuse/tests/s3-force-path-style_test.yaml`): module
- **s3-media-upload-validation_test** (`charts/langfuse/tests/s3-media-upload-validation_test.yaml`): module
- **scaled-object** (`charts/langfuse/templates/web/scaled-object.yaml`): module
- **scaled-object** (`charts/langfuse/templates/worker/scaled-object.yaml`): module
- **seaweedfs-image_test** (`charts/langfuse/tests/seaweedfs-image_test.yaml`): module
- **secret** (`charts/langfuse/templates/clickhouse/secret.yaml`): module
- **secret** (`charts/langfuse/templates/s3/secret.yaml`): module
- **service** (`charts/langfuse/templates/gateway/service.yaml`): module
- **service** (`charts/langfuse/templates/web/service.yaml`): module
- **serviceaccount** (`charts/langfuse/templates/serviceaccount.yaml`): module
- **v1-upgrade-guard_test** (`charts/langfuse/tests/v1-upgrade-guard_test.yaml`): module
- **validations** (`charts/langfuse/templates/validations.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (72.75/100)
- **Technical Debt Score**: 27.25
- **Estimated Remediation Effort**: 19.31h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 25.00 | 0.15 | workflows=5, operational_antipatterns=8, parallel_branches=False |
| Security | `F` | 50.00 | 0.20 | vulnerabilities=0, secrets=2, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 0 | **Vulnerabilities**: 0 | **Secrets**: 2

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `README.md:467` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `examples/minimal-installation/secret.yaml:39` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_charts_langfuse["charts/langfuse"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_release_yaml_release["release.yaml#release"]:::atlasJob
        job_test_yaml_unit_tests["test.yaml#unit-tests"]:::atlasJob
        job_update_langfuse_version_yml_check_and_update["update-langfuse-version.yml#check-and-update"]:::atlasJob
        job_validate_yaml_validate["validate.yaml#validate"]:::atlasJob
        job_zizmor_yml_zizmor["zizmor.yml#zizmor"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_azure["azure"]:::atlasTarget
        env_kubernetes["kubernetes"]:::atlasTarget
    end
    job_release_yaml_release -->|DEPLOYS_TO| env_azure
    job_release_yaml_release -->|DEPLOYS_TO| env_kubernetes
    job_test_yaml_unit_tests -->|DEPLOYS_TO| env_azure
    job_test_yaml_unit_tests -->|DEPLOYS_TO| env_kubernetes
    job_validate_yaml_validate -->|DEPLOYS_TO| env_azure
    job_validate_yaml_validate -->|DEPLOYS_TO| env_kubernetes
    mod_charts_langfuse -->|BUILT_BY| job_update_langfuse_version_yml_check_and_update
    mod_charts_langfuse -->|BUILT_BY| job_zizmor_yml_zizmor
    mod_charts_langfuse -->|DEPLOYED_BY| job_release_yaml_release
    mod_charts_langfuse -->|DEPLOYED_BY| job_test_yaml_unit_tests
    mod_charts_langfuse -->|DEPLOYED_BY| job_validate_yaml_validate
```

- `release.yaml#release` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `release.yaml#release` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test.yaml#unit-tests` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `test.yaml#unit-tests` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `validate.yaml#validate` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `validate.yaml#validate` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `charts/langfuse` (code_module) --[BUILT_BY]--> `update-langfuse-version.yml#check-and-update` (ci_job)
- `charts/langfuse` (code_module) --[BUILT_BY]--> `zizmor.yml#zizmor` (ci_job)
- `charts/langfuse` (code_module) --[DEPLOYED_BY]--> `release.yaml#release` (ci_job)
- `charts/langfuse` (code_module) --[DEPLOYED_BY]--> `test.yaml#unit-tests` (ci_job)
- `charts/langfuse` (code_module) --[DEPLOYED_BY]--> `validate.yaml#validate` (ci_job)


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
  pipeline_root(["langfuse/langfuse-k8s (5 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_1_Unit_Tests["Unit Tests (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_1_Unit_Tests
  job_1_unit_tests["unit-tests"]:::atlasJob
  wf_1_Unit_Tests --> job_1_unit_tests
  wf_3_Validate_Helm_Charts["Validate Helm Charts (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_3_Validate_Helm_Charts
  job_3_validate["validate"]:::atlasJob
  wf_3_Validate_Helm_Charts --> job_3_validate
  grp_1_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Scheduled___Manual
  wf_2_Update_Langfuse_Version["Update Langfuse Version (1 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_2_Update_Langfuse_Version
  job_2_check_and_update["check-and-update"]:::atlasJob
  wf_2_Update_Langfuse_Version --> job_2_check_and_update
  wf_4_Check_GitHub_Actions["Check GitHub Actions (1 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_4_Check_GitHub_Actions
  job_4_zizmor["zizmor"]:::atlasJob
  wf_4_Check_GitHub_Actions --> job_4_zizmor
  grp_2_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Release___Deploy
  wf_0_Release_Charts["Release Charts (1 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_0_Release_Charts
  job_0_release["release"]:::atlasJob
  wf_0_Release_Charts --> job_0_release
```
