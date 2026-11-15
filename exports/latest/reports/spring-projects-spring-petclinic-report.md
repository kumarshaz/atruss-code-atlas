---
title: Architecture — spring-projects/spring-petclinic
description: Arc42 and Pipeline report for spring-projects/spring-petclinic
---

# Repository Architecture Analysis: spring-projects/spring-petclinic

## Metadata
- **SHA**: `500158f732419217507c7656904b8e6aa1bcc0d6`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.62
- **avg_cyclomatic_complexity**: 1.49
- **component_count**: 17
- **dead_code_count**: 10
- **dead_code_symbols**: 10 entry(ies)
- **duplication_pct**: 78.46
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 50
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: Spring Boot
- **import_edges**: 100 entry(ies)
- **loc**: 4297
- **max_cognitive_complexity**: 17
- **max_cyclomatic_complexity**: 14
- **sloc**: 2542
- **test_file_count**: 21

# Architecture: spring-projects/spring-petclinic

## Context
- **Repository**: `spring-projects/spring-petclinic`
- **SHA**: `500158f732419217507c7656904b8e6aa1bcc0d6`
- **Ecosystem**: Java
- **Framework**: Spring Boot

## Building Block View

```mermaid
graph TD;
    spring_petclinic["spring-petclinic : MODULE"]
    PetClinicApplication["PetClinicApplication : CONFIG"]
    Owner["Owner : DATA_ACCESS_LAYER"]
    OwnerController["OwnerController : API_ROUTE"]
    Pet["Pet : DATA_ACCESS_LAYER"]
    PetController["PetController : API_ROUTE"]
    PetType["PetType : DATA_ACCESS_LAYER"]
    Visit["Visit : DATA_ACCESS_LAYER"]
    VisitController["VisitController : API_ROUTE"]
    CacheConfiguration["CacheConfiguration : CONFIG"]
    CrashController["CrashController : API_ROUTE"]
    WebConfiguration["WebConfiguration : CONFIG"]
    WelcomeController["WelcomeController : API_ROUTE"]
    Specialty["Specialty : DATA_ACCESS_LAYER"]
    Vet["Vet : DATA_ACCESS_LAYER"]
    VetController["VetController : API_ROUTE"]
    MysqlTestApplication["MysqlTestApplication : CONFIG"]
    repo_root(["spring-projects/spring-petclinic"])
    repo_root --> CacheConfiguration
    repo_root --> CrashController
    repo_root --> WebConfiguration
    repo_root --> WelcomeController
    repo_root --> spring_petclinic
    MysqlTestApplication --> PetClinicApplication
    Owner --> Pet
    Owner --> Visit
    OwnerController --> Owner
    Pet --> PetType
    Pet --> Visit
    PetController --> Owner
    PetController --> Pet
    PetController --> PetType
    Specialty --> Vet
    Vet --> Specialty
    VetController --> Vet
    VisitController --> Owner
    VisitController --> Pet
    VisitController --> Visit
    linkStyle 14 stroke:#ba1a1a,stroke-width:2px,stroke-dasharray: 5 5
```

## Component Details
- **spring-petclinic** (`pom.xml`): MODULE
- **PetClinicApplication** (`src/main/java/org/springframework/samples/petclinic/PetClinicApplication.java`): CONFIG
- **Owner** (`src/main/java/org/springframework/samples/petclinic/owner/Owner.java`): DATA_ACCESS_LAYER (deps: Pet, Visit)
- **OwnerController** (`src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`): API_ROUTE (deps: Owner)
- **Pet** (`src/main/java/org/springframework/samples/petclinic/owner/Pet.java`): DATA_ACCESS_LAYER (deps: PetType, Visit)
- **PetController** (`src/main/java/org/springframework/samples/petclinic/owner/PetController.java`): API_ROUTE (deps: Owner, Pet, PetType)
- **PetType** (`src/main/java/org/springframework/samples/petclinic/owner/PetType.java`): DATA_ACCESS_LAYER
- **Visit** (`src/main/java/org/springframework/samples/petclinic/owner/Visit.java`): DATA_ACCESS_LAYER
- **VisitController** (`src/main/java/org/springframework/samples/petclinic/owner/VisitController.java`): API_ROUTE (deps: Owner, Pet, Visit)
- **CacheConfiguration** (`src/main/java/org/springframework/samples/petclinic/system/CacheConfiguration.java`): CONFIG
- **CrashController** (`src/main/java/org/springframework/samples/petclinic/system/CrashController.java`): API_ROUTE
- **WebConfiguration** (`src/main/java/org/springframework/samples/petclinic/system/WebConfiguration.java`): CONFIG
- **WelcomeController** (`src/main/java/org/springframework/samples/petclinic/system/WelcomeController.java`): API_ROUTE
- **Specialty** (`src/main/java/org/springframework/samples/petclinic/vet/Specialty.java`): DATA_ACCESS_LAYER (deps: Vet)
- **Vet** (`src/main/java/org/springframework/samples/petclinic/vet/Vet.java`): DATA_ACCESS_LAYER (deps: Specialty)
- **VetController** (`src/main/java/org/springframework/samples/petclinic/vet/VetController.java`): API_ROUTE (deps: Vet)
- **MysqlTestApplication** (`src/test/java/org/springframework/samples/petclinic/MysqlTestApplication.java`): CONFIG (deps: PetClinicApplication)

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (65.20/100)
- **Technical Debt Score**: 34.80
- **Estimated Remediation Effort**: 41.89h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 55.00 | 0.20 | avg_cc=1.49, max_cc=14, duplication=78.46%, dead_code=10 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=50, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `B` | 82.00 | 0.15 | avg_cognitive=0.62, max_cognitive=17, fitness_violations=2, oversized_files=0 |
| Pipeline Health | `C` | 71.00 | 0.15 | workflows=3, operational_antipatterns=4, parallel_branches=False |
| Security | `F` | 40.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=5 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[HIGH] `ATRUSS-ARCH-004` (CIRCULAR_DEPENDENCY)**: Circular dependency detected between architectural components. (Specialty -> Vet -> Specialty)
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (78.46) exceeds policy threshold (15.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 50 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `com.github.ben-manes.caffeine:caffeine` `*` (Maven, `build.gradle`)
- `com.github.ben-manes.caffeine:caffeine` `*` (Maven, `pom.xml`)
- `com.h2database:h2` `*` (Maven, `build.gradle`)
- `com.h2database:h2` `*` (Maven, `pom.xml`)
- `com.mysql:mysql-connector-j` `*` (Maven, `build.gradle`)
- `com.mysql:mysql-connector-j` `*` (Maven, `pom.xml`)
- `jakarta.xml.bind:jakarta.xml.bind-api` `*` (Maven, `build.gradle`)
- `jakarta.xml.bind:jakarta.xml.bind-api` `*` (Maven, `pom.xml`)
- `javax.cache:cache-api` `*` (Maven, `build.gradle`)
- `javax.cache:cache-api` `*` (Maven, `pom.xml`)
- `org.postgresql:postgresql` `*` (Maven, `build.gradle`)
- `org.postgresql:postgresql` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-devtools` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-docker-compose` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-docker-compose` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-actuator` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-actuator` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-actuator-test` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-cache` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-cache` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-cache-test` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-data-jpa` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-data-jpa` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-data-jpa-test` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-data-jpa-test` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-restclient` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-restclient-test` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-restclient-test` `*` (Maven, `pom.xml`)
- `org.springframework.boot:spring-boot-starter-thymeleaf` `*` (Maven, `build.gradle`)
- `org.springframework.boot:spring-boot-starter-thymeleaf` `*` (Maven, `pom.xml`)
- ... (+20 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod__devcontainer[".devcontainer"]
        mod_48c3516b_754a_4033_93da_9d0145f0c9d2["48c3516b-754a-4033-93da-9d0145f0c9d2"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art__devcontainer_Dockerfile[".devcontainer/Dockerfile"]
        art_docker_compose_yml["docker-compose.yml"]
        art_k8s_db_yml["k8s/db.yml"]
        art_k8s_petclinic_yml["k8s/petclinic.yml"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_deploy_and_test_cluster_yml_deploy_and_test_cluster["deploy-and-test-cluster.yml#deploy-and-test-cluster"]
    end
    subgraph runtime_envs["Runtime Environments"]
        env_kubernetes["kubernetes"]
    end
    job_deploy_and_test_cluster_yml_deploy_and_test_cluster -->|DEPLOYS_TO| env_kubernetes
    mod__devcontainer -->|PACKAGED_BY| art__devcontainer_Dockerfile
    mod_48c3516b_754a_4033_93da_9d0145f0c9d2 -->|PACKAGED_BY| art_docker_compose_yml
    art_k8s_db_yml -->|DEPLOYED_BY| job_deploy_and_test_cluster_yml_deploy_and_test_cluster
    art_k8s_petclinic_yml -->|DEPLOYED_BY| job_deploy_and_test_cluster_yml_deploy_and_test_cluster
```

- `deploy-and-test-cluster.yml#deploy-and-test-cluster` (ci_job) --[DEPLOYS_TO]--> `kubernetes` (environment)
- `.devcontainer` (code_module) --[PACKAGED_BY]--> `.devcontainer/Dockerfile` (container)
- `48c3516b-754a-4033-93da-9d0145f0c9d2` (code_module) --[PACKAGED_BY]--> `docker-compose.yml` (container)
- `k8s/db.yml` (iac) --[DEPLOYED_BY]--> `deploy-and-test-cluster.yml#deploy-and-test-cluster` (ci_job)
- `k8s/petclinic.yml` (iac) --[DEPLOYED_BY]--> `deploy-and-test-cluster.yml#deploy-and-test-cluster` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["spring-projects/spring-petclinic"])
  subgraph Deploy_and_Test_Cluster_0["Deploy and Test Cluster"]
    direction TB
    0_deploy_and_test_cluster["deploy-and-test-cluster"]
  end
  pipeline_root --> 0_deploy_and_test_cluster
  subgraph Java_CI_with_Gradle_1["Java CI with Gradle"]
    direction TB
    1_build["build"]
  end
  pipeline_root --> 1_build
  subgraph Java_CI_with_Maven_2["Java CI with Maven"]
    direction TB
    2_build["build"]
  end
  pipeline_root --> 2_build
```
