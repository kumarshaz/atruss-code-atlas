---
title: Architecture — kumarshaz/atruss-code-atlas
description: Arc42 and Pipeline report for kumarshaz/atruss-code-atlas
---

# Repository Architecture Analysis: kumarshaz/atruss-code-atlas

## Metadata
- **SHA**: `57dd5638aa381e3cc2338e713752117eaad9eebd`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 11.14
- **avg_cyclomatic_complexity**: 6.99
- **component_count**: 44
- **dead_code_count**: 3
- **dead_code_symbols**: 3 entry(ies)
- **duplication_pct**: 77.24
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 104
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 26979
- **max_cognitive_complexity**: 304
- **max_cyclomatic_complexity**: 122
- **sloc**: 23883
- **test_file_count**: 39

# Architecture: kumarshaz/atruss-code-atlas

## Context
- **Repository**: `kumarshaz/atruss-code-atlas`
- **SHA**: `57dd5638aa381e3cc2338e713752117eaad9eebd`
- **Ecosystem**: Python
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    repo_root(["kumarshaz/atruss-code-atlas (44 components)"])
    dir_0_src["src (42)"]
    repo_root --> dir_0_src
    sub_0_0_models["models (22)"]
    dir_0_src --> sub_0_0_models
    sub_0_1_core["core (11)"]
    dir_0_src --> sub_0_1_core
    sub_0_2_cli["cli (9)"]
    dir_0_src --> sub_0_2_cli
    dir_1_tests["tests (1)"]
    repo_root --> dir_1_tests
    dir_2_web["web (1)"]
    repo_root --> dir_2_web
    sub_0_2_cli -.->|"17 deps"| sub_0_1_core
    sub_0_2_cli -.->|"13 deps"| sub_0_0_models
    sub_0_1_core -.->|"7 deps"| sub_0_0_models
```

## Component Details
- **analyze_code** (`src/cli/commands/analyze_code.py`): CLI_COMMAND (deps: ExportManager, JSONExporter, MarkdownExporter, PortableArtifact)
- **analyze_coverage** (`src/cli/commands/analyze_coverage.py`): CLI_COMMAND
- **analyze_pipeline** (`src/cli/commands/analyze_pipeline.py`): CLI_COMMAND (deps: ExportManager, JSONExporter, MarkdownArchiver, MarkdownExporter, PipelineWorkflow, PortableArtifact, TopologyArchiver)
- **benchmark** (`src/cli/commands/benchmark.py`): CLI_COMMAND (deps: AnomalyRecord, BenchmarkManifest, BenchmarkRepoResult, BenchmarkSummary, CorpusEntry, DiscoveryArchiver, DiscoveryManifestItem, ExportManager, MarkdownArchiver, MarkdownExporter, PortableArtifact, TopologyArchiver, analyze_code, analyze_pipeline)
- **check** (`src/cli/commands/check.py`): CLI_COMMAND (deps: ExportManager, PipelineWorkflow, PortableArtifact)
- **diff** (`src/cli/commands/diff.py`): CLI_COMMAND (deps: ExportManager)
- **discover** (`src/cli/commands/discover.py`): CLI_COMMAND (deps: DiscoveryArchiver, DiscoveryManifestItem, ExportManager)
- **mcp** (`src/cli/commands/mcp_server.py`): CLI_COMMAND
- **version** (`src/cli/main.py`): CLI_COMMAND (deps: analyze_code, analyze_coverage, analyze_pipeline, benchmark, check, diff, discover)
- **BaseExporter** (`src/core/exporters/base_exporter.py`): SERVICE
- **CSVExporter** (`src/core/exporters/csv_exporter.py`): SERVICE (deps: BaseExporter)
- **DiscoveryArchiver** (`src/core/exporters/discovery_exporter.py`): SERVICE (deps: DiscoveryManifestItem, ExportManager)
- **JSONExporter** (`src/core/exporters/json_exporter.py`): SERVICE (deps: BaseExporter, PortableArtifact)
- **MarkdownArchiver** (`src/core/exporters/markdown_exporter.py`): SERVICE (deps: ExportManager, PortableArtifact)
- **TopologyArchiver** (`src/core/exporters/pipeline_exporter.py`): SERVICE (deps: ExportManager)
- **SBOMExporter** (`src/core/exporters/sbom_exporter.py`): SERVICE (deps: DependencyRecord, VulnerabilityRecord)
- **YAMLExporter** (`src/core/exporters/yaml_exporter.py`): SERVICE (deps: BaseExporter)
- **ExportManager** (`src/core/utils/export_manager.py`): SERVICE
- **JSONExporter** (`src/core/utils/json_exporter.py`): SERVICE (deps: PortableArtifact)
- **MarkdownExporter** (`src/core/utils/markdown_exporter.py`): SERVICE (deps: MarkdownArchiver, PortableArtifact)
- **AntiPatternFinding** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **FitnessViolation** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **WorkspacePackage** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **CrossWorkflowEdge** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **DependencyRecord** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **VulnerabilityRecord** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **SecretFinding** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **ScorecardDimension** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **RepositoryScorecard** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **CodeToCloudEdge** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **PipelineWorkflow** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **PortableArtifact** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **HarnessFixture** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **DiscoveryManifestItem** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **Node** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **Edge** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **PipelineDAG** (`src/models/artifacts.py`): DATA_ACCESS_LAYER
- **CorpusEntry** (`src/models/benchmark.py`): DATA_ACCESS_LAYER
- **BenchmarkRepoResult** (`src/models/benchmark.py`): DATA_ACCESS_LAYER
- **AnomalyRecord** (`src/models/benchmark.py`): DATA_ACCESS_LAYER
- **BenchmarkManifest** (`src/models/benchmark.py`): DATA_ACCESS_LAYER
- **BenchmarkSummary** (`src/models/benchmark.py`): DATA_ACCESS_LAYER
- **FixtureManager** (`tests/utils/fixture_manager.py`): SERVICE
- **atruss-code-atlas-web** (`web/package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (68.89/100)
- **Technical Debt Score**: 31.11
- **Estimated Remediation Effort**: 47.98h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 28.04 | 0.20 | avg_cc=6.99, max_cc=122, duplication=77.24%, dead_code=3 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=600, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 18.58 | 0.15 | avg_cognitive=11.14, max_cognitive=304, fitness_violations=3, oversized_files=13 |
| Pipeline Health | `A` | 100.00 | 0.15 | workflows=3, operational_antipatterns=0, parallel_branches=True |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (77.24) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (304.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (122.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 600 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `bandit` `1.7.8` (PyPI, `pyproject.toml`)
- `bandit` `1.7.8` (PyPI, `requirements.txt`)
- `httpx` `0.27.0` (PyPI, `pyproject.toml`)
- `httpx` `0.27.0` (PyPI, `requirements.txt`)
- `networkx` `3.2.1` (PyPI, `pyproject.toml`)
- `networkx` `3.2.1` (PyPI, `requirements.txt`)
- `pydantic` `2.7.0` (PyPI, `pyproject.toml`)
- `pydantic` `2.7.0` (PyPI, `requirements.txt`)
- `pytest` `8.1.1` (PyPI, `pyproject.toml`)
- `pytest` `8.1.1` (PyPI, `requirements.txt`)
- `pytest-asyncio` `0.23.6` (PyPI, `pyproject.toml`)
- `pytest-asyncio` `0.23.6` (PyPI, `requirements.txt`)
- `pyyaml` `6.0.1` (PyPI, `pyproject.toml`)
- `pyyaml` `6.0.1` (PyPI, `requirements.txt`)
- `radon` `6.0.1` (PyPI, `pyproject.toml`)
- `radon` `6.0.1` (PyPI, `requirements.txt`)
- `requests` `2.31.0` (PyPI, `pyproject.toml`)
- `requests` `2.31.0` (PyPI, `requirements.txt`)
- `ruff` `0.3.4` (PyPI, `pyproject.toml`)
- `ruff` `0.3.4` (PyPI, `requirements.txt`)
- `tree-sitter` `0.23.0` (PyPI, `pyproject.toml`)
- `tree-sitter` `0.23.0` (PyPI, `requirements.txt`)
- `tree-sitter-c-sharp` `0.23.0` (PyPI, `pyproject.toml`)
- `tree-sitter-c-sharp` `0.23.0` (PyPI, `requirements.txt`)
- `tree-sitter-java` `0.23.0` (PyPI, `pyproject.toml`)
- `tree-sitter-java` `0.23.0` (PyPI, `requirements.txt`)
- `tree-sitter-javascript` `0.23.0` (PyPI, `pyproject.toml`)
- `tree-sitter-javascript` `0.23.0` (PyPI, `requirements.txt`)
- `tree-sitter-python` `0.23.0` (PyPI, `pyproject.toml`)
- `tree-sitter-python` `0.23.0` (PyPI, `requirements.txt`)
- ... (+570 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_web["web"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_deploy_pages_yml_build["deploy-pages.yml#build"]
        job_deploy_pages_yml_deploy["deploy-pages.yml#deploy"]
        job_tests_yml_web_check["tests.yml#web-check"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_github_pages["github-pages"]
    end
    job_deploy_pages_yml_build -->|DEPLOYS_TO| env_github_pages
    job_deploy_pages_yml_deploy -->|DEPLOYS_TO| env_github_pages
    mod_web -->|BUILT_BY| job_deploy_pages_yml_build
    mod_web -->|BUILT_BY| job_tests_yml_web_check
```

- `deploy-pages.yml#build` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `deploy-pages.yml#deploy` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `web` (code_module) --[BUILT_BY]--> `deploy-pages.yml#build` (ci_job)
- `web` (code_module) --[BUILT_BY]--> `tests.yml#web-check` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["kumarshaz/atruss-code-atlas"])
  subgraph Scheduled_Public_GitHub_Benchmark_0["Scheduled Public GitHub Benchmark"]
    direction TB
    0_benchmark["benchmark"]
  end
  pipeline_root --> 0_benchmark
  subgraph Deploy_Material_UI_to_GitHub_Pages_1["Deploy Material UI to GitHub Pages"]
    direction TB
    1_build["build"]
    1_deploy["deploy"]
    1_build --> 1_deploy
  end
  pipeline_root --> 1_build
  subgraph CI_Suite_2["CI Suite"]
    direction TB
    2_lint_and_unit["lint-and-unit"]
    2_web_check["web-check"]
    2_integration_and_e2e["integration-and-e2e"]
    2_lint_and_unit --> 2_integration_and_e2e
    2_agent_workflow_eval["agent-workflow-eval"]
    2_integration_and_e2e --> 2_agent_workflow_eval
  end
  pipeline_root --> 2_lint_and_unit
```
