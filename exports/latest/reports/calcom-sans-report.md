---
title: Architecture — calcom/sans
description: Arc42 and Pipeline report for calcom/sans
---

# Repository Architecture Analysis: calcom/sans

## Metadata
- **SHA**: `06c9819281db8f1bdae17e3d3ed359b09e56fbfc`
- **Primary Ecosystem**: Python

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 8.66
- **avg_cyclomatic_complexity**: 5.51
- **component_count**: 0
- **dead_code_count**: 3
- **dead_code_symbols**: 3 entry(ies)
- **duplication_pct**: 56.23
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 26
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Unknown
- **import_edges**: 100 entry(ies)
- **loc**: 8463
- **max_cognitive_complexity**: 81
- **max_cyclomatic_complexity**: 55
- **sloc**: 6698

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (55.45/100)
- **Technical Debt Score**: 44.55
- **Estimated Remediation Effort**: 33.63h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 33.96 | 0.20 | avg_cc=5.51, max_cc=55, duplication=56.23%, dead_code=3 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=6, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 26.02 | 0.15 | avg_cognitive=8.66, max_cognitive=81, fitness_violations=3, oversized_files=4 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (56.23) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (81.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (55.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 6 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `brotli` `*` (PyPI, `requirements.txt`)
- `fontTools` `*` (PyPI, `requirements.txt`)
- `fontmake` `*` (PyPI, `requirements.txt`)
- `glyphsLib` `*` (PyPI, `requirements.txt`)
- `tqdm` `*` (PyPI, `requirements.txt`)
- `uharfbuzz` `*` (PyPI, `requirements.txt`)


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
  NoWorkflows[No Workflows Detected]:::atlasMore
```
