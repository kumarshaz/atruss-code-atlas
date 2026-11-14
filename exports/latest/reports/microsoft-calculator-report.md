---
title: Architecture — microsoft/calculator
description: Arc42 and Pipeline report for microsoft/calculator
---

# Repository Architecture Analysis: microsoft/calculator

## Metadata
- **SHA**: `79e1ac53bba690cdf930e5dcd6ed9dbc4cbfb128`
- **Primary Ecosystem**: .NET

## Quality Metrics
- **avg_cyclomatic_complexity**: 10.96
- **component_count**: 6
- **files_analyzed**: 150
- **framework**: Unknown
- **loc**: 36361
- **max_cyclomatic_complexity**: 229
- **sloc**: 29853

# Architecture: microsoft/calculator

## Context
- **Repository**: `microsoft/calculator`
- **SHA**: `79e1ac53bba690cdf930e5dcd6ed9dbc4cbfb128`
- **Ecosystem**: .NET
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    Calculator["Calculator : MODULE"]
    Calculator_Tests["Calculator.Tests : MODULE"]
    Calculator_ViewModels["Calculator.ViewModels : MODULE"]
    CalculatorUITestFramework["CalculatorUITestFramework : MODULE"]
    CalculatorUITests["CalculatorUITests : MODULE"]
    TraceLogging_Managed["TraceLogging.Managed : MODULE"]
    Calculator --> CalcManager_Interop
    Calculator --> Calculator_ViewModels
    Calculator --> GraphControl
    Calculator --> TraceLogging_Managed
    CalculatorUITests --> CalculatorUITestFramework
    Calculator_Tests --> CalcManager_Interop
    Calculator_Tests --> Calculator_ViewModels
    Calculator_Tests --> GraphControl
    Calculator_ViewModels --> CalcManager_Interop
    Calculator_ViewModels --> GraphControl
    Calculator_ViewModels --> TraceLogging_Managed
```

## Component Details
- **Calculator** (`src/Calculator/Calculator.csproj`): MODULE (deps: CalcManager.Interop, Calculator.ViewModels, GraphControl, TraceLogging.Managed)
- **Calculator.Tests** (`src/Calculator.Tests/Calculator.Tests.csproj`): MODULE (deps: CalcManager.Interop, Calculator.ViewModels, GraphControl)
- **Calculator.ViewModels** (`src/Calculator.ViewModels/Calculator.ViewModels.csproj`): MODULE (deps: CalcManager.Interop, GraphControl, TraceLogging.Managed)
- **CalculatorUITestFramework** (`src/CalculatorUITestFramework/CalculatorUITestFramework.csproj`): MODULE
- **CalculatorUITests** (`src/CalculatorUITests/CalculatorUITests.csproj`): MODULE (deps: CalculatorUITestFramework)
- **TraceLogging.Managed** (`src/TraceLogging.Managed/TraceLogging.Managed.csproj`): MODULE


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
