---
title: Architecture — getsentry/self-hosted
description: Arc42 and Pipeline report for getsentry/self-hosted
---

# Repository Architecture Analysis: getsentry/self-hosted

## Metadata
- **SHA**: `2c7379ea6ca9ce199d34e2c737758a0e034168b1`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.97
- **avg_cyclomatic_complexity**: 1.38
- **component_count**: 3
- **dead_code_count**: 1
- **dead_code_symbols**: 1 entry(ies)
- **duplication_pct**: 52.14
- **file_complexities**: 11 entry(ies)
- **files_analyzed**: 13
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: Unknown
- **import_edges**: 70 entry(ies)
- **loc**: 1871
- **max_cognitive_complexity**: 12
- **max_cyclomatic_complexity**: 10
- **sloc**: 1184
- **test_file_count**: 4

# Architecture: getsentry/self-hosted

## Context
- **Repository**: `getsentry/self-hosted`
- **SHA**: `2c7379ea6ca9ce199d34e2c737758a0e034168b1`
- **Ecosystem**: Python
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
    docker_compose_test["docker-compose.test : module"]:::atlasJob
    sentry_self_hosted_integration_test_nodejs["sentry-self-hosted-integration-test-nodejs : MODULE"]:::atlasJob
    config_example["config.example : module"]:::atlasJob
```

## Component Details
- **docker-compose.test** (`_integration-test/custom-ca-roots/docker-compose.test.yml`): module
- **sentry-self-hosted-integration-test-nodejs** (`_integration-test/nodejs/package.json`): MODULE
- **config.example** (`sentry/config.example.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (59.60/100)
- **Technical Debt Score**: 40.40
- **Estimated Remediation Effort**: 44.78h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `C` | 73.00 | 0.20 | avg_cc=1.38, max_cc=10, duplication=52.14%, dead_code=1 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=55, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `B` | 84.00 | 0.15 | avg_cognitive=0.97, max_cognitive=12, fitness_violations=1, oversized_files=2 |
| Pipeline Health | `F` | 26.00 | 0.15 | workflows=7, operational_antipatterns=11, parallel_branches=True |
| Security | `F` | 15.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=5 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (52.14) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 55 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `sentry/config.example.yml:135` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `beautifulsoup4` `4.14.2` (PyPI, `uv.lock`)
- `beautifulsoup4` `4.7.1` (PyPI, `pyproject.toml`)
- `cryptography` `48.0.1` (PyPI, `pyproject.toml`)
- `cryptography` `48.0.1` (PyPI, `uv.lock`)
- `httpx` `0.25.2` (PyPI, `pyproject.toml`)
- `httpx` `0.28.1` (PyPI, `uv.lock`)
- `pytest` `9.0.3` (PyPI, `pyproject.toml`)
- `pytest` `9.0.3` (PyPI, `uv.lock`)
- `pytest-cov` `4.1.0` (PyPI, `pyproject.toml`)
- `pytest-cov` `7.0.0` (PyPI, `uv.lock`)
- `pytest-rerunfailures` `11.0` (PyPI, `pyproject.toml`)
- `pytest-rerunfailures` `16.1` (PyPI, `uv.lock`)
- `pytest-sentry` `0.1.11` (PyPI, `pyproject.toml`)
- `pytest-sentry` `0.3.3` (PyPI, `uv.lock`)
- `sentry-sdk` `2.58.0` (PyPI, `pyproject.toml`)
- `sentry-sdk` `2.58.0` (PyPI, `uv.lock`)
- `@sentry/node` `10.58.0` (npm, `_integration-test/nodejs/package-lock.json`)
- `@sentry/node` `10.58.0` (npm, `_integration-test/nodejs/package.json`)
- `anyio` `4.14.2` (PyPI, `uv.lock`)
- `certifi` `2026.10.19` (PyPI, `uv.lock`)
- `cffi` `2.0.0` (PyPI, `uv.lock`)
- `colorama` `0.4.6` (PyPI, `uv.lock`)
- `coverage` `7.12.0` (PyPI, `uv.lock`)
- `h11` `0.16.0` (PyPI, `uv.lock`)
- `httpcore` `1.0.9` (PyPI, `uv.lock`)
- `idna` `3.11` (PyPI, `uv.lock`)
- `iniconfig` `2.3.0` (PyPI, `uv.lock`)
- `packaging` `25.0` (PyPI, `uv.lock`)
- `pluggy` `1.6.0` (PyPI, `uv.lock`)
- `pycparser` `2.23` (PyPI, `uv.lock`)
- ... (+25 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod__integration_test_custom_ca_roots["_integration-test/custom-ca-roots"]:::atlasCategory
        mod_clickhouse["clickhouse"]:::atlasCategory
        mod_cron["cron"]:::atlasCategory
        mod_e812dfff_95b8_4b5a_87f0_e9f284e5f7b5["e812dfff-95b8-4b5a-87f0-e9f284e5f7b5"]:::atlasCategory
        mod_sentry["sentry"]:::atlasCategory
        mod_workstation_postinstall["workstation/postinstall"]:::atlasCategory
        mod_workstation_preinstall["workstation/preinstall"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__integration_test_custom_ca_roots_docker_compose_test_yml["_integration-test/custom-ca-roots/docker-compose.test.yml"]:::atlasWorkflow
        art_clickhouse_Dockerfile["clickhouse/Dockerfile"]:::atlasWorkflow
        art_cron_Dockerfile["cron/Dockerfile"]:::atlasWorkflow
        art_docker_compose_yml["docker-compose.yml"]:::atlasWorkflow
        art_sentry_Dockerfile["sentry/Dockerfile"]:::atlasWorkflow
        art_workstation_postinstall_Dockerfile["workstation/postinstall/Dockerfile"]:::atlasWorkflow
        art_workstation_preinstall_Dockerfile["workstation/preinstall/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_fast_revert_yml_revert["fast-revert.yml#revert"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_fast_revert["fast-revert"]:::atlasTarget
    end
    job_fast_revert_yml_revert -->|DEPLOYS_TO| env_fast_revert
    mod__integration_test_custom_ca_roots -->|PACKAGED_BY| art__integration_test_custom_ca_roots_docker_compose_test_yml
    mod_clickhouse -->|PACKAGED_BY| art_clickhouse_Dockerfile
    mod_clickhouse -->|PACKAGED_BY| art_docker_compose_yml
    mod_cron -->|PACKAGED_BY| art_cron_Dockerfile
    mod_e812dfff_95b8_4b5a_87f0_e9f284e5f7b5 -->|PACKAGED_BY| art_docker_compose_yml
    mod_sentry -->|PACKAGED_BY| art_docker_compose_yml
    mod_sentry -->|PACKAGED_BY| art_sentry_Dockerfile
    mod_sentry -->|PACKAGED_BY| art_workstation_postinstall_Dockerfile
    mod_sentry -->|PACKAGED_BY| art_workstation_preinstall_Dockerfile
    mod_workstation_postinstall -->|PACKAGED_BY| art_workstation_postinstall_Dockerfile
    mod_workstation_preinstall -->|PACKAGED_BY| art_workstation_preinstall_Dockerfile
```

- `fast-revert.yml#revert` (ci_job) --[DEPLOYS_TO]--> `fast-revert` (environment)
- `_integration-test/custom-ca-roots` (code_module) --[PACKAGED_BY]--> `_integration-test/custom-ca-roots/docker-compose.test.yml` (container)
- `clickhouse` (code_module) --[PACKAGED_BY]--> `clickhouse/Dockerfile` (container)
- `clickhouse` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `cron` (code_module) --[PACKAGED_BY]--> `cron/Dockerfile` (container)
- `e812dfff-95b8-4b5a-87f0-e9f284e5f7b5` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `sentry` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `sentry` (code_module) --[PACKAGED_BY]--> `sentry/Dockerfile` (container)
- `sentry` (code_module) --[PACKAGED_BY]--> `workstation/postinstall/Dockerfile` (container)
- `sentry` (code_module) --[PACKAGED_BY]--> `workstation/preinstall/Dockerfile` (container)
- `workstation/postinstall` (code_module) --[PACKAGED_BY]--> `workstation/postinstall/Dockerfile` (container)
- `workstation/preinstall` (code_module) --[PACKAGED_BY]--> `workstation/preinstall/Dockerfile` (container)


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
  pipeline_root(["getsentry/self-hosted (7 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_0_Enforce_License_Compliance["Enforce License Compliance (1 jobs)"]
      direction TB
      wf_0_Enforce_License_Compliance(["Trigger: Enforce License Compliance"]):::atlasWorkflow
      job_0_enforce_license_compliance["enforce-license-compliance"]:::atlasJob
      wf_0_Enforce_License_Compliance --> job_0_enforce_license_compliance
    end
    pipeline_root --> wf_0_Enforce_License_Compliance
    subgraph sg_wf_3_pre_commit["pre-commit (1 jobs)"]
      direction TB
      wf_3_pre_commit(["Trigger: pre-commit"]):::atlasWorkflow
      job_3_pre_commit["pre-commit"]:::atlasJob
      wf_3_pre_commit --> job_3_pre_commit
    end
    pipeline_root --> wf_3_pre_commit
    subgraph sg_wf_5_ShellCheck["ShellCheck (1 jobs)"]
      direction TB
      wf_5_ShellCheck(["Trigger: ShellCheck"]):::atlasWorkflow
      job_5_shellcheck["shellcheck"]:::atlasJob
      wf_5_ShellCheck --> job_5_shellcheck
    end
    pipeline_root --> wf_5_ShellCheck
  end
  subgraph sg_grp_1_Scheduled___Manual["Scheduled & Manual (2 workflows · 4 jobs)"]
    direction TB
    subgraph sg_wf_1_fast_revert_yml["fast-revert.yml (1 jobs)"]
      direction TB
      wf_1_fast_revert_yml(["Trigger: fast-revert.yml"]):::atlasWorkflow
      job_1_revert["revert"]:::atlasJob
      wf_1_fast_revert_yml --> job_1_revert
    end
    pipeline_root --> wf_1_fast_revert_yml
    subgraph sg_wf_6_Test["Test (3 jobs)"]
      direction TB
      wf_6_Test(["Trigger: Test"]):::atlasWorkflow
      job_6_unit_test["unit-test"]:::atlasJob
      job_6_integration_test["integration-test"]:::atlasJob
      job_6_integration_test_errors_only["integration-test-errors-only"]:::atlasJob
      wf_6_Test --> job_6_unit_test
      wf_6_Test --> job_6_integration_test
      wf_6_Test --> job_6_integration_test_errors_only
    end
    pipeline_root --> wf_6_Test
  end
  subgraph sg_grp_2_Release___Deploy["Release & Deploy (1 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_4_Release["Release (2 jobs)"]
      direction TB
      wf_4_Release(["Trigger: Release"]):::atlasWorkflow
      job_4_release["release"]:::atlasJob
      job_4_dogfood_release["dogfood-release"]:::atlasJob
      wf_4_Release --> job_4_release
      job_4_release --> job_4_dogfood_release
    end
    pipeline_root --> wf_4_Release
  end
  subgraph sg_grp_3_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_2_Lock_closed_issues_PRs["Lock closed issues/PRs (1 jobs)"]
      direction TB
      wf_2_Lock_closed_issues_PRs(["Trigger: Lock closed issues/PRs"]):::atlasWorkflow
      job_2_lock["lock"]:::atlasJob
      wf_2_Lock_closed_issues_PRs --> job_2_lock
    end
    pipeline_root --> wf_2_Lock_closed_issues_PRs
  end
```
