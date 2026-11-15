---
title: Architecture — keycloak/keycloak-client
description: Arc42 and Pipeline report for keycloak/keycloak-client
---

# Repository Architecture Analysis: keycloak/keycloak-client

## Metadata
- **SHA**: `332a5deae89555d4d8adc1a7108def58fb405e65`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.72
- **avg_cyclomatic_complexity**: 1.51
- **component_count**: 15
- **dead_code_count**: 15
- **dead_code_symbols**: 15 entry(ies)
- **duplication_pct**: 92.79
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 596
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Java Maven/Gradle
- **import_edges**: 100 entry(ies)
- **loc**: 86021
- **max_cognitive_complexity**: 82
- **max_cyclomatic_complexity**: 45
- **sloc**: 54761
- **test_file_count**: 127

# Architecture: keycloak/keycloak-client

## Context
- **Repository**: `keycloak/keycloak-client`
- **SHA**: `332a5deae89555d4d8adc1a7108def58fb405e65`
- **Ecosystem**: Java
- **Framework**: Java Maven/Gradle

## Building Block View

```mermaid
graph TD;
    keycloak_admin_client["keycloak-admin-client : MODULE"]
    keycloak_admin_client_jackson3["keycloak-admin-client-jackson3 : MODULE"]
    keycloak_authz_client["keycloak-authz-client : MODULE"]
    keycloak_client_common_synced["keycloak-client-common-synced : MODULE"]
    keycloak_client_common_synced_jackson3["keycloak-client-common-synced-jackson3 : MODULE"]
    keycloak_client_guides["keycloak-client-guides : MODULE"]
    keycloak_client_guides_maven_plugin["keycloak-client-guides-maven-plugin : MODULE"]
    keycloak_client_docs_parent["keycloak-client-docs-parent : MODULE"]
    keycloak_policy_enforcer["keycloak-policy-enforcer : MODULE"]
    keycloak_client_parent["keycloak-client-parent : MODULE"]
    keycloak_admin_client_testsuite["keycloak-admin-client-testsuite : MODULE"]
    keycloak_autz_client_testsuite["keycloak-autz-client-testsuite : MODULE"]
    keycloak_client_testsuite_framework["keycloak-client-testsuite-framework : MODULE"]
    keycloak_client_testsuite_parent["keycloak-client-testsuite-parent : MODULE"]
    keycloak_client_testsuite_providers["keycloak-client-testsuite-providers : MODULE"]
    repo_root(["keycloak/keycloak-client"])
    repo_root --> keycloak_admin_client
    repo_root --> keycloak_admin_client_jackson3
    repo_root --> keycloak_admin_client_testsuite
    repo_root --> keycloak_authz_client
    repo_root --> keycloak_autz_client_testsuite
    repo_root --> keycloak_client_common_synced
    repo_root --> keycloak_client_common_synced_jackson3
    repo_root --> keycloak_client_docs_parent
    repo_root --> keycloak_client_guides
    repo_root --> keycloak_client_guides_maven_plugin
    repo_root --> keycloak_client_parent
    repo_root --> keycloak_client_testsuite_framework
    repo_root --> keycloak_client_testsuite_parent
    repo_root --> keycloak_client_testsuite_providers
    repo_root --> keycloak_policy_enforcer
```

## Component Details
- **keycloak-admin-client** (`admin-client/pom.xml`): MODULE
- **keycloak-admin-client-jackson3** (`admin-client-jackson3/pom.xml`): MODULE
- **keycloak-authz-client** (`authz-client/pom.xml`): MODULE
- **keycloak-client-common-synced** (`client-common-synced/pom.xml`): MODULE
- **keycloak-client-common-synced-jackson3** (`client-common-synced-jackson3/pom.xml`): MODULE
- **keycloak-client-guides** (`docs/guides/pom.xml`): MODULE
- **keycloak-client-guides-maven-plugin** (`docs/maven-plugin/pom.xml`): MODULE
- **keycloak-client-docs-parent** (`docs/pom.xml`): MODULE
- **keycloak-policy-enforcer** (`policy-enforcer/pom.xml`): MODULE
- **keycloak-client-parent** (`pom.xml`): MODULE
- **keycloak-admin-client-testsuite** (`testsuite/admin-client-tests/pom.xml`): MODULE
- **keycloak-autz-client-testsuite** (`testsuite/authz-tests/pom.xml`): MODULE
- **keycloak-client-testsuite-framework** (`testsuite/framework/pom.xml`): MODULE
- **keycloak-client-testsuite-parent** (`testsuite/pom.xml`): MODULE
- **keycloak-client-testsuite-providers** (`testsuite/providers/pom.xml`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (38.25/100)
- **Technical Debt Score**: 61.75
- **Estimated Remediation Effort**: 91.25h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.00 | 0.20 | avg_cc=1.51, max_cc=45, duplication=92.79%, dead_code=15 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=60, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=0.72, max_cognitive=82, fitness_violations=3, oversized_files=13 |
| Pipeline Health | `F` | 23.00 | 0.15 | workflows=7, operational_antipatterns=12, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=2, pipeline_security_findings=9 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (92.79) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (82.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (45.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 60 | **Vulnerabilities**: 0 | **Secrets**: 2

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `client-common-synced/src/main/java/org/keycloak/common/util/PemUtils.java:41` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `client-common-synced/src/main/java/org/keycloak/common/util/PemUtils.java:43` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `com.fasterxml.jackson.core:jackson-annotations` `*` (Maven, `admin-client/pom.xml`)
- `com.fasterxml.jackson.core:jackson-annotations` `*` (Maven, `authz-client/pom.xml`)
- `com.fasterxml.jackson.core:jackson-annotations` `*` (Maven, `client-common-synced-jackson3/pom.xml`)
- `com.fasterxml.jackson.core:jackson-annotations` `*` (Maven, `client-common-synced/pom.xml`)
- `com.fasterxml.jackson.core:jackson-core` `*` (Maven, `admin-client/pom.xml`)
- `com.fasterxml.jackson.core:jackson-core` `*` (Maven, `authz-client/pom.xml`)
- `com.fasterxml.jackson.core:jackson-core` `*` (Maven, `client-common-synced/pom.xml`)
- `com.fasterxml.jackson.core:jackson-databind` `*` (Maven, `authz-client/pom.xml`)
- `com.fasterxml.jackson.core:jackson-databind` `*` (Maven, `client-common-synced/pom.xml`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jdk8` `*` (Maven, `admin-client/pom.xml`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jdk8` `*` (Maven, `authz-client/pom.xml`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jdk8` `*` (Maven, `client-common-synced/pom.xml`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jsr310` `*` (Maven, `admin-client/pom.xml`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jsr310` `*` (Maven, `authz-client/pom.xml`)
- `com.fasterxml.jackson.datatype:jackson-datatype-jsr310` `*` (Maven, `client-common-synced/pom.xml`)
- `com.fasterxml.jackson.jakarta.rs:jackson-jakarta-rs-yaml-provider` `*` (Maven, `admin-client/pom.xml`)
- `com.github.dasniko:testcontainers-keycloak` `*` (Maven, `testsuite/framework/pom.xml`)
- `commons-io:commons-io` `*` (Maven, `testsuite/framework/pom.xml`)
- `dev.resteasy.providers:resteasy-jackson-provider` `*` (Maven, `admin-client-jackson3/pom.xml`)
- `io.undertow:undertow-core` `*` (Maven, `testsuite/authz-tests/pom.xml`)
- `jakarta.servlet:jakarta.servlet-api` `*` (Maven, `policy-enforcer/pom.xml`)
- `org.apache.httpcomponents:httpclient` `*` (Maven, `authz-client/pom.xml`)
- `org.apache.logging.log4j:log4j-slf4j2-impl` `*` (Maven, `testsuite/framework/pom.xml`)
- `org.apache.maven.plugin-tools:maven-plugin-annotations` `*` (Maven, `docs/maven-plugin/pom.xml`)
- `org.apache.maven:maven-core` `*` (Maven, `docs/maven-plugin/pom.xml`)
- `org.apache.maven:maven-plugin-api` `*` (Maven, `docs/maven-plugin/pom.xml`)
- `org.eclipse.microprofile.openapi:microprofile-openapi-api` `*` (Maven, `admin-client-jackson3/pom.xml`)
- `org.eclipse.microprofile.openapi:microprofile-openapi-api` `*` (Maven, `admin-client/pom.xml`)
- `org.eclipse.microprofile.openapi:microprofile-openapi-api` `*` (Maven, `authz-client/pom.xml`)
- `org.eclipse.microprofile.openapi:microprofile-openapi-api` `*` (Maven, `client-common-synced-jackson3/pom.xml`)
- ... (+30 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_admin_client["admin-client"]
        mod_admin_client_jackson3["admin-client-jackson3"]
        mod_authz_client["authz-client"]
        mod_client_common_synced["client-common-synced"]
        mod_client_common_synced_jackson3["client-common-synced-jackson3"]
        mod_testsuite["testsuite"]
        mod_testsuite_admin_client_tests["testsuite/admin-client-tests"]
        mod_testsuite_authz_tests["testsuite/authz-tests"]
        mod_testsuite_providers["testsuite/providers"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_run_tests_yml_client_tests_jackson3["run-tests.yml#client-tests-jackson3"]
        job_run_tests_yml_client_tests_java_11["run-tests.yml#client-tests-java-11"]
        job_run_tests_yml_client_tests_srv_26["run-tests.yml#client-tests-srv-26"]
        job_run_tests_yml_client_tests_srv_nightly["run-tests.yml#client-tests-srv-nightly"]
        job_sync_and_send_pr_yml_sync["sync-and-send-pr.yml#sync"]
    end
    mod_admin_client -->|BUILT_BY| job_run_tests_yml_client_tests_jackson3
    mod_admin_client -->|BUILT_BY| job_run_tests_yml_client_tests_java_11
    mod_admin_client -->|BUILT_BY| job_run_tests_yml_client_tests_srv_26
    mod_admin_client -->|BUILT_BY| job_run_tests_yml_client_tests_srv_nightly
    mod_admin_client -->|BUILT_BY| job_sync_and_send_pr_yml_sync
    mod_admin_client_jackson3 -->|BUILT_BY| job_run_tests_yml_client_tests_jackson3
    mod_admin_client_jackson3 -->|BUILT_BY| job_sync_and_send_pr_yml_sync
    mod_authz_client -->|BUILT_BY| job_sync_and_send_pr_yml_sync
    mod_client_common_synced -->|BUILT_BY| job_sync_and_send_pr_yml_sync
    mod_client_common_synced_jackson3 -->|BUILT_BY| job_sync_and_send_pr_yml_sync
    mod_testsuite -->|BUILT_BY| job_run_tests_yml_client_tests_jackson3
    mod_testsuite -->|BUILT_BY| job_run_tests_yml_client_tests_java_11
    mod_testsuite -->|BUILT_BY| job_run_tests_yml_client_tests_srv_26
    mod_testsuite -->|BUILT_BY| job_run_tests_yml_client_tests_srv_nightly
    mod_testsuite_admin_client_tests -->|BUILT_BY| job_run_tests_yml_client_tests_jackson3
    mod_testsuite_admin_client_tests -->|BUILT_BY| job_run_tests_yml_client_tests_java_11
    mod_testsuite_admin_client_tests -->|BUILT_BY| job_run_tests_yml_client_tests_srv_26
    mod_testsuite_admin_client_tests -->|BUILT_BY| job_run_tests_yml_client_tests_srv_nightly
    mod_testsuite_authz_tests -->|BUILT_BY| job_run_tests_yml_client_tests_java_11
    mod_testsuite_authz_tests -->|BUILT_BY| job_run_tests_yml_client_tests_srv_26
    mod_testsuite_authz_tests -->|BUILT_BY| job_run_tests_yml_client_tests_srv_nightly
    mod_testsuite_providers -->|BUILT_BY| job_run_tests_yml_client_tests_jackson3
    mod_testsuite_providers -->|BUILT_BY| job_run_tests_yml_client_tests_java_11
    mod_testsuite_providers -->|BUILT_BY| job_run_tests_yml_client_tests_srv_26
    mod_testsuite_providers -->|BUILT_BY| job_run_tests_yml_client_tests_srv_nightly
```

- `admin-client` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-jackson3` (ci_job)
- `admin-client` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-java-11` (ci_job)
- `admin-client` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-26` (ci_job)
- `admin-client` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-nightly` (ci_job)
- `admin-client` (code_module) --[BUILT_BY]--> `sync-and-send-pr.yml#sync` (ci_job)
- `admin-client-jackson3` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-jackson3` (ci_job)
- `admin-client-jackson3` (code_module) --[BUILT_BY]--> `sync-and-send-pr.yml#sync` (ci_job)
- `authz-client` (code_module) --[BUILT_BY]--> `sync-and-send-pr.yml#sync` (ci_job)
- `client-common-synced` (code_module) --[BUILT_BY]--> `sync-and-send-pr.yml#sync` (ci_job)
- `client-common-synced-jackson3` (code_module) --[BUILT_BY]--> `sync-and-send-pr.yml#sync` (ci_job)
- `testsuite` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-jackson3` (ci_job)
- `testsuite` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-java-11` (ci_job)
- `testsuite` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-26` (ci_job)
- `testsuite` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-nightly` (ci_job)
- `testsuite/admin-client-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-jackson3` (ci_job)
- `testsuite/admin-client-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-java-11` (ci_job)
- `testsuite/admin-client-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-26` (ci_job)
- `testsuite/admin-client-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-nightly` (ci_job)
- `testsuite/authz-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-java-11` (ci_job)
- `testsuite/authz-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-26` (ci_job)
- `testsuite/authz-tests` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-nightly` (ci_job)
- `testsuite/providers` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-jackson3` (ci_job)
- `testsuite/providers` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-java-11` (ci_job)
- `testsuite/providers` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-26` (ci_job)
- `testsuite/providers` (code_module) --[BUILT_BY]--> `run-tests.yml#client-tests-srv-nightly` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["keycloak/keycloak-client (7 workflows)"])
  grp_0_Scheduled___Manual["Scheduled & Manual (4 workflows · 6 jobs)"]
  pipeline_root --> grp_0_Scheduled___Manual
  grp_1_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]
  pipeline_root --> grp_1_Release___Deploy
  grp_2_CI___Verification["CI & Verification (1 workflows · 4 jobs)"]
  pipeline_root --> grp_2_CI___Verification
```
