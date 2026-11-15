---
title: Architecture — PostHog/posthog-go
description: Arc42 and Pipeline report for PostHog/posthog-go
---

# Repository Architecture Analysis: PostHog/posthog-go

## Metadata
- **SHA**: `cde0aa1f97a1a4438f14597a2a2bd244b0cf5a17`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 208
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 208
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Go Service
- **import_edges**: 0 entry(ies)
- **loc**: 65658
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 54558
- **test_file_count**: 112

# Architecture: PostHog/posthog-go

## Context
- **Repository**: `PostHog/posthog-go`
- **SHA**: `cde0aa1f97a1a4438f14597a2a2bd244b0cf5a17`
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
    repo_root(["PostHog/posthog-go (208 components)"]):::atlasRoot
    dir_0__root_["(root) (126)"]:::atlasCategory
    repo_root --> dir_0__root_
    dir_1_posthogmcp["posthogmcp (23)"]:::atlasCategory
    repo_root --> dir_1_posthogmcp
    sub_1_0__module_root_["(module root) (22)"]:::atlasWorkflow
    dir_1_posthogmcp --> sub_1_0__module_root_
    sub_1_1_testdata["testdata (1)"]:::atlasWorkflow
    dir_1_posthogmcp --> sub_1_1_testdata
    dir_2_otel["otel (14)"]:::atlasCategory
    repo_root --> dir_2_otel
    sub_2_0__module_root_["(module root) (13)"]:::atlasWorkflow
    dir_2_otel --> sub_2_0__module_root_
    sub_2_1_example["example (1)"]:::atlasWorkflow
    dir_2_otel --> sub_2_1_example
    dir_3_posthogmcpsdk["posthogmcpsdk (14)"]:::atlasCategory
    repo_root --> dir_3_posthogmcpsdk
    dir_4_posthogmcpgo["posthogmcpgo (13)"]:::atlasCategory
    repo_root --> dir_4_posthogmcpgo
    dir_other_modules["+6 more modules (18)"]:::atlasMore
    repo_root --> dir_other_modules
```

## Component Details

Showing top 60 representative components out of 208 across 11 module group(s):

- **Module `(root)`** (126 components — module: 126)
- **Module `posthogmcp`** (23 components — module: 23)
- **Module `otel`** (14 components — module: 14)
- **Module `posthogmcpsdk`** (14 components — module: 14)
- **Module `posthogmcpgo`** (13 components — module: 13)
- **Module `examples`** (7 components — module: 7)
- **Module `extras`** (5 components — module: 5)
- **Module `sdk_compliance_adapter`** (3 components — module: 3)
- **Module `cmd`** (1 components — module: 1)
- **Module `internal`** (1 components — module: 1)
- **Module `testdata`** (1 components — module: 1)

- **alias** (`alias.go`): module
- **alias_test** (`alias_test.go`): module
- **analytics** (`posthogmcp/analytics.go`): module
- **analytics_test** (`posthogmcp/analytics_test.go`): module
- **arguments** (`posthogmcpgo/arguments.go`): module
- **arguments** (`posthogmcpsdk/arguments.go`): module
- **async_test** (`async_test.go`): module
- **backoff** (`backoff.go`): module
- **backoff_test** (`backoff_test.go`): module
- **batching_test** (`batching_test.go`): module
- **before_send_test** (`before_send_test.go`): module
- **benchmark_test** (`benchmark_test.go`): module
- **calls** (`posthogmcpgo/calls.go`): module
- **calls_test** (`posthogmcpgo/calls_test.go`): module
- **capture** (`capture.go`): module
- **capture** (`examples/capture.go`): module
- **capture_local_eval_test** (`capture_local_eval_test.go`): module
- **capture_test** (`capture_test.go`): module
- **capture_v1** (`capture_v1.go`): module
- **capture_v1_errors** (`capture_v1_errors.go`): module
- **capture_v1_errors_test** (`capture_v1_errors_test.go`): module
- **capture_v1_integration_test** (`capture_v1_integration_test.go`): module
- **capture_v1_send** (`capture_v1_send.go`): module
- **capture_v1_send_test** (`capture_v1_send_test.go`): module
- **capture_v1_test** (`capture_v1_test.go`): module
- **capturer** (`capturer.go`): module
- **compression_test** (`compression_test.go`): module
- **concurrency_test** (`concurrency_test.go`): module
- **config** (`config.go`): module
- **config** (`otel/config.go`): module
- **config_test** (`config_test.go`): module
- **constants** (`posthogmcp/constants.go`): module
- **context_span_processor** (`otel/context_span_processor.go`): module
- **context_span_processor_test** (`otel/context_span_processor_test.go`): module
- **contextmarshaler** (`testdata/contextmarshaler/contextmarshaler.go`): module
- **conversation_test** (`posthogmcpsdk/conversation_test.go`): module
- **doc** (`otel/doc.go`): module
- **doc** (`posthogmcp/doc.go`): module
- **doc** (`posthogmcpgo/doc.go`): module
- **doc** (`posthogmcpsdk/doc.go`): module
- **docker-compose** (`sdk_compliance_adapter/docker-compose.yml`): module
- **emails** (`emails.go`): module
- **emails_attachments** (`emails_attachments.go`): module
- **emails_attachments_test** (`emails_attachments_test.go`): module
- **emails_error** (`emails_error.go`): module
- **emails_fakes_test** (`emails_fakes_test.go`): module
- **emails_test** (`emails_test.go`): module
- **eof_test** (`extras/eof_test.go`): module
- **error** (`error.go`): module
- **error_test** (`error_test.go`): module
- **error_tracking** (`error_tracking.go`): module
- **error_tracking** (`examples/error_tracking.go`): module
- **error_tracking_debug_images** (`error_tracking_debug_images.go`): module
- **error_tracking_debug_images_darwin** (`error_tracking_debug_images_darwin.go`): module
- **error_tracking_debug_images_darwin_test** (`error_tracking_debug_images_darwin_test.go`): module
- **error_tracking_debug_images_linux** (`error_tracking_debug_images_linux.go`): module
- **error_tracking_debug_images_linux_test** (`error_tracking_debug_images_linux_test.go`): module
- **error_tracking_debug_images_other** (`error_tracking_debug_images_other.go`): module
- **error_tracking_debug_images_test** (`error_tracking_debug_images_test.go`): module
- **error_tracking_slog** (`error_tracking_slog.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (66.45/100)
- **Technical Debt Score**: 33.55
- **Estimated Remediation Effort**: 30.39h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=124, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 21.00 | 0.15 | workflows=11, operational_antipatterns=27, parallel_branches=True |
| Security | `F` | 14.00 | 0.20 | vulnerabilities=0, secrets=4, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 124 | **Vulnerabilities**: 0 | **Secrets**: 4

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `posthogmcp/analytics_test.go:282` (`token := "phc_***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `posthogmcp/sanitize_test.go:16` (`token := "phc_***REDACTED***"`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `posthogmcp/secrets_test.go:41` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `posthogmcp/secrets_test.go:42` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `github.com/andybalholm/brotli` `1.1.1` (golang, `go.mod`)
- `github.com/goccy/go-json` `0.10.6` (golang, `go.mod`)
- `github.com/google/go-cmp` `0.7.0` (golang, `go.mod`)
- `github.com/google/uuid` `1.6.0` (golang, `go.mod`)
- `github.com/google/uuid` `1.6.0` (golang, `posthogmcpgo/go.mod`)
- `github.com/google/uuid` `1.6.0` (golang, `posthogmcpsdk/go.mod`)
- `github.com/hashicorp/golang-lru/v2` `2.0.7` (golang, `go.mod`)
- `github.com/joho/godotenv` `1.5.1` (golang, `go.mod`)
- `github.com/klauspost/compress` `1.17.11` (golang, `go.mod`)
- `github.com/mark3labs/mcp-go` `0.58.0` (golang, `posthogmcpgo/go.mod`)
- `github.com/modelcontextprotocol/go-sdk` `1.6.1` (golang, `posthogmcpgo/go.mod`)
- `github.com/modelcontextprotocol/go-sdk` `1.6.1` (golang, `posthogmcpsdk/go.mod`)
- `github.com/orian/flakyhttp` `0.1.1` (golang, `go.mod`)
- `github.com/posthog/posthog-go` `1.44.1` (golang, `otel/go.mod`)
- `github.com/posthog/posthog-go` `1.44.1` (golang, `posthogmcpgo/go.mod`)
- `github.com/posthog/posthog-go` `1.44.1` (golang, `posthogmcpsdk/go.mod`)
- `github.com/posthog/posthog-go/posthogmcpsdk` `1.39.0` (golang, `posthogmcpgo/go.mod`)
- `github.com/stretchr/testify` `1.11.1` (golang, `go.mod`)
- `github.com/stretchr/testify` `1.11.1` (golang, `posthogmcpgo/go.mod`)
- `github.com/stretchr/testify` `1.11.1` (golang, `posthogmcpsdk/go.mod`)
- `github.com/urfave/cli` `1.22.17` (golang, `go.mod`)
- `go.opentelemetry.io/otel` `1.46.0` (golang, `otel/go.mod`)
- `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp` `1.46.0` (golang, `otel/go.mod`)
- `go.opentelemetry.io/otel/sdk` `1.46.0` (golang, `otel/go.mod`)
- `go.opentelemetry.io/otel/trace` `1.46.0` (golang, `otel/go.mod`)
- `go.opentelemetry.io/proto/otlp` `1.11.0` (golang, `otel/go.mod`)
- `golang.org/x/sys` `0.21.0` (golang, `go.mod`)
- `golang.org/x/text` `0.21.0` (golang, `go.mod`)
- `google.golang.org/protobuf` `1.36.12` (golang, `otel/go.mod`)
- `@changesets/cli` `3.0.3` (npm, `package.json`)
- ... (+94 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_otel["otel"]:::atlasCategory
        mod_posthogmcpgo["posthogmcpgo"]:::atlasCategory
        mod_posthogmcpsdk["posthogmcpsdk"]:::atlasCategory
        mod_sdk_compliance_adapter["sdk_compliance_adapter"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_sdk_compliance_adapter_Dockerfile["sdk_compliance_adapter/Dockerfile"]:::atlasWorkflow
        art_sdk_compliance_adapter_Dockerfile_v1["sdk_compliance_adapter/Dockerfile.v1"]:::atlasWorkflow
        art_sdk_compliance_adapter_docker_compose_yml["sdk_compliance_adapter/docker-compose.yml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_fmt_yml_mcp_go_fmt_tidy["fmt.yml#mcp-go-fmt-tidy"]:::atlasJob
        job_fmt_yml_mcp_go_sdk_fmt_tidy["fmt.yml#mcp-go-sdk-fmt-tidy"]:::atlasJob
        job_fmt_yml_otel_fmt_tidy["fmt.yml#otel-fmt-tidy"]:::atlasJob
        job_release_yml_release["release.yml#release"]:::atlasJob
        job_unit_tests_yml_mcp_go["unit-tests.yml#mcp-go"]:::atlasJob
        job_unit_tests_yml_mcp_go_sdk["unit-tests.yml#mcp-go-sdk"]:::atlasJob
        job_unit_tests_yml_otel_bridge["unit-tests.yml#otel-bridge"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_Release["Release"]:::atlasTarget
    end
    job_release_yml_release -->|DEPLOYS_TO| env_Release
    mod_otel -->|BUILT_BY| job_fmt_yml_otel_fmt_tidy
    mod_otel -->|BUILT_BY| job_unit_tests_yml_otel_bridge
    mod_otel -->|DEPLOYED_BY| job_release_yml_release
    mod_posthogmcpgo -->|BUILT_BY| job_fmt_yml_mcp_go_fmt_tidy
    mod_posthogmcpgo -->|BUILT_BY| job_unit_tests_yml_mcp_go
    mod_posthogmcpgo -->|DEPLOYED_BY| job_release_yml_release
    mod_posthogmcpsdk -->|BUILT_BY| job_fmt_yml_mcp_go_sdk_fmt_tidy
    mod_posthogmcpsdk -->|BUILT_BY| job_unit_tests_yml_mcp_go
    mod_posthogmcpsdk -->|BUILT_BY| job_unit_tests_yml_mcp_go_sdk
    mod_posthogmcpsdk -->|DEPLOYED_BY| job_release_yml_release
    mod_sdk_compliance_adapter -->|PACKAGED_BY| art_sdk_compliance_adapter_Dockerfile
    mod_sdk_compliance_adapter -->|PACKAGED_BY| art_sdk_compliance_adapter_Dockerfile_v1
    mod_sdk_compliance_adapter -->|PACKAGED_BY| art_sdk_compliance_adapter_docker_compose_yml
```

- `release.yml#release` (ci_job) --[DEPLOYS_TO]--> `Release` (environment)
- `otel` (code_module) --[BUILT_BY]--> `fmt.yml#otel-fmt-tidy` (ci_job)
- `otel` (code_module) --[BUILT_BY]--> `unit-tests.yml#otel-bridge` (ci_job)
- `otel` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `posthogmcpgo` (code_module) --[BUILT_BY]--> `fmt.yml#mcp-go-fmt-tidy` (ci_job)
- `posthogmcpgo` (code_module) --[BUILT_BY]--> `unit-tests.yml#mcp-go` (ci_job)
- `posthogmcpgo` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `posthogmcpsdk` (code_module) --[BUILT_BY]--> `fmt.yml#mcp-go-sdk-fmt-tidy` (ci_job)
- `posthogmcpsdk` (code_module) --[BUILT_BY]--> `unit-tests.yml#mcp-go` (ci_job)
- `posthogmcpsdk` (code_module) --[BUILT_BY]--> `unit-tests.yml#mcp-go-sdk` (ci_job)
- `posthogmcpsdk` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `sdk_compliance_adapter` (code_module) --[PACKAGED_BY]--> `sdk_compliance_adapter/Dockerfile` (container)
- `sdk_compliance_adapter` (code_module) --[PACKAGED_BY]--> `sdk_compliance_adapter/Dockerfile.v1` (container)
- `sdk_compliance_adapter` (code_module) --[PACKAGED_BY]--> `sdk_compliance_adapter/docker-compose.yml` (container)


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
  pipeline_root(["PostHog/posthog-go (11 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (5 workflows · 17 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_0_Call_Feature_Flags_Project_Workflow["Call Feature Flags Project Workflow (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_0_Call_Feature_Flags_Project_Workflow
  job_0_call_flags_project["call-flags-project"]:::atlasJob
  wf_0_Call_Feature_Flags_Project_Workflow --> job_0_call_flags_project
  wf_2_Check_Formatting["Check Formatting (5 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_2_Check_Formatting
  job_2_fmt["fmt"]:::atlasJob
  job_2_mod_tidy["mod-tidy"]:::atlasJob
  job_2_otel_fmt_tidy["otel-fmt-tidy"]:::atlasJob
  wf_2_Check_Formatting --> job_2_fmt
  wf_2_Check_Formatting --> job_2_mod_tidy
  wf_2_Check_Formatting --> job_2_otel_fmt_tidy
  wf_8_SDK_Compliance_Tests["SDK Compliance Tests (2 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_8_SDK_Compliance_Tests
  job_8_compliance["compliance"]:::atlasJob
  job_8_compliance_v1["compliance-v1"]:::atlasJob
  wf_8_SDK_Compliance_Tests --> job_8_compliance
  wf_8_SDK_Compliance_Tests --> job_8_compliance_v1
  wf_10_Unit_Tests["Unit Tests (8 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_10_Unit_Tests
  job_10_build["build"]:::atlasJob
  job_10_otel_bridge["otel-bridge"]:::atlasJob
  job_10_mcp_go_sdk["mcp-go-sdk"]:::atlasJob
  wf_10_Unit_Tests --> job_10_build
  wf_10_Unit_Tests --> job_10_otel_bridge
  wf_10_Unit_Tests --> job_10_mcp_go_sdk
  grp_1_Release___Deploy["Release & Deploy (2 workflows · 7 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Release___Deploy
  wf_6_Release_failure_notification["Release failure notification (1 jobs)"]:::atlasWorkflow
  grp_1_Release___Deploy --> wf_6_Release_failure_notification
  job_6_notify_failed["notify-failed"]:::atlasJob
  wf_6_Release_failure_notification --> job_6_notify_failed
  wf_7_Release["Release (6 jobs)"]:::atlasWorkflow
  grp_1_Release___Deploy --> wf_7_Release
  job_7_check_changesets["check-changesets"]:::atlasJob
  job_7_notify_approval_needed["notify-approval-needed"]:::atlasJob
  job_7_preserve_slack_thread["preserve-slack-thread"]:::atlasJob
  wf_7_Release --> job_7_check_changesets
  job_7_check_changesets --> job_7_notify_approval_needed
  job_7_notify_approval_needed --> job_7_preserve_slack_thread
  grp_2_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Scheduled___Manual
  wf_3_Generate_references["Generate references (1 jobs)"]:::atlasWorkflow
  grp_2_Scheduled___Manual --> wf_3_Generate_references
  job_3_generate_references["generate-references"]:::atlasJob
  wf_3_Generate_references --> job_3_generate_references
  wf_5_PostHog_Upgrade["PostHog Upgrade (1 jobs)"]:::atlasWorkflow
  grp_2_Scheduled___Manual --> wf_5_PostHog_Upgrade
  job_5_posthog_upgrade["posthog-upgrade"]:::atlasJob
  wf_5_PostHog_Upgrade --> job_5_posthog_upgrade
  grp_3_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]:::atlasCategory
  pipeline_root --> grp_3_Security___Governance
  wf_1_CodeQL_Advanced["CodeQL Advanced (1 jobs)"]:::atlasWorkflow
  grp_3_Security___Governance --> wf_1_CodeQL_Advanced
  job_1_analyze["analyze"]:::atlasJob
  wf_1_CodeQL_Advanced --> job_1_analyze
  wf_9_Handle_stale_issues_and_PRs["Handle stale issues and PRs (1 jobs)"]:::atlasWorkflow
  grp_3_Security___Governance --> wf_9_Handle_stale_issues_and_PRs
  wf_more["+1 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
