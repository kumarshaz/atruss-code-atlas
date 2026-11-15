---
title: Architecture — nextcloud/forms
description: Arc42 and Pipeline report for nextcloud/forms
---

# Repository Architecture Analysis: nextcloud/forms

## Metadata
- **SHA**: `721c146513097c1d6d1c0a716ec20c2e9514edc1`
- **Primary Ecosystem**: PHP

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 151
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 151
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: PHP Composer
- **import_edges**: 0 entry(ies)
- **loc**: 29646
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 21131
- **test_file_count**: 61

# Architecture: nextcloud/forms

## Context
- **Repository**: `nextcloud/forms`
- **SHA**: `721c146513097c1d6d1c0a716ec20c2e9514edc1`
- **Ecosystem**: PHP
- **Framework**: PHP Composer

## Building Block View

```mermaid
graph TD;
    repo_root(["nextcloud/forms (151 components)"])
    dir_0_lib["lib (100)"]
    repo_root --> dir_0_lib
    sub_0_0_Migration["Migration (41)"]
    dir_0_lib --> sub_0_0_Migration
    sub_0_1_Db["Db (14)"]
    dir_0_lib --> sub_0_1_Db
    sub_0_2_Activity["Activity (8)"]
    dir_0_lib --> sub_0_2_Activity
    sub_0_more["+15 more submodules (37)"]
    dir_0_lib --> sub_0_more
    dir_1_tests["tests (46)"]
    repo_root --> dir_1_tests
    sub_1_0_Unit["Unit (36)"]
    dir_1_tests --> sub_1_0_Unit
    sub_1_1_Integration["Integration (6)"]
    dir_1_tests --> sub_1_1_Integration
    sub_1_2_stubs["stubs (3)"]
    dir_1_tests --> sub_1_2_stubs
    sub_1_more["+1 more submodules (1)"]
    dir_1_tests --> sub_1_more
    dir_2__root_["(root) (3)"]
    repo_root --> dir_2__root_
    dir_3_templates["templates (2)"]
    repo_root --> dir_3_templates
```

## Component Details

Showing top 60 representative components out of 151 across 4 module group(s):

- **Module `lib`** (100 components — module: 100)
- **Module `tests`** (46 components — module: 46)
- **Module `(root)`** (3 components — module: 3)
- **Module `templates`** (2 components — module: 2)

- **.php-cs-fixer.dist** (`.php-cs-fixer.dist.php`): module
- **AbstractFormEvent** (`lib/Events/AbstractFormEvent.php`): module
- **ActivityConstants** (`lib/Activity/ActivityConstants.php`): module
- **ActivityManager** (`lib/Activity/ActivityManager.php`): module
- **ActivityManagerTest** (`tests/Unit/Activity/ActivityManagerTest.php`): module
- **AnalyticsDatasource** (`lib/Analytics/AnalyticsDatasource.php`): module
- **AnalyticsDatasourceListener** (`lib/Listener/AnalyticsDatasourceListener.php`): module
- **AnalyticsDatasourceTest** (`tests/Unit/Analytics/AnalyticsDatasourceTest.php`): module
- **Answer** (`lib/Db/Answer.php`): module
- **AnswerMapper** (`lib/Db/AnswerMapper.php`): module
- **ApiController** (`lib/Controller/ApiController.php`): module
- **ApiControllerTest** (`tests/Unit/Controller/ApiControllerTest.php`): module
- **ApiV3Test** (`tests/Integration/Api/ApiV3Test.php`): module
- **Application** (`lib/AppInfo/Application.php`): module
- **ApplicationTest** (`tests/Unit/AppInfo/ApplicationTest.php`): module
- **AuditEvents** (`tests/Unit/AuditLog/AuditEvents.php`): module
- **AuditLogger** (`lib/AuditLog/AuditLogger.php`): module
- **AuditLoggerTest** (`tests/Unit/AuditLog/AuditLoggerTest.php`): module
- **Capabilities** (`lib/Capabilities.php`): module
- **CirclesService** (`lib/Service/CirclesService.php`): module
- **CirclesServiceTest** (`tests/Unit/Service/CirclesServiceTest.php`): module
- **CleanupUploadedFilesJob** (`lib/BackgroundJob/CleanupUploadedFilesJob.php`): module
- **CleanupUploadedFilesJobTest** (`tests/Unit/BackgroundJob/CleanupUploadedFilesJobTest.php`): module
- **CommentsEntityListener** (`lib/Listener/CommentsEntityListener.php`): module
- **ConfigController** (`lib/Controller/ConfigController.php`): module
- **ConfigControllerTest** (`tests/Unit/Controller/ConfigControllerTest.php`): module
- **ConfigService** (`lib/Service/ConfigService.php`): module
- **ConfigServiceTest** (`tests/Unit/Service/ConfigServiceTest.php`): module
- **ConfirmationEmailService** (`lib/Service/ConfirmationEmailService.php`): module
- **ConfirmationEmailServiceTest** (`tests/Unit/Service/ConfirmationEmailServiceTest.php`): module
- **Constants** (`lib/Constants.php`): module
- **DeleteQuestionFoldersJob** (`lib/BackgroundJob/DeleteQuestionFoldersJob.php`): module
- **DeleteQuestionFoldersJobTest** (`tests/Integration/BackgroundJob/DeleteQuestionFoldersJobTest.php`): module
- **FilePathHelper** (`lib/Helper/FilePathHelper.php`): module
- **FilePathHelperTest** (`tests/Unit/Helper/FilePathHelperTest.php`): module
- **Filter** (`lib/Activity/Filter.php`): module
- **FilterTest** (`tests/Unit/Activity/FilterTest.php`): module
- **Form** (`lib/Db/Form.php`): module
- **FormMapper** (`lib/Db/FormMapper.php`): module
- **FormMapperTest** (`tests/Unit/Db/FormMapperTest.php`): module
- **FormSubmittedEvent** (`lib/Events/FormSubmittedEvent.php`): module
- **FormsActivitySettings** (`lib/Activity/Settings/FormsActivitySettings.php`): module
- **FormsActivitySettingsTest** (`tests/Unit/Activity/Settings/FormsActivitySettingsTest.php`): module
- **FormsMigrator** (`lib/FormsMigrator.php`): module
- **FormsMigratorTest** (`tests/Unit/FormsMigratorTest.php`): module
- **FormsSearchResultEntry** (`lib/Search/FormsSearchResultEntry.php`): module
- **FormsService** (`lib/Service/FormsService.php`): module
- **FormsServiceTest** (`tests/Unit/Service/FormsServiceTest.php`): module
- **IntegrationBase** (`tests/Integration/IntegrationBase.php`): module
- **MockedMapperException** (`tests/Unit/MockedMapperException.php`): module
- **NewShare** (`lib/Activity/Settings/NewShare.php`): module
- **NewShareTest** (`tests/Unit/Activity/Settings/NewShareTest.php`): module
- **NewSharedSubmission** (`lib/Activity/Settings/NewSharedSubmission.php`): module
- **NewSharedSubmissionTest** (`tests/Unit/Activity/Settings/NewSharedSubmissionTest.php`): module
- **NewSubmission** (`lib/Activity/Settings/NewSubmission.php`): module
- **NewSubmissionTest** (`tests/Unit/Activity/Settings/NewSubmissionTest.php`): module
- **NoSuchFormException** (`lib/Exception/NoSuchFormException.php`): module
- **Operation** (`lib/AuditLog/Operation.php`): module
- **OperationTest** (`tests/Unit/AuditLog/OperationTest.php`): module
- **Option** (`lib/Db/Option.php`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (60.50/100)
- **Technical Debt Score**: 39.50
- **Estimated Remediation Effort**: 66.38h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1030, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=22, operational_antipatterns=50, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=5, pipeline_security_findings=8 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1030 | **Vulnerabilities**: 0 | **Secrets**: 5

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `docs/API_v3.md:696` (`"token": "abcd***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `l10n/zh_HK.js:261` (`"Set the public share link token to something easy to remember or generate a new token." : "將公開分***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `l10n/zh_HK.json:259` (`"Set the public share link token to something easy to remember or generate a new token." : "將公開分***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `l10n/zh_TW.js:262` (`"Set the public share link token to something easy to remember or generate a new token." : "將公開分***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `l10n/zh_TW.json:260` (`"Set the public share link token to something easy to remember or generate a new token." : "將公開分***REDACTED***",`)

### Inventory Sample
- `maennchen/zipstream-php` `2.4` (composer, `composer.json`)
- `nextcloud/coding-standard` `1.3` (composer, `vendor-bin/cs-fixer/composer.json`)
- `phpoffice/phpspreadsheet` `5.0` (composer, `composer.json`)
- `@material-symbols/svg-400` `0.48.3` (npm, `package-lock.json`)
- `@material-symbols/svg-400` `0.48.3` (npm, `package.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/auth` `2.6.0` (npm, `package.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package-lock.json`)
- `@nextcloud/axios` `2.6.0` (npm, `package.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package-lock.json`)
- `@nextcloud/browserslist-config` `3.1.2` (npm, `package.json`)
- `@nextcloud/dialogs` `8.0.0` (npm, `package-lock.json`)
- `@nextcloud/dialogs` `8.0.0` (npm, `package.json`)
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
- `@nextcloud/logger` `3.0.3` (npm, `package-lock.json`)
- `@nextcloud/logger` `3.0.3` (npm, `package.json`)
- `@nextcloud/moment` `1.3.5` (npm, `package-lock.json`)
- `@nextcloud/moment` `1.3.5` (npm, `package.json`)
- `@nextcloud/prettier-config` `1.2.0` (npm, `package-lock.json`)
- ... (+1000 more dependencies)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["nextcloud/forms (22 workflows)"])
  grp_0_CI___Verification["CI & Verification (15 workflows · 35 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Scheduled___Manual["Scheduled & Manual (3 workflows · 3 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  grp_2_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]
  pipeline_root --> grp_2_Release___Deploy
  grp_3_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]
  pipeline_root --> grp_3_Security___Governance
```
