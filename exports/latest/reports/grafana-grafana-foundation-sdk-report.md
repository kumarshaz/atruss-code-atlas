---
title: Architecture — grafana/grafana-foundation-sdk
description: Arc42 and Pipeline report for grafana/grafana-foundation-sdk
---

# Repository Architecture Analysis: grafana/grafana-foundation-sdk

## Metadata
- **SHA**: `72b873117be02d3cd352c4ac8590b6555b0d1ce2`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.64
- **avg_cyclomatic_complexity**: 1.67
- **component_count**: 17
- **dead_code_count**: 3
- **dead_code_symbols**: 3 entry(ies)
- **duplication_pct**: 98.32
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 1651
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Java Maven/Gradle
- **import_edges**: 100 entry(ies)
- **loc**: 115950
- **max_cognitive_complexity**: 52
- **max_cyclomatic_complexity**: 35
- **sloc**: 97111
- **test_file_count**: 2

# Architecture: grafana/grafana-foundation-sdk

## Context
- **Repository**: `grafana/grafana-foundation-sdk`
- **SHA**: `72b873117be02d3cd352c4ac8590b6555b0d1ce2`
- **Ecosystem**: Java
- **Framework**: Java Maven/Gradle

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
    runtime["runtime : module"]:::atlasJob
    variants["variants : module"]:::atlasJob
    main["main : module"]:::atlasJob
    custompanel["custompanel : module"]:::atlasJob
    customquery["customquery : module"]:::atlasJob
    common["common : module"]:::atlasJob
    discovery["discovery : module"]:::atlasJob
    overview["overview : module"]:::atlasJob
    retrieval["retrieval : module"]:::atlasJob
    repo_root(["grafana/grafana-foundation-sdk"]):::atlasRoot
    repo_root --> common
    repo_root --> custompanel
    repo_root --> customquery
    repo_root --> discovery
    repo_root --> main
    repo_root --> overview
    repo_root --> retrieval
    repo_root --> runtime
    repo_root --> variants
```

## Component Details
- **runtime** (`.cog/templates/go/extra/cog/runtime.go`): module
- **variants** (`.cog/templates/go/extra/cog/plugins/variants.go`): module
- **variants** (`.cog/templates/go/extra/cog/variants/variants.go`): module
- **main** (`examples/go/alert-rule/main.go`): module
- **custompanel** (`examples/go/custom-panel/custompanel.go`): module
- **main** (`examples/go/custom-panel/main.go`): module
- **customquery** (`examples/go/custom-query/customquery.go`): module
- **main** (`examples/go/custom-query/main.go`): module
- **main** (`examples/go/dashboardv1-with-expr-queries/main.go`): module
- **main** (`examples/go/dashboardv2beta1-with-expr-queries/main.go`): module
- **main** (`examples/go/dashboardv2beta1-with-tabs-and-rows/main.go`): module
- **common** (`examples/go/grafana-agent-overview/common.go`): module
- **discovery** (`examples/go/grafana-agent-overview/discovery.go`): module
- **main** (`examples/go/grafana-agent-overview/main.go`): module
- **overview** (`examples/go/grafana-agent-overview/overview.go`): module
- **retrieval** (`examples/go/grafana-agent-overview/retrieval.go`): module
- **main** (`examples/go/grafana-openapi-client-go/main.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (43.85/100)
- **Technical Debt Score**: 56.15
- **Estimated Remediation Effort**: 96.45h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 44.00 | 0.20 | avg_cc=1.67, max_cc=35, duplication=98.32%, dead_code=3 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=539, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=0.64, max_cognitive=52, fitness_violations=3, oversized_files=17 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=8, operational_antipatterns=24, parallel_branches=True |
| Security | `F` | 20.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=6 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (98.32) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (52.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (35.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 539 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `com.fasterxml.jackson.core:jackson-databind` `2.19.1` (Maven, `.cog/templates/java/extra/build.gradle`)
- `com.fasterxml.jackson.core:jackson-databind` `2.19.1` (Maven, `java/build.gradle`)
- `com.grafana:grafana-foundation-sdk` `0.0.6` (Maven, `examples/java/alert-rule/build.gradle`)
- `com.grafana:grafana-foundation-sdk` `0.0.6` (Maven, `examples/java/custom-panel/build.gradle`)
- `com.grafana:grafana-foundation-sdk` `0.0.6` (Maven, `examples/java/custom-query/build.gradle`)
- `com.grafana:grafana-foundation-sdk` `0.0.6` (Maven, `examples/java/grafana-agent-overview/build.gradle`)
- `com.grafana:grafana-foundation-sdk` `0.0.6` (Maven, `examples/java/linux-node-overview/build.gradle`)
- `com.grafana:grafana-foundation-sdk` `0.0.6` (Maven, `examples/java/red-method/build.gradle`)
- `Babel` `2.18.0` (PyPI, `requirements.txt`)
- `Jinja2` `3.1.6` (PyPI, `requirements.txt`)
- `Markdown` `3.11.2` (PyPI, `requirements.txt`)
- `MarkupSafe` `3.0.4` (PyPI, `requirements.txt`)
- `PyYAML` `6.0.3` (PyPI, `requirements.txt`)
- `Pygments` `2.20.0` (PyPI, `requirements.txt`)
- `brotlicffi` `1.2.1.0` (PyPI, `requirements.txt`)
- `certifi` `2026.10.23` (PyPI, `requirements.txt`)
- `cffi` `2.1.1` (PyPI, `requirements.txt`)
- `charset-normalizer` `3.5.2` (PyPI, `requirements.txt`)
- `click` `8.5.0` (PyPI, `requirements.txt`)
- `colorama` `0.4.6` (PyPI, `requirements.txt`)
- `ghp-import` `2.1.0` (PyPI, `requirements.txt`)
- `grafana_foundation_sdk` `*` (PyPI, `examples/pulumi/python/requirements.txt`)
- `grafana_foundation_sdk` `0.0.11` (PyPI, `examples/python/dashboardv2beta1-with-tabs-and-rows/requirements.txt`)
- `grafana_foundation_sdk` `0.0.6` (PyPI, `examples/python/alert-rule/requirements.txt`)
- `grafana_foundation_sdk` `0.0.6` (PyPI, `examples/python/custom-panel/requirements.txt`)
- `grafana_foundation_sdk` `0.0.6` (PyPI, `examples/python/custom-query/requirements.txt`)
- `grafana_foundation_sdk` `0.0.6` (PyPI, `examples/python/grafana-agent-overview/requirements.txt`)
- `grafana_foundation_sdk` `0.0.6` (PyPI, `examples/python/linux-node-overview/requirements.txt`)
- `grafana_foundation_sdk` `0.0.6` (PyPI, `examples/python/red-method/requirements.txt`)
- `idna` `3.20` (PyPI, `requirements.txt`)
- ... (+509 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_examples_go_custom_panel["examples/go/custom-panel"]:::atlasCategory
        mod_examples_go_custom_query["examples/go/custom-query"]:::atlasCategory
        mod_examples_go_grafana_agent_overview["examples/go/grafana-agent-overview"]:::atlasCategory
        mod_examples_go_linux_node_overview["examples/go/linux-node-overview"]:::atlasCategory
        mod_examples_go_red_method["examples/go/red-method"]:::atlasCategory
        mod_examples_java_custom_panel["examples/java/custom-panel"]:::atlasCategory
        mod_examples_java_custom_query["examples/java/custom-query"]:::atlasCategory
        mod_examples_java_grafana_agent_overview["examples/java/grafana-agent-overview"]:::atlasCategory
        mod_examples_java_linux_node_overview["examples/java/linux-node-overview"]:::atlasCategory
        mod_examples_java_red_method["examples/java/red-method"]:::atlasCategory
        mod_examples_php_custom_panel["examples/php/custom-panel"]:::atlasCategory
        mod_examples_php_custom_query["examples/php/custom-query"]:::atlasCategory
        mod_examples_php_grafana_agent_overview["examples/php/grafana-agent-overview"]:::atlasCategory
        mod_examples_php_linux_node_overview["examples/php/linux-node-overview"]:::atlasCategory
        mod_examples_php_red_method["examples/php/red-method"]:::atlasCategory
        mod_examples_pulumi_go["examples/pulumi/go"]:::atlasCategory
        mod_examples_python_custom_panel["examples/python/custom-panel"]:::atlasCategory
        mod_examples_python_custom_query["examples/python/custom-query"]:::atlasCategory
        mod_examples_python_grafana_agent_overview["examples/python/grafana-agent-overview"]:::atlasCategory
        mod_examples_python_linux_node_overview["examples/python/linux-node-overview"]:::atlasCategory
        mod_examples_python_red_method["examples/python/red-method"]:::atlasCategory
        mod_examples_typescript_custom_panel["examples/typescript/custom-panel"]:::atlasCategory
        mod_examples_typescript_custom_query["examples/typescript/custom-query"]:::atlasCategory
        mod_examples_typescript_grafana_agent_overview["examples/typescript/grafana-agent-overview"]:::atlasCategory
        mod_examples_typescript_linux_node_overview["examples/typescript/linux-node-overview"]:::atlasCategory
        mod_examples_typescript_red_method["examples/typescript/red-method"]:::atlasCategory
        mod_go["go"]:::atlasCategory
        mod_java["java"]:::atlasCategory
        mod_python["python"]:::atlasCategory
        mod_scripts_dashboard_converter["scripts/dashboard-converter"]:::atlasCategory
        mod_typescript["typescript"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_examples_terraform_dashboards_tf["examples/terraform/dashboards.tf"]:::atlasWorkflow
        art_scripts_dashboard_converter_Dockerfile["scripts/dashboard-converter/Dockerfile"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_dashboard_converter_yaml_build_and_export_digest["dashboard-converter.yaml#build-and-export-digest"]:::atlasJob
        job_dashboard_converter_yaml_test["dashboard-converter.yaml#test"]:::atlasJob
        job_docs_yaml_build["docs.yaml#build"]:::atlasJob
        job_docs_yaml_deploy["docs.yaml#deploy"]:::atlasJob
        job_java_release_yaml_release["java-release.yaml#release"]:::atlasJob
        job_python_release_yaml_release["python-release.yaml#release"]:::atlasJob
        job_sdk_ci_yaml_diff_preview["sdk-ci.yaml#diff_preview"]:::atlasJob
        job_typescript_release_yaml_release["typescript-release.yaml#release"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_github_pages["github-pages"]:::atlasTarget
        env_pypi["pypi"]:::atlasTarget
        env_typescript["typescript"]:::atlasTarget
    end
    job_docs_yaml_build -->|DEPLOYS_TO| env_github_pages
    job_docs_yaml_deploy -->|DEPLOYS_TO| env_github_pages
    job_python_release_yaml_release -->|DEPLOYS_TO| env_pypi
    job_typescript_release_yaml_release -->|DEPLOYS_TO| env_typescript
    mod_examples_go_custom_panel -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_go_custom_query -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_go_grafana_agent_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_go_linux_node_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_go_red_method -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_java_custom_panel -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_java_custom_query -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_java_grafana_agent_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_java_linux_node_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_java_red_method -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_php_custom_panel -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_php_custom_query -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_php_grafana_agent_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_php_linux_node_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_php_red_method -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_pulumi_go -->|PACKAGED_BY| art_scripts_dashboard_converter_Dockerfile
    mod_examples_pulumi_go -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_python_custom_panel -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_python_custom_query -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_python_grafana_agent_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_python_linux_node_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_python_red_method -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_typescript_custom_panel -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_typescript_custom_query -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_typescript_grafana_agent_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_typescript_linux_node_overview -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_examples_typescript_red_method -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_go -->|PACKAGED_BY| art_scripts_dashboard_converter_Dockerfile
    mod_go -->|PACKAGED_BY| art_examples_terraform_dashboards_tf
    mod_java -->|DEPLOYED_BY| job_java_release_yaml_release
    mod_python -->|DEPLOYED_BY| job_python_release_yaml_release
    mod_scripts_dashboard_converter -->|BUILT_BY| job_dashboard_converter_yaml_build_and_export_digest
    mod_scripts_dashboard_converter -->|BUILT_BY| job_dashboard_converter_yaml_test
    mod_scripts_dashboard_converter -->|PACKAGED_BY| art_scripts_dashboard_converter_Dockerfile
    mod_typescript -->|BUILT_BY| job_sdk_ci_yaml_diff_preview
    mod_typescript -->|DEPLOYED_BY| job_typescript_release_yaml_release
    art_scripts_dashboard_converter_Dockerfile -->|BUILT_BY| job_dashboard_converter_yaml_build_and_export_digest
```

- `docs.yaml#build` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `docs.yaml#deploy` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `python-release.yaml#release` (ci_job) --[DEPLOYS_TO]--> `pypi` (environment)
- `typescript-release.yaml#release` (ci_job) --[DEPLOYS_TO]--> `typescript` (environment)
- `examples/go/custom-panel` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/go/custom-query` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/go/grafana-agent-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/go/linux-node-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/go/red-method` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/java/custom-panel` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/java/custom-query` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/java/grafana-agent-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/java/linux-node-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/java/red-method` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/php/custom-panel` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/php/custom-query` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/php/grafana-agent-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/php/linux-node-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/php/red-method` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/pulumi/go` (code_module) --[PACKAGED_BY]--> `scripts/dashboard-converter/Dockerfile` (container)
- `examples/pulumi/go` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/python/custom-panel` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/python/custom-query` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/python/grafana-agent-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/python/linux-node-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/python/red-method` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/typescript/custom-panel` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/typescript/custom-query` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/typescript/grafana-agent-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/typescript/linux-node-overview` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `examples/typescript/red-method` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `go` (code_module) --[PACKAGED_BY]--> `scripts/dashboard-converter/Dockerfile` (container)
- `go` (code_module) --[PACKAGED_BY]--> `examples/terraform/dashboards.tf` (iac)
- `java` (code_module) --[DEPLOYED_BY]--> `java-release.yaml#release` (ci_job)
- `python` (code_module) --[DEPLOYED_BY]--> `python-release.yaml#release` (ci_job)
- `scripts/dashboard-converter` (code_module) --[BUILT_BY]--> `dashboard-converter.yaml#build-and-export-digest` (ci_job)
- `scripts/dashboard-converter` (code_module) --[BUILT_BY]--> `dashboard-converter.yaml#test` (ci_job)
- `scripts/dashboard-converter` (code_module) --[PACKAGED_BY]--> `scripts/dashboard-converter/Dockerfile` (container)
- `typescript` (code_module) --[BUILT_BY]--> `sdk-ci.yaml#diff_preview` (ci_job)
- `typescript` (code_module) --[DEPLOYED_BY]--> `typescript-release.yaml#release` (ci_job)


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
  pipeline_root(["grafana/grafana-foundation-sdk (8 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Release___Deploy["Release & Deploy (5 workflows · 6 jobs)"]
    direction TB
    subgraph sg_wf_1_Publish_documentation["Publish documentation (2 jobs)"]
      direction TB
      wf_1_Publish_documentation(["Trigger: Publish documentation"]):::atlasWorkflow
      job_1_build["build"]:::atlasJob
      job_1_deploy["deploy"]:::atlasJob
      wf_1_Publish_documentation --> job_1_build
      job_1_build --> job_1_deploy
    end
    pipeline_root --> wf_1_Publish_documentation
    subgraph sg_wf_2_Java_Release["Java Release (1 jobs)"]
      direction TB
      wf_2_Java_Release(["Trigger: Java Release"]):::atlasWorkflow
      job_2_release["release"]:::atlasJob
      wf_2_Java_Release --> job_2_release
    end
    pipeline_root --> wf_2_Java_Release
    subgraph sg_wf_3_Python_Release["Python Release (1 jobs)"]
      direction TB
      wf_3_Python_Release(["Trigger: Python Release"]):::atlasWorkflow
      job_3_release["release"]:::atlasJob
      wf_3_Python_Release --> job_3_release
    end
    pipeline_root --> wf_3_Python_Release
    subgraph sg_wf_4_Release["Release (1 jobs)"]
      direction TB
      wf_4_Release(["Trigger: Release"]):::atlasWorkflow
      job_4_release["release"]:::atlasJob
      wf_4_Release --> job_4_release
    end
    pipeline_root --> wf_4_Release
    subgraph sg_wf_6_TypeScript_Release["TypeScript Release (1 jobs)"]
      direction TB
      wf_6_TypeScript_Release(["Trigger: TypeScript Release"]):::atlasWorkflow
      job_6_release["release"]:::atlasJob
      wf_6_TypeScript_Release --> job_6_release
    end
    pipeline_root --> wf_6_TypeScript_Release
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (2 workflows · 7 jobs)"]
    direction TB
    subgraph sg_wf_0_Dashboard_Converter["Dashboard Converter (4 jobs)"]
      direction TB
      wf_0_Dashboard_Converter(["Trigger: Dashboard Converter"]):::atlasWorkflow
      job_0_test["test"]:::atlasJob
      job_0_version["version"]:::atlasJob
      job_0_build_and_export_digest["build-and-export-digest"]:::atlasJob
      wf_0_Dashboard_Converter --> job_0_test
      wf_0_Dashboard_Converter --> job_0_version
      job_0_version --> job_0_build_and_export_digest
    end
    pipeline_root --> wf_0_Dashboard_Converter
    subgraph sg_wf_5_SDK_CI["SDK CI (3 jobs)"]
      direction TB
      wf_5_SDK_CI(["Trigger: SDK CI"]):::atlasWorkflow
      job_5_run_codegen["run_codegen"]:::atlasJob
      job_5_run_examples["run_examples"]:::atlasJob
      job_5_diff_preview["diff_preview"]:::atlasJob
      wf_5_SDK_CI --> job_5_run_codegen
      wf_5_SDK_CI --> job_5_run_examples
      wf_5_SDK_CI --> job_5_diff_preview
    end
    pipeline_root --> wf_5_SDK_CI
  end
  subgraph sg_grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_7_Schema_updates["Schema updates (1 jobs)"]
      direction TB
      wf_7_Schema_updates(["Trigger: Schema updates"]):::atlasWorkflow
      job_7_schema_updates["schema_updates"]:::atlasJob
      wf_7_Schema_updates --> job_7_schema_updates
    end
    pipeline_root --> wf_7_Schema_updates
  end
```
