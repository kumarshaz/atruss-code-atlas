# Atruss Code Atlas: Portable Analyzer

**Passive, offline-capable architectural and pipeline observability.**

Atruss Code Atlas is a fast, lightweight CLI tool generating portable Docs-as-Code boundaries without active instrumentation. It bridges **Structural Architecture** with **Pipeline Topology** and outputs it as an **immutable, portable artifact** (JSON + Markdown/Mermaid).

## The Value Proposition
Enterprises suffer from architectural drift and pipeline fragmentation. Developers are acting as "Master Blacksmiths," hand-crafting CI/CD workflows and hiding domain logic in undocumented repositories. 

Atruss Code Atlas tells you exactly *what* is being built (structural architecture) and *how* it gets to production (pipeline topology) without requiring a single agent or webhook.

### The Market Gap
* **Unlike SonarQube**, which is blind to CI/CD pipelines, we understand the GitHub Actions DAG and detect pipeline anti-patterns.
* **Unlike GitHub Advanced Security (GHAS)**, which locks your data in the UI, we output deterministic, offline Arc42 Markdown documentation.
* **Unlike Spotify Backstage**, which requires heavy active integration, we are *passive*—we ingest, analyze, and report locally without altering the target repo.
* **Unlike Datadog CI Visibility**, which lacks architectural context, we map your CI topology directly to Python/React/C# AST configurations.

## Quickstart

```bash
# Clone the repository
git clone https://github.com/organization/atruss-code-atlas.git
cd atruss-code-atlas

# Create environment and install
python -m venv .venv
source .venv/bin/activate
pip install -e .

PS C:\learnCoding\localrepo\atruss-code-atlas> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
PS C:\learnCoding\localrepo\atruss-code-atlas> .\.venv\Scripts\Activate.ps1  

### 1. Perform Multi-Phase Structural Extraction (CSV, JSON, YAML)

The newest version aggressively replaces legacy table extractions with massive off-line structural dumps securely targeting `exports/{timestamp}` bindings mapping explicitly to ADO parity schemas allowing Astro to ingest the data natively.

```bash
export GH_TOKEN="ghp_xxx"

# Discover repositories natively building dynamic structural columns
repo-analyzer discover --org your-org

# Crawl the output building Pipeline Relationship Graphs (Mermaid + Arrays)
repo-analyzer analyze-pipeline --from-discovery ./exports/latest/repos/repositories.json
```

# Alternatively, pass flat text array lists sequentially 
repo-analyzer analyze-pipeline --repos-file targets.txt --output-dir ./reports/

# Deep Code Scan generating architectural AST bindings explicitly 
repo-analyzer analyze-code --repos-file targets.txt --output-dir ./architecture-reports/
```

## Core Architecture (Hexagonal / Ports & Adapters)

To ensure the Python engine remains a rigid skeleton that can support future expansions (like an Astro-based UI), the system enforces strict boundaries:
* **Core Domain (The "Lego" Logic):** The immutable rules of classification. Handles AST parsing, DAG reconstruction, and pipeline anti-pattern detection. Has zero knowledge of external UI.
* **Inbound Ports (Interfaces):**
  * `CLIAdapter`: For local developer execution and CI/CD runner integration.
* **Outbound Adapters (The "Modular Joints"):**
  * `GitHubRESTClient`: Fetches the raw state.
  * `JSONExporter` / `MarkdownExporter`: Generates the deterministic canonical output and the Arc42/Mermaid files.

## The Astro Visualizer Architecture (Docs-as-Code)

Atruss Code Atlas is completely Astro-ready. The Markdown output is entirely self-contained so it can be ingested natively by Astro Content Collections for a static, zero-JS visualizer.

1. **The Generator:** Our Python tool analyses repositories and outputs `./output/analysis-result.json` (the raw facts) and `./output/report.md` (Arc42 standard `mermaid` blocks).
2. **The Consumer:** Easily point Astro Content Collections to the `./output/` directory directly at build time.
3. **Static Output:** Run `astro build`. The output becomes pure HTML/CSS/SVG deployable on GitHub Pages or S3!
