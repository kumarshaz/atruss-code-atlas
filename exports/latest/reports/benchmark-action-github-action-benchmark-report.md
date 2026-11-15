---
title: Architecture — benchmark-action/github-action-benchmark
description: Arc42 and Pipeline report for benchmark-action/github-action-benchmark
---

# Repository Architecture Analysis: benchmark-action/github-action-benchmark

## Metadata
- **SHA**: `84ec6ea748925b6580796c05ce7a1c8fd0d15f3b`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.03
- **avg_cyclomatic_complexity**: 1.7
- **component_count**: 10
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 68.83
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 46
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: TypeScript
- **import_edges**: 100 entry(ies)
- **loc**: 6523
- **max_cognitive_complexity**: 44
- **max_cyclomatic_complexity**: 19
- **sloc**: 5730
- **test_file_count**: 45

# Architecture: benchmark-action/github-action-benchmark

## Context
- **Repository**: `benchmark-action/github-action-benchmark`
- **SHA**: `84ec6ea748925b6580796c05ce7a1c8fd0d15f3b`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: TypeScript

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
    benchmark_example["benchmark-example : MODULE"]:::atlasJob
    github_action_benchmark["github-action-benchmark : MODULE"]:::atlasJob
    Sample["Sample : MODULE"]:::atlasJob
    bench["bench : module"]:::atlasJob
    lib["lib : module"]:::atlasJob
    fib["fib : module"]:::atlasJob
    fib_test["fib_test : module"]:::atlasJob
    jmh_sample["jmh-sample : MODULE"]:::atlasJob
    repo_root(["benchmark-action/github-action-benchmark"]):::atlasRoot
    repo_root --> Sample
    repo_root --> bench
    repo_root --> benchmark_example
    repo_root --> fib
    repo_root --> fib_test
    repo_root --> github_action_benchmark
    repo_root --> jmh_sample
    repo_root --> lib
```

## Component Details
- **benchmark-example** (`examples/benchmarkjs/package.json`): MODULE
- **github-action-benchmark** (`package.json`): MODULE
- **Sample** (`examples/benchmarkdotnet/Sample.csproj`): MODULE
- **bench** (`examples/criterion-rs/benches/bench.rs`): module
- **lib** (`examples/criterion-rs/src/lib.rs`): module
- **fib** (`examples/go/fib.go`): module
- **fib_test** (`examples/go/fib_test.go`): module
- **jmh-sample** (`examples/java/pom.xml`): MODULE
- **bench** (`examples/rust/benches/bench.rs`): module
- **lib** (`examples/rust/src/lib.rs`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (46.50/100)
- **Technical Debt Score**: 53.50
- **Estimated Remediation Effort**: 104.64h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `D` | 69.00 | 0.20 | avg_cc=1.70, max_cc=19, duplication=68.83%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=573, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 48.00 | 0.15 | avg_cognitive=1.03, max_cognitive=44, fitness_violations=2, oversized_files=3 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=16, operational_antipatterns=42, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=32 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (68.83) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (44.0) exceeds policy threshold (25.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 573 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `org.openjdk.jmh:jmh-core` `1.29` (Maven, `examples/java/pom.xml`)
- `org.openjdk.jmh:jmh-generator-annprocess` `1.29` (Maven, `examples/java/pom.xml`)
- `BenchmarkDotNet` `0.13.1` (NuGet, `examples/benchmarkdotnet/Sample.csproj`)
- `atomicwrites` `1.3.0` (PyPI, `examples/pytest/requirements.txt`)
- `attrs` `19.3.0` (PyPI, `examples/pytest/requirements.txt`)
- `importlib-metadata` `0.23` (PyPI, `examples/pytest/requirements.txt`)
- `more-itertools` `7.2.0` (PyPI, `examples/pytest/requirements.txt`)
- `packaging` `19.2` (PyPI, `examples/pytest/requirements.txt`)
- `pluggy` `0.13.0` (PyPI, `examples/pytest/requirements.txt`)
- `py` `1.10.0` (PyPI, `examples/pytest/requirements.txt`)
- `py-cpuinfo` `5.0.0` (PyPI, `examples/pytest/requirements.txt`)
- `pyparsing` `2.4.5` (PyPI, `examples/pytest/requirements.txt`)
- `pytest` `5.2.4` (PyPI, `examples/pytest/requirements.txt`)
- `pytest-benchmark` `3.2.2` (PyPI, `examples/pytest/requirements.txt`)
- `six` `1.13.0` (PyPI, `examples/pytest/requirements.txt`)
- `wcwidth` `0.1.7` (PyPI, `examples/pytest/requirements.txt`)
- `zipp` `3.19.1` (PyPI, `examples/pytest/requirements.txt`)
- `criterion` `*` (cargo, `examples/criterion-rs/Cargo.toml`)
- `@actions/core` `1.11.1` (npm, `package-lock.json`)
- `@actions/core` `1.11.1` (npm, `package.json`)
- `@actions/exec` `1.1.1` (npm, `package-lock.json`)
- `@actions/exec` `1.1.1` (npm, `package.json`)
- `@actions/github` `5.1.1` (npm, `package-lock.json`)
- `@actions/github` `5.1.1` (npm, `package.json`)
- `@actions/io` `1.1.2` (npm, `package-lock.json`)
- `@actions/io` `1.1.2` (npm, `package.json`)
- `@types/acorn` `4.0.5` (npm, `package-lock.json`)
- `@types/acorn` `4.0.5` (npm, `package.json`)
- `@types/cheerio` `0.22.16` (npm, `package-lock.json`)
- `@types/cheerio` `0.22.16` (npm, `package.json`)
- ... (+543 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_examples_benchmarkdotnet["examples/benchmarkdotnet"]:::atlasCategory
        mod_examples_benchmarkjs["examples/benchmarkjs"]:::atlasCategory
        mod_examples_criterion_rs["examples/criterion-rs"]:::atlasCategory
        mod_examples_go["examples/go"]:::atlasCategory
        mod_examples_java["examples/java"]:::atlasCategory
        mod_examples_pytest["examples/pytest"]:::atlasCategory
        mod_examples_rust["examples/rust"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_benchmarkdotnet_yml_benchmark["benchmarkdotnet.yml#benchmark"]:::atlasJob
        job_benchmarkjs_yml_benchmark["benchmarkjs.yml#benchmark"]:::atlasJob
        job_ci_results_repo_yml_benchmarkdotnet_framework["ci-results-repo.yml#benchmarkdotnet-framework"]:::atlasJob
        job_ci_results_repo_yml_benchmarkjs["ci-results-repo.yml#benchmarkjs"]:::atlasJob
        job_ci_results_repo_yml_go["ci-results-repo.yml#go"]:::atlasJob
        job_ci_results_repo_yml_java_jmh["ci-results-repo.yml#java-jmh"]:::atlasJob
        job_ci_results_repo_yml_only_alert_with_cache["ci-results-repo.yml#only-alert-with-cache"]:::atlasJob
        job_ci_results_repo_yml_pytest_benchmark["ci-results-repo.yml#pytest-benchmark"]:::atlasJob
        job_ci_results_repo_yml_rust["ci-results-repo.yml#rust"]:::atlasJob
        job_ci_results_repo_yml_rust_criterion_rs_framework["ci-results-repo.yml#rust-criterion-rs-framework"]:::atlasJob
        job_ci_yml_benchmarkdotnet_framework["ci.yml#benchmarkdotnet-framework"]:::atlasJob
        job_ci_yml_benchmarkjs["ci.yml#benchmarkjs"]:::atlasJob
        job_ci_yml_go["ci.yml#go"]:::atlasJob
        job_ci_yml_java_jmh["ci.yml#java-jmh"]:::atlasJob
        job_ci_yml_only_alert_with_cache["ci.yml#only-alert-with-cache"]:::atlasJob
        job_ci_yml_pytest_benchmark["ci.yml#pytest-benchmark"]:::atlasJob
        job_ci_yml_rust["ci.yml#rust"]:::atlasJob
        job_ci_yml_rust_criterion_rs_framework["ci.yml#rust-criterion-rs-framework"]:::atlasJob
        job_commit_comment_yml_benchmark["commit-comment.yml#benchmark"]:::atlasJob
        job_go_yml_benchmark["go.yml#benchmark"]:::atlasJob
        job_java_yml_benchmark["java.yml#benchmark"]:::atlasJob
        job_minimal_yml_benchmark["minimal.yml#benchmark"]:::atlasJob
        job_pytest_yml_benchmark["pytest.yml#benchmark"]:::atlasJob
        job_rust_criterion_rs_yml_benchmark["rust-criterion-rs.yml#benchmark"]:::atlasJob
        job_rust_yml_benchmark["rust.yml#benchmark"]:::atlasJob
    end
    mod_examples_benchmarkdotnet -->|BUILT_BY| job_benchmarkdotnet_yml_benchmark
    mod_examples_benchmarkdotnet -->|BUILT_BY| job_ci_results_repo_yml_benchmarkdotnet_framework
    mod_examples_benchmarkdotnet -->|BUILT_BY| job_ci_yml_benchmarkdotnet_framework
    mod_examples_benchmarkjs -->|BUILT_BY| job_benchmarkjs_yml_benchmark
    mod_examples_benchmarkjs -->|BUILT_BY| job_ci_results_repo_yml_benchmarkjs
    mod_examples_benchmarkjs -->|BUILT_BY| job_ci_yml_benchmarkjs
    mod_examples_criterion_rs -->|BUILT_BY| job_ci_results_repo_yml_rust_criterion_rs_framework
    mod_examples_criterion_rs -->|BUILT_BY| job_ci_yml_rust_criterion_rs_framework
    mod_examples_criterion_rs -->|BUILT_BY| job_rust_criterion_rs_yml_benchmark
    mod_examples_go -->|BUILT_BY| job_ci_results_repo_yml_go
    mod_examples_go -->|BUILT_BY| job_ci_results_repo_yml_only_alert_with_cache
    mod_examples_go -->|BUILT_BY| job_ci_yml_go
    mod_examples_go -->|BUILT_BY| job_ci_yml_only_alert_with_cache
    mod_examples_go -->|BUILT_BY| job_commit_comment_yml_benchmark
    mod_examples_go -->|BUILT_BY| job_go_yml_benchmark
    mod_examples_go -->|BUILT_BY| job_minimal_yml_benchmark
    mod_examples_java -->|BUILT_BY| job_ci_results_repo_yml_java_jmh
    mod_examples_java -->|BUILT_BY| job_ci_yml_java_jmh
    mod_examples_java -->|BUILT_BY| job_java_yml_benchmark
    mod_examples_pytest -->|BUILT_BY| job_ci_results_repo_yml_pytest_benchmark
    mod_examples_pytest -->|BUILT_BY| job_ci_yml_pytest_benchmark
    mod_examples_pytest -->|BUILT_BY| job_pytest_yml_benchmark
    mod_examples_rust -->|BUILT_BY| job_ci_results_repo_yml_rust
    mod_examples_rust -->|BUILT_BY| job_ci_yml_rust
    mod_examples_rust -->|BUILT_BY| job_rust_yml_benchmark
```

- `examples/benchmarkdotnet` (code_module) --[BUILT_BY]--> `benchmarkdotnet.yml#benchmark` (ci_job)
- `examples/benchmarkdotnet` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#benchmarkdotnet-framework` (ci_job)
- `examples/benchmarkdotnet` (code_module) --[BUILT_BY]--> `ci.yml#benchmarkdotnet-framework` (ci_job)
- `examples/benchmarkjs` (code_module) --[BUILT_BY]--> `benchmarkjs.yml#benchmark` (ci_job)
- `examples/benchmarkjs` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#benchmarkjs` (ci_job)
- `examples/benchmarkjs` (code_module) --[BUILT_BY]--> `ci.yml#benchmarkjs` (ci_job)
- `examples/criterion-rs` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#rust-criterion-rs-framework` (ci_job)
- `examples/criterion-rs` (code_module) --[BUILT_BY]--> `ci.yml#rust-criterion-rs-framework` (ci_job)
- `examples/criterion-rs` (code_module) --[BUILT_BY]--> `rust-criterion-rs.yml#benchmark` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#go` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#only-alert-with-cache` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `ci.yml#go` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `ci.yml#only-alert-with-cache` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `commit-comment.yml#benchmark` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `go.yml#benchmark` (ci_job)
- `examples/go` (code_module) --[BUILT_BY]--> `minimal.yml#benchmark` (ci_job)
- `examples/java` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#java-jmh` (ci_job)
- `examples/java` (code_module) --[BUILT_BY]--> `ci.yml#java-jmh` (ci_job)
- `examples/java` (code_module) --[BUILT_BY]--> `java.yml#benchmark` (ci_job)
- `examples/pytest` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#pytest-benchmark` (ci_job)
- `examples/pytest` (code_module) --[BUILT_BY]--> `ci.yml#pytest-benchmark` (ci_job)
- `examples/pytest` (code_module) --[BUILT_BY]--> `pytest.yml#benchmark` (ci_job)
- `examples/rust` (code_module) --[BUILT_BY]--> `ci-results-repo.yml#rust` (ci_job)
- `examples/rust` (code_module) --[BUILT_BY]--> `ci.yml#rust` (ci_job)
- `examples/rust` (code_module) --[BUILT_BY]--> `rust.yml#benchmark` (ci_job)


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
  pipeline_root(["benchmark-action/github-action-benchmark (16 workflows)"]):::atlasRoot
  grp_0_CI___Verification["CI & Verification (15 workflows · 39 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_CI___Verification
  wf_0_Benchmark_Net_Example["Benchmark.Net Example (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_0_Benchmark_Net_Example
  job_0_benchmark["benchmark"]:::atlasJob
  wf_0_Benchmark_Net_Example --> job_0_benchmark
  wf_1_Benchmark_js_Example["Benchmark.js Example (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_1_Benchmark_js_Example
  job_1_benchmark["benchmark"]:::atlasJob
  wf_1_Benchmark_js_Example --> job_1_benchmark
  wf_2_Catch2_C___Example["Catch2 C++ Example (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_2_Catch2_C___Example
  job_2_benchmark["benchmark"]:::atlasJob
  wf_2_Catch2_C___Example --> job_2_benchmark
  wf_3_Catch2_C___Example["Catch2 C++ Example (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_3_Catch2_C___Example
  job_3_benchmark["benchmark"]:::atlasJob
  wf_3_Catch2_C___Example --> job_3_benchmark
  wf_4_CI___separate_results_repo["CI - separate results repo (12 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_4_CI___separate_results_repo
  job_4_benchmarkdotnet_framework["benchmarkdotnet-framework"]:::atlasJob
  job_4_benchmarkjs["benchmarkjs"]:::atlasJob
  job_4_catch2_v2_framework["catch2-v2-framework"]:::atlasJob
  wf_4_CI___separate_results_repo --> job_4_benchmarkdotnet_framework
  wf_4_CI___separate_results_repo --> job_4_benchmarkjs
  wf_4_CI___separate_results_repo --> job_4_catch2_v2_framework
  wf_5_CI["CI (14 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_5_CI
  job_5_benchmarkdotnet_framework["benchmarkdotnet-framework"]:::atlasJob
  job_5_benchmarkjs["benchmarkjs"]:::atlasJob
  job_5_catch2_v2_framework["catch2-v2-framework"]:::atlasJob
  wf_5_CI --> job_5_benchmarkdotnet_framework
  wf_5_CI --> job_5_benchmarkjs
  wf_5_CI --> job_5_catch2_v2_framework
  wf_6_Example_for_alert_with_commit_comment["Example for alert with commit comment (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_6_Example_for_alert_with_commit_comment
  job_6_benchmark["benchmark"]:::atlasJob
  wf_6_Example_for_alert_with_commit_comment --> job_6_benchmark
  wf_7_C___Example["C++ Example (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_7_C___Example
  job_7_benchmark["benchmark"]:::atlasJob
  wf_7_C___Example --> job_7_benchmark
  wf_13_Criterion_rs_Example["Criterion.rs Example (1 jobs)"]:::atlasWorkflow
  grp_0_CI___Verification --> wf_13_Criterion_rs_Example
  job_13_benchmark["benchmark"]:::atlasJob
  wf_13_Criterion_rs_Example --> job_13_benchmark
  grp_1_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_Scheduled___Manual
  wf_15_Validate_action_typings["Validate action typings (1 jobs)"]:::atlasWorkflow
  grp_1_Scheduled___Manual --> wf_15_Validate_action_typings
  job_15_validate_typings["validate-typings"]:::atlasJob
  wf_15_Validate_action_typings --> job_15_validate_typings
  wf_more["+6 more workflows"]:::atlasMore
  pipeline_root --> wf_more
```
