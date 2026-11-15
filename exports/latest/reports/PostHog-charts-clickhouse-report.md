---
title: Architecture — PostHog/charts-clickhouse
description: Arc42 and Pipeline report for PostHog/charts-clickhouse
---

# Repository Architecture Analysis: PostHog/charts-clickhouse

## Metadata
- **SHA**: `7daf90bf9361c17f677aa87142361dc1ae54592a`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.05
- **avg_cyclomatic_complexity**: 1.73
- **component_count**: 137
- **dead_code_count**: 1
- **dead_code_symbols**: 1 entry(ies)
- **duplication_pct**: 5.47
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 175
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 20611
- **max_cognitive_complexity**: 23
- **max_cyclomatic_complexity**: 15
- **sloc**: 17136
- **test_file_count**: 124

# Architecture: PostHog/charts-clickhouse

## Context
- **Repository**: `PostHog/charts-clickhouse`
- **SHA**: `7daf90bf9361c17f677aa87142361dc1ae54592a`
- **Ecosystem**: Python
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    repo_root(["PostHog/charts-clickhouse (137 components)"])
    dir_0_charts["charts (136)"]
    repo_root --> dir_0_charts
    sub_0_0_posthog_tests["posthog/tests (67)"]
    dir_0_charts --> sub_0_0_posthog_tests
    sub_0_1_posthog_templates["posthog/templates (64)"]
    dir_0_charts --> sub_0_1_posthog_templates
    sub_0_2_posthog_crds["posthog/crds (3)"]
    dir_0_charts --> sub_0_2_posthog_crds
    sub_0_more["+1 more submodules (2)"]
    dir_0_charts --> sub_0_more
    dir_1__devcontainer[".devcontainer (1)"]
    repo_root --> dir_1__devcontainer
```

## Component Details

Showing top 60 representative components out of 137 across 2 module group(s):

- **Module `charts`** (136 components — module: 136)
- **Module `.devcontainer`** (1 components — module: 1)

- **Chart** (`charts/posthog/Chart.yaml`): module
- **_clickhouse.tpl** (`charts/posthog/tests/_clickhouse.tpl.yaml`): module
- **_initContainers-wait-for-migrations** (`charts/posthog/tests/_initContainers-wait-for-migrations.yaml`): module
- **_postgresql.tpl** (`charts/posthog/tests/_postgresql.tpl.yaml`): module
- **_statsd** (`charts/posthog/tests/_statsd.yaml`): module
- **_topologySpreadConstraints** (`charts/posthog/tests/_topologySpreadConstraints.yaml`): module
- **application-settings** (`charts/posthog/tests/application-settings.yaml`): module
- **cert-issuer** (`charts/posthog/templates/cert-issuer.yaml`): module
- **cert-issuer** (`charts/posthog/tests/cert-issuer.yaml`): module
- **clickhouse-backup-cronjob** (`charts/posthog/templates/clickhouse-backup-cronjob.yaml`): module
- **clickhouse-backup-cronjob** (`charts/posthog/tests/clickhouse-backup-cronjob.yaml`): module
- **clickhouse-instance** (`charts/posthog/tests/clickhouse-instance.yaml`): module
- **clickhouse_instance** (`charts/posthog/templates/clickhouse_instance.yaml`): module
- **clickhouseinstallations.clickhouse.altinity.com** (`charts/posthog/crds/clickhouseinstallations.clickhouse.altinity.com.yaml`): module
- **clickhouseinstallationtemplates.clickhouse.altinity.com** (`charts/posthog/crds/clickhouseinstallationtemplates.clickhouse.altinity.com.yaml`): module
- **clickhouseoperatorconfigurations.clickhouse.altinity.com** (`charts/posthog/crds/clickhouseoperatorconfigurations.clickhouse.altinity.com.yaml`): module
- **cloudwatch** (`charts/posthog/templates/cloudwatch.yaml`): module
- **clusterrole** (`charts/posthog/templates/clickhouse-operator/clusterrole.yaml`): module
- **clusterrole** (`charts/posthog/tests/clickhouse-operator/clusterrole.yaml`): module
- **clusterrolebinding** (`charts/posthog/templates/clickhouse-operator/clusterrolebinding.yaml`): module
- **clusterrolebinding** (`charts/posthog/tests/clickhouse-operator/clusterrolebinding.yaml`): module
- **configmap** (`charts/posthog/templates/clickhouse-operator/configmap.yaml`): module
- **configmap** (`charts/posthog/tests/clickhouse-operator/configmap.yaml`): module
- **cronjob-backup-configmap** (`charts/posthog/templates/cronjob-backup-configmap.yaml`): module
- **decide-deployment** (`charts/posthog/templates/decide-deployment.yaml`): module
- **decide-hpa** (`charts/posthog/templates/decide-hpa.yaml`): module
- **decide-pdb** (`charts/posthog/templates/decide-pdb.yaml`): module
- **decide-service** (`charts/posthog/templates/decide-service.yaml`): module
- **deployment** (`charts/posthog/templates/clickhouse-operator/deployment.yaml`): module
- **deployment** (`charts/posthog/tests/clickhouse-operator/__snapshot__/deployment.yaml`): module
- **deployment** (`charts/posthog/tests/clickhouse-operator/deployment.yaml`): module
- **email-settings** (`charts/posthog/tests/email-settings.yaml`): module
- **error-on-invalid-values** (`charts/posthog/templates/error-on-invalid-values.yaml`): module
- **error-on-invalid-values** (`charts/posthog/tests/error-on-invalid-values.yaml`): module
- **eventrouter** (`charts/posthog/templates/eventrouter.yaml`): module
- **eventrouter** (`charts/posthog/tests/eventrouter.yaml`): module
- **events-deployment** (`charts/posthog/templates/events-deployment.yaml`): module
- **events-deployment** (`charts/posthog/tests/events-deployment.yaml`): module
- **events-hpa** (`charts/posthog/templates/events-hpa.yaml`): module
- **events-hpa** (`charts/posthog/tests/events-hpa.yaml`): module
- **events-pdb** (`charts/posthog/templates/events-pdb.yaml`): module
- **events-service** (`charts/posthog/templates/events-service.yaml`): module
- **events-service** (`charts/posthog/tests/events-service.yaml`): module
- **gce-frontend-config** (`charts/posthog/templates/gce-frontend-config.yaml`): module
- **gke-cert-issuer** (`charts/posthog/templates/gke-cert-issuer.yaml`): module
- **grafana-annotation-post.job** (`charts/posthog/templates/grafana-annotation-post.job.yaml`): module
- **grafana-annotation-pre.job** (`charts/posthog/templates/grafana-annotation-pre.job.yaml`): module
- **grafana-dashboards** (`charts/posthog/templates/grafana-dashboards.yaml`): module
- **grafana-dashboards** (`charts/posthog/tests/grafana-dashboards.yaml`): module
- **ingress** (`charts/posthog/templates/ingress.yaml`): module
- **ingress** (`charts/posthog/tests/ingress.yaml`): module
- **kafka-settings** (`charts/posthog/tests/kafka-settings.yaml`): module
- **migrate-job** (`charts/posthog/tests/migrate-job.yaml`): module
- **migrate.job** (`charts/posthog/templates/migrate.job.yaml`): module
- **object-storage-settings** (`charts/posthog/tests/object-storage-settings.yaml`): module
- **pgbouncer-deployment** (`charts/posthog/templates/pgbouncer-deployment.yaml`): module
- **pgbouncer-deployment** (`charts/posthog/tests/pgbouncer-deployment.yaml`): module
- **pgbouncer-deployment-read** (`charts/posthog/tests/pgbouncer-deployment-read.yaml`): module
- **pgbouncer-hpa** (`charts/posthog/templates/pgbouncer-hpa.yaml`): module
- **pgbouncer-hpa** (`charts/posthog/tests/pgbouncer-hpa.yaml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (55.53/100)
- **Technical Debt Score**: 44.47
- **Estimated Remediation Effort**: 63.46h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `B` | 89.80 | 0.20 | avg_cc=1.73, max_cc=15, duplication=5.47%, dead_code=1 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=7, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 95.50 | 0.15 | avg_cognitive=1.05, max_cognitive=23, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=15, operational_antipatterns=21, parallel_branches=False |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=3, pipeline_security_findings=17 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 7 | **Vulnerabilities**: 0 | **Secrets**: 3

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `ci/kubetest/custom_k8s_resources/redis_external_with_existing_secret.yaml:57` (`redis-password: c3Rh***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `ci/kubetest/custom_k8s_resources/redis_internal_with_existing_secret.yaml:7` (`redis-password: c3Rh***REDACTED***`)
- **[HIGH] `ATRUSS-SEC-005`** at `perf-testing/README.md:8` (`export API_KEY='ws6x***REDACTED***'`)

### Inventory Sample
- `black` `21.12b0` (PyPI, `ci/kubetest/requirements.txt`)
- `click` `8.0.4` (PyPI, `ci/kubetest/requirements.txt`)
- `flake8` `4.0.1` (PyPI, `ci/kubetest/requirements.txt`)
- `isort` `5.10.1` (PyPI, `ci/kubetest/requirements.txt`)
- `kubernetes` `17.17.0` (PyPI, `ci/kubetest/requirements.txt`)
- `kubetest` `0.9.5` (PyPI, `ci/kubetest/requirements.txt`)
- `eslint` `8.27.0` (npm, `package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod__devcontainer[".devcontainer"]
        mod_charts_posthog["charts/posthog"]
        mod_ci_kubetest["ci/kubetest"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__devcontainer_Dockerfile[".devcontainer/Dockerfile"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_pr_deploy_cleanup_yaml_cleanup["pr-deploy-cleanup.yaml#cleanup"]
        job_pr_deploy_yaml_deploy["pr-deploy.yaml#deploy"]
        job_release_chart_yml_release["release-chart.yml#release"]
        job_test_amazon_web_services_install_yaml_aws_install["test-amazon-web-services-install.yaml#aws-install"]
        job_test_digitalocean_install_yaml_do_install["test-digitalocean-install.yaml#do-install"]
        job_test_google_cloud_platform_install_yaml_gcp_install["test-google-cloud-platform-install.yaml#gcp-install"]
        job_test_k6_yaml_test_chart["test-k6.yaml#test-chart"]
        job_test_kubetest_yaml_test_kubetest["test-kubetest.yaml#test-kubetest"]
        job_test_kubetest_yaml_test_kubetest_prep["test-kubetest.yaml#test-kubetest-prep"]
        job_test_lint_helm_yaml_helm_lint["test-lint-helm.yaml#helm-lint"]
        job_test_lint_kubetest_yaml_kubetest["test-lint-kubetest.yaml#kubetest"]
        job_test_unit_helm_yaml_helm_unittest["test-unit-helm.yaml#helm-unittest"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_azure["azure"]
        env_kubernetes["kubernetes"]
    end
    job_pr_deploy_cleanup_yaml_cleanup -->|DEPLOYS_TO| env_kubernetes
    job_pr_deploy_yaml_deploy -->|DEPLOYS_TO| env_kubernetes
    job_release_chart_yml_release -->|DEPLOYS_TO| env_azure
    job_release_chart_yml_release -->|DEPLOYS_TO| env_kubernetes
    job_test_amazon_web_services_install_yaml_aws_install -->|DEPLOYS_TO| env_kubernetes
    job_test_digitalocean_install_yaml_do_install -->|DEPLOYS_TO| env_kubernetes
    job_test_google_cloud_platform_install_yaml_gcp_install -->|DEPLOYS_TO| env_kubernetes
    job_test_k6_yaml_test_chart -->|DEPLOYS_TO| env_kubernetes
    job_test_kubetest_yaml_test_kubetest -->|DEPLOYS_TO| env_kubernetes
    job_test_lint_helm_yaml_helm_lint -->|DEPLOYS_TO| env_kubernetes
    job_test_unit_helm_yaml_helm_unittest -->|DEPLOYS_TO| env_kubernetes
    mod__devcontainer -->|PACKAGED_BY| art__devcontainer_Dockerfile
    mod_charts_posthog -->|BUILT_BY| job_test_lint_helm_yaml_helm_lint
    mod_charts_posthog -->|BUILT_BY| job_test_unit_helm_yaml_helm_unittest
    mod_charts_posthog -->|DEPLOYED_BY| job_pr_deploy_yaml_deploy
    mod_charts_posthog -->|DEPLOYED_BY| job_release_chart_yml_release
    mod_charts_posthog -->|DEPLOYED_BY| job_test_amazon_web_services_install_yaml_aws_install
    mod_charts_posthog -->|DEPLOYED_BY| job_test_digitalocean_install_yaml_do_install
    mod_charts_posthog -->|DEPLOYED_BY| job_test_google_cloud_platform_install_yaml_gcp_install
    mod_charts_posthog -->|DEPLOYED_BY| job_test_k6_yaml_test_chart
    mod_ci_kubetest -->|BUILT_BY| job_test_kubetest_yaml_test_kubetest
    mod_ci_kubetest -->|BUILT_BY| job_test_kubetest_yaml_test_kubetest_prep
    mod_ci_kubetest -->|BUILT_BY| job_test_lint_kubetest_yaml_kubetest
```

- `pr-deploy-cleanup.yaml#cleanup` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `pr-deploy.yaml#deploy` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `release-chart.yml#release` (ci_job) --[DEPLOYS_TO]--> `azure` (environment)
- `release-chart.yml#release` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-amazon-web-services-install.yaml#aws-install` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-digitalocean-install.yaml#do-install` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-google-cloud-platform-install.yaml#gcp-install` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-k6.yaml#test-chart` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-kubetest.yaml#test-kubetest` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-lint-helm.yaml#helm-lint` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `test-unit-helm.yaml#helm-unittest` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `.devcontainer` (code_module) --[PACKAGED_BY]--> `.devcontainer/Dockerfile` (container)
- `charts/posthog` (code_module) --[BUILT_BY]--> `test-lint-helm.yaml#helm-lint` (ci_job)
- `charts/posthog` (code_module) --[BUILT_BY]--> `test-unit-helm.yaml#helm-unittest` (ci_job)
- `charts/posthog` (code_module) --[DEPLOYED_BY]--> `pr-deploy.yaml#deploy` (ci_job)
- `charts/posthog` (code_module) --[DEPLOYED_BY]--> `release-chart.yml#release` (ci_job)
- `charts/posthog` (code_module) --[DEPLOYED_BY]--> `test-amazon-web-services-install.yaml#aws-install` (ci_job)
- `charts/posthog` (code_module) --[DEPLOYED_BY]--> `test-digitalocean-install.yaml#do-install` (ci_job)
- `charts/posthog` (code_module) --[DEPLOYED_BY]--> `test-google-cloud-platform-install.yaml#gcp-install` (ci_job)
- `charts/posthog` (code_module) --[DEPLOYED_BY]--> `test-k6.yaml#test-chart` (ci_job)
- `ci/kubetest` (code_module) --[BUILT_BY]--> `test-kubetest.yaml#test-kubetest` (ci_job)
- `ci/kubetest` (code_module) --[BUILT_BY]--> `test-kubetest.yaml#test-kubetest-prep` (ci_job)
- `ci/kubetest` (code_module) --[BUILT_BY]--> `test-lint-kubetest.yaml#kubetest` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["PostHog/charts-clickhouse (15 workflows)"])
  grp_0_Scheduled___Manual["Scheduled & Manual (10 workflows · 11 jobs)"]
  pipeline_root --> grp_0_Scheduled___Manual
  grp_1_Release___Deploy["Release & Deploy (3 workflows · 3 jobs)"]
  pipeline_root --> grp_1_Release___Deploy
  grp_2_CI___Verification["CI & Verification (2 workflows · 2 jobs)"]
  pipeline_root --> grp_2_CI___Verification
```
