---
title: Architecture — nextcloud/desktop
description: Arc42 and Pipeline report for nextcloud/desktop
---

# Repository Architecture Analysis: nextcloud/desktop

## Metadata
- **SHA**: `9ca4db9d5850499fe9b953708ed5f5666caa4a94`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 26.21
- **avg_cyclomatic_complexity**: 13.79
- **component_count**: 0
- **dead_code_count**: 1
- **dead_code_symbols**: 1 entry(ies)
- **duplication_pct**: 99.81
- **file_complexities**: 13 entry(ies)
- **files_analyzed**: 65
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 0 entry(ies)
- **loc**: 510218
- **max_cognitive_complexity**: 54
- **max_cyclomatic_complexity**: 26
- **sloc**: 508659
- **test_file_count**: 150

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (57.10/100)
- **Technical Debt Score**: 42.90
- **Estimated Remediation Effort**: 53.44h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 26.50 | 0.20 | avg_cc=13.79, max_cc=26, duplication=99.81%, dead_code=1 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `F` | 12.00 | 0.15 | avg_cognitive=26.21, max_cognitive=54, fitness_violations=3, oversized_files=12 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (99.81) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (54.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (26.0) exceeds policy threshold (20.0).


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
