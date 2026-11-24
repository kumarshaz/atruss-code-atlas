---
title: Architecture — drone-runners/drone-runner-kube
description: Arc42 and Pipeline report for drone-runners/drone-runner-kube
---

# Repository Architecture Analysis: drone-runners/drone-runner-kube

## Metadata
- **SHA**: `018c41607ac6366a59beaa9a2cf497669dc07258`
- **Primary Ecosystem**: Go

## Quality Metrics
- **ast_engine**: fallback
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 0.0
- **component_count**: 67
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.0
- **file_complexities**: 0 entry(ies)
- **files_analyzed**: 67
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Go Service
- **import_edges**: 0 entry(ies)
- **loc**: 8875
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 0
- **sloc**: 6827
- **test_file_count**: 21

# Architecture: drone-runners/drone-runner-kube

## Context
- **Repository**: `drone-runners/drone-runner-kube`
- **SHA**: `018c41607ac6366a59beaa9a2cf497669dc07258`
- **Ecosystem**: Go
- **Framework**: Go Service

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
    repo_root(["drone-runners/drone-runner-kube (67 components)"]):::atlasRoot
    subgraph sg_dir_0_engine["engine (47)"]
      direction TB
      dir_0_engine["engine (47)"]:::atlasCategory
      sub_0_0_compiler["compiler (15)"]:::atlasWorkflow
      dir_0_engine --> sub_0_0_compiler
      sub_0_1__module_root_["(module root) (9)"]:::atlasWorkflow
      dir_0_engine --> sub_0_1__module_root_
      sub_0_2_policy["policy (7)"]:::atlasWorkflow
      dir_0_engine --> sub_0_2_policy
      sub_0_more["+5 more submodules (16)"]:::atlasMore
      dir_0_engine --> sub_0_more
    end
    repo_root --> dir_0_engine
    subgraph sg_dir_1_internal["internal (12)"]
      direction TB
      dir_1_internal["internal (12)"]:::atlasCategory
      sub_1_0_docker["docker (3)"]:::atlasWorkflow
      dir_1_internal --> sub_1_0_docker
      sub_1_1_mock["mock (3)"]:::atlasWorkflow
      dir_1_internal --> sub_1_1_mock
      sub_1_2_encoder["encoder (2)"]:::atlasWorkflow
      dir_1_internal --> sub_1_2_encoder
      sub_1_more["+3 more submodules (4)"]:::atlasMore
      dir_1_internal --> sub_1_more
    end
    repo_root --> dir_1_internal
    dir_2_command["command (6)"]:::atlasCategory
    repo_root --> dir_2_command
    dir_3__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_3__root_
    dir_4_docker["docker (1)"]:::atlasCategory
    repo_root --> dir_4_docker
```

## Component Details

Showing top 60 representative components out of 67 across 5 module group(s):

- **Module `engine`** (47 components — module: 47)
- **Module `internal`** (12 components — module: 12)
- **Module `command`** (6 components — module: 6)
- **Module `(root)`** (1 components — module: 1)
- **Module `docker`** (1 components — module: 1)

- **cancellable_copy** (`engine/cancellable_copy.go`): module
- **clone** (`engine/compiler/clone.go`): module
- **clone_test** (`engine/compiler/clone_test.go`): module
- **command** (`command/command.go`): module
- **compile** (`command/compile.go`): module
- **compiler** (`engine/compiler/compiler.go`): module
- **compiler_test** (`engine/compiler/compiler_test.go`): module
- **config** (`command/daemon/config.go`): module
- **const** (`engine/const.go`): module
- **const_test** (`engine/const_test.go`): module
- **container** (`engine/podwatcher/container.go`): module
- **convert** (`engine/convert.go`): module
- **convert_test** (`engine/convert_test.go`): module
- **daemon** (`command/daemon/daemon.go`): module
- **docker** (`internal/docker/docker.go`): module
- **dump** (`engine/dump.go`): module
- **encoder** (`internal/encoder/encoder.go`): module
- **encoder_test** (`internal/encoder/encoder_test.go`): module
- **engine** (`engine/engine.go`): module
- **engine_impl** (`engine/engine_impl.go`): module
- **errors** (`engine/podwatcher/errors.go`): module
- **exec** (`command/exec.go`): module
- **flags** (`command/internal/flags.go`): module
- **image** (`internal/docker/image/image.go`): module
- **image_test** (`internal/docker/image/image_test.go`): module
- **internal** (`internal/internal.go`): module
- **kube** (`internal/kube/kube.go`): module
- **kubernetes** (`engine/podwatcher/kubernetes.go`): module
- **launcher** (`engine/launcher/launcher.go`): module
- **linter** (`engine/linter/linter.go`): module
- **linter_test** (`engine/linter/linter_test.go`): module
- **lookup** (`engine/resource/lookup.go`): module
- **lookup_test** (`engine/resource/lookup_test.go`): module
- **main** (`docker/placeholder/main.go`): module
- **main** (`main.go`): module
- **match** (`engine/policy/match.go`): module
- **match** (`internal/match/match.go`): module
- **match_test** (`engine/policy/match_test.go`): module
- **match_test** (`internal/match/match_test.go`): module
- **mock** (`internal/mock/mock.go`): module
- **mock_engine_gen** (`internal/mock/mock_engine_gen.go`): module
- **mock_execer_gen** (`internal/mock/mock_execer_gen.go`): module
- **parser** (`engine/policy/parser.go`): module
- **parser** (`engine/resource/parser.go`): module
- **parser_test** (`engine/policy/parser_test.go`): module
- **parser_test** (`engine/resource/parser_test.go`): module
- **pipeline** (`engine/resource/pipeline.go`): module
- **pipeline_test** (`engine/resource/pipeline_test.go`): module
- **policy** (`engine/policy/policy.go`): module
- **policy_test** (`engine/policy/policy_test.go`): module
- **powershell** (`engine/compiler/shell/powershell/powershell.go`): module
- **powershell_test** (`engine/compiler/shell/powershell/powershell_test.go`): module
- **rand** (`engine/policy/rand.go`): module
- **replacer** (`engine/replacer/replacer.go`): module
- **replacer_test** (`engine/replacer/replacer_test.go`): module
- **script** (`engine/compiler/script.go`): module
- **script_test** (`engine/compiler/script_test.go`): module
- **shell** (`engine/compiler/shell/shell.go`): module
- **shell_test** (`engine/compiler/shell/shell_test.go`): module
- **spec** (`engine/spec.go`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `B` (84.25/100)
- **Technical Debt Score**: 15.75
- **Estimated Remediation Effort**: 3.94h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 100.00 | 0.20 | avg_cc=0.00, max_cc=0, duplication=0.00%, dead_code=0 |
| Dependency Health | `B` | 85.00 | 0.15 | dependencies=25, outdated=0, vulnerable=0, has_lockfile=False |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 40.00 | 0.15 | workflows=0 |
| Security | `A` | 100.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=0 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=False, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 25 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `github.com/bmatcuk/doublestar` `1.1.1` (golang, `go.mod`)
- `github.com/buildkite/yaml` `2.1.0+incompatible` (golang, `go.mod`)
- `github.com/dchest/uniuri` `0.0.0-20160212164326-8902c56451e9` (golang, `go.mod`)
- `github.com/docker/distribution` `2.8.0+incompatible` (golang, `go.mod`)
- `github.com/docker/go-units` `0.4.0` (golang, `go.mod`)
- `github.com/drone/drone-go` `1.7.1` (golang, `go.mod`)
- `github.com/drone/envsubst` `1.0.3` (golang, `go.mod`)
- `github.com/drone/runner-go` `1.12.0` (golang, `go.mod`)
- `github.com/drone/signal` `1.0.0` (golang, `go.mod`)
- `github.com/ghodss/yaml` `1.0.0` (golang, `go.mod`)
- `github.com/golang/mock` `1.4.1` (golang, `go.mod`)
- `github.com/google/go-cmp` `0.5.5` (golang, `go.mod`)
- `github.com/gosimple/slug` `1.9.0` (golang, `go.mod`)
- `github.com/joho/godotenv` `1.3.0` (golang, `go.mod`)
- `github.com/kelseyhightower/envconfig` `1.4.0` (golang, `go.mod`)
- `github.com/mattn/go-isatty` `0.0.8` (golang, `go.mod`)
- `github.com/sirupsen/logrus` `1.4.2` (golang, `go.mod`)
- `golang.org/x/sync` `0.0.0-20201020160332-67f06af15bc9` (golang, `go.mod`)
- `gopkg.in/alecthomas/kingpin.v2` `2.2.6` (golang, `go.mod`)
- `k8s.io/api` `0.21.8` (golang, `go.mod`)
- `k8s.io/apimachinery` `0.21.8` (golang, `go.mod`)
- `k8s.io/client-go` `0.21.8` (golang, `go.mod`)
- `github.com/alecthomas/template` `0.0.0-20190718012654-fb15b899a751` (golang, `go.mod`)
- `github.com/alecthomas/units` `0.0.0-20190924025748-f65c72e2690d` (golang, `go.mod`)
- `github.com/opencontainers/go-digest` `1.0.0-rc1` (golang, `go.mod`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_docker["docker"]:::atlasCategory
        mod_docker_placeholder["docker/placeholder"]:::atlasCategory
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_docker_Dockerfile_linux_amd64["docker/Dockerfile.linux.amd64"]:::atlasWorkflow
        art_docker_Dockerfile_linux_arm64["docker/Dockerfile.linux.arm64"]:::atlasWorkflow
        art_docker_placeholder_Dockerfile["docker/placeholder/Dockerfile"]:::atlasWorkflow
    end
    mod_docker -->|PACKAGED_BY| art_docker_Dockerfile_linux_amd64
    mod_docker -->|PACKAGED_BY| art_docker_Dockerfile_linux_arm64
    mod_docker -->|PACKAGED_BY| art_docker_placeholder_Dockerfile
    mod_docker_placeholder -->|PACKAGED_BY| art_docker_placeholder_Dockerfile
```

- `docker` (code_module) --[PACKAGED_BY]--> `docker/Dockerfile.linux.amd64` (container)
- `docker` (code_module) --[PACKAGED_BY]--> `docker/Dockerfile.linux.arm64` (container)
- `docker` (code_module) --[PACKAGED_BY]--> `docker/placeholder/Dockerfile` (container)
- `docker/placeholder` (code_module) --[PACKAGED_BY]--> `docker/placeholder/Dockerfile` (container)


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
  NoWorkflows[No Workflows Detected]:::atlasMore
```
