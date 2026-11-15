---
title: Architecture — nextcloud/richdocuments
description: Arc42 and Pipeline report for nextcloud/richdocuments
---

# Repository Architecture Analysis: nextcloud/richdocuments

## Metadata
- **SHA**: `4e8b9888284103007f1021dfbb3e84070f674122`
- **Primary Ecosystem**: PHP

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 179
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 179
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: PHP Composer
- **import_edges**: 0 entry(ies)
- **loc**: 20512
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 14397
- **test_file_count**: 68

# Architecture: nextcloud/richdocuments

## Context
- **Repository**: `nextcloud/richdocuments`
- **SHA**: `4e8b9888284103007f1021dfbb3e84070f674122`
- **Ecosystem**: PHP
- **Framework**: PHP Composer

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
    repo_root(["nextcloud/richdocuments (179 components)"]):::atlasRoot
    subgraph sg_dir_0_lib["lib (131)"]
      direction TB
      dir_0_lib["lib (131)"]:::atlasCategory
      sub_0_0_Service["Service (22)"]:::atlasWorkflow
      dir_0_lib --> sub_0_0_Service
      sub_0_1_Listener["Listener (16)"]:::atlasWorkflow
      dir_0_lib --> sub_0_1_Listener
      sub_0_2_Controller["Controller (14)"]:::atlasWorkflow
      dir_0_lib --> sub_0_2_Controller
      sub_0_more["+21 more submodules (79)"]:::atlasMore
      dir_0_lib --> sub_0_more
    end
    repo_root --> dir_0_lib
    subgraph sg_dir_1_tests["tests (41)"]
      direction TB
      dir_1_tests["tests (41)"]:::atlasCategory
      sub_1_0_lib["lib (33)"]:::atlasWorkflow
      dir_1_tests --> sub_1_0_lib
      sub_1_1_features["features (6)"]:::atlasWorkflow
      dir_1_tests --> sub_1_1_features
      sub_1_2__module_root_["(module root) (1)"]:::atlasWorkflow
      dir_1_tests --> sub_1_2__module_root_
      sub_1_more["+1 more submodules (1)"]:::atlasMore
      dir_1_tests --> sub_1_more
    end
    repo_root --> dir_1_tests
    dir_2_templates["templates (3)"]:::atlasCategory
    repo_root --> dir_2_templates
    dir_3__root_["(root) (2)"]:::atlasCategory
    repo_root --> dir_3__root_
    dir_4_appinfo["appinfo (1)"]:::atlasCategory
    repo_root --> dir_4_appinfo
    dir_other_modules["+1 more modules (1)"]:::atlasMore
    repo_root --> dir_other_modules
```

## Component Details

Showing top 60 representative components out of 179 across 6 module group(s):

- **Module `lib`** (131 components — module: 131)
- **Module `tests`** (41 components — module: 41)
- **Module `templates`** (3 components — module: 3)
- **Module `(root)`** (2 components — module: 2)
- **Module `appinfo`** (1 components — module: 1)
- **Module `composer`** (1 components — module: 1)

- **.php-cs-fixer.dist** (`.php-cs-fixer.dist.php`): module
- **AbstractOfficeCreator** (`lib/DirectEditing/AbstractOfficeCreator.php`): module
- **ActivateConfig** (`lib/Command/ActivateConfig.php`): module
- **AddContentSecurityPolicyListener** (`lib/Listener/AddContentSecurityPolicyListener.php`): module
- **AddContentSecurityPolicyListenerTest** (`tests/lib/Listener/AddContentSecurityPolicyListenerTest.php`): module
- **AddFeaturePolicyListener** (`lib/Listener/AddFeaturePolicyListener.php`): module
- **AddFeaturePolicyListenerTest** (`tests/OCA/Richdocuments/Listener/AddFeaturePolicyListenerTest.php`): module
- **AddMissingIndicesListener** (`lib/Listener/AddMissingIndicesListener.php`): module
- **AddSabrePluginListener** (`lib/Listener/AddSabrePluginListener.php`): module
- **Admin** (`lib/Settings/Admin.php`): module
- **AdminTest** (`tests/lib/Settings/AdminTest.php`): module
- **ApiContext** (`tests/features/bootstrap/ApiContext.php`): module
- **AppConfig** (`lib/AppConfig.php`): module
- **AppConfigTest** (`tests/lib/AppConfigTest.php`): module
- **Application** (`lib/AppInfo/Application.php`): module
- **Asset** (`lib/Db/Asset.php`): module
- **AssetMapper** (`lib/Db/AssetMapper.php`): module
- **AssetsController** (`lib/Controller/AssetsController.php`): module
- **BeforeFederationRedirectEvent** (`lib/Events/BeforeFederationRedirectEvent.php`): module
- **BeforeFetchPreviewListener** (`lib/Listener/BeforeFetchPreviewListener.php`): module
- **BeforeGetTemplatesListener** (`lib/Listener/BeforeGetTemplatesListener.php`): module
- **BeforeTemplateRenderedListener** (`lib/Listener/BeforeTemplateRenderedListener.php`): module
- **CachedRequestService** (`lib/Service/CachedRequestService.php`): module
- **CachedRequestServiceTest** (`tests/lib/Service/CachedRequestServiceTest.php`): module
- **Capabilities** (`lib/Capabilities.php`): module
- **CapabilitiesService** (`lib/Service/CapabilitiesService.php`): module
- **CapabilitiesServiceTest** (`tests/lib/Service/CapabilitiesServiceTest.php`): module
- **Cleanup** (`lib/Backgroundjobs/Cleanup.php`): module
- **CollaboraTemplateProvider** (`lib/Template/CollaboraTemplateProvider.php`): module
- **CollaboraUpdate** (`lib/SetupCheck/CollaboraUpdate.php`): module
- **CollaboraUpdateTest** (`tests/lib/SetupCheck/CollaboraUpdateTest.php`): module
- **ConnectivityCheck** (`lib/SetupCheck/ConnectivityCheck.php`): module
- **ConnectivityCheckTest** (`tests/lib/SetupCheck/ConnectivityCheckTest.php`): module
- **ConnectivityService** (`lib/Service/ConnectivityService.php`): module
- **ConnectivityServiceTest** (`tests/lib/Service/ConnectivityServiceTest.php`): module
- **ConversionProvider** (`lib/Conversion/ConversionProvider.php`): module
- **ConversionProviderTest** (`tests/lib/Conversion/ConversionProviderTest.php`): module
- **ConvertToBigInt** (`lib/Command/ConvertToBigInt.php`): module
- **CreateDocument** (`lib/DirectEditing/CreateDocument.php`): module
- **CreateDrawing** (`lib/DirectEditing/CreateDrawing.php`): module
- **CreatePresentation** (`lib/DirectEditing/CreatePresentation.php`): module
- **CreateSpreadsheet** (`lib/DirectEditing/CreateSpreadsheet.php`): module
- **DemoService** (`lib/Service/DemoService.php`): module
- **Direct** (`lib/Db/Direct.php`): module
- **DirectContext** (`tests/features/bootstrap/DirectContext.php`): module
- **DirectEditingViewService** (`lib/Service/DirectEditingViewService.php`): module
- **DirectMapper** (`lib/Db/DirectMapper.php`): module
- **DirectViewController** (`lib/Controller/DirectViewController.php`): module
- **DiscoveryService** (`lib/Service/DiscoveryService.php`): module
- **DiscoveryServiceTest** (`tests/lib/Service/DiscoveryServiceTest.php`): module
- **DocumentAPIController** (`lib/Controller/DocumentAPIController.php`): module
- **DocumentController** (`lib/Controller/DocumentController.php`): module
- **DocumentControllerTest** (`tests/lib/Controller/DocumentControllerTest.php`): module
- **DocumentGenerationService** (`lib/Service/DocumentGenerationService.php`): module
- **DocumentOpenedEvent** (`lib/Events/DocumentOpenedEvent.php`): module
- **DocumentTrait** (`lib/Controller/DocumentTrait.php`): module
- **EMF** (`lib/Preview/EMF.php`): module
- **ExpiredTokenException** (`lib/Exceptions/ExpiredTokenException.php`): module
- **FederationContext** (`tests/features/bootstrap/FederationContext.php`): module
- **FederationController** (`lib/Controller/FederationController.php`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (60.50/100)
- **Technical Debt Score**: 39.50
- **Estimated Remediation Effort**: 56.38h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1494, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=22, operational_antipatterns=46, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=9 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1494 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `league/commonmark` `2.10` (composer, `composer.json`)
- `mikehaertl/php-pdftk` `0.14.4` (composer, `composer.json`)
- `phpseclib/phpseclib` `4.0` (composer, `composer.json`)
- `@cypress/webpack-batteries-included-preprocessor` `5.0.0` (npm, `package-lock.json`)
- `@cypress/webpack-batteries-included-preprocessor` `5.0.0` (npm, `package.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package.json`)
- `@nextcloud/babel-config` `1.3.0` (npm, `package-lock.json`)
- `@nextcloud/babel-config` `1.3.0` (npm, `package.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package-lock.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package.json`)
- `@nextcloud/capabilities` `1.2.1` (npm, `package-lock.json`)
- `@nextcloud/capabilities` `1.2.1` (npm, `package.json`)
- `@nextcloud/dialogs` `7.5.0` (npm, `package-lock.json`)
- `@nextcloud/dialogs` `7.5.0` (npm, `package.json`)
- `@nextcloud/e2e-test-server` `0.6.1` (npm, `package-lock.json`)
- `@nextcloud/e2e-test-server` `0.6.1` (npm, `package.json`)
- `@nextcloud/eslint-config` `9.0.1` (npm, `package-lock.json`)
- `@nextcloud/eslint-config` `9.0.1` (npm, `package.json`)
- `@nextcloud/event-bus` `3.3.3` (npm, `package-lock.json`)
- `@nextcloud/event-bus` `3.3.3` (npm, `package.json`)
- `@nextcloud/files` `4.1.1` (npm, `package-lock.json`)
- `@nextcloud/files` `4.1.1` (npm, `package.json`)
- `@nextcloud/initial-state` `3.0.0` (npm, `package-lock.json`)
- `@nextcloud/initial-state` `3.0.0` (npm, `package.json`)
- `@nextcloud/l10n` `3.4.1` (npm, `package-lock.json`)
- `@nextcloud/l10n` `3.4.1` (npm, `package.json`)
- `@nextcloud/paths` `3.1.0` (npm, `package-lock.json`)
- ... (+1464 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_tests["tests"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_integration_yml_mysql["integration.yml#mysql"]:::atlasJob
        job_integration_yml_oci["integration.yml#oci"]:::atlasJob
        job_integration_yml_pgsql["integration.yml#pgsql"]:::atlasJob
        job_integration_yml_sqlite["integration.yml#sqlite"]:::atlasJob
        job_phpunit_mysql_yml_phpunit_mysql["phpunit-mysql.yml#phpunit-mysql"]:::atlasJob
        job_phpunit_oci_yml_phpunit_oci["phpunit-oci.yml#phpunit-oci"]:::atlasJob
        job_phpunit_pgsql_yml_phpunit_pgsql["phpunit-pgsql.yml#phpunit-pgsql"]:::atlasJob
        job_phpunit_sqlite_yml_phpunit_sqlite["phpunit-sqlite.yml#phpunit-sqlite"]:::atlasJob
    end
    mod_tests -->|BUILT_BY| job_integration_yml_mysql
    mod_tests -->|BUILT_BY| job_integration_yml_oci
    mod_tests -->|BUILT_BY| job_integration_yml_pgsql
    mod_tests -->|BUILT_BY| job_integration_yml_sqlite
    mod_tests -->|BUILT_BY| job_phpunit_mysql_yml_phpunit_mysql
    mod_tests -->|BUILT_BY| job_phpunit_oci_yml_phpunit_oci
    mod_tests -->|BUILT_BY| job_phpunit_pgsql_yml_phpunit_pgsql
    mod_tests -->|BUILT_BY| job_phpunit_sqlite_yml_phpunit_sqlite
```

- `tests` (code_module) --[BUILT_BY]--> `integration.yml#mysql` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `integration.yml#oci` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `integration.yml#pgsql` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `integration.yml#sqlite` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `phpunit-mysql.yml#phpunit-mysql` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `phpunit-oci.yml#phpunit-oci` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `phpunit-pgsql.yml#phpunit-pgsql` (ci_job)
- `tests` (code_module) --[BUILT_BY]--> `phpunit-sqlite.yml#phpunit-sqlite` (ci_job)


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
  pipeline_root(["nextcloud/richdocuments (22 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (14 workflows · 32 jobs)"]
    direction TB
    subgraph sg_wf_4_WOPI_Integration_tests["WOPI Integration tests (6 jobs)"]
      direction TB
      wf_4_WOPI_Integration_tests(["Trigger: WOPI Integration tests"]):::atlasWorkflow
      job_4_changes["changes"]:::atlasJob
      job_4_sqlite["sqlite"]:::atlasJob
      job_4_mysql["mysql"]:::atlasJob
      wf_4_WOPI_Integration_tests --> job_4_changes
      job_4_changes --> job_4_sqlite
      job_4_changes --> job_4_mysql
    end
    pipeline_root --> wf_4_WOPI_Integration_tests
    subgraph sg_wf_5_Lint_eslint["Lint eslint (3 jobs)"]
      direction TB
      wf_5_Lint_eslint(["Trigger: Lint eslint"]):::atlasWorkflow
      job_5_changes["changes"]:::atlasJob
      job_5_lint["lint"]:::atlasJob
      job_5_summary["summary"]:::atlasJob
      wf_5_Lint_eslint --> job_5_changes
      job_5_changes --> job_5_lint
      job_5_changes --> job_5_summary
      job_5_lint --> job_5_summary
    end
    pipeline_root --> wf_5_Lint_eslint
    subgraph sg_wf_8_Lint_php["Lint php (3 jobs)"]
      direction TB
      wf_8_Lint_php(["Trigger: Lint php"]):::atlasWorkflow
      job_8_matrix["matrix"]:::atlasJob
      job_8_php_lint["php-lint"]:::atlasJob
      job_8_summary["summary"]:::atlasJob
      wf_8_Lint_php --> job_8_matrix
      job_8_matrix --> job_8_php_lint
      job_8_php_lint --> job_8_summary
    end
    pipeline_root --> wf_8_Lint_php
  end
  subgraph sg_grp_1_Scheduled___Manual["Scheduled & Manual (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_16_Ask_for_feedback_on_PRs["Ask for feedback on PRs (1 jobs)"]
      direction TB
      wf_16_Ask_for_feedback_on_PRs(["Trigger: Ask for feedback on PRs"]):::atlasWorkflow
      job_16_pr_feedback["pr-feedback"]:::atlasJob
      wf_16_Ask_for_feedback_on_PRs --> job_16_pr_feedback
    end
    pipeline_root --> wf_16_Ask_for_feedback_on_PRs
    subgraph sg_wf_20_Update_workflows["Update workflows (1 jobs)"]
      direction TB
      wf_20_Update_workflows(["Trigger: Update workflows"]):::atlasWorkflow
      job_20_dispatch["dispatch"]:::atlasJob
      wf_20_Update_workflows --> job_20_dispatch
    end
    pipeline_root --> wf_20_Update_workflows
    subgraph sg_wf_21_Update_nextcloud_ocp["Update nextcloud/ocp (1 jobs)"]
      direction TB
      wf_21_Update_nextcloud_ocp(["Trigger: Update nextcloud/ocp"]):::atlasWorkflow
      job_21_update_nextcloud_ocp["update-nextcloud-ocp"]:::atlasJob
      wf_21_Update_nextcloud_ocp --> job_21_update_nextcloud_ocp
    end
    pipeline_root --> wf_21_Update_nextcloud_ocp
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_2_Auto_approve_Dependabot_PRs["Auto approve Dependabot PRs (1 jobs)"]
      direction TB
      wf_2_Auto_approve_Dependabot_PRs(["Trigger: Auto approve Dependabot PRs"]):::atlasWorkflow
      job_2_auto_approve_merge["auto-approve-merge"]:::atlasJob
      wf_2_Auto_approve_Dependabot_PRs --> job_2_auto_approve_merge
    end
    pipeline_root --> wf_2_Auto_approve_Dependabot_PRs
    subgraph sg_wf_3_Block_fixup_and_squash_commits["Block fixup and squash commits (1 jobs)"]
      direction TB
      wf_3_Block_fixup_and_squash_commits(["Trigger: Block fixup and squash commits"]):::atlasWorkflow
      job_3_commit_message_check["commit-message-check"]:::atlasJob
      wf_3_Block_fixup_and_squash_commits --> job_3_commit_message_check
    end
    pipeline_root --> wf_3_Block_fixup_and_squash_commits
  end
  subgraph sg_grp_3_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_0_Build_and_publish_app_release["Build and publish app release (1 jobs)"]
      direction TB
      wf_0_Build_and_publish_app_release(["Trigger: Build and publish app release"]):::atlasWorkflow
      job_0_build_and_publish["build_and_publish"]:::atlasJob
      wf_0_Build_and_publish_app_release --> job_0_build_and_publish
    end
    pipeline_root --> wf_0_Build_and_publish_app_release
    subgraph sg_wf_18_Notify_release_relay_on_release["Notify release-relay on release (1 jobs)"]
      direction TB
      wf_18_Notify_release_relay_on_release(["Trigger: Notify release-relay on release"]):::atlasWorkflow
      job_18_notify["notify"]:::atlasJob
      wf_18_Notify_release_relay_on_release --> job_18_notify
    end
    pipeline_root --> wf_18_Notify_release_relay_on_release
  end
  wf_more["+12 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
