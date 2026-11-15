---
title: Architecture — PostHog/duckgres
description: Arc42 and Pipeline report for PostHog/duckgres
---

# Repository Architecture Analysis: PostHog/duckgres

## Metadata
- **SHA**: `7fb3ac9bb32d8d75858119e7ec2ca2621375051e`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 5.14
- **avg_cyclomatic_complexity**: 4.45
- **component_count**: 322
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 4.84
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 1013
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: Go Gin / Echo / Fiber
- **import_edges**: 100 entry(ies)
- **loc**: 325843
- **max_cognitive_complexity**: 730
- **max_cyclomatic_complexity**: 92
- **sloc**: 260213
- **test_file_count**: 607

# Architecture: PostHog/duckgres

## Context
- **Repository**: `PostHog/duckgres`
- **SHA**: `7fb3ac9bb32d8d75858119e7ec2ca2621375051e`
- **Ecosystem**: Go
- **Framework**: Go Gin / Echo / Fiber

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
    repo_root(["PostHog/duckgres (322 components)"]):::atlasRoot
    subgraph sg_dir_0_controlplane["controlplane (270)"]
      direction TB
      dir_0_controlplane["controlplane (270)"]:::atlasCategory
      sub_0_0__module_root_["(module root) (204)"]:::atlasWorkflow
      dir_0_controlplane --> sub_0_0__module_root_
      sub_0_1_admin["admin (66)"]:::atlasWorkflow
      dir_0_controlplane --> sub_0_1_admin
    end
    repo_root --> dir_0_controlplane
    subgraph sg_dir_1_cmd["cmd (31)"]
      direction TB
      dir_1_cmd["cmd (31)"]:::atlasCategory
      sub_1_0_cache_proxy["cache-proxy (27)"]:::atlasWorkflow
      dir_1_cmd --> sub_1_0_cache_proxy
      sub_1_1_duckgres_controlplane["duckgres-controlplane (1)"]:::atlasWorkflow
      dir_1_cmd --> sub_1_1_duckgres_controlplane
      sub_1_2_duckgres_perf_publisher["duckgres-perf-publisher (1)"]:::atlasWorkflow
      dir_1_cmd --> sub_1_2_duckgres_perf_publisher
      sub_1_more["+2 more submodules (2)"]:::atlasMore
      dir_1_cmd --> sub_1_more
    end
    repo_root --> dir_1_cmd
    dir_2_configresolve["configresolve (7)"]:::atlasCategory
    repo_root --> dir_2_configresolve
    dir_3__root_["(root) (6)"]:::atlasCategory
    repo_root --> dir_3__root_
    dir_4_scripts["scripts (6)"]:::atlasCategory
    repo_root --> dir_4_scripts
    dir_other_modules["+1 more modules (2)"]:::atlasMore
    repo_root --> dir_other_modules
```

## Component Details

Showing top 60 representative components out of 322 across 6 module group(s):

- **Module `controlplane`** (270 components — module: 204, UI_COMPONENT: 65, MODULE: 1)
- **Module `cmd`** (31 components — module: 31)
- **Module `configresolve`** (7 components — module: 7)
- **Module `(root)`** (6 components — module: 6)
- **Module `scripts`** (6 components — module: 4, MODULE: 2)
- **Module `configloader`** (2 components — module: 2)

- **TrinoCluster** (`controlplane/admin/ui/src/pages/TrinoCluster.tsx`): UI_COMPONENT (deps: TrinoRecovery)
- **AddOrgDialog** (`controlplane/admin/ui/src/components/AddOrgDialog.tsx`): UI_COMPONENT
- **AdminGate** (`controlplane/admin/ui/src/components/AdminOnly.tsx`): UI_COMPONENT
- **App** (`controlplane/admin/ui/src/App.tsx`): UI_COMPONENT
- **AppShell** (`controlplane/admin/ui/src/components/AppShell.tsx`): UI_COMPONENT
- **Audit** (`controlplane/admin/ui/src/pages/Audit.tsx`): UI_COMPONENT
- **BackfillBadge** (`controlplane/admin/ui/src/components/OrgTeamDialogs.tsx`): UI_COMPONENT
- **ConfigStore** (`controlplane/admin/ui/src/pages/ConfigStore.tsx`): UI_COMPONENT
- **CopyButton** (`controlplane/admin/ui/src/components/CopyButton.tsx`): UI_COMPONENT
- **CreateTeamDialog** (`controlplane/admin/ui/src/components/OrgTeamDialogs.tsx`): UI_COMPONENT
- **DataTable** (`controlplane/admin/ui/src/components/DataTable.tsx`): UI_COMPONENT
- **DeleteTeamDialog** (`controlplane/admin/ui/src/components/OrgTeamDialogs.tsx`): UI_COMPONENT
- **DeprecationBanner** (`controlplane/admin/ui/src/components/DeprecationBanner.tsx`): UI_COMPONENT
- **EarliestEventDateCell** (`controlplane/admin/ui/src/components/OrgTeamDialogs.tsx`): UI_COMPONENT
- **EditTeamDialog** (`controlplane/admin/ui/src/components/OrgTeamDialogs.tsx`): UI_COMPONENT
- **EmptyState** (`controlplane/admin/ui/src/components/states.tsx`): UI_COMPONENT
- **ErrorState** (`controlplane/admin/ui/src/components/states.tsx`): UI_COMPONENT
- **Errors** (`controlplane/admin/ui/src/pages/Errors.tsx`): UI_COMPONENT
- **IdentityProvider** (`controlplane/admin/ui/src/components/IdentityProvider.tsx`): UI_COMPONENT
- **Impersonate** (`controlplane/admin/ui/src/pages/Impersonate.tsx`): UI_COMPONENT
- **InfoTooltip** (`controlplane/admin/ui/src/components/InfoTooltip.tsx`): UI_COMPONENT
- **JsonValue** (`controlplane/admin/ui/src/components/JsonView.tsx`): UI_COMPONENT
- **LegacyNamesBadge** (`controlplane/admin/ui/src/components/OrgTeamDialogs.tsx`): UI_COMPONENT
- **Live** (`controlplane/admin/ui/src/pages/Live.tsx`): UI_COMPONENT
- **LoadingState** (`controlplane/admin/ui/src/components/states.tsx`): UI_COMPONENT
- **Metrics** (`controlplane/admin/ui/src/pages/Metrics.tsx`): UI_COMPONENT
- **NAV** (`controlplane/admin/ui/src/components/nav.ts`): UI_COMPONENT
- **Nodes** (`controlplane/admin/ui/src/pages/Nodes.tsx`): UI_COMPONENT
- **NotAuthorized** (`controlplane/admin/ui/src/pages/NotAuthorized.tsx`): UI_COMPONENT
- **NotFound** (`controlplane/admin/ui/src/pages/NotFound.tsx`): UI_COMPONENT
- **Operators** (`controlplane/admin/ui/src/pages/Operators.tsx`): UI_COMPONENT
- **OrgDetail** (`controlplane/admin/ui/src/pages/OrgDetail.tsx`): UI_COMPONENT
- **OrgRef** (`controlplane/admin/ui/src/components/OrgRef.tsx`): UI_COMPONENT
- **OrgTeams** (`controlplane/admin/ui/src/pages/OrgTeams.tsx`): UI_COMPONENT
- **OrgTrinoCard** (`controlplane/admin/ui/src/pages/OrgTrinoCard.tsx`): UI_COMPONENT
- **OrgTrinoSettings** (`controlplane/admin/ui/src/pages/OrgTrinoSettings.tsx`): UI_COMPONENT
- **OrgUsageSection** (`controlplane/admin/ui/src/pages/OrgUsage.tsx`): UI_COMPONENT
- **Orgs** (`controlplane/admin/ui/src/pages/Orgs.tsx`): UI_COMPONENT
- **Overview** (`controlplane/admin/ui/src/pages/Overview.tsx`): UI_COMPONENT
- **POLL** (`controlplane/admin/ui/src/lib/query.ts`): UI_COMPONENT
- **PageBody** (`controlplane/admin/ui/src/components/AppShell.tsx`): UI_COMPONENT
- **PageHeader** (`controlplane/admin/ui/src/components/AppShell.tsx`): UI_COMPONENT
- **ProgressBar** (`controlplane/admin/ui/src/components/ProgressBar.tsx`): UI_COMPONENT
- **QueryDetailDialog** (`controlplane/admin/ui/src/components/QueryDetailDialog.tsx`): UI_COMPONENT
- **RESHARD_LOG_CATCHUP_PAGE** (`controlplane/admin/ui/src/hooks/useApi.ts`): UI_COMPONENT
- **REVEAL_TICKS_TARGET** (`controlplane/admin/ui/src/lib/logReplay.ts`): UI_COMPONENT
- **REVEAL_TICK_MS** (`controlplane/admin/ui/src/lib/logReplay.ts`): UI_COMPONENT
- **ReshardForm** (`controlplane/admin/ui/src/pages/ReshardForm.tsx`): UI_COMPONENT
- **ReshardOperation** (`controlplane/admin/ui/src/pages/ReshardOperation.tsx`): UI_COMPONENT
- **Reshards** (`controlplane/admin/ui/src/pages/Reshards.tsx`): UI_COMPONENT
- **Separator** (`controlplane/admin/ui/src/components/ui/separator.tsx`): UI_COMPONENT
- **ShardBadge** (`controlplane/admin/ui/src/components/ShardBadge.tsx`): UI_COMPONENT
- **Sidebar** (`controlplane/admin/ui/src/components/Sidebar.tsx`): UI_COMPONENT
- **Sparkline** (`controlplane/admin/ui/src/components/Sparkline.tsx`): UI_COMPONENT
- **StatCard** (`controlplane/admin/ui/src/components/StatCard.tsx`): UI_COMPONENT
- **StateBadge** (`controlplane/admin/ui/src/components/StateBadge.tsx`): UI_COMPONENT
- **TableSkeleton** (`controlplane/admin/ui/src/components/states.tsx`): UI_COMPONENT
- **Topbar** (`controlplane/admin/ui/src/components/Topbar.tsx`): UI_COMPONENT
- **TrinoCellPicker** (`controlplane/admin/ui/src/components/TrinoCellPicker.tsx`): UI_COMPONENT
- **TrinoQueries** (`controlplane/admin/ui/src/pages/TrinoQueries.tsx`): UI_COMPONENT

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (54.48/100)
- **Technical Debt Score**: 45.52
- **Estimated Remediation Effort**: 62.35h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 61.94 | 0.20 | avg_cc=4.45, max_cc=92, duplication=4.84%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=778, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 42.58 | 0.15 | avg_cognitive=5.14, max_cognitive=730, fitness_violations=2, oversized_files=6 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=13, operational_antipatterns=37, parallel_branches=True |
| Security | `F` | 51.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=3 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (730.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (92.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 778 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `server/tlscert/acme_dns_test.go:73` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `org.postgresql:postgresql` `42.7.12` (Maven, `scripts/client-compat/clients/jdbc/pom.xml`)
- `org.yaml:snakeyaml` `2.3` (Maven, `scripts/client-compat/clients/jdbc/pom.xml`)
- `native-tls` `0.2` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `postgres-native-tls` `0.5` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `reqwest` `0.12` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `serde` `1` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `serde_json` `1` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `serde_yaml` `0.9` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `tokio` `1` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `tokio-postgres` `0.7` (cargo, `scripts/client-compat/clients/tokio-postgres/Cargo.toml`)
- `github.com/apache/arrow-go/v18` `18.5.1` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2` `1.45.1` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/config` `1.32.29` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/credentials` `1.19.28` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/feature/s3/manager` `1.22.32` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/athena` `1.64.0` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/glue` `1.155.0` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/route53` `1.62.3` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/s3` `1.105.0` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/sts` `1.44.0` (golang, `go.mod`)
- `github.com/cloudflare/tableflip` `1.2.3` (golang, `go.mod`)
- `github.com/duckdb/duckdb-go-bindings` `0.10505.0` (golang, `go.mod`)
- `github.com/duckdb/duckdb-go/v2` `2.10505.0` (golang, `go.mod`)
- `github.com/gin-contrib/gzip` `1.2.6` (golang, `go.mod`)
- `github.com/gin-gonic/gin` `1.12.0` (golang, `go.mod`)
- `github.com/google/uuid` `1.6.0` (golang, `go.mod`)
- `github.com/hashicorp/golang-lru/v2` `2.0.7` (golang, `go.mod`)
- `github.com/jackc/pgx/v5` `5.9.2` (golang, `go.mod`)
- `github.com/jackc/pgx/v5` `5.9.2` (golang, `scripts/client-compat/clients/pgx/go.mod`)
- `github.com/lib/pq` `1.10.9` (golang, `go.mod`)
- ... (+748 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_b28807bf_dc5b_4a18_9055_854894d4e803["b28807bf-dc5b-4a18-9055-854894d4e803"]:::atlasCategory
        mod_cmd_cache_proxy["cmd/cache-proxy"]:::atlasCategory
        mod_controlplane_admin_ui["controlplane/admin/ui"]:::atlasCategory
        mod_scripts_client_compat["scripts/client-compat"]:::atlasCategory
        mod_scripts_client_compat_clients_dbt["scripts/client-compat/clients/dbt"]:::atlasCategory
        mod_scripts_client_compat_clients_harlequin["scripts/client-compat/clients/harlequin"]:::atlasCategory
        mod_scripts_client_compat_clients_jdbc["scripts/client-compat/clients/jdbc"]:::atlasCategory
        mod_scripts_client_compat_clients_node_postgres["scripts/client-compat/clients/node-postgres"]:::atlasCategory
        mod_scripts_client_compat_clients_pgadmin["scripts/client-compat/clients/pgadmin"]:::atlasCategory
        mod_scripts_client_compat_clients_pgx["scripts/client-compat/clients/pgx"]:::atlasCategory
        mod_scripts_client_compat_clients_psql["scripts/client-compat/clients/psql"]:::atlasCategory
        mod_scripts_client_compat_clients_psycopg["scripts/client-compat/clients/psycopg"]:::atlasCategory
        mod_scripts_client_compat_clients_sqlalchemy["scripts/client-compat/clients/sqlalchemy"]:::atlasCategory
        mod_scripts_client_compat_clients_tokio_postgres["scripts/client-compat/clients/tokio-postgres"]:::atlasCategory
        mod_tests_integration["tests/integration"]:::atlasCategory
        mod_tests_integration_trino["tests/integration/trino"]:::atlasCategory
        mod_tests_mw_dev_scenario["tests/mw-dev/scenario"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_____inputs_dockerfile___["${{ inputs.dockerfile }}"]:::atlasWorkflow
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
        art_Dockerfile_controlplane["Dockerfile.controlplane"]:::atlasWorkflow
        art_Dockerfile_worker["Dockerfile.worker"]:::atlasWorkflow
        art_cmd_cache_proxy_Dockerfile["cmd/cache-proxy/Dockerfile"]:::atlasWorkflow
        art_docker_compose_yaml["docker-compose.yaml"]:::atlasWorkflow
        art_k8s_control_plane_multitenant_local_yaml["k8s/control-plane-multitenant-local.yaml"]:::atlasWorkflow
        art_k8s_kind_control_plane_yaml["k8s/kind/control-plane.yaml"]:::atlasWorkflow
        art_scripts_client_compat_Dockerfile_results["scripts/client-compat/Dockerfile.results"]:::atlasWorkflow
        art_scripts_client_compat_clients_dbt_Dockerfile["scripts/client-compat/clients/dbt/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_harlequin_Dockerfile["scripts/client-compat/clients/harlequin/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_jdbc_Dockerfile["scripts/client-compat/clients/jdbc/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_node_postgres_Dockerfile["scripts/client-compat/clients/node-postgres/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_pgadmin_Dockerfile["scripts/client-compat/clients/pgadmin/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_pgx_Dockerfile["scripts/client-compat/clients/pgx/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_psql_Dockerfile["scripts/client-compat/clients/psql/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_psycopg_Dockerfile["scripts/client-compat/clients/psycopg/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_sqlalchemy_Dockerfile["scripts/client-compat/clients/sqlalchemy/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_clients_tokio_postgres_Dockerfile["scripts/client-compat/clients/tokio-postgres/Dockerfile"]:::atlasWorkflow
        art_scripts_client_compat_docker_compose_yml["scripts/client-compat/docker-compose.yml"]:::atlasWorkflow
        art_tests_integration_docker_compose_yml["tests/integration/docker-compose.yml"]:::atlasWorkflow
        art_tests_integration_trino_Dockerfile["tests/integration/trino/Dockerfile"]:::atlasWorkflow
        art_tests_mw_dev_scenario_Dockerfile["tests/mw-dev/scenario/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job__image_build_yml_build["_image-build.yml#build"]:::atlasJob
        job_ci_yml_integration_tests["ci.yml#integration-tests"]:::atlasJob
        job_container_image_cache_proxy_cd_yml_build["container-image-cache-proxy-cd.yml#build"]:::atlasJob
        job_container_image_cd_yml_build["container-image-cd.yml#build"]:::atlasJob
        job_container_image_controlplane_cd_yml_build["container-image-controlplane-cd.yml#build"]:::atlasJob
        job_container_image_worker_cd_yml_build["container-image-worker-cd.yml#build"]:::atlasJob
        job_e2e_mw_dev_yml_e2e_cleanup["e2e-mw-dev.yml#e2e-cleanup"]:::atlasJob
        job_e2e_mw_dev_yml_e2e_teardown["e2e-mw-dev.yml#e2e-teardown"]:::atlasJob
        job_e2e_mw_dev_yml_e2e_lanes["e2e-mw-dev.yml#e2e_lanes"]:::atlasJob
        job_scenario_dev_yml_scenario["scenario-dev.yml#scenario"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_azure["azure"]:::atlasTarget
    end
    job_e2e_mw_dev_yml_e2e_cleanup -->|DEPLOYS_TO| env_azure
    job_e2e_mw_dev_yml_e2e_teardown -->|DEPLOYS_TO| env_azure
    job_e2e_mw_dev_yml_e2e_lanes -->|DEPLOYS_TO| env_azure
    job_scenario_dev_yml_scenario -->|DEPLOYS_TO| env_azure
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|DEPLOYED_BY| job__image_build_yml_build
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|DEPLOYED_BY| job_container_image_cache_proxy_cd_yml_build
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|DEPLOYED_BY| job_container_image_cd_yml_build
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|DEPLOYED_BY| job_container_image_controlplane_cd_yml_build
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|DEPLOYED_BY| job_container_image_worker_cd_yml_build
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_____inputs_dockerfile___
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_Dockerfile
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_Dockerfile_controlplane
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_Dockerfile_worker
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_docker_compose_yaml
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_b28807bf_dc5b_4a18_9055_854894d4e803 -->|PACKAGED_BY| art_tests_integration_docker_compose_yml
    mod_cmd_cache_proxy -->|PACKAGED_BY| art_cmd_cache_proxy_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_Dockerfile_controlplane
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_Dockerfile_worker
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_cmd_cache_proxy_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_scripts_client_compat_clients_harlequin_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_scripts_client_compat_clients_jdbc_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_scripts_client_compat_clients_pgx_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_scripts_client_compat_clients_tokio_postgres_Dockerfile
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_tests_integration_docker_compose_yml
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_k8s_control_plane_multitenant_local_yaml
    mod_controlplane_admin_ui -->|PACKAGED_BY| art_k8s_kind_control_plane_yaml
    mod_scripts_client_compat -->|PACKAGED_BY| art_scripts_client_compat_Dockerfile_results
    mod_scripts_client_compat -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_dbt -->|PACKAGED_BY| art_scripts_client_compat_clients_dbt_Dockerfile
    mod_scripts_client_compat_clients_dbt -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_dbt -->|PACKAGED_BY| art_tests_mw_dev_scenario_Dockerfile
    mod_scripts_client_compat_clients_harlequin -->|PACKAGED_BY| art_scripts_client_compat_clients_harlequin_Dockerfile
    mod_scripts_client_compat_clients_jdbc -->|PACKAGED_BY| art_scripts_client_compat_clients_jdbc_Dockerfile
    mod_scripts_client_compat_clients_jdbc -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_node_postgres -->|PACKAGED_BY| art_scripts_client_compat_clients_node_postgres_Dockerfile
    mod_scripts_client_compat_clients_node_postgres -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_pgadmin -->|PACKAGED_BY| art_scripts_client_compat_clients_pgadmin_Dockerfile
    mod_scripts_client_compat_clients_pgadmin -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_pgx -->|PACKAGED_BY| art_scripts_client_compat_clients_pgx_Dockerfile
    mod_scripts_client_compat_clients_pgx -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_psql -->|PACKAGED_BY| art_scripts_client_compat_clients_psql_Dockerfile
    mod_scripts_client_compat_clients_psql -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_psql -->|PACKAGED_BY| art_tests_integration_docker_compose_yml
    mod_scripts_client_compat_clients_psycopg -->|PACKAGED_BY| art_scripts_client_compat_clients_harlequin_Dockerfile
    mod_scripts_client_compat_clients_psycopg -->|PACKAGED_BY| art_scripts_client_compat_clients_pgadmin_Dockerfile
    mod_scripts_client_compat_clients_psycopg -->|PACKAGED_BY| art_scripts_client_compat_clients_psycopg_Dockerfile
    mod_scripts_client_compat_clients_psycopg -->|PACKAGED_BY| art_scripts_client_compat_clients_sqlalchemy_Dockerfile
    mod_scripts_client_compat_clients_psycopg -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_sqlalchemy -->|PACKAGED_BY| art_scripts_client_compat_clients_sqlalchemy_Dockerfile
    mod_scripts_client_compat_clients_sqlalchemy -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_scripts_client_compat_clients_tokio_postgres -->|PACKAGED_BY| art_scripts_client_compat_clients_tokio_postgres_Dockerfile
    mod_scripts_client_compat_clients_tokio_postgres -->|PACKAGED_BY| art_scripts_client_compat_docker_compose_yml
    mod_tests_integration -->|BUILT_BY| job_ci_yml_integration_tests
    mod_tests_integration -->|PACKAGED_BY| art_tests_integration_docker_compose_yml
    mod_tests_integration_trino -->|PACKAGED_BY| art_tests_integration_docker_compose_yml
    mod_tests_integration_trino -->|PACKAGED_BY| art_tests_integration_trino_Dockerfile
    mod_tests_mw_dev_scenario -->|DEPLOYED_BY| job_scenario_dev_yml_scenario
    mod_tests_mw_dev_scenario -->|PACKAGED_BY| art_tests_mw_dev_scenario_Dockerfile
    art_Dockerfile -->|BUILT_BY| job__image_build_yml_build
    art_Dockerfile -->|BUILT_BY| job_container_image_cache_proxy_cd_yml_build
    art_Dockerfile -->|BUILT_BY| job_container_image_cd_yml_build
    art_Dockerfile -->|BUILT_BY| job_container_image_controlplane_cd_yml_build
    art_Dockerfile -->|BUILT_BY| job_container_image_worker_cd_yml_build
    art_Dockerfile_controlplane -->|BUILT_BY| job_container_image_controlplane_cd_yml_build
    art_Dockerfile_worker -->|BUILT_BY| job_container_image_worker_cd_yml_build
    art_cmd_cache_proxy_Dockerfile -->|BUILT_BY| job_container_image_cache_proxy_cd_yml_build
    art_tests_integration_docker_compose_yml -->|BUILT_BY| job_ci_yml_integration_tests
    art_tests_mw_dev_scenario_Dockerfile -->|DEPLOYED_BY| job_scenario_dev_yml_scenario
```

- `e2e-mw-dev.yml#e2e-cleanup` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `e2e-mw-dev.yml#e2e-teardown` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `e2e-mw-dev.yml#e2e_lanes` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `scenario-dev.yml#scenario` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[DEPLOYED_BY]--> `_image-build.yml#build` (ci_job)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[DEPLOYED_BY]--> `container-image-cache-proxy-cd.yml#build` (ci_job)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[DEPLOYED_BY]--> `container-image-cd.yml#build` (ci_job)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[DEPLOYED_BY]--> `container-image-controlplane-cd.yml#build` (ci_job)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[DEPLOYED_BY]--> `container-image-worker-cd.yml#build` (ci_job)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `${{ inputs.dockerfile }}` (container)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `Dockerfile.controlplane` (container)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `Dockerfile.worker` (container)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `docker-compose.yaml` (container)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/docker-compose.yml` (container)
- `b28807bf-dc5b-4a18-9055-854894d4e803` (code_module) --[PACKAGED_BY]--> `tests/integration/docker-compose.yml` (container)
- `cmd/cache-proxy` (code_module) --[PACKAGED_BY]--> `cmd/cache-proxy/Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `Dockerfile.controlplane` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `Dockerfile.worker` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `cmd/cache-proxy/Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/harlequin/Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/jdbc/Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/pgx/Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/tokio-postgres/Dockerfile` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/docker-compose.yml` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `tests/integration/docker-compose.yml` (container)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `k8s/control-plane-multitenant-local.yaml` (iac)
- `controlplane/admin/ui` (code_module) --[PACKAGED_BY]--> `k8s/kind/control-plane.yaml` (iac)
- `scripts/client-compat` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/Dockerfile.results` (container)
- `scripts/client-compat` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/docker-compose.yml` (container)
- `scripts/client-compat/clients/dbt` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/dbt/Dockerfile` (container)
- `scripts/client-compat/clients/dbt` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/docker-compose.yml` (container)
- `scripts/client-compat/clients/dbt` (code_module) --[PACKAGED_BY]--> `tests/mw-dev/scenario/Dockerfile` (container)
- `scripts/client-compat/clients/harlequin` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/harlequin/Dockerfile` (container)
- `scripts/client-compat/clients/jdbc` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/jdbc/Dockerfile` (container)
- `scripts/client-compat/clients/jdbc` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/docker-compose.yml` (container)
- `scripts/client-compat/clients/node-postgres` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/node-postgres/Dockerfile` (container)
- `scripts/client-compat/clients/node-postgres` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/docker-compose.yml` (container)
- `scripts/client-compat/clients/pgadmin` (code_module) --[PACKAGED_BY]--> `scripts/client-compat/clients/pgadmin/Dockerfile` (container)


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
  pipeline_root(["PostHog/duckgres (13 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Scheduled___Manual["Scheduled & Manual (8 workflows · 26 jobs)"]
    direction TB
    subgraph sg_wf_1_CI["CI (9 jobs)"]
      direction TB
      wf_1_CI(["Trigger: CI"]):::atlasWorkflow
      job_1_lint["lint"]:::atlasJob
      job_1_controlplane_no_libduckdb["controlplane-no-libduckdb"]:::atlasJob
      job_1_unit_tests["unit-tests"]:::atlasJob
      wf_1_CI --> job_1_lint
      wf_1_CI --> job_1_controlplane_no_libduckdb
      wf_1_CI --> job_1_unit_tests
    end
    pipeline_root --> wf_1_CI
    subgraph sg_wf_4_Container_Image_CD["Container Image CD (2 jobs)"]
      direction TB
      wf_4_Container_Image_CD(["Trigger: Container Image CD"]):::atlasWorkflow
      job_4_build["build"]:::atlasJob
      job_4_manifest["manifest"]:::atlasJob
      wf_4_Container_Image_CD --> job_4_build
      job_4_build --> job_4_manifest
    end
    pipeline_root --> wf_4_Container_Image_CD
    subgraph sg_wf_6_Container_Image_Worker_CD__per_DuckDB_version_["Container Image Worker CD (per DuckDB version) (3 jobs)"]
      direction TB
      wf_6_Container_Image_Worker_CD__per_DuckDB_version_(["Trigger: Container Image Worker CD (per DuckDB version)"]):::atlasWorkflow
      job_6_validate_matrix["validate-matrix"]:::atlasJob
      job_6_build["build"]:::atlasJob
      job_6_manifest["manifest"]:::atlasJob
      wf_6_Container_Image_Worker_CD__per_DuckDB_version_ --> job_6_validate_matrix
      job_6_validate_matrix --> job_6_build
      job_6_build --> job_6_manifest
    end
    pipeline_root --> wf_6_Container_Image_Worker_CD__per_DuckDB_version_
    subgraph sg_wf_7_e2e_mw_dev["e2e-mw-dev (5 jobs)"]
      direction TB
      wf_7_e2e_mw_dev(["Trigger: e2e-mw-dev"]):::atlasWorkflow
      job_7_build["build"]:::atlasJob
      job_7_e2e_lanes["e2e_lanes"]:::atlasJob
      job_7_e2e["e2e"]:::atlasJob
      wf_7_e2e_mw_dev --> job_7_build
      job_7_build --> job_7_e2e_lanes
      job_7_e2e_lanes --> job_7_e2e
    end
    pipeline_root --> wf_7_e2e_mw_dev
    subgraph sg_wf_10_scenario_dev["scenario-dev (3 jobs)"]
      direction TB
      wf_10_scenario_dev(["Trigger: scenario-dev"]):::atlasWorkflow
      job_10_scenario_runner_image["scenario-runner-image"]:::atlasJob
      job_10_duckgres_image["duckgres-image"]:::atlasJob
      job_10_scenario["scenario"]:::atlasJob
      wf_10_scenario_dev --> job_10_scenario_runner_image
      wf_10_scenario_dev --> job_10_duckgres_image
      job_10_scenario_runner_image --> job_10_scenario
      job_10_duckgres_image --> job_10_scenario
    end
    pipeline_root --> wf_10_scenario_dev
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (3 workflows · 3 jobs)"]
    direction TB
    subgraph sg_wf_0__image_build["_image-build (1 jobs)"]
      direction TB
      wf_0__image_build(["Trigger: _image-build"]):::atlasWorkflow
      job_0_build["build"]:::atlasJob
      wf_0__image_build --> job_0_build
    end
    pipeline_root --> wf_0__image_build
    subgraph sg_wf_11_test_impact_plan_comment["test-impact-plan-comment (1 jobs)"]
      direction TB
      wf_11_test_impact_plan_comment(["Trigger: test-impact-plan-comment"]):::atlasWorkflow
      job_11_comment["comment"]:::atlasJob
      wf_11_test_impact_plan_comment --> job_11_comment
    end
    pipeline_root --> wf_11_test_impact_plan_comment
    wf_12_test_impact_plan["test-impact-plan (1 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_12_test_impact_plan
  end
  subgraph sg_grp_2_Release___Deploy["Release & Deploy (1 workflows · 2 jobs)"]
    direction TB
    wf_8_Release_Build["Release Build (2 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_8_Release_Build
  end
  subgraph sg_grp_3_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    wf_2_CodeQL_Advanced["CodeQL Advanced (1 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_2_CodeQL_Advanced
  end
  wf_more["+3 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
