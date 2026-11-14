# Phase 1: CLI Contract Definitions

**File:** `specs/002-chain-analysis/contracts/discovery-manifest.md`

This document defines the interface boundary crossing between the `discover` module and the `analyze` modules.

## Schema: Discovery Manifest JSON

The JSON file emitted by `repo-analyzer discover --format json > out.json` must unconditionally adhere to the following schema to be blindly accepted by `analyze-code` and `analyze-pipeline`:

**Schema Rules**:
- Must be a top-level JSON Array.
- Required keys per object: `name`, `clone_url`.
- Optional keys per object: `ecosystem`, `framework`.

**Example Interface**:
```json
[
  {
    "name": "repo-analyzer-core",
    "clone_url": "https://github.com/org/repo-analyzer-core.git",
    "ecosystem": "python",
    "framework": "fastapi"
  }
]
```
