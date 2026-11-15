---
title: Architecture — medusajs/medusa-agent-skills
description: Arc42 and Pipeline report for medusajs/medusa-agent-skills
---

# Repository Architecture Analysis: medusajs/medusa-agent-skills

## Metadata
- **SHA**: `c5a56b4646b2c39d49b1da10c8a5404236b6b4ba`
- **Primary Ecosystem**: Unknown

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 0
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 0
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Unknown
- **import_edges**: 0 entry(ies)
- **loc**: 0
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 0

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (87.70/100)
- **Technical Debt Score**: 12.30
- **Estimated Remediation Effort**: 5.08h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `B` | 88.00 | 0.15 | workflows=2, operational_antipatterns=3, parallel_branches=False |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["medusajs/medusa-agent-skills"])
  subgraph Skills_stats___PostHog_0["Skills stats → PostHog"]
    direction TB
    0_snapshot["snapshot"]
  end
  pipeline_root --> 0_snapshot
  subgraph Sync_Medusa_Docs_Changes_1["Sync Medusa Docs Changes"]
    direction TB
    1_sync["sync"]
  end
  pipeline_root --> 1_sync
```
