---
title: Architecture — goharbor/harbor-helm
description: Arc42 and Pipeline report for goharbor/harbor-helm
---

# Repository Architecture Analysis: goharbor/harbor-helm

## Metadata
- **SHA**: `ed46e35fc022100d90c9fd743e72ddc8b5b82de4`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 4
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 4
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Unknown
- **import_edges**: 0 entry(ies)
- **loc**: 243
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 207
- **test_file_count**: 24

# Architecture: goharbor/harbor-helm

## Context
- **Repository**: `goharbor/harbor-helm`
- **SHA**: `ed46e35fc022100d90c9fd743e72ddc8b5b82de4`
- **Ecosystem**: Go
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
    test["test : module"]:::atlasJob
    base["base : module"]:::atlasJob
    ingress_test["ingress_test : module"]:::atlasJob
    node_port_test["node_port_test : module"]:::atlasJob
```

## Component Details
- **test** (`test/test.go`): module
- **base** (`test/integration/base.go`): module
- **ingress_test** (`test/integration/ingress_test.go`): module
- **node_port_test** (`test/integration/node_port_test.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (58.40/100)
- **Technical Debt Score**: 41.60
- **Estimated Remediation Effort**: 41.90h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=3, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 1.00 | 0.15 | workflows=5, operational_antipatterns=10, parallel_branches=False |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=12 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 3 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `values.yaml:917` (`# htpasswdString: "harb***REDACTED***" # example string, bcrypt is the only accepted hashing algorithm in htpasswd here.`)

### Inventory Sample
- `github.com/gruntwork-io/terratest` `0.38.1` (golang, `test/go.mod`)
- `github.com/stretchr/testify` `1.7.0` (golang, `test/go.mod`)
- `k8s.io/api` `0.20.6` (golang, `test/go.mod`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_test["test"]:::atlasCategory
        mod_test_e2e["test/e2e"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_test_e2e_Dockerfile["test/e2e/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_integration_yaml_integration_test["integration.yaml#integration-test"]:::atlasJob
        job_lint_yaml_lint["lint.yaml#lint"]:::atlasJob
        job_publish_release_yaml_release["publish_release.yaml#release"]:::atlasJob
        job_unittest_yaml_unit_test["unittest.yaml#unit-test"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_azure["azure"]:::atlasTarget
        env_kubernetes["kubernetes"]:::atlasTarget
    end
    job_integration_yaml_integration_test -->|DEPLOYS_TO| env_kubernetes
    job_lint_yaml_lint -->|DEPLOYS_TO| env_azure
    job_lint_yaml_lint -->|DEPLOYS_TO| env_kubernetes
    job_publish_release_yaml_release -->|DEPLOYS_TO| env_azure
    job_publish_release_yaml_release -->|DEPLOYS_TO| env_kubernetes
    job_unittest_yaml_unit_test -->|DEPLOYS_TO| env_azure
    job_unittest_yaml_unit_test -->|DEPLOYS_TO| env_kubernetes
    mod_test -->|DEPLOYED_BY| job_integration_yaml_integration_test
    mod_test -->|DEPLOYED_BY| job_unittest_yaml_unit_test
    mod_test_e2e -->|PACKAGED_BY| art_test_e2e_Dockerfile
    art_test_e2e_Dockerfile -->|DEPLOYED_BY| job_integration_yaml_integration_test
```

- `integration.yaml#integration-test` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `lint.yaml#lint` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `lint.yaml#lint` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `publish_release.yaml#release` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `publish_release.yaml#release` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `unittest.yaml#unit-test` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `unittest.yaml#unit-test` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test` (code_module) --[DEPLOYED_BY]--> `integration.yaml#integration-test` (ci_job)
- `test` (code_module) --[DEPLOYED_BY]--> `unittest.yaml#unit-test` (ci_job)
- `test/e2e` (code_module) --[PACKAGED_BY]--> `test/e2e/Dockerfile` (container)
- `test/e2e/Dockerfile` (container) --[DEPLOYED_BY]--> `integration.yaml#integration-test` (ci_job)


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
  pipeline_root(["goharbor/harbor-helm (5 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_1_Integration_test["Integration test (1 jobs)"]
      direction TB
      wf_1_Integration_test(["Trigger: Integration test"]):::atlasWorkflow
      job_1_integration_test["integration-test"]:::atlasJob
      wf_1_Integration_test --> job_1_integration_test
    end
    pipeline_root --> wf_1_Integration_test
    subgraph sg_wf_2_Lint["Lint (1 jobs)"]
      direction TB
      wf_2_Lint(["Trigger: Lint"]):::atlasWorkflow
      job_2_lint["lint"]:::atlasJob
      wf_2_Lint --> job_2_lint
    end
    pipeline_root --> wf_2_Lint
    subgraph sg_wf_4_Unit_test["Unit test (1 jobs)"]
      direction TB
      wf_4_Unit_test(["Trigger: Unit test"]):::atlasWorkflow
      job_4_unit_test["unit-test"]:::atlasJob
      wf_4_Unit_test --> job_4_unit_test
    end
    pipeline_root --> wf_4_Unit_test
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_3_Publish_Release["Publish Release (1 jobs)"]
      direction TB
      wf_3_Publish_Release(["Trigger: Publish Release"]):::atlasWorkflow
      job_3_release["release"]:::atlasJob
      wf_3_Publish_Release --> job_3_release
    end
    pipeline_root --> wf_3_Publish_Release
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_0_Housekeeping___Close_stale_issues_and_PRs["Housekeeping - Close stale issues and PRs (1 jobs)"]
      direction TB
      wf_0_Housekeeping___Close_stale_issues_and_PRs(["Trigger: Housekeeping - Close stale issues and PRs"]):::atlasWorkflow
      job_0_stale["stale"]:::atlasJob
      wf_0_Housekeeping___Close_stale_issues_and_PRs --> job_0_stale
    end
    pipeline_root --> wf_0_Housekeeping___Close_stale_issues_and_PRs
  end
```
