---
title: Architecture — hamvocke/spring-testing
description: Arc42 and Pipeline report for hamvocke/spring-testing
---

# Repository Architecture Analysis: hamvocke/spring-testing

## Metadata
- **SHA**: `9cff812e1a71e399bc231ce8323107d1283b9505`
- **Primary Ecosystem**: Java

## Quality Metrics
- **avg_cyclomatic_complexity**: 1.78
- **component_count**: 3
- **files_analyzed**: 18
- **framework**: Spring Boot
- **loc**: 812
- **max_cyclomatic_complexity**: 5
- **sloc**: 635

# Architecture: hamvocke/spring-testing

## Context
- **Repository**: `hamvocke/spring-testing`
- **SHA**: `9cff812e1a71e399bc231ce8323107d1283b9505`
- **Ecosystem**: Java
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    ExampleApplication["ExampleApplication : CONFIG"]
    ExampleController["ExampleController : API_ROUTE"]
    Person["Person : DATA_ACCESS_LAYER"]
```

## Component Details
- **ExampleApplication** (`src/main/java/example/ExampleApplication.java`): CONFIG
- **ExampleController** (`src/main/java/example/ExampleController.java`): API_ROUTE
- **Person** (`src/main/java/example/person/Person.java`): DATA_ACCESS_LAYER


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
