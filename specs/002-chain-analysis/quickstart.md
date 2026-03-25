# Quickstart: Chained Analysis

This guide walks through leveraging the chained CLI pipeline for bulk organization scanning.

### 1. Discover Repositories

Generate the manifest representing all repositories in the bounds of the GitHub organization.

```bash
repo-analyzer discover --org my-org --output discovery.json
```

*(You can also use `--format json > discovery.json`)*

### 2. Run Massive Code Scans

Pass the generated JSON manifest directly into the code architectures analyzer. The tool will handle cloning the repositories temporarily and aggregating the Arc42 markdown outputs into `./reports/`.

```bash
repo-analyzer analyze-code --from-discovery discovery.json --output-dir ./reports/
```

### 3. Analyze Pipeline DAGs

Pass the same manifest into the pipeline analyzer to generate anti-pattern warnings and DAG workflows for the CI/CD footprints of every repo.

```bash
repo-analyzer analyze-pipeline --from-discovery discovery.json --output-dir ./pipeline_reports/
```
