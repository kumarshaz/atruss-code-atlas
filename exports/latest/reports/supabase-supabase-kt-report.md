---
title: Architecture — supabase/supabase-kt
description: Arc42 and Pipeline report for supabase/supabase-kt
---

# Repository Architecture Analysis: supabase/supabase-kt

## Metadata
- **SHA**: `4b844142f64512926377cf834e5431c7ae0ff4df`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 1.72
- **avg_cyclomatic_complexity**: 6.38
- **component_count**: 0
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 78.86
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 637
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Java Maven/Gradle
- **import_edges**: 0 entry(ies)
- **loc**: 41867
- **max_cognitive_complexity**: 106
- **max_cyclomatic_complexity**: 169
- **sloc**: 31134
- **test_file_count**: 13

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (37.60/100)
- **Technical Debt Score**: 62.40
- **Estimated Remediation Effort**: 85.37h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 36.48 | 0.20 | avg_cc=6.38, max_cc=169, duplication=78.86%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=1, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 47.00 | 0.15 | avg_cognitive=1.72, max_cognitive=106, fitness_violations=3, oversized_files=2 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=9, operational_antipatterns=18, parallel_branches=False |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=2, pipeline_security_findings=18 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (78.86) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (106.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (169.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1 | **Vulnerabilities**: 0 | **Secrets**: 2

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `Auth/src/commonTest/kotlin/AuthPasskeyApiTest.kt:169` (`...4YW1wbGUuY29tIn0=","authenticatorData":"SZYN***REDACTED***","signature":"MEQCIB..."}}"""`)
- **[HIGH] `ATRUSS-SEC-005`** at `demos/android-login/common/src/commonMain/kotlin/io/github/jan/supabase/common/di/supabaseModule.kt:18` (`supabaseKey = "eyJh***REDACTED***"`)

### Inventory Sample
- `com.google.accompanist:accompanist-webview` `0.31.1-alpha` (Maven, `demos/android-login/common/build.gradle.kts`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_integration_test["integration-test"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_dokka_yml_deploy["dokka.yml#deploy"]:::atlasJob
        job_integration_test_yml_integration_test["integration-test.yml#integration-test"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_github_pages["github-pages"]:::atlasTarget
    end
    job_dokka_yml_deploy -->|DEPLOYS_TO| env_github_pages
    mod_integration_test -->|BUILT_BY| job_integration_test_yml_integration_test
```

- `dokka.yml#deploy` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `integration-test` (code_module) --[BUILT_BY]--> `integration-test.yml#integration-test` (ci_job)


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
  pipeline_root(["supabase/supabase-kt (9 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (6 workflows · 6 jobs)"]
    direction TB
    subgraph sg_wf_0_Build_project["Build project (1 jobs)"]
      direction TB
      wf_0_Build_project(["Trigger: Build project"]):::atlasWorkflow
      job_0_build["build"]:::atlasJob
      wf_0_Build_project --> job_0_build
    end
    pipeline_root --> wf_0_Build_project
    subgraph sg_wf_2_Analyze_code_using_detekt["Analyze code using detekt (1 jobs)"]
      direction TB
      wf_2_Analyze_code_using_detekt(["Trigger: Analyze code using detekt"]):::atlasWorkflow
      job_2_analyze["analyze"]:::atlasJob
      wf_2_Analyze_code_using_detekt --> job_2_analyze
    end
    pipeline_root --> wf_2_Analyze_code_using_detekt
    subgraph sg_wf_4_Integration_Tests["Integration Tests (1 jobs)"]
      direction TB
      wf_4_Integration_Tests(["Trigger: Integration Tests"]):::atlasWorkflow
      job_4_integration_test["integration-test"]:::atlasJob
      wf_4_Integration_Tests --> job_4_integration_test
    end
    pipeline_root --> wf_4_Integration_Tests
    subgraph sg_wf_5_Pull_Request_Labeler["Pull Request Labeler (1 jobs)"]
      direction TB
      wf_5_Pull_Request_Labeler(["Trigger: Pull Request Labeler"]):::atlasWorkflow
      job_5_labeler["labeler"]:::atlasJob
      wf_5_Pull_Request_Labeler --> job_5_labeler
    end
    pipeline_root --> wf_5_Pull_Request_Labeler
    subgraph sg_wf_7_Build_samples["Build samples (1 jobs)"]
      direction TB
      wf_7_Build_samples(["Trigger: Build samples"]):::atlasWorkflow
      job_7_build["build"]:::atlasJob
      wf_7_Build_samples --> job_7_build
    end
    pipeline_root --> wf_7_Build_samples
    subgraph sg_wf_8_Test_project["Test project (1 jobs)"]
      direction TB
      wf_8_Test_project(["Trigger: Test project"]):::atlasWorkflow
      job_8_test["test"]:::atlasJob
      wf_8_Test_project --> job_8_test
    end
    pipeline_root --> wf_8_Test_project
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_3_Deploy_multi_module_dokka_to_GitHub_Pages["Deploy multi-module dokka to GitHub Pages (1 jobs)"]
      direction TB
      wf_3_Deploy_multi_module_dokka_to_GitHub_Pages(["Trigger: Deploy multi-module dokka to GitHub Pages"]):::atlasWorkflow
      job_3_deploy["deploy"]:::atlasJob
      wf_3_Deploy_multi_module_dokka_to_GitHub_Pages --> job_3_deploy
    end
    pipeline_root --> wf_3_Deploy_multi_module_dokka_to_GitHub_Pages
    subgraph sg_wf_6_Release_to_Maven_Central["Release to Maven Central (1 jobs)"]
      direction TB
      wf_6_Release_to_Maven_Central(["Trigger: Release to Maven Central"]):::atlasWorkflow
      job_6_publish["publish"]:::atlasJob
      wf_6_Release_to_Maven_Central --> job_6_publish
    end
    pipeline_root --> wf_6_Release_to_Maven_Central
  end
  subgraph sg_grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_1_Clear_all_Github_actions_caches["Clear all Github actions caches (1 jobs)"]
      direction TB
      wf_1_Clear_all_Github_actions_caches(["Trigger: Clear all Github actions caches"]):::atlasWorkflow
      job_1_clear_cache["clear-cache"]:::atlasJob
      wf_1_Clear_all_Github_actions_caches --> job_1_clear_cache
    end
    pipeline_root --> wf_1_Clear_all_Github_actions_caches
  end
```
