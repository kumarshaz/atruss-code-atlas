---
title: Architecture — nextcloud/viewer
description: Arc42 and Pipeline report for nextcloud/viewer
---

# Repository Architecture Analysis: nextcloud/viewer

## Metadata
- **SHA**: `441c3edf740c277603d3403143ecc1febe11ffc0`
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

- **Overall Grade**: `B` (82.35/100)
- **Technical Debt Score**: 17.65
- **Estimated Remediation Effort**: 9.91h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `C` | 79.00 | 0.15 | workflows=4, operational_antipatterns=6, parallel_branches=False |
| Security | `B` | 80.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=1 |
| Test Coverage | `F` | 40.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=False |


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["nextcloud/viewer (4 workflows)"])
  grp_0_Scheduled___Manual["Scheduled & Manual (2 workflows · 2 jobs)"]
  pipeline_root --> grp_0_Scheduled___Manual
  wf_2_Update_workflows["Update workflows (1 jobs)"]
  grp_0_Scheduled___Manual --> wf_2_Update_workflows
  wf_3_Update_nextcloud_ocp["Update nextcloud/ocp (1 jobs)"]
  grp_0_Scheduled___Manual --> wf_3_Update_nextcloud_ocp
  grp_1_Automation___Other["Automation & Other (1 workflows · 2 jobs)"]
  pipeline_root --> grp_1_Automation___Other
  wf_0_Compile_Command["Compile Command (2 jobs)"]
  grp_1_Automation___Other --> wf_0_Compile_Command
  grp_2_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
  pipeline_root --> grp_2_Security___Governance
  wf_1_Npm_audit_fix_and_compile["Npm audit fix and compile (1 jobs)"]
  grp_2_Security___Governance --> wf_1_Npm_audit_fix_and_compile
```
