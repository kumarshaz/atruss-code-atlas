---
title: Architecture — hamvocke/spring-testing
description: Arc42 and Pipeline report for hamvocke/spring-testing
---

# Repository Architecture Analysis: hamvocke/spring-testing

## Metadata
- **SHA**: `9cff812e1a71e399bc231ce8323107d1283b9505`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.23
- **avg_cyclomatic_complexity**: 1.25
- **component_count**: 3
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 64.11
- **file_complexities**: 18 entry(ies)
- **files_analyzed**: 18
- **fitness_passed**: False
- **fitness_violation_count**: 1
- **framework**: Spring Boot
- **import_edges**: 100 entry(ies)
- **loc**: 812
- **max_cognitive_complexity**: 4
- **max_cyclomatic_complexity**: 6
- **sloc**: 635
- **test_file_count**: 14

# Architecture: hamvocke/spring-testing

## Context
- **Repository**: `hamvocke/spring-testing`
- **SHA**: `9cff812e1a71e399bc231ce8323107d1283b9505`
- **Ecosystem**: Java
- **Framework**: Spring Boot

## Building Block View

```mermaid
graph TD;
    %% title: Building Block View — hamvocke/spring-testing
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
    ExampleApplication["ExampleApplication : CONFIG"]:::atlasJob
    ExampleController["ExampleController : API_ROUTE"]:::atlasJob
    Person["Person : DATA_ACCESS_LAYER"]:::atlasJob
```

## Component Details
- **ExampleApplication** (`src/main/java/example/ExampleApplication.java`): CONFIG
- **ExampleController** (`src/main/java/example/ExampleController.java`): API_ROUTE
- **Person** (`src/main/java/example/person/Person.java`): DATA_ACCESS_LAYER

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (56.30/100)
- **Technical Debt Score**: 43.70
- **Estimated Remediation Effort**: 41.25h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `C` | 75.00 | 0.20 | avg_cc=1.25, max_cc=6, duplication=64.11%, dead_code=0 |
| Dependency Health | `C` | 71.36 | 0.15 | dependencies=11, outdated=0, vulnerable=3, has_lockfile=False |
| Maintainability | `A` | 94.00 | 0.15 | avg_cognitive=0.23, max_cognitive=4, fitness_violations=1, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=16, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (64.11) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 11 | **Vulnerabilities**: 16 | **Secrets**: 0

### Known Vulnerabilities (OSV)
- **[MEDIUM] `GHSA-22wj-vf5f-wrvj`** `com.h2database:h2` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-24rp-q3w6-vc56`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-36p3-wjmg-h94x`** `org.springframework.boot:spring-boot-starter-web` `` (fixed: `none`, REACHABLE_FROM_RUNTIME)
- **[MEDIUM] `GHSA-45hx-wfhj-473x`** `com.h2database:h2` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-562r-vg33-8x8h`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-673j-qm5f-xpv8`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-727h-hrw8-jg8q`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-7rpj-hg47-cx62`** `com.h2database:h2` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-88cc-g835-76rp`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-98qh-xjc8-98pq`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-h376-j262-vhq6`** `com.h2database:h2` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-h86w-m5rm-xr33`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-hq9p-pm7w-8p54`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-j92g-9f8w-j867`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-r38f-c4h4-hqq2`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)
- **[MEDIUM] `GHSA-v7wg-cpwc-24m4`** `org.postgresql:postgresql` `` (fixed: `none`, UNREACHABLE_DORMANT)

### Inventory Sample
- `au.com.dius.pact.consumer:junit5` `4.6.17` (Maven, `build.gradle`)
- `au.com.dius.pact.provider:junit5spring` `4.6.17` (Maven, `build.gradle`)
- `com.h2database:h2` `*` (Maven, `build.gradle`)
- `io.github.bonigarcia:webdrivermanager` `6.3.2` (Maven, `build.gradle`)
- `io.rest-assured:rest-assured` `5.5.6` (Maven, `build.gradle`)
- `org.postgresql:postgresql` `*` (Maven, `build.gradle`)
- `org.seleniumhq.selenium:selenium-java` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-data-jpa` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-test` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-web` `*` (Maven, `build.gradle`)
- `org.wiremock:wiremock-jetty12` `3.13.1` (Maven, `build.gradle`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    %% title: Code-to-Cloud Deployment Traceability
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_4d349bfc_a5d9_4b65_8601_c10538350358["4d349bfc-a5d9-4b65-8601-c10538350358"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_Dockerfile["Dockerfile"]:::atlasWorkflow
    end
    mod_4d349bfc_a5d9_4b65_8601_c10538350358 -->|PACKAGED_BY| art_Dockerfile
```

- `4d349bfc-a5d9-4b65-8601-c10538350358` (code_module) --[PACKAGED_BY]--> `Dockerfile` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  %% title: CI/CD Pipeline Topology — hamvocke/spring-testing
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
  NoWorkflows[No Workflows Detected]:::atlasMore
```
