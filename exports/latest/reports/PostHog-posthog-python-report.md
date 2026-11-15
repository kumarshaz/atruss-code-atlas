---
title: Architecture — PostHog/posthog-python
description: Arc42 and Pipeline report for PostHog/posthog-python
---

# Repository Architecture Analysis: PostHog/posthog-python

## Metadata
- **SHA**: `ec112a6201569e1cf5e9b8827a01793de523f643`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.52
- **avg_cyclomatic_complexity**: 2.08
- **component_count**: 45
- **dead_code_count**: 40
- **dead_code_symbols**: 40 entry(ies)
- **duplication_pct**: 82.71
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 410
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: FastAPI
- **import_edges**: 100 entry(ies)
- **loc**: 164011
- **max_cognitive_complexity**: 57
- **max_cyclomatic_complexity**: 24
- **sloc**: 134186
- **test_file_count**: 192

# Architecture: PostHog/posthog-python

## Context
- **Repository**: `PostHog/posthog-python`
- **SHA**: `ec112a6201569e1cf5e9b8827a01793de523f643`
- **Ecosystem**: Python
- **Framework**: FastAPI

## Building Block View

```mermaid
graph TD;
    repo_root(["PostHog/posthog-python (45 components)"])
    dir_0_posthog["posthog (21)"]
    repo_root --> dir_0_posthog
    sub_0_0_test["test (17)"]
    dir_0_posthog --> sub_0_0_test
    sub_0_1_tracing["tracing (2)"]
    dir_0_posthog --> sub_0_1_tracing
    sub_0_2__module_root_["(module root) (1)"]
    dir_0_posthog --> sub_0_2__module_root_
    sub_0_more["+1 more submodules (1)"]
    dir_0_posthog --> sub_0_more
    dir_1_playgrounds["playgrounds (12)"]
    repo_root --> dir_1_playgrounds
    sub_1_0_fastapi_async_client["fastapi-async-client (10)"]
    dir_1_playgrounds --> sub_1_0_fastapi_async_client
    sub_1_1_fastapi_exception_capture["fastapi-exception-capture (2)"]
    dir_1_playgrounds --> sub_1_1_fastapi_exception_capture
    dir_2_sdk_compliance_adapter["sdk_compliance_adapter (11)"]
    repo_root --> dir_2_sdk_compliance_adapter
    dir_3_examples["examples (1)"]
    repo_root --> dir_3_examples
    sub_0_0_test -.->|"2 deps"| sub_0_more
    sub_0_0_test -.->|"1 dep"| sub_0_1_tracing
    sub_0_more -.->|"1 dep"| sub_0_1_tracing
```

## Component Details
- **UserInfo** (`examples/example-ai-instructor/extract.py`): DATA_ACCESS_LAYER
- **root** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **capture** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **capture_immediate** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **identify** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **group_identify** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **alias** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **evaluate_flags** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **remote_config** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **flush** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **test_exception** (`playgrounds/fastapi-async-client/main.py`): API_ROUTE
- **root** (`playgrounds/fastapi-exception-capture/app.py`): API_ROUTE
- **test_exception** (`playgrounds/fastapi-exception-capture/app.py`): API_ROUTE
- **_GatedExporter** (`posthog/_metrics_autocapture.py`): SERVICE
- **PostHogTraceExporter** (`posthog/ai/otel/exporter.py`): SERVICE (deps: SpanExporter)
- **ModelV2** (`posthog/test/test_utils.py`): DATA_ACCESS_LAYER
- **NestedModel** (`posthog/test/test_utils.py`): DATA_ACCESS_LAYER
- **_Parsed** (`posthog/test/ai/test_privacy_mode.py`): DATA_ACCESS_LAYER (deps: PostHogTraceExporter)
- **TestPostHogTraceExporter** (`posthog/test/ai/otel/test_exporter.py`): SERVICE (deps: PostHogTraceExporter)
- **view** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **privacy_failure** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **failure** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **handled** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **missing** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **capture_event** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **ignored** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **identity** (`posthog/test/integrations/test_flask_integration.py`): API_ROUTE
- **view** (`posthog/test/integrations/test_flask_spans.py`): API_ROUTE
- **view** (`posthog/test/integrations/test_tracing_headers.py`): API_ROUTE
- **Totals** (`posthog/test/mcp/test_review_fixes.py`): DATA_ACCESS_LAYER
- **RecordingExporter** (`posthog/test/tracing/helpers.py`): SERVICE (deps: SpanExporter)
- **TestContextManager** (`posthog/test/tracing/test_span.py`): SERVICE
- **SpanExporter** (`posthog/tracing/_export.py`): SERVICE
- **Exporter** (`posthog/tracing/_pipeline.py`): SERVICE
- **health** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **init** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **capture** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **capture_ai** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **identify** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **flush** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **get_state** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **reload_feature_flag_definitions** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **get_feature_flag** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **get_feature_flag_payload** (`sdk_compliance_adapter/adapter.py`): API_ROUTE
- **reset** (`sdk_compliance_adapter/adapter.py`): API_ROUTE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (39.35/100)
- **Technical Debt Score**: 60.65
- **Estimated Remediation Effort**: 115.70h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 41.50 | 0.20 | avg_cc=2.08, max_cc=24, duplication=82.71%, dead_code=40 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=2418, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=1.52, max_cognitive=57, fitness_violations=3, oversized_files=24 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=12, operational_antipatterns=30, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=6, pipeline_security_findings=2 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (82.71) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (57.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (24.0) exceeds policy threshold (20.0).

### Workspace Packages
- **openfeature-provider-posthog** (`openfeature-provider`, python, uv)

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 2418 | **Vulnerabilities**: 0 | **Secrets**: 6

### Secret Findings (Redacted)
- **[CRITICAL] `ATRUSS-SEC-003`** at `posthog/test/mcp/test_error_properties.py:302` (`error=ValueError("auth failed for sk-p***REDACTED***"),`)
- **[HIGH] `ATRUSS-SEC-005`** at `posthog/test/test_code_variables.py:532` (`secret = "n8fK***REDACTED***"`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `posthog/test/test_code_variables.py:1214` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[CRITICAL] `ATRUSS-SEC-004`** at `posthog/test/test_code_variables.py:1215` (`-----BEGIN ... PRIVATE KEY----- [REDACTED]`)
- **[HIGH] `ATRUSS-SEC-005`** at `posthog/test/test_code_variables.py:1355` (`secret = "n8fK***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `posthog/test/test_utils.py:22` (`TEST_API_KEY = "kOOl***REDACTED***"`)

### Inventory Sample
- `anthropic` `0.72` (PyPI, `pyproject.toml`)
- `anthropic` `0.80.0` (PyPI, `examples/example-ai-anthropic/pyproject.toml`)
- `anthropic` `0.87.0` (PyPI, `examples/example-ai-anthropic/uv.lock`)
- `anthropic` `1.13.0` (PyPI, `uv.lock`)
- `autogen-agentchat` `0.4.0` (PyPI, `examples/example-ai-autogen/pyproject.toml`)
- `autogen-agentchat` `0.7.5` (PyPI, `examples/example-ai-autogen/uv.lock`)
- `autogen-ext` `0.4.0` (PyPI, `examples/example-ai-autogen/pyproject.toml`)
- `autogen-ext` `0.7.5` (PyPI, `examples/example-ai-autogen/uv.lock`)
- `azure-ai-agents` `1.2.0b6` (PyPI, `examples/example-ai-semantic-kernel/pyproject.toml`)
- `azure-ai-agents` `1.2.0b6` (PyPI, `examples/example-ai-semantic-kernel/uv.lock`)
- `backoff` `1.10.0` (PyPI, `pyproject.toml`)
- `backoff` `2.2.1` (PyPI, `uv.lock`)
- `boto3` `1.35.0` (PyPI, `examples/example-ai-aws-bedrock/pyproject.toml`)
- `boto3` `1.42.76` (PyPI, `examples/example-ai-aws-bedrock/uv.lock`)
- `celery` `5.3` (PyPI, `pyproject.toml`)
- `celery` `5.6.3` (PyPI, `uv.lock`)
- `claude-agent-sdk` `*` (PyPI, `examples/example-ai-claude-agent-sdk/requirements.txt`)
- `claude-agent-sdk` `*` (PyPI, `pyproject.toml`)
- `claude-agent-sdk` `0.2.121` (PyPI, `uv.lock`)
- `coverage` `*` (PyPI, `pyproject.toml`)
- `coverage` `7.9.2` (PyPI, `uv.lock`)
- `crewai` `0.80.0` (PyPI, `examples/example-ai-crewai/pyproject.toml`)
- `crewai` `0.95.0` (PyPI, `examples/example-ai-crewai/uv.lock`)
- `distro` `1.5.0` (PyPI, `pyproject.toml`)
- `distro` `1.9.0` (PyPI, `uv.lock`)
- `django` `5.2.15` (PyPI, `pyproject.toml`)
- `django` `5.2.17` (PyPI, `integration_tests/django5/pyproject.toml`)
- `django` `5.2.17` (PyPI, `integration_tests/django5/uv.lock`)
- `django` `5.2.17` (PyPI, `uv.lock`)
- `django-stubs` `*` (PyPI, `pyproject.toml`)
- ... (+2388 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_benchmarks["benchmarks"]
        mod_integration_tests_django5["integration_tests/django5"]
        mod_openfeature_provider["openfeature-provider"]
        mod_sdk_compliance_adapter["sdk_compliance_adapter"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_sdk_compliance_adapter_Dockerfile["sdk_compliance_adapter/Dockerfile"]
        art_sdk_compliance_adapter_Dockerfile_v1["sdk_compliance_adapter/Dockerfile.v1"]
        art_sdk_compliance_adapter_docker_compose_yml["sdk_compliance_adapter/docker-compose.yml"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_benchmarks_yml_benchmark["benchmarks.yml#benchmark"]
        job_ci_yml_django5_integration["ci.yml#django5-integration"]
        job_ci_yml_openfeature_provider["ci.yml#openfeature-provider"]
        job_release_yml_dry_run_testpypi["release.yml#dry-run-testpypi"]
        job_release_yml_version_bump["release.yml#version-bump"]
        job_sdk_compliance_yml_adapter_tests["sdk-compliance.yml#adapter-tests"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_Release["Release"]
    end
    job_release_yml_version_bump -->|DEPLOYS_TO| env_Release
    mod_benchmarks -->|BUILT_BY| job_benchmarks_yml_benchmark
    mod_integration_tests_django5 -->|BUILT_BY| job_ci_yml_django5_integration
    mod_openfeature_provider -->|BUILT_BY| job_ci_yml_openfeature_provider
    mod_openfeature_provider -->|DEPLOYED_BY| job_release_yml_dry_run_testpypi
    mod_openfeature_provider -->|DEPLOYED_BY| job_release_yml_version_bump
    mod_sdk_compliance_adapter -->|BUILT_BY| job_sdk_compliance_yml_adapter_tests
    mod_sdk_compliance_adapter -->|PACKAGED_BY| art_sdk_compliance_adapter_Dockerfile
    mod_sdk_compliance_adapter -->|PACKAGED_BY| art_sdk_compliance_adapter_Dockerfile_v1
    mod_sdk_compliance_adapter -->|PACKAGED_BY| art_sdk_compliance_adapter_docker_compose_yml
    art_sdk_compliance_adapter_Dockerfile -->|BUILT_BY| job_sdk_compliance_yml_adapter_tests
    art_sdk_compliance_adapter_Dockerfile_v1 -->|BUILT_BY| job_sdk_compliance_yml_adapter_tests
    art_sdk_compliance_adapter_docker_compose_yml -->|BUILT_BY| job_sdk_compliance_yml_adapter_tests
```

- `release.yml#version-bump` (ci_job) --[DEPLOYS_TO]--> `Release` (environment)
- `benchmarks` (code_module) --[BUILT_BY]--> `benchmarks.yml#benchmark` (ci_job)
- `integration_tests/django5` (code_module) --[BUILT_BY]--> `ci.yml#django5-integration` (ci_job)
- `openfeature-provider` (code_module) --[BUILT_BY]--> `ci.yml#openfeature-provider` (ci_job)
- `openfeature-provider` (code_module) --[DEPLOYED_BY]--> `release.yml#dry-run-testpypi` (ci_job)
- `openfeature-provider` (code_module) --[DEPLOYED_BY]--> `release.yml#version-bump` (ci_job)
- `sdk_compliance_adapter` (code_module) --[BUILT_BY]--> `sdk-compliance.yml#adapter-tests` (ci_job)
- `sdk_compliance_adapter` (code_module) --[PACKAGED_BY]--> `sdk_compliance_adapter/Dockerfile` (container)
- `sdk_compliance_adapter` (code_module) --[PACKAGED_BY]--> `sdk_compliance_adapter/Dockerfile.v1` (container)
- `sdk_compliance_adapter` (code_module) --[PACKAGED_BY]--> `sdk_compliance_adapter/docker-compose.yml` (container)
- `sdk_compliance_adapter/Dockerfile` (container) --[BUILT_BY]--> `sdk-compliance.yml#adapter-tests` (ci_job)
- `sdk_compliance_adapter/Dockerfile.v1` (container) --[BUILT_BY]--> `sdk-compliance.yml#adapter-tests` (ci_job)
- `sdk_compliance_adapter/docker-compose.yml` (container) --[BUILT_BY]--> `sdk-compliance.yml#adapter-tests` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["PostHog/posthog-python (12 workflows)"])
  grp_0_CI___Verification["CI & Verification (5 workflows · 19 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Release___Deploy["Release & Deploy (2 workflows · 9 jobs)"]
  pipeline_root --> grp_1_Release___Deploy
  grp_2_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]
  pipeline_root --> grp_2_Scheduled___Manual
  grp_3_Security___Governance["Security & Governance (2 workflows · 2 jobs)"]
  pipeline_root --> grp_3_Security___Governance
  grp_4_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]
  pipeline_root --> grp_4_Automation___Other
```
