---
title: Architecture — hexojs/hexo
description: Arc42 and Pipeline report for hexojs/hexo
---

# Repository Architecture Analysis: hexojs/hexo

## Metadata
- **SHA**: `36e6a73058cef7502291a69171f052b83eae42dd`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **avg_cyclomatic_complexity**: 5.51
- **component_count**: 2
- **files_analyzed**: 274
- **framework**: TypeScript
- **loc**: 33780
- **max_cyclomatic_complexity**: 92
- **sloc**: 26568

# Architecture: hexojs/hexo

## Context
- **Repository**: `hexojs/hexo`
- **SHA**: `36e6a73058cef7502291a69171f052b83eae42dd`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    hexo["hexo : MODULE"]
    GET_test["GET_test : API_ROUTE"]
```

## Component Details
- **hexo** (`package.json`): MODULE
- **GET_test** (`test/scripts/hexo/router.ts`): API_ROUTE


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
