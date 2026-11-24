---
title: Architecture — grafana/ai-sdk
description: Arc42 and Pipeline report for grafana/ai-sdk
---

# Repository Architecture Analysis: grafana/ai-sdk

## Metadata
- **SHA**: `edcebe5e9acf9a7a50d89268b534a708c5e201cb`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.77
- **avg_cyclomatic_complexity**: 3.35
- **component_count**: 255
- **dead_code_count**: 1
- **dead_code_symbols**: 1 entry(ies)
- **duplication_pct**: 6.82
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 819
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: Go Service
- **import_edges**: 100 entry(ies)
- **loc**: 198359
- **max_cognitive_complexity**: 75
- **max_cyclomatic_complexity**: 49
- **sloc**: 176552
- **test_file_count**: 1403

# Architecture: grafana/ai-sdk

## Context
- **Repository**: `grafana/ai-sdk`
- **SHA**: `edcebe5e9acf9a7a50d89268b534a708c5e201cb`
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
    repo_root(["grafana/ai-sdk (255 components)"]):::atlasRoot
    subgraph sg_dir_0_ai_gateway["ai-gateway (181)"]
      direction TB
      dir_0_ai_gateway["ai-gateway (181)"]:::atlasCategory
      sub_0_0_pkg["pkg (84)"]:::atlasWorkflow
      dir_0_ai_gateway --> sub_0_0_pkg
      sub_0_1_internal["internal (39)"]:::atlasWorkflow
      dir_0_ai_gateway --> sub_0_1_internal
      sub_0_2_providerwire["providerwire (30)"]:::atlasWorkflow
      dir_0_ai_gateway --> sub_0_2_providerwire
      sub_0_more["+4 more submodules (28)"]:::atlasMore
      dir_0_ai_gateway --> sub_0_more
    end
    repo_root --> dir_0_ai_gateway
    dir_1__root_["(root) (70)"]:::atlasCategory
    repo_root --> dir_1__root_
    dir_2_test["test (3)"]:::atlasCategory
    repo_root --> dir_2_test
    dir_3_release["release (1)"]:::atlasCategory
    repo_root --> dir_3_release
```

## Component Details

Showing top 60 representative components out of 255 across 4 module group(s):

- **Module `ai-gateway`** (181 components — module: 180, MODULE: 1)
- **Module `(root)`** (70 components — module: 70)
- **Module `test`** (3 components — MODULE: 3)
- **Module `release`** (1 components — MODULE: 1)

- **@ai-sdk/conformance-tools** (`test/conformance/tools/package.json`): MODULE
- **@ai-sdk/providerwire-v4-contract** (`ai-gateway/test/providerwire-v4/package.json`): MODULE
- **@ai-sdk/test-cli** (`test/cli/package.json`): MODULE
- **@ai-sdk/test-integration** (`test/integration/package.json`): MODULE
- **Magefile** (`ai-gateway/Magefile.go`): module
- **access** (`ai-gateway/pkg/internal/auth/access.go`): module
- **access_test** (`ai-gateway/pkg/internal/auth/access_test.go`): module
- **adapter** (`ai-gateway/internal/testadapter/adapter.go`): module
- **adapter_test** (`ai-gateway/internal/execution/adapter_test.go`): module
- **adapter_test** (`ai-gateway/openai/chatcompletions/adapter_test.go`): module
- **agent** (`agent.go`): module
- **agent_export_timeout_test** (`ai-gateway/pkg/internal/service/agent_export_timeout_test.go`): module
- **agent_test** (`agent_test.go`): module
- **agent_ui_validation** (`agent_ui_validation.go`): module
- **agent_ui_validation_test** (`agent_ui_validation_test.go`): module
- **ai-sdk-release-tooling** (`release/tooling/package.json`): MODULE
- **aigateway_manifest** (`ai-gateway/pkg/internal/manifestdata/aigateway_manifest.go`): module
- **anthropic_policy** (`ai-gateway/pkg/internal/nativeoptions/anthropic_policy.go`): module
- **anthropic_policy_test** (`ai-gateway/pkg/internal/nativeoptions/anthropic_policy_test.go`): module
- **approval_observability_test** (`ai-gateway/pkg/internal/service/approval_observability_test.go`): module
- **approvals_test** (`ai-gateway/providerwire/v4/approvals_test.go`): module
- **attempts** (`ai-gateway/internal/execution/attempts.go`): module
- **attempts_test** (`ai-gateway/internal/execution/attempts_test.go`): module
- **capture_test** (`ai-gateway/internal/execution/capture_test.go`): module
- **catalog** (`ai-gateway/catalog/catalog.go`): module
- **catalog** (`ai-gateway/pkg/internal/service/catalog.go`): module
- **catalog_test** (`ai-gateway/pkg/internal/service/catalog_test.go`): module
- **chunk** (`chunk.go`): module
- **chunk_test** (`chunk_test.go`): module
- **citations** (`ai-gateway/providerwire/v4/citations.go`): module
- **citations** (`citations.go`): module
- **citations_test** (`ai-gateway/providerwire/v4/citations_test.go`): module
- **citations_test** (`citations_test.go`): module
- **classify** (`ai-gateway/internal/execution/classify.go`): module
- **classify_test** (`ai-gateway/internal/execution/classify_test.go`): module
- **compose** (`ai-gateway/pkg/internal/routing/compose.go`): module
- **compose_test** (`ai-gateway/pkg/internal/routing/compose_test.go`): module
- **config** (`ai-gateway/openai/chatcompletions/config.go`): module
- **controls** (`ai-gateway/pkg/internal/routing/controls.go`): module
- **controls_test** (`ai-gateway/pkg/internal/routing/controls_test.go`): module
- **convert** (`convert.go`): module
- **convert_test** (`convert_test.go`): module
- **convert_tool_state_test** (`convert_tool_state_test.go`): module
- **defaults** (`ai-gateway/openai/chatcompletions/defaults.go`): module
- **dependency_test** (`ai-gateway/catalog/dependency_test.go`): module
- **diagnostics** (`ai-gateway/openai/chatcompletions/diagnostics.go`): module
- **discovery** (`ai-gateway/internal/host/discovery.go`): module
- **discovery** (`ai-gateway/providerwire/v4/discovery.go`): module
- **discovery_test** (`ai-gateway/providerwire/v4/discovery_test.go`): module
- **doc** (`ai-gateway/catalog/doc.go`): module
- **doc** (`ai-gateway/internal/execution/doc.go`): module
- **doc** (`ai-gateway/internal/host/doc.go`): module
- **doc** (`ai-gateway/pkg/gateway/doc.go`): module
- **doc** (`ai-gateway/providerwire/v4/doc.go`): module
- **doc** (`doc.go`): module
- **effective_tool_choice_test** (`effective_tool_choice_test.go`): module
- **error** (`ai-gateway/internal/execution/error.go`): module
- **error_response** (`ai-gateway/providerwire/v4/error_response.go`): module
- **error_test** (`ai-gateway/internal/execution/error_test.go`): module
- **errors** (`ai-gateway/catalog/errors.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (59.97/100)
- **Technical Debt Score**: 40.03
- **Estimated Remediation Effort**: 46.62h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 61.37 | 0.20 | avg_cc=3.35, max_cc=49, duplication=6.82%, dead_code=1 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=847, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 48.00 | 0.15 | avg_cognitive=3.77, max_cognitive=75, fitness_violations=2, oversized_files=3 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=8, operational_antipatterns=31, parallel_branches=True |
| Security | `C` | 75.00 | 0.20 | vulnerabilities=0, secrets=1, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (75.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (49.0) exceeds policy threshold (20.0).

### Workspace Packages
- **@grafana/aigateway-app** (`ai-gateway`, react_ts_js, pnpm)
- **@ai-sdk/providerwire-v4-contract** (`ai-gateway/test/providerwire-v4`, react_ts_js, pnpm)
- **@ai-sdk/test-cli** (`test/cli`, react_ts_js, pnpm)
- **@ai-sdk/conformance-tools** (`test/conformance/tools`, react_ts_js, pnpm)
- **@ai-sdk/test-integration** (`test/integration`, react_ts_js, pnpm)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 847 | **Vulnerabilities**: 0 | **Secrets**: 1

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `ai-gateway/test/providerwire-v4/native-provider-proxy.ts:8` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)

### Inventory Sample
- `github.com/anthropics/anthropic-sdk-go` `1.80.0` (golang, `ai-gateway/go.mod`)
- `github.com/anthropics/anthropic-sdk-go` `1.80.0` (golang, `middleware/agentobservability/go.mod`)
- `github.com/anthropics/anthropic-sdk-go` `1.80.0` (golang, `providers/anthropic/go.mod`)
- `github.com/anthropics/anthropic-sdk-go` `1.80.0` (golang, `providers/azure/go.mod`)
- `github.com/anthropics/anthropic-sdk-go` `1.80.0` (golang, `test/conformance/go.mod`)
- `github.com/aws/aws-sdk-go-v2` `1.47.4` (golang, `providers/bedrock/go.mod`)
- `github.com/aws/aws-sdk-go-v2/config` `1.33.10` (golang, `providers/bedrock/go.mod`)
- `github.com/aws/aws-sdk-go-v2/credentials` `1.20.10` (golang, `providers/bedrock/go.mod`)
- `github.com/aws/aws-sdk-go-v2/credentials` `1.20.10` (golang, `test/conformance/go.mod`)
- `github.com/go-jose/go-jose/v4` `4.1.6` (golang, `ai-gateway/go.mod`)
- `github.com/grafana/agento11y/go` `0.20.0` (golang, `ai-gateway/go.mod`)
- `github.com/grafana/agento11y/go` `0.20.0` (golang, `middleware/agentobservability/go.mod`)
- `github.com/grafana/agento11y/go-providers/anthropic` `0.20.0` (golang, `middleware/agentobservability/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `ai-gateway/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `examples/agent-chat/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `examples/structured-extraction/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `middleware/agentobservability/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `middleware/enrichment/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `middleware/logger/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `middleware/prometheus/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `providers/anthropic/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `providers/azure/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `providers/bedrock/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `providers/grafana/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `providers/openai-compatible/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `providers/openai/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `test/conformance/go.mod`)
- `github.com/grafana/ai-sdk` `0.1.0-alpha.5` (golang, `test/integration/testserver/go.mod`)
- `github.com/grafana/ai-sdk/middleware/agentobservability` `0.1.0-alpha.2` (golang, `ai-gateway/go.mod`)
- `github.com/grafana/ai-sdk/middleware/logger` `0.1.0-alpha.2` (golang, `ai-gateway/go.mod`)
- ... (+817 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_4c24d0b1_08c9_4388_9405_dfe82a3640b3["4c24d0b1-08c9-4388-9405-dfe82a3640b3"]:::atlasCategory
        mod_ai_gateway["ai-gateway"]:::atlasCategory
        mod_ai_gateway__config["ai-gateway/.config"]:::atlasCategory
        mod_providers_anthropic["providers/anthropic"]:::atlasCategory
        mod_providers_grafana["providers/grafana"]:::atlasCategory
        mod_release_tooling["release/tooling"]:::atlasCategory
        mod_test_conformance["test/conformance"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_ai_gateway__config_Dockerfile["ai-gateway/.config/Dockerfile"]:::atlasWorkflow
        art_ai_gateway__config_docker_compose_base_yaml["ai-gateway/.config/docker-compose-base.yaml"]:::atlasWorkflow
        art_ai_gateway_docker_compose_e2e_yaml["ai-gateway/docker-compose.e2e.yaml"]:::atlasWorkflow
        art_ai_gateway_docker_compose_yaml["ai-gateway/docker-compose.yaml"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_ci_yml_build_test["ci.yml#build-test"]:::atlasJob
        job_ci_yml_gateway_test["ci.yml#gateway-test"]:::atlasJob
        job_ci_yml_module_resolution["ci.yml#module-resolution"]:::atlasJob
        job_ci_yml_parity_baseline["ci.yml#parity-baseline"]:::atlasJob
        job_ci_yml_plugin_build["ci.yml#plugin-build"]:::atlasJob
        job_ci_yml_plugin_validation["ci.yml#plugin-validation"]:::atlasJob
        job_publish_ai_gateway_dev_yml_source_ci["publish-ai-gateway-dev.yml#source-ci"]:::atlasJob
        job_publish_ai_gateway_ops_yml_source_ci["publish-ai-gateway-ops.yml#source-ci"]:::atlasJob
        job_release_please_yml_release_please["release-please.yml#release-please"]:::atlasJob
    end
    mod_4c24d0b1_08c9_4388_9405_dfe82a3640b3 -->|PACKAGED_BY| art_ai_gateway__config_docker_compose_base_yaml
    mod_ai_gateway -->|BUILT_BY| job_ci_yml_gateway_test
    mod_ai_gateway -->|BUILT_BY| job_ci_yml_module_resolution
    mod_ai_gateway -->|BUILT_BY| job_ci_yml_plugin_build
    mod_ai_gateway -->|BUILT_BY| job_ci_yml_plugin_validation
    mod_ai_gateway -->|PACKAGED_BY| art_ai_gateway_docker_compose_e2e_yaml
    mod_ai_gateway -->|PACKAGED_BY| art_ai_gateway_docker_compose_yaml
    mod_ai_gateway__config -->|PACKAGED_BY| art_ai_gateway__config_Dockerfile
    mod_ai_gateway__config -->|PACKAGED_BY| art_ai_gateway__config_docker_compose_base_yaml
    mod_ai_gateway__config -->|PACKAGED_BY| art_ai_gateway_docker_compose_yaml
    mod_providers_anthropic -->|PACKAGED_BY| art_ai_gateway_docker_compose_e2e_yaml
    mod_providers_grafana -->|PACKAGED_BY| art_ai_gateway__config_Dockerfile
    mod_providers_grafana -->|PACKAGED_BY| art_ai_gateway__config_docker_compose_base_yaml
    mod_providers_grafana -->|PACKAGED_BY| art_ai_gateway_docker_compose_e2e_yaml
    mod_providers_grafana -->|PACKAGED_BY| art_ai_gateway_docker_compose_yaml
    mod_release_tooling -->|BUILT_BY| job_ci_yml_build_test
    mod_release_tooling -->|BUILT_BY| job_publish_ai_gateway_dev_yml_source_ci
    mod_release_tooling -->|BUILT_BY| job_publish_ai_gateway_ops_yml_source_ci
    mod_release_tooling -->|DEPLOYED_BY| job_release_please_yml_release_please
    mod_test_conformance -->|BUILT_BY| job_ci_yml_parity_baseline
    art_ai_gateway_docker_compose_e2e_yaml -->|BUILT_BY| job_ci_yml_plugin_build
    art_ai_gateway_docker_compose_e2e_yaml -->|BUILT_BY| job_ci_yml_plugin_validation
    art_ai_gateway_docker_compose_yaml -->|BUILT_BY| job_ci_yml_plugin_build
    art_ai_gateway_docker_compose_yaml -->|BUILT_BY| job_ci_yml_plugin_validation
```

- `4c24d0b1-08c9-4388-9405-dfe82a3640b3` (code_module) --[PACKAGED_BY]--> `ai-gateway/.config/docker-compose-base.yaml` (container)
- `ai-gateway` (code_module) --[BUILT_BY]--> `ci.yml#gateway-test` (ci_job)
- `ai-gateway` (code_module) --[BUILT_BY]--> `ci.yml#module-resolution` (ci_job)
- `ai-gateway` (code_module) --[BUILT_BY]--> `ci.yml#plugin-build` (ci_job)
- `ai-gateway` (code_module) --[BUILT_BY]--> `ci.yml#plugin-validation` (ci_job)
- `ai-gateway` (code_module) --[PACKAGED_BY]--> `ai-gateway/docker-compose.e2e.yaml` (container)
- `ai-gateway` (code_module) --[PACKAGED_BY]--> `ai-gateway/docker-compose.yaml` (container)
- `ai-gateway/.config` (code_module) --[PACKAGED_BY]--> `ai-gateway/.config/Dockerfile` (container)
- `ai-gateway/.config` (code_module) --[PACKAGED_BY]--> `ai-gateway/.config/docker-compose-base.yaml` (container)
- `ai-gateway/.config` (code_module) --[PACKAGED_BY]--> `ai-gateway/docker-compose.yaml` (container)
- `providers/anthropic` (code_module) --[PACKAGED_BY]--> `ai-gateway/docker-compose.e2e.yaml` (container)
- `providers/grafana` (code_module) --[PACKAGED_BY]--> `ai-gateway/.config/Dockerfile` (container)
- `providers/grafana` (code_module) --[PACKAGED_BY]--> `ai-gateway/.config/docker-compose-base.yaml` (container)
- `providers/grafana` (code_module) --[PACKAGED_BY]--> `ai-gateway/docker-compose.e2e.yaml` (container)
- `providers/grafana` (code_module) --[PACKAGED_BY]--> `ai-gateway/docker-compose.yaml` (container)
- `release/tooling` (code_module) --[BUILT_BY]--> `ci.yml#build-test` (ci_job)
- `release/tooling` (code_module) --[BUILT_BY]--> `publish-ai-gateway-dev.yml#source-ci` (ci_job)
- `release/tooling` (code_module) --[BUILT_BY]--> `publish-ai-gateway-ops.yml#source-ci` (ci_job)
- `release/tooling` (code_module) --[DEPLOYED_BY]--> `release-please.yml#release-please` (ci_job)
- `test/conformance` (code_module) --[BUILT_BY]--> `ci.yml#parity-baseline` (ci_job)
- `ai-gateway/docker-compose.e2e.yaml` (container) --[BUILT_BY]--> `ci.yml#plugin-build` (ci_job)
- `ai-gateway/docker-compose.e2e.yaml` (container) --[BUILT_BY]--> `ci.yml#plugin-validation` (ci_job)
- `ai-gateway/docker-compose.yaml` (container) --[BUILT_BY]--> `ci.yml#plugin-build` (ci_job)
- `ai-gateway/docker-compose.yaml` (container) --[BUILT_BY]--> `ci.yml#plugin-validation` (ci_job)


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
  pipeline_root(["grafana/ai-sdk (8 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Release___Deploy["Release & Deploy (5 workflows · 9 jobs)"]
    direction TB
    subgraph sg_wf_3_Publish_AI_Gateway_plugin__dev_["Publish AI Gateway plugin (dev) (3 jobs)"]
      direction TB
      wf_3_Publish_AI_Gateway_plugin__dev_(["Trigger: Publish AI Gateway plugin (dev)"]):::atlasWorkflow
      job_3_source_ci["source-ci"]:::atlasJob
      job_3_publish["publish"]:::atlasJob
      job_3_update_plugin_version["update-plugin-version"]:::atlasJob
      wf_3_Publish_AI_Gateway_plugin__dev_ --> job_3_source_ci
      job_3_source_ci --> job_3_publish
      job_3_publish --> job_3_update_plugin_version
    end
    pipeline_root --> wf_3_Publish_AI_Gateway_plugin__dev_
    subgraph sg_wf_4_Publish_AI_Gateway_plugin__ops_["Publish AI Gateway plugin (ops) (3 jobs)"]
      direction TB
      wf_4_Publish_AI_Gateway_plugin__ops_(["Trigger: Publish AI Gateway plugin (ops)"]):::atlasWorkflow
      job_4_source_ci["source-ci"]:::atlasJob
      job_4_publish["publish"]:::atlasJob
      job_4_update_plugin_version["update-plugin-version"]:::atlasJob
      wf_4_Publish_AI_Gateway_plugin__ops_ --> job_4_source_ci
      job_4_source_ci --> job_4_publish
      job_4_publish --> job_4_update_plugin_version
    end
    pipeline_root --> wf_4_Publish_AI_Gateway_plugin__ops_
    subgraph sg_wf_5_Release["Release (1 jobs)"]
      direction TB
      wf_5_Release(["Trigger: Release"]):::atlasWorkflow
      job_5_release_please["release-please"]:::atlasJob
      wf_5_Release --> job_5_release_please
    end
    pipeline_root --> wf_5_Release
    subgraph sg_wf_6_Release_readiness["Release readiness (1 jobs)"]
      direction TB
      wf_6_Release_readiness(["Trigger: Release readiness"]):::atlasWorkflow
      job_6_release_readiness["release-readiness"]:::atlasJob
      wf_6_Release_readiness --> job_6_release_readiness
    end
    pipeline_root --> wf_6_Release_readiness
    subgraph sg_wf_7_Release_verification["Release verification (1 jobs)"]
      direction TB
      wf_7_Release_verification(["Trigger: Release verification"]):::atlasWorkflow
      job_7_verify_published_library["verify-published-library"]:::atlasJob
      wf_7_Release_verification --> job_7_verify_published_library
    end
    pipeline_root --> wf_7_Release_verification
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (3 workflows · 15 jobs)"]
    direction TB
    subgraph sg_wf_0_Build___Test["Build & Test (13 jobs)"]
      direction TB
      wf_0_Build___Test(["Trigger: Build & Test"]):::atlasWorkflow
      job_0_changes["changes"]:::atlasJob
      job_0_ci["ci"]:::atlasJob
      job_0_build_test["build-test"]:::atlasJob
      wf_0_Build___Test --> job_0_changes
      job_0_build_test --> job_0_ci
      job_0_changes --> job_0_build_test
    end
    pipeline_root --> wf_0_Build___Test
    subgraph sg_wf_1_Conventional_commits["Conventional commits (1 jobs)"]
      direction TB
      wf_1_Conventional_commits(["Trigger: Conventional commits"]):::atlasWorkflow
      job_1_check["check"]:::atlasJob
      wf_1_Conventional_commits --> job_1_check
    end
    pipeline_root --> wf_1_Conventional_commits
    subgraph sg_wf_2_OpenSpec["OpenSpec (1 jobs)"]
      direction TB
      wf_2_OpenSpec(["Trigger: OpenSpec"]):::atlasWorkflow
      job_2_check["check"]:::atlasJob
      wf_2_OpenSpec --> job_2_check
    end
    pipeline_root --> wf_2_OpenSpec
  end
```
