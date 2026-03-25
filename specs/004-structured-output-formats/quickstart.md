# Quickstart: Structured Output Generation (Parity Edition)

## Running the Complete Export Pipeline

Atruss Code Atlas has been migrated from generating singular outputs to performing comprehensive, 8-phase architectural extractions across your GitHub organizations spanning CSV, hierarchical JSON, and Mermaid files automatically.

```bash
# Set your token
export GITHUB_TOKEN="ghp_xxx"

# 1. Run Complete Discovery (Phase 1)
# This will automatically create an `exports/YYYY-MM-DD_HH-MM-SS/repos/` directory 
# filled with repositories.csv, repositories.json, and summary.txt.
repo-analyzer discover --org "your-org"

# 2. Run Pipeline Extraction (Phases 2-8)
# Automatically analyzes the outputs from the discovery phase to pull YAML, Runners, Environments 
# and compiles the relationships into the same exports tree under `/reports` 
# outputting pipeline topology in JSON, .md Arc42 docs, and CSV tables natively.
repo-analyzer analyze-pipeline --from-discovery ./exports/latest/repos/repositories.json
```
