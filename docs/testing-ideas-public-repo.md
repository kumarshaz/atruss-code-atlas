## 1. Testing Scope & Objectives

**Objective:** Validate classification, analysis, and pipeline visualization of Atruss Code Atlas using only public GitHub repositories and GitHub Actions workflows across:

- Python  
- .NET  
- React/TypeScript/JavaScript  
- Java with Spring Boot  

All tests consume repos at pinned SHAs to keep expectations stable.

***

## 2. Fixture Repository Catalog

### 2.1 Python Fixtures

1. **Python benchmark with pytest & Actions**  
   - Repo: `benchmark-action/github-action-benchmark` [github](https://github.com/benchmark-action/github-action-benchmark/actions?query=workflow%3A%22Python+Example+with+pytest%22)
   - URL: https://github.com/benchmark-action/github-action-benchmark  
   - Purpose: Contains example workflows “Python Example with pytest” and benchmark workflows; used to validate pytest discovery, matrix, and pipeline DAG.  

2. **Pytest parallelization pattern**  
   - Article: “How to run pytest in parallel on GitHub actions” [guicommits](https://guicommits.com/parallelize-pytest-tests-github-actions/)
   - URL: https://github.com/guicommits/ (use the sample repo referenced in article) [guicommits](https://guicommits.com/parallelize-pytest-tests-github-actions/)
   - Purpose: Validate matrix/parallel strategy detection and pipeline branching.  

3. **GitHub official Python CI pattern**  
   - Docs: “Building and testing Python” in GitHub Actions docs [docs.github](https://docs.github.com/en/actions/tutorials/build-and-test-code)
   - URL: https://docs.github.com/en/actions/tutorials/build-and-test-code  
   - Purpose: Use example workflow content as canonical pattern for Python build+test.

### 2.2 .NET Fixtures

1. **Official .NET test workflow**  
   - Docs: “Create a test validation GitHub workflow - .NET” [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)
   - URL: https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action  
   - Sample YAML includes matrix across `ubuntu-latest`, `windows-latest`, `macOS-latest` and `dotnet test`. [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)

2. **Sample .NET 8 build-and-test pipeline**  
   - Gist: Sample GitHub Action for .NET 8 [gist.github](https://gist.github.com/guibranco/bb7952adc79b2a37ad4db489e394a2d0)
   - URL: https://gist.github.com/guibranco/bb7952adc79b2a37ad4db489e394a2d0  
   - Purpose: Validate multi-step build+test pipeline, caching, and OS matrix.  

3. **Community repo with Actions-based tests**  
   - Example: Use open-source .NET repos that rely on GitHub Actions for CI (various OSS libraries; you’ll pin specific SHAs).  

### 2.3 React / TypeScript / JavaScript Fixtures

1. **Example GitHub Action in TypeScript**  
   - Repo: `jeffrafter/example-github-action-typescript` [github](https://github.com/jeffrafter/example-github-action-typescript)
   - URL: https://github.com/jeffrafter/example-github-action-typescript  
   - Purpose: TypeScript project with compiled action, tests, and Actions workflow; validates JS/TS classification, Jest test jobs, and pipeline structure. [github](https://github.com/jeffrafter/example-github-action-typescript)

2. **TypeScript Jest coverage with GitHub Actions**  
   - Article: “Measuring Typescript Code Coverage with Jest and GitHub Actions” [about.codecov](https://about.codecov.io/blog/measuring-typescript-code-coverage-with-jest-and-github-actions/)
   - URL: https://github.com/codecov/example-typescript-jest (referenced pattern) [about.codecov](https://about.codecov.io/blog/measuring-typescript-code-coverage-with-jest-and-github-actions/)
   - Purpose: Validate detection of Jest, coverage collection, and coverage upload steps.  

3. **Unit testing TypeScript Actions**  
   - Article: “Write Unit Test for your Typescript GitHub Action” [dev](https://dev.to/balastrong/write-unit-test-for-your-typescript-github-action-503p)
   - URL: uses example repo from the article; to be pinned at a specific SHA. [dev](https://dev.to/balastrong/write-unit-test-for-your-typescript-github-action-503p)

### 2.4 Java / Spring Boot Fixtures

1. **Spring Boot testing patterns**  
   - Repo: `hamvocke/spring-testing` [github](https://github.com/hamvocke/spring-testing)
   - URL: https://github.com/hamvocke/spring-testing  
   - Purpose: Spring Boot app with multiple test styles; used for framework detection and test layering. [github](https://github.com/hamvocke/spring-testing)

2. **Spring Boot test examples with GitHub Actions**  
   - Repo: `knowledgefactory4u/spring-boot-test-examples` [github](https://github.com/knowledgefactory4u/spring-boot-test-examples/actions)
   - URL: https://github.com/knowledgefactory4u/spring-boot-test-examples  
   - Actions: https://github.com/knowledgefactory4u/spring-boot-test-examples/actions [github](https://github.com/knowledgefactory4u/spring-boot-test-examples/actions)
   - Purpose: Validate Spring Boot + Maven tests and pipeline extraction.  

3. **Spring Boot CI/CD with GitHub Actions**  
   - Article: “Deploy a SpringBoot application using GitHub Actions” [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)
   - URL (example repo in article): as referenced in the tutorial [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)
   - Purpose: Validate build+test+deploy pipeline, caching, and DB services.

***

## 3. Test Requirement Matrix

### 3.1 Classification & Discovery Tests

**TR‑CLS‑001 (Python Classification)**  
- **Given**: `benchmark-action/github-action-benchmark` at pinned SHA [github](https://github.com/benchmark-action/github-action-benchmark/actions?query=workflow%3A%22Python+Example+with+pytest%22)
- **Expect**:  
  - Ecosystem = `python`  
  - Test tool = `pytest` detected from workflow and/or project files.  
  - Workflow jobs that run pytest labeled `type = test`.  

**TR‑CLS‑002 (.NET Classification)**  
- **Given**: Any public .NET repo that uses the Microsoft sample workflow pattern [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)
- **Expect**:  
  - Ecosystem = `.net`  
  - Presence of `dotnet test` step recognized as `.NET test` job.  

**TR‑CLS‑003 (React/TS Classification)**  
- **Given**: `jeffrafter/example-github-action-typescript` [github](https://github.com/jeffrafter/example-github-action-typescript)
- **Expect**:  
  - Ecosystem = `react_ts_js` or equivalent JS/TS classification.  
  - Framework = `typescript` (and `github-action` if you sub-classify).  
  - Jest test job recognized from workflow. [github](https://github.com/jeffrafter/example-github-action-typescript)

**TR‑CLS‑004 (Spring Boot Classification)**  
- **Given**: `hamvocke/spring-testing` [github](https://github.com/hamvocke/spring-testing)
- **Expect**:  
  - Ecosystem = `java_springboot`.  
  - Framework = `spring-boot`.  
  - Test sources correctly detected at `src/test/java`. [github](https://github.com/hamvocke/spring-testing)

***

### 3.2 Code Analysis & Coverage Tests

**TR‑ANA‑PY‑001 (Python Coverage Extraction)**  
- **Given**: Python fixture with Actions using pytest and coverage reports from `benchmark-action/github-action-benchmark` [github](https://github.com/benchmark-action/github-action-benchmark/actions?query=workflow%3A%22Python+Example+with+pytest%22)
- **Expect**:  
  - CodeLens coverage% within ±2% of coverage reported in the workflow run artifacts.  

**TR‑ANA‑DOTNET‑001 (.NET Test & Coverage)**  
- **Given**: .NET repo using “build and test” workflow from Microsoft docs [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)
- **Expect**:  
  - CodeLens identifies a single `build-and-test` job with `dotnet test`.  
  - Test count and status reflect the workflow outcome (success/failure). [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)

**TR‑ANA‑TS‑001 (Jest Coverage with Actions)**  
- **Given**: Example TS Jest repo with Codecov integration as in Codecov tutorial [about.codecov](https://about.codecov.io/blog/measuring-typescript-code-coverage-with-jest-and-github-actions/)
- **Expect**:  
  - Jest recognized as test runner.  
  - Coverage% extracted and matches coverage summary within tolerance. [about.codecov](https://about.codecov.io/blog/measuring-typescript-code-coverage-with-jest-and-github-actions/)

**TR‑ANA‑JAVA‑001 (Spring Boot Test Layers)**  
- **Given**: `hamvocke/spring-testing` [github](https://github.com/hamvocke/spring-testing)
- **Expect**:  
  - Multi-layer tests (unit, slice, integration) recognized as distinct test sets (at least counted).  
  - Total test classes reflect reality (±1 tolerance). [github](https://github.com/hamvocke/spring-testing)

***

### 3.3 Pipeline DAG & Anti-Pattern Tests

**TR‑DAG‑GEN‑001 (Basic DAG Reconstruction)**  
- **Given**: A simple build+test workflow from GitHub docs (e.g., Python or Node section) [docs.github](https://docs.github.com/en/actions/tutorials/build-and-test-code)
- **Expect**:  
  - DAG with correct number of jobs (1) and no edges.  
  - Triggers match `on:` configuration. [docs.github](https://docs.github.com/en/actions/tutorials/build-and-test-code)

**TR‑DAG‑MAT‑001 (.NET OS Matrix)**  
- **Given**: Sample workflow from Microsoft docs with matrix over `ubuntu-latest`, `windows-latest`, `macOS-latest` [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)
- **Expect**:  
  - DAG has one logical job with 3 matrix instances or 3 nodes depending on your representation.  
  - All nodes share same logical job name, distinct `runner` metadata. [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/devops/dotnet-test-github-action)

**TR‑DAG‑PAR‑PY‑001 (Parallel pytest)**  
- **Given**: Repo patterned after GuiCommits’ “parallelize pytest on GitHub Actions” [guicommits](https://guicommits.com/parallelize-pytest-tests-github-actions/)
- **Expect**:  
  - DAG includes parallel jobs for test partitions or matrix entries.  
  - Pipeline classification: `has_parallelism = true`. [guicommits](https://guicommits.com/parallelize-pytest-tests-github-actions/)

**TR‑DAG‑TS‑001 (Separate lint/test/build Jobs)**  
- **Given**: React/TS fixture with separate `lint`, `test`, `build` jobs, as common JS/TS practice [dev](https://dev.to/balastrong/write-unit-test-for-your-typescript-github-action-503p)
- **Expect**:  
  - DAG shows branching from checkout to `lint`/`test`/`build`.  
  - All three jobs identified with correct type tags. [dev](https://dev.to/balastrong/write-unit-test-for-your-typescript-github-action-503p)

**TR‑DAG‑SPRING‑001 (Spring Boot Build/Test/Deploy)**  
- **Given**: Spring Boot pipeline from Teco tutorial [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)
- **Expect**:  
  - DAG sequence: build → test → (optionally) deploy.  
  - Caching steps detected; DB service usage recognized as pipeline service. [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)

**TR‑DAG‑ANTI‑001 (No Test Gate Before Deploy)**  
- **Given**: A public workflow where deploy job has no `needs:` chain back to any test job (you may fork a template and host it as public)  
- **Expect**:  
  - Anti-pattern “no test gate before deploy” flagged at HIGH severity in report.  

**TR‑DAG‑ANTI‑002 (No Dependency Caching)**  
- **Given**: Workflow that installs dependencies but does not use `actions/cache` [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)
- **Expect**:  
  - Anti-pattern “no dependency caching” flagged. [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)

***

### 3.4 Performance & Scale Tests

**TR‑PERF‑001 (Medium Python Repo)**  
- **Given**: Medium-sized Python repo with Actions tests (e.g., a popular library using pytest; public) [guicommits](https://guicommits.com/parallelize-pytest-tests-github-actions/)
- **Expect**:  
  - CodeLens analysis completes in < 3 minutes.  

**TR‑PERF‑002 (Medium Spring Boot Repo)**  
- **Given**: Medium-sized Spring Boot project with CI (public OSS; pinned SHA, like a mid-sized sample from Maven central ecosystem) [blog.tericcabrel](https://blog.tericcabrel.com/springboot-github-actions-ci-cd/)
- **Expect**:  
  - Analysis completes in < 3 minutes.  

**TR‑PERF‑003 (Mixed Ecosystem Monorepo)**  
- **Given**: Public monorepo combining backend and frontend (e.g., Java + React or .NET + React). [youtube](https://www.youtube.com/watch?v=5PdEmeopJVQ)
- **Expect**:  
  - Multiple modules classified correctly.  
  - Overall report and per-module reports produced within combined SLA.

***

### 3.5 Regression & Contract Tests

**TR‑CON‑001 (Schema Stability)**  
- **Given**: Any fixture repo at pinned SHA  
- **Expect**:  
  - Generated JSON report conforms to CodeLens Report Schema v1 on every run (JSON Schema validation).  

**TR‑CON‑002 (Golden Snapshot for Pipelines)**  
- **Given**: `.github/workflows` from each fixture repo  
- **Expect**:  
  - DAG JSON equals stored golden file (ignoring timestamps and run IDs).  
  - Differences trigger regression alerts.  

**TR‑CON‑003 (Fixture Drift Monitoring)**  
- **Given**: Latest default branch HEAD for each fixture repo (non-pinned) [github](https://github.com/knowledgefactory4u/spring-boot-test-examples/actions)
- **Expect**:  
  - Periodic job compares new outputs to pinned expectations.  
  - On structural drift, mark fixture as needing review but do not fail main contract suite.

***

## 4. Your Own CI for This Testing Spec

Create a `tests.yml` workflow in your CodeLens repo with jobs:

- `unit-tests` — pure code-level tests for classification and parsing.  
- `integration-python`, `integration-dotnet`, `integration-js`, `integration-java` — run analysis against the pinned fixture repos above (via shallow clone).  
- `golden-report` — compare JSON outputs and DAGs against golden snapshots.  
- `performance-smoke` — run selected PERF tests nightly.  

Use matrix strategies for multiple runtimes (Python/Node versions, etc.), following patterns in GitHub and Microsoft docs. [docs.github](https://docs.github.com/en/actions/tutorials/build-and-test-code)
