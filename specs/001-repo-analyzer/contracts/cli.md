# Interface Contract: CLI

The system provides a command-line interface as its primary UX.

## Commands

### `discover`
Scans an organization for repositories and outputs classification.
```bash
repo-analyzer discover --org <github_org> [--token <pat>] --format [table|json]
```
**Output**: A list of repositories with their detected ecosystem.

### `analyze-pipeline`
Analyzes CI/CD pipelines for a targeted remote or local repository.
```bash
repo-analyzer analyze-pipeline --repo <org/repo_name> [--output-dir <path>]
```
**Output**: Generates a DAG visualization SVG and JSON finding report concerning pipeline anti-patterns.

### `analyze-code`
Performs a deep architectural analysis of a local codebase.
```bash
repo-analyzer analyze-code --path <local_directory> --output-dir <path>
```
**Output**: Generates Arc42 markdown documentation with embedded Mermaid diagrams.
