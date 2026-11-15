---
title: Architecture — owncloud/android
description: Arc42 and Pipeline report for owncloud/android
---

# Repository Architecture Analysis: owncloud/android

## Metadata
- **SHA**: `dc748c73c4d491107a27eb22490dafe7cde2903c`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.56
- **avg_cyclomatic_complexity**: 6.0
- **component_count**: 0
- **dead_code_count**: 2
- **dead_code_symbols**: 2 entry(ies)
- **duplication_pct**: 85.31
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 1012
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Java Maven/Gradle
- **import_edges**: 100 entry(ies)
- **loc**: 118084
- **max_cognitive_complexity**: 382
- **max_cyclomatic_complexity**: 338
- **sloc**: 77624
- **test_file_count**: 119

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (63.85/100)
- **Technical Debt Score**: 36.15
- **Estimated Remediation Effort**: 61.10h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 34.00 | 0.20 | avg_cc=6.00, max_cc=338, duplication=85.31%, dead_code=2 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=6, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=3.56, max_cognitive=382, fitness_violations=3, oversized_files=15 |
| Pipeline Health | `F` | 55.00 | 0.15 | workflows=11, operational_antipatterns=13, parallel_branches=False |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (85.31) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (382.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (338.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 6 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `com.facebook.stetho:stetho-okhttp3` `1.6.0` (Maven, `owncloudComLibrary/build.gradle`)
- `com.github.owncloud:dav4android` `oc_support_2.1.5` (Maven, `owncloudComLibrary/build.gradle`)
- `com.squareup.okhttp3:okhttp` `4.9.2` (Maven, `owncloudComLibrary/build.gradle`)
- `junit:junit` `4.13.2` (Maven, `owncloudComLibrary/build.gradle`)
- `org.apache.commons:commons-lang3` `3.20.0` (Maven, `owncloudComLibrary/build.gradle`)
- `org.robolectric:robolectric` `4.16.1` (Maven, `owncloudComLibrary/build.gradle`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_owncloudApp["owncloudApp"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_build_apk_yml_build_apk["build-apk.yml#build_apk"]:::atlasJob
        job_validate_source_strings_yml_validate_strings["validate-source-strings.yml#validate-strings"]:::atlasJob
    end
    mod_owncloudApp -->|BUILT_BY| job_build_apk_yml_build_apk
    mod_owncloudApp -->|BUILT_BY| job_validate_source_strings_yml_validate_strings
```

- `owncloudApp` (code_module) --[BUILT_BY]--> `build-apk.yml#build_apk` (ci_job)
- `owncloudApp` (code_module) --[BUILT_BY]--> `validate-source-strings.yml#validate-strings` (ci_job)


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
  pipeline_root(["owncloud/android (11 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (7 workflows · 7 jobs)"]
    direction TB
    subgraph sg_wf_0_Android_Instrumented_Data_Tests["Android Instrumented Data Tests (1 jobs)"]
      direction TB
      wf_0_Android_Instrumented_Data_Tests(["Trigger: Android Instrumented Data Tests"]):::atlasWorkflow
      job_0_instrumented_tests["instrumented-tests"]:::atlasJob
      wf_0_Android_Instrumented_Data_Tests --> job_0_instrumented_tests
    end
    pipeline_root --> wf_0_Android_Instrumented_Data_Tests
    subgraph sg_wf_1_Android_Unit_Tests["Android Unit Tests (1 jobs)"]
      direction TB
      wf_1_Android_Unit_Tests(["Trigger: Android Unit Tests"]):::atlasWorkflow
      job_1_unit_tests["unit-tests"]:::atlasJob
      wf_1_Android_Unit_Tests --> job_1_unit_tests
    end
    pipeline_root --> wf_1_Android_Unit_Tests
    subgraph sg_wf_3_Calens_Changelog["Calens Changelog (1 jobs)"]
      direction TB
      wf_3_Calens_Changelog(["Trigger: Calens Changelog"]):::atlasWorkflow
      job_3_changelog["changelog"]:::atlasJob
      wf_3_Calens_Changelog --> job_3_changelog
    end
    pipeline_root --> wf_3_Calens_Changelog
    subgraph sg_wf_4_Conventional_Commits["Conventional Commits (1 jobs)"]
      direction TB
      wf_4_Conventional_Commits(["Trigger: Conventional Commits"]):::atlasWorkflow
      job_4_validate_commit_names["validate-commit-names"]:::atlasJob
      wf_4_Conventional_Commits --> job_4_validate_commit_names
    end
    pipeline_root --> wf_4_Conventional_Commits
    subgraph sg_wf_5_Detekt["Detekt (1 jobs)"]
      direction TB
      wf_5_Detekt(["Trigger: Detekt"]):::atlasWorkflow
      job_5_Detekt["Detekt"]:::atlasJob
      wf_5_Detekt --> job_5_Detekt
    end
    pipeline_root --> wf_5_Detekt
    subgraph sg_wf_9_Validate_Android_source_strings["Validate Android source strings (1 jobs)"]
      direction TB
      wf_9_Validate_Android_source_strings(["Trigger: Validate Android source strings"]):::atlasWorkflow
      job_9_validate_strings["validate-strings"]:::atlasJob
      wf_9_Validate_Android_source_strings --> job_9_validate_strings
    end
    pipeline_root --> wf_9_Validate_Android_source_strings
  end
  subgraph sg_grp_1_Scheduled___Manual["Scheduled & Manual (4 workflows · 4 jobs)"]
    direction TB
    subgraph sg_wf_2_Build_apk["Build apk (1 jobs)"]
      direction TB
      wf_2_Build_apk(["Trigger: Build apk"]):::atlasWorkflow
      job_2_build_apk["build_apk"]:::atlasJob
      wf_2_Build_apk --> job_2_build_apk
    end
    pipeline_root --> wf_2_Build_apk
    subgraph sg_wf_7_SBOM["SBOM (1 jobs)"]
      direction TB
      wf_7_SBOM(["Trigger: SBOM"]):::atlasWorkflow
      job_7_sbom["sbom"]:::atlasJob
      wf_7_SBOM --> job_7_sbom
    end
    pipeline_root --> wf_7_SBOM
    subgraph sg_wf_8_Update_translations["Update translations (1 jobs)"]
      direction TB
      wf_8_Update_translations(["Trigger: Update translations"]):::atlasWorkflow
      job_8_update_translations["update-translations"]:::atlasJob
      wf_8_Update_translations --> job_8_update_translations
    end
    pipeline_root --> wf_8_Update_translations
    subgraph sg_wf_10_Zizmor["Zizmor (1 jobs)"]
      direction TB
      wf_10_Zizmor(["Trigger: Zizmor"]):::atlasWorkflow
      job_10_zizmor["zizmor"]:::atlasJob
      wf_10_Zizmor --> job_10_zizmor
    end
    pipeline_root --> wf_10_Zizmor
  end
  wf_more["+1 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
