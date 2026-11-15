---
title: Architecture — grafana/grafana
description: Arc42 and Pipeline report for grafana/grafana
---

# Repository Architecture Analysis: grafana/grafana

## Metadata
- **SHA**: `3f36380cfd6240f348c2a6226f6fb07647746d60`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 4.88
- **avg_cyclomatic_complexity**: 3.5
- **component_count**: 261
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.01
- **file_complexities**: 3 entry(ies)
- **files_analyzed**: 7126
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Go Service
- **import_edges**: 10 entry(ies)
- **loc**: 1785860
- **max_cognitive_complexity**: 25
- **max_cyclomatic_complexity**: 12
- **sloc**: 1458480
- **test_file_count**: 6254

# Architecture: grafana/grafana

## Context
- **Repository**: `grafana/grafana`
- **SHA**: `3f36380cfd6240f348c2a6226f6fb07647746d60`
- **Ecosystem**: Go
- **Framework**: Go Service

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
    repo_root(["grafana/grafana (261 components)"]):::atlasRoot
    dir_0_apps["apps (249)"]:::atlasCategory
    repo_root --> dir_0_apps
    sub_0_0_alerting["alerting (180)"]:::atlasWorkflow
    dir_0_apps --> sub_0_0_alerting
    sub_0_1_advisor["advisor (69)"]:::atlasWorkflow
    dir_0_apps --> sub_0_1_advisor
    dir_1_devenv["devenv (10)"]:::atlasCategory
    repo_root --> dir_1_devenv
    sub_1_0_docker_blocks_auth["docker/blocks/auth (9)"]:::atlasWorkflow
    dir_1_devenv --> sub_1_0_docker_blocks_auth
    sub_1_1_docker_blocks_alert_webhook_listener["docker/blocks/alert_webhook_listener (1)"]:::atlasWorkflow
    dir_1_devenv --> sub_1_1_docker_blocks_alert_webhook_listener
    dir_2__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_2__root_
    dir_3__github[".github (1)"]:::atlasCategory
    repo_root --> dir_3__github
```

## Component Details

Showing top 60 representative components out of 261 across 4 module group(s):

- **Module `apps`** (249 components — module: 249)
- **Module `devenv`** (10 components — module: 10)
- **Module `(root)`** (1 components — module: 1)
- **Module `.github`** (1 components — MODULE: 1)

- **advisor_manifest** (`apps/advisor/pkg/apis/advisor_manifest.go`): module
- **alertenrichment_client_gen** (`apps/alerting/alertenrichment/pkg/generated/alertenrichment/v1beta1/alertenrichment_client_gen.go`): module
- **alertenrichment_codec_gen** (`apps/alerting/alertenrichment/pkg/generated/alertenrichment/v1beta1/alertenrichment_codec_gen.go`): module
- **alertenrichment_manifest** (`apps/alerting/alertenrichment/pkg/generated/manifestdata/alertenrichment_manifest.go`): module
- **alertenrichment_object_gen** (`apps/alerting/alertenrichment/pkg/generated/alertenrichment/v1beta1/alertenrichment_object_gen.go`): module
- **alertenrichment_schema_gen** (`apps/alerting/alertenrichment/pkg/generated/alertenrichment/v1beta1/alertenrichment_schema_gen.go`): module
- **alertenrichment_spec_gen** (`apps/alerting/alertenrichment/pkg/generated/alertenrichment/v1beta1/alertenrichment_spec_gen.go`): module
- **alertingnotifications_manifest** (`apps/alerting/notifications/pkg/apis/alertingnotifications_manifest.go`): module
- **alertrule_client_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_client_gen.go`): module
- **alertrule_client_gen** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_client_gen.go`): module
- **alertrule_codec_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_codec_gen.go`): module
- **alertrule_codec_gen** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_codec_gen.go`): module
- **alertrule_ext** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_ext.go`): module
- **alertrule_ext** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_ext.go`): module
- **alertrule_object_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_object_gen.go`): module
- **alertrule_object_gen** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_object_gen.go`): module
- **alertrule_schema_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_schema_gen.go`): module
- **alertrule_schema_gen** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_schema_gen.go`): module
- **alertrule_spec_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_spec_gen.go`): module
- **alertrule_spec_gen** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_spec_gen.go`): module
- **alertrule_status_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/alertrule_status_gen.go`): module
- **alertrule_status_gen** (`apps/alerting/rules/pkg/apis/alerting/v1beta1/alertrule_status_gen.go`): module
- **app** (`apps/advisor/pkg/app/app.go`): module
- **app** (`apps/alerting/notifications/pkg/app/app.go`): module
- **changelog** (`.github/actions/changelog/package.json`): MODULE
- **check** (`apps/advisor/pkg/app/checks/authchecks/check.go`): module
- **check** (`apps/advisor/pkg/app/checks/configchecks/check.go`): module
- **check** (`apps/advisor/pkg/app/checks/datasourcecheck/check.go`): module
- **check** (`apps/advisor/pkg/app/checks/instancechecks/check.go`): module
- **check** (`apps/advisor/pkg/app/checks/plugincheck/check.go`): module
- **check_client_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/check_client_gen.go`): module
- **check_codec_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/check_codec_gen.go`): module
- **check_object_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/check_object_gen.go`): module
- **check_schema_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/check_schema_gen.go`): module
- **check_spec_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/check_spec_gen.go`): module
- **check_status_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/check_status_gen.go`): module
- **check_test** (`apps/advisor/pkg/app/checks/authchecks/check_test.go`): module
- **check_test** (`apps/advisor/pkg/app/checks/datasourcecheck/check_test.go`): module
- **check_test** (`apps/advisor/pkg/app/checks/instancechecks/check_test.go`): module
- **check_test** (`apps/advisor/pkg/app/checks/plugincheck/check_test.go`): module
- **checkregistry** (`apps/advisor/pkg/app/checkregistry/checkregistry.go`): module
- **checkregistry_test** (`apps/advisor/pkg/app/checkregistry/checkregistry_test.go`): module
- **checkscheduler** (`apps/advisor/pkg/app/checkscheduler/checkscheduler.go`): module
- **checkscheduler_test** (`apps/advisor/pkg/app/checkscheduler/checkscheduler_test.go`): module
- **checktype_client_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/checktype_client_gen.go`): module
- **checktype_codec_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/checktype_codec_gen.go`): module
- **checktype_object_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/checktype_object_gen.go`): module
- **checktype_schema_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/checktype_schema_gen.go`): module
- **checktype_spec_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/checktype_spec_gen.go`): module
- **checktype_status_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/checktype_status_gen.go`): module
- **checktyperegisterer** (`apps/advisor/pkg/app/checktyperegisterer/checktyperegisterer.go`): module
- **checktyperegisterer_test** (`apps/advisor/pkg/app/checktyperegisterer/checktyperegisterer_test.go`): module
- **client_gen** (`apps/advisor/pkg/apis/advisor/v0alpha1/client_gen.go`): module
- **client_gen** (`apps/alerting/notifications/pkg/apis/alertingnotifications/v0alpha1/client_gen.go`): module
- **client_gen** (`apps/alerting/notifications/pkg/apis/alertingnotifications/v1beta1/client_gen.go`): module
- **client_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/client_gen.go`): module
- **config** (`apps/alerting/notifications/pkg/app/config.go`): module
- **config_client_gen** (`apps/alerting/notifications/pkg/apis/alertingnotifications/v0alpha1/config_client_gen.go`): module
- **config_client_gen** (`apps/alerting/notifications/pkg/apis/alertingnotifications/v1beta1/config_client_gen.go`): module
- **config_client_gen** (`apps/alerting/rules/pkg/apis/alerting/v0alpha1/config_client_gen.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (56.72/100)
- **Technical Debt Score**: 43.28
- **Estimated Remediation Effort**: 275.82h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 97.98 | 0.20 | avg_cc=3.50, max_cc=12, duplication=0.01%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=5610, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 92.50 | 0.15 | avg_cognitive=4.88, max_cognitive=25, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=100, operational_antipatterns=239, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=4, pipeline_security_findings=64 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

### Workspace Packages
- **github.com/grafana/grafana** (`.`, go, go) -> internal deps: `github.com/grafana/grafana/apps/advisor, github.com/grafana/grafana/apps/alerting/alertenrichment, github.com/grafana/grafana/apps/alerting/alertrulequality, github.com/grafana/grafana/apps/alerting/notifications, github.com/grafana/grafana/apps/alerting/rules, github.com/grafana/grafana/apps/annotation, github.com/grafana/grafana/apps/collections, github.com/grafana/grafana/apps/correlations, github.com/grafana/grafana/apps/dashboard, github.com/grafana/grafana/apps/dashvalidator, github.com/grafana/grafana/apps/example, github.com/grafana/grafana/apps/folder, github.com/grafana/grafana/apps/iam, github.com/grafana/grafana/apps/live, github.com/grafana/grafana/apps/logsdrilldown, github.com/grafana/grafana/apps/playlist, github.com/grafana/grafana/apps/plugins, github.com/grafana/grafana/apps/preferences, github.com/grafana/grafana/apps/provisioning, github.com/grafana/grafana/apps/quotas, github.com/grafana/grafana/apps/scope, github.com/grafana/grafana/apps/secret, github.com/grafana/grafana/apps/shorturl, github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/apiserver, github.com/grafana/grafana/pkg/infra/features, github.com/grafana/grafana/pkg/infra/log, github.com/grafana/grafana/pkg/infra/metrics, github.com/grafana/grafana/pkg/infra/slugify, github.com/grafana/grafana/pkg/infra/tracing, github.com/grafana/grafana/pkg/legacyapi, github.com/grafana/grafana/pkg/plugins, github.com/grafana/grafana/pkg/storage/dbproxy, github.com/grafana/grafana/pkg/storage/unified/apistore, github.com/grafana/grafana/pkg/storage/unified/resource/kv, github.com/grafana/grafana/pkg/storage/unified/resourceclient, github.com/grafana/grafana/pkg/storage/unified/resourcepb, github.com/grafana/grafana/pkg/util/sqlite`
- **github.com/grafana/grafana/apps/advisor** (`apps/advisor`, go, go) -> internal deps: `github.com/grafana/grafana, github.com/grafana/grafana/apps/provisioning, github.com/grafana/grafana/apps/secret, github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/apiserver, github.com/grafana/grafana/pkg/infra/features, github.com/grafana/grafana/pkg/infra/log, github.com/grafana/grafana/pkg/infra/metrics, github.com/grafana/grafana/pkg/infra/slugify, github.com/grafana/grafana/pkg/infra/tracing, github.com/grafana/grafana/pkg/plugins, github.com/grafana/grafana/pkg/storage/unified/resourcepb, github.com/grafana/grafana/pkg/util/sqlite`
- **github.com/grafana/grafana/apps/alerting/alertenrichment** (`apps/alerting/alertenrichment`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/alerting/alertrulequality** (`apps/alerting/alertrulequality`, go, go)
- **github.com/grafana/grafana/apps/alerting/notifications** (`apps/alerting/notifications`, go, go)
- **github.com/grafana/grafana/apps/alerting/rules** (`apps/alerting/rules`, go, go)
- **github.com/grafana/grafana/apps/annotation** (`apps/annotation`, go, go)
- **github.com/grafana/grafana/apps/collections** (`apps/collections`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/correlations** (`apps/correlations`, go, go)
- **github.com/grafana/grafana/apps/dashboard** (`apps/dashboard`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/dashvalidator** (`apps/dashvalidator`, go, go) -> internal deps: `github.com/grafana/grafana, github.com/grafana/grafana/apps/annotation, github.com/grafana/grafana/apps/dashboard, github.com/grafana/grafana/apps/folder, github.com/grafana/grafana/apps/iam, github.com/grafana/grafana/apps/provisioning, github.com/grafana/grafana/apps/secret, github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/apiserver, github.com/grafana/grafana/pkg/infra/features, github.com/grafana/grafana/pkg/infra/log, github.com/grafana/grafana/pkg/infra/metrics, github.com/grafana/grafana/pkg/infra/slugify, github.com/grafana/grafana/pkg/infra/tracing, github.com/grafana/grafana/pkg/plugins, github.com/grafana/grafana/pkg/storage/unified/resourcepb, github.com/grafana/grafana/pkg/util/sqlite`
- **github.com/grafana/grafana/apps/example** (`apps/example`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/folder** (`apps/folder`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/iam** (`apps/iam`, go, go) -> internal deps: `github.com/grafana/grafana, github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/live** (`apps/live`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/infra/log`
- **github.com/grafana/grafana/apps/logsdrilldown** (`apps/logsdrilldown`, go, go)
- **github.com/grafana/grafana/apps/playlist** (`apps/playlist`, go, go)
- **github.com/grafana/grafana/apps/plugins** (`apps/plugins`, go, go) -> internal deps: `github.com/grafana/grafana, github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/apiserver, github.com/grafana/grafana/pkg/infra/features, github.com/grafana/grafana/pkg/infra/log, github.com/grafana/grafana/pkg/infra/metrics, github.com/grafana/grafana/pkg/infra/tracing, github.com/grafana/grafana/pkg/plugins`
- **github.com/grafana/grafana/apps/preferences** (`apps/preferences`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/provisioning** (`apps/provisioning`, go, go) -> internal deps: `github.com/grafana/grafana/apps/dashboard, github.com/grafana/grafana/apps/secret, github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/quotas** (`apps/quotas`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/storage/unified/resourceclient, github.com/grafana/grafana/pkg/storage/unified/resourcepb`
- **github.com/grafana/grafana/apps/scope** (`apps/scope`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/secret** (`apps/secret`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/apps/shorturl** (`apps/shorturl`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/pkg/apimachinery** (`pkg/apimachinery`, go, go)
- **github.com/grafana/grafana/pkg/apiserver** (`pkg/apiserver`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/pkg/build/wire** (`pkg/build/wire`, go, go)
- **github.com/grafana/grafana/pkg/codegen** (`pkg/codegen`, go, go)
- **github.com/grafana/grafana/pkg/infra/features** (`pkg/infra/features`, go, go)
- **github.com/grafana/grafana/pkg/infra/log** (`pkg/infra/log`, go, go)
- **github.com/grafana/grafana/pkg/infra/metrics** (`pkg/infra/metrics`, go, go)
- **github.com/grafana/grafana/pkg/infra/slugify** (`pkg/infra/slugify`, go, go)
- **github.com/grafana/grafana/pkg/infra/tracing** (`pkg/infra/tracing`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/infra/log`
- **github.com/grafana/grafana/pkg/legacyapi** (`pkg/legacyapi`, go, go) -> internal deps: `github.com/grafana/grafana/apps/dashboard, github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/infra/slugify`
- **github.com/grafana/grafana/pkg/plugins** (`pkg/plugins`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery`
- **github.com/grafana/grafana/pkg/plugins/codegen** (`pkg/plugins/codegen`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/codegen`
- **github.com/grafana/grafana/pkg/storage/dbproxy** (`pkg/storage/dbproxy`, go, go)
- **github.com/grafana/grafana/pkg/storage/unified/apistore** (`pkg/storage/unified/apistore`, go, go) -> internal deps: `github.com/grafana/grafana/apps/alerting/alertrulequality, github.com/grafana/grafana/apps/dashboard, github.com/grafana/grafana/apps/folder, github.com/grafana/grafana/apps/provisioning, github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/apiserver, github.com/grafana/grafana/pkg/storage/unified/resourceclient, github.com/grafana/grafana/pkg/storage/unified/resourcepb`
- **github.com/grafana/grafana/pkg/storage/unified/resource/kv** (`pkg/storage/unified/resource/kv`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/util/sqlite`
- **github.com/grafana/grafana/pkg/storage/unified/resourceclient** (`pkg/storage/unified/resourceclient`, go, go) -> internal deps: `github.com/grafana/grafana/pkg/apimachinery, github.com/grafana/grafana/pkg/storage/unified/resourcepb`

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 5610 | **Vulnerabilities**: 0 | **Secrets**: 4

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `.github/workflows/community-release.yml:41` (`GRAFANABOT_FORUM_KEY=comm***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `.github/workflows/issue-opened.yml:63` (`AUTOTRIAGER_OPENAI_API_KEY=plug***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `.github/workflows/issue-opened.yml:191` (`AUTOTRIAGER_OPENAI_API_KEY=plug***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `apps/advisor/pkg/translations/ja-JP/grafana-advisor.json:13` (`"advisor.datasource.prom-dep-auth.description": "Prom***REDACTED***",`)

### Inventory Sample
- `Jinja2` `3.1.6` (PyPI, `devenv/docker/blocks/collectd/requirements.txt`)
- `MarkupSafe` `2.1.5` (PyPI, `devenv/docker/blocks/collectd/requirements.txt`)
- `envtpl` `0.7.0` (PyPI, `devenv/docker/blocks/collectd/requirements.txt`)
- `cloud.google.com/go/aiplatform` `1.126.0` (golang, `go.mod`)
- `cloud.google.com/go/discoveryengine` `1.33.0` (golang, `go.mod`)
- `cloud.google.com/go/kms` `1.32.0` (golang, `go.mod`)
- `cloud.google.com/go/storage` `1.67.1` (golang, `go.mod`)
- `cuelang.org/go` `0.17.1` (golang, `apps/dashboard/go.mod`)
- `cuelang.org/go` `0.17.1` (golang, `pkg/codegen/go.mod`)
- `cuelang.org/go` `0.17.1` (golang, `pkg/plugins/codegen/go.mod`)
- `dario.cat/mergo` `1.0.2` (golang, `go.mod`)
- `filippo.io/age` `1.3.2` (golang, `go.mod`)
- `github.com/Azure/azure-sdk-for-go` `68.0.0+incompatible` (golang, `go.mod`)
- `github.com/Azure/azure-sdk-for-go/sdk/azcore` `1.23.1` (golang, `go.mod`)
- `github.com/Azure/azure-sdk-for-go/sdk/azidentity` `1.14.1` (golang, `go.mod`)
- `github.com/Azure/azure-sdk-for-go/sdk/keyvault/azkeys` `0.10.0` (golang, `go.mod`)
- `github.com/Azure/azure-sdk-for-go/sdk/storage/azblob` `1.8.0` (golang, `go.mod`)
- `github.com/Azure/go-autorest/autorest` `0.11.30` (golang, `go.mod`)
- `github.com/Azure/go-autorest/autorest/adal` `0.9.24` (golang, `go.mod`)
- `github.com/Bose/minisentinel` `0.0.0-20200130220412-917c5a9223bb` (golang, `go.mod`)
- `github.com/BurntSushi/toml` `1.6.0` (golang, `go.mod`)
- `github.com/DATA-DOG/go-sqlmock` `1.5.2` (golang, `go.mod`)
- `github.com/DATA-DOG/go-sqlmock` `1.5.2` (golang, `pkg/storage/unified/resource/kv/go.mod`)
- `github.com/Machiel/slugify` `1.0.1` (golang, `pkg/plugins/go.mod`)
- `github.com/Masterminds/semver` `1.5.0` (golang, `go.mod`)
- `github.com/Masterminds/semver/v3` `3.5.0` (golang, `apps/advisor/go.mod`)
- `github.com/Masterminds/semver/v3` `3.5.0` (golang, `go.mod`)
- `github.com/Masterminds/semver/v3` `3.5.0` (golang, `pkg/plugins/go.mod`)
- `github.com/Masterminds/sprig/v3` `3.3.0` (golang, `go.mod`)
- `github.com/PaesslerAG/jsonpath` `0.1.1` (golang, `go.mod`)
- ... (+5580 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod__citools_src_cue[".citools/src/cue"]:::atlasCategory
        mod__citools_src_govulncheck[".citools/src/govulncheck"]:::atlasCategory
        mod__github_actions_changelog[".github/actions/changelog"]:::atlasCategory
        mod_apps_dashboard["apps/dashboard"]:::atlasCategory
        mod_devenv_docker_blocks_alert_webhook_listener["devenv/docker/blocks/alert_webhook_listener"]:::atlasCategory
        mod_devenv_docker_blocks_auth_apache_proxy["devenv/docker/blocks/auth/apache_proxy"]:::atlasCategory
        mod_devenv_docker_blocks_auth_apache_proxy_mac["devenv/docker/blocks/auth/apache_proxy_mac"]:::atlasCategory
        mod_devenv_docker_blocks_auth_authentik["devenv/docker/blocks/auth/authentik"]:::atlasCategory
        mod_devenv_docker_blocks_auth_freeipa["devenv/docker/blocks/auth/freeipa"]:::atlasCategory
        mod_devenv_docker_blocks_auth_jwt_proxy["devenv/docker/blocks/auth/jwt_proxy"]:::atlasCategory
        mod_devenv_docker_blocks_auth_nginx_proxy["devenv/docker/blocks/auth/nginx_proxy"]:::atlasCategory
        mod_devenv_docker_blocks_auth_nginx_proxy_mac["devenv/docker/blocks/auth/nginx_proxy_mac"]:::atlasCategory
        mod_devenv_docker_blocks_auth_oauth["devenv/docker/blocks/auth/oauth"]:::atlasCategory
        mod_devenv_docker_blocks_auth_openldap["devenv/docker/blocks/auth/openldap"]:::atlasCategory
        mod_devenv_docker_blocks_auth_openldap_multiple["devenv/docker/blocks/auth/openldap-multiple"]:::atlasCategory
        mod_devenv_docker_blocks_auth_prometheus_basic_auth_proxy["devenv/docker/blocks/auth/prometheus_basic_auth_proxy"]:::atlasCategory
        mod_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure["devenv/docker/blocks/auth/prometheus_oauth2_proxy_azure"]:::atlasCategory
        mod_devenv_docker_blocks_caddy_tls["devenv/docker/blocks/caddy_tls"]:::atlasCategory
        mod_devenv_docker_blocks_clickhouse["devenv/docker/blocks/clickhouse"]:::atlasCategory
        mod_devenv_docker_blocks_collectd["devenv/docker/blocks/collectd"]:::atlasCategory
        mod_devenv_docker_blocks_elastic["devenv/docker/blocks/elastic"]:::atlasCategory
        mod_devenv_docker_blocks_elastic_data["devenv/docker/blocks/elastic/data"]:::atlasCategory
        mod_devenv_docker_blocks_elasticstack["devenv/docker/blocks/elasticstack"]:::atlasCategory
        mod_devenv_docker_blocks_etcd["devenv/docker/blocks/etcd"]:::atlasCategory
        mod_devenv_docker_blocks_grafana["devenv/docker/blocks/grafana"]:::atlasCategory
        mod_devenv_docker_blocks_graphite["devenv/docker/blocks/graphite"]:::atlasCategory
        mod_devenv_docker_blocks_graphite1["devenv/docker/blocks/graphite1"]:::atlasCategory
        mod_devenv_docker_blocks_influxdb["devenv/docker/blocks/influxdb"]:::atlasCategory
        mod_devenv_docker_blocks_influxdb1["devenv/docker/blocks/influxdb1"]:::atlasCategory
        mod_devenv_docker_blocks_jaeger["devenv/docker/blocks/jaeger"]:::atlasCategory
        mod_devenv_docker_blocks_jaegeronly["devenv/docker/blocks/jaegeronly"]:::atlasCategory
        mod_devenv_docker_blocks_loki["devenv/docker/blocks/loki"]:::atlasCategory
        mod_devenv_docker_blocks_loki_promtail["devenv/docker/blocks/loki-promtail"]:::atlasCategory
        mod_devenv_docker_blocks_loki_data["devenv/docker/blocks/loki/data"]:::atlasCategory
        mod_devenv_docker_blocks_maildev["devenv/docker/blocks/maildev"]:::atlasCategory
        mod_devenv_docker_blocks_mariadb["devenv/docker/blocks/mariadb"]:::atlasCategory
        mod_devenv_docker_blocks_memcached["devenv/docker/blocks/memcached"]:::atlasCategory
        mod_devenv_docker_blocks_mimir_backend["devenv/docker/blocks/mimir_backend"]:::atlasCategory
        mod_devenv_docker_blocks_mqtt["devenv/docker/blocks/mqtt"]:::atlasCategory
        mod_devenv_docker_blocks_mssql["devenv/docker/blocks/mssql"]:::atlasCategory
        mod_devenv_docker_blocks_mssql_arm64["devenv/docker/blocks/mssql_arm64"]:::atlasCategory
        mod_devenv_docker_blocks_mssql_tests["devenv/docker/blocks/mssql_tests"]:::atlasCategory
        mod_devenv_docker_blocks_mssql_tls["devenv/docker/blocks/mssql_tls"]:::atlasCategory
        mod_devenv_docker_blocks_mysql["devenv/docker/blocks/mysql"]:::atlasCategory
        mod_devenv_docker_blocks_mysql_exporter["devenv/docker/blocks/mysql_exporter"]:::atlasCategory
        mod_devenv_docker_blocks_mysql_opendata["devenv/docker/blocks/mysql_opendata"]:::atlasCategory
        mod_devenv_docker_blocks_mysql_tests["devenv/docker/blocks/mysql_tests"]:::atlasCategory
        mod_devenv_docker_blocks_opentsdb["devenv/docker/blocks/opentsdb"]:::atlasCategory
        mod_devenv_docker_blocks_pgvector["devenv/docker/blocks/pgvector"]:::atlasCategory
        mod_devenv_docker_blocks_postgres["devenv/docker/blocks/postgres"]:::atlasCategory
        mod_devenv_docker_blocks_postgres_tests["devenv/docker/blocks/postgres_tests"]:::atlasCategory
        mod_devenv_docker_blocks_prometheus["devenv/docker/blocks/prometheus"]:::atlasCategory
        mod_devenv_docker_blocks_prometheus_high_card["devenv/docker/blocks/prometheus_high_card"]:::atlasCategory
        mod_devenv_docker_blocks_prometheus_random_data["devenv/docker/blocks/prometheus_random_data"]:::atlasCategory
        mod_devenv_docker_blocks_prometheus_utf8["devenv/docker/blocks/prometheus_utf8"]:::atlasCategory
        mod_devenv_docker_blocks_pyroscope["devenv/docker/blocks/pyroscope"]:::atlasCategory
        mod_devenv_docker_blocks_redis["devenv/docker/blocks/redis"]:::atlasCategory
        mod_devenv_docker_blocks_self_instrumentation["devenv/docker/blocks/self-instrumentation"]:::atlasCategory
        mod_devenv_docker_blocks_sensugo["devenv/docker/blocks/sensugo"]:::atlasCategory
        mod_devenv_docker_blocks_slow_proxy["devenv/docker/blocks/slow_proxy"]:::atlasCategory
        mod_devenv_docker_blocks_smtp["devenv/docker/blocks/smtp"]:::atlasCategory
        mod_devenv_docker_blocks_stateful_webhook["devenv/docker/blocks/stateful_webhook"]:::atlasCategory
        mod_devenv_docker_blocks_tempo["devenv/docker/blocks/tempo"]:::atlasCategory
        mod_devenv_docker_blocks_traefik["devenv/docker/blocks/traefik"]:::atlasCategory
        mod_devenv_docker_blocks_webdav["devenv/docker/blocks/webdav"]:::atlasCategory
        mod_devenv_docker_blocks_zipkin["devenv/docker/blocks/zipkin"]:::atlasCategory
        mod_devenv_docker_buildcontainer["devenv/docker/buildcontainer"]:::atlasCategory
        mod_devenv_docker_debtest["devenv/docker/debtest"]:::atlasCategory
        mod_devenv_docker_ha_test_unified_alerting["devenv/docker/ha-test-unified-alerting"]:::atlasCategory
        mod_devenv_docker_ha_test["devenv/docker/ha_test"]:::atlasCategory
        mod_devenv_frontend_service["devenv/frontend-service"]:::atlasCategory
        mod_devenv_local_npm["devenv/local-npm"]:::atlasCategory
        mod_devenv_local_cdn["devenv/local_cdn"]:::atlasCategory
        mod_emails["emails"]:::atlasCategory
        mod_github_com_grafana_grafana["github.com/grafana/grafana"]:::atlasCategory
        mod_hack["hack"]:::atlasCategory
        mod_packages_grafana_data["packages/grafana-data"]:::atlasCategory
        mod_packages_grafana_e2e_selectors["packages/grafana-e2e-selectors"]:::atlasCategory
        mod_packages_grafana_schema["packages/grafana-schema"]:::atlasCategory
        mod_packaging_docker_custom["packaging/docker/custom"]:::atlasCategory
        mod_pkg_storage_dbproxy["pkg/storage/dbproxy"]:::atlasCategory
        mod_pkg_storage_unified_resourcepb["pkg/storage/unified/resourcepb"]:::atlasCategory
        mod_scripts_cli["scripts/cli"]:::atlasCategory
        mod_scripts_modowners["scripts/modowners"]:::atlasCategory
        mod_scripts_verify_repo_update["scripts/verify-repo-update"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_alert_webhook_listener_Dockerfile["devenv/docker/blocks/alert_webhook_listener/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_alert_webhook_listener_docker_compose_yaml["devenv/docker/blocks/alert_webhook_listener/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_apache_proxy_Dockerfile["devenv/docker/blocks/auth/apache_proxy/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_apache_proxy_docker_compose_yaml["devenv/docker/blocks/auth/apache_proxy/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_apache_proxy_mac_Dockerfile["devenv/docker/blocks/auth/apache_proxy_mac/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_apache_proxy_mac_docker_compose_yaml["devenv/docker/blocks/auth/apache_proxy_mac/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_authentik_docker_compose_yaml["devenv/docker/blocks/auth/authentik/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_freeipa_docker_compose_yaml["devenv/docker/blocks/auth/freeipa/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_jwt_proxy_docker_compose_yaml["devenv/docker/blocks/auth/jwt_proxy/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_nginx_proxy_docker_compose_yaml["devenv/docker/blocks/auth/nginx_proxy/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_nginx_proxy_mac_Dockerfile["devenv/docker/blocks/auth/nginx_proxy_mac/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_nginx_proxy_mac_docker_compose_yaml["devenv/docker/blocks/auth/nginx_proxy_mac/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_oauth_docker_compose_yaml["devenv/docker/blocks/auth/oauth/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_openldap_multiple_docker_compose_yaml["devenv/docker/blocks/auth/openldap-multiple/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_openldap_docker_compose_yaml["devenv/docker/blocks/auth/openldap/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_prometheus_basic_auth_proxy_Dockerfile["devenv/docker/blocks/auth/prometheus_basic_auth_proxy/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_prometheus_basic_auth_proxy_docker_compose_yaml["devenv/docker/blocks/auth/prometheus_basic_auth_proxy/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure_docker_compose_yaml["devenv/docker/blocks/auth/prometheus_oauth2_proxy_azure/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_caddy_tls_docker_compose_yaml["devenv/docker/blocks/caddy_tls/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_clickhouse_docker_compose_yaml["devenv/docker/blocks/clickhouse/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_collectd_Dockerfile["devenv/docker/blocks/collectd/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_collectd_docker_compose_yaml["devenv/docker/blocks/collectd/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_elastic_data_Dockerfile["devenv/docker/blocks/elastic/data/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_elastic_docker_compose_yaml["devenv/docker/blocks/elastic/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_elasticstack_docker_compose_yaml["devenv/docker/blocks/elasticstack/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_etcd_docker_compose_yaml["devenv/docker/blocks/etcd/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_grafana_docker_compose_yaml["devenv/docker/blocks/grafana/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_graphite_docker_compose_yaml["devenv/docker/blocks/graphite/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_graphite1_docker_compose_yaml["devenv/docker/blocks/graphite1/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_influxdb_docker_compose_yaml["devenv/docker/blocks/influxdb/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_influxdb1_docker_compose_yaml["devenv/docker/blocks/influxdb1/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_jaeger_docker_compose_yaml["devenv/docker/blocks/jaeger/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_jaegeronly_docker_compose_yaml["devenv/docker/blocks/jaegeronly/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_loki_promtail_docker_compose_yaml["devenv/docker/blocks/loki-promtail/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_loki_data_Dockerfile["devenv/docker/blocks/loki/data/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_loki_docker_compose_yaml["devenv/docker/blocks/loki/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_maildev_docker_compose_yaml["devenv/docker/blocks/maildev/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mariadb_docker_compose_yaml["devenv/docker/blocks/mariadb/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_memcached_docker_compose_yaml["devenv/docker/blocks/memcached/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mimir_backend_docker_compose_yaml["devenv/docker/blocks/mimir_backend/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mqtt_docker_compose_yaml["devenv/docker/blocks/mqtt/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mssql_docker_compose_yaml["devenv/docker/blocks/mssql/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mssql_arm64_docker_compose_yaml["devenv/docker/blocks/mssql_arm64/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mssql_tests_docker_compose_yaml["devenv/docker/blocks/mssql_tests/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mssql_tls_docker_compose_yaml["devenv/docker/blocks/mssql_tls/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mysql_docker_compose_yaml["devenv/docker/blocks/mysql/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mysql_exporter_docker_compose_yaml["devenv/docker/blocks/mysql_exporter/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mysql_opendata_Dockerfile["devenv/docker/blocks/mysql_opendata/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_mysql_opendata_docker_compose_yaml["devenv/docker/blocks/mysql_opendata/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_mysql_tests_Dockerfile["devenv/docker/blocks/mysql_tests/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_mysql_tests_docker_compose_yaml["devenv/docker/blocks/mysql_tests/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_opentsdb_docker_compose_yaml["devenv/docker/blocks/opentsdb/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_pgvector_docker_compose_yaml["devenv/docker/blocks/pgvector/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_postgres_docker_compose_yaml["devenv/docker/blocks/postgres/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_postgres_tests_Dockerfile["devenv/docker/blocks/postgres_tests/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_postgres_tests_docker_compose_yaml["devenv/docker/blocks/postgres_tests/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_Dockerfile["devenv/docker/blocks/prometheus/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_docker_compose_yaml["devenv/docker/blocks/prometheus/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_high_card_Dockerfile["devenv/docker/blocks/prometheus_high_card/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_high_card_docker_compose_yaml["devenv/docker/blocks/prometheus_high_card/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_random_data_Dockerfile["devenv/docker/blocks/prometheus_random_data/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_utf8_Dockerfile["devenv/docker/blocks/prometheus_utf8/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_prometheus_utf8_docker_compose_yaml["devenv/docker/blocks/prometheus_utf8/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_pyroscope_docker_compose_yaml["devenv/docker/blocks/pyroscope/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_redis_docker_compose_yaml["devenv/docker/blocks/redis/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml["devenv/docker/blocks/self-instrumentation/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_sensugo_docker_compose_yaml["devenv/docker/blocks/sensugo/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_slow_proxy_Dockerfile["devenv/docker/blocks/slow_proxy/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_slow_proxy_docker_compose_yaml["devenv/docker/blocks/slow_proxy/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_smtp_Dockerfile["devenv/docker/blocks/smtp/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_smtp_docker_compose_yaml["devenv/docker/blocks/smtp/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_stateful_webhook_Dockerfile["devenv/docker/blocks/stateful_webhook/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_blocks_stateful_webhook_docker_compose_yaml["devenv/docker/blocks/stateful_webhook/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_tempo_docker_compose_yaml["devenv/docker/blocks/tempo/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_traefik_docker_compose_yml["devenv/docker/blocks/traefik/docker-compose.yml"]:::atlasWorkflow
        art_devenv_docker_blocks_webdav_docker_compose_yaml["devenv/docker/blocks/webdav/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_blocks_zipkin_docker_compose_yaml["devenv/docker/blocks/zipkin/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_buildcontainer_Dockerfile["devenv/docker/buildcontainer/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_debtest_Dockerfile["devenv/docker/debtest/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_ha_test_unified_alerting_Dockerfile["devenv/docker/ha-test-unified-alerting/Dockerfile"]:::atlasWorkflow
        art_devenv_docker_ha_test_unified_alerting_docker_compose_yaml["devenv/docker/ha-test-unified-alerting/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_docker_ha_test_docker_compose_yaml["devenv/docker/ha_test/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_frontend_service_docker_compose_yaml["devenv/frontend-service/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_local_npm_docker_compose_yaml["devenv/local-npm/docker-compose.yaml"]:::atlasWorkflow
        art_devenv_local_cdn_docker_compose_yaml["devenv/local_cdn/docker-compose.yaml"]:::atlasWorkflow
        art_packaging_docker_custom_Dockerfile["packaging/docker/custom/Dockerfile"]:::atlasWorkflow
        art_scripts_verify_repo_update_Dockerfile_deb["scripts/verify-repo-update/Dockerfile.deb"]:::atlasWorkflow
        art_scripts_verify_repo_update_Dockerfile_rpm["scripts/verify-repo-update/Dockerfile.rpm"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_backend_code_checks_yml_validate_configs["backend-code-checks.yml#validate-configs"]:::atlasJob
        job_changelog_yml_main["changelog.yml#main"]:::atlasJob
        job_deploy_frontend_preview_yml_deploy["deploy-frontend-preview.yml#deploy"]:::atlasJob
        job_deploy_storybook_preview_yml_deploy_storybook_preview["deploy-storybook-preview.yml#deploy-storybook-preview"]:::atlasJob
        job_external_fr_weekly_digest_yml_digest["external-fr-weekly-digest.yml#digest"]:::atlasJob
        job_external_issue_weekly_digest_yml_digest["external-issue-weekly-digest.yml#digest"]:::atlasJob
        job_external_pr_weekly_digest_yml_report["external-pr-weekly-digest.yml#report"]:::atlasJob
        job_govulncheck_yml_govulncheck["govulncheck.yml#govulncheck"]:::atlasJob
        job_modowners_reviewers_yml_request["modowners-reviewers.yml#request"]:::atlasJob
        job_pr_bundle_size_yml_build["pr-bundle-size.yml#build"]:::atlasJob
        job_pr_bundle_size_yml_bundle_size["pr-bundle-size.yml#bundle-size"]:::atlasJob
        job_pr_frontend_unit_tests_yml_generate_golden_files["pr-frontend-unit-tests.yml#generate-golden-files"]:::atlasJob
        job_pr_k8s_codegen_check_yml_check["pr-k8s-codegen-check.yml#check"]:::atlasJob
        job_pr_resource_search_result_format_yml_check["pr-resource-search-result-format.yml#check"]:::atlasJob
        job_pr_test_integration_yml_postgres["pr-test-integration.yml#postgres"]:::atlasJob
        job_pr_test_integration_yml_postgres_enterprise["pr-test-integration.yml#postgres-enterprise"]:::atlasJob
        job_proto_breaking_changes_yml_generated["proto-breaking-changes.yml#generated"]:::atlasJob
        job_release_npm_yml_publish["release-npm.yml#publish"]:::atlasJob
        job_release_pr_yml_create_prs["release-pr.yml#create-prs"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_____github_event_name_____workflow_dispatch______manual_trigger__________["${{ github.event_name == 'workflow_dispatch' && 'manual-trigger' || '' }}"]:::atlasTarget
        env_frontend_preview_pr_____needs_check_outputs_pr_number___["frontend-preview-pr-${{ needs.check.outputs.pr-number }}"]:::atlasTarget
        env_npm_publish["npm-publish"]:::atlasTarget
        env_storybook_pr_preview_____github_event_pull_request_number___["storybook-pr-preview-${{ github.event.pull_request.number }}"]:::atlasTarget
    end
    job_deploy_frontend_preview_yml_deploy -->|DEPLOYS_TO| env_frontend_preview_pr_____needs_check_outputs_pr_number___
    job_deploy_storybook_preview_yml_deploy_storybook_preview -->|DEPLOYS_TO| env_storybook_pr_preview_____github_event_pull_request_number___
    job_external_fr_weekly_digest_yml_digest -->|DEPLOYS_TO| env_____github_event_name_____workflow_dispatch______manual_trigger__________
    job_external_issue_weekly_digest_yml_digest -->|DEPLOYS_TO| env_____github_event_name_____workflow_dispatch______manual_trigger__________
    job_external_pr_weekly_digest_yml_report -->|DEPLOYS_TO| env_____github_event_name_____workflow_dispatch______manual_trigger__________
    job_release_npm_yml_publish -->|DEPLOYS_TO| env_npm_publish
    mod__citools_src_cue -->|PACKAGED_BY| art_Dockerfile
    mod__citools_src_govulncheck -->|BUILT_BY| job_govulncheck_yml_govulncheck
    mod__github_actions_changelog -->|BUILT_BY| job_changelog_yml_main
    mod__github_actions_changelog -->|DEPLOYED_BY| job_release_pr_yml_create_prs
    mod_apps_dashboard -->|BUILT_BY| job_pr_frontend_unit_tests_yml_generate_golden_files
    mod_devenv_docker_blocks_alert_webhook_listener -->|PACKAGED_BY| art_devenv_docker_blocks_alert_webhook_listener_Dockerfile
    mod_devenv_docker_blocks_alert_webhook_listener -->|PACKAGED_BY| art_devenv_docker_blocks_alert_webhook_listener_docker_compose_yaml
    mod_devenv_docker_blocks_auth_apache_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_Dockerfile
    mod_devenv_docker_blocks_auth_apache_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_auth_apache_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_mac_docker_compose_yaml
    mod_devenv_docker_blocks_auth_apache_proxy_mac -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_mac_Dockerfile
    mod_devenv_docker_blocks_auth_apache_proxy_mac -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_mac_docker_compose_yaml
    mod_devenv_docker_blocks_auth_authentik -->|PACKAGED_BY| art_devenv_docker_blocks_auth_authentik_docker_compose_yaml
    mod_devenv_docker_blocks_auth_freeipa -->|PACKAGED_BY| art_devenv_docker_blocks_auth_freeipa_docker_compose_yaml
    mod_devenv_docker_blocks_auth_jwt_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_jwt_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_auth_nginx_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_nginx_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_auth_nginx_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_nginx_proxy_mac_docker_compose_yaml
    mod_devenv_docker_blocks_auth_nginx_proxy_mac -->|PACKAGED_BY| art_devenv_docker_blocks_auth_nginx_proxy_mac_Dockerfile
    mod_devenv_docker_blocks_auth_nginx_proxy_mac -->|PACKAGED_BY| art_devenv_docker_blocks_auth_nginx_proxy_mac_docker_compose_yaml
    mod_devenv_docker_blocks_auth_oauth -->|PACKAGED_BY| art_devenv_docker_blocks_auth_authentik_docker_compose_yaml
    mod_devenv_docker_blocks_auth_oauth -->|PACKAGED_BY| art_devenv_docker_blocks_auth_jwt_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_auth_oauth -->|PACKAGED_BY| art_devenv_docker_blocks_auth_oauth_docker_compose_yaml
    mod_devenv_docker_blocks_auth_oauth -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure_docker_compose_yaml
    mod_devenv_docker_blocks_auth_openldap -->|PACKAGED_BY| art_devenv_docker_blocks_auth_openldap_multiple_docker_compose_yaml
    mod_devenv_docker_blocks_auth_openldap -->|PACKAGED_BY| art_devenv_docker_blocks_auth_openldap_docker_compose_yaml
    mod_devenv_docker_blocks_auth_openldap_multiple -->|PACKAGED_BY| art_devenv_docker_blocks_auth_openldap_multiple_docker_compose_yaml
    mod_devenv_docker_blocks_auth_prometheus_basic_auth_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_basic_auth_proxy_Dockerfile
    mod_devenv_docker_blocks_auth_prometheus_basic_auth_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_basic_auth_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure_docker_compose_yaml
    mod_devenv_docker_blocks_caddy_tls -->|PACKAGED_BY| art_devenv_docker_blocks_caddy_tls_docker_compose_yaml
    mod_devenv_docker_blocks_clickhouse -->|PACKAGED_BY| art_devenv_docker_blocks_clickhouse_docker_compose_yaml
    mod_devenv_docker_blocks_collectd -->|PACKAGED_BY| art_devenv_docker_blocks_collectd_Dockerfile
    mod_devenv_docker_blocks_collectd -->|PACKAGED_BY| art_devenv_docker_blocks_collectd_docker_compose_yaml
    mod_devenv_docker_blocks_elastic -->|PACKAGED_BY| art_devenv_docker_blocks_elastic_docker_compose_yaml
    mod_devenv_docker_blocks_elastic -->|PACKAGED_BY| art_devenv_docker_blocks_elasticstack_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_Dockerfile
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_auth_freeipa_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_elastic_data_Dockerfile
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_elastic_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_elasticstack_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_grafana_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_graphite_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_graphite1_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb1_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_jaeger_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_loki_promtail_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_loki_data_Dockerfile
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_loki_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tls_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_Dockerfile
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_opentsdb_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_sensugo_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_docker_blocks_webdav_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_elastic_data -->|PACKAGED_BY| art_devenv_local_cdn_docker_compose_yaml
    mod_devenv_docker_blocks_elasticstack -->|PACKAGED_BY| art_devenv_docker_blocks_elasticstack_docker_compose_yaml
    mod_devenv_docker_blocks_etcd -->|PACKAGED_BY| art_devenv_docker_blocks_etcd_docker_compose_yaml
    mod_devenv_docker_blocks_etcd -->|PACKAGED_BY| art_devenv_docker_blocks_sensugo_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_Dockerfile
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_apache_proxy_mac_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_jwt_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_nginx_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_nginx_proxy_mac_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_openldap_multiple_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_auth_openldap_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_elasticstack_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_grafana_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_graphite_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_graphite1_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb1_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_jaeger_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_loki_promtail_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_loki_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mariadb_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mimir_backend_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tls_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_Dockerfile
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_opentsdb_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_pgvector_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_pyroscope_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_blocks_traefik_docker_compose_yml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_buildcontainer_Dockerfile
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_ha_test_unified_alerting_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_docker_ha_test_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_devenv_local_cdn_docker_compose_yaml
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_packaging_docker_custom_Dockerfile
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_scripts_verify_repo_update_Dockerfile_deb
    mod_devenv_docker_blocks_grafana -->|PACKAGED_BY| art_scripts_verify_repo_update_Dockerfile_rpm
    mod_devenv_docker_blocks_graphite -->|PACKAGED_BY| art_devenv_docker_blocks_collectd_docker_compose_yaml
    mod_devenv_docker_blocks_graphite -->|PACKAGED_BY| art_devenv_docker_blocks_graphite_docker_compose_yaml
    mod_devenv_docker_blocks_graphite -->|PACKAGED_BY| art_devenv_docker_blocks_graphite1_docker_compose_yaml
    mod_devenv_docker_blocks_graphite1 -->|PACKAGED_BY| art_devenv_docker_blocks_graphite_docker_compose_yaml
    mod_devenv_docker_blocks_graphite1 -->|PACKAGED_BY| art_devenv_docker_blocks_graphite1_docker_compose_yaml
    mod_devenv_docker_blocks_influxdb -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb_docker_compose_yaml
    mod_devenv_docker_blocks_influxdb -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb1_docker_compose_yaml
    mod_devenv_docker_blocks_influxdb1 -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb1_docker_compose_yaml
    mod_devenv_docker_blocks_jaeger -->|PACKAGED_BY| art_devenv_docker_blocks_jaeger_docker_compose_yaml
    mod_devenv_docker_blocks_jaeger -->|PACKAGED_BY| art_devenv_docker_blocks_jaegeronly_docker_compose_yaml
    mod_devenv_docker_blocks_jaeger -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_jaeger -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_jaegeronly -->|PACKAGED_BY| art_devenv_docker_blocks_jaegeronly_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_docker_blocks_jaeger_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_docker_blocks_loki_promtail_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_docker_blocks_loki_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_docker_ha_test_docker_compose_yaml
    mod_devenv_docker_blocks_loki -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_loki_promtail -->|PACKAGED_BY| art_devenv_docker_blocks_loki_promtail_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_Dockerfile
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_auth_freeipa_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_elastic_data_Dockerfile
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_elastic_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_elasticstack_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_grafana_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_graphite_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_graphite1_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_influxdb1_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_jaeger_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_loki_promtail_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_loki_data_Dockerfile
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_loki_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tls_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_Dockerfile
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_opentsdb_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_sensugo_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_docker_blocks_webdav_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_loki_data -->|PACKAGED_BY| art_devenv_local_cdn_docker_compose_yaml
    mod_devenv_docker_blocks_maildev -->|PACKAGED_BY| art_devenv_docker_blocks_maildev_docker_compose_yaml
    mod_devenv_docker_blocks_maildev -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_mariadb -->|PACKAGED_BY| art_devenv_docker_blocks_mariadb_docker_compose_yaml
    mod_devenv_docker_blocks_memcached -->|PACKAGED_BY| art_devenv_docker_blocks_memcached_docker_compose_yaml
    mod_devenv_docker_blocks_mimir_backend -->|PACKAGED_BY| art_devenv_docker_blocks_mimir_backend_docker_compose_yaml
    mod_devenv_docker_blocks_mqtt -->|PACKAGED_BY| art_devenv_docker_blocks_mqtt_docker_compose_yaml
    mod_devenv_docker_blocks_mssql -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_docker_compose_yaml
    mod_devenv_docker_blocks_mssql -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_arm64_docker_compose_yaml
    mod_devenv_docker_blocks_mssql -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_mssql -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tls_docker_compose_yaml
    mod_devenv_docker_blocks_mssql_arm64 -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_arm64_docker_compose_yaml
    mod_devenv_docker_blocks_mssql_tests -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_mssql_tls -->|PACKAGED_BY| art_devenv_docker_blocks_mssql_tls_docker_compose_yaml
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_docker_compose_yaml
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_exporter_docker_compose_yaml
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_Dockerfile
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_docker_compose_yaml
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_Dockerfile
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_ha_test_unified_alerting_docker_compose_yaml
    mod_devenv_docker_blocks_mysql -->|PACKAGED_BY| art_devenv_docker_ha_test_docker_compose_yaml
    mod_devenv_docker_blocks_mysql_exporter -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_exporter_docker_compose_yaml
    mod_devenv_docker_blocks_mysql_opendata -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_Dockerfile
    mod_devenv_docker_blocks_mysql_opendata -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_opendata_docker_compose_yaml
    mod_devenv_docker_blocks_mysql_tests -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_Dockerfile
    mod_devenv_docker_blocks_mysql_tests -->|PACKAGED_BY| art_devenv_docker_blocks_mysql_tests_docker_compose_yaml
    mod_devenv_docker_blocks_opentsdb -->|PACKAGED_BY| art_devenv_docker_blocks_opentsdb_docker_compose_yaml
    mod_devenv_docker_blocks_pgvector -->|PACKAGED_BY| art_devenv_docker_blocks_pgvector_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|BUILT_BY| job_pr_test_integration_yml_postgres
    mod_devenv_docker_blocks_postgres -->|BUILT_BY| job_pr_test_integration_yml_postgres_enterprise
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_auth_authentik_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_auth_jwt_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_auth_oauth_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_pgvector_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_Dockerfile
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_docker_ha_test_docker_compose_yaml
    mod_devenv_docker_blocks_postgres -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_postgres_tests -->|BUILT_BY| job_pr_test_integration_yml_postgres
    mod_devenv_docker_blocks_postgres_tests -->|BUILT_BY| job_pr_test_integration_yml_postgres_enterprise
    mod_devenv_docker_blocks_postgres_tests -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_Dockerfile
    mod_devenv_docker_blocks_postgres_tests -->|PACKAGED_BY| art_devenv_docker_blocks_postgres_tests_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_basic_auth_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_Dockerfile
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_high_card_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_random_data_Dockerfile
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_utf8_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_ha_test_unified_alerting_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_docker_ha_test_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus_high_card -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus_high_card -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_high_card_Dockerfile
    mod_devenv_docker_blocks_prometheus_high_card -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_high_card_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus_random_data -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus_random_data -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_random_data_Dockerfile
    mod_devenv_docker_blocks_prometheus_utf8 -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_docker_compose_yaml
    mod_devenv_docker_blocks_prometheus_utf8 -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_utf8_Dockerfile
    mod_devenv_docker_blocks_prometheus_utf8 -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_utf8_docker_compose_yaml
    mod_devenv_docker_blocks_pyroscope -->|PACKAGED_BY| art_devenv_docker_blocks_pyroscope_docker_compose_yaml
    mod_devenv_docker_blocks_pyroscope -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_redis -->|PACKAGED_BY| art_devenv_docker_blocks_auth_authentik_docker_compose_yaml
    mod_devenv_docker_blocks_redis -->|PACKAGED_BY| art_devenv_docker_blocks_redis_docker_compose_yaml
    mod_devenv_docker_blocks_self_instrumentation -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_sensugo -->|PACKAGED_BY| art_devenv_docker_blocks_sensugo_docker_compose_yaml
    mod_devenv_docker_blocks_slow_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_slow_proxy_Dockerfile
    mod_devenv_docker_blocks_slow_proxy -->|PACKAGED_BY| art_devenv_docker_blocks_slow_proxy_docker_compose_yaml
    mod_devenv_docker_blocks_smtp -->|PACKAGED_BY| art_devenv_docker_blocks_smtp_Dockerfile
    mod_devenv_docker_blocks_smtp -->|PACKAGED_BY| art_devenv_docker_blocks_smtp_docker_compose_yaml
    mod_devenv_docker_blocks_stateful_webhook -->|PACKAGED_BY| art_devenv_docker_blocks_stateful_webhook_Dockerfile
    mod_devenv_docker_blocks_stateful_webhook -->|PACKAGED_BY| art_devenv_docker_blocks_stateful_webhook_docker_compose_yaml
    mod_devenv_docker_blocks_tempo -->|PACKAGED_BY| art_devenv_docker_blocks_self_instrumentation_docker_compose_yaml
    mod_devenv_docker_blocks_tempo -->|PACKAGED_BY| art_devenv_docker_blocks_tempo_docker_compose_yaml
    mod_devenv_docker_blocks_tempo -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_docker_blocks_traefik -->|PACKAGED_BY| art_devenv_docker_blocks_traefik_docker_compose_yml
    mod_devenv_docker_blocks_webdav -->|PACKAGED_BY| art_devenv_docker_blocks_webdav_docker_compose_yaml
    mod_devenv_docker_blocks_zipkin -->|PACKAGED_BY| art_devenv_docker_blocks_zipkin_docker_compose_yaml
    mod_devenv_docker_buildcontainer -->|PACKAGED_BY| art_devenv_docker_buildcontainer_Dockerfile
    mod_devenv_docker_debtest -->|PACKAGED_BY| art_devenv_docker_debtest_Dockerfile
    mod_devenv_docker_ha_test_unified_alerting -->|PACKAGED_BY| art_devenv_docker_ha_test_unified_alerting_Dockerfile
    mod_devenv_docker_ha_test_unified_alerting -->|PACKAGED_BY| art_devenv_docker_ha_test_unified_alerting_docker_compose_yaml
    mod_devenv_docker_ha_test -->|PACKAGED_BY| art_devenv_docker_ha_test_docker_compose_yaml
    mod_devenv_frontend_service -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_devenv_local_npm -->|PACKAGED_BY| art_devenv_local_npm_docker_compose_yaml
    mod_devenv_local_cdn -->|PACKAGED_BY| art_devenv_local_cdn_docker_compose_yaml
    mod_emails -->|PACKAGED_BY| art_Dockerfile
    mod_github_com_grafana_grafana -->|PACKAGED_BY| art_Dockerfile
    mod_github_com_grafana_grafana -->|PACKAGED_BY| art_devenv_docker_ha_test_unified_alerting_docker_compose_yaml
    mod_github_com_grafana_grafana -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_hack -->|BUILT_BY| job_pr_k8s_codegen_check_yml_check
    mod_packages_grafana_data -->|PACKAGED_BY| art_Dockerfile
    mod_packages_grafana_e2e_selectors -->|DEPLOYED_BY| job_release_npm_yml_publish
    mod_packages_grafana_schema -->|PACKAGED_BY| art_Dockerfile
    mod_packaging_docker_custom -->|PACKAGED_BY| art_devenv_docker_blocks_auth_authentik_docker_compose_yaml
    mod_packaging_docker_custom -->|PACKAGED_BY| art_devenv_frontend_service_docker_compose_yaml
    mod_packaging_docker_custom -->|PACKAGED_BY| art_packaging_docker_custom_Dockerfile
    mod_pkg_storage_dbproxy -->|BUILT_BY| job_proto_breaking_changes_yml_generated
    mod_pkg_storage_unified_resourcepb -->|BUILT_BY| job_pr_resource_search_result_format_yml_check
    mod_pkg_storage_unified_resourcepb -->|BUILT_BY| job_proto_breaking_changes_yml_generated
    mod_scripts_cli -->|BUILT_BY| job_pr_bundle_size_yml_build
    mod_scripts_cli -->|BUILT_BY| job_pr_bundle_size_yml_bundle_size
    mod_scripts_cli -->|PACKAGED_BY| art_devenv_docker_blocks_auth_authentik_docker_compose_yaml
    mod_scripts_cli -->|PACKAGED_BY| art_devenv_docker_blocks_auth_jwt_proxy_docker_compose_yaml
    mod_scripts_cli -->|PACKAGED_BY| art_devenv_docker_blocks_auth_prometheus_oauth2_proxy_azure_docker_compose_yaml
    mod_scripts_cli -->|PACKAGED_BY| art_devenv_docker_blocks_clickhouse_docker_compose_yaml
    mod_scripts_cli -->|PACKAGED_BY| art_devenv_docker_blocks_prometheus_random_data_Dockerfile
    mod_scripts_cli -->|PACKAGED_BY| art_packaging_docker_custom_Dockerfile
    mod_scripts_modowners -->|BUILT_BY| job_backend_code_checks_yml_validate_configs
    mod_scripts_modowners -->|BUILT_BY| job_modowners_reviewers_yml_request
    mod_scripts_verify_repo_update -->|PACKAGED_BY| art_scripts_verify_repo_update_Dockerfile_deb
    mod_scripts_verify_repo_update -->|PACKAGED_BY| art_scripts_verify_repo_update_Dockerfile_rpm
    art_devenv_docker_blocks_postgres_tests_Dockerfile -->|BUILT_BY| job_pr_test_integration_yml_postgres
    art_devenv_docker_blocks_postgres_tests_Dockerfile -->|BUILT_BY| job_pr_test_integration_yml_postgres_enterprise
    art_devenv_docker_blocks_postgres_tests_docker_compose_yaml -->|BUILT_BY| job_pr_test_integration_yml_postgres
    art_devenv_docker_blocks_postgres_tests_docker_compose_yaml -->|BUILT_BY| job_pr_test_integration_yml_postgres_enterprise
```

- `deploy-frontend-preview.yml#deploy` (ci_job) --[DEPLOYS_TO]--> `frontend-preview-pr-${{ needs.check.outputs.pr-number }}` (environment)
- `deploy-storybook-preview.yml#deploy-storybook-preview` (ci_job) --[DEPLOYS_TO]--> `storybook-pr-preview-${{ github.event.pull_request.number }}` (environment)
- `external-fr-weekly-digest.yml#digest` (ci_job) --[DEPLOYS_TO]--> `${{ github.event_name == 'workflow_dispatch' && 'manual-trigger' || '' }}` (environment)
- `external-issue-weekly-digest.yml#digest` (ci_job) --[DEPLOYS_TO]--> `${{ github.event_name == 'workflow_dispatch' && 'manual-trigger' || '' }}` (environment)
- `external-pr-weekly-digest.yml#report` (ci_job) --[DEPLOYS_TO]--> `${{ github.event_name == 'workflow_dispatch' && 'manual-trigger' || '' }}` (environment)
- `release-npm.yml#publish` (ci_job) --[DEPLOYS_TO]--> `npm-publish` (environment)
- `.citools/src/cue` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `.citools/src/govulncheck` (code_module) --[BUILT_BY]--> `govulncheck.yml#govulncheck` (ci_job)
- `.github/actions/changelog` (code_module) --[BUILT_BY]--> `changelog.yml#main` (ci_job)
- `.github/actions/changelog` (code_module) --[DEPLOYED_BY]--> `release-pr.yml#create-prs` (ci_job)
- `apps/dashboard` (code_module) --[BUILT_BY]--> `pr-frontend-unit-tests.yml#generate-golden-files` (ci_job)
- `devenv/docker/blocks/alert_webhook_listener` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/alert_webhook_listener/Dockerfile` (container)
- `devenv/docker/blocks/alert_webhook_listener` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/alert_webhook_listener/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/apache_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/apache_proxy/Dockerfile` (container)
- `devenv/docker/blocks/auth/apache_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/apache_proxy/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/apache_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/apache_proxy_mac/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/apache_proxy_mac` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/apache_proxy_mac/Dockerfile` (container)
- `devenv/docker/blocks/auth/apache_proxy_mac` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/apache_proxy_mac/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/authentik` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/authentik/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/freeipa` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/freeipa/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/jwt_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/jwt_proxy/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/nginx_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/nginx_proxy/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/nginx_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/nginx_proxy_mac/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/nginx_proxy_mac` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/nginx_proxy_mac/Dockerfile` (container)
- `devenv/docker/blocks/auth/nginx_proxy_mac` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/nginx_proxy_mac/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/oauth` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/authentik/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/oauth` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/jwt_proxy/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/oauth` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/oauth/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/oauth` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/prometheus_oauth2_proxy_azure/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/openldap` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/openldap-multiple/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/openldap` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/openldap/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/openldap-multiple` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/openldap-multiple/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/prometheus_basic_auth_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/prometheus_basic_auth_proxy/Dockerfile` (container)
- `devenv/docker/blocks/auth/prometheus_basic_auth_proxy` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/prometheus_basic_auth_proxy/docker-compose.yaml` (container)
- `devenv/docker/blocks/auth/prometheus_oauth2_proxy_azure` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/auth/prometheus_oauth2_proxy_azure/docker-compose.yaml` (container)
- `devenv/docker/blocks/caddy_tls` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/caddy_tls/docker-compose.yaml` (container)
- `devenv/docker/blocks/clickhouse` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/clickhouse/docker-compose.yaml` (container)
- `devenv/docker/blocks/collectd` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/collectd/Dockerfile` (container)
- `devenv/docker/blocks/collectd` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/collectd/docker-compose.yaml` (container)
- `devenv/docker/blocks/elastic` (code_module) --[PACKAGED_BY]--> `devenv/docker/blocks/elastic/docker-compose.yaml` (container)


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
  pipeline_root(["grafana/grafana (100 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (48 workflows · 99 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_46_Lint_Frontend["Lint Frontend (12 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_46_Lint_Frontend
  job_46_detect_changes["detect-changes"]:::atlasJob
  job_46_lint_frontend_prettier["lint-frontend-prettier"]:::atlasJob
  job_46_lint_frontend_prettier_enterprise["lint-frontend-prettier-enterprise"]:::atlasJob
  wf_46_Lint_Frontend --> job_46_detect_changes
  job_46_detect_changes --> job_46_lint_frontend_prettier
  job_46_detect_changes --> job_46_lint_frontend_prettier_enterprise
  wf_66_End_to_end_tests["End-to-end tests (9 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_66_End_to_end_tests
  job_66_detect_changes["detect-changes"]:::atlasJob
  job_66_build_backend["build-backend"]:::atlasJob
  job_66_build_frontend["build-frontend"]:::atlasJob
  wf_66_End_to_end_tests --> job_66_detect_changes
  job_66_detect_changes --> job_66_build_backend
  job_66_detect_changes --> job_66_build_frontend
  grp_1_Scheduled___Manual["Scheduled & Manual (24 workflows · 38 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Scheduled___Manual
  wf_55_Run_commands_when_issues_are_opened["Run commands when issues are opened (5 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_55_Run_commands_when_issues_are_opened
  job_55_main["main"]:::atlasJob
  job_55_auto_triage["auto-triage"]:::atlasJob
  job_55_auto_label_internal_issues["auto-label-internal-issues"]:::atlasJob
  wf_55_Run_commands_when_issues_are_opened --> job_55_main
  job_55_main --> job_55_auto_triage
  job_55_main --> job_55_auto_label_internal_issues
  wf_61_PR_build_Docker_image["PR build Docker image (7 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_61_PR_build_Docker_image
  job_61_detect_changes["detect-changes"]:::atlasJob
  job_61_build_frontend["build-frontend"]:::atlasJob
  job_61_build_backend["build-backend"]:::atlasJob
  wf_61_PR_build_Docker_image --> job_61_detect_changes
  job_61_detect_changes --> job_61_build_frontend
  job_61_detect_changes --> job_61_build_backend
  grp_2_Release___Deploy["Release & Deploy (17 workflows · 68 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Release___Deploy
  wf_82_Build_Release_Packages["Build Release Packages (26 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_82_Build_Release_Packages
  job_82_setup["setup"]:::atlasJob
  job_82_downstream["downstream"]:::atlasJob
  job_82_build_frontend["build-frontend"]:::atlasJob
  wf_82_Build_Release_Packages --> job_82_setup
  job_82_setup --> job_82_downstream
  job_82_setup --> job_82_build_frontend
  wf_83_Post_release["Post-release (11 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_83_Post_release
  job_83_setup["setup"]:::atlasJob
  wf_83_Post_release --> job_83_setup
  grp_3_Automation___Other["Automation & Other (7 workflows · 8 jobs)"]:::atlasCategory
  pipeline_root --> grp_3_Automation___Other
  wf_9_Backport__workflow_["Backport (workflow) (1 jobs)"]:::atlasWorkflow
  grp_3_Automation___Other --> wf_9_Backport__workflow_
  wf_16_Run_commands_when_issues_are_labeled_or_comments_added["Run commands when issues are labeled or comments added (2 jobs)"]:::atlasWorkflow
  grp_3_Automation___Other --> wf_16_Run_commands_when_issues_are_labeled_or_comments_added
  grp_4_Security___Governance["Security & Governance (4 workflows · 4 jobs)"]:::atlasCategory
  pipeline_root --> grp_4_Security___Governance
  wf_21_Create_security_branch["Create security branch (1 jobs)"]:::atlasWorkflow
  grp_4_Security___Governance --> wf_21_Create_security_branch
  wf_94_Close_stale_issues_and_PRs["Close stale issues and PRs (1 jobs)"]:::atlasWorkflow
  grp_4_Security___Governance --> wf_94_Close_stale_issues_and_PRs
  wf_more["+90 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
