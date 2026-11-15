---
title: Architecture — argoproj/argoproj
description: Arc42 and Pipeline report for argoproj/argoproj
---

# Repository Architecture Analysis: argoproj/argoproj

## Metadata
- **SHA**: `2d1d41a6984fc34626052280b0fbc83eeb0a206f`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 24.0
- **avg_cyclomatic_complexity**: 15.0
- **component_count**: 0
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 54.88
- **file_complexities**: 1 entry(ies)
- **files_analyzed**: 1
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: Unknown
- **import_edges**: 4 entry(ies)
- **loc**: 86
- **max_cognitive_complexity**: 24
- **max_cyclomatic_complexity**: 15
- **sloc**: 70

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (63.95/100)
- **Technical Debt Score**: 36.05
- **Estimated Remediation Effort**: 21.49h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 45.00 | 0.20 | avg_cc=15.00, max_cc=15, duplication=54.88%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `D` | 63.00 | 0.15 | avg_cognitive=24.00, max_cognitive=24, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (54.88) exceeds policy threshold (15.0).


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
