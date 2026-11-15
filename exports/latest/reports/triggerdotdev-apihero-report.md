---
title: Architecture — triggerdotdev/apihero
description: Arc42 and Pipeline report for triggerdotdev/apihero
---

# Repository Architecture Analysis: triggerdotdev/apihero

## Metadata
- **SHA**: `2f204e8fc57343a584d8b244d7ad492b72ed1242`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 2.07
- **avg_cyclomatic_complexity**: 2.59
- **component_count**: 232
- **dead_code_count**: 9
- **dead_code_symbols**: 9 entry(ies)
- **duplication_pct**: 81.35
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 361
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Next.js
- **import_edges**: 100 entry(ies)
- **loc**: 29644
- **max_cognitive_complexity**: 53
- **max_cyclomatic_complexity**: 34
- **sloc**: 25724
- **test_file_count**: 48

# Architecture: triggerdotdev/apihero

## Context
- **Repository**: `triggerdotdev/apihero`
- **SHA**: `2f204e8fc57343a584d8b244d7ad492b72ed1242`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Next.js

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
    repo_root(["triggerdotdev/apihero (232 components)"]):::atlasRoot
    dir_0_apps["apps (164)"]:::atlasCategory
    repo_root --> dir_0_apps
    sub_0_0_webapp["webapp (161)"]:::atlasWorkflow
    dir_0_apps --> sub_0_0_webapp
    sub_0_1_proxy["proxy (2)"]:::atlasWorkflow
    dir_0_apps --> sub_0_1_proxy
    sub_0_2_logs["logs (1)"]:::atlasWorkflow
    dir_0_apps --> sub_0_2_logs
    dir_1_packages["packages (55)"]:::atlasCategory
    repo_root --> dir_1_packages
    sub_1_0_interceptors_js["interceptors-js (27)"]:::atlasWorkflow
    dir_1_packages --> sub_1_0_interceptors_js
    sub_1_1_apihero_node["apihero-node (12)"]:::atlasWorkflow
    dir_1_packages --> sub_1_1_apihero_node
    sub_1_2_apihero_browser["apihero-browser (10)"]:::atlasWorkflow
    dir_1_packages --> sub_1_2_apihero_browser
    sub_1_more["+3 more submodules (6)"]:::atlasMore
    dir_1_packages --> sub_1_more
    dir_2_examples["examples (7)"]:::atlasCategory
    repo_root --> dir_2_examples
    dir_3_config_packages["config-packages (5)"]:::atlasCategory
    repo_root --> dir_3_config_packages
    dir_4__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_4__root_
    sub_1_1_apihero_node -.->|"9 deps"| sub_1_0_interceptors_js
    sub_1_2_apihero_browser -.->|"3 deps"| sub_1_0_interceptors_js
    sub_1_2_apihero_browser -.->|"1 dep"| sub_1_1_apihero_node
```

## Component Details

Showing top 60 representative components out of 232 across 5 module group(s):

- **Module `apps`** (164 components — UI_COMPONENT: 160, MODULE: 3, SERVICE: 1)
- **Module `packages`** (55 components — API_ROUTE: 49, MODULE: 6)
- **Module `examples`** (7 components — UI_COMPONENT: 4, MODULE: 2, API_ROUTE: 1)
- **Module `config-packages`** (5 components — MODULE: 5)
- **Module `(root)`** (1 components — MODULE: 1)

- **CountdownToRefreshButton** (`apps/webapp/app/libraries/ui/src/components/LogsOnboarding.tsx`): UI_COMPONENT (deps: CopyTextButton, DestructiveButton, PrimaryA, PrimaryButton, PrimaryLink, SecondaryA (+5 more))
- **LogsFilters** (`apps/webapp/app/libraries/ui/src/components/LogsFilters.tsx`): UI_COMPONENT (deps: ComboBox, FormField, Input, MultipleComboBox, SingleComboBox, StatusCode (+5 more))
- **LogsOnboarding** (`apps/webapp/app/libraries/ui/src/components/LogsOnboarding.tsx`): UI_COMPONENT (deps: CopyTextButton, DestructiveButton, PrimaryA, PrimaryButton, PrimaryLink, SecondaryA (+5 more))
- **OperationIndexRoute** (`apps/webapp/app/routes/admin/operations/$operationId/index.tsx`): UI_COMPONENT (deps: ModelRoute, SchemaOperationClientRoute, SchemaOperationLayoutRoute, Tabs)
- **ApiSchemaDetailsRoute** (`apps/webapp/app/routes/admin/schemas/$id/index.tsx`): UI_COMPONENT (deps: ApiIntegrationIdRoute, ApiSchemaIdRoute, Tabs)
- **EditIntegrationRoute** (`apps/webapp/app/routes/admin/integrations/$id/edit.tsx`): UI_COMPONENT (deps: ApiIntegrationIdRoute, ApiSchemaIdRoute, Tabs)
- **Header** (`apps/webapp/app/libraries/ui/src/components/Header.tsx`): UI_COMPONENT (deps: FeedbackMenu, Logo, UserProfileMenu)
- **IntegrationDetailsRoute** (`apps/webapp/app/routes/admin/integrations/$id/index.tsx`): UI_COMPONENT (deps: ApiIntegrationIdRoute, ApiSchemaIdRoute, Tabs)
- **ReleaseRoute** (`apps/webapp/app/routes/admin/schemas/$id/releases/$releaseId.tsx`): UI_COMPONENT (deps: ApiIntegrationIdRoute, ApiSchemaIdRoute, Tabs)
- **SchemaDocumentRoute** (`apps/webapp/app/routes/admin/schemas/$id/document.tsx`): UI_COMPONENT (deps: ApiIntegrationIdRoute, ApiSchemaIdRoute, Tabs)
- **HTTPMethodLabel** (`apps/webapp/app/libraries/common/src/components/HTTPMethod.tsx`): UI_COMPONENT (deps: ModelRoute, SchemaOperationClientRoute)
- **ProjectKey** (`apps/webapp/app/libraries/ui/src/components/ProjectKey.tsx`): UI_COMPONENT (deps: CopyTextButton, Label)
- **WorkspaceMenu** (`apps/webapp/app/libraries/ui/src/components/WorkspaceMenu.tsx`): UI_COMPONENT (deps: ModelRoute, SchemaOperationClientRoute)
- **CopyTextButton** (`apps/webapp/app/libraries/ui/src/components/Buttons/CopyTextButton.tsx`): UI_COMPONENT (deps: CopyText)
- **CopyTextButton** (`apps/webapp/app/libraries/ui/src/components/CopyTextButton.tsx`): UI_COMPONENT (deps: CopyText)
- **DELETE_delete** (`packages/apihero-browser/test/browser/setupWorker.test.ts`): API_ROUTE (deps: GET_root)
- **FormField** (`apps/webapp/app/libraries/ui/src/components/Primitives/FormField.tsx`): UI_COMPONENT (deps: Label)
- **GET_get** (`packages/apihero-browser/test/browser/setupWorker.noAllow.test.ts`): API_ROUTE (deps: GET_root)
- **GET_get** (`packages/apihero-browser/test/browser/setupWorker.test.ts`): API_ROUTE (deps: GET_root)
- **GET_get** (`packages/apihero-fetch/test/createFetchProxy.test.ts`): API_ROUTE (deps: GET_root)
- **GET_get** (`packages/apihero-node/test/node/fetch.allow.test.ts`): API_ROUTE (deps: GET_root)
- **GET_get** (`packages/apihero-node/test/node/fetch.deny.test.ts`): API_ROUTE (deps: GET_root)
- **GET_get** (`packages/apihero-node/test/node/fetch.native.test.ts`): API_ROUTE (deps: GET_root)
- **GET_get** (`packages/apihero-node/test/node/fetch.test.ts`): API_ROUTE (deps: GET_root)
- **GET_proxyServiceWorker.js** (`packages/apihero-browser/test/vitest.setup.ts`): API_ROUTE (deps: POST_console_:messageType)
- **Home** (`examples/next-github-stars/pages/index.tsx`): UI_COMPONENT (deps: Main)
- **InfoPanel** (`apps/webapp/app/libraries/ui/src/components/InfoPanel.tsx`): UI_COMPONENT (deps: ApiLogoContainer)
- **LogsTable** (`apps/webapp/app/libraries/logging/LogsTable.tsx`): UI_COMPONENT (deps: LogRow)
- **Main** (`examples/next-github-stars/components/Main.tsx`): UI_COMPONENT (deps: StarCount)
- **NavBar** (`apps/webapp/app/libraries/ui/src/components/NavBar.tsx`): UI_COMPONENT (deps: Breadcrumb)
- **PATCH_patch** (`packages/apihero-browser/test/browser/setupWorker.test.ts`): API_ROUTE (deps: GET_root)
- **POST_console_:messageType** (`packages/apihero-browser/test/support/workerConsole.ts`): API_ROUTE (deps: GET_root)
- **POST_console_:messageType** (`packages/apihero-node/test/support/workerConsole.ts`): API_ROUTE (deps: GET_root)
- **POST_post** (`packages/apihero-browser/test/browser/setupWorker.test.ts`): API_ROUTE (deps: GET_root)
- **POST_post** (`packages/apihero-fetch/test/createFetchProxy.test.ts`): API_ROUTE (deps: GET_root)
- **POST_post** (`packages/apihero-node/test/node/fetch.allow.test.ts`): API_ROUTE (deps: GET_root)
- **POST_post** (`packages/apihero-node/test/node/fetch.deny.test.ts`): API_ROUTE (deps: GET_root)
- **POST_post** (`packages/apihero-node/test/node/fetch.native.test.ts`): API_ROUTE (deps: GET_root)
- **POST_post** (`packages/apihero-node/test/node/fetch.test.ts`): API_ROUTE (deps: GET_root)
- **POST_v3_apihero.run_messages** (`packages/apihero-node/test/node/fetch.allow.test.ts`): API_ROUTE (deps: GET_root)
- **PUT_put** (`packages/apihero-browser/test/browser/setupWorker.test.ts`): API_ROUTE (deps: GET_root)
- **PanelHeader** (`apps/webapp/app/libraries/ui/src/components/Panel/PanelHeader.tsx`): UI_COMPONENT (deps: SmallTitle)
- **RequestResponseViewer** (`apps/webapp/app/libraries/request-response-viewer/src/RequestResponseViewer.tsx`): UI_COMPONENT (deps: RequestViewer)
- **RequestUrlBar** (`apps/webapp/app/libraries/request-response-viewer/src/RequestResponseViewer.tsx`): UI_COMPONENT (deps: RequestViewer)
- **ResponseInfo** (`apps/webapp/app/libraries/ui/src/components/ResponseInfo.tsx`): UI_COMPONENT (deps: StatusCode)
- **UserProfileMenu** (`apps/webapp/app/libraries/ui/src/components/UserProfileMenu.tsx`): UI_COMPONENT (deps: UserProfilePhoto)
- **@apihero/browser** (`packages/apihero-browser/package.json`): MODULE
- **@apihero/eslint-config-vite** (`config-packages/eslint-config-vite/package.json`): MODULE
- **@apihero/fetch** (`packages/apihero-fetch/package.json`): MODULE
- **@apihero/interceptors-js** (`packages/interceptors-js/package.json`): MODULE
- **@apihero/node** (`packages/apihero-node/package.json`): MODULE
- **@apihero/tailwind-config** (`config-packages/tailwind-config/package.json`): MODULE
- **@apihero/tsconfig** (`config-packages/tsconfig/package.json`): MODULE
- **@examples/fetch-load-test** (`examples/fetch-load-test/package.json`): MODULE
- **@examples/next-github-stars** (`examples/next-github-stars/package.json`): MODULE
- **APIHeroProvider** (`apps/webapp/app/libraries/client/src/react.tsx`): UI_COMPONENT
- **API_api_hello** (`examples/next-github-stars/pages/api/hello.ts`): API_ROUTE
- **AdminDashboardRoute** (`apps/webapp/app/routes/admin/index.tsx`): UI_COMPONENT
- **Alerts** (`apps/webapp/app/routes/__app/workspaces/$workspaceSlug/projects/$projectSlug/alerts/index.tsx`): UI_COMPONENT
- **ApiIntegrationIdRoute** (`apps/webapp/app/routes/admin/integrations/$id.tsx`): UI_COMPONENT

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (41.35/100)
- **Technical Debt Score**: 58.65
- **Estimated Remediation Effort**: 109.18h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 32.00 | 0.20 | avg_cc=2.59, max_cc=34, duplication=81.35%, dead_code=9 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=2505, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=2.07, max_cognitive=53, fitness_violations=3, oversized_files=4 |
| Pipeline Health | `F` | 26.00 | 0.15 | workflows=3, operational_antipatterns=13, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=2, pipeline_security_findings=34 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (81.35) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (53.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (34.0) exceeds policy threshold (20.0).

### Workspace Packages
- **logs** (`apps/logs`, react_ts_js, pnpm) -> internal deps: `internal-logs`
- **proxy** (`apps/proxy`, react_ts_js, pnpm) -> internal deps: `internal-logs`
- **webapp** (`apps/webapp`, react_ts_js, pnpm) -> internal deps: `@apihero/node, @apihero/tailwind-config, internal-logs`
- **eslint-config-custom** (`config-packages/eslint-config-custom`, react_ts_js, pnpm)
- **eslint-config-custom-next** (`config-packages/eslint-config-custom-next`, react_ts_js, pnpm)
- **@apihero/eslint-config-vite** (`config-packages/eslint-config-vite`, react_ts_js, pnpm)
- **@apihero/tailwind-config** (`config-packages/tailwind-config`, react_ts_js, pnpm)
- **@apihero/tsconfig** (`config-packages/tsconfig`, react_ts_js, pnpm)
- **@examples/fetch-load-test** (`examples/fetch-load-test`, react_ts_js, pnpm) -> internal deps: `@apihero/node, @apihero/tsconfig`
- **@examples/next-github-stars** (`examples/next-github-stars`, react_ts_js, pnpm) -> internal deps: `@apihero/browser, @apihero/node`
- **@apihero/browser** (`packages/apihero-browser`, react_ts_js, pnpm) -> internal deps: `@apihero/eslint-config-vite, @apihero/tsconfig`
- **@apihero/fetch** (`packages/apihero-fetch`, react_ts_js, pnpm) -> internal deps: `@apihero/eslint-config-vite, @apihero/tsconfig, internal-constants`
- **@apihero/node** (`packages/apihero-node`, react_ts_js, pnpm) -> internal deps: `@apihero/eslint-config-vite, @apihero/interceptors-js, @apihero/tsconfig, internal-constants`
- **@apihero/interceptors-js** (`packages/interceptors-js`, react_ts_js, pnpm) -> internal deps: `@apihero/eslint-config-vite, @apihero/tsconfig`
- **internal-constants** (`packages/internal-constants`, react_ts_js, pnpm)
- **internal-logs** (`packages/internal-logs`, react_ts_js, pnpm) -> internal deps: `@apihero/eslint-config-vite, @apihero/tsconfig`

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 2505 | **Vulnerabilities**: 0 | **Secrets**: 2

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `packages/apihero-browser/test/support/certs/key.pem:1` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `packages/apihero-node/test/support/certs/key.pem:1` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `@apihero/browser` `*` (npm, `examples/next-github-stars/package.json`)
- `@apihero/eslint-config-vite` `*` (npm, `packages/apihero-browser/package.json`)
- `@apihero/eslint-config-vite` `*` (npm, `packages/apihero-fetch/package.json`)
- `@apihero/eslint-config-vite` `*` (npm, `packages/apihero-node/package.json`)
- `@apihero/eslint-config-vite` `*` (npm, `packages/interceptors-js/package.json`)
- `@apihero/eslint-config-vite` `*` (npm, `packages/internal-logs/package.json`)
- `@apihero/interceptors-js` `*` (npm, `packages/apihero-node/package.json`)
- `@apihero/node` `*` (npm, `apps/webapp/package.json`)
- `@apihero/node` `*` (npm, `examples/fetch-load-test/package.json`)
- `@apihero/node` `*` (npm, `examples/next-github-stars/package.json`)
- `@apihero/openapi-spec-generator` `0.1.6` (npm, `apps/webapp/package.json`)
- `@apihero/openapi-spec-generator` `0.1.6` (npm, `pnpm-lock.yaml`)
- `@apihero/tailwind-config` `*` (npm, `apps/webapp/package.json`)
- `@apihero/tsconfig` `*` (npm, `examples/fetch-load-test/package.json`)
- `@apihero/tsconfig` `*` (npm, `packages/apihero-browser/package.json`)
- `@apihero/tsconfig` `*` (npm, `packages/apihero-fetch/package.json`)
- `@apihero/tsconfig` `*` (npm, `packages/apihero-node/package.json`)
- `@apihero/tsconfig` `*` (npm, `packages/interceptors-js/package.json`)
- `@apihero/tsconfig` `*` (npm, `packages/internal-logs/package.json`)
- `@aws-sdk/client-s3` `3.186.0` (npm, `apps/webapp/package.json`)
- `@aws-sdk/client-s3` `3.188.0` (npm, `pnpm-lock.yaml`)
- `@aws-sdk/s3-request-presigner` `3.186.0` (npm, `apps/webapp/package.json`)
- `@aws-sdk/s3-request-presigner` `3.188.0` (npm, `pnpm-lock.yaml`)
- `@cfworker/json-schema` `1.12.4` (npm, `apps/webapp/package.json`)
- `@cfworker/json-schema` `1.12.5` (npm, `pnpm-lock.yaml`)
- `@changesets/cli` `2.25.2` (npm, `package.json`)
- `@changesets/cli` `2.25.2` (npm, `pnpm-lock.yaml`)
- `@cloudflare/workers-types` `3.18.0` (npm, `apps/proxy/package.json`)
- `@cloudflare/workers-types` `3.18.0` (npm, `pnpm-lock.yaml`)
- `@codemirror/autocomplete` `6.3.1` (npm, `apps/webapp/package.json`)
- ... (+2475 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_a93ce632_2141_4e29_8d3e_118b1500489f["a93ce632-2141-4e29-8d3e-118b1500489f"]:::atlasCategory
        mod_apps_logs["apps/logs"]:::atlasCategory
        mod_apps_logs_test["apps/logs/test"]:::atlasCategory
        mod_apps_proxy_test["apps/proxy/test"]:::atlasCategory
        mod_apps_webapp["apps/webapp"]:::atlasCategory
        mod_packages_apihero_node["packages/apihero-node"]:::atlasCategory
        mod_packages_internal_logs["packages/internal-logs"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_apps_logs_Dockerfile["apps/logs/Dockerfile"]:::atlasWorkflow
        art_apps_logs_fly_toml["apps/logs/fly.toml"]:::atlasWorkflow
        art_apps_webapp_Dockerfile["apps/webapp/Dockerfile"]:::atlasWorkflow
        art_apps_webapp_fly_toml["apps/webapp/fly.toml"]:::atlasWorkflow
        art_docker_compose_ci_yml["docker-compose-ci.yml"]:::atlasWorkflow
        art_docker_compose_yml["docker-compose.yml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_logs_yml_build["logs.yml#build"]:::atlasJob
        job_logs_yml_deploy["logs.yml#deploy"]:::atlasJob
        job_webapp_yml_build["webapp.yml#build"]:::atlasJob
        job_webapp_yml_deploy["webapp.yml#deploy"]:::atlasJob
    end
    mod_a93ce632_2141_4e29_8d3e_118b1500489f -->|BUILT_BY| job_logs_yml_build
    mod_a93ce632_2141_4e29_8d3e_118b1500489f -->|BUILT_BY| job_webapp_yml_build
    mod_a93ce632_2141_4e29_8d3e_118b1500489f -->|PACKAGED_BY| art_docker_compose_ci_yml
    mod_a93ce632_2141_4e29_8d3e_118b1500489f -->|PACKAGED_BY| art_docker_compose_yml
    mod_apps_logs -->|BUILT_BY| job_logs_yml_build
    mod_apps_logs -->|DEPLOYED_BY| job_logs_yml_deploy
    mod_apps_logs -->|PACKAGED_BY| art_apps_logs_Dockerfile
    mod_apps_logs -->|PACKAGED_BY| art_apps_logs_fly_toml
    mod_apps_logs -->|PACKAGED_BY| art_apps_webapp_Dockerfile
    mod_apps_logs -->|PACKAGED_BY| art_docker_compose_yml
    mod_apps_logs_test -->|PACKAGED_BY| art_docker_compose_ci_yml
    mod_apps_logs_test -->|PACKAGED_BY| art_docker_compose_yml
    mod_apps_proxy_test -->|PACKAGED_BY| art_docker_compose_ci_yml
    mod_apps_proxy_test -->|PACKAGED_BY| art_docker_compose_yml
    mod_apps_webapp -->|BUILT_BY| job_webapp_yml_build
    mod_apps_webapp -->|DEPLOYED_BY| job_webapp_yml_deploy
    mod_apps_webapp -->|PACKAGED_BY| art_apps_webapp_Dockerfile
    mod_apps_webapp -->|PACKAGED_BY| art_apps_webapp_fly_toml
    mod_packages_apihero_node -->|PACKAGED_BY| art_apps_webapp_Dockerfile
    mod_packages_internal_logs -->|PACKAGED_BY| art_apps_logs_Dockerfile
    mod_packages_internal_logs -->|PACKAGED_BY| art_apps_webapp_Dockerfile
    art_apps_logs_Dockerfile -->|BUILT_BY| job_logs_yml_build
    art_apps_webapp_Dockerfile -->|BUILT_BY| job_webapp_yml_build
```

- `a93ce632-2141-4e29-8d3e-118b1500489f` (code_module) --[BUILT_BY]--> `logs.yml#build` (ci_job)
- `a93ce632-2141-4e29-8d3e-118b1500489f` (code_module) --[BUILT_BY]--> `webapp.yml#build` (ci_job)
- `a93ce632-2141-4e29-8d3e-118b1500489f` (code_module) --[PACKAGED_BY]--> `docker-compose-ci.yml` (container)
- `a93ce632-2141-4e29-8d3e-118b1500489f` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `apps/logs` (code_module) --[BUILT_BY]--> `logs.yml#build` (ci_job)
- `apps/logs` (code_module) --[DEPLOYED_BY]--> `logs.yml#deploy` (ci_job)
- `apps/logs` (code_module) --[PACKAGED_BY]--> `apps/logs/Dockerfile` (container)
- `apps/logs` (code_module) --[PACKAGED_BY]--> `apps/logs/fly.toml` (container)
- `apps/logs` (code_module) --[PACKAGED_BY]--> `apps/webapp/Dockerfile` (container)
- `apps/logs` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `apps/logs/test` (code_module) --[PACKAGED_BY]--> `docker-compose-ci.yml` (container)
- `apps/logs/test` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `apps/proxy/test` (code_module) --[PACKAGED_BY]--> `docker-compose-ci.yml` (container)
- `apps/proxy/test` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `apps/webapp` (code_module) --[BUILT_BY]--> `webapp.yml#build` (ci_job)
- `apps/webapp` (code_module) --[DEPLOYED_BY]--> `webapp.yml#deploy` (ci_job)
- `apps/webapp` (code_module) --[PACKAGED_BY]--> `apps/webapp/Dockerfile` (container)
- `apps/webapp` (code_module) --[PACKAGED_BY]--> `apps/webapp/fly.toml` (container)
- `packages/apihero-node` (code_module) --[PACKAGED_BY]--> `apps/webapp/Dockerfile` (container)
- `packages/internal-logs` (code_module) --[PACKAGED_BY]--> `apps/logs/Dockerfile` (container)
- `packages/internal-logs` (code_module) --[PACKAGED_BY]--> `apps/webapp/Dockerfile` (container)
- `apps/logs/Dockerfile` (container) --[BUILT_BY]--> `logs.yml#build` (ci_job)
- `apps/webapp/Dockerfile` (container) --[BUILT_BY]--> `webapp.yml#build` (ci_job)


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
  pipeline_root(["triggerdotdev/apihero"]):::atlasRoot
  subgraph __Logs_CI_0["🚀 Logs CI"]
    direction TB
    0_lint["lint"]:::atlasJob
    0_typecheck["typecheck"]:::atlasJob
    0_build["build"]:::atlasJob
    0_deploy["deploy"]:::atlasJob
    0_lint --> 0_deploy
    0_typecheck --> 0_deploy
    0_build --> 0_deploy
    wf_entry_0(["Trigger: 🚀 Logs CI"]):::atlasWorkflow
    wf_entry_0 --> 0_lint
    wf_entry_0 --> 0_typecheck
    wf_entry_0 --> 0_build
  end
  pipeline_root --> wf_entry_0
  subgraph __Deploy_Proxy_1["🚀 Deploy Proxy"]
    direction TB
    1_typecheck["typecheck"]:::atlasJob
    1_tests["tests"]:::atlasJob
    1_deploy["deploy"]:::atlasJob
    1_typecheck --> 1_deploy
    1_tests --> 1_deploy
  end
  pipeline_root --> 1_typecheck
  subgraph __WebApp_CI_2["🚀 WebApp CI"]
    direction TB
    2_lint["lint"]:::atlasJob
    2_typecheck["typecheck"]:::atlasJob
    2_build["build"]:::atlasJob
    2_deploy["deploy"]:::atlasJob
    2_lint --> 2_deploy
    2_typecheck --> 2_deploy
    2_build --> 2_deploy
    wf_entry_2(["Trigger: 🚀 WebApp CI"]):::atlasWorkflow
    wf_entry_2 --> 2_lint
    wf_entry_2 --> 2_typecheck
    wf_entry_2 --> 2_build
  end
  pipeline_root --> wf_entry_2
```
