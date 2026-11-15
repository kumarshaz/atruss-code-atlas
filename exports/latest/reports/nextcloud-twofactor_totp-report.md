---
title: Architecture — nextcloud/twofactor_totp
description: Arc42 and Pipeline report for nextcloud/twofactor_totp
---

# Repository Architecture Analysis: nextcloud/twofactor_totp

## Metadata
- **SHA**: `5db86a77b183884835a7d4a66e74dabae9438074`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 9.83
- **avg_cyclomatic_complexity**: 6.22
- **component_count**: 1
- **dead_code_count**: 150
- **dead_code_symbols**: 50 entry(ies)
- **duplication_pct**: 87.02
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 111
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 2696
- **max_cognitive_complexity**: 771
- **max_cyclomatic_complexity**: 391
- **sloc**: 2282
- **test_file_count**: 23

# Architecture: nextcloud/twofactor_totp

## Context
- **Repository**: `nextcloud/twofactor_totp`
- **SHA**: `5db86a77b183884835a7d4a66e74dabae9438074`
- **Ecosystem**: JavaScript/TypeScript
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
    twofactor_totp["twofactor_totp : MODULE"]:::atlasJob
```

## Component Details
- **twofactor_totp** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (51.30/100)
- **Technical Debt Score**: 48.70
- **Estimated Remediation Effort**: 95.58h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 17.12 | 0.20 | avg_cc=6.22, max_cc=391, duplication=87.02%, dead_code=150 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1614, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 42.51 | 0.15 | avg_cognitive=9.83, max_cognitive=771, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=18, operational_antipatterns=36, parallel_branches=True |
| Security | `B` | 80.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=1 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (87.02) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (771.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (391.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1614 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `christian-riesen/base32` `1.6.0` (composer, `composer.json`)
- `rullzer/easytotp` `0.1.4` (composer, `composer.json`)
- `@chenfengyuan/vue-qrcode` `2.0.0` (npm, `package-lock.json`)
- `@chenfengyuan/vue-qrcode` `2.0.0` (npm, `package.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package.json`)
- `@nextcloud/babel-config` `1.3.0` (npm, `package-lock.json`)
- `@nextcloud/babel-config` `1.3.0` (npm, `package.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package-lock.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package.json`)
- `@nextcloud/eslint-config` `8.4.2` (npm, `package-lock.json`)
- `@nextcloud/eslint-config` `8.4.2` (npm, `package.json`)
- `@nextcloud/initial-state` `3.0.0` (npm, `package-lock.json`)
- `@nextcloud/initial-state` `3.0.0` (npm, `package.json`)
- `@nextcloud/logger` `3.0.3` (npm, `package-lock.json`)
- `@nextcloud/logger` `3.0.3` (npm, `package.json`)
- `@nextcloud/password-confirmation` `6.1.0` (npm, `package-lock.json`)
- `@nextcloud/password-confirmation` `6.1.0` (npm, `package.json`)
- `@nextcloud/router` `3.1.0` (npm, `package-lock.json`)
- `@nextcloud/router` `3.1.0` (npm, `package.json`)
- `@nextcloud/stylelint-config` `3.2.2` (npm, `package-lock.json`)
- `@nextcloud/stylelint-config` `3.2.2` (npm, `package.json`)
- `@nextcloud/webpack-vue-config` `7.0.2` (npm, `package.json`)
- `@nextcloud/webpack-vue-config` `7.0.4` (npm, `package-lock.json`)
- `@playwright/test` `1.61.1` (npm, `package-lock.json`)
- `@playwright/test` `1.61.1` (npm, `package.json`)
- `@vue/test-utils` `2.4.11` (npm, `package-lock.json`)
- `@vue/test-utils` `2.4.11` (npm, `package.json`)
- ... (+1584 more dependencies)


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
  pipeline_root(["nextcloud/twofactor_totp (18 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (11 workflows · 21 jobs)"]
    direction TB
    subgraph sg_wf_3_Lint_eslint["Lint eslint (3 jobs)"]
      direction TB
      wf_3_Lint_eslint(["Trigger: Lint eslint"]):::atlasWorkflow
      job_3_changes["changes"]:::atlasJob
      job_3_lint["lint"]:::atlasJob
      job_3_summary["summary"]:::atlasJob
      wf_3_Lint_eslint --> job_3_changes
      job_3_changes --> job_3_lint
      job_3_changes --> job_3_summary
      job_3_lint --> job_3_summary
    end
    pipeline_root --> wf_3_Lint_eslint
    subgraph sg_wf_6_Lint_php["Lint php (3 jobs)"]
      direction TB
      wf_6_Lint_php(["Trigger: Lint php"]):::atlasWorkflow
      job_6_matrix["matrix"]:::atlasJob
      job_6_php_lint["php-lint"]:::atlasJob
      job_6_summary["summary"]:::atlasJob
      wf_6_Lint_php --> job_6_matrix
      job_6_matrix --> job_6_php_lint
      job_6_php_lint --> job_6_summary
    end
    pipeline_root --> wf_6_Lint_php
    subgraph sg_wf_10_Build_Javascript["Build Javascript (3 jobs)"]
      direction TB
      wf_10_Build_Javascript(["Trigger: Build Javascript"]):::atlasWorkflow
      job_10_changes["changes"]:::atlasJob
      job_10_build["build"]:::atlasJob
      job_10_summary["summary"]:::atlasJob
      wf_10_Build_Javascript --> job_10_changes
      job_10_changes --> job_10_build
      job_10_changes --> job_10_summary
      job_10_build --> job_10_summary
    end
    pipeline_root --> wf_10_Build_Javascript
  end
  subgraph sg_grp_1_Security___Governance["Security & Governance (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_0_Block_merges_during_freezes["Block merges during freezes (1 jobs)"]
      direction TB
      wf_0_Block_merges_during_freezes(["Trigger: Block merges during freezes"]):::atlasWorkflow
      job_0_block_merges_during_freeze["block-merges-during-freeze"]:::atlasJob
      wf_0_Block_merges_during_freezes --> job_0_block_merges_during_freeze
    end
    pipeline_root --> wf_0_Block_merges_during_freezes
    subgraph sg_wf_2_Block_fixup_and_squash_commits["Block fixup and squash commits (1 jobs)"]
      direction TB
      wf_2_Block_fixup_and_squash_commits(["Trigger: Block fixup and squash commits"]):::atlasWorkflow
      job_2_commit_message_check["commit-message-check"]:::atlasJob
      wf_2_Block_fixup_and_squash_commits --> job_2_commit_message_check
    end
    pipeline_root --> wf_2_Block_fixup_and_squash_commits
    subgraph sg_wf_9_Npm_audit_fix_and_compile["Npm audit fix and compile (1 jobs)"]
      direction TB
      wf_9_Npm_audit_fix_and_compile(["Trigger: Npm audit fix and compile"]):::atlasWorkflow
      job_9_build["build"]:::atlasJob
      wf_9_Npm_audit_fix_and_compile --> job_9_build
    end
    pipeline_root --> wf_9_Npm_audit_fix_and_compile
  end
  subgraph sg_grp_2_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_12_Ask_for_feedback_on_PRs["Ask for feedback on PRs (1 jobs)"]
      direction TB
      wf_12_Ask_for_feedback_on_PRs(["Trigger: Ask for feedback on PRs"]):::atlasWorkflow
      job_12_pr_feedback["pr-feedback"]:::atlasJob
      wf_12_Ask_for_feedback_on_PRs --> job_12_pr_feedback
    end
    pipeline_root --> wf_12_Ask_for_feedback_on_PRs
    subgraph sg_wf_16_Update_workflows["Update workflows (1 jobs)"]
      direction TB
      wf_16_Update_workflows(["Trigger: Update workflows"]):::atlasWorkflow
      job_16_dispatch["dispatch"]:::atlasJob
      wf_16_Update_workflows --> job_16_dispatch
    end
    pipeline_root --> wf_16_Update_workflows
  end
  subgraph sg_grp_3_Automation___Other["Automation & Other (1 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_1_Compile_Command["Compile Command (2 jobs)"]
      direction TB
      wf_1_Compile_Command(["Trigger: Compile Command"]):::atlasWorkflow
      job_1_init["init"]:::atlasJob
      job_1_process["process"]:::atlasJob
      wf_1_Compile_Command --> job_1_init
      job_1_init --> job_1_process
    end
    pipeline_root --> wf_1_Compile_Command
  end
  subgraph sg_grp_4_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]
    direction TB
    wf_14_Notify_release_relay_on_release["Notify release-relay on release (1 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_14_Notify_release_relay_on_release
  end
  wf_more["+8 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
