# Atruss Code Atlas: Portable Analyzer

A fast, lightweight CLI tool generating portable Docs-as-Code bounds without databases. Performs code coverage mapping, JSON pipeline topological sweeps, and natively generates Arc42 architecture Markdown + Mermaid diagrams automatically.

## Quickstart

```bash
# Clone the repository
git clone https://github.com/organization/atruss-code-atlas.git
cd atruss-code-atlas

# Create environment and install
python -m venv .venv
# or on windows: .\.venv\Scripts\activate
source .venv/bin/activate
pip install -e .

# Discover an organization and export as JSON manifest
repo-analyzer discover --org your-github-org --output org-repos.json

# Analyze pipelines mapping explicitly to local JSON / Markdown targets natively
repo-analyzer analyze-pipeline --from-discovery org-repos.json --output-dir ./reports/

# Alternatively, pass flat text array lists sequentially 
repo-analyzer analyze-pipeline --repos-file targets.txt --output-dir ./reports/

# Deep Code Scan generating architectural AST bindings explicitly 
repo-analyzer analyze-code --repos-file targets.txt --output-dir ./architecture-reports/
```

## Features
- **Classification Engine**: Fast, remote matching checking manifest files vs downloading `git clone` trees. 
- **Pipeline Extractor (DAG)**: Extracts GitHub Actions sequences scaling upstream/downstream maps alongside heuristic anti-pattern checking.
- **Architectural Generation**: Detects Python AST syntax boundaries automatically generating Arc42 compliant Mermaid mapping without local execution. 
