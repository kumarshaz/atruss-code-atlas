---
title: Architecture — mastodon/mastodon
description: Arc42 and Pipeline report for mastodon/mastodon
---

# Repository Architecture Analysis: mastodon/mastodon

## Metadata
- **SHA**: `296ca2874f3b7c02e79d2041b54f352a392f17ba`
- **Primary Ecosystem**: Ruby

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 14.35
- **avg_cyclomatic_complexity**: 5.55
- **component_count**: 255
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.43
- **file_complexities**: 9 entry(ies)
- **files_analyzed**: 3369
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: Ruby on Rails
- **import_edges**: 40 entry(ies)
- **loc**: 198442
- **max_cognitive_complexity**: 287
- **max_cyclomatic_complexity**: 110
- **sloc**: 148598
- **test_file_count**: 34

# Architecture: mastodon/mastodon

## Context
- **Repository**: `mastodon/mastodon`
- **SHA**: `296ca2874f3b7c02e79d2041b54f352a392f17ba`
- **Ecosystem**: Ruby
- **Framework**: Ruby on Rails

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
    repo_root(["mastodon/mastodon (255 components)"]):::atlasRoot
    dir_0_app["app (250)"]:::atlasCategory
    repo_root --> dir_0_app
    sub_0_0_controllers["controllers (244)"]:::atlasWorkflow
    dir_0_app --> sub_0_0_controllers
    sub_0_1_chewy["chewy (6)"]:::atlasWorkflow
    dir_0_app --> sub_0_1_chewy
    dir_1_streaming["streaming (4)"]:::atlasCategory
    repo_root --> dir_1_streaming
    dir_2__devcontainer[".devcontainer (1)"]:::atlasCategory
    repo_root --> dir_2__devcontainer
```

## Component Details

Showing top 60 representative components out of 255 across 3 module group(s):

- **Module `app`** (250 components — module: 250)
- **Module `streaming`** (4 components — API_ROUTE: 3, MODULE: 1)
- **Module `.devcontainer`** (1 components — module: 1)

- **@mastodon/streaming** (`streaming/package.json`): MODULE
- **GET_api_v1_streaming_health** (`streaming/index.js`): API_ROUTE
- **GET_favicon.ico** (`streaming/index.js`): API_ROUTE
- **GET_metrics** (`streaming/index.js`): API_ROUTE
- **about_controller** (`app/controllers/about_controller.rb`): module
- **about_controller** (`app/controllers/admin/settings/about_controller.rb`): module
- **account_actions_controller** (`app/controllers/admin/account_actions_controller.rb`): module
- **account_actions_controller** (`app/controllers/api/v1/admin/account_actions_controller.rb`): module
- **account_moderation_notes_controller** (`app/controllers/admin/account_moderation_notes_controller.rb`): module
- **accounts_controller** (`app/controllers/accounts_controller.rb`): module
- **accounts_controller** (`app/controllers/admin/accounts_controller.rb`): module
- **accounts_controller** (`app/controllers/admin/email_subscriptions/accounts_controller.rb`): module
- **accounts_controller** (`app/controllers/api/v1/accounts_controller.rb`): module
- **accounts_controller** (`app/controllers/api/v1/admin/accounts_controller.rb`): module
- **accounts_controller** (`app/controllers/api/v1/lists/accounts_controller.rb`): module
- **accounts_index** (`app/chewy/accounts_index.rb`): module
- **action_logs_controller** (`app/controllers/admin/action_logs_controller.rb`): module
- **actions_controller** (`app/controllers/admin/reports/actions_controller.rb`): module
- **activity_controller** (`app/controllers/api/v1/instances/activity_controller.rb`): module
- **additional_footer_texts_controller** (`app/controllers/admin/email_subscriptions/additional_footer_texts_controller.rb`): module
- **announcements_controller** (`app/controllers/admin/announcements_controller.rb`): module
- **announcements_controller** (`app/controllers/api/v1/announcements_controller.rb`): module
- **annual_reports_controller** (`app/controllers/api/v1/annual_reports_controller.rb`): module
- **appeals_controller** (`app/controllers/admin/disputes/appeals_controller.rb`): module
- **appearance_controller** (`app/controllers/admin/settings/appearance_controller.rb`): module
- **application_controller** (`app/controllers/application_controller.rb`): module
- **approvals_controller** (`app/controllers/admin/trends/approvals_controller.rb`): module
- **apps_controller** (`app/controllers/api/v1/apps_controller.rb`): module
- **authorize_interactions_controller** (`app/controllers/authorize_interactions_controller.rb`): module
- **avatars_controller** (`app/controllers/api/v1/profile/avatars_controller.rb`): module
- **backfill_requests_controller** (`app/controllers/api/fasp/data_sharing/v0/backfill_requests_controller.rb`): module
- **backups_controller** (`app/controllers/backups_controller.rb`): module
- **base_controller** (`app/controllers/activitypub/base_controller.rb`): module
- **base_controller** (`app/controllers/admin/base_controller.rb`): module
- **base_controller** (`app/controllers/api/base_controller.rb`): module
- **base_controller** (`app/controllers/api/fasp/base_controller.rb`): module
- **base_controller** (`app/controllers/api/v1/accounts/base_controller.rb`): module
- **base_controller** (`app/controllers/api/v1/instances/base_controller.rb`): module
- **base_controller** (`app/controllers/api/v1/statuses/base_controller.rb`): module
- **base_controller** (`app/controllers/api/v1/timelines/base_controller.rb`): module
- **blocks_controller** (`app/controllers/api/v1/blocks_controller.rb`): module
- **bookmarks_controller** (`app/controllers/api/v1/bookmarks_controller.rb`): module
- **bookmarks_controller** (`app/controllers/api/v1/statuses/bookmarks_controller.rb`): module
- **branding_controller** (`app/controllers/admin/settings/branding_controller.rb`): module
- **callbacks_controller** (`app/controllers/admin/fasp/debug/callbacks_controller.rb`): module
- **canonical_email_blocks_controller** (`app/controllers/api/v1/admin/canonical_email_blocks_controller.rb`): module
- **capability_activations_controller** (`app/controllers/admin/fasp/capability_activations_controller.rb`): module
- **change_emails_controller** (`app/controllers/admin/change_emails_controller.rb`): module
- **collection_items_controller** (`app/controllers/api/v1/collection_items_controller.rb`): module
- **collection_items_controller** (`app/controllers/collection_items_controller.rb`): module
- **collections_controller** (`app/controllers/activitypub/collections_controller.rb`): module
- **collections_controller** (`app/controllers/admin/collections_controller.rb`): module
- **collections_controller** (`app/controllers/api/v1/collections_controller.rb`): module
- **collections_controller** (`app/controllers/collections_controller.rb`): module
- **compose** (`.devcontainer/compose.yaml`): module
- **confirmations_controller** (`app/controllers/admin/confirmations_controller.rb`): module
- **confirmations_controller** (`app/controllers/api/v1/emails/confirmations_controller.rb`): module
- **content_retention_controller** (`app/controllers/admin/settings/content_retention_controller.rb`): module
- **contexts_controller** (`app/controllers/activitypub/contexts_controller.rb`): module
- **contexts_controller** (`app/controllers/api/v1/statuses/contexts_controller.rb`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (44.78/100)
- **Technical Debt Score**: 55.22
- **Estimated Remediation Effort**: 62.89h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 64.16 | 0.20 | avg_cc=5.55, max_cc=110, duplication=0.43%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=316, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 33.00 | 0.15 | avg_cognitive=14.35, max_cognitive=287, fitness_violations=2, oversized_files=1 |
| Pipeline Health | `F` | 25.00 | 0.15 | workflows=22, operational_antipatterns=21, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=4, pipeline_security_findings=17 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (287.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (110.0) exceeds policy threshold (20.0).

### Workspace Packages
- **@mastodon/streaming** (`streaming`, react_ts_js, yarn)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 316 | **Vulnerabilities**: 0 | **Secrets**: 4

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `.env.development:2` (`ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY=fkSx***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `.env.development:3` (`ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT=r0hv***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `.env.development:4` (`ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY=PhdF***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `app/javascript/mastodon/locales/th.json:417` (`"keyboard_shortcuts.toggle_hidden": "แสดง***REDACTED***",`)

### Inventory Sample
- `active_model_serializers` `0.10` (gem, `Gemfile`)
- `addressable` `2.8` (gem, `Gemfile`)
- `annotaterb` `4.13` (gem, `Gemfile`)
- `aws-sdk-core` `*` (gem, `Gemfile`)
- `aws-sdk-s3` `1.123` (gem, `Gemfile`)
- `base58` `0.2.3` (gem, `Gemfile`)
- `better_errors` `2.9` (gem, `Gemfile`)
- `binding_of_caller` `*` (gem, `Gemfile`)
- `bloom_fit` `1.2` (gem, `Gemfile`)
- `blurhash` `0.1` (gem, `Gemfile`)
- `bootsnap` `*` (gem, `Gemfile`)
- `brakeman` `8.0` (gem, `Gemfile`)
- `browser` `*` (gem, `Gemfile`)
- `bundler-audit` `0.9` (gem, `Gemfile`)
- `capybara` `3.39` (gem, `Gemfile`)
- `capybara-playwright-driver` `*` (gem, `Gemfile`)
- `charlock_holmes` `0.7.7` (gem, `Gemfile`)
- `chewy` `*` (gem, `Gemfile`)
- `climate_control` `*` (gem, `Gemfile`)
- `cocoon` `1.2` (gem, `Gemfile`)
- `color_diff` `0.1` (gem, `Gemfile`)
- `concurrent-ruby` `*` (gem, `Gemfile`)
- `connection_pool` `*` (gem, `Gemfile`)
- `csv` `3.2` (gem, `Gemfile`)
- `database_cleaner-active_record` `*` (gem, `Gemfile`)
- `debug` `1.8` (gem, `Gemfile`)
- `devise` `*` (gem, `Gemfile`)
- `devise-two-factor` `*` (gem, `Gemfile`)
- `devise_pam_authenticatable2` `9.2` (gem, `Gemfile`)
- `discard` `2.0` (gem, `Gemfile`)
- ... (+286 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod__devcontainer[".devcontainer"]:::atlasCategory
        mod_70293a41_3f23_45a7_8cdf_ea568d8d99f3["70293a41-3f23-45a7-8cdf-ea568d8d99f3"]:::atlasCategory
        mod_streaming["streaming"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_____inputs_file_to_build___["${{ inputs.file_to_build }}"]:::atlasWorkflow
        art__devcontainer_Dockerfile[".devcontainer/Dockerfile"]:::atlasWorkflow
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
        art_docker_compose_yml["docker-compose.yml"]:::atlasWorkflow
        art_streaming_Dockerfile["streaming/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_build_container_image_yml_build_image["build-container-image.yml#build-image"]:::atlasJob
        job_test_ruby_yml_test_e2e["test-ruby.yml#test-e2e"]:::atlasJob
    end
    mod__devcontainer -->|PACKAGED_BY| art__devcontainer_Dockerfile
    mod_70293a41_3f23_45a7_8cdf_ea568d8d99f3 -->|BUILT_BY| job_build_container_image_yml_build_image
    mod_70293a41_3f23_45a7_8cdf_ea568d8d99f3 -->|PACKAGED_BY| art_____inputs_file_to_build___
    mod_70293a41_3f23_45a7_8cdf_ea568d8d99f3 -->|PACKAGED_BY| art_Dockerfile
    mod_70293a41_3f23_45a7_8cdf_ea568d8d99f3 -->|PACKAGED_BY| art_docker_compose_yml
    mod_streaming -->|BUILT_BY| job_test_ruby_yml_test_e2e
    mod_streaming -->|PACKAGED_BY| art_docker_compose_yml
    mod_streaming -->|PACKAGED_BY| art_streaming_Dockerfile
    art_Dockerfile -->|BUILT_BY| job_build_container_image_yml_build_image
```

- `.devcontainer` (code_module) --[PACKAGED_BY]--> `.devcontainer/Dockerfile` (container)
- `70293a41-3f23-45a7-8cdf-ea568d8d99f3` (code_module) --[BUILT_BY]--> `build-container-image.yml#build-image` (ci_job)
- `70293a41-3f23-45a7-8cdf-ea568d8d99f3` (code_module) --[PACKAGED_BY]--> `${{ inputs.file_to_build }}` (container)
- `70293a41-3f23-45a7-8cdf-ea568d8d99f3` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `70293a41-3f23-45a7-8cdf-ea568d8d99f3` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `streaming` (code_module) --[BUILT_BY]--> `test-ruby.yml#test-e2e` (ci_job)
- `streaming` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `streaming` (code_module) --[PACKAGED_BY]--> `streaming/Dockerfile` (container)
- `Dockerfile` (container) --[BUILT_BY]--> `build-container-image.yml#build-image` (ci_job)


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
  pipeline_root(["mastodon/mastodon (22 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (13 workflows · 21 jobs)"]
    direction TB
    subgraph sg_wf_2_Build_container_image_for_PR["Build container image for PR (3 jobs)"]
      direction TB
      wf_2_Build_container_image_for_PR(["Trigger: Build container image for PR"]):::atlasWorkflow
      job_2_compute_suffix["compute-suffix"]:::atlasJob
      job_2_build_image["build-image"]:::atlasJob
      job_2_build_image_streaming["build-image-streaming"]:::atlasJob
      wf_2_Build_container_image_for_PR --> job_2_compute_suffix
      job_2_compute_suffix --> job_2_build_image
      job_2_compute_suffix --> job_2_build_image_streaming
    end
    pipeline_root --> wf_2_Build_container_image_for_PR
    subgraph sg_wf_7_Chromatic["Chromatic (2 jobs)"]
      direction TB
      wf_7_Chromatic(["Trigger: Chromatic"]):::atlasWorkflow
      job_7_pathcheck["pathcheck"]:::atlasJob
      job_7_chromatic["chromatic"]:::atlasJob
      wf_7_Chromatic --> job_7_pathcheck
      job_7_pathcheck --> job_7_chromatic
    end
    pipeline_root --> wf_7_Chromatic
    subgraph sg_wf_21_Ruby_Testing["Ruby Testing (4 jobs)"]
      direction TB
      wf_21_Ruby_Testing(["Trigger: Ruby Testing"]):::atlasWorkflow
      job_21_build["build"]:::atlasJob
      job_21_test["test"]:::atlasJob
      job_21_test_e2e["test-e2e"]:::atlasJob
      wf_21_Ruby_Testing --> job_21_build
      job_21_build --> job_21_test
      job_21_build --> job_21_test_e2e
    end
    pipeline_root --> wf_21_Ruby_Testing
  end
  subgraph sg_grp_1_Scheduled___Manual["Scheduled & Manual (5 workflows · 7 jobs)"]
    direction TB
    subgraph sg_wf_1_Build_nightly_container_image["Build nightly container image (3 jobs)"]
      direction TB
      wf_1_Build_nightly_container_image(["Trigger: Build nightly container image"]):::atlasWorkflow
      job_1_compute_suffix["compute-suffix"]:::atlasJob
      job_1_build_image["build-image"]:::atlasJob
      job_1_build_image_streaming["build-image-streaming"]:::atlasJob
      wf_1_Build_nightly_container_image --> job_1_compute_suffix
      job_1_compute_suffix --> job_1_build_image
      job_1_compute_suffix --> job_1_build_image_streaming
    end
    pipeline_root --> wf_1_Build_nightly_container_image
    subgraph sg_wf_9_Crowdin___Download_translations__stable_branches_["Crowdin / Download translations (stable branches) (1 jobs)"]
      direction TB
      wf_9_Crowdin___Download_translations__stable_branches_(["Trigger: Crowdin / Download translations (stable branches)"]):::atlasWorkflow
      job_9_download_translations_stable["download-translations-stable"]:::atlasJob
      wf_9_Crowdin___Download_translations__stable_branches_ --> job_9_download_translations_stable
    end
    pipeline_root --> wf_9_Crowdin___Download_translations__stable_branches_
    subgraph sg_wf_10_Crowdin___Download_translations["Crowdin / Download translations (1 jobs)"]
      direction TB
      wf_10_Crowdin___Download_translations(["Trigger: Crowdin / Download translations"]):::atlasWorkflow
      job_10_download_translations["download-translations"]:::atlasJob
      wf_10_Crowdin___Download_translations --> job_10_download_translations
    end
    pipeline_root --> wf_10_Crowdin___Download_translations
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (3 workflows · 5 jobs)"]
    direction TB
    subgraph sg_wf_4_Build_security_nightly_container_image["Build security nightly container image (3 jobs)"]
      direction TB
      wf_4_Build_security_nightly_container_image(["Trigger: Build security nightly container image"]):::atlasWorkflow
      job_4_compute_suffix["compute-suffix"]:::atlasJob
      job_4_build_image["build-image"]:::atlasJob
      job_4_build_image_streaming["build-image-streaming"]:::atlasJob
      wf_4_Build_security_nightly_container_image --> job_4_compute_suffix
      job_4_compute_suffix --> job_4_build_image
      job_4_compute_suffix --> job_4_build_image_streaming
    end
    pipeline_root --> wf_4_Build_security_nightly_container_image
    wf_5_Bundler_Audit["Bundler Audit (1 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_5_Bundler_Audit
    wf_8_CodeQL["CodeQL (1 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_8_CodeQL
  end
  subgraph sg_grp_3_Release___Deploy["Release & Deploy (1 workflows · 3 jobs)"]
    direction TB
    wf_3_Build_container_release_images["Build container release images (3 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_3_Build_container_release_images
  end
  wf_more["+12 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
