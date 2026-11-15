---
title: Architecture — TryGhost/docker-library-ghost
description: Arc42 and Pipeline report for TryGhost/docker-library-ghost
---

# Repository Architecture Analysis: TryGhost/docker-library-ghost

## Metadata
- **SHA**: `a235302a801ceac861ca6944ebce03995f27d0dd`
- **Primary Ecosystem**: Container / Helm / IaC

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 4
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 4
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Container
- **import_edges**: 0 entry(ies)
- **loc**: 391
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 313

# Architecture: TryGhost/docker-library-ghost

## Context
- **Repository**: `TryGhost/docker-library-ghost`
- **SHA**: `a235302a801ceac861ca6944ebce03995f27d0dd`
- **Ecosystem**: Container / Helm / IaC
- **Framework**: Container

## Building Block View

```mermaid
graph TD;
    action["action : module"]
    ci["ci : module"]
    update["update : module"]
    verify_templating["verify-templating : module"]
```

## Component Details
- **action** (`.github/actions/bashbrew/action.yml`): module
- **ci** (`.github/workflows/ci.yml`): module
- **update** (`.github/workflows/update.yml`): module
- **verify-templating** (`.github/workflows/verify-templating.yml`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `A` (92.20/100)
- **Technical Debt Score**: 7.80
- **Estimated Remediation Effort**: 3.95h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 90.00 | 0.15 | dependencies=0 (no manifests parsed) |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `B` | 88.00 | 0.15 | workflows=3, operational_antipatterns=4, parallel_branches=False |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_6_next_alpine3_23["6-next/alpine3.23"]
        mod_6_next_bookworm["6-next/bookworm"]
        mod_6_alpine3_23["6/alpine3.23"]
        mod_6_bookworm["6/bookworm"]
        mod_bd90a236_f18b_43f4_ae87_dab3bad56000["bd90a236-f18b-43f4-ae87-dab3bad56000"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_6_next_alpine3_23_Dockerfile["6-next/alpine3.23/Dockerfile"]
        art_6_next_bookworm_Dockerfile["6-next/bookworm/Dockerfile"]
        art_6_alpine3_23_Dockerfile["6/alpine3.23/Dockerfile"]
        art_6_bookworm_Dockerfile["6/bookworm/Dockerfile"]
        art_Dockerfile_template["Dockerfile.template"]
    end
    mod_6_next_alpine3_23 -->|PACKAGED_BY| art_6_next_alpine3_23_Dockerfile
    mod_6_next_alpine3_23 -->|PACKAGED_BY| art_6_alpine3_23_Dockerfile
    mod_6_next_bookworm -->|PACKAGED_BY| art_6_next_bookworm_Dockerfile
    mod_6_next_bookworm -->|PACKAGED_BY| art_6_bookworm_Dockerfile
    mod_6_next_bookworm -->|PACKAGED_BY| art_Dockerfile_template
    mod_6_alpine3_23 -->|PACKAGED_BY| art_6_next_alpine3_23_Dockerfile
    mod_6_alpine3_23 -->|PACKAGED_BY| art_6_alpine3_23_Dockerfile
    mod_6_bookworm -->|PACKAGED_BY| art_6_next_bookworm_Dockerfile
    mod_6_bookworm -->|PACKAGED_BY| art_6_bookworm_Dockerfile
    mod_6_bookworm -->|PACKAGED_BY| art_Dockerfile_template
    mod_bd90a236_f18b_43f4_ae87_dab3bad56000 -->|PACKAGED_BY| art_Dockerfile_template
```

- `6-next/alpine3.23` (code_module) --[PACKAGED_BY]--> `6-next/alpine3.23/Dockerfile` (container)
- `6-next/alpine3.23` (code_module) --[PACKAGED_BY]--> `6/alpine3.23/Dockerfile` (container)
- `6-next/bookworm` (code_module) --[PACKAGED_BY]--> `6-next/bookworm/Dockerfile` (container)
- `6-next/bookworm` (code_module) --[PACKAGED_BY]--> `6/bookworm/Dockerfile` (container)
- `6-next/bookworm` (code_module) --[PACKAGED_BY]--> `Dockerfile.template` (container)
- `6/alpine3.23` (code_module) --[PACKAGED_BY]--> `6-next/alpine3.23/Dockerfile` (container)
- `6/alpine3.23` (code_module) --[PACKAGED_BY]--> `6/alpine3.23/Dockerfile` (container)
- `6/bookworm` (code_module) --[PACKAGED_BY]--> `6-next/bookworm/Dockerfile` (container)
- `6/bookworm` (code_module) --[PACKAGED_BY]--> `6/bookworm/Dockerfile` (container)
- `6/bookworm` (code_module) --[PACKAGED_BY]--> `Dockerfile.template` (container)
- `bd90a236-f18b-43f4-ae87-dab3bad56000` (code_module) --[PACKAGED_BY]--> `Dockerfile.template` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["TryGhost/docker-library-ghost"])
  subgraph GitHub_CI_0["GitHub CI"]
    direction TB
    0_generate_jobs["generate-jobs"]
    0_test["test"]
    0_generate_jobs --> 0_test
  end
  pipeline_root --> 0_generate_jobs
  subgraph Update_Dockerfiles_1["Update Dockerfiles"]
    direction TB
    1_update["update"]
  end
  pipeline_root --> 1_update
  subgraph Verify_Templating_2["Verify Templating"]
    direction TB
    2_apply_templates["apply-templates"]
  end
  pipeline_root --> 2_apply_templates
```
