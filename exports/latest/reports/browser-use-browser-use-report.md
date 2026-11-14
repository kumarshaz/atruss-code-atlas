---
title: Architecture — browser-use/browser-use
description: Arc42 and Pipeline report for browser-use/browser-use
---

# Repository Architecture Analysis: browser-use/browser-use

## Metadata
- **SHA**: `dfb6a73d520809341c975c6a01c228327991e88b`
- **Primary Ecosystem**: Python

## Quality Metrics
- **avg_cyclomatic_complexity**: 4.6
- **component_count**: 9
- **files_analyzed**: 70
- **framework**: Unknown
- **loc**: 32616
- **max_cyclomatic_complexity**: 41
- **sloc**: 27161

# Architecture: browser-use/browser-use

## Context
- **Repository**: `browser-use/browser-use`
- **SHA**: `dfb6a73d520809341c975c6a01c228327991e88b`
- **Ecosystem**: Python
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    ActionResult["ActionResult : DATA_ACCESS_LAYER"]
    Story["Story : DATA_ACCESS_LAYER"]
    Order["Order : DATA_ACCESS_LAYER"]
    Account["Account : DATA_ACCESS_LAYER"]
    _Author["_Author : DATA_ACCESS_LAYER"]
    _Authors["_Authors : DATA_ACCESS_LAYER"]
    Count["Count : DATA_ACCESS_LAYER"]
    Creds["Creds : DATA_ACCESS_LAYER"]
    repo_root(["browser-use/browser-use"])
    repo_root --> Count
    repo_root --> Creds
    repo_root --> _Author
    repo_root --> _Authors
    Account --> ActionResult
    Order --> ActionResult
    Story --> ActionResult
```

## Component Details
- **ActionResult** (`browser_use/tools.py`): DATA_ACCESS_LAYER
- **Story** (`tests/ci/test_agent.py`): DATA_ACCESS_LAYER
- **Order** (`tests/ci/test_compat.py`): DATA_ACCESS_LAYER (deps: ActionResult)
- **Account** (`tests/ci/test_compat.py`): DATA_ACCESS_LAYER (deps: ActionResult)
- **Story** (`tests/ci/test_compat.py`): DATA_ACCESS_LAYER (deps: ActionResult)
- **_Author** (`tests/ci/test_loop.py`): DATA_ACCESS_LAYER
- **_Authors** (`tests/ci/test_loop.py`): DATA_ACCESS_LAYER
- **Count** (`tests/ci/test_loop.py`): DATA_ACCESS_LAYER
- **Creds** (`tests/ci/test_repl.py`): DATA_ACCESS_LAYER


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
