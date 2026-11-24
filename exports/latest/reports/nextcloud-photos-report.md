---
title: Architecture — nextcloud/photos
description: Arc42 and Pipeline report for nextcloud/photos
---

# Repository Architecture Analysis: nextcloud/photos

## Metadata
- **SHA**: `fb6721820486169409559d14df300167e51010c9`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 12.29
- **avg_cyclomatic_complexity**: 4.04
- **component_count**: 1
- **dead_code_count**: 723
- **dead_code_symbols**: 27 entry(ies)
- **duplication_pct**: 83.8
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 506
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: React (Vite)
- **import_edges**: 100 entry(ies)
- **loc**: 30501
- **max_cognitive_complexity**: 49778
- **max_cyclomatic_complexity**: 1363
- **sloc**: 23240
- **test_file_count**: 149

# Architecture: nextcloud/photos

## Context
- **Repository**: `nextcloud/photos`
- **SHA**: `fb6721820486169409559d14df300167e51010c9`
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
    photos["photos : MODULE"]:::atlasJob
```

## Component Details
- **photos** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (35.94/100)
- **Technical Debt Score**: 64.06
- **Estimated Remediation Effort**: 255.52h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 25.84 | 0.20 | avg_cc=4.04, max_cc=1363, duplication=83.80%, dead_code=723 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1415, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 35.13 | 0.15 | avg_cognitive=12.29, max_cognitive=49778, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=26, operational_antipatterns=50, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=5 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (83.8) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (49778.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (1363.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1415 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `hexogen/kdtree` `0.2.5` (composer, `composer.json`)
- `woltlab/webp-exif` `0.1.5` (composer, `composer.json`)
- `@essentials/request-timeout` `1.3.0` (npm, `package-lock.json`)
- `@essentials/request-timeout` `1.3.0` (npm, `package.json`)
- `@mdi/svg` `7.4.47` (npm, `package-lock.json`)
- `@mdi/svg` `7.4.47` (npm, `package.json`)
- `@nextcloud/auth` `2.1.0` (npm, `package.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/axios` `2.1.0` (npm, `package.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/babel-config` `1.3.0` (npm, `package-lock.json`)
- `@nextcloud/babel-config` `1.3.0` (npm, `package.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package-lock.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package.json`)
- `@nextcloud/dialogs` `7.5.0` (npm, `package.json`)
- `@nextcloud/dialogs` `7.6.0` (npm, `package-lock.json`)
- `@nextcloud/e2e-test-server` `0.6.0` (npm, `package-lock.json`)
- `@nextcloud/e2e-test-server` `0.6.0` (npm, `package.json`)
- `@nextcloud/eslint-config` `9.0.1` (npm, `package-lock.json`)
- `@nextcloud/eslint-config` `9.0.1` (npm, `package.json`)
- `@nextcloud/event-bus` `3.1.0` (npm, `package.json`)
- `@nextcloud/event-bus` `3.3.3` (npm, `package-lock.json`)
- `@nextcloud/files` `4.1.0-beta.2` (npm, `package.json`)
- `@nextcloud/files` `4.1.1` (npm, `package-lock.json`)
- `@nextcloud/initial-state` `3.0.0` (npm, `package-lock.json`)
- `@nextcloud/initial-state` `3.0.0` (npm, `package.json`)
- `@nextcloud/l10n` `3.4.1` (npm, `package-lock.json`)
- `@nextcloud/l10n` `3.4.1` (npm, `package.json`)
- `@nextcloud/logger` `3.0.2` (npm, `package.json`)
- `@nextcloud/logger` `3.0.3` (npm, `package-lock.json`)
- ... (+1385 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_tests_playwright["tests/playwright"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_playwright_yml_merge_reports["playwright.yml#merge-reports"]:::atlasJob
    end
    mod_tests_playwright -->|BUILT_BY| job_playwright_yml_merge_reports
```

- `tests/playwright` (code_module) --[BUILT_BY]--> `playwright.yml#merge-reports` (ci_job)


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
  pipeline_root(["nextcloud/photos (26 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (15 workflows · 34 jobs)"]
    direction TB
    subgraph sg_wf_6_Lint_eslint["Lint eslint (3 jobs)"]
      direction TB
      wf_6_Lint_eslint(["Trigger: Lint eslint"]):::atlasWorkflow
      job_6_changes["changes"]:::atlasJob
      job_6_lint["lint"]:::atlasJob
      job_6_summary["summary"]:::atlasJob
      wf_6_Lint_eslint --> job_6_changes
      job_6_changes --> job_6_lint
      job_6_changes --> job_6_summary
      job_6_lint --> job_6_summary
    end
    pipeline_root --> wf_6_Lint_eslint
    subgraph sg_wf_13_Build_Javascript["Build Javascript (3 jobs)"]
      direction TB
      wf_13_Build_Javascript(["Trigger: Build Javascript"]):::atlasWorkflow
      job_13_changes["changes"]:::atlasJob
      job_13_build["build"]:::atlasJob
      job_13_summary["summary"]:::atlasJob
      wf_13_Build_Javascript --> job_13_changes
      job_13_changes --> job_13_build
      job_13_changes --> job_13_summary
      job_13_build --> job_13_summary
    end
    pipeline_root --> wf_13_Build_Javascript
    subgraph sg_wf_18_Playwright_Tests["Playwright Tests (4 jobs)"]
      direction TB
      wf_18_Playwright_Tests(["Trigger: Playwright Tests"]):::atlasWorkflow
      job_18_playwright_setup["playwright-setup"]:::atlasJob
      job_18_playwright_tests["playwright-tests"]:::atlasJob
      job_18_merge_reports["merge-reports"]:::atlasJob
      wf_18_Playwright_Tests --> job_18_playwright_setup
      job_18_playwright_setup --> job_18_playwright_tests
      job_18_playwright_tests --> job_18_merge_reports
    end
    pipeline_root --> wf_18_Playwright_Tests
  end
  subgraph sg_grp_1_Security___Governance["Security & Governance (6 workflows · 6 jobs)"]
    direction TB
    subgraph sg_wf_1_Block_merges_during_freezes["Block merges during freezes (1 jobs)"]
      direction TB
      wf_1_Block_merges_during_freezes(["Trigger: Block merges during freezes"]):::atlasWorkflow
      job_1_block_merges_during_freeze["block-merges-during-freeze"]:::atlasJob
      wf_1_Block_merges_during_freezes --> job_1_block_merges_during_freeze
    end
    pipeline_root --> wf_1_Block_merges_during_freezes
    subgraph sg_wf_4_Auto_approve_Dependabot_PRs["Auto approve Dependabot PRs (1 jobs)"]
      direction TB
      wf_4_Auto_approve_Dependabot_PRs(["Trigger: Auto approve Dependabot PRs"]):::atlasWorkflow
      job_4_auto_approve_merge["auto-approve-merge"]:::atlasJob
      wf_4_Auto_approve_Dependabot_PRs --> job_4_auto_approve_merge
    end
    pipeline_root --> wf_4_Auto_approve_Dependabot_PRs
    subgraph sg_wf_5_Block_fixup_and_squash_commits["Block fixup and squash commits (1 jobs)"]
      direction TB
      wf_5_Block_fixup_and_squash_commits(["Trigger: Block fixup and squash commits"]):::atlasWorkflow
      job_5_commit_message_check["commit-message-check"]:::atlasJob
      wf_5_Block_fixup_and_squash_commits --> job_5_commit_message_check
    end
    pipeline_root --> wf_5_Block_fixup_and_squash_commits
  end
  subgraph sg_grp_2_Scheduled___Manual["Scheduled & Manual (4 workflows · 4 jobs)"]
    direction TB
    subgraph sg_wf_19_Ask_for_feedback_on_PRs["Ask for feedback on PRs (1 jobs)"]
      direction TB
      wf_19_Ask_for_feedback_on_PRs(["Trigger: Ask for feedback on PRs"]):::atlasWorkflow
      job_19_pr_feedback["pr-feedback"]:::atlasJob
      wf_19_Ask_for_feedback_on_PRs --> job_19_pr_feedback
    end
    pipeline_root --> wf_19_Ask_for_feedback_on_PRs
    subgraph sg_wf_21_Apply_rector_changes["Apply rector changes (1 jobs)"]
      direction TB
      wf_21_Apply_rector_changes(["Trigger: Apply rector changes"]):::atlasWorkflow
      job_21_build["build"]:::atlasJob
      wf_21_Apply_rector_changes --> job_21_build
    end
    pipeline_root --> wf_21_Apply_rector_changes
    subgraph sg_wf_24_Update_nextcloud_ocp["Update nextcloud/ocp (1 jobs)"]
      direction TB
      wf_24_Update_nextcloud_ocp(["Trigger: Update nextcloud/ocp"]):::atlasWorkflow
      job_24_update_nextcloud_ocp["update-nextcloud-ocp"]:::atlasJob
      wf_24_Update_nextcloud_ocp --> job_24_update_nextcloud_ocp
    end
    pipeline_root --> wf_24_Update_nextcloud_ocp
  end
  subgraph sg_grp_3_Automation___Other["Automation & Other (1 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_3_Compile_Command["Compile Command (2 jobs)"]
      direction TB
      wf_3_Compile_Command(["Trigger: Compile Command"]):::atlasWorkflow
      job_3_init["init"]:::atlasJob
      wf_3_Compile_Command --> job_3_init
    end
    pipeline_root --> wf_3_Compile_Command
  end
  wf_more["+16 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
