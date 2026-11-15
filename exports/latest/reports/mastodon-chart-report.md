---
title: Architecture — mastodon/chart
description: Arc42 and Pipeline report for mastodon/chart
---

# Repository Architecture Analysis: mastodon/chart

## Metadata
- **SHA**: `7b553728474820d5e44dfcef5f91612aed9bafa4`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 35
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 35
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Helm Chart
- **import_edges**: 0 entry(ies)
- **loc**: 3521
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 2825
- **test_file_count**: 1

# Architecture: mastodon/chart

## Context
- **Repository**: `mastodon/chart`
- **SHA**: `7b553728474820d5e44dfcef5f91612aed9bafa4`
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
    repo_root(["mastodon/chart (35 components)"]):::atlasRoot
    dir_0_templates["templates (31)"]:::atlasCategory
    repo_root --> dir_0_templates
    sub_0_0__module_root_["(module root) (30)"]:::atlasWorkflow
    dir_0_templates --> sub_0_0__module_root_
    sub_0_1_tests["tests (1)"]:::atlasWorkflow
    dir_0_templates --> sub_0_1_tests
    dir_1__root_["(root) (3)"]:::atlasCategory
    repo_root --> dir_1__root_
    dir_2__github[".github (1)"]:::atlasCategory
    repo_root --> dir_2__github
```

## Component Details
- **Chart** (`Chart.yaml`): module
- **dev-values** (`dev-values.yaml`): module
- **values** (`values.yaml`): module
- **test-chart** (`.github/workflows/test-chart.yml`): module
- **_statsd** (`templates/_statsd.yaml`): module
- **configmap-env** (`templates/configmap-env.yaml`): module
- **cronjob-media-remove** (`templates/cronjob-media-remove.yaml`): module
- **deployment-sidekiq** (`templates/deployment-sidekiq.yaml`): module
- **deployment-streaming** (`templates/deployment-streaming.yaml`): module
- **deployment-web** (`templates/deployment-web.yaml`): module
- **httproute-streaming** (`templates/httproute-streaming.yaml`): module
- **httproute** (`templates/httproute.yaml`): module
- **ingress-streaming** (`templates/ingress-streaming.yml`): module
- **ingress** (`templates/ingress.yaml`): module
- **job-assets-copy** (`templates/job-assets-copy.yaml`): module
- **job-create-admin** (`templates/job-create-admin.yaml`): module
- **job-db-migrate** (`templates/job-db-migrate.yaml`): module
- **job-db-pre-migrate** (`templates/job-db-pre-migrate.yaml`): module
- **job-db-prepare** (`templates/job-db-prepare.yaml`): module
- **job-deploy-search** (`templates/job-deploy-search.yaml`): module
- **pdb-streaming** (`templates/pdb-streaming.yaml`): module
- **pdb-web** (`templates/pdb-web.yaml`): module
- **pvc-assets** (`templates/pvc-assets.yaml`): module
- **pvc-system** (`templates/pvc-system.yaml`): module
- **secret-prepare** (`templates/secret-prepare.yml`): module
- **secret-redis-preinstall** (`templates/secret-redis-preinstall.yaml`): module
- **secret-redis** (`templates/secret-redis.yaml`): module
- **secret-smtp-bulk** (`templates/secret-smtp-bulk.yaml`): module
- **secret-smtp** (`templates/secret-smtp.yaml`): module
- **secrets** (`templates/secrets.yaml`): module
- **service-streaming** (`templates/service-streaming.yaml`): module
- **service-web** (`templates/service-web.yaml`): module
- **serviceaccount** (`templates/serviceaccount.yaml`): module
- **statsd-exporter-mappings** (`templates/statsd-exporter-mappings.yaml`): module
- **test-connection** (`templates/tests/test-connection.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (88.60/100)
- **Technical Debt Score**: 11.40
- **Estimated Remediation Effort**: 7.35h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `A` | 96.00 | 0.15 | workflows=1, operational_antipatterns=2, parallel_branches=True |
| Security | `C` | 76.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=2 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_1635b4c7_8da3_4f16_a3e7_5ccb0559e4ca["1635b4c7-8da3-4f16-a3e7-5ccb0559e4ca"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_test_chart_yml_lint_templates["test-chart.yml#lint-templates"]:::atlasJob
        job_test_chart_yml_test_install["test-chart.yml#test-install"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_kubernetes["kubernetes"]:::atlasTarget
    end
    job_test_chart_yml_lint_templates -->|DEPLOYS_TO| env_kubernetes
    job_test_chart_yml_test_install -->|DEPLOYS_TO| env_kubernetes
    mod_1635b4c7_8da3_4f16_a3e7_5ccb0559e4ca -->|BUILT_BY| job_test_chart_yml_lint_templates
    mod_1635b4c7_8da3_4f16_a3e7_5ccb0559e4ca -->|DEPLOYED_BY| job_test_chart_yml_test_install
```

- `test-chart.yml#lint-templates` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-chart.yml#test-install` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `1635b4c7-8da3-4f16-a3e7-5ccb0559e4ca` (code_module) --[BUILT_BY]--> `test-chart.yml#lint-templates` (ci_job)
- `1635b4c7-8da3-4f16-a3e7-5ccb0559e4ca` (code_module) --[DEPLOYED_BY]--> `test-chart.yml#test-install` (ci_job)


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
  subgraph Test_chart_0["Test chart"]
    direction TB
    0_lint_templates["lint-templates"]:::atlasJob
    0_test_install["test-install"]:::atlasJob
  end
```
