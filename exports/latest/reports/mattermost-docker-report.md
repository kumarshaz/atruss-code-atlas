---
title: Architecture — mattermost/docker
description: Arc42 and Pipeline report for mattermost/docker
---

# Repository Architecture Analysis: mattermost/docker

## Metadata
- **SHA**: `12bbeda5009e1d8381be294a88d1cb69dc624290`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 5
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 5
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Docker Compose
- **import_edges**: 0 entry(ies)
- **loc**: 208
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 153

# Architecture: mattermost/docker

## Context
- **Repository**: `mattermost/docker`
- **SHA**: `12bbeda5009e1d8381be294a88d1cb69dc624290`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Docker Compose

## Building Block View

```mermaid
graph TD;
    docker_compose_nginx["docker-compose.nginx : module"]
    docker_compose_without_nginx["docker-compose.without-nginx : module"]
    docker_compose["docker-compose : module"]
    docker_test["docker-test : module"]
    shellcheck["shellcheck : module"]
    repo_root(["mattermost/docker"])
    repo_root --> docker_compose
    repo_root --> docker_compose_nginx
    repo_root --> docker_compose_without_nginx
    repo_root --> docker_test
    repo_root --> shellcheck
```

## Component Details
- **docker-compose.nginx** (`docker-compose.nginx.yml`): module
- **docker-compose.without-nginx** (`docker-compose.without-nginx.yml`): module
- **docker-compose** (`docker-compose.yml`): module
- **docker-test** (`.github/workflows/docker-test.yml`): module
- **shellcheck** (`.github/workflows/shellcheck.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (84.55/100)
- **Technical Debt Score**: 15.45
- **Estimated Remediation Effort**: 10.86h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `B` | 85.00 | 0.15 | workflows=2, operational_antipatterns=4, parallel_branches=False |
| Security | `D` | 64.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=3 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_97faa1dc_dbc9_4ad1_8cfd_1ad359fe309e["97faa1dc-dbc9-4ad1-8cfd-1ad359fe309e"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_docker_compose_nginx_yml["docker-compose.nginx.yml"]
        art_docker_compose_without_nginx_yml["docker-compose.without-nginx.yml"]
        art_docker_compose_yml["docker-compose.yml"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_docker_test_yml_test_docker_deployment["docker-test.yml#test-docker-deployment"]
        job_docker_test_yml_validate_compose_files["docker-test.yml#validate-compose-files"]
        job_shellcheck_yml_shellcheck["shellcheck.yml#shellcheck"]
    end
    mod_97faa1dc_dbc9_4ad1_8cfd_1ad359fe309e -->|BUILT_BY| job_shellcheck_yml_shellcheck
    mod_97faa1dc_dbc9_4ad1_8cfd_1ad359fe309e -->|PACKAGED_BY| art_docker_compose_nginx_yml
    mod_97faa1dc_dbc9_4ad1_8cfd_1ad359fe309e -->|PACKAGED_BY| art_docker_compose_without_nginx_yml
    mod_97faa1dc_dbc9_4ad1_8cfd_1ad359fe309e -->|PACKAGED_BY| art_docker_compose_yml
    art_docker_compose_nginx_yml -->|BUILT_BY| job_docker_test_yml_validate_compose_files
    art_docker_compose_without_nginx_yml -->|BUILT_BY| job_docker_test_yml_validate_compose_files
    art_docker_compose_without_nginx_yml -->|DEPLOYED_BY| job_docker_test_yml_test_docker_deployment
    art_docker_compose_yml -->|BUILT_BY| job_docker_test_yml_validate_compose_files
    art_docker_compose_yml -->|DEPLOYED_BY| job_docker_test_yml_test_docker_deployment
```

- `97faa1dc-dbc9-4ad1-8cfd-1ad359fe309e` (code_module) --[BUILT_BY]--> `shellcheck.yml#shellcheck` (ci_job)
- `97faa1dc-dbc9-4ad1-8cfd-1ad359fe309e` (code_module) --[PACKAGED_BY]--> `docker-compose.nginx.yml` (container)
- `97faa1dc-dbc9-4ad1-8cfd-1ad359fe309e` (code_module) --[PACKAGED_BY]--> `docker-compose.without-nginx.yml` (container)
- `97faa1dc-dbc9-4ad1-8cfd-1ad359fe309e` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `docker-compose.nginx.yml` (container) --[BUILT_BY]--> `docker-test.yml#validate-compose-files` (ci_job)
- `docker-compose.without-nginx.yml` (container) --[BUILT_BY]--> `docker-test.yml#validate-compose-files` (ci_job)
- `docker-compose.without-nginx.yml` (container) --[DEPLOYED_BY]--> `docker-test.yml#test-docker-deployment` (ci_job)
- `docker-compose.yml` (container) --[BUILT_BY]--> `docker-test.yml#validate-compose-files` (ci_job)
- `docker-compose.yml` (container) --[DEPLOYED_BY]--> `docker-test.yml#test-docker-deployment` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["mattermost/docker"])
  subgraph Docker_Test_0["Docker Test"]
    direction TB
    0_validate_compose_files["validate-compose-files"]
    0_test_docker_deployment["test-docker-deployment"]
    0_validate_compose_files --> 0_test_docker_deployment
  end
  pipeline_root --> 0_validate_compose_files
  subgraph ShellCheck_1["ShellCheck"]
    direction TB
    1_shellcheck["shellcheck"]
  end
  pipeline_root --> 1_shellcheck
```
