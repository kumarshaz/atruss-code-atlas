---
title: Architecture — nextcloud/files_mindmap
description: Arc42 and Pipeline report for nextcloud/files_mindmap
---

# Repository Architecture Analysis: nextcloud/files_mindmap

## Metadata
- **SHA**: `46625e243af396fe29a2f99d618fbc121474804c`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.76
- **avg_cyclomatic_complexity**: 2.17
- **component_count**: 1
- **dead_code_count**: 9
- **dead_code_symbols**: 9 entry(ies)
- **duplication_pct**: 76.83
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 106
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: React (Vite)
- **import_edges**: 100 entry(ies)
- **loc**: 5431
- **max_cognitive_complexity**: 51
- **max_cyclomatic_complexity**: 27
- **sloc**: 4934
- **test_file_count**: 9

# Architecture: nextcloud/files_mindmap

## Context
- **Repository**: `nextcloud/files_mindmap`
- **SHA**: `46625e243af396fe29a2f99d618fbc121474804c`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: React (Vite)

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
    files_mindmap["files_mindmap : MODULE"]:::atlasJob
```

## Component Details
- **files_mindmap** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (47.05/100)
- **Technical Debt Score**: 52.95
- **Estimated Remediation Effort**: 56.85h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 39.00 | 0.20 | avg_cc=2.17, max_cc=27, duplication=76.83%, dead_code=9 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1222, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 57.00 | 0.15 | avg_cognitive=1.76, max_cognitive=51, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `F` | 8.00 | 0.15 | workflows=7, operational_antipatterns=17, parallel_branches=True |
| Security | `F` | 20.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=4 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (76.83) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (51.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (27.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1222 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@babel/core` `7.3.3` (npm, `vendor/jquery/package.json`)
- `@babel/plugin-transform-for-of` `7.2.0` (npm, `vendor/jquery/package.json`)
- `@markedjs/html-differ` `2.0.0` (npm, `vendor/marked/package-lock.json`)
- `@markedjs/html-differ` `2.0.0` (npm, `vendor/marked/package.json`)
- `@nextcloud/auth` `2.5.0` (npm, `package.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/axios` `2.4.0` (npm, `package.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/browserslist-config` `3.0.0` (npm, `package.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package-lock.json`)
- `@nextcloud/dialogs` `7.5.0` (npm, `package.json`)
- `@nextcloud/dialogs` `7.6.0` (npm, `package-lock.json`)
- `@nextcloud/eslint-config` `9.0.1` (npm, `package-lock.json`)
- `@nextcloud/eslint-config` `9.0.1` (npm, `package.json`)
- `@nextcloud/event-bus` `3.1.0` (npm, `package.json`)
- `@nextcloud/event-bus` `3.3.3` (npm, `package-lock.json`)
- `@nextcloud/files` `4.1.1` (npm, `package-lock.json`)
- `@nextcloud/files` `4.1.1` (npm, `package.json`)
- `@nextcloud/l10n` `3.0.0` (npm, `package.json`)
- `@nextcloud/l10n` `3.4.1` (npm, `package-lock.json`)
- `@nextcloud/logger` `3.0.0` (npm, `package.json`)
- `@nextcloud/logger` `3.0.3` (npm, `package-lock.json`)
- `@nextcloud/paths` `3.1.0` (npm, `package-lock.json`)
- `@nextcloud/paths` `3.1.0` (npm, `package.json`)
- `@nextcloud/router` `3.2.0` (npm, `package-lock.json`)
- `@nextcloud/router` `3.2.0` (npm, `package.json`)
- `@nextcloud/sharing` `0.4.0` (npm, `package-lock.json`)
- `@nextcloud/sharing` `0.4.0` (npm, `package.json`)
- `@nextcloud/viewer` `2.0.0-beta.20` (npm, `package.json`)
- `@nextcloud/viewer` `2.0.0-beta.21` (npm, `package-lock.json`)
- ... (+1192 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_78312536_d854_443a_a6ca_c44ef2d834c1["78312536-d854-443a-a6ca-c44ef2d834c1"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_ai_policy_yml_check_ai_trailers["ai-policy.yml#check-ai-trailers"]:::atlasJob
        job_appstore_build_publish_yml_build_and_publish["appstore-build-publish.yml#build_and_publish"]:::atlasJob
        job_lint_eslint_yml_changes["lint-eslint.yml#changes"]:::atlasJob
        job_lint_eslint_yml_lint["lint-eslint.yml#lint"]:::atlasJob
        job_lint_eslint_yml_summary["lint-eslint.yml#summary"]:::atlasJob
        job_node_test_yml_changes["node-test.yml#changes"]:::atlasJob
        job_node_test_yml_summary["node-test.yml#summary"]:::atlasJob
        job_node_test_yml_test["node-test.yml#test"]:::atlasJob
        job_npm_audit_fix_yml_build["npm-audit-fix.yml#build"]:::atlasJob
        job_pr_feedback_yml_pr_feedback["pr-feedback.yml#pr-feedback"]:::atlasJob
        job_release_relay_yml_notify["release-relay.yml#notify"]:::atlasJob
    end
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_ai_policy_yml_check_ai_trailers
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_lint_eslint_yml_changes
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_lint_eslint_yml_lint
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_lint_eslint_yml_summary
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_node_test_yml_changes
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_node_test_yml_summary
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_node_test_yml_test
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_npm_audit_fix_yml_build
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|BUILT_BY| job_pr_feedback_yml_pr_feedback
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|DEPLOYED_BY| job_appstore_build_publish_yml_build_and_publish
    mod_78312536_d854_443a_a6ca_c44ef2d834c1 -->|DEPLOYED_BY| job_release_relay_yml_notify
```

- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `ai-policy.yml#check-ai-trailers` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `lint-eslint.yml#changes` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `lint-eslint.yml#lint` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `lint-eslint.yml#summary` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `node-test.yml#changes` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `node-test.yml#summary` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `node-test.yml#test` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `npm-audit-fix.yml#build` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[BUILT_BY]--> `pr-feedback.yml#pr-feedback` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[DEPLOYED_BY]--> `appstore-build-publish.yml#build_and_publish` (ci_job)
- `78312536-d854-443a-a6ca-c44ef2d834c1` (code_module) --[DEPLOYED_BY]--> `release-relay.yml#notify` (ci_job)


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
  pipeline_root(["nextcloud/files_mindmap (7 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (3 workflows · 7 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_0_AI_Policy["AI Policy (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_0_AI_Policy
  job_0_check_ai_trailers["check-ai-trailers"]:::atlasJob
  wf_0_AI_Policy --> job_0_check_ai_trailers
  wf_2_Lint_eslint["Lint eslint (3 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_2_Lint_eslint
  job_2_changes["changes"]:::atlasJob
  job_2_lint["lint"]:::atlasJob
  job_2_summary["summary"]:::atlasJob
  wf_2_Lint_eslint --> job_2_changes
  job_2_changes --> job_2_lint
  job_2_changes --> job_2_summary
  job_2_lint --> job_2_summary
  wf_3_Node_tests["Node tests (3 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_3_Node_tests
  job_3_changes["changes"]:::atlasJob
  job_3_test["test"]:::atlasJob
  job_3_summary["summary"]:::atlasJob
  wf_3_Node_tests --> job_3_changes
  job_3_changes --> job_3_test
  job_3_changes --> job_3_summary
  job_3_test --> job_3_summary
  grp_1_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Release___Deploy
  wf_1_Build_and_publish_app_release["Build and publish app release (1 jobs)"]:::atlasWorkflow
  grp_1_Release___Deploy --> wf_1_Build_and_publish_app_release
  job_1_build_and_publish["build_and_publish"]:::atlasJob
  wf_1_Build_and_publish_app_release --> job_1_build_and_publish
  wf_6_Notify_release_relay_on_release["Notify release-relay on release (1 jobs)"]:::atlasWorkflow
  grp_1_Release___Deploy --> wf_6_Notify_release_relay_on_release
  job_6_notify["notify"]:::atlasJob
  wf_6_Notify_release_relay_on_release --> job_6_notify
  grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Scheduled___Manual
  wf_5_Ask_for_feedback_on_PRs["Ask for feedback on PRs (1 jobs)"]:::atlasWorkflow
  grp_2_Scheduled___Manual --> wf_5_Ask_for_feedback_on_PRs
  job_5_pr_feedback["pr-feedback"]:::atlasJob
  wf_5_Ask_for_feedback_on_PRs --> job_5_pr_feedback
  grp_3_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_3_Security___Governance
  wf_4_Npm_audit_fix_and_compile["Npm audit fix and compile (1 jobs)"]:::atlasWorkflow
  grp_3_Security___Governance --> wf_4_Npm_audit_fix_and_compile
  job_4_build["build"]:::atlasJob
  wf_4_Npm_audit_fix_and_compile --> job_4_build
```
