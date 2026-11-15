---
title: Architecture — RocketChat/helm-charts
description: Arc42 and Pipeline report for RocketChat/helm-charts
---

# Repository Architecture Analysis: RocketChat/helm-charts

## Metadata
- **SHA**: `c3c3f5bfde5f1757f57220a10815eee02c69447f`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 77
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 77
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Helm Chart
- **import_edges**: 0 entry(ies)
- **loc**: 5590
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 4705
- **test_file_count**: 9

# Architecture: RocketChat/helm-charts

## Context
- **Repository**: `RocketChat/helm-charts`
- **SHA**: `c3c3f5bfde5f1757f57220a10815eee02c69447f`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Helm Chart

## Building Block View

```mermaid
graph TD;
    repo_root(["RocketChat/helm-charts (77 components)"])
    dir_0_rocketchat["rocketchat (30)"]
    repo_root --> dir_0_rocketchat
    sub_0_0_templates["templates (26)"]
    dir_0_rocketchat --> sub_0_0_templates
    sub_0_1__module_root_["(module root) (2)"]
    dir_0_rocketchat --> sub_0_1__module_root_
    sub_0_2_tests["tests (2)"]
    dir_0_rocketchat --> sub_0_2_tests
    dir_1_rocketchat_voip["rocketchat-voip (15)"]
    repo_root --> dir_1_rocketchat_voip
    sub_1_0_templates["templates (12)"]
    dir_1_rocketchat_voip --> sub_1_0_templates
    sub_1_1__module_root_["(module root) (3)"]
    dir_1_rocketchat_voip --> sub_1_1__module_root_
    dir_2_rocketchat_livekit["rocketchat-livekit (14)"]
    repo_root --> dir_2_rocketchat_livekit
    sub_2_0_templates["templates (9)"]
    dir_2_rocketchat_livekit --> sub_2_0_templates
    sub_2_1__module_root_["(module root) (4)"]
    dir_2_rocketchat_livekit --> sub_2_1__module_root_
    sub_2_2_tests["tests (1)"]
    dir_2_rocketchat_livekit --> sub_2_2_tests
    dir_3_monitoring["monitoring (13)"]
    repo_root --> dir_3_monitoring
    sub_3_0_templates["templates (8)"]
    dir_3_monitoring --> sub_3_0_templates
    sub_3_1__module_root_["(module root) (2)"]
    dir_3_monitoring --> sub_3_1__module_root_
    sub_3_2_config["config (2)"]
    dir_3_monitoring --> sub_3_2_config
    sub_3_more["+1 more submodules (1)"]
    dir_3_monitoring --> sub_3_more
    dir_4_mock["mock (5)"]
    repo_root --> dir_4_mock
```

## Component Details

Showing top 60 representative components out of 77 across 5 module group(s):

- **Module `rocketchat`** (30 components — module: 30)
- **Module `rocketchat-voip`** (15 components — module: 15)
- **Module `rocketchat-livekit`** (14 components — module: 14)
- **Module `monitoring`** (13 components — module: 13)
- **Module `mock`** (5 components — module: 5)

- **Chart** (`monitoring/Chart.yaml`): module
- **Chart** (`rocketchat-livekit/Chart.yaml`): module
- **Chart** (`rocketchat-voip/Chart.yaml`): module
- **Chart** (`rocketchat/Chart.yaml`): module
- **_validations** (`rocketchat/templates/_validations.yaml`): module
- **chat-deployment** (`rocketchat/templates/chat-deployment.yaml`): module
- **compose** (`mock/compose.yaml`): module
- **configmap** (`rocketchat-livekit/templates/configmap.yaml`): module
- **deployment** (`rocketchat-livekit/templates/deployment.yaml`): module
- **drachtio-deployment** (`rocketchat-voip/templates/drachtio-deployment.yaml`): module
- **drachtio-secret** (`rocketchat-voip/templates/drachtio-secret.yaml`): module
- **drachtio-service** (`rocketchat-voip/templates/drachtio-service.yaml`): module
- **drachtio-servicemonitor** (`rocketchat-voip/templates/drachtio-servicemonitor.yaml`): module
- **events** (`monitoring/config/opentelemetry/events.yaml`): module
- **freeswitch-configmap** (`rocketchat-voip/templates/freeswitch-configmap.yaml`): module
- **freeswitch-deployment** (`rocketchat-voip/templates/freeswitch-deployment.yaml`): module
- **freeswitch-ingress** (`rocketchat-voip/templates/freeswitch-ingress.yaml`): module
- **freeswitch-rtp-service-nlb** (`rocketchat-voip/templates/freeswitch-rtp-service-nlb.yaml`): module
- **freeswitch-secret** (`rocketchat-voip/templates/freeswitch-secret.yaml`): module
- **freeswitch-service** (`rocketchat-voip/templates/freeswitch-service.yaml`): module
- **freeswitch-servicemonitor** (`rocketchat-voip/templates/freeswitch-servicemonitor.yaml`): module
- **grafana** (`monitoring/templates/grafana.yaml`): module
- **grafana-dashboards** (`monitoring/templates/grafana-dashboards.yaml`): module
- **ingress** (`monitoring/templates/ingress.yaml`): module
- **ingress** (`rocketchat-livekit/templates/ingress.yaml`): module
- **ingress** (`rocketchat/templates/ingress.yaml`): module
- **kubeconfig** (`mock/kubeconfig.yaml`): module
- **lighttpd** (`rocketchat/templates/lighttpd.yaml`): module
- **logs** (`monitoring/config/opentelemetry/logs.yaml`): module
- **media-service** (`rocketchat-livekit/templates/media-service.yaml`): module
- **microservices-account-deployment** (`rocketchat/templates/microservices-account-deployment.yaml`): module
- **microservices-account-service** (`rocketchat/templates/microservices-account-service.yaml`): module
- **microservices-authorization-deployment** (`rocketchat/templates/microservices-authorization-deployment.yaml`): module
- **microservices-authorization-service** (`rocketchat/templates/microservices-authorization-service.yaml`): module
- **microservices-ddp-streamer-deployment** (`rocketchat/templates/microservices-ddp-streamer-deployment.yaml`): module
- **microservices-ddp-streamer-service** (`rocketchat/templates/microservices-ddp-streamer-service.yaml`): module
- **microservices-presence-deployment** (`rocketchat/templates/microservices-presence-deployment.yaml`): module
- **microservices-presence-service** (`rocketchat/templates/microservices-presence-service.yaml`): module
- **microservices-stream-hub-deployment** (`rocketchat/templates/microservices-stream-hub-deployment.yaml`): module
- **microservices-stream-hub-service** (`rocketchat/templates/microservices-stream-hub-service.yaml`): module
- **microservices-values** (`rocketchat/tests/microservices-values.yaml`): module
- **mongodb-init-configmap** (`rocketchat/templates/mongodb-init-configmap.yaml`): module
- **mongodb-monitor** (`rocketchat/templates/mongodb-monitor.yaml`): module
- **monolith-values** (`rocketchat/tests/monolith-values.yaml`): module
- **nats-monitor** (`rocketchat/templates/nats-monitor.yaml`): module
- **nodes** (`mock/manifests/nodes.yaml`): module
- **otel-collector-configmap** (`monitoring/templates/opentelemetry/otel-collector-configmap.yaml`): module
- **otel-collector-events-deployment** (`monitoring/templates/opentelemetry/otel-collector-events-deployment.yaml`): module
- **otel-collector-logs-daemonset** (`monitoring/templates/opentelemetry/otel-collector-logs-daemonset.yaml`): module
- **otel-collector-service-account** (`monitoring/templates/opentelemetry/otel-collector-service-account.yaml`): module
- **plugin** (`rocketchat-livekit/plugin.yaml`): module
- **poddisruptionbudget** (`rocketchat/templates/poddisruptionbudget.yaml`): module
- **podmonitor** (`rocketchat/templates/podmonitor.yaml`): module
- **pvc** (`rocketchat/templates/pvc.yaml`): module
- **scripts-configmap** (`rocketchat/templates/scripts-configmap.yaml`): module
- **secret** (`rocketchat-livekit/templates/secret.yaml`): module
- **secret** (`rocketchat/templates/secret.yaml`): module
- **service** (`rocketchat-livekit/templates/service.yaml`): module
- **service** (`rocketchat/templates/service.yaml`): module
- **serviceaccount** (`rocketchat-livekit/templates/serviceaccount.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (76.90/100)
- **Technical Debt Score**: 23.10
- **Estimated Remediation Effort**: 20.27h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 34.00 | 0.15 | workflows=4, operational_antipatterns=14, parallel_branches=True |
| Security | `D` | 64.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=3 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_mock["mock"]
        mod_monitoring["monitoring"]
        mod_rocketchat["rocketchat"]
        mod_rocketchat_livekit["rocketchat-livekit"]
        mod_rocketchat_voip["rocketchat-voip"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_mock_Dockerfile["mock/Dockerfile"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_release_yml_release["release.yml#release"]
        job_test_yml_detect_changes["test.yml#detect-changes"]
        job_test_yml_mock["test.yml#mock"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_kubernetes["kubernetes"]
    end
    job_release_yml_release -->|DEPLOYS_TO| env_kubernetes
    mod_mock -->|BUILT_BY| job_test_yml_detect_changes
    mod_mock -->|BUILT_BY| job_test_yml_mock
    mod_mock -->|PACKAGED_BY| art_mock_Dockerfile
    mod_monitoring -->|BUILT_BY| job_test_yml_detect_changes
    mod_monitoring -->|DEPLOYED_BY| job_release_yml_release
    mod_rocketchat -->|BUILT_BY| job_test_yml_detect_changes
    mod_rocketchat -->|DEPLOYED_BY| job_release_yml_release
    mod_rocketchat_livekit -->|BUILT_BY| job_test_yml_detect_changes
    mod_rocketchat_livekit -->|DEPLOYED_BY| job_release_yml_release
    mod_rocketchat_voip -->|DEPLOYED_BY| job_release_yml_release
    art_mock_Dockerfile -->|BUILT_BY| job_test_yml_detect_changes
```

- `release.yml#release` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `mock` (code_module) --[BUILT_BY]--> `test.yml#detect-changes` (ci_job)
- `mock` (code_module) --[BUILT_BY]--> `test.yml#mock` (ci_job)
- `mock` (code_module) --[PACKAGED_BY]--> `mock/Dockerfile` (container)
- `monitoring` (code_module) --[BUILT_BY]--> `test.yml#detect-changes` (ci_job)
- `monitoring` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `rocketchat` (code_module) --[BUILT_BY]--> `test.yml#detect-changes` (ci_job)
- `rocketchat` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `rocketchat-livekit` (code_module) --[BUILT_BY]--> `test.yml#detect-changes` (ci_job)
- `rocketchat-livekit` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `rocketchat-voip` (code_module) --[DEPLOYED_BY]--> `release.yml#release` (ci_job)
- `mock/Dockerfile` (container) --[BUILT_BY]--> `test.yml#detect-changes` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["RocketChat/helm-charts (4 workflows)"])
  grp_0_Release___Deploy["Release & Deploy (3 workflows · 6 jobs)"]
  pipeline_root --> grp_0_Release___Deploy
  wf_0_Test_and_or_release_helm_chart["Test and/or release helm chart (3 jobs)"]
  grp_0_Release___Deploy --> wf_0_Test_and_or_release_helm_chart
  wf_1_New_chart_release["New chart release (2 jobs)"]
  grp_0_Release___Deploy --> wf_1_New_chart_release
  wf_2_Release_helm_chart["Release helm chart (1 jobs)"]
  grp_0_Release___Deploy --> wf_2_Release_helm_chart
  grp_1_Scheduled___Manual["Scheduled & Manual (1 workflows · 5 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  wf_3_Test_helm_chart["Test helm chart (5 jobs)"]
  grp_1_Scheduled___Manual --> wf_3_Test_helm_chart
```
