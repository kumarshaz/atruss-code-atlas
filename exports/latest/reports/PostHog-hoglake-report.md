---
title: Architecture — PostHog/hoglake
description: Arc42 and Pipeline report for PostHog/hoglake
---

# Repository Architecture Analysis: PostHog/hoglake

## Metadata
- **SHA**: `91bd3373eaf9271227506f7436ff4bc3ed2f4811`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 5.47
- **avg_cyclomatic_complexity**: 7.43
- **component_count**: 57
- **dead_code_count**: 1
- **dead_code_symbols**: 1 entry(ies)
- **duplication_pct**: 79.91
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 927
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 366534
- **max_cognitive_complexity**: 460
- **max_cyclomatic_complexity**: 690
- **sloc**: 273588
- **test_file_count**: 1708

# Architecture: PostHog/hoglake

## Context
- **Repository**: `PostHog/hoglake`
- **SHA**: `91bd3373eaf9271227506f7436ff4bc3ed2f4811`
- **Ecosystem**: Java
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
    repo_root(["PostHog/hoglake (57 components)"]):::atlasRoot
    dir_0_webui["webui (34)"]:::atlasCategory
    repo_root --> dir_0_webui
    sub_0_0_src["src (33)"]:::atlasWorkflow
    dir_0_webui --> sub_0_0_src
    sub_0_1__module_root_["(module root) (1)"]:::atlasWorkflow
    dir_0_webui --> sub_0_1__module_root_
    dir_1_pyhoglake_variant_codec["pyhoglake-variant-codec (17)"]:::atlasCategory
    repo_root --> dir_1_pyhoglake_variant_codec
    sub_1_0_src["src (11)"]:::atlasWorkflow
    dir_1_pyhoglake_variant_codec --> sub_1_0_src
    sub_1_1_tests["tests (4)"]:::atlasWorkflow
    dir_1_pyhoglake_variant_codec --> sub_1_1_tests
    sub_1_2_fuzz["fuzz (2)"]:::atlasWorkflow
    dir_1_pyhoglake_variant_codec --> sub_1_2_fuzz
    dir_2_millrace["millrace (3)"]:::atlasCategory
    repo_root --> dir_2_millrace
    dir_3_hedgerow["hedgerow (2)"]:::atlasCategory
    repo_root --> dir_3_hedgerow
    dir_4_ci["ci (1)"]:::atlasCategory
    repo_root --> dir_4_ci
```

## Component Details
- **docker-compose.live-millrace** (`ci/docker-compose.live-millrace.yml`): module
- **BufferedService** (`hedgerow/src/hedgerow/buffered_service.py`): SERVICE
- **Service** (`hedgerow/tests/test_buffered_cli.py`): SERVICE (deps: BufferedService)
- **MaintenanceService** (`millrace/maintenance.py`): SERVICE
- **StageManager** (`millrace/stage.py`): SERVICE
- **JournalingStageManager** (`millrace/tests/test_consumer.py`): SERVICE (deps: StageManager)
- **decode** (`pyhoglake-variant-codec/fuzz/fuzz_targets/decode.rs`): module
- **encode_json** (`pyhoglake-variant-codec/fuzz/fuzz_targets/encode_json.rs`): module
- **consts** (`pyhoglake-variant-codec/src/consts.rs`): module
- **lib** (`pyhoglake-variant-codec/src/lib.rs`): module
- **python** (`pyhoglake-variant-codec/src/python.rs`): module
- **mod** (`pyhoglake-variant-codec/src/decode/mod.rs`): module
- **storage** (`pyhoglake-variant-codec/src/decode/storage.rs`): module
- **tagged** (`pyhoglake-variant-codec/src/decode/tagged.rs`): module
- **value** (`pyhoglake-variant-codec/src/decode/value.rs`): module
- **mod** (`pyhoglake-variant-codec/src/encode/mod.rs`): module
- **parse** (`pyhoglake-variant-codec/src/encode/parse.rs`): module
- **shred** (`pyhoglake-variant-codec/src/encode/shred.rs`): module
- **write** (`pyhoglake-variant-codec/src/encode/write.rs`): module
- **decode** (`pyhoglake-variant-codec/tests/decode.rs`): module
- **encode** (`pyhoglake-variant-codec/tests/encode.rs`): module
- **shred** (`pyhoglake-variant-codec/tests/shred.rs`): module
- **mod** (`pyhoglake-variant-codec/tests/oracle/mod.rs`): module
- **hoglake-webui** (`webui/package.json`): MODULE
- **App** (`webui/src/App.tsx`): UI_COMPONENT (deps: CatalogPage, CatalogsPage, CentralMaintenancePage, ConsumersPage, DatabasePage, Layout, MaintenancePage, MetricsPage, NamespacePage, PartitionsPage, TablePage)
- **AuthStatus** (`webui/src/components/Auth.tsx`): UI_COMPONENT (deps: EXPIRY_WARNING_SECONDS)
- **SignInPanel** (`webui/src/components/Auth.tsx`): UI_COMPONENT (deps: EXPIRY_WARNING_SECONDS)
- **OperatorTokenNotice** (`webui/src/components/Auth.tsx`): UI_COMPONENT (deps: EXPIRY_WARNING_SECONDS)
- **ClampedText** (`webui/src/components/ClampedText.tsx`): UI_COMPONENT (deps: CopyButton)
- **CopyButton** (`webui/src/components/CopyButton.tsx`): UI_COMPONENT
- **ErrorBox** (`webui/src/components/ErrorBox.tsx`): UI_COMPONENT (deps: EXPIRY_WARNING_SECONDS)
- **Layout** (`webui/src/components/Layout.tsx`): UI_COMPONENT (deps: AuthStatus, OperatorTokenNotice, SignInPanel)
- **PartitionLookupPanel** (`webui/src/components/PartitionLookupPanel.tsx`): UI_COMPONENT (deps: ChangeBadge, CopyButton, ErrorBox, SkeletonBlock, SkeletonRows, SnapshotId, StatsStateBadge)
- **SkeletonRows** (`webui/src/components/Skeleton.tsx`): UI_COMPONENT
- **SkeletonBlock** (`webui/src/components/Skeleton.tsx`): UI_COMPONENT
- **SnapshotId** (`webui/src/components/SnapshotId.tsx`): UI_COMPONENT
- **SortableTh** (`webui/src/components/SortableTh.tsx`): UI_COMPONENT
- **TimeSeriesChart** (`webui/src/components/TimeSeriesChart.tsx`): UI_COMPONENT
- **StatsStateBadge** (`webui/src/components/badges.tsx`): UI_COMPONENT
- **ChangeBadge** (`webui/src/components/badges.tsx`): UI_COMPONENT
- **RunStateBadge** (`webui/src/components/maintenance.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows)
- **RunOutcomeBadge** (`webui/src/components/maintenance.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows)
- **RunSummary** (`webui/src/components/maintenance.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows)
- **RUN_TASK_FILTERS** (`webui/src/components/maintenance.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows)
- **RunsTable** (`webui/src/components/maintenance.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows)
- **LedgerUnavailableNotice** (`webui/src/components/maintenance.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows)
- **EXPIRY_WARNING_SECONDS** (`webui/src/lib/auth.ts`): UI_COMPONENT
- **CatalogPage** (`webui/src/pages/CatalogPage.tsx`): UI_COMPONENT (deps: ChangeBadge, ClampedText, ErrorBox, LedgerUnavailableNotice, RUN_TASK_FILTERS, RunOutcomeBadge, RunStateBadge, RunSummary, RunsTable, SkeletonBlock, SkeletonRows, SnapshotId, StatsStateBadge)
- **CatalogsPage** (`webui/src/pages/CatalogsPage.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows, SnapshotId, SortableTh)
- **CentralMaintenancePage** (`webui/src/pages/CentralMaintenancePage.tsx`): UI_COMPONENT (deps: AuthStatus, ErrorBox, LedgerUnavailableNotice, OperatorTokenNotice, RUN_TASK_FILTERS, RunOutcomeBadge, RunStateBadge, RunSummary, RunsTable, SignInPanel, SkeletonBlock, SkeletonRows)
- **ConsumersPage** (`webui/src/pages/ConsumersPage.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows, SnapshotId, SortableTh)
- **DatabasePage** (`webui/src/pages/DatabasePage.tsx`): UI_COMPONENT (deps: AuthStatus, ErrorBox, OperatorTokenNotice, SignInPanel, SkeletonBlock, SkeletonRows, SortableTh)
- **MaintenancePage** (`webui/src/pages/MaintenancePage.tsx`): UI_COMPONENT (deps: ErrorBox, LedgerUnavailableNotice, RUN_TASK_FILTERS, RunOutcomeBadge, RunStateBadge, RunSummary, RunsTable, SkeletonBlock, SkeletonRows, SnapshotId)
- **MetricsPage** (`webui/src/pages/MetricsPage.tsx`): UI_COMPONENT (deps: AuthStatus, ErrorBox, OperatorTokenNotice, SignInPanel, SkeletonBlock, SkeletonRows, TimeSeriesChart)
- **NamespacePage** (`webui/src/pages/NamespacePage.tsx`): UI_COMPONENT (deps: ClampedText, ErrorBox, SkeletonBlock, SkeletonRows, SnapshotId, SortableTh)
- **PartitionsPage** (`webui/src/pages/PartitionsPage.tsx`): UI_COMPONENT (deps: ErrorBox, SkeletonBlock, SkeletonRows, SortableTh)
- **TablePage** (`webui/src/pages/TablePage.tsx`): UI_COMPONENT (deps: ChangeBadge, ClampedText, CopyButton, ErrorBox, PartitionLookupPanel, SkeletonBlock, SkeletonRows, SnapshotId, SortableTh, StatsStateBadge)

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (36.89/100)
- **Technical Debt Score**: 63.11
- **Estimated Remediation Effort**: 130.01h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.28 | 0.20 | avg_cc=7.43, max_cc=690, duplication=79.91%, dead_code=1 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=565, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 35.59 | 0.15 | avg_cognitive=5.47, max_cognitive=460, fitness_violations=3, oversized_files=25 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=16, operational_antipatterns=26, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=14, pipeline_security_findings=1 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (79.91) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (460.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (690.0) exceeds policy threshold (20.0).

### Workspace Packages
- **hoglake-bench** (`bench`, python, uv) -> internal deps: `pyhoglake`
- **hedgerow** (`hedgerow`, python, uv) -> internal deps: `pyhoglake`
- **millrace** (`millrace`, python, uv) -> internal deps: `pyhoglake`
- **pyhoglake** (`pyhoglake`, python, uv) -> internal deps: `pyhoglake-variant-codec`
- **pyhoglake-variant-codec** (`pyhoglake-variant-codec`, python, uv)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 565 | **Vulnerabilities**: 0 | **Secrets**: 14

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/kotlin/com/posthog/hoglake/auth/ContractVectors.kt:62` (`private const val KEY_X = "DJAd***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/kotlin/com/posthog/hoglake/auth/ContractVectors.kt:63` (`private const val KEY_Y = "HIhw***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:45` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:85` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:126` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:163` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:205` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:258` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:317` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:377` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:426` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:471` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:515` (`"token": "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `server/src/test/resources/oauth/contract-vectors.json:557` (`"token": "eyJh***REDACTED***",`)

### Inventory Sample
- `ch.qos.logback:logback-classic` `1.6.6` (Maven, `server/build.gradle.kts`)
- `com.code-intelligence:jazzer-junit` `0.30.0` (Maven, `server/build.gradle.kts`)
- `com.fasterxml.jackson.core:jackson-databind` `2.22.4` (Maven, `server/trino/build.gradle.kts`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jsr310` `2.22.4` (Maven, `server/build.gradle.kts`)
- `com.fasterxml.jackson.module:jackson-module-kotlin` `2.22.4` (Maven, `server/build.gradle.kts`)
- `com.zaxxer:HikariCP` `7.1.0` (Maven, `server/build.gradle.kts`)
- `com.zaxxer:HikariCP` `7.1.0` (Maven, `server/trino/build.gradle.kts`)
- `dev.hardwood:hardwood-core` `1.1.0.Beta3` (Maven, `server/trino/build.gradle.kts`)
- `io.github.oshai:kotlin-logging-jvm` `8.0.4` (Maven, `server/build.gradle.kts`)
- `io.kotest:kotest-property` `6.2.6` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-client-content-negotiation` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-serialization-jackson` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-call-logging` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-content-negotiation` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-core` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-core` `3.6.1` (Maven, `server/trino/build.gradle.kts`)
- `io.ktor:ktor-server-metrics-micrometer` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-netty` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-netty` `3.6.1` (Maven, `server/trino/build.gradle.kts`)
- `io.ktor:ktor-server-status-pages` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.ktor:ktor-server-test-host` `3.6.1` (Maven, `server/build.gradle.kts`)
- `io.micrometer:micrometer-registry-prometheus` `1.17.2` (Maven, `server/build.gradle.kts`)
- `io.trino:trino-jdbc` `484` (Maven, `server/trino/build.gradle.kts`)
- `net.logstash.logback:logstash-logback-encoder` `8.1` (Maven, `server/build.gradle.kts`)
- `org.apache.hadoop:hadoop-client-api` `3.5.0` (Maven, `server/build.gradle.kts`)
- `org.apache.hadoop:hadoop-client-runtime` `3.5.0` (Maven, `server/build.gradle.kts`)
- `org.apache.parquet:parquet-hadoop` `1.18.1` (Maven, `server/build.gradle.kts`)
- `org.assertj:assertj-core` `3.27.7` (Maven, `server/build.gradle.kts`)
- `org.assertj:assertj-core` `3.27.7` (Maven, `server/trino/build.gradle.kts`)
- `org.awaitility:awaitility` `4.3.0` (Maven, `server/build.gradle.kts`)
- ... (+535 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0["982c8ecb-4a51-4c52-906d-bc6506c36ae0"]:::atlasCategory
        mod_bench["bench"]:::atlasCategory
        mod_ci["ci"]:::atlasCategory
        mod_hedgerow["hedgerow"]:::atlasCategory
        mod_millrace["millrace"]:::atlasCategory
        mod_pyhoglake["pyhoglake"]:::atlasCategory
        mod_pyhoglake_variant_codec["pyhoglake-variant-codec"]:::atlasCategory
        mod_pyhoglake_variant_codec_fuzz["pyhoglake-variant-codec/fuzz"]:::atlasCategory
        mod_server["server"]:::atlasCategory
        mod_server_trino["server/trino"]:::atlasCategory
        mod_webui["webui"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_bench_Dockerfile["bench/Dockerfile"]:::atlasWorkflow
        art_ci_docker_compose_live_millrace_yml["ci/docker-compose.live-millrace.yml"]:::atlasWorkflow
        art_millrace_Dockerfile["millrace/Dockerfile"]:::atlasWorkflow
        art_server_Dockerfile["server/Dockerfile"]:::atlasWorkflow
        art_server_docker_compose_yml["server/docker-compose.yml"]:::atlasWorkflow
        art_webui_Dockerfile["webui/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_bench_image_yml_image["bench-image.yml#image"]:::atlasJob
        job_bench_image_yml_publish["bench-image.yml#publish"]:::atlasJob
        job_ci_python_yml_codec_version["ci-python.yml#codec-version"]:::atlasJob
        job_ci_python_yml_millrace["ci-python.yml#millrace"]:::atlasJob
        job_ecr_release_yml_publish["ecr-release.yml#publish"]:::atlasJob
        job_fuzz_yml_fuzz["fuzz.yml#fuzz"]:::atlasJob
        job_fuzz_yml_variant_codec["fuzz.yml#variant-codec"]:::atlasJob
        job_migration_chain_yml_migration_chain["migration-chain.yml#migration-chain"]:::atlasJob
        job_millrace_image_yml_image["millrace-image.yml#image"]:::atlasJob
        job_millrace_image_yml_publish["millrace-image.yml#publish"]:::atlasJob
        job_publish_pyhoglake_variant_codec_yml_github_release["publish-pyhoglake-variant-codec.yml#github-release"]:::atlasJob
        job_publish_pyhoglake_variant_codec_yml_publish["publish-pyhoglake-variant-codec.yml#publish"]:::atlasJob
        job_publish_pyhoglake_yml_codec["publish-pyhoglake.yml#codec"]:::atlasJob
        job_publish_pyhoglake_yml_github_release["publish-pyhoglake.yml#github-release"]:::atlasJob
        job_publish_pyhoglake_yml_publish["publish-pyhoglake.yml#publish"]:::atlasJob
        job_pyhoglake_checks_yml_build["pyhoglake-checks.yml#build"]:::atlasJob
        job_pyhoglake_checks_yml_lint["pyhoglake-checks.yml#lint"]:::atlasJob
        job_pyhoglake_checks_yml_pyarrow["pyhoglake-checks.yml#pyarrow"]:::atlasJob
        job_pyhoglake_checks_yml_test["pyhoglake-checks.yml#test"]:::atlasJob
        job_pyhoglake_checks_yml_variant_codec["pyhoglake-checks.yml#variant-codec"]:::atlasJob
        job_python_live_yml_live["python-live.yml#live"]:::atlasJob
        job_python_live_yml_live_millrace["python-live.yml#live-millrace"]:::atlasJob
        job_semgrep_yml_semgrep_general["semgrep.yml#semgrep-general"]:::atlasJob
        job_semgrep_yml_semgrep_jvm["semgrep.yml#semgrep-jvm"]:::atlasJob
        job_semgrep_yml_semgrep_python["semgrep.yml#semgrep-python"]:::atlasJob
        job_server_yml_deploy["server.yml#deploy"]:::atlasJob
        job_server_yml_hoglite_live["server.yml#hoglite-live"]:::atlasJob
        job_server_yml_image["server.yml#image"]:::atlasJob
        job_server_yml_server_test["server.yml#server-test"]:::atlasJob
        job_server_yml_trino_test["server.yml#trino-test"]:::atlasJob
        job_variant_codec_wheels_yml_manylinux["variant-codec-wheels.yml#manylinux"]:::atlasJob
        job_variant_codec_wheels_yml_others["variant-codec-wheels.yml#others"]:::atlasJob
        job_webui_yml_deploy["webui.yml#deploy"]:::atlasJob
        job_webui_yml_webui_test["webui.yml#webui-test"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_pypi["pypi"]:::atlasTarget
    end
    job_publish_pyhoglake_variant_codec_yml_publish -->|DEPLOYS_TO| env_pypi
    job_publish_pyhoglake_yml_publish -->|DEPLOYS_TO| env_pypi
    mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0 -->|BUILT_BY| job_bench_image_yml_image
    mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0 -->|BUILT_BY| job_millrace_image_yml_image
    mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0 -->|BUILT_BY| job_webui_yml_webui_test
    mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0 -->|DEPLOYED_BY| job_bench_image_yml_publish
    mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0 -->|DEPLOYED_BY| job_millrace_image_yml_publish
    mod_982c8ecb_4a51_4c52_906d_bc6506c36ae0 -->|PACKAGED_BY| art_server_docker_compose_yml
    mod_bench -->|BUILT_BY| job_bench_image_yml_image
    mod_bench -->|BUILT_BY| job_semgrep_yml_semgrep_general
    mod_bench -->|BUILT_BY| job_semgrep_yml_semgrep_python
    mod_bench -->|DEPLOYED_BY| job_bench_image_yml_publish
    mod_bench -->|PACKAGED_BY| art_bench_Dockerfile
    mod_bench -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_ci -->|BUILT_BY| job_bench_image_yml_image
    mod_ci -->|BUILT_BY| job_millrace_image_yml_image
    mod_ci -->|BUILT_BY| job_publish_pyhoglake_yml_codec
    mod_ci -->|BUILT_BY| job_pyhoglake_checks_yml_lint
    mod_ci -->|BUILT_BY| job_pyhoglake_checks_yml_pyarrow
    mod_ci -->|BUILT_BY| job_python_live_yml_live
    mod_ci -->|BUILT_BY| job_python_live_yml_live_millrace
    mod_ci -->|BUILT_BY| job_server_yml_hoglite_live
    mod_ci -->|BUILT_BY| job_server_yml_image
    mod_ci -->|BUILT_BY| job_variant_codec_wheels_yml_manylinux
    mod_ci -->|BUILT_BY| job_variant_codec_wheels_yml_others
    mod_ci -->|BUILT_BY| job_webui_yml_webui_test
    mod_ci -->|DEPLOYED_BY| job_millrace_image_yml_publish
    mod_ci -->|PACKAGED_BY| art_bench_Dockerfile
    mod_ci -->|PACKAGED_BY| art_ci_docker_compose_live_millrace_yml
    mod_ci -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_ci -->|PACKAGED_BY| art_server_Dockerfile
    mod_ci -->|PACKAGED_BY| art_server_docker_compose_yml
    mod_ci -->|PACKAGED_BY| art_webui_Dockerfile
    mod_hedgerow -->|BUILT_BY| job_semgrep_yml_semgrep_general
    mod_hedgerow -->|BUILT_BY| job_semgrep_yml_semgrep_python
    mod_hedgerow -->|PACKAGED_BY| art_bench_Dockerfile
    mod_hedgerow -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_millrace -->|BUILT_BY| job_ci_python_yml_millrace
    mod_millrace -->|BUILT_BY| job_millrace_image_yml_image
    mod_millrace -->|BUILT_BY| job_python_live_yml_live_millrace
    mod_millrace -->|DEPLOYED_BY| job_millrace_image_yml_publish
    mod_millrace -->|PACKAGED_BY| art_bench_Dockerfile
    mod_millrace -->|PACKAGED_BY| art_ci_docker_compose_live_millrace_yml
    mod_millrace -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_pyhoglake -->|BUILT_BY| job_bench_image_yml_image
    mod_pyhoglake -->|BUILT_BY| job_ci_python_yml_codec_version
    mod_pyhoglake -->|BUILT_BY| job_millrace_image_yml_image
    mod_pyhoglake -->|BUILT_BY| job_publish_pyhoglake_yml_codec
    mod_pyhoglake -->|BUILT_BY| job_pyhoglake_checks_yml_build
    mod_pyhoglake -->|BUILT_BY| job_pyhoglake_checks_yml_lint
    mod_pyhoglake -->|BUILT_BY| job_pyhoglake_checks_yml_pyarrow
    mod_pyhoglake -->|BUILT_BY| job_pyhoglake_checks_yml_test
    mod_pyhoglake -->|BUILT_BY| job_pyhoglake_checks_yml_variant_codec
    mod_pyhoglake -->|BUILT_BY| job_semgrep_yml_semgrep_general
    mod_pyhoglake -->|BUILT_BY| job_semgrep_yml_semgrep_python
    mod_pyhoglake -->|BUILT_BY| job_variant_codec_wheels_yml_manylinux
    mod_pyhoglake -->|BUILT_BY| job_variant_codec_wheels_yml_others
    mod_pyhoglake -->|DEPLOYED_BY| job_publish_pyhoglake_variant_codec_yml_github_release
    mod_pyhoglake -->|DEPLOYED_BY| job_publish_pyhoglake_yml_github_release
    mod_pyhoglake -->|PACKAGED_BY| art_bench_Dockerfile
    mod_pyhoglake -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_pyhoglake_variant_codec -->|BUILT_BY| job_ci_python_yml_codec_version
    mod_pyhoglake_variant_codec -->|BUILT_BY| job_publish_pyhoglake_yml_codec
    mod_pyhoglake_variant_codec -->|BUILT_BY| job_pyhoglake_checks_yml_variant_codec
    mod_pyhoglake_variant_codec -->|BUILT_BY| job_variant_codec_wheels_yml_manylinux
    mod_pyhoglake_variant_codec -->|BUILT_BY| job_variant_codec_wheels_yml_others
    mod_pyhoglake_variant_codec -->|DEPLOYED_BY| job_publish_pyhoglake_variant_codec_yml_github_release
    mod_pyhoglake_variant_codec -->|PACKAGED_BY| art_bench_Dockerfile
    mod_pyhoglake_variant_codec -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_pyhoglake_variant_codec_fuzz -->|BUILT_BY| job_fuzz_yml_variant_codec
    mod_server -->|BUILT_BY| job_fuzz_yml_fuzz
    mod_server -->|BUILT_BY| job_migration_chain_yml_migration_chain
    mod_server -->|BUILT_BY| job_semgrep_yml_semgrep_general
    mod_server -->|BUILT_BY| job_semgrep_yml_semgrep_jvm
    mod_server -->|BUILT_BY| job_server_yml_hoglite_live
    mod_server -->|BUILT_BY| job_server_yml_image
    mod_server -->|BUILT_BY| job_server_yml_server_test
    mod_server -->|BUILT_BY| job_server_yml_trino_test
    mod_server -->|BUILT_BY| job_webui_yml_webui_test
    mod_server -->|DEPLOYED_BY| job_ecr_release_yml_publish
    mod_server -->|DEPLOYED_BY| job_server_yml_deploy
    mod_server -->|PACKAGED_BY| art_bench_Dockerfile
    mod_server -->|PACKAGED_BY| art_ci_docker_compose_live_millrace_yml
    mod_server -->|PACKAGED_BY| art_millrace_Dockerfile
    mod_server -->|PACKAGED_BY| art_server_Dockerfile
    mod_server -->|PACKAGED_BY| art_server_docker_compose_yml
    mod_server -->|PACKAGED_BY| art_webui_Dockerfile
    mod_server_trino -->|PACKAGED_BY| art_server_Dockerfile
    mod_webui -->|BUILT_BY| job_webui_yml_webui_test
    mod_webui -->|DEPLOYED_BY| job_ecr_release_yml_publish
    mod_webui -->|DEPLOYED_BY| job_webui_yml_deploy
    mod_webui -->|PACKAGED_BY| art_bench_Dockerfile
    mod_webui -->|PACKAGED_BY| art_server_Dockerfile
    mod_webui -->|PACKAGED_BY| art_server_docker_compose_yml
    mod_webui -->|PACKAGED_BY| art_webui_Dockerfile
    art_bench_Dockerfile -->|BUILT_BY| job_bench_image_yml_image
    art_bench_Dockerfile -->|BUILT_BY| job_bench_image_yml_publish
    art_bench_Dockerfile -->|BUILT_BY| job_semgrep_yml_semgrep_general
    art_bench_Dockerfile -->|BUILT_BY| job_semgrep_yml_semgrep_python
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_millrace_image_yml_image
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_publish_pyhoglake_yml_codec
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_python_live_yml_live
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_python_live_yml_live_millrace
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_server_yml_hoglite_live
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_variant_codec_wheels_yml_manylinux
    art_ci_docker_compose_live_millrace_yml -->|BUILT_BY| job_variant_codec_wheels_yml_others
    art_millrace_Dockerfile -->|BUILT_BY| job_millrace_image_yml_image
    art_millrace_Dockerfile -->|BUILT_BY| job_millrace_image_yml_publish
    art_server_Dockerfile -->|BUILT_BY| job_ecr_release_yml_publish
    art_server_Dockerfile -->|BUILT_BY| job_fuzz_yml_fuzz
    art_server_Dockerfile -->|BUILT_BY| job_migration_chain_yml_migration_chain
    art_server_Dockerfile -->|BUILT_BY| job_semgrep_yml_semgrep_general
    art_server_Dockerfile -->|BUILT_BY| job_semgrep_yml_semgrep_jvm
    art_server_Dockerfile -->|BUILT_BY| job_server_yml_deploy
    art_server_Dockerfile -->|BUILT_BY| job_server_yml_hoglite_live
    art_server_Dockerfile -->|BUILT_BY| job_server_yml_image
    art_server_Dockerfile -->|BUILT_BY| job_server_yml_server_test
    art_server_Dockerfile -->|BUILT_BY| job_server_yml_trino_test
    art_server_docker_compose_yml -->|BUILT_BY| job_fuzz_yml_fuzz
    art_server_docker_compose_yml -->|BUILT_BY| job_migration_chain_yml_migration_chain
    art_server_docker_compose_yml -->|BUILT_BY| job_semgrep_yml_semgrep_general
    art_server_docker_compose_yml -->|BUILT_BY| job_semgrep_yml_semgrep_jvm
    art_server_docker_compose_yml -->|BUILT_BY| job_server_yml_hoglite_live
    art_server_docker_compose_yml -->|BUILT_BY| job_server_yml_server_test
    art_server_docker_compose_yml -->|BUILT_BY| job_server_yml_trino_test
    art_webui_Dockerfile -->|BUILT_BY| job_ecr_release_yml_publish
    art_webui_Dockerfile -->|BUILT_BY| job_webui_yml_deploy
    art_webui_Dockerfile -->|BUILT_BY| job_webui_yml_webui_test
```

- `publish-pyhoglake-variant-codec.yml#publish` (ci_job) --[DEPLOYS_TO]--> `pypi` (environment)
- `publish-pyhoglake.yml#publish` (ci_job) --[DEPLOYS_TO]--> `pypi` (environment)
- `982c8ecb-4a51-4c52-906d-bc6506c36ae0` (code_module) --[BUILT_BY]--> `bench-image.yml#image` (ci_job)
- `982c8ecb-4a51-4c52-906d-bc6506c36ae0` (code_module) --[BUILT_BY]--> `millrace-image.yml#image` (ci_job)
- `982c8ecb-4a51-4c52-906d-bc6506c36ae0` (code_module) --[BUILT_BY]--> `webui.yml#webui-test` (ci_job)
- `982c8ecb-4a51-4c52-906d-bc6506c36ae0` (code_module) --[DEPLOYED_BY]--> `bench-image.yml#publish` (ci_job)
- `982c8ecb-4a51-4c52-906d-bc6506c36ae0` (code_module) --[DEPLOYED_BY]--> `millrace-image.yml#publish` (ci_job)
- `982c8ecb-4a51-4c52-906d-bc6506c36ae0` (code_module) --[PACKAGED_BY]--> `server/docker-compose.yml` (container)
- `bench` (code_module) --[BUILT_BY]--> `bench-image.yml#image` (ci_job)
- `bench` (code_module) --[BUILT_BY]--> `semgrep.yml#semgrep-general` (ci_job)
- `bench` (code_module) --[BUILT_BY]--> `semgrep.yml#semgrep-python` (ci_job)
- `bench` (code_module) --[DEPLOYED_BY]--> `bench-image.yml#publish` (ci_job)
- `bench` (code_module) --[PACKAGED_BY]--> `bench/Dockerfile` (container)
- `bench` (code_module) --[PACKAGED_BY]--> `millrace/Dockerfile` (container)
- `ci` (code_module) --[BUILT_BY]--> `bench-image.yml#image` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `millrace-image.yml#image` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `publish-pyhoglake.yml#codec` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `pyhoglake-checks.yml#lint` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `pyhoglake-checks.yml#pyarrow` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `python-live.yml#live` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `python-live.yml#live-millrace` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `server.yml#hoglite-live` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `server.yml#image` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `variant-codec-wheels.yml#manylinux` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `variant-codec-wheels.yml#others` (ci_job)
- `ci` (code_module) --[BUILT_BY]--> `webui.yml#webui-test` (ci_job)
- `ci` (code_module) --[DEPLOYED_BY]--> `millrace-image.yml#publish` (ci_job)
- `ci` (code_module) --[PACKAGED_BY]--> `bench/Dockerfile` (container)
- `ci` (code_module) --[PACKAGED_BY]--> `ci/docker-compose.live-millrace.yml` (container)
- `ci` (code_module) --[PACKAGED_BY]--> `millrace/Dockerfile` (container)
- `ci` (code_module) --[PACKAGED_BY]--> `server/Dockerfile` (container)
- `ci` (code_module) --[PACKAGED_BY]--> `server/docker-compose.yml` (container)
- `ci` (code_module) --[PACKAGED_BY]--> `webui/Dockerfile` (container)
- `hedgerow` (code_module) --[BUILT_BY]--> `semgrep.yml#semgrep-general` (ci_job)
- `hedgerow` (code_module) --[BUILT_BY]--> `semgrep.yml#semgrep-python` (ci_job)
- `hedgerow` (code_module) --[PACKAGED_BY]--> `bench/Dockerfile` (container)
- `hedgerow` (code_module) --[PACKAGED_BY]--> `millrace/Dockerfile` (container)
- `millrace` (code_module) --[BUILT_BY]--> `ci-python.yml#millrace` (ci_job)
- `millrace` (code_module) --[BUILT_BY]--> `millrace-image.yml#image` (ci_job)
- `millrace` (code_module) --[BUILT_BY]--> `python-live.yml#live-millrace` (ci_job)


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
  pipeline_root(["PostHog/hoglake (16 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (11 workflows · 38 jobs)"]
    direction TB
    subgraph sg_wf_0_Bench_image["Bench image (3 jobs)"]
      direction TB
      wf_0_Bench_image(["Trigger: Bench image"]):::atlasWorkflow
      job_0_python_live["python-live"]:::atlasJob
      job_0_image["image"]:::atlasJob
      job_0_publish["publish"]:::atlasJob
      wf_0_Bench_image --> job_0_python_live
      wf_0_Bench_image --> job_0_image
      job_0_image --> job_0_publish
      job_0_python_live --> job_0_publish
    end
    pipeline_root --> wf_0_Bench_image
    subgraph sg_wf_1_CI_python["CI python (7 jobs)"]
      direction TB
      wf_1_CI_python(["Trigger: CI python"]):::atlasWorkflow
      job_1_changes["changes"]:::atlasJob
      job_1_python_checks["python-checks"]:::atlasJob
      job_1_pyhoglake["pyhoglake"]:::atlasJob
      wf_1_CI_python --> job_1_changes
      job_1_changes --> job_1_python_checks
      job_1_pyhoglake --> job_1_python_checks
      job_1_changes --> job_1_pyhoglake
    end
    pipeline_root --> wf_1_CI_python
    subgraph sg_wf_6_Millrace_image["Millrace image (3 jobs)"]
      direction TB
      wf_6_Millrace_image(["Trigger: Millrace image"]):::atlasWorkflow
      job_6_python_live["python-live"]:::atlasJob
      job_6_image["image"]:::atlasJob
      job_6_publish["publish"]:::atlasJob
      wf_6_Millrace_image --> job_6_python_live
      wf_6_Millrace_image --> job_6_image
      job_6_image --> job_6_publish
      job_6_python_live --> job_6_publish
    end
    pipeline_root --> wf_6_Millrace_image
    subgraph sg_wf_9_pyhoglake_checks["pyhoglake checks (6 jobs)"]
      direction TB
      wf_9_pyhoglake_checks(["Trigger: pyhoglake checks"]):::atlasWorkflow
      job_9_python_live["python-live"]:::atlasJob
      job_9_lint["lint"]:::atlasJob
      job_9_test["test"]:::atlasJob
      wf_9_pyhoglake_checks --> job_9_python_live
      wf_9_pyhoglake_checks --> job_9_lint
      wf_9_pyhoglake_checks --> job_9_test
    end
    pipeline_root --> wf_9_pyhoglake_checks
    subgraph sg_wf_12_Server["Server (8 jobs)"]
      direction TB
      wf_12_Server(["Trigger: Server"]):::atlasWorkflow
      job_12_changes["changes"]:::atlasJob
      job_12_python_live["python-live"]:::atlasJob
      job_12_server_checks["server-checks"]:::atlasJob
      wf_12_Server --> job_12_changes
      job_12_changes --> job_12_python_live
      job_12_changes --> job_12_server_checks
      job_12_python_live --> job_12_server_checks
    end
    pipeline_root --> wf_12_Server
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (3 workflows · 9 jobs)"]
    direction TB
    subgraph sg_wf_3_ECR_release["ECR release (2 jobs)"]
      direction TB
      wf_3_ECR_release(["Trigger: ECR release"]):::atlasWorkflow
      job_3_gate["gate"]:::atlasJob
      wf_3_ECR_release --> job_3_gate
    end
    pipeline_root --> wf_3_ECR_release
    wf_7_Publish_pyhoglake_variant_codec["Publish pyhoglake-variant-codec (3 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_7_Publish_pyhoglake_variant_codec
    wf_8_Publish_pyhoglake["Publish pyhoglake (4 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_8_Publish_pyhoglake
  end
  subgraph sg_grp_2_Automation___Other["Automation & Other (1 workflows · 2 jobs)"]
    direction TB
    wf_14_Variant_codec_wheels["Variant codec wheels (2 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_14_Variant_codec_wheels
  end
  subgraph sg_grp_3_Scheduled___Manual["Scheduled & Manual (1 workflows · 3 jobs)"]
    direction TB
    wf_4_Fuzz_nightly["Fuzz nightly (3 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_4_Fuzz_nightly
  end
  wf_more["+6 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
