---
title: Architecture — home-assistant/android
description: Arc42 and Pipeline report for home-assistant/android
---

# Repository Architecture Analysis: home-assistant/android

## Metadata
- **SHA**: `6f48337910158c5ca1a3965e499143114bd6a3d3`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 6.56
- **avg_cyclomatic_complexity**: 11.56
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 85.47
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 1341
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 195015
- **max_cognitive_complexity**: 526
- **max_cyclomatic_complexity**: 339
- **sloc**: 156508
- **test_file_count**: 296

# Architecture: home-assistant/android

## Context
- **Repository**: `home-assistant/android`
- **SHA**: `6f48337910158c5ca1a3965e499143114bd6a3d3`
- **Ecosystem**: Java
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
    Home["Home : DATA_ACCESS_LAYER"]:::atlasJob
```

## Component Details
- **Home** (`lint/src/test/kotlin/io/homeassistant/lint/room/RoomEntityMutablePropertiesIssueTest.kt`): DATA_ACCESS_LAYER

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (34.35/100)
- **Technical Debt Score**: 65.65
- **Estimated Remediation Effort**: 172.51h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 20.00 | 0.20 | avg_cc=11.56, max_cc=339, duplication=85.47%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=2, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 32.32 | 0.15 | avg_cognitive=6.56, max_cognitive=526, fitness_violations=3, oversized_files=15 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=12, operational_antipatterns=39, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=50 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (85.47) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (526.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (339.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 2 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `.github/e2e/homeassistant/.storage/auth_provider.homeassistant:9` (`"password": "JDJi***REDACTED***"`)

### Inventory Sample
- `fastlane` `*` (gem, `Gemfile`)
- `fastlane-plugin-amazon_app_submission` `*` (gem, `Gemfile`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_app["app"]:::atlasCategory
        mod_automotive["automotive"]:::atlasCategory
        mod_common["common"]:::atlasCategory
        mod_lint["lint"]:::atlasCategory
        mod_wear["wear"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_e2e_triage_lock_yml_agent["e2e-triage.lock.yml#agent"]:::atlasJob
        job_e2e_triage_lock_yml_detection["e2e-triage.lock.yml#detection"]:::atlasJob
        job_e2e_yml_maestro["e2e.yml#maestro"]:::atlasJob
        job_onPush_yml_app_build["onPush.yml#app_build"]:::atlasJob
        job_pr_emulator_wtf_yml_check_inputs["pr-emulator-wtf.yml#check_inputs"]:::atlasJob
        job_pr_emulator_wtf_yml_emulator_wtf["pr-emulator-wtf.yml#emulator_wtf"]:::atlasJob
        job_pr_yml_build_emulator_wtf_apks["pr.yml#build_emulator_wtf_apks"]:::atlasJob
        job_pr_yml_ktlint["pr.yml#ktlint"]:::atlasJob
        job_pr_yml_license_check["pr.yml#license_check"]:::atlasJob
        job_pr_yml_lint["pr.yml#lint"]:::atlasJob
        job_pr_yml_pr_build["pr.yml#pr_build"]:::atlasJob
        job_pr_yml_unit_tests["pr.yml#unit_tests"]:::atlasJob
        job_pr_yml_validate_localize_setup["pr.yml#validate_localize_setup"]:::atlasJob
        job_pr_yml_yamllint["pr.yml#yamllint"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_ui_test["ui-test"]:::atlasTarget
    end
    job_e2e_yml_maestro -->|DEPLOYS_TO| env_ui_test
    job_pr_emulator_wtf_yml_emulator_wtf -->|DEPLOYS_TO| env_ui_test
    mod_app -->|BUILT_BY| job_e2e_triage_lock_yml_agent
    mod_app -->|BUILT_BY| job_e2e_triage_lock_yml_detection
    mod_app -->|BUILT_BY| job_pr_emulator_wtf_yml_check_inputs
    mod_app -->|BUILT_BY| job_pr_yml_build_emulator_wtf_apks
    mod_app -->|BUILT_BY| job_pr_yml_license_check
    mod_app -->|BUILT_BY| job_pr_yml_pr_build
    mod_app -->|BUILT_BY| job_pr_yml_unit_tests
    mod_app -->|DEPLOYED_BY| job_e2e_yml_maestro
    mod_app -->|DEPLOYED_BY| job_onPush_yml_app_build
    mod_app -->|DEPLOYED_BY| job_pr_emulator_wtf_yml_emulator_wtf
    mod_automotive -->|BUILT_BY| job_pr_yml_license_check
    mod_automotive -->|BUILT_BY| job_pr_yml_pr_build
    mod_automotive -->|BUILT_BY| job_pr_yml_unit_tests
    mod_automotive -->|DEPLOYED_BY| job_onPush_yml_app_build
    mod_common -->|BUILT_BY| job_pr_yml_pr_build
    mod_common -->|BUILT_BY| job_pr_yml_validate_localize_setup
    mod_lint -->|BUILT_BY| job_pr_yml_ktlint
    mod_lint -->|BUILT_BY| job_pr_yml_lint
    mod_lint -->|BUILT_BY| job_pr_yml_yamllint
    mod_wear -->|BUILT_BY| job_pr_yml_license_check
    mod_wear -->|BUILT_BY| job_pr_yml_pr_build
    mod_wear -->|DEPLOYED_BY| job_onPush_yml_app_build
```

- `e2e.yml#maestro` (ci_job) --[DEPLOYS_TO]--> `ui-test` (environment)
- `pr-emulator-wtf.yml#emulator_wtf` (ci_job) --[DEPLOYS_TO]--> `ui-test` (environment)
- `app` (code_module) --[BUILT_BY]--> `e2e-triage.lock.yml#agent` (ci_job)
- `app` (code_module) --[BUILT_BY]--> `e2e-triage.lock.yml#detection` (ci_job)
- `app` (code_module) --[BUILT_BY]--> `pr-emulator-wtf.yml#check_inputs` (ci_job)
- `app` (code_module) --[BUILT_BY]--> `pr.yml#build_emulator_wtf_apks` (ci_job)
- `app` (code_module) --[BUILT_BY]--> `pr.yml#license_check` (ci_job)
- `app` (code_module) --[BUILT_BY]--> `pr.yml#pr_build` (ci_job)
- `app` (code_module) --[BUILT_BY]--> `pr.yml#unit_tests` (ci_job)
- `app` (code_module) --[DEPLOYED_BY]--> `e2e.yml#maestro` (ci_job)
- `app` (code_module) --[DEPLOYED_BY]--> `onPush.yml#app_build` (ci_job)
- `app` (code_module) --[DEPLOYED_BY]--> `pr-emulator-wtf.yml#emulator_wtf` (ci_job)
- `automotive` (code_module) --[BUILT_BY]--> `pr.yml#license_check` (ci_job)
- `automotive` (code_module) --[BUILT_BY]--> `pr.yml#pr_build` (ci_job)
- `automotive` (code_module) --[BUILT_BY]--> `pr.yml#unit_tests` (ci_job)
- `automotive` (code_module) --[DEPLOYED_BY]--> `onPush.yml#app_build` (ci_job)
- `common` (code_module) --[BUILT_BY]--> `pr.yml#pr_build` (ci_job)
- `common` (code_module) --[BUILT_BY]--> `pr.yml#validate_localize_setup` (ci_job)
- `lint` (code_module) --[BUILT_BY]--> `pr.yml#ktlint` (ci_job)
- `lint` (code_module) --[BUILT_BY]--> `pr.yml#lint` (ci_job)
- `lint` (code_module) --[BUILT_BY]--> `pr.yml#yamllint` (ci_job)
- `wear` (code_module) --[BUILT_BY]--> `pr.yml#license_check` (ci_job)
- `wear` (code_module) --[BUILT_BY]--> `pr.yml#pr_build` (ci_job)
- `wear` (code_module) --[DEPLOYED_BY]--> `onPush.yml#app_build` (ci_job)


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
  pipeline_root(["home-assistant/android (12 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Scheduled___Manual["Scheduled & Manual (6 workflows · 25 jobs)"]
    direction TB
    subgraph sg_wf_0_E2E_failure_triage["E2E failure triage (5 jobs)"]
      direction TB
      wf_0_E2E_failure_triage(["Trigger: E2E failure triage"]):::atlasWorkflow
      job_0_activation["activation"]:::atlasJob
      job_0_agent["agent"]:::atlasJob
      job_0_conclusion["conclusion"]:::atlasJob
      wf_0_E2E_failure_triage --> job_0_activation
      job_0_activation --> job_0_agent
      job_0_activation --> job_0_conclusion
      job_0_agent --> job_0_conclusion
    end
    pipeline_root --> wf_0_E2E_failure_triage
    subgraph sg_wf_1_E2E["E2E (3 jobs)"]
      direction TB
      wf_1_E2E(["Trigger: E2E"]):::atlasWorkflow
      job_1_maestro["maestro"]:::atlasJob
      job_1_triage_failure["triage-failure"]:::atlasJob
      job_1_close_failure_issue["close-failure-issue"]:::atlasJob
      wf_1_E2E --> job_1_maestro
      job_1_maestro --> job_1_triage_failure
      job_1_maestro --> job_1_close_failure_issue
    end
    pipeline_root --> wf_1_E2E
    subgraph sg_wf_3_On_Push["On Push (2 jobs)"]
      direction TB
      wf_3_On_Push(["Trigger: On Push"]):::atlasWorkflow
      job_3_app_build["app_build"]:::atlasJob
      job_3_play_publish["play_publish"]:::atlasJob
      wf_3_On_Push --> job_3_app_build
      wf_3_On_Push --> job_3_play_publish
    end
    pipeline_root --> wf_3_On_Push
    subgraph sg_wf_5_Pull_Request["Pull Request (13 jobs)"]
      direction TB
      wf_5_Pull_Request(["Trigger: Pull Request"]):::atlasWorkflow
      job_5_validate_localize_setup["validate_localize_setup"]:::atlasJob
      job_5_yamllint["yamllint"]:::atlasJob
      job_5_lockfiles["lockfiles"]:::atlasJob
      wf_5_Pull_Request --> job_5_validate_localize_setup
      wf_5_Pull_Request --> job_5_yamllint
      wf_5_Pull_Request --> job_5_lockfiles
    end
    pipeline_root --> wf_5_Pull_Request
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_6_Production_Deploy["Production Deploy (1 jobs)"]
      direction TB
      wf_6_Production_Deploy(["Trigger: Production Deploy"]):::atlasWorkflow
      job_6_play_promote_production["play_promote_production"]:::atlasJob
      wf_6_Production_Deploy --> job_6_play_promote_production
    end
    pipeline_root --> wf_6_Production_Deploy
    subgraph sg_wf_10_Tag_Weekly_Release["Tag Weekly Release (1 jobs)"]
      direction TB
      wf_10_Tag_Weekly_Release(["Trigger: Tag Weekly Release"]):::atlasWorkflow
      job_10_tag["tag"]:::atlasJob
      wf_10_Tag_Weekly_Release --> job_10_tag
    end
    pipeline_root --> wf_10_Tag_Weekly_Release
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (2 workflows · 4 jobs)"]
    direction TB
    subgraph sg_wf_7_Auto_update_Renovate_lockfiles["Auto-update Renovate lockfiles (1 jobs)"]
      direction TB
      wf_7_Auto_update_Renovate_lockfiles(["Trigger: Auto-update Renovate lockfiles"]):::atlasWorkflow
      job_7_update_lockfiles["update-lockfiles"]:::atlasJob
      wf_7_Auto_update_Renovate_lockfiles --> job_7_update_lockfiles
    end
    pipeline_root --> wf_7_Auto_update_Renovate_lockfiles
    subgraph sg_wf_11_Zizmor_GitHub_Actions_security_analysis["Zizmor GitHub Actions security analysis (3 jobs)"]
      direction TB
      wf_11_Zizmor_GitHub_Actions_security_analysis(["Trigger: Zizmor GitHub Actions security analysis"]):::atlasWorkflow
      job_11_zizmor_scan["zizmor_scan"]:::atlasJob
      job_11_upload_zizmor_reports["upload_zizmor_reports"]:::atlasJob
      wf_11_Zizmor_GitHub_Actions_security_analysis --> job_11_zizmor_scan
      job_11_zizmor_scan --> job_11_upload_zizmor_reports
    end
    pipeline_root --> wf_11_Zizmor_GitHub_Actions_security_analysis
  end
  subgraph sg_grp_3_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]
    direction TB
    wf_8_Restrict_task_creation["Restrict task creation (1 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_8_Restrict_task_creation
  end
  subgraph sg_grp_4_CI___Verification["CI & Verification (1 workflows · 3 jobs)"]
    direction TB
    wf_4_PR_Emulator_wtf["PR Emulator.wtf (3 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_4_PR_Emulator_wtf
  end
  wf_more["+2 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
