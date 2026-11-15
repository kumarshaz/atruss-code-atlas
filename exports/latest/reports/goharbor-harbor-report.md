---
title: Architecture — goharbor/harbor
description: Arc42 and Pipeline report for goharbor/harbor
---

# Repository Architecture Analysis: goharbor/harbor

## Metadata
- **SHA**: `e7dbdea223486b177ce87b6c954eaad756dd0b4f`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.26
- **avg_cyclomatic_complexity**: 3.6
- **component_count**: 5
- **dead_code_count**: 5
- **dead_code_symbols**: 5 entry(ies)
- **duplication_pct**: 69.3
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 50
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Go Service
- **import_edges**: 100 entry(ies)
- **loc**: 2493
- **max_cognitive_complexity**: 91
- **max_cyclomatic_complexity**: 77
- **sloc**: 1961
- **test_file_count**: 1207

# Architecture: goharbor/harbor

## Context
- **Repository**: `goharbor/harbor`
- **SHA**: `e7dbdea223486b177ce87b6c954eaad756dd0b4f`
- **Ecosystem**: Go
- **Framework**: Go Service

## Building Block View

```mermaid
graph TD;
    JaegerExporter["JaegerExporter : SERVICE"]
    OtelExporter["OtelExporter : SERVICE"]
    gencert["gencert : CLI_COMMAND"]
    migrate["migrate : CLI_COMMAND"]
    prepare["prepare : CLI_COMMAND"]
    repo_root(["goharbor/harbor"])
    repo_root --> JaegerExporter
    repo_root --> OtelExporter
    repo_root --> gencert
    repo_root --> migrate
    repo_root --> prepare
```

## Component Details
- **JaegerExporter** (`make/photon/prepare/models.py`): SERVICE
- **OtelExporter** (`make/photon/prepare/models.py`): SERVICE
- **gencert** (`make/photon/prepare/commands/gencerts.py`): CLI_COMMAND
- **migrate** (`make/photon/prepare/commands/migrate.py`): CLI_COMMAND
- **prepare** (`make/photon/prepare/commands/prepare.py`): CLI_COMMAND

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (41.57/100)
- **Technical Debt Score**: 58.43
- **Estimated Remediation Effort**: 114.72h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 37.60 | 0.20 | avg_cc=3.60, max_cc=77, duplication=69.30%, dead_code=5 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=2193, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 57.00 | 0.15 | avg_cognitive=3.26, max_cognitive=91, fitness_violations=3, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=11, operational_antipatterns=21, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=15, pipeline_security_findings=20 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (69.3) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (91.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (77.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 2193 | **Vulnerabilities**: 0 | **Secrets**: 15

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `src/common/http/transport_test.go:78` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `src/common/http/transport_test.go:154` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `src/common/http/transport_test.go:296` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/common/utils/uaa/test/uaa-token.json:1` (`...,"token_type":"bearer","refresh_token":"eyJh***REDACTED***","expires_in":43199,"jti":"279a6b614a33...`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/common/utils/uaa/test/uaa-token.json:1` (`{"access_token":"eyJh***REDACTED***","token_type":"bearer","refresh_token":...`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/core/controllers/oidc_test.go:17` (`refreshToken:  "eyJh***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/core/controllers/oidc_test.go:29` (`refreshToken:  "eyJh***REDACTED***",`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `src/core/service/token/test/private_key.pem:1` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `src/jobservice/server.key:1` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/pkg/oidc/fix_test.go:25` (`Secret: "<enc***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/pkg/oidc/metamanager_test.go:17` (`var encSecret = "<enc***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/pkg/reg/adapter/awsecr/adapter_test.go:396` (`"authorizationToken" : "QVdT***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/pkg/reg/adapter/huawei/huawei_adapter_test.go:33` (`Credential:  &model.Credential{AccessKey: "cn-n***REDACTED***", AccessSecret: "2f7ec95070592fd4838a3aa4fd09338c047fd1cd654b3422197318f97281cd9"},`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/pkg/reg/adapter/huawei/image_registry_test.go:39` (`Credential:  &model.Credential{AccessKey: "cn-n***REDACTED***", AccessSecret: "f31e8e2b948265afdae32e83722a7705fd43e154585ff69e64108247750e5d"},`)
- **[HIGH] `ATRUSS-SEC-005`** at `src/pkg/registry/auth/bearer/authorizer_test.go:32` (`token := "eyJ0***REDACTED***"`)

### Inventory Sample
- `github.com/FZambia/sentinel` `1.1.1` (golang, `src/go.mod`)
- `github.com/Masterminds/semver/v3` `3.5.0` (golang, `src/go.mod`)
- `github.com/aliyun/alibaba-cloud-sdk-go` `1.63.107` (golang, `src/go.mod`)
- `github.com/asaskevich/govalidator` `0.0.0-20230301143203-a9d515a09cc2` (golang, `src/go.mod`)
- `github.com/aws/aws-sdk-go-v2` `1.46.0` (golang, `src/go.mod`)
- `github.com/aws/aws-sdk-go-v2/config` `1.32.20` (golang, `src/go.mod`)
- `github.com/aws/aws-sdk-go-v2/credentials` `1.20.3` (golang, `src/go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/ecr` `1.58.0` (golang, `src/go.mod`)
- `github.com/aws/smithy-go` `1.28.1` (golang, `src/go.mod`)
- `github.com/beego/beego/v2` `2.3.10` (golang, `src/go.mod`)
- `github.com/beego/i18n` `0.0.0-20140604031826-e87155e8f0c0` (golang, `src/go.mod`)
- `github.com/bmatcuk/doublestar` `1.3.4` (golang, `src/go.mod`)
- `github.com/casbin/casbin/v3` `3.11.0` (golang, `src/go.mod`)
- `github.com/cenkalti/backoff/v4` `4.3.0` (golang, `src/go.mod`)
- `github.com/cloudevents/sdk-go/v2` `2.16.2` (golang, `src/go.mod`)
- `github.com/coreos/go-oidc/v3` `3.15.0` (golang, `src/go.mod`)
- `github.com/dghubble/sling` `1.4.2` (golang, `src/go.mod`)
- `github.com/docker/distribution` `2.8.3+incompatible` (golang, `src/go.mod`)
- `github.com/docker/libtrust` `0.0.0-20160708172513-aabc10ec26b7` (golang, `src/go.mod`)
- `github.com/go-asn1-ber/asn1-ber` `1.5.8` (golang, `src/go.mod`)
- `github.com/go-ldap/ldap/v3` `3.4.14` (golang, `src/go.mod`)
- `github.com/go-openapi/errors` `0.22.8` (golang, `src/go.mod`)
- `github.com/go-openapi/loads` `0.25.2` (golang, `src/go.mod`)
- `github.com/go-openapi/runtime` `0.33.2` (golang, `src/go.mod`)
- `github.com/go-openapi/spec` `1.0.0` (golang, `src/go.mod`)
- `github.com/go-openapi/strfmt` `0.27.1` (golang, `src/go.mod`)
- `github.com/go-openapi/swag` `0.23.1` (golang, `src/go.mod`)
- `github.com/go-openapi/validate` `1.0.0` (golang, `src/go.mod`)
- `github.com/gocarina/gocsv` `0.0.0-20210516172204-ca9e8a8ddea8` (golang, `src/go.mod`)
- `github.com/goccy/go-yaml` `1.19.2` (golang, `src/go.mod`)
- ... (+2163 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod__oss_scanner[".oss-scanner"]
        mod_make_photon_common["make/photon/common"]
        mod_make_photon_core["make/photon/core"]
        mod_make_photon_db["make/photon/db"]
        mod_make_photon_exporter["make/photon/exporter"]
        mod_make_photon_jobservice["make/photon/jobservice"]
        mod_make_photon_log["make/photon/log"]
        mod_make_photon_nginx["make/photon/nginx"]
        mod_make_photon_portal["make/photon/portal"]
        mod_make_photon_prepare["make/photon/prepare"]
        mod_make_photon_registry["make/photon/registry"]
        mod_make_photon_registryctl["make/photon/registryctl"]
        mod_make_photon_standalone_db_migrator["make/photon/standalone-db-migrator"]
        mod_make_photon_trivy_adapter["make/photon/trivy-adapter"]
        mod_make_photon_valkey["make/photon/valkey"]
        mod_src["src"]
        mod_src_portal["src/portal"]
        mod_src_portal_app_swagger_ui["src/portal/app-swagger-ui"]
        mod_src_portal_docker_build["src/portal/docker-build"]
        mod_src_portal_server["src/portal/server"]
        mod_tests["tests"]
        mod_tests_robot_cases_Group2_Longevity["tests/robot-cases/Group2-Longevity"]
        mod_tests_test_engine_image["tests/test-engine-image"]
        mod_tools_migrate_chart["tools/migrate_chart"]
        mod_tools_mockery["tools/mockery"]
        mod_tools_spectral["tools/spectral"]
        mod_tools_swagger["tools/swagger"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__oss_scanner_Dockerfile[".oss-scanner/Dockerfile"]
        art_make_photon_common_Dockerfile["make/photon/common/Dockerfile"]
        art_make_photon_core_Dockerfile["make/photon/core/Dockerfile"]
        art_make_photon_core_Dockerfile_base["make/photon/core/Dockerfile.base"]
        art_make_photon_db_Dockerfile["make/photon/db/Dockerfile"]
        art_make_photon_db_Dockerfile_base["make/photon/db/Dockerfile.base"]
        art_make_photon_exporter_Dockerfile["make/photon/exporter/Dockerfile"]
        art_make_photon_exporter_Dockerfile_base["make/photon/exporter/Dockerfile.base"]
        art_make_photon_jobservice_Dockerfile["make/photon/jobservice/Dockerfile"]
        art_make_photon_jobservice_Dockerfile_base["make/photon/jobservice/Dockerfile.base"]
        art_make_photon_log_Dockerfile["make/photon/log/Dockerfile"]
        art_make_photon_log_Dockerfile_base["make/photon/log/Dockerfile.base"]
        art_make_photon_nginx_Dockerfile["make/photon/nginx/Dockerfile"]
        art_make_photon_nginx_Dockerfile_base["make/photon/nginx/Dockerfile.base"]
        art_make_photon_portal_Dockerfile["make/photon/portal/Dockerfile"]
        art_make_photon_portal_Dockerfile_base["make/photon/portal/Dockerfile.base"]
        art_make_photon_prepare_Dockerfile["make/photon/prepare/Dockerfile"]
        art_make_photon_prepare_Dockerfile_base["make/photon/prepare/Dockerfile.base"]
        art_make_photon_registry_Dockerfile["make/photon/registry/Dockerfile"]
        art_make_photon_registry_Dockerfile_base["make/photon/registry/Dockerfile.base"]
        art_make_photon_registry_Dockerfile_binary["make/photon/registry/Dockerfile.binary"]
        art_make_photon_registryctl_Dockerfile["make/photon/registryctl/Dockerfile"]
        art_make_photon_registryctl_Dockerfile_base["make/photon/registryctl/Dockerfile.base"]
        art_make_photon_standalone_db_migrator_Dockerfile["make/photon/standalone-db-migrator/Dockerfile"]
        art_make_photon_trivy_adapter_Dockerfile["make/photon/trivy-adapter/Dockerfile"]
        art_make_photon_trivy_adapter_Dockerfile_base["make/photon/trivy-adapter/Dockerfile.base"]
        art_make_photon_trivy_adapter_Dockerfile_binary["make/photon/trivy-adapter/Dockerfile.binary"]
        art_make_photon_valkey_Dockerfile["make/photon/valkey/Dockerfile"]
        art_make_photon_valkey_Dockerfile_base["make/photon/valkey/Dockerfile.base"]
        art_src_portal_docker_build_Dockerfile["src/portal/docker-build/Dockerfile"]
        art_tests_docker_compose_test_yml["tests/docker-compose.test.yml"]
        art_tests_robot_cases_Group2_Longevity_Dockerfile_longevity["tests/robot-cases/Group2-Longevity/Dockerfile.longevity"]
        art_tests_test_engine_image_Dockerfile_api_test["tests/test-engine-image/Dockerfile.api_test"]
        art_tests_test_engine_image_Dockerfile_common["tests/test-engine-image/Dockerfile.common"]
        art_tests_test_engine_image_Dockerfile_ui_test["tests/test-engine-image/Dockerfile.ui_test"]
        art_tools_migrate_chart_Dockerfile["tools/migrate_chart/Dockerfile"]
        art_tools_mockery_Dockerfile["tools/mockery/Dockerfile"]
        art_tools_spectral_Dockerfile["tools/spectral/Dockerfile"]
        art_tools_swagger_Dockerfile["tools/swagger/Dockerfile"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_CI_yml_APITEST_DB["CI.yml#APITEST_DB"]
        job_CI_yml_APITEST_DB_PROXY_CACHE["CI.yml#APITEST_DB_PROXY_CACHE"]
        job_CI_yml_APITEST_LDAP["CI.yml#APITEST_LDAP"]
        job_CI_yml_OFFLINE["CI.yml#OFFLINE"]
        job_CI_yml_UI_UT["CI.yml#UI_UT"]
        job_CI_yml_UTTEST["CI.yml#UTTEST"]
        job_build_package_yml_BUILD_BASE_IMAGE["build-package.yml#BUILD_BASE_IMAGE"]
        job_build_package_yml_BUILD_PACKAGE["build-package.yml#BUILD_PACKAGE"]
        job_conformance_test_yml_CONFORMANCE_TEST["conformance_test.yml#CONFORMANCE_TEST"]
        job_publish_release_yml_release["publish_release.yml#release"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_aws["aws"]
    end
    job_conformance_test_yml_CONFORMANCE_TEST -->|DEPLOYS_TO| env_aws
    job_publish_release_yml_release -->|DEPLOYS_TO| env_aws
    mod__oss_scanner -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_common -->|BUILT_BY| job_build_package_yml_BUILD_BASE_IMAGE
    mod_make_photon_common -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_common_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_core_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_exporter_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_jobservice_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_registry_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_registryctl_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_make_photon_trivy_adapter_Dockerfile
    mod_make_photon_common -->|PACKAGED_BY| art_tests_docker_compose_test_yml
    mod_make_photon_common -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_common
    mod_make_photon_core -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_core -->|PACKAGED_BY| art_make_photon_core_Dockerfile
    mod_make_photon_core -->|PACKAGED_BY| art_make_photon_core_Dockerfile_base
    mod_make_photon_core -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile_base
    mod_make_photon_core -->|PACKAGED_BY| art_tests_docker_compose_test_yml
    mod_make_photon_db -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_db -->|PACKAGED_BY| art_make_photon_db_Dockerfile
    mod_make_photon_db -->|PACKAGED_BY| art_make_photon_db_Dockerfile_base
    mod_make_photon_db -->|PACKAGED_BY| art_make_photon_standalone_db_migrator_Dockerfile
    mod_make_photon_db -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile_base
    mod_make_photon_db -->|PACKAGED_BY| art_tests_docker_compose_test_yml
    mod_make_photon_db -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_api_test
    mod_make_photon_db -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_ui_test
    mod_make_photon_exporter -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_exporter -->|PACKAGED_BY| art_make_photon_exporter_Dockerfile
    mod_make_photon_exporter -->|PACKAGED_BY| art_make_photon_exporter_Dockerfile_base
    mod_make_photon_jobservice -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_jobservice -->|PACKAGED_BY| art_make_photon_jobservice_Dockerfile
    mod_make_photon_jobservice -->|PACKAGED_BY| art_make_photon_jobservice_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_core_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_exporter_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_jobservice_Dockerfile
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_jobservice_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_log_Dockerfile
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_log_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_nginx_Dockerfile
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_nginx_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_portal_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_registry_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_registryctl_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_trivy_adapter_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile_base
    mod_make_photon_log -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_make_photon_log -->|PACKAGED_BY| art_tools_mockery_Dockerfile
    mod_make_photon_nginx -->|PACKAGED_BY| art_make_photon_nginx_Dockerfile
    mod_make_photon_nginx -->|PACKAGED_BY| art_make_photon_nginx_Dockerfile_base
    mod_make_photon_nginx -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_make_photon_nginx -->|PACKAGED_BY| art_make_photon_portal_Dockerfile_base
    mod_make_photon_nginx -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_make_photon_portal -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_portal -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_make_photon_portal -->|PACKAGED_BY| art_make_photon_portal_Dockerfile_base
    mod_make_photon_portal -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_make_photon_prepare -->|PACKAGED_BY| art_make_photon_core_Dockerfile
    mod_make_photon_prepare -->|PACKAGED_BY| art_make_photon_prepare_Dockerfile
    mod_make_photon_prepare -->|PACKAGED_BY| art_make_photon_prepare_Dockerfile_base
    mod_make_photon_registry -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_db_Dockerfile
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_registry_Dockerfile
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_registry_Dockerfile_base
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_registry_Dockerfile_binary
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_registryctl_Dockerfile
    mod_make_photon_registry -->|PACKAGED_BY| art_make_photon_registryctl_Dockerfile_base
    mod_make_photon_registry -->|PACKAGED_BY| art_tests_docker_compose_test_yml
    mod_make_photon_registryctl -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_registryctl -->|PACKAGED_BY| art_make_photon_registryctl_Dockerfile
    mod_make_photon_registryctl -->|PACKAGED_BY| art_make_photon_registryctl_Dockerfile_base
    mod_make_photon_standalone_db_migrator -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_make_photon_standalone_db_migrator -->|PACKAGED_BY| art_make_photon_standalone_db_migrator_Dockerfile
    mod_make_photon_trivy_adapter -->|PACKAGED_BY| art_make_photon_trivy_adapter_Dockerfile
    mod_make_photon_trivy_adapter -->|PACKAGED_BY| art_make_photon_trivy_adapter_Dockerfile_base
    mod_make_photon_trivy_adapter -->|PACKAGED_BY| art_make_photon_trivy_adapter_Dockerfile_binary
    mod_make_photon_valkey -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile
    mod_make_photon_valkey -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile_base
    mod_make_photon_valkey -->|PACKAGED_BY| art_tests_docker_compose_test_yml
    mod_src -->|BUILT_BY| job_CI_yml_APITEST_DB
    mod_src -->|BUILT_BY| job_CI_yml_APITEST_DB_PROXY_CACHE
    mod_src -->|BUILT_BY| job_CI_yml_APITEST_LDAP
    mod_src -->|BUILT_BY| job_CI_yml_OFFLINE
    mod_src -->|BUILT_BY| job_CI_yml_UI_UT
    mod_src -->|BUILT_BY| job_CI_yml_UTTEST
    mod_src -->|DEPLOYED_BY| job_build_package_yml_BUILD_PACKAGE
    mod_src -->|DEPLOYED_BY| job_conformance_test_yml_CONFORMANCE_TEST
    mod_src -->|DEPLOYED_BY| job_publish_release_yml_release
    mod_src -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_src -->|PACKAGED_BY| art_make_photon_core_Dockerfile
    mod_src -->|PACKAGED_BY| art_make_photon_exporter_Dockerfile
    mod_src -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_src -->|PACKAGED_BY| art_make_photon_prepare_Dockerfile
    mod_src -->|PACKAGED_BY| art_make_photon_registry_Dockerfile_binary
    mod_src -->|PACKAGED_BY| art_make_photon_trivy_adapter_Dockerfile_binary
    mod_src -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_src -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_common
    mod_src_portal -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_src_portal -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_src_portal -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_src_portal_app_swagger_ui -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_src_portal_app_swagger_ui -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_src_portal_app_swagger_ui -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_src_portal_docker_build -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_src_portal_server -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_src_portal_server -->|PACKAGED_BY| art_make_photon_db_Dockerfile_base
    mod_src_portal_server -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile
    mod_src_portal_server -->|PACKAGED_BY| art_make_photon_valkey_Dockerfile_base
    mod_tests -->|BUILT_BY| job_CI_yml_APITEST_DB
    mod_tests -->|BUILT_BY| job_CI_yml_APITEST_DB_PROXY_CACHE
    mod_tests -->|BUILT_BY| job_CI_yml_APITEST_LDAP
    mod_tests -->|BUILT_BY| job_CI_yml_OFFLINE
    mod_tests -->|BUILT_BY| job_CI_yml_UI_UT
    mod_tests -->|BUILT_BY| job_CI_yml_UTTEST
    mod_tests -->|DEPLOYED_BY| job_build_package_yml_BUILD_PACKAGE
    mod_tests -->|DEPLOYED_BY| job_conformance_test_yml_CONFORMANCE_TEST
    mod_tests -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_tests -->|PACKAGED_BY| art_tests_docker_compose_test_yml
    mod_tests_robot_cases_Group2_Longevity -->|PACKAGED_BY| art_tests_robot_cases_Group2_Longevity_Dockerfile_longevity
    mod_tests_test_engine_image -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_api_test
    mod_tests_test_engine_image -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_common
    mod_tests_test_engine_image -->|PACKAGED_BY| art_tests_test_engine_image_Dockerfile_ui_test
    mod_tools_migrate_chart -->|PACKAGED_BY| art_tools_migrate_chart_Dockerfile
    mod_tools_mockery -->|PACKAGED_BY| art_tools_mockery_Dockerfile
    mod_tools_spectral -->|PACKAGED_BY| art_tools_spectral_Dockerfile
    mod_tools_swagger -->|PACKAGED_BY| art__oss_scanner_Dockerfile
    mod_tools_swagger -->|PACKAGED_BY| art_make_photon_portal_Dockerfile
    mod_tools_swagger -->|PACKAGED_BY| art_src_portal_docker_build_Dockerfile
    mod_tools_swagger -->|PACKAGED_BY| art_tools_swagger_Dockerfile
    art_make_photon_common_Dockerfile -->|BUILT_BY| job_build_package_yml_BUILD_BASE_IMAGE
    art_tests_docker_compose_test_yml -->|BUILT_BY| job_CI_yml_APITEST_DB
    art_tests_docker_compose_test_yml -->|BUILT_BY| job_CI_yml_APITEST_DB_PROXY_CACHE
    art_tests_docker_compose_test_yml -->|BUILT_BY| job_CI_yml_APITEST_LDAP
    art_tests_docker_compose_test_yml -->|BUILT_BY| job_CI_yml_OFFLINE
    art_tests_docker_compose_test_yml -->|BUILT_BY| job_CI_yml_UI_UT
    art_tests_docker_compose_test_yml -->|BUILT_BY| job_CI_yml_UTTEST
    art_tests_docker_compose_test_yml -->|DEPLOYED_BY| job_build_package_yml_BUILD_PACKAGE
    art_tests_docker_compose_test_yml -->|DEPLOYED_BY| job_conformance_test_yml_CONFORMANCE_TEST
```

- `conformance_test.yml#CONFORMANCE_TEST` (ci_job) --[DEPLOYS_TO]--> `aws` (environment)
- `publish_release.yml#release` (ci_job) --[DEPLOYS_TO]--> `aws` (environment)
- `.oss-scanner` (code_module) --[PACKAGED_BY]--> `.oss-scanner/Dockerfile` (container)
- `make/photon/common` (code_module) --[BUILT_BY]--> `build-package.yml#BUILD_BASE_IMAGE` (ci_job)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `.oss-scanner/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/common/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/core/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/exporter/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/jobservice/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/registry/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/registryctl/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `make/photon/trivy-adapter/Dockerfile` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `tests/docker-compose.test.yml` (container)
- `make/photon/common` (code_module) --[PACKAGED_BY]--> `tests/test-engine-image/Dockerfile.common` (container)
- `make/photon/core` (code_module) --[PACKAGED_BY]--> `.oss-scanner/Dockerfile` (container)
- `make/photon/core` (code_module) --[PACKAGED_BY]--> `make/photon/core/Dockerfile` (container)
- `make/photon/core` (code_module) --[PACKAGED_BY]--> `make/photon/core/Dockerfile.base` (container)
- `make/photon/core` (code_module) --[PACKAGED_BY]--> `make/photon/valkey/Dockerfile.base` (container)
- `make/photon/core` (code_module) --[PACKAGED_BY]--> `tests/docker-compose.test.yml` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `.oss-scanner/Dockerfile` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `make/photon/db/Dockerfile` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `make/photon/db/Dockerfile.base` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `make/photon/standalone-db-migrator/Dockerfile` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `make/photon/valkey/Dockerfile.base` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `tests/docker-compose.test.yml` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `tests/test-engine-image/Dockerfile.api_test` (container)
- `make/photon/db` (code_module) --[PACKAGED_BY]--> `tests/test-engine-image/Dockerfile.ui_test` (container)
- `make/photon/exporter` (code_module) --[PACKAGED_BY]--> `.oss-scanner/Dockerfile` (container)
- `make/photon/exporter` (code_module) --[PACKAGED_BY]--> `make/photon/exporter/Dockerfile` (container)
- `make/photon/exporter` (code_module) --[PACKAGED_BY]--> `make/photon/exporter/Dockerfile.base` (container)
- `make/photon/jobservice` (code_module) --[PACKAGED_BY]--> `.oss-scanner/Dockerfile` (container)
- `make/photon/jobservice` (code_module) --[PACKAGED_BY]--> `make/photon/jobservice/Dockerfile` (container)
- `make/photon/jobservice` (code_module) --[PACKAGED_BY]--> `make/photon/jobservice/Dockerfile.base` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/core/Dockerfile.base` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/exporter/Dockerfile.base` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/jobservice/Dockerfile` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/jobservice/Dockerfile.base` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/log/Dockerfile` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/log/Dockerfile.base` (container)
- `make/photon/log` (code_module) --[PACKAGED_BY]--> `make/photon/nginx/Dockerfile` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["goharbor/harbor (11 workflows)"])
  grp_0_CI___Verification["CI & Verification (5 workflows · 17 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Scheduled___Manual["Scheduled & Manual (3 workflows · 3 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  grp_2_Release___Deploy["Release & Deploy (2 workflows · 2 jobs)"]
  pipeline_root --> grp_2_Release___Deploy
  grp_3_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
  pipeline_root --> grp_3_Security___Governance
```
