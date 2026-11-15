---
title: Architecture — argoproj/argo-rollouts
description: Arc42 and Pipeline report for argoproj/argo-rollouts
---

# Repository Architecture Analysis: argoproj/argo-rollouts

## Metadata
- **SHA**: `1147bc34b4ee737e1a6a40d17fff13a73909da4b`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 299
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 453
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Go Service
- **import_edges**: 0 entry(ies)
- **loc**: 229681
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 205463
- **test_file_count**: 272

# Architecture: argoproj/argo-rollouts

## Context
- **Repository**: `argoproj/argo-rollouts`
- **SHA**: `1147bc34b4ee737e1a6a40d17fff13a73909da4b`
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
    repo_root(["argoproj/argo-rollouts (299 components)"]):::atlasRoot
    dir_0_pkg["pkg (113)"]:::atlasCategory
    repo_root --> dir_0_pkg
    sub_0_0_kubectl_argo_rollouts["kubectl-argo-rollouts (55)"]:::atlasWorkflow
    dir_0_pkg --> sub_0_0_kubectl_argo_rollouts
    sub_0_1_client["client (37)"]:::atlasWorkflow
    dir_0_pkg --> sub_0_1_client
    sub_0_2_apis["apis (15)"]:::atlasWorkflow
    dir_0_pkg --> sub_0_2_apis
    sub_0_more["+2 more submodules (6)"]:::atlasMore
    dir_0_pkg --> sub_0_more
    dir_1_rollout["rollout (49)"]:::atlasCategory
    repo_root --> dir_1_rollout
    sub_1_0__module_root_["(module root) (33)"]:::atlasWorkflow
    dir_1_rollout --> sub_1_0__module_root_
    sub_1_1_steps["steps (10)"]:::atlasWorkflow
    dir_1_rollout --> sub_1_1_steps
    sub_1_2_trafficrouting["trafficrouting (5)"]:::atlasWorkflow
    dir_1_rollout --> sub_1_2_trafficrouting
    sub_1_more["+1 more submodules (1)"]:::atlasMore
    dir_1_rollout --> sub_1_more
    dir_2_metricproviders["metricproviders (44)"]:::atlasCategory
    repo_root --> dir_2_metricproviders
    sub_2_0_datadog["datadog (6)"]:::atlasWorkflow
    dir_2_metricproviders --> sub_2_0_datadog
    sub_2_1_graphite["graphite (5)"]:::atlasWorkflow
    dir_2_metricproviders --> sub_2_1_graphite
    sub_2_2_plugin["plugin (5)"]:::atlasWorkflow
    dir_2_metricproviders --> sub_2_2_plugin
    sub_2_more["+11 more submodules (28)"]:::atlasMore
    dir_2_metricproviders --> sub_2_more
    dir_3_manifests["manifests (36)"]:::atlasCategory
    repo_root --> dir_3_manifests
    sub_3_0_notifications["notifications (11)"]:::atlasWorkflow
    dir_3_manifests --> sub_3_0_notifications
    sub_3_1_base["base (7)"]:::atlasWorkflow
    dir_3_manifests --> sub_3_1_base
    sub_3_2_crds["crds (6)"]:::atlasWorkflow
    dir_3_manifests --> sub_3_2_crds
    sub_3_more["+3 more submodules (12)"]:::atlasMore
    dir_3_manifests --> sub_3_more
    dir_4_controller["controller (18)"]:::atlasCategory
    repo_root --> dir_4_controller
    sub_4_0_metrics["metrics (13)"]:::atlasWorkflow
    dir_4_controller --> sub_4_0_metrics
    sub_4_1__module_root_["(module root) (5)"]:::atlasWorkflow
    dir_4_controller --> sub_4_1__module_root_
    dir_other_modules["+8 more modules (39)"]:::atlasMore
    repo_root --> dir_other_modules
```

## Component Details

Showing top 60 representative components out of 299 across 13 module group(s):

- **Module `pkg`** (113 components — module: 113)
- **Module `rollout`** (49 components — module: 49)
- **Module `metricproviders`** (44 components — module: 44)
- **Module `manifests`** (36 components — module: 36)
- **Module `controller`** (18 components — module: 18)
- **Module `examples`** (11 components — module: 11)
- **Module `experiments`** (10 components — module: 10)
- **Module `analysis`** (5 components — module: 5)
- **Module `ingress`** (4 components — module: 4)
- **Module `cmd`** (3 components — module: 3)
- **Module `hack`** (3 components — module: 3)
- **Module `docs`** (2 components — module: 2)

- **Chart** (`examples/helm-blue-green/Chart.yaml`): module
- **MetricsRecorder** (`controller/metrics/mocks/MetricsRecorder.go`): module
- **Provider** (`metricproviders/mocks/Provider.go`): module
- **Resolver** (`rollout/steps/plugin/mocks/Resolver.go`): module
- **StepPlugin** (`rollout/steps/plugin/mocks/StepPlugin.go`): module
- **StepPlugin** (`rollout/steps/plugin/rpc/mocks/StepPlugin.go`): module
- **TrafficRoutingReconciler** (`rollout/mocks/TrafficRoutingReconciler.go`): module
- **abort** (`pkg/kubectl-argo-rollouts/cmd/abort/abort.go`): module
- **abort_test** (`pkg/kubectl-argo-rollouts/cmd/abort/abort_test.go`): module
- **add-namespaced-flag** (`manifests/namespace-install/add-namespaced-flag.yaml`): module
- **alb** (`ingress/alb.go`): module
- **alb** (`rollout/trafficrouting/alb/alb.go`): module
- **alb_test** (`ingress/alb_test.go`): module
- **alb_test** (`rollout/trafficrouting/alb/alb_test.go`): module
- **analysis** (`analysis/analysis.go`): module
- **analysis** (`controller/metrics/analysis.go`): module
- **analysis** (`rollout/analysis.go`): module
- **analysis-run-crd** (`manifests/crds/analysis-run-crd.yaml`): module
- **analysis-template-crd** (`manifests/crds/analysis-template-crd.yaml`): module
- **analysis_test** (`analysis/analysis_test.go`): module
- **analysis_test** (`controller/metrics/analysis_test.go`): module
- **analysis_test** (`rollout/analysis_test.go`): module
- **analysis_types** (`pkg/apis/rollouts/v1alpha1/analysis_types.go`): module
- **analysisrun** (`pkg/client/clientset/versioned/typed/rollouts/v1alpha1/analysisrun.go`): module
- **analysisrun** (`pkg/client/informers/externalversions/rollouts/v1alpha1/analysisrun.go`): module
- **analysisrun** (`pkg/client/listers/rollouts/v1alpha1/analysisrun.go`): module
- **analysisrun_info** (`pkg/kubectl-argo-rollouts/info/analysisrun_info.go`): module
- **analysisrun_test** (`experiments/analysisrun_test.go`): module
- **analysistemplate** (`pkg/client/clientset/versioned/typed/rollouts/v1alpha1/analysistemplate.go`): module
- **analysistemplate** (`pkg/client/informers/externalversions/rollouts/v1alpha1/analysistemplate.go`): module
- **analysistemplate** (`pkg/client/listers/rollouts/v1alpha1/analysistemplate.go`): module
- **api** (`metricproviders/graphite/api.go`): module
- **api_test** (`metricproviders/graphite/api_test.go`): module
- **argo-rollouts-aggregate-roles** (`manifests/base/argo-rollouts-aggregate-roles.yaml`): module
- **argo-rollouts-clusterrolebinding** (`manifests/cluster-install/argo-rollouts-clusterrolebinding.yaml`): module
- **argo-rollouts-config** (`manifests/base/argo-rollouts-config.yaml`): module
- **argo-rollouts-deployment** (`manifests/base/argo-rollouts-deployment.yaml`): module
- **argo-rollouts-metrics-service** (`manifests/base/argo-rollouts-metrics-service.yaml`): module
- **argo-rollouts-notification-configmap** (`manifests/notifications/argo-rollouts-notification-configmap.yaml`): module
- **argo-rollouts-notification-secret** (`manifests/base/argo-rollouts-notification-secret.yaml`): module
- **argo-rollouts-rolebinding** (`manifests/namespace-install/argo-rollouts-rolebinding.yaml`): module
- **argo-rollouts-sa** (`manifests/base/argo-rollouts-sa.yaml`): module
- **bluegreen** (`rollout/bluegreen.go`): module
- **bluegreen_test** (`rollout/bluegreen_test.go`): module
- **canary** (`rollout/canary.go`): module
- **canary_test** (`rollout/canary_test.go`): module
- **client** (`controller/metrics/client.go`): module
- **client** (`metricproviders/plugin/client/client.go`): module
- **client** (`rollout/steps/plugin/client/client.go`): module
- **client_test** (`controller/metrics/client_test.go`): module
- **clientset** (`pkg/client/clientset/versioned/clientset.go`): module
- **clientset_generated** (`pkg/client/clientset/versioned/fake/clientset_generated.go`): module
- **cloudwatch** (`metricproviders/cloudwatch/cloudwatch.go`): module
- **cloudwatch_test** (`metricproviders/cloudwatch/cloudwatch_test.go`): module
- **cluster-analysis-template-crd** (`manifests/crds/cluster-analysis-template-crd.yaml`): module
- **clusteranalysistemplate** (`pkg/client/clientset/versioned/typed/rollouts/v1alpha1/clusteranalysistemplate.go`): module
- **clusteranalysistemplate** (`pkg/client/informers/externalversions/rollouts/v1alpha1/clusteranalysistemplate.go`): module
- **clusteranalysistemplate** (`pkg/client/listers/rollouts/v1alpha1/clusteranalysistemplate.go`): module
- **clusterrole-to-role** (`manifests/namespace-install/clusterrole-to-role.yaml`): module
- **cmd** (`pkg/kubectl-argo-rollouts/cmd/cmd.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (60.50/100)
- **Technical Debt Score**: 39.50
- **Estimated Remediation Effort**: 73.38h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1997, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=13, operational_antipatterns=39, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=6, pipeline_security_findings=17 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1997 | **Vulnerabilities**: 0 | **Secrets**: 6

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-004`** at `docs/generated/notification-services/github.md:48` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[HIGH] `ATRUSS-SEC-005`** at `examples/rollout-secret.yaml:42` (`secretUrl: aHR0***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `test/e2e/functional/rollout-bg-analysis-withArgs.yaml:47` (`secretUrl: aHR0***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `test/e2e/functional/rollout-secret-withArgs.yaml:48` (`secretUrl: aHR0***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `test/e2e/functional/rollout-secret.yaml:37` (`secretUrl: aHR0***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `test/e2e/functional/rollout-shared-secret.yaml:43` (`secretUrl: aHR0***REDACTED***`)

### Inventory Sample
- `jinja2` `3.1.2` (PyPI, `docs/requirements.txt`)
- `markdown` `3.3.7` (PyPI, `docs/requirements.txt`)
- `markdown_include` `0.8.0` (PyPI, `docs/requirements.txt`)
- `mkdocs` `1.4.2` (PyPI, `docs/requirements.txt`)
- `mkdocs-material` `8.5.11` (PyPI, `docs/requirements.txt`)
- `pygments` `2.13.0` (PyPI, `docs/requirements.txt`)
- `github.com/argoproj/notifications-engine` `0.5.1-0.20260503100631-0cff13b8a717` (golang, `go.mod`)
- `github.com/argoproj/pkg` `0.13.6` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2` `1.47.3` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/config` `1.33.9` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/cloudwatch` `1.73.3` (golang, `go.mod`)
- `github.com/aws/aws-sdk-go-v2/service/elasticloadbalancingv2` `1.63.4` (golang, `go.mod`)
- `github.com/aws/smithy-go` `1.28.9` (golang, `go.mod`)
- `github.com/blang/semver` `3.5.1+incompatible` (golang, `go.mod`)
- `github.com/bombsimon/logrusr/v4` `4.2.0` (golang, `go.mod`)
- `github.com/evanphx/json-patch/v5` `5.9.11` (golang, `go.mod`)
- `github.com/expr-lang/expr` `1.17.8` (golang, `go.mod`)
- `github.com/gogo/protobuf` `1.3.2` (golang, `go.mod`)
- `github.com/golang/mock` `1.6.0` (golang, `go.mod`)
- `github.com/golang/protobuf` `1.5.4` (golang, `go.mod`)
- `github.com/google/uuid` `1.6.0` (golang, `go.mod`)
- `github.com/grpc-ecosystem/grpc-gateway` `1.16.0` (golang, `go.mod`)
- `github.com/hashicorp/go-plugin` `1.8.0` (golang, `go.mod`)
- `github.com/influxdata/influxdb-client-go/v2` `2.14.0` (golang, `go.mod`)
- `github.com/juju/ansiterm` `1.0.0` (golang, `go.mod`)
- `github.com/machinebox/graphql` `0.2.2` (golang, `go.mod`)
- `github.com/mitchellh/mapstructure` `1.5.0` (golang, `go.mod`)
- `github.com/newrelic/newrelic-client-go/v2` `2.97.5` (golang, `go.mod`)
- `github.com/prometheus/client_golang` `1.24.0` (golang, `go.mod`)
- `github.com/prometheus/client_model` `0.6.3` (golang, `go.mod`)
- ... (+1967 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_fcccb900_0da2_4301_a2f5_68f45cacfc20["fcccb900-0da2-4301-a2f5-68f45cacfc20"]:::atlasCategory
        mod_manifests_crds["manifests/crds"]:::atlasCategory
        mod_manifests_role["manifests/role"]:::atlasCategory
        mod_test_kustomize_rollout["test/kustomize/rollout"]:::atlasCategory
        mod_ui["ui"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
        art_Dockerfile_dev["Dockerfile.dev"]:::atlasWorkflow
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_cherry_pick_single_yml_cherry_pick["cherry-pick-single.yml#cherry-pick"]:::atlasJob
        job_image_reuse_yaml_publish["image-reuse.yaml#publish"]:::atlasJob
        job_release_yaml_generate_sbom["release.yaml#generate-sbom"]:::atlasJob
        job_testing_yaml_test_e2e["testing.yaml#test-e2e"]:::atlasJob
        job_testing_yaml_test_ui["testing.yaml#test-ui"]:::atlasJob
    end
    subgraph runtime_envs["Runtime Environments"]
        env_kubernetes["kubernetes"]:::atlasTarget
    end
    job_testing_yaml_test_e2e -->|DEPLOYS_TO| env_kubernetes
    mod_fcccb900_0da2_4301_a2f5_68f45cacfc20 -->|DEPLOYED_BY| job_image_reuse_yaml_publish
    mod_fcccb900_0da2_4301_a2f5_68f45cacfc20 -->|PACKAGED_BY| art_Dockerfile
    mod_fcccb900_0da2_4301_a2f5_68f45cacfc20 -->|PACKAGED_BY| art_Dockerfile_dev
    mod_manifests_crds -->|DEPLOYED_BY| job_testing_yaml_test_e2e
    mod_manifests_role -->|PACKAGED_BY| art_Dockerfile
    mod_manifests_role -->|PACKAGED_BY| art_Dockerfile_dev
    mod_test_kustomize_rollout -->|PACKAGED_BY| art_Dockerfile
    mod_test_kustomize_rollout -->|PACKAGED_BY| art_Dockerfile_dev
    mod_ui -->|BUILT_BY| job_cherry_pick_single_yml_cherry_pick
    mod_ui -->|BUILT_BY| job_release_yaml_generate_sbom
    mod_ui -->|BUILT_BY| job_testing_yaml_test_ui
    mod_ui -->|DEPLOYED_BY| job_testing_yaml_test_e2e
    mod_ui -->|PACKAGED_BY| art_Dockerfile
    mod_ui -->|PACKAGED_BY| art_Dockerfile_dev
    art_Dockerfile -->|BUILT_BY| job_image_reuse_yaml_publish
```

- `testing.yaml#test-e2e` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `fcccb900-0da2-4301-a2f5-68f45cacfc20` (code_module) --[DEPLOYED_BY]--> `image-reuse.yaml#publish` (ci_job)
- `fcccb900-0da2-4301-a2f5-68f45cacfc20` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `fcccb900-0da2-4301-a2f5-68f45cacfc20` (code_module) --[PACKAGED_BY]--> `Dockerfile.dev` (container)
- `manifests/crds` (code_module) --[DEPLOYED_BY]--> `testing.yaml#test-e2e` (ci_job)
- `manifests/role` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `manifests/role` (code_module) --[PACKAGED_BY]--> `Dockerfile.dev` (container)
- `test/kustomize/rollout` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `test/kustomize/rollout` (code_module) --[PACKAGED_BY]--> `Dockerfile.dev` (container)
- `ui` (code_module) --[BUILT_BY]--> `cherry-pick-single.yml#cherry-pick` (ci_job)
- `ui` (code_module) --[BUILT_BY]--> `release.yaml#generate-sbom` (ci_job)
- `ui` (code_module) --[BUILT_BY]--> `testing.yaml#test-ui` (ci_job)
- `ui` (code_module) --[DEPLOYED_BY]--> `testing.yaml#test-e2e` (ci_job)
- `ui` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)
- `ui` (code_module) --[PACKAGED_BY]--> `Dockerfile.dev` (container)
- `Dockerfile` (container) --[BUILT_BY]--> `image-reuse.yaml#publish` (ci_job)


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
  pipeline_root(["argoproj/argo-rollouts (13 workflows)"]):::atlasRoot
  subgraph sg_grp_0_CI___Verification["CI & Verification (6 workflows · 12 jobs)"]
    direction TB
    subgraph sg_wf_2_Cherry_Pick["Cherry Pick (2 jobs)"]
      direction TB
      wf_2_Cherry_Pick(["Trigger: Cherry Pick"]):::atlasWorkflow
      job_2_find_labels["find-labels"]:::atlasJob
      job_2_cherry_pick["cherry-pick"]:::atlasJob
      wf_2_Cherry_Pick --> job_2_find_labels
      job_2_find_labels --> job_2_cherry_pick
    end
    pipeline_root --> wf_2_Cherry_Pick
    subgraph sg_wf_4_Docker["Docker (3 jobs)"]
      direction TB
      wf_4_Docker(["Trigger: Docker"]):::atlasWorkflow
      job_4_set_vars["set-vars"]:::atlasJob
      job_4_build_and_push_controller_image["build-and-push-controller-image"]:::atlasJob
      job_4_build_and_push_plugin_image["build-and-push-plugin-image"]:::atlasJob
      wf_4_Docker --> job_4_set_vars
      job_4_set_vars --> job_4_build_and_push_controller_image
      job_4_set_vars --> job_4_build_and_push_plugin_image
    end
    pipeline_root --> wf_4_Docker
    subgraph sg_wf_5_Go["Go (4 jobs)"]
      direction TB
      wf_5_Go(["Trigger: Go"]):::atlasWorkflow
      job_5_changes["changes"]:::atlasJob
      job_5_lint_go["lint-go"]:::atlasJob
      job_5_build["build"]:::atlasJob
      wf_5_Go --> job_5_changes
      job_5_changes --> job_5_lint_go
      job_5_changes --> job_5_build
    end
    pipeline_root --> wf_5_Go
  end
  subgraph sg_grp_1_Release___Deploy["Release & Deploy (3 workflows · 11 jobs)"]
    direction TB
    subgraph sg_wf_0_Update_Changelog["Update Changelog (1 jobs)"]
      direction TB
      wf_0_Update_Changelog(["Trigger: Update Changelog"]):::atlasWorkflow
      job_0_updateChangelog["updateChangelog"]:::atlasJob
      wf_0_Update_Changelog --> job_0_updateChangelog
    end
    pipeline_root --> wf_0_Update_Changelog
    subgraph sg_wf_6_Publish_and_Sign_Container_Image["Publish and Sign Container Image (1 jobs)"]
      direction TB
      wf_6_Publish_and_Sign_Container_Image(["Trigger: Publish and Sign Container Image"]):::atlasWorkflow
      job_6_publish["publish"]:::atlasJob
      wf_6_Publish_and_Sign_Container_Image --> job_6_publish
    end
    pipeline_root --> wf_6_Publish_and_Sign_Container_Image
    subgraph sg_wf_8_Release["Release (9 jobs)"]
      direction TB
      wf_8_Release(["Trigger: Release"]):::atlasWorkflow
      job_8_set_registry_namespace["set-registry-namespace"]:::atlasJob
      job_8_controller_image["controller-image"]:::atlasJob
      job_8_plugin_image["plugin-image"]:::atlasJob
      wf_8_Release --> job_8_set_registry_namespace
      job_8_set_registry_namespace --> job_8_controller_image
      job_8_set_registry_namespace --> job_8_plugin_image
    end
    pipeline_root --> wf_8_Release
  end
  subgraph sg_grp_2_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_9_Close_stale_issues_and_PRs["Close stale issues and PRs (1 jobs)"]
      direction TB
      wf_9_Close_stale_issues_and_PRs(["Trigger: Close stale issues and PRs"]):::atlasWorkflow
      job_9_stale["stale"]:::atlasJob
      wf_9_Close_stale_issues_and_PRs --> job_9_stale
    end
    pipeline_root --> wf_9_Close_stale_issues_and_PRs
    subgraph sg_wf_12_Close_stale_issues_and_PRs_waiting_for_response["Close stale issues and PRs waiting for response (1 jobs)"]
      direction TB
      wf_12_Close_stale_issues_and_PRs_waiting_for_response(["Trigger: Close stale issues and PRs waiting for response"]):::atlasWorkflow
      job_12_stale["stale"]:::atlasJob
      wf_12_Close_stale_issues_and_PRs_waiting_for_response --> job_12_stale
    end
    pipeline_root --> wf_12_Close_stale_issues_and_PRs_waiting_for_response
  end
  subgraph sg_grp_3_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_1_Cherry_Pick_Single["Cherry Pick Single (1 jobs)"]
      direction TB
      wf_1_Cherry_Pick_Single(["Trigger: Cherry Pick Single"]):::atlasWorkflow
      job_1_cherry_pick["cherry-pick"]:::atlasJob
      wf_1_Cherry_Pick_Single --> job_1_cherry_pick
    end
    pipeline_root --> wf_1_Cherry_Pick_Single
  end
  subgraph sg_grp_4_Scheduled___Manual["Scheduled & Manual (1 workflows · 7 jobs)"]
    direction TB
    wf_11_Testing["Testing (7 jobs)"]:::atlasWorkflow
    pipeline_root --> wf_11_Testing
  end
  wf_more["+3 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
