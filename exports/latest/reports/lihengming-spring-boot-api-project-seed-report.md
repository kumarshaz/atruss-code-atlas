---
title: Architecture — lihengming/spring-boot-api-project-seed
description: Arc42 and Pipeline report for lihengming/spring-boot-api-project-seed
---

# Repository Architecture Analysis: lihengming/spring-boot-api-project-seed

## Metadata
- **SHA**: `c305af6a6bb2b698b02d731ac27218bff51c5c1c`
- **Primary Ecosystem**: Java

## Quality Metrics
- **avg_cyclomatic_complexity**: 3.08
- **component_count**: 4
- **files_analyzed**: 13
- **framework**: Spring Boot
- **loc**: 761
- **max_cyclomatic_complexity**: 17
- **sloc**: 564

# Architecture: lihengming/spring-boot-api-project-seed

## Context
- **Repository**: `lihengming/spring-boot-api-project-seed`
- **SHA**: `c305af6a6bb2b698b02d731ac27218bff51c5c1c`
- **Ecosystem**: Java
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    spring_boot_api_project_seed["spring-boot-api-project-seed : MODULE"]
    Application["Application : CONFIG"]
    MybatisConfigurer["MybatisConfigurer : CONFIG"]
    WebMvcConfigurer["WebMvcConfigurer : CONFIG"]
```

## Component Details
- **spring-boot-api-project-seed** (`pom.xml`): MODULE
- **Application** (`src/main/java/com/company/project/Application.java`): CONFIG
- **MybatisConfigurer** (`src/main/java/com/company/project/configurer/MybatisConfigurer.java`): CONFIG
- **WebMvcConfigurer** (`src/main/java/com/company/project/configurer/WebMvcConfigurer.java`): CONFIG


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
