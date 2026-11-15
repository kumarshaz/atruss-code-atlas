---
title: Architecture — home-assistant/operating-system
description: Arc42 and Pipeline report for home-assistant/operating-system
---

# Repository Architecture Analysis: home-assistant/operating-system

## Metadata
- **SHA**: `945ba38d88e7e7d7321d42294b222b8deb2208d2`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 6.44
- **avg_cyclomatic_complexity**: 4.53
- **component_count**: 0
- **dead_code_count**: 1
- **dead_code_symbols**: 1 entry(ies)
- **duplication_pct**: 55.07
- **file_complexities**: 8 entry(ies)
- **files_analyzed**: 8
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 65 entry(ies)
- **loc**: 8090
- **max_cognitive_complexity**: 89
- **max_cyclomatic_complexity**: 45
- **sloc**: 5113
- **test_file_count**: 12

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (38.78/100)
- **Technical Debt Score**: 61.22
- **Estimated Remediation Effort**: 62.57h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 41.88 | 0.20 | avg_cc=4.53, max_cc=45, duplication=55.07%, dead_code=1 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=3, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 47.68 | 0.15 | avg_cognitive=6.44, max_cognitive=89, fitness_violations=3, oversized_files=1 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=9, operational_antipatterns=19, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=9 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (55.07) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (89.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (45.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 3 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `.github/workflows/build.yaml:326` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `labgrid` `26.0.1` (PyPI, `tests/requirements.txt`)
- `pytest-dependency` `0.6.1` (PyPI, `tests/requirements.txt`)
- `pytest-timeout` `2.4.0` (PyPI, `tests/requirements.txt`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_d4391456_6227_409f_8b8e_ba95e5bf13c2["d4391456-6227-409f-8b8e-ba95e5bf13c2"]
        mod_tests["tests"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_artifacts_index_yaml_build_index["artifacts-index.yaml#build-index"]
        job_build_yaml_build["build.yaml#build"]
        job_build_yaml_bump_version["build.yaml#bump_version"]
        job_build_yaml_prepare["build.yaml#prepare"]
        job_build_yaml_sign["build.yaml#sign"]
        job_pr_checks_yml_linters["pr-checks.yml#linters"]
        job_test_yaml_test["test.yaml#test"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_____needs_prepare_outputs_channel___["${{ needs.prepare.outputs.channel }}"]
        env_aws["aws"]
    end
    job_artifacts_index_yaml_build_index -->|DEPLOYS_TO| env_aws
    job_build_yaml_build -->|DEPLOYS_TO| env_aws
    job_build_yaml_bump_version -->|DEPLOYS_TO| env_____needs_prepare_outputs_channel___
    job_build_yaml_sign -->|DEPLOYS_TO| env_aws
    mod_d4391456_6227_409f_8b8e_ba95e5bf13c2 -->|BUILT_BY| job_build_yaml_prepare
    mod_d4391456_6227_409f_8b8e_ba95e5bf13c2 -->|BUILT_BY| job_pr_checks_yml_linters
    mod_d4391456_6227_409f_8b8e_ba95e5bf13c2 -->|PACKAGED_BY| art_Dockerfile
    mod_tests -->|BUILT_BY| job_test_yaml_test
    art_Dockerfile -->|BUILT_BY| job_build_yaml_prepare
    art_Dockerfile -->|BUILT_BY| job_pr_checks_yml_linters
```

- `artifacts-index.yaml#build-index` (ci_job) --[DEPLOYS_TO]--> `aws` (environment)
- `build.yaml#build` (ci_job) --[DEPLOYS_TO]--> `aws` (environment)
- `build.yaml#bump_version` (ci_job) --[DEPLOYS_TO]--> `${{ needs.prepare.outputs.channel }}` (environment)
- `build.yaml#sign` (ci_job) --[DEPLOYS_TO]--> `aws` (environment)
- `d4391456-6227-409f-8b8e-ba95e5bf13c2` (code_module) --[BUILT_BY]--> `build.yaml#prepare` (ci_job)
- `d4391456-6227-409f-8b8e-ba95e5bf13c2` (code_module) --[BUILT_BY]--> `pr-checks.yml#linters` (ci_job)
- `d4391456-6227-409f-8b8e-ba95e5bf13c2` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `tests` (code_module) --[BUILT_BY]--> `test.yaml#test` (ci_job)
- `Dockerfile` (container) --[BUILT_BY]--> `build.yaml#prepare` (ci_job)
- `Dockerfile` (container) --[BUILT_BY]--> `pr-checks.yml#linters` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["home-assistant/operating-system (9 workflows)"])
  grp_0_CI___Verification["CI & Verification (2 workflows · 2 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Release___Deploy["Release & Deploy (2 workflows · 7 jobs)"]
  pipeline_root --> grp_1_Release___Deploy
  grp_2_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]
  pipeline_root --> grp_2_Scheduled___Manual
  grp_3_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]
  pipeline_root --> grp_3_Security___Governance
  grp_4_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]
  pipeline_root --> grp_4_Automation___Other
```
