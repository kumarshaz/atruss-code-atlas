---
title: Architecture — slab/quill
description: Arc42 and Pipeline report for slab/quill
---

# Repository Architecture Analysis: slab/quill

## Metadata
- **SHA**: `539cbffd0a13b18e9c65eb84dd35e6596e403158`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **avg_cyclomatic_complexity**: 6.42
- **component_count**: 16
- **files_analyzed**: 315
- **framework**: Next.js
- **loc**: 43670
- **max_cyclomatic_complexity**: 92
- **sloc**: 38904

# Architecture: slab/quill

## Context
- **Repository**: `slab/quill`
- **SHA**: `539cbffd0a13b18e9c65eb84dd35e6596e403158`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    quill_monorepo["quill-monorepo : MODULE"]
    quill["quill : MODULE"]
    website["website : MODULE"]
    Heading1["Heading1 : UI_COMPONENT"]
    Heading2["Heading2 : UI_COMPONENT"]
    Heading3["Heading3 : UI_COMPONENT"]
    Heading4["Heading4 : UI_COMPONENT"]
    Heading5["Heading5 : UI_COMPONENT"]
    Heading6["Heading6 : UI_COMPONENT"]
    MDX["MDX : UI_COMPONENT"]
    StandaloneSandpack["StandaloneSandpack : UI_COMPONENT"]
    SandpackWithQuillTemplate["SandpackWithQuillTemplate : UI_COMPONENT"]
    Head["Head : UI_COMPONENT"]
    MyApp["MyApp : UI_COMPONENT"]
    Document["Document : UI_COMPONENT"]
    Doc["Doc : UI_COMPONENT"]
    repo_root(["slab/quill"])
    repo_root --> Document
    repo_root --> Head
    repo_root --> MyApp
    repo_root --> quill
    repo_root --> quill_monorepo
    repo_root --> website
    Doc --> MDX
    MDX --> Heading1
    MDX --> Heading2
    MDX --> Heading3
    MDX --> Heading4
    MDX --> Heading5
    MDX --> Heading6
    MDX --> SandpackWithQuillTemplate
    MDX --> StandaloneSandpack
```

## Component Details
- **quill-monorepo** (`package.json`): MODULE
- **quill** (`packages/quill/package.json`): MODULE
- **website** (`packages/website/package.json`): MODULE
- **Heading1** (`packages/website/src/components/Heading.jsx`): UI_COMPONENT
- **Heading2** (`packages/website/src/components/Heading.jsx`): UI_COMPONENT
- **Heading3** (`packages/website/src/components/Heading.jsx`): UI_COMPONENT
- **Heading4** (`packages/website/src/components/Heading.jsx`): UI_COMPONENT
- **Heading5** (`packages/website/src/components/Heading.jsx`): UI_COMPONENT
- **Heading6** (`packages/website/src/components/Heading.jsx`): UI_COMPONENT
- **MDX** (`packages/website/src/components/MDX.jsx`): UI_COMPONENT (deps: Heading1, Heading2, Heading3, Heading4, Heading5, Heading6, SandpackWithQuillTemplate, StandaloneSandpack)
- **StandaloneSandpack** (`packages/website/src/components/Sandpack.jsx`): UI_COMPONENT
- **SandpackWithQuillTemplate** (`packages/website/src/components/Sandpack.jsx`): UI_COMPONENT
- **Head** (`packages/website/src/pages/404.jsx`): UI_COMPONENT
- **MyApp** (`packages/website/src/pages/_app.jsx`): UI_COMPONENT
- **Document** (`packages/website/src/pages/_document.jsx`): UI_COMPONENT
- **Doc** (`packages/website/src/pages/docs/[...id].jsx`): UI_COMPONENT (deps: MDX)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
