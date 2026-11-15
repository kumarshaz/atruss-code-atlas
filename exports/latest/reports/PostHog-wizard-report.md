---
title: Architecture — PostHog/wizard
description: Arc42 and Pipeline report for PostHog/wizard
---

# Repository Architecture Analysis: PostHog/wizard

## Metadata
- **SHA**: `39e6166812974bff7a02e1ee6a94e786b5c21e2a`
- **Primary Ecosystem**: JavaScript/TypeScript

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 2.17
- **avg_cyclomatic_complexity**: 3.26
- **component_count**: 356
- **dead_code_count**: 9
- **dead_code_symbols**: 9 entry(ies)
- **duplication_pct**: 83.71
- **file_complexities**: 25 entry(ies)
- **files_analyzed**: 1149
- **fitness_passed**: False
- **fitness_violation_count**: 3
- **framework**: Next.js
- **import_edges**: 100 entry(ies)
- **loc**: 178747
- **max_cognitive_complexity**: 218
- **max_cyclomatic_complexity**: 151
- **sloc**: 144689
- **test_file_count**: 424

# Architecture: PostHog/wizard

## Context
- **Repository**: `PostHog/wizard`
- **SHA**: `39e6166812974bff7a02e1ee6a94e786b5c21e2a`
- **Ecosystem**: JavaScript/TypeScript
- **Framework**: Next.js

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
    repo_root(["PostHog/wizard (356 components)"]):::atlasRoot
    dir_0_src["src (287)"]:::atlasCategory
    repo_root --> dir_0_src
    sub_0_0_tui["tui (177)"]:::atlasWorkflow
    dir_0_src --> sub_0_0_tui
    sub_0_1_shared["shared (73)"]:::atlasWorkflow
    dir_0_src --> sub_0_1_shared
    sub_0_2_services["services (18)"]:::atlasWorkflow
    dir_0_src --> sub_0_2_services
    sub_0_more["+2 more submodules (19)"]:::atlasMore
    dir_0_src --> sub_0_more
    dir_1_e2e_tests["e2e-tests (62)"]:::atlasCategory
    repo_root --> dir_1_e2e_tests
    sub_1_0_test_applications["test-applications (61)"]:::atlasWorkflow
    dir_1_e2e_tests --> sub_1_0_test_applications
    sub_1_1__module_root_["(module root) (1)"]:::atlasWorkflow
    dir_1_e2e_tests --> sub_1_1__module_root_
    dir_2___mocks__["__mocks__ (6)"]:::atlasCategory
    repo_root --> dir_2___mocks__
    dir_3__root_["(root) (1)"]:::atlasCategory
    repo_root --> dir_3__root_
    sub_0_0_tui -.->|"1 dep"| sub_0_2_services
```

## Component Details

Showing top 60 representative components out of 356 across 4 module group(s):

- **Module `src`** (287 components — UI_COMPONENT: 271, SERVICE: 15, MODULE: 1)
- **Module `e2e-tests`** (62 components — UI_COMPONENT: 50, MODULE: 11, API_ROUTE: 1)
- **Module `__mocks__`** (6 components — UI_COMPONENT: 6)
- **Module `(root)`** (1 components — MODULE: 1)

- **PhaseVisual** (`src/tui/components/PhaseVisuals.tsx`): UI_COMPONENT (deps: CrateStack, DashboardGrid, DiffCascade, LibraryShelf, MATRIX_FADE, MatrixRain (+2 more))
- **VisualizerTab** (`src/tui/components/PhaseVisuals.tsx`): UI_COMPONENT (deps: CrateStack, DashboardGrid, DiffCascade, LibraryShelf, MATRIX_FADE, MatrixRain (+2 more))
- **FRAMEWORK_REGISTRY** (`src/services/frameworks/registry.ts`): UI_COMPONENT (deps: REACT_NATIVE_AGENT_CONFIG, REACT_ROUTER_AGENT_CONFIG, TANSTACK_ROUTER_AGENT_CONFIG, TANSTACK_START_AGENT_CONFIG)
- **NOT_A_TARGET** (`src/services/detection/decisions/questions.ts`): UI_COMPONENT (deps: DECISIONS_ACCEPT_PROBABILITY, DECISIONS_AGREE_PROBABILITY, FRAMEWORK_CHOICES, NO_FRAMEWORK)
- **PRIMARY_APP** (`src/services/detection/decisions/questions.ts`): UI_COMPONENT (deps: DECISIONS_ACCEPT_PROBABILITY, DECISIONS_AGREE_PROBABILITY, FRAMEWORK_CHOICES, NO_FRAMEWORK)
- **QUESTIONS** (`src/services/detection/decisions/questions.ts`): UI_COMPONENT (deps: DECISIONS_ACCEPT_PROBABILITY, DECISIONS_AGREE_PROBABILITY, FRAMEWORK_CHOICES, NO_FRAMEWORK)
- **SYMBOL_UPLOAD_CLI_FRAMEWORKS** (`src/programs/error-tracking/index.ts`): UI_COMPONENT (deps: BARE_REACT_NATIVE_REASON, FLUTTER_NO_BUILD_TARGET_REASON, SOURCE_MAPS_TARGETS)
- **CrateStack** (`src/tui/components/visualizer/CrateStack.tsx`): UI_COMPONENT (deps: MATRIX_FADE, Panel)
- **DashboardGrid** (`src/tui/components/visualizer/DashboardGrid.tsx`): UI_COMPONENT (deps: MATRIX_FADE, Panel)
- **DiffCascade** (`src/tui/components/visualizer/DiffCascade.tsx`): UI_COMPONENT (deps: MATRIX_FADE, Panel)
- **ExitScreen** (`src/tui/screens/ExitScreen.tsx`): UI_COMPONENT (deps: SessionStore, WizardStore)
- **LibraryShelf** (`src/tui/components/visualizer/LibraryShelf.tsx`): UI_COMPONENT (deps: MATRIX_FADE, Panel)
- **MatrixRain** (`src/tui/components/visualizer/MatrixRain.tsx`): UI_COMPONENT (deps: MATRIX_FADE, Panel)
- **Route** (`e2e-tests/test-applications/react-tanstack-test-app/src/routes/users.route.tsx`): UI_COMPONENT (deps: APIRoute, DEPLOY_URL)
- **Tumblers** (`src/tui/components/visualizer/Tumblers.tsx`): UI_COMPONENT (deps: MATRIX_FADE, Panel)
- **APIRoute** (`e2e-tests/test-applications/react-tanstack-test-app/src/routes/api/users.$id.ts`): UI_COMPONENT (deps: DEPLOY_URL)
- **APIRoute** (`e2e-tests/test-applications/react-tanstack-test-app/src/routes/api/users.ts`): UI_COMPONENT (deps: DEPLOY_URL)
- **REACT_NATIVE_AGENT_CONFIG** (`src/services/frameworks/react-native/react-native-wizard-agent.ts`): UI_COMPONENT (deps: FRAMEWORK_PACKAGES)
- **REACT_ROUTER_AGENT_CONFIG** (`src/services/frameworks/react-router/react-router-wizard-agent.ts`): UI_COMPONENT (deps: FRAMEWORK_PACKAGES)
- **TANSTACK_ROUTER_AGENT_CONFIG** (`src/services/frameworks/tanstack-router/tanstack-router-wizard-agent.ts`): UI_COMPONENT (deps: FRAMEWORK_PACKAGES)
- **TANSTACK_START_AGENT_CONFIG** (`src/services/frameworks/tanstack-start/tanstack-start-wizard-agent.ts`): UI_COMPONENT (deps: FRAMEWORK_PACKAGES)
- **@posthog/wizard** (`package.json`): MODULE
- **AGENTIC_DETECTION_FIRST_ATTEMPT_TIMEOUT_MS** (`src/shared/constants.ts`): UI_COMPONENT
- **AGENTIC_DETECTION_RETRY_TIMEOUT_MS** (`src/shared/constants.ts`): UI_COMPONENT
- **ANALYTICS_HOST_URL** (`src/shared/constants.ts`): UI_COMPONENT
- **ANALYTICS_POSTHOG_PUBLIC_PROJECT_WRITE_KEY** (`src/shared/constants.ts`): UI_COMPONENT
- **ANALYTICS_TEAM_TAG** (`src/shared/constants.ts`): UI_COMPONENT
- **API_api_hello** (`e2e-tests/test-applications/nextjs-pages-router-test-app/src/pages/api/hello.ts`): API_ROUTE
- **AUTOMATABLE_VARIANTS** (`src/programs/error-tracking-upload-source-maps/detect.ts`): UI_COMPONENT
- **AWS_SKILLS_BASE_URL** (`src/shared/constants.ts`): UI_COMPONENT
- **AgentSkillIntroScreen** (`src/tui/programs/shared/screens/AgentSkillIntroScreen.tsx`): UI_COMPONENT
- **AiObservabilityIntroScreen** (`src/tui/programs/ai-observability/screens/AiObservabilityIntroScreen.tsx`): UI_COMPONENT
- **AiOptInDemo** (`src/tui/playground/demos/AiOptInDemo.tsx`): UI_COMPONENT
- **AiOptInRequiredScreen** (`src/tui/screens/AiOptInRequiredScreen.tsx`): UI_COMPONENT
- **App** (`e2e-tests/test-applications/nextjs-pages-router-test-app/src/pages/_app.tsx`): UI_COMPONENT
- **App** (`src/tui/App.tsx`): UI_COMPONENT
- **AreaHeaderRow** (`src/tui/programs/audit/screens/AuditChecksViewer/AreaHeaderRow.tsx`): UI_COMPONENT
- **AskModalDemo** (`src/tui/playground/demos/AskModalDemo.tsx`): UI_COMPONENT
- **AuditAreaPane** (`src/tui/programs/audit/screens/AuditAreaPane.tsx`): UI_COMPONENT
- **AuditChecksDemo** (`src/tui/playground/demos/AuditChecksDemo.tsx`): UI_COMPONENT
- **AuditChecksOutroSection** (`src/tui/programs/audit/screens/AuditChecksOutroSection.tsx`): UI_COMPONENT
- **AuditChecksViewer** (`src/tui/programs/audit/screens/AuditChecksViewer/AuditChecksViewer.tsx`): UI_COMPONENT
- **AuditIntroScreen** (`src/tui/programs/audit/screens/AuditIntroScreen.tsx`): UI_COMPONENT
- **AuditOutroScreen** (`src/tui/programs/audit/screens/AuditOutroScreen.tsx`): UI_COMPONENT
- **AuditRunScreen** (`src/tui/programs/audit/screens/AuditRunScreen.tsx`): UI_COMPONENT
- **AuthErrorScreen** (`src/tui/screens/AuthErrorScreen.tsx`): UI_COMPONENT
- **AuthScreen** (`src/tui/screens/AuthScreen.tsx`): UI_COMPONENT
- **BARE_REACT_NATIVE_REASON** (`src/programs/error-tracking-upload-source-maps/detect-agentic.ts`): UI_COMPONENT
- **BlurTabBarBackground** (`e2e-tests/test-applications/expo-test-app/components/ui/TabBarBackground.ios.tsx`): UI_COMPONENT
- **Box** (`__mocks__/ink.ts`): UI_COMPONENT
- **C** (`src/services/warehouse-sources/__tests__/detect.test.ts`): UI_COMPONENT
- **CONTEXT_MILL_RELEASES_URL** (`src/shared/constants.ts`): UI_COMPONENT
- **CONTEXT_MILL_URL** (`src/shared/constants.ts`): UI_COMPONENT
- **CardLayout** (`src/tui/primitives/CardLayout.tsx`): UI_COMPONENT
- **ChatGptWebMCPClient** (`src/shared/mcp-clients/clients/chatgpt-web.ts`): SERVICE
- **CheckRow** (`src/tui/programs/audit/screens/AuditChecksViewer/CheckRow.tsx`): UI_COMPONENT
- **ClaudeCodeMCPClient** (`src/shared/mcp-clients/clients/claude-code.ts`): SERVICE
- **ClaudeMCPClient** (`src/shared/mcp-clients/clients/claude.ts`): SERVICE
- **ClaudeWebMCPClient** (`src/shared/mcp-clients/clients/claude-web.ts`): SERVICE
- **CodexMCPClient** (`src/shared/mcp-clients/clients/codex.ts`): SERVICE

## 6-Dimension Repository Scorecard

- **Overall Grade**: `F` (48.19/100)
- **Technical Debt Score**: 51.81
- **Estimated Remediation Effort**: 92.94h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `F` | 30.96 | 0.20 | avg_cc=3.26, max_cc=151, duplication=83.71%, dead_code=9 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=6797, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `F` | 37.00 | 0.15 | avg_cognitive=2.17, max_cognitive=218, fitness_violations=3, oversized_files=17 |
| Pipeline Health | `C` | 73.00 | 0.15 | workflows=9, operational_antipatterns=3, parallel_branches=True |
| Security | `F` | 0.00 | 0.20 | vulnerabilities=0, secrets=11, pipeline_security_findings=4 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Architecture Fitness & Workspace Boundaries

- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository duplication_pct (83.71) exceeds policy threshold (15.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cognitive_complexity (218.0) exceeds policy threshold (25.0).
- **[MEDIUM] `ATRUSS-ARCH-005` (COMPLEXITY_THRESHOLD)**: Repository max_cyclomatic_complexity (151.0) exceeds policy threshold (20.0).

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 6797 | **Vulnerabilities**: 0 | **Secrets**: 11

### Secret Findings (Redacted)
- **[HIGH] `ATRUSS-SEC-005`** at `README.md:245` (`WIZARD_CI_GATEWAY_TOKEN_FILE="$HOM***REDACTED***" \`)
- **[HIGH] `ATRUSS-SEC-005`** at `README.md:826` (`WIZARD_CI_GATEWAY_TOKEN_FILE="$HOM***REDACTED***" \`)
- **[HIGH] `ATRUSS-SEC-005`** at `docs/benchmarking.md:69` (`export WIZARD_CI_GATEWAY_TOKEN_FILE="$HOM***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `docs/local-dev.md:35` (`export WIZARD_CI_GATEWAY_TOKEN_FILE="$HOM***REDACTED***"`)
- **[HIGH] `ATRUSS-SEC-005`** at `scripts/smoke-test-ci.sh:19` (`#   export WIZARD_CI_GATEWAY_TOKEN_FILE="$HOM***REDACTED***"`)
- **[CRITICAL] `ATRUSS-SEC-002`** at `src/shared/mcp-clients/__tests__/results.test.ts:70` (`"fatal: could not read from 'https://vincent:ghp_***REDACTED***@github.com/PostHog/ai-plugin.git'",`)
- **[CRITICAL] `ATRUSS-SEC-002`** at `src/shared/mcp-clients/__tests__/results.test.ts:72` (`expect(out).not.toContain('ghp_***REDACTED***');`)
- **[CRITICAL] `ATRUSS-SEC-002`** at `src/shared/mcp-clients/__tests__/results.test.ts:95` (`expect(redactSecrets('remote: token ghp_***REDACTED*** denied')).toBe(`)
- **[CRITICAL] `ATRUSS-SEC-002`** at `src/shared/mcp-clients/__tests__/results.test.ts:99` (`redactSecrets('using gith***REDACTED*** now'),`)
- **[CRITICAL] `ATRUSS-SEC-003`** at `src/shared/mcp-clients/__tests__/results.test.ts:105` (`redactSecrets('OPENAI_API_KEY sk-p***REDACTED*** is invalid'),`)
- **[CRITICAL] `ATRUSS-SEC-003`** at `src/shared/mcp-clients/__tests__/results.test.ts:130` (`redactSecrets('Missing OPENAI_API_KEY=sk-p***REDACTED***'),`)

### Inventory Sample
- `com.android.tools.build:gradle` `*` (Maven, `e2e-tests/test-applications/react-native-test-app/android/build.gradle`)
- `com.facebook.react:hermes-android` `*` (Maven, `e2e-tests/test-applications/react-native-test-app/android/app/build.gradle`)
- `com.facebook.react:react-android` `*` (Maven, `e2e-tests/test-applications/react-native-test-app/android/app/build.gradle`)
- `com.facebook.react:react-native-gradle-plugin` `*` (Maven, `e2e-tests/test-applications/react-native-test-app/android/build.gradle`)
- `org.jetbrains.kotlin:kotlin-gradle-plugin` `*` (Maven, `e2e-tests/test-applications/react-native-test-app/android/build.gradle`)
- `activesupport` `6.1.7.5` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `benchmark` `*` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `bigdecimal` `*` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `cocoapods` `1.13` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `concurrent-ruby` `1.3.4` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `logger` `*` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `mutex_m` `*` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `xcodeproj` `1.26.0` (gem, `e2e-tests/test-applications/react-native-test-app/Gemfile`)
- `@anthropic-ai/claude-agent-sdk` `0.3.169` (npm, `package.json`)
- `@anthropic-ai/claude-agent-sdk` `0.3.169` (npm, `pnpm-lock.yaml`)
- `@babel/core` `7.25.2` (npm, `e2e-tests/test-applications/expo-test-app/package.json`)
- `@babel/core` `7.25.2` (npm, `e2e-tests/test-applications/react-native-test-app/package.json`)
- `@babel/core` `7.28.5` (npm, `e2e-tests/pnpm-lock.yaml`)
- `@babel/core` `7.28.5` (npm, `e2e-tests/test-applications/expo-test-app/package-lock.json`)
- `@babel/core` `7.28.5` (npm, `e2e-tests/test-applications/expo-test-app/pnpm-lock.yaml`)
- `@babel/core` `7.29.0` (npm, `package.json`)
- `@babel/core` `7.29.0` (npm, `pnpm-lock.yaml`)
- `@babel/plugin-transform-modules-commonjs` `7.28.6` (npm, `package.json`)
- `@babel/plugin-transform-modules-commonjs` `7.28.6` (npm, `pnpm-lock.yaml`)
- `@babel/preset-env` `7.25.3` (npm, `e2e-tests/test-applications/react-native-test-app/package.json`)
- `@babel/preset-env` `7.28.5` (npm, `e2e-tests/pnpm-lock.yaml`)
- `@babel/preset-env` `7.29.0` (npm, `package.json`)
- `@babel/preset-env` `7.29.0` (npm, `pnpm-lock.yaml`)
- `@babel/runtime` `7.25.0` (npm, `e2e-tests/test-applications/react-native-test-app/package.json`)
- `@babel/runtime` `7.28.4` (npm, `e2e-tests/pnpm-lock.yaml`)
- ... (+6767 more dependencies)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb
    classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb
    classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb
    classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6
    subgraph code_modules["Code Modules"]
        mod_src["src"]:::atlasCategory
        mod_src_programs["src/programs"]:::atlasCategory
        mod_src_programs_posthog_integration["src/programs/posthog-integration"]:::atlasCategory
        mod_src_services["src/services"]:::atlasCategory
        mod_src_shared["src/shared"]:::atlasCategory
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_build_yml_job_native_command_security["build.yml#job_native_command_security"]:::atlasJob
    end
    mod_src -->|BUILT_BY| job_build_yml_job_native_command_security
    mod_src_programs -->|BUILT_BY| job_build_yml_job_native_command_security
    mod_src_programs_posthog_integration -->|BUILT_BY| job_build_yml_job_native_command_security
    mod_src_services -->|BUILT_BY| job_build_yml_job_native_command_security
    mod_src_shared -->|BUILT_BY| job_build_yml_job_native_command_security
```

- `src` (code_module) --[BUILT_BY]--> `build.yml#job_native_command_security` (ci_job)
- `src/programs` (code_module) --[BUILT_BY]--> `build.yml#job_native_command_security` (ci_job)
- `src/programs/posthog-integration` (code_module) --[BUILT_BY]--> `build.yml#job_native_command_security` (ci_job)
- `src/services` (code_module) --[BUILT_BY]--> `build.yml#job_native_command_security` (ci_job)
- `src/shared` (code_module) --[BUILT_BY]--> `build.yml#job_native_command_security` (ci_job)


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
  pipeline_root(["PostHog/wizard (9 workflows)"]):::atlasRoot
  grp_0_Scheduled___Manual["Scheduled & Manual (4 workflows · 6 jobs)"]:::atlasCategory
  pipeline_root --> grp_0_Scheduled___Manual
  wf_2_MCP_Install["MCP Install (1 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_2_MCP_Install
  job_2_mcp_install["mcp-install"]:::atlasJob
  wf_2_MCP_Install --> job_2_mcp_install
  wf_4_Provisioning_Probe["Provisioning Probe (1 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_4_Provisioning_Probe
  job_4_probe["probe"]:::atlasJob
  wf_4_Provisioning_Probe --> job_4_probe
  wf_7_Smoke_Test["Smoke Test (1 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_7_Smoke_Test
  job_7_smoke_test["smoke-test"]:::atlasJob
  wf_7_Smoke_Test --> job_7_smoke_test
  wf_8_Wizard_CI_Trigger["Wizard CI Trigger (3 jobs)"]:::atlasWorkflow
  grp_0_Scheduled___Manual --> wf_8_Wizard_CI_Trigger
  job_8_post_welcome["post-welcome"]:::atlasJob
  job_8_handle_command["handle-command"]:::atlasJob
  job_8_handle_snapshots_command["handle-snapshots-command"]:::atlasJob
  wf_8_Wizard_CI_Trigger --> job_8_post_welcome
  wf_8_Wizard_CI_Trigger --> job_8_handle_command
  wf_8_Wizard_CI_Trigger --> job_8_handle_snapshots_command
  grp_1_CI___Verification["CI & Verification (2 workflows · 5 jobs)"]:::atlasCategory
  pipeline_root --> grp_1_CI___Verification
  wf_0_Build___Test["Build & Test (4 jobs)"]:::atlasWorkflow
  grp_1_CI___Verification --> wf_0_Build___Test
  job_0_job_build["job_build"]:::atlasJob
  job_0_job_lint["job_lint"]:::atlasJob
  job_0_job_native_command_security["job_native_command_security"]:::atlasJob
  wf_0_Build___Test --> job_0_job_build
  job_0_job_build --> job_0_job_lint
  wf_0_Build___Test --> job_0_job_native_command_security
  wf_3_PR_Conventional_Commit_Validation["PR Conventional Commit Validation (1 jobs)"]:::atlasWorkflow
  grp_1_CI___Verification --> wf_3_PR_Conventional_Commit_Validation
  job_3_validate_pr_title["validate-pr-title"]:::atlasJob
  wf_3_PR_Conventional_Commit_Validation --> job_3_validate_pr_title
  grp_2_Release___Deploy["Release & Deploy (2 workflows · 3 jobs)"]:::atlasCategory
  pipeline_root --> grp_2_Release___Deploy
  wf_5_Publish["Publish (2 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_5_Publish
  job_5_check_package_version["check-package-version"]:::atlasJob
  job_5_release["release"]:::atlasJob
  wf_5_Publish --> job_5_check_package_version
  job_5_check_package_version --> job_5_release
  wf_6_release_please["release-please (1 jobs)"]:::atlasWorkflow
  grp_2_Release___Deploy --> wf_6_release_please
  job_6_release_please["release-please"]:::atlasJob
  wf_6_release_please --> job_6_release_please
  grp_3_Automation___Other["Automation & Other (1 workflows · 1 jobs)"]:::atlasCategory
  pipeline_root --> grp_3_Automation___Other
  wf_1_Notify_Slack_for_wizard_issues["Notify Slack for wizard issues (1 jobs)"]:::atlasWorkflow
  grp_3_Automation___Other --> wf_1_Notify_Slack_for_wizard_issues
  job_1_notify["notify"]:::atlasJob
  wf_1_Notify_Slack_for_wizard_issues --> job_1_notify
```
