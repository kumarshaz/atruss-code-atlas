---
title: Architecture — home-assistant/home-assistant-js-websocket
description: Arc42 and Pipeline report for home-assistant/home-assistant-js-websocket
---

# Repository Architecture Analysis: home-assistant/home-assistant-js-websocket

## Metadata
- **SHA**: `ddc91ec9b8ba02e802b4a7fb0d2cb46ee8933db2`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 2.87
- **avg_cyclomatic_complexity**: 2.51
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 50.45
- **file_complexities**: 24 entry(ies)
- **files_analyzed**: 24
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: TypeScript
- **import_edges**: 100 entry(ies)
- **loc**: 3705
- **max_cognitive_complexity**: 59
- **max_cyclomatic_complexity**: 23
- **sloc**: 2971
- **test_file_count**: 8

# Architecture: home-assistant/home-assistant-js-websocket

## Context
- **Repository**: `home-assistant/home-assistant-js-websocket`
- **SHA**: `ddc91ec9b8ba02e802b4a7fb0d2cb46ee8933db2`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: TypeScript

## Building Block View

```mermaid
graph TD;
    home_assistant_js_websocket["home-assistant-js-websocket : MODULE"]
```

## Component Details
- **home-assistant-js-websocket** (`package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (57.80/100)
- **Technical Debt Score**: 42.20
- **Estimated Remediation Effort**: 44.64h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 63.00 | 0.20 | avg_cc=2.51, max_cc=23, duplication=50.45%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=9, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 47.00 | 0.15 | avg_cognitive=2.87, max_cognitive=59, fitness_violations=3, oversized_files=2 |
| Pipeline Health | `F` | 14.00 | 0.15 | workflows=4, operational_antipatterns=13, parallel_branches=False |
| Security | `D` | 64.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=3 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (50.45) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (59.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (23.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 9 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@types/assert` `1.4.7` (npm, `package.json`)
- `@types/mocha` `10.0.9` (npm, `package.json`)
- `assert` `2.0.0` (npm, `package.json`)
- `husky` `9.0.0` (npm, `package.json`)
- `lint-staged` `17.0.7` (npm, `package.json`)
- `mocha` `12.0.0` (npm, `package.json`)
- `prettier` `3.0.0` (npm, `package.json`)
- `rollup` `4.3.0` (npm, `package.json`)
- `typescript` `7.0.0` (npm, `package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_22efe112_66e2_429d_b701_92ab3e89a715["22efe112-66e2-429d-b701-92ab3e89a715"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_ci_yml_build["ci.yml#build"]
        job_npmpublish_yml_build["npmpublish.yml#build"]
        job_npmpublish_yml_publish_npm["npmpublish.yml#publish-npm"]
        job_publish_pages_yml_build["publish-pages.yml#build"]
        job_publish_pages_yml_deploy["publish-pages.yml#deploy"]
        job_release_drafter_yaml_update_release_draft["release-drafter.yaml#update_release_draft"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_github_pages["github-pages"]
    end
    job_publish_pages_yml_build -->|DEPLOYS_TO| env_github_pages
    job_publish_pages_yml_deploy -->|DEPLOYS_TO| env_github_pages
    mod_22efe112_66e2_429d_b701_92ab3e89a715 -->|BUILT_BY| job_ci_yml_build
    mod_22efe112_66e2_429d_b701_92ab3e89a715 -->|BUILT_BY| job_npmpublish_yml_build
    mod_22efe112_66e2_429d_b701_92ab3e89a715 -->|BUILT_BY| job_publish_pages_yml_build
    mod_22efe112_66e2_429d_b701_92ab3e89a715 -->|DEPLOYED_BY| job_npmpublish_yml_publish_npm
    mod_22efe112_66e2_429d_b701_92ab3e89a715 -->|DEPLOYED_BY| job_publish_pages_yml_deploy
    mod_22efe112_66e2_429d_b701_92ab3e89a715 -->|DEPLOYED_BY| job_release_drafter_yaml_update_release_draft
```

- `publish-pages.yml#build` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `publish-pages.yml#deploy` (ci_job) --[DEPLOYS_TO]--> `github-pages` (environment)
- `22efe112-66e2-429d-b701-92ab3e89a715` (code_module) --[BUILT_BY]--> `ci.yml#build` (ci_job)
- `22efe112-66e2-429d-b701-92ab3e89a715` (code_module) --[BUILT_BY]--> `npmpublish.yml#build` (ci_job)
- `22efe112-66e2-429d-b701-92ab3e89a715` (code_module) --[BUILT_BY]--> `publish-pages.yml#build` (ci_job)
- `22efe112-66e2-429d-b701-92ab3e89a715` (code_module) --[DEPLOYED_BY]--> `npmpublish.yml#publish-npm` (ci_job)
- `22efe112-66e2-429d-b701-92ab3e89a715` (code_module) --[DEPLOYED_BY]--> `publish-pages.yml#deploy` (ci_job)
- `22efe112-66e2-429d-b701-92ab3e89a715` (code_module) --[DEPLOYED_BY]--> `release-drafter.yaml#update_release_draft` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["home-assistant/home-assistant-js-websocket (4 workflows)"])
  grp_0_Release___Deploy["Release & Deploy (3 workflows · 5 jobs)"]
  pipeline_root --> grp_0_Release___Deploy
  wf_1_Node_js_Package["Node.js Package (2 jobs)"]
  grp_0_Release___Deploy --> wf_1_Node_js_Package
  wf_2_Deploy_to_GitHub_Pages["Deploy to GitHub Pages (2 jobs)"]
  grp_0_Release___Deploy --> wf_2_Deploy_to_GitHub_Pages
  wf_3_Release_Drafter["Release Drafter (1 jobs)"]
  grp_0_Release___Deploy --> wf_3_Release_Drafter
  grp_1_CI___Verification["CI & Verification (1 workflows · 1 jobs)"]
  pipeline_root --> grp_1_CI___Verification
  wf_0_CI["CI (1 jobs)"]
  grp_1_CI___Verification --> wf_0_CI
```
