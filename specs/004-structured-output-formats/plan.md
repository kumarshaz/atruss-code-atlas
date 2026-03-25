# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Implement structural output formats (CSV, JSON, YAML) for repository discovery and pipeline visualization, allowing developers to retrieve programmatically parsable data via a simple `--format` flag, fully bypassing visual/markdown defaults where necessary.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+
**Primary Dependencies**: `json` (stdlib), `csv` (stdlib), `pyyaml` (existing), `pydantic` (for models/schemas)
**Storage**: Local Filesystem (`--output-dir`)
**Testing**: `pytest` fixture-based tests checking output file validity
**Target Platform**: Any (Offline CLI)
**Project Type**: CLI Tool
**Performance Goals**: Generate output schemas for <500k LoC in under 3 minutes
**Constraints**: Pure offline file writing. No remote DB, no background brokers.
**Scale/Scope**: ~100 repositories per discovery payload

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Policy-as-Code & Extensibility**: PASS. New formats simply serialize the existing declarative Pydantic schemas.
- **II. Single Source of Truth**: PASS. The JSON format remains the canonical truth and native representation.
- **IV. Performance & Scalability**: PASS. Validation happens explicitly outside the runtime loop, yielding maximum output speed.
- **VII. Strict Test DD**: PASS. Validation output formats align nicely to fixture testing against `github-samples/pets-workshop`.
- **Orchestration constraints**: PASS. No FastAPI/Redis/Postgres added. Offline file dumping logic natively.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

```text
# Source Code (repository root)
src/atruss/
├── core/
│   ├── exporters/
│   │   ├── json_exporter.py
│   │   ├── csv_exporter.py
│   │   └── yaml_exporter.py
│   └── models/
│       ├── discovery.py
│       └── pipeline.py
└── cli/
    ├── discover.py
    └── analyze_pipeline.py

tests/
├── integration/
│   └── test_structured_exports.py
```

**Structure Decision**: Utilizing the primary single project layout native to Atruss Code Atlas, implementing dedicated exporter classes per format to adhere to the Single Responsibility Principle, invoked dynamically via the CLI's `--format` flag.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
