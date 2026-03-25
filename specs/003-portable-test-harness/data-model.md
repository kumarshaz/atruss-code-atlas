# Phase 1: Data Model

With the elimination of the active persistent database tier, the "Data Model" becomes the localized JSON schema contract mapped within pure Python Pydantic structs.

## Entities

### `PortableArtifact`
The immutable state of truth created after processing a target repository. It is NOT saved in Postgres; it is serialized statically.
- **Fields**:
  - `repository` (string): Organziation/repo name.
  - `sha` (string): The Git hash that was processed at execution time.
  - `ecosystem` (EcosystemEnum): e.g., PYTHON, CSHARP.
  - `metrics` (dict): Extracted performance and coverage scores.
  - `pipelines` (list[PipelineWorkflow]): Abstract parsed DAG sequences natively.
- **Validations**: Must serialize entirely into `.json` cleanly. 

### `HarnessFixture`
Testing wrapper representing the pinned public repositories mapped within Pytest logic.
- **Fields**:
  - `repo_url` (string): Full GH URL mapped (e.g., `https://github.com/github-samples/pets-workshop`).
  - `pinned_sha` (string): The exact 40-char commit hash target.
  - `expected_modules` (list[string]): Paths the DAG extraction is expected to trace successfully (e.g. `['client', 'server', 'content']`).
