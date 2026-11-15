---
title: Architecture — langfuse/skills
description: Arc42 and Pipeline report for langfuse/skills
---

# Repository Architecture Analysis: langfuse/skills

## Metadata
- **SHA**: `f0bcb13088b490c04b3f4870bace17f6d57b199c`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 2.33
- **avg_cyclomatic_complexity**: 5.33
- **component_count**: 1
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 1 entry(ies)
- **files_analyzed**: 1
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Unknown
- **import_edges**: 9 entry(ies)
- **loc**: 108
- **max_cognitive_complexity**: 5
- **max_cyclomatic_complexity**: 12
- **sloc**: 98

# Architecture: langfuse/skills

## Context
- **Repository**: `langfuse/skills`
- **SHA**: `f0bcb13088b490c04b3f4870bace17f6d57b199c`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    halo_skill_publishing["halo-skill-publishing : MODULE"]
```

## Component Details
- **halo-skill-publishing** (`halo-skill-publishing/package.json`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (72.04/100)
- **Technical Debt Score**: 27.96
- **Estimated Remediation Effort**: 23.49h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 90.68 | 0.20 | avg_cc=5.33, max_cc=12, duplication=0.00%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=4, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=2.33, max_cognitive=5, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 36.00 | 0.15 | workflows=2, operational_antipatterns=7, parallel_branches=True |
| Security | `F` | 40.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=5 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=False |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 4 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `@langfuse/cli` `1.3.0-beta.3` (npm, `halo-skill-publishing/package-lock.json`)
- `@langfuse/cli` `1.3.0-beta.3` (npm, `halo-skill-publishing/package.json`)
- `yaml` `2.9.0` (npm, `halo-skill-publishing/package-lock.json`)
- `yaml` `2.9.0` (npm, `halo-skill-publishing/package.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_halo_skill_publishing["halo-skill-publishing"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_sync_halo_skills_yml_prepare["sync-halo-skills.yml#prepare"]
        job_sync_halo_skills_yml_publish_eu["sync-halo-skills.yml#publish-eu"]
        job_sync_halo_skills_yml_publish_hipaa["sync-halo-skills.yml#publish-hipaa"]
        job_sync_halo_skills_yml_publish_jp["sync-halo-skills.yml#publish-jp"]
        job_sync_halo_skills_yml_publish_staging["sync-halo-skills.yml#publish-staging"]
        job_sync_halo_skills_yml_publish_us["sync-halo-skills.yml#publish-us"]
        job_zizmor_yml_zizmor["zizmor.yml#zizmor"]
    end
    mod_halo_skill_publishing -->|BUILT_BY| job_sync_halo_skills_yml_prepare
    mod_halo_skill_publishing -->|BUILT_BY| job_zizmor_yml_zizmor
    mod_halo_skill_publishing -->|DEPLOYED_BY| job_sync_halo_skills_yml_publish_eu
    mod_halo_skill_publishing -->|DEPLOYED_BY| job_sync_halo_skills_yml_publish_hipaa
    mod_halo_skill_publishing -->|DEPLOYED_BY| job_sync_halo_skills_yml_publish_jp
    mod_halo_skill_publishing -->|DEPLOYED_BY| job_sync_halo_skills_yml_publish_staging
    mod_halo_skill_publishing -->|DEPLOYED_BY| job_sync_halo_skills_yml_publish_us
```

- `halo-skill-publishing` (code_module) --[BUILT_BY]--> `sync-halo-skills.yml#prepare` (ci_job)
- `halo-skill-publishing` (code_module) --[BUILT_BY]--> `zizmor.yml#zizmor` (ci_job)
- `halo-skill-publishing` (code_module) --[DEPLOYED_BY]--> `sync-halo-skills.yml#publish-eu` (ci_job)
- `halo-skill-publishing` (code_module) --[DEPLOYED_BY]--> `sync-halo-skills.yml#publish-hipaa` (ci_job)
- `halo-skill-publishing` (code_module) --[DEPLOYED_BY]--> `sync-halo-skills.yml#publish-jp` (ci_job)
- `halo-skill-publishing` (code_module) --[DEPLOYED_BY]--> `sync-halo-skills.yml#publish-staging` (ci_job)
- `halo-skill-publishing` (code_module) --[DEPLOYED_BY]--> `sync-halo-skills.yml#publish-us` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["langfuse/skills"])
  subgraph Sync_Halo_skills_0["Sync Halo skills"]
    direction TB
    0_prepare["prepare"]
    0_publish_staging["publish-staging"]
    0_prepare --> 0_publish_staging
    0_publish_eu["publish-eu"]
    0_prepare --> 0_publish_eu
    0_publish_us["publish-us"]
    0_prepare --> 0_publish_us
    0_publish_jp["publish-jp"]
    0_prepare --> 0_publish_jp
    0_publish_hipaa["publish-hipaa"]
    0_prepare --> 0_publish_hipaa
  end
  pipeline_root --> 0_prepare
  subgraph Check_GitHub_Actions_1["Check GitHub Actions"]
    direction TB
    1_zizmor["zizmor"]
  end
  pipeline_root --> 1_zizmor
```
