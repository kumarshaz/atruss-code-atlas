---
title: Architecture — getsentry/sentry-php
description: Arc42 and Pipeline report for getsentry/sentry-php
---

# Repository Architecture Analysis: getsentry/sentry-php

## Metadata
- **SHA**: `f55afd0b9e64be39621d42e820d2b50284785c2b`
- **Primary Ecosystem**: PHP

## Quality Metrics
- **ast_engine**: tree-sitter
- **avg_cognitive_complexity**: 0.0
- **avg_cyclomatic_complexity**: 1.0
- **component_count**: 251
- **dead_code_count**: 0
- **dead_code_symbols**: 0 entry(ies)
- **duplication_pct**: 0.13
- **file_complexities**: 1 entry(ies)
- **files_analyzed**: 310
- **fitness_passed**: True
- **fitness_violation_count**: 0
- **framework**: Symfony
- **import_edges**: 3 entry(ies)
- **loc**: 57678
- **max_cognitive_complexity**: 0
- **max_cyclomatic_complexity**: 1
- **sloc**: 38775
- **test_file_count**: 180

# Architecture: getsentry/sentry-php

## Context
- **Repository**: `getsentry/sentry-php`
- **SHA**: `f55afd0b9e64be39621d42e820d2b50284785c2b`
- **Ecosystem**: PHP
- **Framework**: Symfony

## Building Block View

```mermaid
graph TD;
    repo_root(["getsentry/sentry-php (251 components)"])
    dir_0_src["src (174)"]
    repo_root --> dir_0_src
    sub_0_0__module_root_["(module root) (28)"]
    dir_0_src --> sub_0_0__module_root_
    sub_0_1_Serializer["Serializer (20)"]
    dir_0_src --> sub_0_1_Serializer
    sub_0_2_DataCollection["DataCollection (18)"]
    dir_0_src --> sub_0_2_DataCollection
    sub_0_more["+19 more submodules (108)"]
    dir_0_src --> sub_0_more
    dir_1_tests["tests (74)"]
    repo_root --> dir_1_tests
    sub_1_0__module_root_["(module root) (29)"]
    dir_1_tests --> sub_1_0__module_root_
    sub_1_1_DataCollection["DataCollection (14)"]
    dir_1_tests --> sub_1_1_DataCollection
    sub_1_2_Integration["Integration (9)"]
    dir_1_tests --> sub_1_2_Integration
    sub_1_more["+6 more submodules (22)"]
    dir_1_tests --> sub_1_more
    dir_2__root_["(root) (1)"]
    repo_root --> dir_2__root_
    dir_3_decision_model_linter["decision-model-linter (1)"]
    repo_root --> dir_3_decision_model_linter
    dir_4_stubs["stubs (1)"]
    repo_root --> dir_4_stubs
```

## Component Details

Showing top 60 representative components out of 251 across 5 module group(s):

- **Module `src`** (174 components — module: 174)
- **Module `tests`** (74 components — module: 74)
- **Module `(root)`** (1 components — module: 1)
- **Module `decision-model-linter`** (1 components — MODULE: 1)
- **Module `stubs`** (1 components — module: 1)

- **.php-cs-fixer.dist** (`.php-cs-fixer.dist.php`): module
- **AbstractErrorListenerIntegration** (`src/Integration/AbstractErrorListenerIntegration.php`): module
- **AbstractSerializer** (`src/Serializer/AbstractSerializer.php`): module
- **AgentClient** (`src/Agent/Transport/AgentClient.php`): module
- **AgentClientBuilder** (`src/Agent/Transport/AgentClientBuilder.php`): module
- **AgentClientBuilderTest** (`tests/HttpClient/AgentClientBuilderTest.php`): module
- **AgentClientTest** (`tests/HttpClient/AgentClientTest.php`): module
- **Arr** (`src/Util/Arr.php`): module
- **Attachment** (`src/Attachment/Attachment.php`): module
- **AttachmentItem** (`src/Serializer/EnvelopItems/AttachmentItem.php`): module
- **AttachmentTest** (`tests/Attachment/AttachmentTest.php`): module
- **Attribute** (`src/Attributes/Attribute.php`): module
- **AttributeBag** (`src/Attributes/AttributeBag.php`): module
- **AttributeBagTest** (`tests/Attributes/AttributeBagTest.php`): module
- **AttributeTest** (`tests/Attributes/AttributeTest.php`): module
- **Breadcrumb** (`src/Breadcrumb.php`): module
- **BreadcrumbHandler** (`src/Monolog/BreadcrumbHandler.php`): module
- **BreadcrumbSeralizerTrait** (`src/Serializer/Traits/BreadcrumbSeralizerTrait.php`): module
- **BreadcrumbTest** (`tests/BreadcrumbTest.php`): module
- **BrokenClass** (`tests/Fixtures/code/BrokenClass.php`): module
- **ByteAttachment** (`src/Attachment/ByteAttachment.php`): module
- **CheckIn** (`src/CheckIn.php`): module
- **CheckInItem** (`src/Serializer/EnvelopItems/CheckInItem.php`): module
- **CheckInStatus** (`src/CheckInStatus.php`): module
- **CheckInTest** (`tests/CheckInTest.php`): module
- **Client** (`src/Client.php`): module
- **ClientBuilder** (`src/ClientBuilder.php`): module
- **ClientBuilderTest** (`tests/ClientBuilderTest.php`): module
- **ClientInterface** (`src/ClientInterface.php`): module
- **ClientReportAggregator** (`src/ClientReport/ClientReportAggregator.php`): module
- **ClientReportAggregatorTest** (`tests/ClientReport/ClientReportAggregatorTest.php`): module
- **ClientReportAssertions** (`tests/ClientReport/ClientReportAssertions.php`): module
- **ClientReportItem** (`src/Serializer/EnvelopItems/ClientReportItem.php`): module
- **ClientTest** (`tests/ClientTest.php`): module
- **CodeLocationResolver** (`src/Util/CodeLocationResolver.php`): module
- **CodeLocationResolverTest** (`tests/CodeLocationResolverTest.php`): module
- **CompatibilityLogLevelTrait** (`src/Monolog/CompatibilityLogLevelTrait.php`): module
- **CompatibilityProcessingHandlerTrait** (`src/Monolog/CompatibilityProcessingHandlerTrait.php`): module
- **ContinuousProfiler** (`src/Profiling/ContinuousProfiler.php`): module
- **CounterMetric** (`src/Metrics/Types/CounterMetric.php`): module
- **DataCategory** (`src/Transport/DataCategory.php`): module
- **DataCollectionOptions** (`src/DataCollection/DataCollectionOptions.php`): module
- **DataCollectionOptionsTest** (`tests/DataCollection/DataCollectionOptionsTest.php`): module
- **DataCollectionPolicy** (`src/DataCollection/DataCollectionPolicy.php`): module
- **DataCollectionPolicyTest** (`tests/DataCollection/DataCollectionPolicyTest.php`): module
- **DatabaseDataCollector** (`src/DataCollection/DatabaseDataCollector.php`): module
- **DatabaseDataCollectorTest** (`tests/DataCollection/DatabaseDataCollectorTest.php`): module
- **DebugFileLogger** (`src/Logger/DebugFileLogger.php`): module
- **DebugLogger** (`src/Logger/DebugLogger.php`): module
- **DebugStdOutLogger** (`src/Logger/DebugStdOutLogger.php`): module
- **DiscardedEvent** (`src/ClientReport/DiscardedEvent.php`): module
- **DistributionMetric** (`src/Metrics/Types/DistributionMetric.php`): module
- **Dsn** (`src/Dsn.php`): module
- **DsnTest** (`tests/DsnTest.php`): module
- **DynamicSamplingContext** (`src/Tracing/DynamicSamplingContext.php`): module
- **EnvelopeItemInterface** (`src/Serializer/EnvelopItems/EnvelopeItemInterface.php`): module
- **EnvironmentIntegration** (`src/Integration/EnvironmentIntegration.php`): module
- **EnvironmentIntegrationTest** (`tests/Integration/EnvironmentIntegrationTest.php`): module
- **ErrorHandler** (`src/ErrorHandler.php`): module
- **ErrorListenerIntegration** (`src/Integration/ErrorListenerIntegration.php`): module

## 6-Dimension Repository Scorecard

- **Overall Grade**: `C` (77.41/100)
- **Technical Debt Score**: 22.59
- **Estimated Remediation Effort**: 19.17h

| Dimension | Grade | Score | Weight | Details |
| :--- | :---: | :---: | :---: | :--- |
| Code Quality | `A` | 99.81 | 0.20 | avg_cc=1.00, max_cc=1, duplication=0.13%, dead_code=0 |
| Dependency Health | `A` | 100.00 | 0.15 | dependencies=22, outdated=0, vulnerable=0, has_lockfile=True |
| Maintainability | `A` | 100.00 | 0.15 | avg_cognitive=0.00, max_cognitive=0, fitness_violations=0, oversized_files=0 |
| Pipeline Health | `F` | 49.00 | 0.15 | workflows=6, operational_antipatterns=12, parallel_branches=True |
| Security | `F` | 48.00 | 0.20 | vulnerabilities=0, secrets=0, pipeline_security_findings=3 |
| Test Coverage | `C` | 70.00 | 0.15 | coverage=unavailable, ci_test_job=True, test_files_detected=True |

## Supply Chain Dependencies, Vulnerabilities & Secrets

- **Dependencies Parsed**: 22 | **Vulnerabilities**: 0 | **Secrets**: 0

### Inventory Sample
- `guzzlehttp/psr7` `*` (composer, `composer.json`)
- `jean85/pretty-package-versions` `*` (composer, `composer.json`)
- `psr/log` `*` (composer, `composer.json`)
- `symfony/options-resolver` `*` (composer, `composer.json`)
- `@sentry/decision-model-linter` `0.3.0` (npm, `decision-model-linter/package-lock.json`)
- `@sentry/decision-model-linter` `0.3.0` (npm, `decision-model-linter/package.json`)
- `carthage-software/mago` `1.30.0` (composer, `composer.json`)
- `friendsofphp/php-cs-fixer` `3.4` (composer, `composer.json`)
- `guzzlehttp/guzzle` `*` (composer, `composer.json`)
- `guzzlehttp/promises` `*` (composer, `composer.json`)
- `monolog/monolog` `*` (composer, `composer.json`)
- `nyholm/psr7` `1.8` (composer, `composer.json`)
- `open-telemetry/api` `1.1` (composer, `composer.json`)
- `open-telemetry/context` `1.1` (composer, `composer.json`)
- `open-telemetry/exporter-otlp` `1.1` (composer, `composer.json`)
- `open-telemetry/gen-otlp-protobuf` `1.2.1` (composer, `composer.json`)
- `open-telemetry/sdk` `1.1` (composer, `composer.json`)
- `open-telemetry/sem-conv` `1.27` (composer, `composer.json`)
- `phpstan/phpstan` `2.2` (composer, `composer.json`)
- `phpunit/phpunit` `*` (composer, `composer.json`)
- `spiral/roadrunner-http` `3.6` (composer, `composer.json`)
- `spiral/roadrunner-worker` `3.6` (composer, `composer.json`)

## Section 7: Code-to-Cloud Deployment Traceability

```mermaid
flowchart LR
    subgraph code_modules["Code Modules"]
        mod_decision_model_linter["decision-model-linter"]
    end
    subgraph ci_jobs["CI/CD Jobs"]
        job_decision_model_lint_yml_lint["decision-model-lint.yml#lint"]
    end
    mod_decision_model_linter -->|BUILT_BY| job_decision_model_lint_yml_lint
```

- `decision-model-linter` (code_module) --[BUILT_BY]--> `decision-model-lint.yml#lint` (ci_job)


## CI/CD Pipeline Topology

```mermaid
graph TD;
  pipeline_root(["getsentry/sentry-php (6 workflows)"])
  grp_0_CI___Verification["CI & Verification (5 workflows · 10 jobs)"]
  pipeline_root --> grp_0_CI___Verification
  grp_1_Release___Deploy["Release & Deploy (1 workflows · 1 jobs)"]
  pipeline_root --> grp_1_Release___Deploy
```
