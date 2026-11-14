# Quickstart: Portable Analysis Workflows

Atruss Code Atlas runs completely offline and disconnected from databases natively dumping immutable, easily portable reporting assets.

## Analyzing specific list of repositories
Instead of running a full organization discovery, you can bind specific target scopes natively using a plain text file list `targets.txt`.

**`targets.txt` format:**
```text
github-samples/pets-workshop
dotnet/eShop
```

**Execute the analysis:**
```bash
# Iterates across the flat file array natively pulling repositories to an isolated temp structure
repo-analyzer analyze-pipeline --repos-file targets.txt --output-dir ./my-reports/
```

Inside your `./my-reports/` directory, you will natively find byte-for-byte exact schema `.json` snapshots alongside Doc-as-Code Arc42 `report.md` Markdown files, perfectly formatted with Mermaid topologies to ingest into your Astro UI sites.
