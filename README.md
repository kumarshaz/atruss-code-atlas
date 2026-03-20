# Atruss Code Atlas: Repository Analyzer

A fast, heuristic-based CLI tool to discover repositories, analyze CI/CD pipelines, extract code coverage, and generate Arc42 architecture Markdown + Mermaid diagrams automatically.

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

# Discover an organization
repo-analyzer discover --org your-github-org

# Analyze pipelines in a local directory matching anti-patterns
repo-analyzer analyze-pipeline --repo ./my-local-project

# Extract test coverage percentages from CI logs
repo-analyzer analyze-coverage --report path/to/pytest-cov.xml

# Deep Code Scan (Python AST) Architecture Extraction
repo-analyzer analyze-code --path ./my-python-api --output-dir ./reports/
```

## Features
- **Classification Engine**: Fast, remote matching checking manifest files vs downloading `git clone` trees. 
- **Pipeline Extractor (DAG)**: Extracts GitHub Actions sequences scaling upstream/downstream maps alongside heuristic anti-pattern checking.
- **Architectural Generation**: Detects Python AST syntax boundaries automatically generating Arc42 compliant Mermaid mapping without local execution. 
