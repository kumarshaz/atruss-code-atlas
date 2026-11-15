---
title: Architecture — zulip/zulip
description: Arc42 and Pipeline report for zulip/zulip
---

# Repository Architecture Analysis: zulip/zulip

## Metadata
- **SHA**: `0d59088c1d4d1741e6ec17074f0ede4d0c467044`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 2.91
- **avg_cyclomatic_complexity**: 2.7
- **component_count**: 108
- **dead_code_count**: 236
- **dead_code_symbols**: 50 entry(ies)
- **duplication_pct**: 91.04
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 2053
- **fitness_passed**: False
- **fitness_violation_count**: 11
- **framework**: Django
- **import_edges**: 100 entry(ies)
- **loc**: 430796
- **max_cognitive_complexity**: 955
- **max_cyclomatic_complexity**: 347
- **sloc**: 342337
- **test_file_count**: 2297

# Architecture: zulip/zulip

## Context
- **Repository**: `zulip/zulip`
- **SHA**: `0d59088c1d4d1741e6ec17074f0ede4d0c467044`
- **Ecosystem**: Python
- **Framework**: Django

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
    repo_root(["zulip/zulip (108 components)"]):::atlasRoot
    dir_0_zerver["zerver (87)"]:::atlasCategory
    repo_root --> dir_0_zerver
    sub_0_0_models["models (58)"]:::atlasWorkflow
    dir_0_zerver --> sub_0_0_models
    sub_0_1_lib["lib (12)"]:::atlasWorkflow
    dir_0_zerver --> sub_0_1_lib
    sub_0_2_views["views (9)"]:::atlasWorkflow
    dir_0_zerver --> sub_0_2_views
    sub_0_more["+5 more submodules (8)"]:::atlasMore
    dir_0_zerver --> sub_0_more
    dir_1_zilencer["zilencer (9)"]:::atlasCategory
    repo_root --> dir_1_zilencer
    dir_2_corporate["corporate (8)"]:::atlasCategory
    repo_root --> dir_2_corporate
    dir_3_analytics["analytics (2)"]:::atlasCategory
    repo_root --> dir_3_analytics
    dir_4_confirmation["confirmation (1)"]:::atlasCategory
    repo_root --> dir_4_confirmation
    dir_other_modules["+1 more modules (1)"]:::atlasMore
    repo_root --> dir_other_modules
    sub_0_2_views -.->|"21 deps"| sub_0_0_models
    dir_1_zilencer -.->|"20 deps"| sub_0_1_lib
    dir_1_zilencer -.->|"19 deps"| sub_0_0_models
    sub_0_1_lib -.->|"17 deps"| sub_0_0_models
    dir_4_confirmation -.->|"7 deps"| sub_0_0_models
    sub_0_0_models -.->|"6 deps"| dir_4_confirmation
    dir_1_zilencer -.->|"5 deps"| dir_3_analytics
    sub_0_2_views -.->|"5 deps"| dir_4_confirmation
    dir_3_analytics -.->|"4 deps"| sub_0_0_models
    dir_2_corporate -.->|"3 deps"| sub_0_0_models
    sub_0_more -.->|"3 deps"| sub_0_0_models
    dir_2_corporate -.->|"2 deps"| dir_1_zilencer
    linkStyle 14 stroke:#ba1a1a,stroke-width:2px,stroke-dasharray: 5 5
```

## Component Details

Showing top 60 representative components out of 108 across 6 module group(s):

- **Module `zerver`** (87 components — DATA_ACCESS_LAYER: 82, SERVICE: 5)
- **Module `zilencer`** (9 components — DATA_ACCESS_LAYER: 9)
- **Module `corporate`** (8 components — DATA_ACCESS_LAYER: 8)
- **Module `analytics`** (2 components — DATA_ACCESS_LAYER: 2)
- **Module `confirmation`** (1 components — DATA_ACCESS_LAYER: 1)
- **Module `starlight_help`** (1 components — MODULE: 1)

- **PushRegistration** (`zilencer/views.py`): DATA_ACCESS_LAYER (deps: AdvertiseRealmData, InstallationCountDataForAnalytics, Realm, RealmAuditLogDataForAnalytics, RealmCountDataForAnalytics, RealmDataForAnalytics (+3 more))
- **RemoteServerNotificationPayload** (`zilencer/views.py`): DATA_ACCESS_LAYER (deps: AdvertiseRealmData, InstallationCountDataForAnalytics, Realm, RealmAuditLogDataForAnalytics, RealmCountDataForAnalytics, RealmDataForAnalytics (+3 more))
- **SendE2EEPushNotificationPayload** (`zilencer/views.py`): DATA_ACCESS_LAYER (deps: AdvertiseRealmData, InstallationCountDataForAnalytics, Realm, RealmAuditLogDataForAnalytics, RealmCountDataForAnalytics, RealmDataForAnalytics (+3 more))
- **TestNotificationPayload** (`zilencer/views.py`): DATA_ACCESS_LAYER (deps: AdvertiseRealmData, InstallationCountDataForAnalytics, Realm, RealmAuditLogDataForAnalytics, RealmCountDataForAnalytics, RealmDataForAnalytics (+3 more))
- **Confirmation** (`confirmation/models.py`): DATA_ACCESS_LAYER (deps: EmailChangeStatus, MultiuseInvite, PreregistrationRealm, PreregistrationUser, Realm, RealmCreationStatus (+1 more))
- **NarrowParameter** (`zerver/lib/narrow.py`): DATA_ACCESS_LAYER (deps: DirectMessageGroup, Realm, Recipient, Stream, Subscription)
- **AbstractRemoteRealmBillingUser** (`zilencer/models.py`): DATA_ACCESS_LAYER (deps: AbstractPushDeviceToken, AbstractRealmAuditLog, BaseCount, Realm)
- **AbstractRemoteServerBillingUser** (`zilencer/models.py`): DATA_ACCESS_LAYER (deps: AbstractPushDeviceToken, AbstractRealmAuditLog, BaseCount, Realm)
- **AbstractScheduledJob** (`zerver/models/scheduled_jobs.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient, Stream)
- **AddSubscriptionData** (`zerver/views/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Stream, UserGroup, UserTopic)
- **ChannelEmailAddress** (`zerver/models/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Realm, Recipient, UserGroup)
- **DefaultStream** (`zerver/models/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Realm, Recipient, UserGroup)
- **DefaultStreamGroup** (`zerver/models/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Realm, Recipient, UserGroup)
- **MissedMessageEmailAddress** (`zerver/models/scheduled_jobs.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient, Stream)
- **ProfileDataElement** (`zerver/views/users.py`): DATA_ACCESS_LAYER (deps: DeactivateUserActions, Realm, Service, Stream)
- **RemotePushDevice** (`zilencer/models.py`): DATA_ACCESS_LAYER (deps: AbstractPushDeviceToken, AbstractRealmAuditLog, BaseCount, Realm)
- **RemoteRealm** (`zilencer/models.py`): DATA_ACCESS_LAYER (deps: AbstractPushDeviceToken, AbstractRealmAuditLog, BaseCount, Realm)
- **RemoteZulipServer** (`zilencer/models.py`): DATA_ACCESS_LAYER (deps: AbstractPushDeviceToken, AbstractRealmAuditLog, BaseCount, Realm)
- **ScheduledMessage** (`zerver/models/scheduled_jobs.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient, Stream)
- **ScheduledMessageNotificationEmail** (`zerver/models/scheduled_jobs.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient, Stream)
- **Stream** (`zerver/models/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Realm, Recipient, UserGroup)
- **Subscription** (`zerver/models/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Realm, Recipient, UserGroup)
- **SubscriptionPropertyChangeRequest** (`zerver/views/streams.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Stream, UserGroup, UserTopic)
- **AbstractAttachment** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **AbstractCustomerPlan** (`corporate/models/plans.py`): DATA_ACCESS_LAYER (deps: Customer, LicenseLedger, Realm)
- **AbstractEmoji** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **AbstractMessage** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **AbstractRealmAuditLog** (`zerver/models/realm_audit_logs.py`): DATA_ACCESS_LAYER (deps: ChannelFolder, Realm, Stream)
- **AbstractSubMessage** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **AbstractUserMessage** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **ArchiveTransaction** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **Customer** (`corporate/models/customers.py`): DATA_ACCESS_LAYER (deps: Realm, RemoteRealm, RemoteZulipServer)
- **DeactivateUserActions** (`zerver/actions/message_delete.py`): DATA_ACCESS_LAYER (deps: Realm, Recipient, Stream)
- **ImageAttachment** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **OnboardingUserMessage** (`zerver/models/messages.py`): DATA_ACCESS_LAYER (deps: Client, Realm, Recipient)
- **PresenceSequence** (`zerver/models/presence.py`): DATA_ACCESS_LAYER (deps: AbstractEmoji, Client, Realm)
- **TargetUsersData** (`zerver/views/user_settings.py`): DATA_ACCESS_LAYER (deps: Confirmation, EmailChangeStatus, UserBaseSettings)
- **TusEvent** (`zerver/views/tusd.py`): DATA_ACCESS_LAYER (deps: Confirmation, PreregistrationRealm, Realm)
- **TusHTTPRequest** (`zerver/views/tusd.py`): DATA_ACCESS_LAYER (deps: Confirmation, PreregistrationRealm, Realm)
- **TusHook** (`zerver/views/tusd.py`): DATA_ACCESS_LAYER (deps: Confirmation, PreregistrationRealm, Realm)
- **TusUpload** (`zerver/views/tusd.py`): DATA_ACCESS_LAYER (deps: Confirmation, PreregistrationRealm, Realm)
- **UserPresence** (`zerver/models/presence.py`): DATA_ACCESS_LAYER (deps: AbstractEmoji, Client, Realm)
- **BaseCount** (`analytics/models.py`): DATA_ACCESS_LAYER (deps: Realm, Stream)
- **DirectMessageGroup** (`zerver/models/recipients.py`): DATA_ACCESS_LAYER (deps: Stream, Subscription)
- **EmailChangeStatus** (`zerver/models/prereg_users.py`): DATA_ACCESS_LAYER (deps: Confirmation, Realm)
- **ExternalAuthID** (`zerver/models/users.py`): DATA_ACCESS_LAYER (deps: CustomProfileFieldValue, Realm)
- **FillState** (`analytics/models.py`): DATA_ACCESS_LAYER (deps: Realm, Stream)
- **GenericOutgoingWebhookService** (`zerver/lib/outgoing_webhook.py`): SERVICE (deps: Realm, Service)
- **MultiuseInvite** (`zerver/models/prereg_users.py`): DATA_ACCESS_LAYER (deps: Confirmation, Realm)
- **PreregistrationRealm** (`zerver/models/prereg_users.py`): DATA_ACCESS_LAYER (deps: Confirmation, Realm)
- **PreregistrationUser** (`zerver/models/prereg_users.py`): DATA_ACCESS_LAYER (deps: Confirmation, Realm)
- **RealmCreationStatus** (`zerver/models/prereg_users.py`): DATA_ACCESS_LAYER (deps: Confirmation, Realm)
- **RealmReactivationStatus** (`zerver/models/prereg_users.py`): DATA_ACCESS_LAYER (deps: Confirmation, Realm)
- **Recipient** (`zerver/models/recipients.py`): DATA_ACCESS_LAYER (deps: Stream, Subscription)
- **SlackOutgoingWebhookService** (`zerver/lib/outgoing_webhook.py`): SERVICE (deps: Realm, Service)
- **UserBaseSettings** (`zerver/models/users.py`): DATA_ACCESS_LAYER (deps: CustomProfileFieldValue, Realm)
- **UserTopic** (`zerver/models/user_topics.py`): DATA_ACCESS_LAYER (deps: Recipient, Stream)
- **ZulipSponsorshipRequest** (`corporate/models/sponsorships.py`): DATA_ACCESS_LAYER (deps: Customer, Realm)
- **AdvertiseRealmData** (`zerver/lib/remote_server.py`): DATA_ACCESS_LAYER (deps: Realm)
- **AlertWord** (`zerver/models/alert_words.py`): DATA_ACCESS_LAYER (deps: Realm)

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (60.95/100)
- **Technical Debt Score**: 39.05
- **Estimated Remediation Effort**: 155.97h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.00 | 0.20 | avg_cc=2.70, max_cc=347, duplication=91.04%, dead_code=236 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=660, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 0.00 | 0.15 | avg_cognitive=2.91, max_cognitive=955, fitness_violations=11, oversized_files=25 |
| Pipeline Health | `D` | 63.00 | 0.15 | workflows=8, operational_antipatterns=14, parallel_branches=True |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Confirmation -> EmailChangeStatus -> Confirmation)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Confirmation -> MultiuseInvite -> Confirmation)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Confirmation -> PreregistrationRealm -> Confirmation)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Confirmation -> PreregistrationUser -> Confirmation)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Confirmation -> RealmCreationStatus -> Confirmation)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Confirmation -> RealmReactivationStatus -> Confirmation)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Recipient -> Stream -> Recipient)
- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Recipient -> Subscription -> Recipient)
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (91.04) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (955.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (347.0) exceeds policy threshold (20.0).

### Workspace Packages
- **starlight_help** (`starlight_help`, react_ts_js, pnpm)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 660 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `PyGithub` `*` (PyPI, `pyproject.toml`)
- `aioapns` `*` (PyPI, `pyproject.toml`)
- `aioapns` `4.0` (PyPI, `uv.lock`)
- `aiohttp` `*` (PyPI, `pyproject.toml`)
- `aiohttp` `3.14.5` (PyPI, `uv.lock`)
- `aiosmtpd` `1.4.6` (PyPI, `pyproject.toml`)
- `aiosmtpd` `1.4.6` (PyPI, `uv.lock`)
- `altcha` `*` (PyPI, `pyproject.toml`)
- `altcha` `2.3.0` (PyPI, `uv.lock`)
- `annotated-types` `*` (PyPI, `pyproject.toml`)
- `annotated-types` `0.8.0` (PyPI, `uv.lock`)
- `asgiref` `*` (PyPI, `pyproject.toml`)
- `asgiref` `3.12.1` (PyPI, `uv.lock`)
- `atpublic` `8.0.1` (PyPI, `uv.lock`)
- `atpublic` `9.0.0` (PyPI, `pyproject.toml`)
- `backports-datetime-fromisoformat` `*` (PyPI, `pyproject.toml`)
- `backports-datetime-fromisoformat` `2.0.3` (PyPI, `uv.lock`)
- `beautifulsoup4` `*` (PyPI, `pyproject.toml`)
- `beautifulsoup4` `4.15.0` (PyPI, `uv.lock`)
- `black` `*` (PyPI, `pyproject.toml`)
- `black` `26.10.1` (PyPI, `uv.lock`)
- `boto3` `*` (PyPI, `pyproject.toml`)
- `boto3` `1.43.115` (PyPI, `uv.lock`)
- `boto3-stubs` `*` (PyPI, `pyproject.toml`)
- `boto3-stubs` `1.43.115` (PyPI, `uv.lock`)
- `certifi` `*` (PyPI, `pyproject.toml`)
- `certifi` `2026.10.19` (PyPI, `uv.lock`)
- `chardet` `*` (PyPI, `pyproject.toml`)
- `chardet` `7.7.0` (PyPI, `uv.lock`)
- `codespell` `*` (PyPI, `pyproject.toml`)
- ... (+630 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_starlight_help["starlight_help"]:::atlasCategory
        mod_tools_ci["tools/ci"]:::atlasCategory
        mod_tools_setup_dev_vagrant_docker["tools/setup/dev-vagrant-docker"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_tools_ci_Dockerfile["tools/ci/Dockerfile"]:::atlasWorkflow
        art_tools_ci_Dockerfile_prod["tools/ci/Dockerfile.prod"]:::atlasWorkflow
        art_tools_setup_dev_vagrant_docker_Dockerfile["tools/setup/dev-vagrant-docker/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_production_suite_yml_production_build["production-suite.yml#production_build"]:::atlasJob
        job_zulip_ci_yml_tests["zulip-ci.yml#tests"]:::atlasJob
    end
    mod_starlight_help -->|BUILT_BY| job_zulip_ci_yml_tests
    mod_tools_ci -->|BUILT_BY| job_production_suite_yml_production_build
    mod_tools_ci -->|BUILT_BY| job_zulip_ci_yml_tests
    mod_tools_ci -->|PACKAGED_BY| art_tools_ci_Dockerfile
    mod_tools_ci -->|PACKAGED_BY| art_tools_ci_Dockerfile_prod
    mod_tools_ci -->|PACKAGED_BY| art_tools_setup_dev_vagrant_docker_Dockerfile
    mod_tools_setup_dev_vagrant_docker -->|PACKAGED_BY| art_tools_setup_dev_vagrant_docker_Dockerfile
    art_tools_ci_Dockerfile -->|BUILT_BY| job_production_suite_yml_production_build
    art_tools_ci_Dockerfile -->|BUILT_BY| job_zulip_ci_yml_tests
    art_tools_ci_Dockerfile_prod -->|BUILT_BY| job_production_suite_yml_production_build
    art_tools_ci_Dockerfile_prod -->|BUILT_BY| job_zulip_ci_yml_tests
```

- `starlight_help` (code_module) --[BUILT_BY]--> `zulip-ci.yml#tests` (ci_job)
- `tools/ci` (code_module) --[BUILT_BY]--> `production-suite.yml#production_build` (ci_job)
- `tools/ci` (code_module) --[BUILT_BY]--> `zulip-ci.yml#tests` (ci_job)
- `tools/ci` (code_module) --[PACKAGED_BY]--> `tools/ci/Dockerfile` (container)
- `tools/ci` (code_module) --[PACKAGED_BY]--> `tools/ci/Dockerfile.prod` (container)
- `tools/ci` (code_module) --[PACKAGED_BY]--> `tools/setup/dev-vagrant-docker/Dockerfile` (container)
- `tools/setup/dev-vagrant-docker` (code_module) --[PACKAGED_BY]--> `tools/setup/dev-vagrant-docker/Dockerfile` (container)
- `tools/ci/Dockerfile` (container) --[BUILT_BY]--> `production-suite.yml#production_build` (ci_job)
- `tools/ci/Dockerfile` (container) --[BUILT_BY]--> `zulip-ci.yml#tests` (ci_job)
- `tools/ci/Dockerfile.prod` (container) --[BUILT_BY]--> `production-suite.yml#production_build` (ci_job)
- `tools/ci/Dockerfile.prod` (container) --[BUILT_BY]--> `zulip-ci.yml#tests` (ci_job)


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
  pipeline_root(["zulip/zulip (8 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Scheduled___Manual["Scheduled & Manual (4 workflows · 9 jobs)"]
    direction TB
    subgraph sg_wf_0_API_Documentation_Update_Check["API Documentation Update Check (2 jobs)"]
      direction TB
      wf_0_API_Documentation_Update_Check(["Trigger: API Documentation Update Check"]):::atlasWorkflow
      job_0_check_feature_level_updated["check-feature-level-updated"]:::atlasJob
      job_0_notify_if_api_docs_changed["notify-if-api-docs-changed"]:::atlasJob
      wf_0_API_Documentation_Update_Check --> job_0_check_feature_level_updated
      job_0_check_feature_level_updated --> job_0_notify_if_api_docs_changed
    end
    pipeline_root --> wf_0_API_Documentation_Update_Check
    subgraph sg_wf_2_Code_scanning["Code scanning (1 jobs)"]
      direction TB
      wf_2_Code_scanning(["Trigger: Code scanning"]):::atlasWorkflow
      job_2_CodeQL["CodeQL"]:::atlasJob
      wf_2_Code_scanning --> job_2_CodeQL
    end
    pipeline_root --> wf_2_Code_scanning
    subgraph sg_wf_3_Zulip_production_suite["Zulip production suite (4 jobs)"]
      direction TB
      wf_3_Zulip_production_suite(["Trigger: Zulip production suite"]):::atlasWorkflow
      job_3_production_build["production_build"]:::atlasJob
      job_3_production_install["production_install"]:::atlasJob
      job_3_production_upgrade["production_upgrade"]:::atlasJob
      wf_3_Zulip_production_suite --> job_3_production_build
      job_3_production_build --> job_3_production_install
      job_3_production_build --> job_3_production_upgrade
    end
    pipeline_root --> wf_3_Zulip_production_suite
    subgraph sg_wf_6_Zulip_CI["Zulip CI (2 jobs)"]
      direction TB
      wf_6_Zulip_CI(["Trigger: Zulip CI"]):::atlasWorkflow
      job_6_tests["tests"]:::atlasJob
      job_6_required_jobs["required-jobs"]:::atlasJob
      wf_6_Zulip_CI --> job_6_tests
      job_6_tests --> job_6_required_jobs
    end
    pipeline_root --> wf_6_Zulip_CI
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (2 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_4_Update_one_click_apps["Update one click apps (1 jobs)"]
      direction TB
      wf_4_Update_one_click_apps(["Trigger: Update one click apps"]):::atlasWorkflow
      job_4_update_digitalocean_oneclick_app["update-digitalocean-oneclick-app"]:::atlasJob
      wf_4_Update_one_click_apps --> job_4_update_digitalocean_oneclick_app
    end
    pipeline_root --> wf_4_Update_one_click_apps
    subgraph sg_wf_7_Notify_of_issues_resolved_in_latest_Zulip_Cloud_deploy["Notify of issues resolved in latest Zulip Cloud deploy (2 jobs)"]
      direction TB
      wf_7_Notify_of_issues_resolved_in_latest_Zulip_Cloud_deploy(["Trigger: Notify of issues resolved in latest Zulip Cloud deploy"]):::atlasWorkflow
      job_7_build_messages["build-messages"]:::atlasJob
      job_7_send_messages["send-messages"]:::atlasJob
      wf_7_Notify_of_issues_resolved_in_latest_Zulip_Cloud_deploy --> job_7_build_messages
      job_7_build_messages --> job_7_send_messages
    end
    pipeline_root --> wf_7_Notify_of_issues_resolved_in_latest_Zulip_Cloud_deploy
  end
  subgraph sg_grp_2_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_1_Auto_add_general_area_label["Auto add general area label (1 jobs)"]
      direction TB
      wf_1_Auto_add_general_area_label(["Trigger: Auto add general area label"]):::atlasWorkflow
      job_1_add_general_label["add-general-label"]:::atlasJob
      wf_1_Auto_add_general_area_label --> job_1_add_general_label
    end
    pipeline_root --> wf_1_Auto_add_general_area_label
  end
  subgraph sg_grp_3_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_5_GitHub_Actions_Security_Analysis_with_zizmor["GitHub Actions Security Analysis with zizmor (1 jobs)"]
      direction TB
      wf_5_GitHub_Actions_Security_Analysis_with_zizmor(["Trigger: GitHub Actions Security Analysis with zizmor"]):::atlasWorkflow
      job_5_zizmor["zizmor"]:::atlasJob
      wf_5_GitHub_Actions_Security_Analysis_with_zizmor --> job_5_zizmor
    end
    pipeline_root --> wf_5_GitHub_Actions_Security_Analysis_with_zizmor
  end
```
