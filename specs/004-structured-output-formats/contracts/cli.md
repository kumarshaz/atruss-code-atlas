# CLI Interface Contract

## Commands Updated

### `discover`
- **Arguments**: `target` (string, the GitHub org/user to scan)
- **New Options**: 
  - `--format`, `-f`: Defines output structural format. 
  - **Choices**: `[json, yaml, csv]`
  - **Default**: `json` (for backwards compatibility)

### `analyze-pipeline`
- **Arguments**: (existing path/discovery inputs)
- **New Options**: 
  - `--format`, `-f`: Defines output structural format.
  - **Choices**: `[json, yaml, csv]`
  - **Default**: `json`

## Exit Codes
- `0`: Success, structure generated and written.
- `1`: Validation error or parsing error.
