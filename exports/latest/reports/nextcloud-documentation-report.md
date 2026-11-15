---
title: Architecture — nextcloud/documentation
description: Arc42 and Pipeline report for nextcloud/documentation
---

# Repository Architecture Analysis: nextcloud/documentation

## Metadata
- **SHA**: `962d63ba78cb757f0c50f2c0b97e4b42983768f1`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.22
- **avg_cyclomatic_complexity**: 2.22
- **component_count**: 0
- **dead_code_count**: 2
- **dead_code_symbols**: 2 entry(ies)
- **duplication_pct**: 58.1
- **file_complexities**: 5 entry(ies)
- **files_analyzed**: 5
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: Unknown
- **import_edges**: 20 entry(ies)
- **loc**: 747
- **max_cognitive_complexity**: 4
- **max_cyclomatic_complexity**: 5
- **sloc**: 420
- **test_file_count**: 3

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (51.55/100)
- **Technical Debt Score**: 48.45
- **Estimated Remediation Effort**: 72.73h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `C` | 71.00 | 0.20 | avg_cc=2.22, max_cc=5, duplication=58.10%, dead_code=2 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=39, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 94.00 | 0.15 | avg_cognitive=1.22, max_cognitive=4, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=19, operational_antipatterns=43, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=2, pipeline_security_findings=8 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (58.1) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 39 | **Vulnerabilities**: 0 | **Secrets**: 2

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `developer_manual/client_apis/LoginFlow/index.rst:137` (`"token":"mQUY***REDACTED***",`)
- **[HIGH] `ATRUSS-SEC-005`** at `developer_manual/client_apis/LoginFlow/index.rst:158` (`"appPassword":"yKTV***REDACTED***"`)

### Inventory Sample
- `Babel` `2.18.0` (PyPI, `requirements.txt`)
- `Jinja2` `3.1.6` (PyPI, `requirements.txt`)
- `MarkupSafe` `3.0.4` (PyPI, `requirements.txt`)
- `Pillow` `13.0.0` (PyPI, `requirements.txt`)
- `PyYAML` `6.0.3` (PyPI, `requirements.txt`)
- `Pygments` `2.21.0` (PyPI, `requirements.txt`)
- `Sphinx` `9.2.0` (PyPI, `requirements.txt`)
- `alabaster` `1.0.0` (PyPI, `requirements.txt`)
- `certifi` `2026.10.23` (PyPI, `requirements.txt`)
- `charset-normalizer` `3.5.2` (PyPI, `requirements.txt`)
- `docutils` `0.21.2` (PyPI, `requirements.txt`)
- `idna` `3.20` (PyPI, `requirements.txt`)
- `imagesize` `2.0.1` (PyPI, `requirements.txt`)
- `importlib-metadata` `10.1.0` (PyPI, `requirements.txt`)
- `packaging` `26.3` (PyPI, `requirements.txt`)
- `reportlab` `4.5.1` (PyPI, `requirements.txt`)
- `requests` `2.34.2` (PyPI, `requirements.txt`)
- `rst2pdf` `0.105` (PyPI, `requirements.txt`)
- `smartypants` `2.0.2` (PyPI, `requirements.txt`)
- `snowballstemmer` `3.1.1` (PyPI, `requirements.txt`)
- `sphinx-copybutton` `0.5.2` (PyPI, `requirements.txt`)
- `sphinx-lint` `1.0.2` (PyPI, `requirements.txt`)
- `sphinx-notfound-page` `1.1.0` (PyPI, `requirements.txt`)
- `sphinx-reredirects` `1.1.0` (PyPI, `requirements.txt`)
- `sphinx-rtd-dark-mode` `1.3.0` (PyPI, `requirements.txt`)
- `sphinx-rtd-theme` `3.1.0` (PyPI, `requirements.txt`)
- `sphinx-toolbox` `4.3.1` (PyPI, `requirements.txt`)
- `sphinxcontrib-applehelp` `2.0.0` (PyPI, `requirements.txt`)
- `sphinxcontrib-devhelp` `2.0.0` (PyPI, `requirements.txt`)
- `sphinxcontrib-htmlhelp` `2.1.0` (PyPI, `requirements.txt`)
- ... (+9 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod__devcontainer[".devcontainer"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__devcontainer_Dockerfile[".devcontainer/Dockerfile"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_build_docs_yml_prepare_pdf_image["build-docs.yml#prepare-pdf-image"]
        job_docker_build_yml_build_and_publish["docker-build.yml#build-and-publish"]
    end
    mod__devcontainer -->|BUILT_BY| job_build_docs_yml_prepare_pdf_image
    mod__devcontainer -->|DEPLOYED_BY| job_docker_build_yml_build_and_publish
    mod__devcontainer -->|PACKAGED_BY| art__devcontainer_Dockerfile
    art__devcontainer_Dockerfile -->|BUILT_BY| job_build_docs_yml_prepare_pdf_image
    art__devcontainer_Dockerfile -->|BUILT_BY| job_docker_build_yml_build_and_publish
```

- `.devcontainer` (code_module) --[BUILT_BY]--> `build-docs.yml#prepare-pdf-image` (ci_job)
- `.devcontainer` (code_module) --[DEPLOYED_BY]--> `docker-build.yml#build-and-publish` (ci_job)
- `.devcontainer` (code_module) --[PACKAGED_BY]--> `.devcontainer/Dockerfile` (container)
- `.devcontainer/Dockerfile` (container) --[BUILT_BY]--> `build-docs.yml#prepare-pdf-image` (ci_job)
- `.devcontainer/Dockerfile` (container) --[BUILT_BY]--> `docker-build.yml#build-and-publish` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["nextcloud/documentation (19 workflows)"])
  grp_0_CI___Verification["CI & Verification (9 workflows · 18 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Scheduled___Manual["Scheduled & Manual (4 workflows · 4 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  grp_2_Release___Deploy["Release & Deploy (3 workflows · 7 jobs)"]
  pipeline_root --> grp_2_Release___Deploy
  grp_3_Security___Governance["Security & Governance (3 workflows · 3 jobs)"]
  pipeline_root --> grp_3_Security___Governance
```
