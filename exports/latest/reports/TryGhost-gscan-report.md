---
title: Architecture — TryGhost/gscan
description: Arc42 and Pipeline report for TryGhost/gscan
---

# Repository Architecture Analysis: TryGhost/gscan

## Metadata
- **SHA**: `afc49bb4b35fb9a6ce39d74b593a8f0075a5d478`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.68
- **avg_cyclomatic_complexity**: 3.52
- **component_count**: 50
- **dead_code_count**: 4
- **dead_code_symbols**: 4 entry(ies)
- **duplication_pct**: 89.51
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 124
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Express / Node API
- **import_edges**: 100 entry(ies)
- **loc**: 19272
- **max_cognitive_complexity**: 36
- **max_cyclomatic_complexity**: 27
- **sloc**: 14910
- **test_file_count**: 647

# Architecture: TryGhost/gscan

## Context
- **Repository**: `TryGhost/gscan`
- **SHA**: `afc49bb4b35fb9a6ce39d74b593a8f0075a5d478`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Express / Node API

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
    repo_root(["TryGhost/gscan (50 components)"]):::atlasRoot
    dir_0_packages["packages (37)"]:::atlasCategory
    repo_root --> dir_0_packages
    sub_0_0_gscan_test["gscan/test (36)"]:::atlasWorkflow
    dir_0_packages --> sub_0_0_gscan_test
    sub_0_1_gscan["gscan (1)"]:::atlasWorkflow
    dir_0_packages --> sub_0_1_gscan
    dir_1_k8s["k8s (9)"]:::atlasCategory
    repo_root --> dir_1_k8s
    sub_1_0_overlays["overlays (5)"]:::atlasWorkflow
    dir_1_k8s --> sub_1_0_overlays
    sub_1_1_base["base (4)"]:::atlasWorkflow
    dir_1_k8s --> sub_1_1_base
    dir_2_apps["apps (3)"]:::atlasCategory
    repo_root --> dir_2_apps
    dir_3__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_3__root_
```

## Component Details
- **@tryghost/gscan-web** (`apps/web/package.json`): MODULE
- **gscan-root** (`package.json`): MODULE
- **gscan** (`packages/gscan/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/bad-config/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/bad-config-2/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/deprecated-engines-ghost-api-v01/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/deprecated-engines-ghost-api-v2/package.json`): MODULE
- **ATheme_test** (`packages/gscan/test/fixtures/themes/010-packagejson/fields-are-invalid/package.json`): MODULE
- **fields-are-missing** (`packages/gscan/test/fixtures/themes/010-packagejson/fields-are-missing/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/fields-are-valid/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/fields-are-valid-v3/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/ghost-api-use/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/invalid-custom-theme/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/no-config/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/010-packagejson/valid-custom-theme/package.json`): MODULE
- **theme** (`packages/gscan/test/fixtures/themes/020-structure/recommendation/package.json`): MODULE
- **valid-card-assets** (`packages/gscan/test/fixtures/themes/050-koenig-css-classes/valid-card-assets/package.json`): MODULE
- **valid-card-assets-exclude** (`packages/gscan/test/fixtures/themes/050-koenig-css-classes/valid-card-assets-exclude/package.json`): MODULE
- **valid-card-assets-exclude-callout** (`packages/gscan/test/fixtures/themes/050-koenig-css-classes/valid-card-assets-exclude-callout/package.json`): MODULE
- **valid-card-assets-include** (`packages/gscan/test/fixtures/themes/050-koenig-css-classes/valid-card-assets-include/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v4/invalid/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v4/invalid-folder/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v4/invalid_all/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v4/mixed/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v4/valid/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v5/invalid-no-empty-translations/package.json`): MODULE
- **my-theme** (`packages/gscan/test/fixtures/themes/080-helper-usage/v5/valid/package.json`): MODULE
- **custom-settings-filter-attribute** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/filter-attribute/package.json`): MODULE
- **custom-settings-filter-attribute-uppercase** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/filter-attribute-uppercase/package.json`): MODULE
- **no-custom-settings** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/no-custom-settings/package.json`): MODULE
- **custom-settings-partial** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/partial/package.json`): MODULE
- **custom-settings-unused** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/unused/package.json`): MODULE
- **custom-settings-valid** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/valid/package.json`): MODULE
- **custom-settings-with-partials** (`packages/gscan/test/fixtures/themes/100-custom-template-settings-usage/with-partials/package.json`): MODULE
- **theme-with-custom-settings** (`packages/gscan/test/fixtures/themes/theme-with-custom-settings/package.json`): MODULE
- **anothertheme** (`packages/gscan/test/fixtures/themes/zip-content/bad-example-folder/package.json`): MODULE
- **ATheme** (`packages/gscan/test/fixtures/themes/zip-content/example/package.json`): MODULE
- **anothertheme** (`packages/gscan/test/fixtures/themes/zip-content/multi-example/theme/theme-name/package.json`): MODULE
- **anothertheme** (`packages/gscan/test/fixtures/themes/zip-content/nested-example/bad-example-folder/package.json`): MODULE
- **GET_root** (`apps/web/index.js`): API_ROUTE
- **POST_root** (`apps/web/index.js`): API_ROUTE
- **deployment** (`k8s/base/deployment.yml`): module
- **kustomization** (`k8s/base/kustomization.yml`): module
- **secret** (`k8s/base/secret.yml`): module
- **service** (`k8s/base/service.yml`): module
- **deployment** (`k8s/overlays/development/deployment.yml`): module
- **kustomization** (`k8s/overlays/development/kustomization.yml`): module
- **deployment** (`k8s/overlays/staging/deployment.yml`): module
- **kustomization** (`k8s/overlays/staging/kustomization.yml`): module
- **secret** (`k8s/overlays/staging/secret.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (68.73/100)
- **Technical Debt Score**: 31.27
- **Estimated Remediation Effort**: 37.22h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 46.92 | 0.20 | avg_cc=3.52, max_cc=27, duplication=89.51%, dead_code=4 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=29, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 58.00 | 0.15 | avg_cognitive=3.68, max_cognitive=36, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `C` | 76.00 | 0.15 | workflows=4, operational_antipatterns=7, parallel_branches=False |
| Security | `B` | 80.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=1 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (89.51) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (36.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (27.0) exceeds policy threshold (20.0).

### Workspace Packages
- **@tryghost/gscan-web** (`apps/web`, react_ts_js, pnpm) -> internal deps: `gscan`
- **gscan** (`packages/gscan`, react_ts_js, pnpm)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 29 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@eslint/compat` `2.1.1` (npm, `package.json`)
- `@eslint/eslintrc` `3.3.7` (npm, `package.json`)
- `@eslint/js` `10.0.1` (npm, `package.json`)
- `@sentry/node` `11.12.0` (npm, `apps/web/package.json`)
- `@tryghost/config` `2.3.22` (npm, `apps/web/package.json`)
- `@tryghost/debug` `2.3.19` (npm, `packages/gscan/package.json`)
- `@tryghost/debug` `2.3.22` (npm, `apps/web/package.json`)
- `@tryghost/errors` `3.4.5` (npm, `packages/gscan/package.json`)
- `@tryghost/errors` `3.4.8` (npm, `apps/web/package.json`)
- `@tryghost/logging` `6.0.5` (npm, `apps/web/package.json`)
- `@tryghost/nql` `0.13.4` (npm, `packages/gscan/package.json`)
- `@tryghost/pretty-cli` `3.4.1` (npm, `packages/gscan/package.json`)
- `@tryghost/pro-ship` `2.0.0` (npm, `packages/gscan/package.json`)
- `@tryghost/server` `3.1.24` (npm, `apps/web/package.json`)
- `@tryghost/zip` `4.0.0` (npm, `packages/gscan/package.json`)
- `@vitest/coverage-v8` `5.1.0` (npm, `package.json`)
- `chalk` `6.0.1` (npm, `packages/gscan/package.json`)
- `eslint` `10.14.0` (npm, `package.json`)
- `eslint-plugin-ghost` `4.0.1` (npm, `package.json`)
- `express` `5.3.0` (npm, `apps/web/package.json`)
- `express-handlebars` `9.0.4` (npm, `apps/web/package.json`)
- `gscan` `*` (npm, `apps/web/package.json`)
- `handlebars` `4.7.10` (npm, `packages/gscan/package.json`)
- `lodash` `4.18.1` (npm, `packages/gscan/package.json`)
- `multer` `2.5.0` (npm, `apps/web/package.json`)
- `nodemon` `3.1.14` (npm, `apps/web/package.json`)
- `semver` `7.8.6` (npm, `packages/gscan/package.json`)
- `validator` `13.0.0` (npm, `packages/gscan/package.json`)
- `vitest` `5.1.0` (npm, `package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_2f76fd23_220f_4d63_b872_3a557d1bac7c["2f76fd23-220f-4d63-b872-3a557d1bac7c"]:::atlasCategory
        mod_apps_web["apps/web"]:::atlasCategory
        mod_k8s_base["k8s/base"]:::atlasCategory
        mod_k8s_overlays_development["k8s/overlays/development"]:::atlasCategory
        mod_k8s_overlays_staging["k8s/overlays/staging"]:::atlasCategory
        mod_packages_gscan["packages/gscan"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
        art_k8s_base_deployment_yml["k8s/base/deployment.yml"]:::atlasWorkflow
        art_k8s_base_kustomization_yml["k8s/base/kustomization.yml"]:::atlasWorkflow
        art_k8s_base_secret_yml["k8s/base/secret.yml"]:::atlasWorkflow
        art_k8s_base_service_yml["k8s/base/service.yml"]:::atlasWorkflow
        art_k8s_overlays_development_deployment_yml["k8s/overlays/development/deployment.yml"]:::atlasWorkflow
        art_k8s_overlays_development_kustomization_yml["k8s/overlays/development/kustomization.yml"]:::atlasWorkflow
        art_k8s_overlays_staging_deployment_yml["k8s/overlays/staging/deployment.yml"]:::atlasWorkflow
        art_k8s_overlays_staging_kustomization_yml["k8s/overlays/staging/kustomization.yml"]:::atlasWorkflow
        art_k8s_overlays_staging_secret_yml["k8s/overlays/staging/secret.yml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_check_links_yml_build["check-links.yml#build"]:::atlasJob
        job_deploy_yml_build_and_push["deploy.yml#build-and-push"]:::atlasJob
        job_publish_yml_publish["publish.yml#publish"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_kubernetes["kubernetes"]:::atlasTarget
    end
    job_deploy_yml_build_and_push -->|DEPLOYS_TO| env_kubernetes
    mod_2f76fd23_220f_4d63_b872_3a557d1bac7c -->|BUILT_BY| job_deploy_yml_build_and_push
    mod_2f76fd23_220f_4d63_b872_3a557d1bac7c -->|PACKAGED_BY| art_Dockerfile
    mod_apps_web -->|PACKAGED_BY| art_Dockerfile
    mod_k8s_base -->|PACKAGED_BY| art_Dockerfile
    mod_k8s_base -->|PACKAGED_BY| art_k8s_base_deployment_yml
    mod_k8s_base -->|PACKAGED_BY| art_k8s_base_kustomization_yml
    mod_k8s_base -->|PACKAGED_BY| art_k8s_base_secret_yml
    mod_k8s_base -->|PACKAGED_BY| art_k8s_base_service_yml
    mod_k8s_base -->|PACKAGED_BY| art_k8s_overlays_development_kustomization_yml
    mod_k8s_base -->|PACKAGED_BY| art_k8s_overlays_staging_kustomization_yml
    mod_k8s_overlays_development -->|PACKAGED_BY| art_Dockerfile
    mod_k8s_overlays_development -->|PACKAGED_BY| art_k8s_overlays_development_deployment_yml
    mod_k8s_overlays_development -->|PACKAGED_BY| art_k8s_overlays_development_kustomization_yml
    mod_k8s_overlays_staging -->|PACKAGED_BY| art_Dockerfile
    mod_k8s_overlays_staging -->|PACKAGED_BY| art_k8s_overlays_staging_deployment_yml
    mod_k8s_overlays_staging -->|PACKAGED_BY| art_k8s_overlays_staging_kustomization_yml
    mod_k8s_overlays_staging -->|PACKAGED_BY| art_k8s_overlays_staging_secret_yml
    mod_packages_gscan -->|BUILT_BY| job_check_links_yml_build
    mod_packages_gscan -->|DEPLOYED_BY| job_publish_yml_publish
    mod_packages_gscan -->|PACKAGED_BY| art_Dockerfile
    mod_packages_gscan -->|PACKAGED_BY| art_k8s_base_deployment_yml
    mod_packages_gscan -->|PACKAGED_BY| art_k8s_base_secret_yml
    mod_packages_gscan -->|PACKAGED_BY| art_k8s_base_service_yml
    mod_packages_gscan -->|PACKAGED_BY| art_k8s_overlays_development_deployment_yml
    mod_packages_gscan -->|PACKAGED_BY| art_k8s_overlays_staging_deployment_yml
    mod_packages_gscan -->|PACKAGED_BY| art_k8s_overlays_staging_secret_yml
    art_Dockerfile -->|BUILT_BY| job_deploy_yml_build_and_push
```

- `deploy.yml#build-and-push` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `2f76fd23-220f-4d63-b872-3a557d1bac7c` (code_module) --[BUILT_BY]--> `deploy.yml#build-and-push` (ci_job)
- `2f76fd23-220f-4d63-b872-3a557d1bac7c` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `apps/web` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `k8s/base/deployment.yml` (iac)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `k8s/base/kustomization.yml` (iac)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `k8s/base/secret.yml` (iac)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `k8s/base/service.yml` (iac)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `k8s/overlays/development/kustomization.yml` (iac)
- `k8s/base` (code_module) --[PACKAGED_BY]--> `k8s/overlays/staging/kustomization.yml` (iac)
- `k8s/overlays/development` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `k8s/overlays/development` (code_module) --[PACKAGED_BY]--> `k8s/overlays/development/deployment.yml` (iac)
- `k8s/overlays/development` (code_module) --[PACKAGED_BY]--> `k8s/overlays/development/kustomization.yml` (iac)
- `k8s/overlays/staging` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `k8s/overlays/staging` (code_module) --[PACKAGED_BY]--> `k8s/overlays/staging/deployment.yml` (iac)
- `k8s/overlays/staging` (code_module) --[PACKAGED_BY]--> `k8s/overlays/staging/kustomization.yml` (iac)
- `k8s/overlays/staging` (code_module) --[PACKAGED_BY]--> `k8s/overlays/staging/secret.yml` (iac)
- `packages/gscan` (code_module) --[BUILT_BY]--> `check-links.yml#build` (ci_job)
- `packages/gscan` (code_module) --[DEPLOYED_BY]--> `publish.yml#publish` (ci_job)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `k8s/base/deployment.yml` (iac)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `k8s/base/secret.yml` (iac)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `k8s/base/service.yml` (iac)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `k8s/overlays/development/deployment.yml` (iac)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `k8s/overlays/staging/deployment.yml` (iac)
- `packages/gscan` (code_module) --[PACKAGED_BY]--> `k8s/overlays/staging/secret.yml` (iac)
- `Dockerfile` (container) --[BUILT_BY]--> `deploy.yml#build-and-push` (ci_job)


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
  pipeline_root(["TryGhost/gscan (4 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Release___Deploy["Release & Deploy (2 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_2_Deploy["Deploy (1 jobs)"]
      direction TB
      wf_2_Deploy(["Trigger: Deploy"]):::atlasWorkflow
      job_2_build_and_push["build-and-push"]:::atlasJob
      wf_2_Deploy --> job_2_build_and_push
    end
    pipeline_root --> wf_2_Deploy
    subgraph sg_wf_3_Publish["Publish (2 jobs)"]
      direction TB
      wf_3_Publish(["Trigger: Publish"]):::atlasWorkflow
      job_3_test["test"]:::atlasJob
      job_3_publish["publish"]:::atlasJob
      wf_3_Publish --> job_3_test
      job_3_test --> job_3_publish
    end
    pipeline_root --> wf_3_Publish
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (1 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_1_CI["CI (2 jobs)"]
      direction TB
      wf_1_CI(["Trigger: CI"]):::atlasWorkflow
      job_1_test["test"]:::atlasJob
      job_1_required_checks_pass["required-checks-pass"]:::atlasJob
      wf_1_CI --> job_1_test
      job_1_test --> job_1_required_checks_pass
    end
    pipeline_root --> wf_1_CI
  end
  subgraph sg_grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_0_Check_Links["Check Links (1 jobs)"]
      direction TB
      wf_0_Check_Links(["Trigger: Check Links"]):::atlasWorkflow
      job_0_build["build"]:::atlasJob
      wf_0_Check_Links --> job_0_build
    end
    pipeline_root --> wf_0_Check_Links
  end
```
