# Phase 1: Quickstart & Examples

This document details how the developer interacts with the new CLI flags and structural format outputs.

## Generating structural repository discovery

**CLI Usage**:
```bash
python -m atruss.cli discover <org> --output-format json
python -m atruss.cli discover <org> --output-format yaml
python -m atruss.cli discover <org> --output-format csv
```

**Expected JSON Output**:
```json
[
  {
    "name": "atruss-api",
    "clone_url": "https://github.com/org/atruss-api.git",
    "ecosystem": "Python"
  }
]
```

## Generating structural pipeline visualization

**CLI Usage**:
```bash
python -m atruss.cli analyze-pipeline --from-discovery out.json --format yaml
```

**Expected YAML Output**:
```yaml
nodes:
  - node_id: "job_build"
    name: "Build Application"
edges:
  - source: "job_lint"
    target: "job_build"
    relationship: "needs"
```
