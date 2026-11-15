---
title: Architecture — backstage/demo
description: Arc42 and Pipeline report for backstage/demo
---

# Repository Architecture Analysis: backstage/demo

## Metadata
- **SHA**: `5c798227dd84439b7ebc7454321e29a5eb3200ec`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.63
- **avg_cyclomatic_complexity**: 1.56
- **component_count**: 15
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 58.75
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 49
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: React (Vite)
- **import_edges**: 100 entry(ies)
- **loc**: 1784
- **max_cognitive_complexity**: 5
- **max_cyclomatic_complexity**: 6
- **sloc**: 1514
- **test_file_count**: 2

# Architecture: backstage/demo

## Context
- **Repository**: `backstage/demo`
- **SHA**: `5c798227dd84439b7ebc7454321e29a5eb3200ec`
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
    root["root : MODULE"]:::atlasJob
    app["app : MODULE"]:::atlasJob
    backend["backend : MODULE"]:::atlasJob
    _internal_plugin_catalog_backend_module_example_processor["@internal/plugin-catalog-backend-module-example-processor : MODULE"]:::atlasJob
    _internal_plugin_notifications_tester_backend["@internal/plugin-notifications-tester-backend : MODULE"]:::atlasJob
    ApertureLogoFull["ApertureLogoFull : UI_COMPONENT"]:::atlasJob
    ApertureLogoIcon["ApertureLogoIcon : UI_COMPONENT"]:::atlasJob
    SidebarContent["SidebarContent : UI_COMPONENT"]:::atlasJob
    SidebarLogo["SidebarLogo : UI_COMPONENT"]:::atlasJob
    NotificationSettings["NotificationSettings : UI_COMPONENT"]:::atlasJob
    POST_test["POST_test : API_ROUTE"]:::atlasJob
    docker_compose["docker-compose : module"]:::atlasJob
    prometheus["prometheus : module"]:::atlasJob
    dashboards["dashboards : module"]:::atlasJob
    prometheus_datasource["prometheus-datasource : module"]:::atlasJob
    repo_root(["backstage/demo"]):::atlasRoot
    repo_root --> NotificationSettings
    repo_root --> POST_test
    repo_root --> _internal_plugin_catalog_backend_module_example_processor
    repo_root --> _internal_plugin_notifications_tester_backend
    repo_root --> app
    repo_root --> backend
    repo_root --> dashboards
    repo_root --> docker_compose
    repo_root --> prometheus
    repo_root --> prometheus_datasource
    repo_root --> root
    SidebarContent --> SidebarLogo
    SidebarLogo --> ApertureLogoFull
    SidebarLogo --> ApertureLogoIcon
```

## Component Details
- **root** (`package.json`): MODULE
- **app** (`packages/app/package.json`): MODULE
- **backend** (`packages/backend/package.json`): MODULE
- **@internal/plugin-catalog-backend-module-example-processor** (`plugins/catalog-backend-module-example-processor/package.json`): MODULE
- **@internal/plugin-notifications-tester-backend** (`plugins/notifications-tester-backend/package.json`): MODULE
- **ApertureLogoFull** (`packages/app/src/components/Root/ApertureLogoFull.tsx`): UI_COMPONENT
- **ApertureLogoIcon** (`packages/app/src/components/Root/ApertureLogoIcon.tsx`): UI_COMPONENT
- **SidebarContent** (`packages/app/src/components/Root/Sidebar.tsx`): UI_COMPONENT (deps: SidebarLogo)
- **SidebarLogo** (`packages/app/src/components/Root/SidebarLogo.tsx`): UI_COMPONENT (deps: ApertureLogoFull, ApertureLogoIcon)
- **NotificationSettings** (`packages/app/src/components/settings/NotificationSettings.tsx`): UI_COMPONENT
- **POST_test** (`plugins/notifications-tester-backend/src/router.ts`): API_ROUTE
- **docker-compose** (`open-telemetry/docker-compose.yaml`): module
- **prometheus** (`open-telemetry/prometheus.yml`): module
- **dashboards** (`open-telemetry/dashboards/dashboards.yml`): module
- **prometheus-datasource** (`open-telemetry/datasources/prometheus-datasource.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (68.60/100)
- **Technical Debt Score**: 31.40
- **Estimated Remediation Effort**: 34.60h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `C` | 75.00 | 0.20 | avg_cc=1.56, max_cc=6, duplication=58.75%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=124, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 94.00 | 0.15 | avg_cognitive=0.63, max_cognitive=5, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `F` | 39.00 | 0.15 | workflows=5, operational_antipatterns=8, parallel_branches=False |
| Security | `F` | 52.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=4 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (58.75) exceeds policy threshold (15.0).

### Workspace Packages
- **app** (`packages/app`, react_ts_js, yarn)
- **backend** (`packages/backend`, react_ts_js, yarn) -> internal deps: `@internal/plugin-catalog-backend-module-example-processor, @internal/plugin-notifications-tester-backend, app`
- **@internal/plugin-catalog-backend-module-example-processor** (`plugins/catalog-backend-module-example-processor`, react_ts_js, yarn)
- **@internal/plugin-notifications-tester-backend** (`plugins/notifications-tester-backend`, react_ts_js, yarn)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 124 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@backstage-community/plugin-badges` `1.0.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-badges-backend` `0.28.0` (npm, `packages/backend/package.json`)
- `@backstage-community/plugin-cost-insights` `0.32.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-explore` `1.0.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-explore-backend` `0.16.0` (npm, `packages/backend/package.json`)
- `@backstage-community/plugin-github-actions` `1.0.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-graphiql` `0.21.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-search-backend-module-explore` `0.11.0` (npm, `packages/backend/package.json`)
- `@backstage-community/plugin-tech-radar` `1.6.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-todo` `0.26.0` (npm, `packages/app/package.json`)
- `@backstage-community/plugin-todo-backend` `0.27.0` (npm, `packages/backend/package.json`)
- `@backstage/backend-defaults` `*` (npm, `packages/backend/package.json`)
- `@backstage/backend-plugin-api` `*` (npm, `packages/backend/package.json`)
- `@backstage/backend-plugin-api` `*` (npm, `plugins/catalog-backend-module-example-processor/package.json`)
- `@backstage/backend-plugin-api` `*` (npm, `plugins/notifications-tester-backend/package.json`)
- `@backstage/catalog-model` `*` (npm, `plugins/catalog-backend-module-example-processor/package.json`)
- `@backstage/cli` `*` (npm, `package.json`)
- `@backstage/cli` `*` (npm, `packages/app/package.json`)
- `@backstage/cli` `*` (npm, `packages/backend/package.json`)
- `@backstage/cli` `*` (npm, `plugins/catalog-backend-module-example-processor/package.json`)
- `@backstage/cli` `*` (npm, `plugins/notifications-tester-backend/package.json`)
- `@backstage/cli-defaults` `*` (npm, `package.json`)
- `@backstage/config` `*` (npm, `plugins/notifications-tester-backend/package.json`)
- `@backstage/core-app-api` `*` (npm, `packages/app/package.json`)
- `@backstage/core-compat-api` `*` (npm, `packages/app/package.json`)
- `@backstage/core-components` `*` (npm, `packages/app/package.json`)
- `@backstage/core-plugin-api` `*` (npm, `packages/app/package.json`)
- `@backstage/e2e-test-utils` `*` (npm, `package.json`)
- `@backstage/frontend-defaults` `*` (npm, `packages/app/package.json`)
- `@backstage/frontend-plugin-api` `*` (npm, `packages/app/package.json`)
- ... (+94 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_8ab86fc0_d7fd_4ce5_9892_4f044a7c8571["8ab86fc0-d7fd-4ce5-9892-4f044a7c8571"]:::atlasCategory
        mod_open_telemetry["open-telemetry"]:::atlasCategory
        mod_packages_app["packages/app"]:::atlasCategory
        mod_packages_backend["packages/backend"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
        art_open_telemetry_docker_compose_yaml["open-telemetry/docker-compose.yaml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_pages_yml_deploy["pages.yml#deploy"]:::atlasJob
        job_pull_yml_build["pull.yml#build"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_github_pages["github-pages"]:::atlasTarget
    end
    job_pages_yml_deploy -->|DEPLOYS_TO| env_github_pages
    mod_8ab86fc0_d7fd_4ce5_9892_4f044a7c8571 -->|BUILT_BY| job_pull_yml_build
    mod_8ab86fc0_d7fd_4ce5_9892_4f044a7c8571 -->|PACKAGED_BY| art_Dockerfile
    mod_open_telemetry -->|PACKAGED_BY| art_open_telemetry_docker_compose_yaml
    mod_packages_app -->|PACKAGED_BY| art_Dockerfile
    mod_packages_backend -->|PACKAGED_BY| art_Dockerfile
```

- `pages.yml#deploy` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `8ab86fc0-d7fd-4ce5-9892-4f044a7c8571` (code_module) --[BUILT_BY]--> `pull.yml#build` (ci_job)
- `8ab86fc0-d7fd-4ce5-9892-4f044a7c8571` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `open-telemetry` (code_module) --[PACKAGED_BY]--> `open-telemetry/docker-compose.yaml` (container)
- `packages/app` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `packages/backend` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)


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
  pipeline_root(["backstage/demo (5 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_0_Main_Master_Build["Main Master Build (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_0_Main_Master_Build
  job_0_build["build"]:::atlasJob
  wf_0_Main_Master_Build --> job_0_build
  wf_1_PR_CI_build["PR CI build (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_1_PR_CI_build
  job_1_build["build"]:::atlasJob
  wf_1_PR_CI_build --> job_1_build
  grp_1_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Release___Deploy
  wf_2_Publish_Backstage_TechDocs["Publish Backstage TechDocs (1 jobs)"]:::atlasWorkflow
  grp_1_Release___Deploy --> wf_2_Publish_Backstage_TechDocs
  job_2_publish_techdocs_site["publish-techdocs-site"]:::atlasJob
  wf_2_Publish_Backstage_TechDocs --> job_2_publish_techdocs_site
  wf_4_Deploy_static_content_to_Pages["Deploy static content to Pages (1 jobs)"]:::atlasWorkflow
  grp_1_Release___Deploy --> wf_4_Deploy_static_content_to_Pages
  job_4_deploy["deploy"]:::atlasJob
  wf_4_Deploy_static_content_to_Pages --> job_4_deploy
  grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Scheduled___Manual
  wf_3_Version_Bump["Version Bump (1 jobs)"]:::atlasWorkflow
  grp_2_Scheduled___Manual --> wf_3_Version_Bump
  job_3_version_bump["version-bump"]:::atlasJob
  wf_3_Version_Bump --> job_3_version_bump
```
