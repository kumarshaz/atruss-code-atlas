---
title: Architecture — App-vNext/Polly
description: Arc42 and Pipeline report for App-vNext/Polly
---

# Repository Architecture Analysis: App-vNext/Polly

## Metadata
- **SHA**: `88f2039c1d865158a91fe05b8ac23d73a88a9092`
- **Primary Ecosystem**: .NET

## Quality Metrics
- **avg_cyclomatic_complexity**: 3.84
- **component_count**: 30
- **files_analyzed**: 1594
- **framework**: ASP.NET Core
- **loc**: 212306
- **max_cyclomatic_complexity**: 182
- **sloc**: 144446

# Architecture: App-vNext/Polly

## Context
- **Repository**: `App-vNext/Polly`
- **SHA**: `88f2039c1d865158a91fe05b8ac23d73a88a9092`
- **Ecosystem**: .NET
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    repo_root(["App-vNext/Polly (30 components)"])
    dir_0_src["src (14)"]
    repo_root --> dir_0_src
    sub_0_0_Polly_Core["Polly.Core (5)"]
    dir_0_src --> sub_0_0_Polly_Core
    sub_0_1_Polly["Polly (4)"]
    dir_0_src --> sub_0_1_Polly
    sub_0_2_Snippets["Snippets (2)"]
    dir_0_src --> sub_0_2_Snippets
    sub_0_more["+3 more submodules (3)"]
    dir_0_src --> sub_0_more
    dir_1_samples["samples (7)"]
    repo_root --> dir_1_samples
    dir_2_test["test (7)"]
    repo_root --> dir_2_test
    dir_3_bench["bench (2)"]
    repo_root --> dir_3_bench
    dir_2_test -.->|"10 deps"| sub_0_more
    dir_2_test -.->|"3 deps"| sub_0_0_Polly_Core
    sub_0_1_Polly -.->|"3 deps"| sub_0_0_Polly_Core
    sub_0_2_Snippets -.->|"3 deps"| sub_0_more
    sub_0_more -.->|"3 deps"| sub_0_0_Polly_Core
    dir_3_bench -.->|"2 deps"| sub_0_1_Polly
    dir_3_bench -.->|"2 deps"| sub_0_more
    dir_2_test -.->|"1 dep"| sub_0_1_Polly
    dir_3_bench -.->|"1 dep"| sub_0_0_Polly_Core
    sub_0_2_Snippets -.->|"1 dep"| sub_0_1_Polly
```

## Component Details
- **Polly.Benchmarks** (`bench/Polly.Benchmarks/Polly.Benchmarks.csproj`): MODULE (deps: Polly)
- **Polly.Core.Benchmarks** (`bench/Polly.Core.Benchmarks/Polly.Core.Benchmarks.csproj`): MODULE (deps: Polly, Polly.Core, Polly.Extensions, Polly.RateLimiting)
- **Chaos** (`samples/Chaos/Chaos.csproj`): MODULE
- **DependencyInjection** (`samples/DependencyInjection/DependencyInjection.csproj`): MODULE
- **Extensibility** (`samples/Extensibility/Extensibility.csproj`): MODULE
- **GenericPipelines** (`samples/GenericPipelines/GenericPipelines.csproj`): MODULE
- **Intro** (`samples/Intro/Intro.csproj`): MODULE
- **Retries** (`samples/Retries/Retries.csproj`): MODULE
- **Polly** (`src/Polly/Polly.csproj`): MODULE (deps: Polly.Core)
- **Polly.Core** (`src/Polly.Core/Polly.Core.csproj`): MODULE
- **Polly.Extensions** (`src/Polly.Extensions/Polly.Extensions.csproj`): MODULE (deps: Polly.Core)
- **Polly.RateLimiting** (`src/Polly.RateLimiting/Polly.RateLimiting.csproj`): MODULE (deps: Polly.Core)
- **Polly.Testing** (`src/Polly.Testing/Polly.Testing.csproj`): MODULE (deps: Polly.Core)
- **Snippets** (`src/Snippets/Snippets.csproj`): MODULE (deps: Polly, Polly.Extensions, Polly.RateLimiting, Polly.Testing)
- **Polly.AotTest** (`test/Polly.AotTest/Polly.AotTest.csproj`): MODULE (deps: Polly.Core, Polly.Extensions, Polly.RateLimiting)
- **Polly.Core.Tests** (`test/Polly.Core.Tests/Polly.Core.Tests.csproj`): MODULE (deps: Polly.Core, Polly.TestUtils, Polly.Testing)
- **Polly.Extensions.Tests** (`test/Polly.Extensions.Tests/Polly.Extensions.Tests.csproj`): MODULE (deps: Polly.Extensions, Polly.RateLimiting, Polly.TestUtils)
- **Polly.RateLimiting.Tests** (`test/Polly.RateLimiting.Tests/Polly.RateLimiting.Tests.csproj`): MODULE (deps: Polly.RateLimiting, Polly.TestUtils, Polly.Testing)
- **Polly.Specs** (`test/Polly.Specs/Polly.Specs.csproj`): MODULE (deps: Polly, Polly.TestUtils)
- **Polly.TestUtils** (`test/Polly.TestUtils/Polly.TestUtils.csproj`): MODULE (deps: Polly.Core)
- **Polly.Testing.Tests** (`test/Polly.Testing.Tests/Polly.Testing.Tests.csproj`): MODULE (deps: Polly.Extensions, Polly.RateLimiting, Polly.Testing)
- **GET_root** (`samples/Chaos/Program.cs`): API_ROUTE
- **CircuitStateController** (`src/Polly.Core/CircuitBreaker/Controller/CircuitStateController.cs`): API_ROUTE
- **FallbackHandler** (`src/Polly.Core/Fallback/FallbackHandler.cs`): SERVICE
- **HedgingController** (`src/Polly.Core/Hedging/Controller/HedgingController.cs`): API_ROUTE (deps: HedgingHandler)
- **HedgingHandler** (`src/Polly.Core/Hedging/Controller/HedgingHandler.cs`): SERVICE
- **AdvancedCircuitController** (`src/Polly/CircuitBreaker/AdvancedCircuitController.cs`): API_ROUTE (deps: CircuitStateController)
- **CircuitStateController** (`src/Polly/CircuitBreaker/CircuitStateController.cs`): API_ROUTE
- **ConsecutiveCountCircuitController** (`src/Polly/CircuitBreaker/ConsecutiveCountCircuitController.cs`): API_ROUTE (deps: CircuitStateController)
- **HedgingHandler** (`src/Snippets/Docs/Hedging.cs`): SERVICE


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
