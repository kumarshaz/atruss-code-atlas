---
title: Architecture — supabase/dbdev
description: Arc42 and Pipeline report for supabase/dbdev
---

# Repository Architecture Analysis: supabase/dbdev

## Metadata
- **SHA**: `4528188cdbdf4f7715eb2912caa9f0e3eb040687`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 1.41
- **avg_cyclomatic_complexity**: 2.26
- **component_count**: 26
- **dead_code_count**: 10
- **dead_code_symbols**: 10 entry(ies)
- **duplication_pct**: 59.16
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 119
- **fitness_passed**: False
- **fitness_violation_count**: 2
- **framework**: Next.js
- **import_edges**: 100 entry(ies)
- **loc**: 9753
- **max_cognitive_complexity**: 21
- **max_cyclomatic_complexity**: 27
- **sloc**: 8400
- **test_file_count**: 9

# Architecture: supabase/dbdev

## Context
- **Repository**: `supabase/dbdev`
- **SHA**: `4528188cdbdf4f7715eb2912caa9f0e3eb040687`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Next.js

## Building Block View

```mermaid
graph TD;
    repo_root(["supabase/dbdev (26 components)"])
    dir_0_cli["cli (14)"]
    repo_root --> dir_0_cli
    sub_0_0_src["src (7)"]
    dir_0_cli --> sub_0_0_src
    sub_0_1_src_commands["src/commands (7)"]
    dir_0_cli --> sub_0_1_src_commands
    dir_1_website["website (11)"]
    repo_root --> dir_1_website
    sub_1_0_components["components (5)"]
    dir_1_website --> sub_1_0_components
    sub_1_1_app["app (3)"]
    dir_1_website --> sub_1_1_app
    sub_1_2_lib["lib (2)"]
    dir_1_website --> sub_1_2_lib
    sub_1_more["+1 more submodules (1)"]
    dir_1_website --> sub_1_more
    dir_2__root_["(root) (1)"]
    repo_root --> dir_2__root_
```

## Component Details
- **dbdev** (`package.json`): MODULE
- **dbdev-website** (`website/package.json`): MODULE
- **RootLayout** (`website/app/layout.tsx`): UI_COMPONENT
- **API_search_route** (`website/app/api/search/route.ts`): API_ROUTE
- **Layout** (`website/app/docs/layout.tsx`): UI_COMPONENT
- **FORM_ERROR** (`website/components/forms/Form.tsx`): UI_COMPONENT
- **LOCAL_STORAGE_KEY** (`website/components/themes/ThemeContext.tsx`): UI_COMPONENT
- **DEFAULT_THEME** (`website/components/themes/ThemeContext.tsx`): UI_COMPONENT
- **ThemeContextProvider** (`website/components/themes/ThemeContext.tsx`): UI_COMPONENT
- **Toaster** (`website/components/ui/toaster.tsx`): UI_COMPONENT
- **AuthContext** (`website/lib/auth.tsx`): UI_COMPONENT
- **AuthProvider** (`website/lib/auth.tsx`): UI_COMPONENT
- **client** (`cli/src/client.rs`): module
- **config** (`cli/src/config.rs`): module
- **credential_store** (`cli/src/credential_store.rs`): module
- **main** (`cli/src/main.rs`): module
- **models** (`cli/src/models.rs`): module
- **secret** (`cli/src/secret.rs`): module
- **util** (`cli/src/util.rs`): module
- **add** (`cli/src/commands/add.rs`): module
- **install** (`cli/src/commands/install.rs`): module
- **list** (`cli/src/commands/list.rs`): module
- **login** (`cli/src/commands/login.rs`): module
- **mod** (`cli/src/commands/mod.rs`): module
- **publish** (`cli/src/commands/publish.rs`): module
- **uninstall** (`cli/src/commands/uninstall.rs`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (54.68/100)
- **Technical Debt Score**: 45.32
- **Estimated Remediation Effort**: 61.66h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 37.00 | 0.20 | avg_cc=2.26, max_cc=27, duplication=59.16%, dead_code=10 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=1326, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `B` | 86.50 | 0.15 | avg_cognitive=1.41, max_cognitive=21, fitness_violations=2, oversized_files=0 |
| Pipeline Health | `F` | 0.00 | 0.15 | workflows=10, operational_antipatterns=26, parallel_branches=True |
| Security | `F` | 44.00 | 0.20 | vulnerabilities=0, secrets=2, pipeline_security_findings=1 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (59.16) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (27.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 1326 | **Vulnerabilities**: 0 | **Secrets**: 2

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `cli/src/config.rs:44` (`api_key: "eyJh***REDACTED***".to_string(),`)
- **[HIGH] `ATRUSS-SEC-005`** at `cli/src/config.rs:67` (`api_key: "eyJh***REDACTED***".to_string(),`)

### Inventory Sample
- `anyhow` `1.0.102` (cargo, `cli/Cargo.toml`)
- `clap` `4.6.1` (cargo, `cli/Cargo.toml`)
- `dirs` `7.0.0` (cargo, `cli/Cargo.toml`)
- `futures` `0.3.32` (cargo, `cli/Cargo.toml`)
- `postgrest` `1.6.0` (cargo, `cli/Cargo.toml`)
- `rand` `0.10.1` (cargo, `cli/Cargo.toml`)
- `regex` `1.12.3` (cargo, `cli/Cargo.toml`)
- `reqwest` `0.13.4` (cargo, `cli/Cargo.toml`)
- `rpassword` `7.5.4` (cargo, `cli/Cargo.toml`)
- `serde` `1.0.228` (cargo, `cli/Cargo.toml`)
- `serde_json` `1.0.150` (cargo, `cli/Cargo.toml`)
- `sqlx` `0.8.6` (cargo, `cli/Cargo.toml`)
- `tempfile` `3.27.0` (cargo, `cli/Cargo.toml`)
- `thiserror` `2.0.18` (cargo, `cli/Cargo.toml`)
- `tokio` `1.52.3` (cargo, `cli/Cargo.toml`)
- `toml` `1.1.2` (cargo, `cli/Cargo.toml`)
- `url` `2.5.8` (cargo, `cli/Cargo.toml`)
- `uuid` `1.23.2` (cargo, `cli/Cargo.toml`)
- `@heroicons/react` `2.2.0` (npm, `website/package.json`)
- `@heroicons/react` `2.2.0` (npm, `website/pnpm-lock.yaml`)
- `@hookform/resolvers` `5.2.2` (npm, `website/package.json`)
- `@hookform/resolvers` `5.2.2` (npm, `website/pnpm-lock.yaml`)
- `@radix-ui/react-avatar` `1.1.11` (npm, `website/package.json`)
- `@radix-ui/react-avatar` `1.1.11` (npm, `website/pnpm-lock.yaml`)
- `@radix-ui/react-dialog` `1.1.15` (npm, `website/package.json`)
- `@radix-ui/react-dialog` `1.1.15` (npm, `website/pnpm-lock.yaml`)
- `@radix-ui/react-dropdown-menu` `2.1.16` (npm, `website/package.json`)
- `@radix-ui/react-dropdown-menu` `2.1.16` (npm, `website/pnpm-lock.yaml`)
- `@radix-ui/react-label` `2.1.8` (npm, `website/package.json`)
- `@radix-ui/react-label` `2.1.8` (npm, `website/pnpm-lock.yaml`)
- ... (+1296 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_cli["cli"]
        mod_website["website"]
    end
    subgraph build_artifacts["Build Artifacts / Containers"]
        art_cli_Cargo_toml["cli/Cargo.toml"]
        art_website_coverage_lcov_info["website/coverage/lcov.info"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_cli_yaml_build["cli.yaml#build"]
        job_release_cli_yaml_build_linux["release-cli.yaml#build-linux"]
        job_release_cli_yaml_build_macos["release-cli.yaml#build-macos"]
        job_release_cli_yaml_build_windows["release-cli.yaml#build-windows"]
        job_release_cli_yaml_create_release["release-cli.yaml#create-release"]
        job_update_supabase_js_yml_update_supabase_js["update-supabase-js.yml#update-supabase-js"]
        job_website_tests_yaml_test["website-tests.yaml#test"]
    end
    mod_cli -->|BUILT_BY| job_cli_yaml_build
    mod_cli -->|DEPLOYED_BY| job_release_cli_yaml_build_linux
    mod_cli -->|DEPLOYED_BY| job_release_cli_yaml_build_macos
    mod_cli -->|DEPLOYED_BY| job_release_cli_yaml_build_windows
    mod_cli -->|DEPLOYED_BY| job_release_cli_yaml_create_release
    mod_cli -->|PACKAGED_BY| art_cli_Cargo_toml
    mod_website -->|BUILT_BY| job_update_supabase_js_yml_update_supabase_js
    mod_website -->|BUILT_BY| job_website_tests_yaml_test
    mod_website -->|PACKAGED_BY| art_website_coverage_lcov_info
```

- `cli` (code_module) --[BUILT_BY]--> `cli.yaml#build` (ci_job)
- `cli` (code_module) --[DEPLOYED_BY]--> `release-cli.yaml#build-linux` (ci_job)
- `cli` (code_module) --[DEPLOYED_BY]--> `release-cli.yaml#build-macos` (ci_job)
- `cli` (code_module) --[DEPLOYED_BY]--> `release-cli.yaml#build-windows` (ci_job)
- `cli` (code_module) --[DEPLOYED_BY]--> `release-cli.yaml#create-release` (ci_job)
- `cli` (code_module) --[PACKAGED_BY]--> `cli/Cargo.toml` (container)
- `website` (code_module) --[BUILT_BY]--> `update-supabase-js.yml#update-supabase-js` (ci_job)
- `website` (code_module) --[BUILT_BY]--> `website-tests.yaml#test` (ci_job)
- `website` (code_module) --[PACKAGED_BY]--> `website/coverage/lcov.info` (container)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["supabase/dbdev (10 workflows)"])
  grp_0_CI___Verification["CI & Verification (5 workflows · 5 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Release___Deploy["Release & Deploy (4 workflows · 10 jobs)"]
  pipeline_root --> grp_1_Release___Deploy
  grp_2_Scheduled___Manual["Scheduled & Manual (1 workflows · 1 jobs)"]
  pipeline_root --> grp_2_Scheduled___Manual
```
