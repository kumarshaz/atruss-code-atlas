---
title: Architecture — backstage/community-plugins
description: Arc42 and Pipeline report for backstage/community-plugins
---

# Repository Architecture Analysis: backstage/community-plugins

## Metadata
- **SHA**: `00f220c8fafbd53fa5f885dd9854ae8b74a51e8d`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 2.43
- **avg_cyclomatic_complexity**: 2.78
- **component_count**: 437
- **dead_code_count**: 10
- **dead_code_symbols**: 10 entry(ies)
- **duplication_pct**: 85.83
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 7391
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: React (Vite)
- **import_edges**: 100 entry(ies)
- **loc**: 746159
- **max_cognitive_complexity**: 99
- **max_cyclomatic_complexity**: 61
- **sloc**: 546599
- **test_file_count**: 1171

# Architecture: backstage/community-plugins

## Context
- **Repository**: `backstage/community-plugins`
- **SHA**: `00f220c8fafbd53fa5f885dd9854ae8b74a51e8d`
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
    repo_root(["backstage/community-plugins (437 components)"]):::atlasRoot
    dir_0_workspaces["workspaces (436)"]:::atlasCategory
    repo_root --> dir_0_workspaces
    sub_0_0_github["github (11)"]:::atlasWorkflow
    dir_0_workspaces --> sub_0_0_github
    sub_0_1_tech_insights["tech-insights (11)"]:::atlasWorkflow
    dir_0_workspaces --> sub_0_1_tech_insights
    sub_0_2_announcements["announcements (10)"]:::atlasWorkflow
    dir_0_workspaces --> sub_0_2_announcements
    sub_0_more["+109 more submodules (404)"]:::atlasMore
    dir_0_workspaces --> sub_0_more
    dir_1__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_1__root_
```

## Component Details

Showing top 60 representative components out of 437 across 2 module group(s):

- **Module `workspaces`** (436 components — MODULE: 436)
- **Module `(root)`** (1 components — MODULE: 1)

- **${{ values.name }}** (`workspaces/mend/examples/template/content/package.json`): MODULE
- **${{ values.name }}** (`workspaces/mta/examples/template/content/package.json`): MODULE
- **${{ values.name }}** (`workspaces/ocm/examples/template/content/package.json`): MODULE
- **${{ values.name }}** (`workspaces/rbac/examples/template/content/package.json`): MODULE
- **${{ values.name }}** (`workspaces/topology/examples/template/content/package.json`): MODULE
- **@backstage-community/backstage-plugin-catalog-backend-module-mta-entity-provider** (`workspaces/mta/plugins/catalog-backend-module-mta-entity-provider/package.json`): MODULE
- **@backstage-community/backstage-plugin-mta-backend** (`workspaces/mta/plugins/mta-backend/package.json`): MODULE
- **@backstage-community/backstage-plugin-mta-frontend** (`workspaces/mta/plugins/mta-frontend/package.json`): MODULE
- **@backstage-community/backstage-plugin-scaffolder-backend-module-mta** (`workspaces/mta/plugins/scaffolder-backend-module-mta/package.json`): MODULE
- **@backstage-community/cli** (`workspaces/repo-tools/packages/cli/package.json`): MODULE
- **@backstage-community/plugin-3scale-backend** (`workspaces/3scale/plugins/3scale-backend/package.json`): MODULE
- **@backstage-community/plugin-acr** (`workspaces/acr/plugins/acr/package.json`): MODULE
- **@backstage-community/plugin-acs** (`workspaces/acs/plugins/acs/package.json`): MODULE
- **@backstage-community/plugin-adr** (`workspaces/adr/plugins/adr/package.json`): MODULE
- **@backstage-community/plugin-adr-backend** (`workspaces/adr/plugins/adr-backend/package.json`): MODULE
- **@backstage-community/plugin-adr-common** (`workspaces/adr/plugins/adr-common/package.json`): MODULE
- **@backstage-community/plugin-agent-forge** (`workspaces/agent-forge/plugins/agent-forge/package.json`): MODULE
- **@backstage-community/plugin-airbrake** (`workspaces/airbrake/plugins/airbrake/package.json`): MODULE
- **@backstage-community/plugin-airbrake-backend** (`workspaces/airbrake/plugins/airbrake-backend/package.json`): MODULE
- **@backstage-community/plugin-akeyless** (`workspaces/akeyless/plugins/akeyless/package.json`): MODULE
- **@backstage-community/plugin-akeyless-backend** (`workspaces/akeyless/plugins/akeyless-backend/package.json`): MODULE
- **@backstage-community/plugin-akeyless-common** (`workspaces/akeyless/plugins/akeyless-common/package.json`): MODULE
- **@backstage-community/plugin-allure** (`workspaces/allure/plugins/allure/package.json`): MODULE
- **@backstage-community/plugin-analytics-module-ga4** (`workspaces/analytics/plugins/analytics-module-ga4/package.json`): MODULE
- **@backstage-community/plugin-analytics-module-matomo** (`workspaces/analytics/plugins/analytics-module-matomo/package.json`): MODULE
- **@backstage-community/plugin-analytics-module-newrelic-browser** (`workspaces/analytics/plugins/analytics-module-newrelic-browser/package.json`): MODULE
- **@backstage-community/plugin-analytics-provider-segment** (`workspaces/analytics/plugins/analytics-provider-segment/package.json`): MODULE
- **@backstage-community/plugin-announcements** (`workspaces/announcements/plugins/announcements/package.json`): MODULE
- **@backstage-community/plugin-announcements-backend** (`workspaces/announcements/plugins/announcements-backend/package.json`): MODULE
- **@backstage-community/plugin-announcements-common** (`workspaces/announcements/plugins/announcements-common/package.json`): MODULE
- **@backstage-community/plugin-announcements-node** (`workspaces/announcements/plugins/announcements-node/package.json`): MODULE
- **@backstage-community/plugin-announcements-react** (`workspaces/announcements/plugins/announcements-react/package.json`): MODULE
- **@backstage-community/plugin-apache-airflow** (`workspaces/apache-airflow/plugins/apache-airflow/package.json`): MODULE
- **@backstage-community/plugin-apiiro** (`workspaces/apiiro/plugins/apiiro/package.json`): MODULE
- **@backstage-community/plugin-apiiro-backend** (`workspaces/apiiro/plugins/apiiro-backend/package.json`): MODULE
- **@backstage-community/plugin-apiiro-common** (`workspaces/apiiro/plugins/apiiro-common/package.json`): MODULE
- **@backstage-community/plugin-apollo-explorer** (`workspaces/apollo-explorer/plugins/apollo-explorer/package.json`): MODULE
- **@backstage-community/plugin-argo-workflows** (`workspaces/argo-workflows/plugins/argo-workflows/package.json`): MODULE
- **@backstage-community/plugin-argo-workflows-backend** (`workspaces/argo-workflows/plugins/argo-workflows-backend/package.json`): MODULE
- **@backstage-community/plugin-argo-workflows-common** (`workspaces/argo-workflows/plugins/argo-workflows-common/package.json`): MODULE
- **@backstage-community/plugin-argo-workflows-react** (`workspaces/argo-workflows/plugins/argo-workflows-react/package.json`): MODULE
- **@backstage-community/plugin-argocd** (`workspaces/argocd/plugins/argocd/package.json`): MODULE
- **@backstage-community/plugin-argocd-backend** (`workspaces/argocd/plugins/argocd-backend/package.json`): MODULE
- **@backstage-community/plugin-argocd-common** (`workspaces/argocd/plugins/argocd-common/package.json`): MODULE
- **@backstage-community/plugin-argocd-node** (`workspaces/argocd/plugins/argocd-node/package.json`): MODULE
- **@backstage-community/plugin-auth-backend-module-keycloak-provider** (`workspaces/keycloak/plugins/auth-backend-module-keycloak-provider/package.json`): MODULE
- **@backstage-community/plugin-auth-backend-module-pingfederate-provider** (`workspaces/pingidentity/plugins/auth-backend-module-pingfederate-provider/package.json`): MODULE
- **@backstage-community/plugin-azure-devops** (`workspaces/azure-devops/plugins/azure-devops/package.json`): MODULE
- **@backstage-community/plugin-azure-devops-backend** (`workspaces/azure-devops/plugins/azure-devops-backend/package.json`): MODULE
- **@backstage-community/plugin-azure-devops-common** (`workspaces/azure-devops/plugins/azure-devops-common/package.json`): MODULE
- **@backstage-community/plugin-azure-resources-node** (`workspaces/azure-resources/plugins/azure-resources-node/package.json`): MODULE
- **@backstage-community/plugin-azure-sites** (`workspaces/azure-sites/plugins/azure-sites/package.json`): MODULE
- **@backstage-community/plugin-azure-sites-backend** (`workspaces/azure-sites/plugins/azure-sites-backend/package.json`): MODULE
- **@backstage-community/plugin-azure-sites-common** (`workspaces/azure-sites/plugins/azure-sites-common/package.json`): MODULE
- **@backstage-community/plugin-azure-storage-explorer** (`workspaces/azure-storage-explorer/plugins/azure-storage/package.json`): MODULE
- **@backstage-community/plugin-azure-storage-explorer-backend** (`workspaces/azure-storage-explorer/plugins/azure-storage-backend/package.json`): MODULE
- **@backstage-community/plugin-badges** (`workspaces/badges/plugins/badges/package.json`): MODULE
- **@backstage-community/plugin-badges-backend** (`workspaces/badges/plugins/badges-backend/package.json`): MODULE
- **@backstage-community/plugin-bazaar** (`workspaces/bazaar/plugins/bazaar/package.json`): MODULE
- **@backstage-community/plugin-bazaar-backend** (`workspaces/bazaar/plugins/bazaar-backend/package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (61.55/100)
- **Technical Debt Score**: 38.45
- **Estimated Remediation Effort**: 51.78h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.00 | 0.20 | avg_cc=2.78, max_cc=61, duplication=85.83%, dead_code=10 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=2.43, max_cognitive=99, fitness_violations=3, oversized_files=12 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (85.83) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (99.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (61.0) exceeds policy threshold (20.0).


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
  pipeline_root(["backstage/community-plugins (21 workflows)"]):::atlasRoot
  grp_0_Scheduled___Manual["Scheduled & Manual (9 workflows · 11 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_Scheduled___Manual
  wf_1_Auto_label_aged_Renovate_PRs["Auto-label aged Renovate PRs (1 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_1_Auto_label_aged_Renovate_PRs
  job_1_label_aged_prs["label-aged-prs"]:::atlasJob
  wf_1_Auto_label_aged_Renovate_PRs --> job_1_label_aged_prs
  wf_2_Auto_Version_Bump_Scheduler["Auto Version Bump Scheduler (2 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_2_Auto_Version_Bump_Scheduler
  job_2_check_and_schedule["check-and-schedule"]:::atlasJob
  job_2_trigger_auto_version_bump["trigger-auto-version-bump"]:::atlasJob
  wf_2_Auto_Version_Bump_Scheduler --> job_2_check_and_schedule
  job_2_check_and_schedule --> job_2_trigger_auto_version_bump
  wf_3_Auto_Version_Bump["Auto Version Bump (2 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_3_Auto_Version_Bump
  job_3_prepare["prepare"]:::atlasJob
  job_3_batch_dispatch["batch-dispatch"]:::atlasJob
  wf_3_Auto_Version_Bump --> job_3_prepare
  job_3_prepare --> job_3_batch_dispatch
  grp_1_CI___Verification["CI & Verification (6 workflows · 11 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_CI___Verification
  wf_0_Add_Workspace_Label_to_Issues_and_PRs["Add Workspace Label to Issues and PRs (2 jobs)"]:::atlasWorkflow
  grp_1_CI___Verification --> wf_0_Add_Workspace_Label_to_Issues_and_PRs
  job_0_triage_issues["triage-issues"]:::atlasJob
  job_0_label_prs["label-prs"]:::atlasJob
  wf_0_Add_Workspace_Label_to_Issues_and_PRs --> job_0_triage_issues
  wf_0_Add_Workspace_Label_to_Issues_and_PRs --> job_0_label_prs
  wf_7_CI["CI (4 jobs)"]:::atlasWorkflow
  grp_1_CI___Verification --> wf_7_CI
  job_7_find_changed_workspaces["find-changed-workspaces"]:::atlasJob
  job_7_ci["ci"]:::atlasJob
  job_7_verify["verify"]:::atlasJob
  wf_7_CI --> job_7_find_changed_workspaces
  job_7_find_changed_workspaces --> job_7_ci
  job_7_find_changed_workspaces --> job_7_verify
  wf_8_Coverage_Baseline["Coverage Baseline (2 jobs)"]:::atlasWorkflow
  grp_1_CI___Verification --> wf_8_Coverage_Baseline
  job_8_detect_workspaces["detect-workspaces"]:::atlasJob
  job_8_coverage["coverage"]:::atlasJob
  wf_8_Coverage_Baseline --> job_8_detect_workspaces
  job_8_detect_workspaces --> job_8_coverage
  grp_2_Release___Deploy["Release & Deploy (4 workflows · 8 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Release___Deploy
  wf_14_Release_all_workspaces["Release all workspaces (2 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_14_Release_all_workspaces
  job_14_find_changed_workspaces["find-changed-workspaces"]:::atlasJob
  job_14_maybe_release_workspace["maybe-release-workspace"]:::atlasJob
  wf_14_Release_all_workspaces --> job_14_find_changed_workspaces
  job_14_find_changed_workspaces --> job_14_maybe_release_workspace
  wf_16_Prior_Version_Release_Workspace["Prior Version Release Workspace (3 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_16_Prior_Version_Release_Workspace
  job_16_check_merged_pr["check-merged-pr"]:::atlasJob
  job_16_changesets_pr["changesets-pr"]:::atlasJob
  wf_16_Prior_Version_Release_Workspace --> job_16_check_merged_pr
  job_16_check_merged_pr --> job_16_changesets_pr
  grp_3_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_3_Security___Governance
  wf_4_Automate_staleness["Automate staleness (1 jobs)"]:::atlasWorkflow
  grp_3_Security___Governance --> wf_4_Automate_staleness
  wf_6_Automate_Renovate_and_Dependabot_changeset["Automate Renovate and Dependabot changeset (1 jobs)"]:::atlasWorkflow
  grp_3_Security___Governance --> wf_6_Automate_Renovate_and_Dependabot_changeset
  wf_more["+11 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
