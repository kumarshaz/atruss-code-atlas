---
title: Architecture — apache/activemq
description: Arc42 and Pipeline report for apache/activemq
---

# Repository Architecture Analysis: apache/activemq

## Metadata
- **SHA**: `03a17a7f4c2a3136289141c29e5324fa033529d6`
- **Primary Ecosystem**: Java

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.29
- **avg_cyclomatic_complexity**: 1.69
- **component_count**: 79
- **dead_code_count**: 24
- **dead_code_symbols**: 24 entry(ies)
- **duplication_pct**: 92.96
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 4613
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Java Maven/Gradle
- **import_edges**: 100 entry(ies)
- **loc**: 767705
- **max_cognitive_complexity**: 144
- **max_cyclomatic_complexity**: 68
- **sloc**: 474471
- **test_file_count**: 2692

# Architecture: apache/activemq

## Context
- **Repository**: `apache/activemq`
- **SHA**: `03a17a7f4c2a3136289141c29e5324fa033529d6`
- **Ecosystem**: Java
- **Framework**: Java Maven/Gradle

## Building Block View

```mermaid
graph TD;
  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff
  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6
  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf
    repo_root(["apache/activemq (79 components)"]):::atlasRoot
    dir_0_assembly["assembly (21)"]:::atlasCategory
    repo_root --> dir_0_assembly
    sub_0_0_src["src (20)"]:::atlasWorkflow
    dir_0_assembly --> sub_0_0_src
    sub_0_1__module_root_["(module root) (1)"]:::atlasWorkflow
    dir_0_assembly --> sub_0_1__module_root_
    dir_1_helm["helm (14)"]:::atlasCategory
    repo_root --> dir_1_helm
    sub_1_0_activemq_templates["activemq/templates (10)"]:::atlasWorkflow
    dir_1_helm --> sub_1_0_activemq_templates
    sub_1_1_activemq["activemq (2)"]:::atlasWorkflow
    dir_1_helm --> sub_1_1_activemq
    sub_1_2_activemq_examples["activemq/examples (2)"]:::atlasWorkflow
    dir_1_helm --> sub_1_2_activemq_examples
    dir_2_activemq_tooling["activemq-tooling (7)"]:::atlasCategory
    repo_root --> dir_2_activemq_tooling
    dir_3__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_3__root_
    dir_4_activemq_all["activemq-all (1)"]:::atlasCategory
    repo_root --> dir_4_activemq_all
    dir_other_modules["+35 more modules (35)"]:::atlasMore
    repo_root --> dir_other_modules
```

## Component Details

Showing top 60 representative components out of 79 across 40 module group(s):

- **Module `assembly`** (21 components — MODULE: 20, module: 1)
- **Module `helm`** (14 components — module: 14)
- **Module `activemq-tooling`** (7 components — MODULE: 7)
- **Module `(root)`** (1 components — MODULE: 1)
- **Module `activemq-all`** (1 components — MODULE: 1)
- **Module `activemq-amqp`** (1 components — MODULE: 1)
- **Module `activemq-blueprint`** (1 components — MODULE: 1)
- **Module `activemq-broker`** (1 components — MODULE: 1)
- **Module `activemq-cf`** (1 components — MODULE: 1)
- **Module `activemq-client`** (1 components — MODULE: 1)
- **Module `activemq-console`** (1 components — MODULE: 1)
- **Module `activemq-http`** (1 components — MODULE: 1)

- **Chart** (`helm/activemq/Chart.yaml`): module
- **Listener** (`assembly/src/release/examples/openwire/csharp/ActiveMQExamples/Listener/Listener.csproj`): MODULE
- **Listener** (`assembly/src/release/examples/stomp/csharp/ActiveMQExamples/Listener/Listener.csproj`): MODULE
- **Publisher** (`assembly/src/release/examples/openwire/csharp/ActiveMQExamples/Publisher/Publisher.csproj`): MODULE
- **Publisher** (`assembly/src/release/examples/stomp/csharp/ActiveMQExamples/Publisher/Publisher.csproj`): MODULE
- **activemq-all** (`activemq-all/pom.xml`): MODULE
- **activemq-amqp** (`activemq-amqp/pom.xml`): MODULE
- **activemq-blueprint** (`activemq-blueprint/pom.xml`): MODULE
- **activemq-bom** (`bom/pom.xml`): MODULE
- **activemq-broker** (`activemq-broker/pom.xml`): MODULE
- **activemq-cf** (`activemq-cf/pom.xml`): MODULE
- **activemq-client** (`activemq-client/pom.xml`): MODULE
- **activemq-console** (`activemq-console/pom.xml`): MODULE
- **activemq-custom** (`helm/activemq/examples/activemq-custom.yaml`): module
- **activemq-http** (`activemq-http/pom.xml`): MODULE
- **activemq-jaas** (`activemq-jaas/pom.xml`): MODULE
- **activemq-jaas-oauth2** (`activemq-jaas-oauth2/pom.xml`): MODULE
- **activemq-jakarta-messaging-tck** (`activemq-tooling/activemq-jakarta-messaging-tck/pom.xml`): MODULE
- **activemq-jdbc-store** (`activemq-jdbc-store/pom.xml`): MODULE
- **activemq-jms-pool** (`activemq-jms-pool/pom.xml`): MODULE
- **activemq-joram-jms-tests** (`activemq-tooling/activemq-joram-jms-tests/pom.xml`): MODULE
- **activemq-junit** (`activemq-tooling/activemq-junit/pom.xml`): MODULE
- **activemq-kahadb-store** (`activemq-kahadb-store/pom.xml`): MODULE
- **activemq-karaf** (`activemq-karaf/pom.xml`): MODULE
- **activemq-karaf-itest** (`activemq-karaf-itest/pom.xml`): MODULE
- **activemq-log4j-appender** (`activemq-log4j-appender/pom.xml`): MODULE
- **activemq-maven-plugin** (`activemq-tooling/activemq-maven-plugin/pom.xml`): MODULE
- **activemq-memtest-maven-plugin** (`activemq-tooling/activemq-memtest-maven-plugin/pom.xml`): MODULE
- **activemq-mqtt** (`activemq-mqtt/pom.xml`): MODULE
- **activemq-opentelemetry** (`activemq-opentelemetry/pom.xml`): MODULE
- **activemq-openwire-generator** (`activemq-openwire-generator/pom.xml`): MODULE
- **activemq-openwire-legacy** (`activemq-openwire-legacy/pom.xml`): MODULE
- **activemq-osgi** (`activemq-osgi/pom.xml`): MODULE
- **activemq-parent** (`pom.xml`): MODULE
- **activemq-perf-maven-plugin** (`activemq-tooling/activemq-perf-maven-plugin/pom.xml`): MODULE
- **activemq-pool** (`activemq-pool/pom.xml`): MODULE
- **activemq-protobuf** (`activemq-protobuf/pom.xml`): MODULE
- **activemq-protobuf-test** (`activemq-protobuf-test/pom.xml`): MODULE
- **activemq-ra** (`activemq-ra/pom.xml`): MODULE
- **activemq-rar** (`activemq-rar/pom.xml`): MODULE
- **activemq-run** (`activemq-run/pom.xml`): MODULE
- **activemq-runtime-config** (`activemq-runtime-config/pom.xml`): MODULE
- **activemq-shiro** (`activemq-shiro/pom.xml`): MODULE
- **activemq-spring** (`activemq-spring/pom.xml`): MODULE
- **activemq-stomp** (`activemq-stomp/pom.xml`): MODULE
- **activemq-tooling** (`activemq-tooling/pom.xml`): MODULE
- **activemq-unit-tests** (`activemq-unit-tests/pom.xml`): MODULE
- **activemq-web** (`activemq-web/pom.xml`): MODULE
- **activemq-web-console** (`activemq-web-console/pom.xml`): MODULE
- **activemq-web-demo** (`activemq-web-demo/pom.xml`): MODULE
- **advanced-openwire-example** (`assembly/src/release/examples/openwire/advanced-scenarios/pom.xml`): MODULE
- **amqp-example** (`assembly/src/release/examples/amqp/java/pom.xml`): MODULE
- **apache-activemq** (`assembly/pom.xml`): MODULE
- **configmap** (`helm/activemq/templates/configmap.yaml`): module
- **docker-compose** (`assembly/src/docker/docker-compose.yml`): module
- **ingress** (`helm/activemq/templates/ingress.yaml`): module
- **jms-example-composite-destinations** (`assembly/src/release/examples/openwire/advanced-scenarios/jms-example-composite-destinations/pom.xml`): MODULE
- **jms-example-durable-sub** (`assembly/src/release/examples/openwire/advanced-scenarios/jms-example-durable-sub/pom.xml`): MODULE
- **jms-example-exclusive-consumer** (`assembly/src/release/examples/openwire/advanced-scenarios/jms-example-exclusive-consumer/pom.xml`): MODULE
- **jms-example-message-browser** (`assembly/src/release/examples/openwire/advanced-scenarios/jms-example-message-browser/pom.xml`): MODULE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `D` (61.55/100)
- **Technical Debt Score**: 38.45
- **Estimated Remediation Effort**: 82.70h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.00 | 0.20 | avg_cc=1.69, max_cc=68, duplication=92.96%, dead_code=24 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=639, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=1.29, max_cognitive=144, fitness_violations=3, oversized_files=25 |
| Pipeline Health | `C` | 77.00 | 0.15 | workflows=6, operational_antipatterns=2, parallel_branches=False |
| Security | `C` | 76.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=4 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (92.96) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (144.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (68.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 639 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `${project.groupId}:activemq-all` `*` (Maven, `activemq-web/pom.xml`)
- `${project.groupId}:activemq-all` `*` (Maven, `assembly/pom.xml`)
- `${project.groupId}:activemq-amqp` `*` (Maven, `activemq-all/pom.xml`)
- `${project.groupId}:activemq-amqp` `*` (Maven, `activemq-osgi/pom.xml`)
- `${project.groupId}:activemq-amqp` `*` (Maven, `assembly/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-console/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-http/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-jms-pool/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-kahadb-store/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-mqtt/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-opentelemetry/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-opentelemetry/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-osgi/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-pool/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-pool/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-shiro/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-shiro/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-spring/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-stomp/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-stomp/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-unit-tests/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-web-console/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-web-demo/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `activemq-web/pom.xml`)
- `${project.groupId}:activemq-broker` `*` (Maven, `assembly/pom.xml`)
- `${project.groupId}:activemq-client` `*` (Maven, `activemq-jaas-oauth2/pom.xml`)
- `${project.groupId}:activemq-client` `*` (Maven, `activemq-pool/pom.xml`)
- `${project.groupId}:activemq-client` `*` (Maven, `assembly/pom.xml`)
- `${project.groupId}:activemq-console` `*` (Maven, `activemq-all/pom.xml`)
- `${project.groupId}:activemq-console` `*` (Maven, `activemq-osgi/pom.xml`)
- ... (+609 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_activemq_web["activemq-web"]:::atlasCategory
        mod_assembly_src_docker["assembly/src/docker"]:::atlasCategory
        mod_assembly_src_release_examples_amqp_java["assembly/src/release/examples/amqp/java"]:::atlasCategory
        mod_assembly_src_release_examples_mqtt_java["assembly/src/release/examples/mqtt/java"]:::atlasCategory
        mod_assembly_src_release_examples_openwire_java["assembly/src/release/examples/openwire/java"]:::atlasCategory
        mod_assembly_src_release_examples_stomp_java["assembly/src/release/examples/stomp/java"]:::atlasCategory
        mod_helm_activemq["helm/activemq"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_assembly_src_docker_Dockerfile["assembly/src/docker/Dockerfile"]:::atlasWorkflow
        art_assembly_src_docker_docker_compose_yml["assembly/src/docker/docker-compose.yml"]:::atlasWorkflow
        art_helm_activemq_Chart_yaml["helm/activemq/Chart.yaml"]:::atlasWorkflow
        art_helm_activemq_examples_activemq_custom_yaml["helm/activemq/examples/activemq-custom.yaml"]:::atlasWorkflow
        art_helm_activemq_examples_production_yaml["helm/activemq/examples/production.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_configmap_yaml["helm/activemq/templates/configmap.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_ingress_yaml["helm/activemq/templates/ingress.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_poddisruptionbudget_yaml["helm/activemq/templates/poddisruptionbudget.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_secret_yaml["helm/activemq/templates/secret.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_service_web_yaml["helm/activemq/templates/service-web.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_service_yaml["helm/activemq/templates/service.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_serviceaccount_yaml["helm/activemq/templates/serviceaccount.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_servicemonitor_yaml["helm/activemq/templates/servicemonitor.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_statefulset_yaml["helm/activemq/templates/statefulset.yaml"]:::atlasWorkflow
        art_helm_activemq_templates_tests_test_connection_yaml["helm/activemq/templates/tests/test-connection.yaml"]:::atlasWorkflow
        art_helm_activemq_values_yaml["helm/activemq/values.yaml"]:::atlasWorkflow
    end
    mod_activemq_web -->|PACKAGED_BY| art_helm_activemq_examples_production_yaml
    mod_assembly_src_docker -->|PACKAGED_BY| art_assembly_src_docker_Dockerfile
    mod_assembly_src_docker -->|PACKAGED_BY| art_assembly_src_docker_docker_compose_yml
    mod_assembly_src_docker -->|PACKAGED_BY| art_helm_activemq_values_yaml
    mod_assembly_src_release_examples_amqp_java -->|PACKAGED_BY| art_assembly_src_docker_Dockerfile
    mod_assembly_src_release_examples_amqp_java -->|PACKAGED_BY| art_helm_activemq_Chart_yaml
    mod_assembly_src_release_examples_mqtt_java -->|PACKAGED_BY| art_assembly_src_docker_Dockerfile
    mod_assembly_src_release_examples_mqtt_java -->|PACKAGED_BY| art_helm_activemq_Chart_yaml
    mod_assembly_src_release_examples_openwire_java -->|PACKAGED_BY| art_assembly_src_docker_Dockerfile
    mod_assembly_src_release_examples_openwire_java -->|PACKAGED_BY| art_helm_activemq_Chart_yaml
    mod_assembly_src_release_examples_stomp_java -->|PACKAGED_BY| art_assembly_src_docker_Dockerfile
    mod_assembly_src_release_examples_stomp_java -->|PACKAGED_BY| art_helm_activemq_Chart_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_assembly_src_docker_Dockerfile
    mod_helm_activemq -->|PACKAGED_BY| art_assembly_src_docker_docker_compose_yml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_Chart_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_examples_activemq_custom_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_examples_production_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_configmap_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_ingress_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_poddisruptionbudget_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_secret_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_service_web_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_service_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_serviceaccount_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_servicemonitor_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_statefulset_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_templates_tests_test_connection_yaml
    mod_helm_activemq -->|PACKAGED_BY| art_helm_activemq_values_yaml
    art_assembly_src_docker_Dockerfile -->|PACKAGED_BY| art_helm_activemq_values_yaml
    art_assembly_src_docker_docker_compose_yml -->|PACKAGED_BY| art_helm_activemq_values_yaml
```

- `activemq-web` (code_module) --[PACKAGED_BY]--> `helm/activemq/examples/production.yaml` (iac)
- `assembly/src/docker` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/Dockerfile` (container)
- `assembly/src/docker` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/docker-compose.yml` (container)
- `assembly/src/docker` (code_module) --[PACKAGED_BY]--> `helm/activemq/values.yaml` (iac)
- `assembly/src/release/examples/amqp/java` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/Dockerfile` (container)
- `assembly/src/release/examples/amqp/java` (code_module) --[PACKAGED_BY]--> `helm/activemq/Chart.yaml` (iac)
- `assembly/src/release/examples/mqtt/java` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/Dockerfile` (container)
- `assembly/src/release/examples/mqtt/java` (code_module) --[PACKAGED_BY]--> `helm/activemq/Chart.yaml` (iac)
- `assembly/src/release/examples/openwire/java` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/Dockerfile` (container)
- `assembly/src/release/examples/openwire/java` (code_module) --[PACKAGED_BY]--> `helm/activemq/Chart.yaml` (iac)
- `assembly/src/release/examples/stomp/java` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/Dockerfile` (container)
- `assembly/src/release/examples/stomp/java` (code_module) --[PACKAGED_BY]--> `helm/activemq/Chart.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/Dockerfile` (container)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `assembly/src/docker/docker-compose.yml` (container)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/Chart.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/examples/activemq-custom.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/examples/production.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/configmap.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/ingress.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/poddisruptionbudget.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/secret.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/service-web.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/service.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/serviceaccount.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/servicemonitor.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/statefulset.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/templates/tests/test-connection.yaml` (iac)
- `helm/activemq` (code_module) --[PACKAGED_BY]--> `helm/activemq/values.yaml` (iac)
- `assembly/src/docker/Dockerfile` (container) --[PACKAGED_BY]--> `helm/activemq/values.yaml` (iac)
- `assembly/src/docker/docker-compose.yml` (container) --[PACKAGED_BY]--> `helm/activemq/values.yaml` (iac)


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
  pipeline_root(["apache/activemq (6 workflows)"]):::atlasRoot
  subgraph sg_grp_0_Scheduled___Manual["Scheduled & Manual (3 workflows · 6 jobs)"]
    direction TB
    subgraph sg_wf_0_CI_Manual["CI Manual (2 jobs)"]
      direction TB
      wf_0_CI_Manual(["Trigger: CI Manual"]):::atlasWorkflow
      job_0_build["build"]:::atlasJob
      job_0_test["test"]:::atlasJob
      wf_0_CI_Manual --> job_0_build
      job_0_build --> job_0_test
    end
    pipeline_root --> wf_0_CI_Manual
    subgraph sg_wf_1_CI_Periodic_Full["CI Periodic Full (2 jobs)"]
      direction TB
      wf_1_CI_Periodic_Full(["Trigger: CI Periodic Full"]):::atlasWorkflow
      job_1_build["build"]:::atlasJob
      job_1_test["test"]:::atlasJob
      wf_1_CI_Periodic_Full --> job_1_build
      job_1_build --> job_1_test
    end
    pipeline_root --> wf_1_CI_Periodic_Full
    subgraph sg_wf_2_CI_Periodic_Quick["CI Periodic Quick (2 jobs)"]
      direction TB
      wf_2_CI_Periodic_Quick(["Trigger: CI Periodic Quick"]):::atlasWorkflow
      job_2_build["build"]:::atlasJob
      job_2_test["test"]:::atlasJob
      wf_2_CI_Periodic_Quick --> job_2_build
      job_2_build --> job_2_test
    end
    pipeline_root --> wf_2_CI_Periodic_Quick
  end
  subgraph sg_grp_1_CI___Verification["CI & Verification (1 workflows · 2 jobs)"]
    direction TB
    subgraph sg_wf_3_CI_Quick["CI Quick (2 jobs)"]
      direction TB
      wf_3_CI_Quick(["Trigger: CI Quick"]):::atlasWorkflow
      job_3_build["build"]:::atlasJob
      job_3_test["test"]:::atlasJob
      wf_3_CI_Quick --> job_3_build
      job_3_build --> job_3_test
    end
    pipeline_root --> wf_3_CI_Quick
  end
  subgraph sg_grp_2_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_4_Deploy["Deploy (1 jobs)"]
      direction TB
      wf_4_Deploy(["Trigger: Deploy"]):::atlasWorkflow
      job_4_deploy["deploy"]:::atlasJob
      wf_4_Deploy --> job_4_deploy
    end
    pipeline_root --> wf_4_Deploy
  end
  subgraph sg_grp_3_Security___Governance["Security & Governance (1 workflows · 1 jobs)"]
    direction TB
    subgraph sg_wf_5_Mark_stale_issues_and_close_stale_PRs["Mark stale issues and close stale PRs (1 jobs)"]
      direction TB
      wf_5_Mark_stale_issues_and_close_stale_PRs(["Trigger: Mark stale issues and close stale PRs"]):::atlasWorkflow
      job_5_stale["stale"]:::atlasJob
      wf_5_Mark_stale_issues_and_close_stale_PRs --> job_5_stale
    end
    pipeline_root --> wf_5_Mark_stale_issues_and_close_stale_PRs
  end
```
