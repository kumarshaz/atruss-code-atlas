---
title: Architecture — grafana/grafana-ansible-collection
description: Arc42 and Pipeline report for grafana/grafana-ansible-collection
---

# Repository Architecture Analysis: grafana/grafana-ansible-collection

## Metadata
- **SHA**: `1f32a13821386f28f9cebafd5e1b6c8f786df33d`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 3.87
- **avg_cyclomatic_complexity**: 3.33
- **component_count**: 0
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 93.42
- **file_complexities**: 16 entry(ies)
- **files_analyzed**: 16
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: Unknown
- **import_edges**: 50 entry(ies)
- **loc**: 2364
- **max_cognitive_complexity**: 41
- **max_cyclomatic_complexity**: 16
- **sloc**: 1943
- **test_file_count**: 20

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (68.49/100)
- **Technical Debt Score**: 31.51
- **Estimated Remediation Effort**: 44.56h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `C` | 72.18 | 0.20 | avg_cc=3.33, max_cc=16, duplication=93.42%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=10, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `D` | 63.00 | 0.15 | avg_cognitive=3.87, max_cognitive=41, fitness_violations=2, oversized_files=0 |
| Pipeline Health | `F` | 9.00 | 0.15 | workflows=10, operational_antipatterns=21, parallel_branches=True |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (93.42) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (41.0) exceeds policy threshold (25.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 10 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `ansible-lint` `6.13.1` (PyPI, `requirements.txt`)
- `pylint` `2.16.2` (PyPI, `requirements.txt`)
- `requests` `*` (PyPI, `tests/integration/requirements.txt`)
- `yamllint` `1.35.1` (PyPI, `requirements.txt`)
- `editorconfig-checker` `5.0.1` (npm, `package.json`)
- `markdownlint-cli2` `0.6.0` (npm, `package.json`)
- `textlint` `12.5.1` (npm, `package.json`)
- `textlint-rule-common-misspellings` `1.0.1` (npm, `package.json`)
- `textlint-rule-no-todo` `2.0.1` (npm, `package.json`)
- `textlint-rule-terminology` `3.0.4` (npm, `package.json`)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["grafana/grafana-ansible-collection (10 workflows)"])
  grp_0_CI___Verification["CI & Verification (6 workflows · 6 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Scheduled___Manual["Scheduled & Manual (3 workflows · 5 jobs)"]
  pipeline_root --> grp_1_Scheduled___Manual
  grp_2_Release___Deploy["Release & Deploy (1 workflows · 4 jobs)"]
  pipeline_root --> grp_2_Release___Deploy
```
