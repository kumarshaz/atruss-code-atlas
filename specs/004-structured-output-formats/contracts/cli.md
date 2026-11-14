# CLI Contracts

## Global Orchestration

The `repo-analyzer` CLI command interface replaces the older single-file outputs with an overarching pipeline model.

### 1. `discover` Configuration
```bash
repo-analyzer discover \
  --org {name} \
  --token {github_pat} \
  --output-path {dir} \
  --log-path {dir} \
  --include-archived \
  --max-concurrent {int} \
  --exclude-repo-names "{list}" \
  --exclude-repo-patterns "{regex}" \
  --dry-run
```
**Side Effects**:
- Connects to GitHub API (validates via `/orgs/{org}`).
- Iterates paginated lists of repos.
- Emits hierarchical `exports/{timestamp}/repos/repositories.json`, `repositories.csv`, `repositories.yaml`.

### 2. `analyze-pipeline` Configuration
```bash
repo-analyzer analyze-pipeline \
  --from-discovery {exports_dir_or_json} \
  --output-dir {dir}
```
**Side Effects**:
- Assumes the 8-phase pipeline progression logic internally mapping relationships.
- Iterates over workloads from phase 1 to run pipelines, runners, and environments phases.
- Emits topological hierarchy under `exports/{timestamp}/relationships/` and `/reports/` automatically retaining `csv`, `json`, and `.md` copies identically.
