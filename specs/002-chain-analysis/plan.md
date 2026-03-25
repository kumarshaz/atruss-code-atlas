# Implementation Plan: Chained Analysis Pipeline

**Branch**: `002-chain-analysis` | **Date**: 2026-03-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-chain-analysis/spec.md`

## Summary

Add JSON export capabilities to the discovery module and consume that JSON globally in `analyze-code` and `analyze-pipeline` modules by automatically cloning target repos into the OS temporary directory via pure `subprocess` `git clone` mappings.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `subprocess` (built-in), `tempfile` (built-in), `json` (built-in)
**Storage**: OS Temporary Filesystem (`tempfile.gettempdir()`)
**Testing**: pytest, native tmpdir fixtures
**Target Platform**: CLI environments (Linux, macOS, Windows)
**Project Type**: CLI
**Performance Goals**: < 3 minutes for 500k LoC repo (Constitution IV)
**Constraints**: Do not leave dangling Git tokens. Clone into isolated TEMP space.
**Scale/Scope**: ~50-100 repositories per JSON manifest.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Policy-as-Code**: No changes to classification manifests.
- **II. Single Source of Truth**: Leveraging JSON outputs as the strict input mechanism for analysis bridging.
- **III. Security & Privacy First**: GITHUB_TOKEN passed directly via environment variables to subprocess. Token is never persisted locally in logs.
- **IV. Performance & Scalability**: OS Temp directory removes need for complex local cleanups that bottleneck scaling.

## Project Structure

### Documentation (this feature)

```text
specs/002-chain-analysis/
├── plan.md              
├── research.md         
├── data-model.md       
├── quickstart.md       
├── contracts/
│   └── discovery-manifest.md           
└── tasks.md             
```

### Source Code 

```text
src/
├── cli/
│   ├── commands/
│   │   ├── discover.py        # Add --output logic
│   │   ├── analyze_code.py    # Add --from-discovery logic + git clone orchestrator
│   │   └── analyze_pipeline.py # Add --from-discovery logic + git clone orchestrator
└── core/
    └── utils/
        └── git_cloner.py      # New orchestration utility
```

**Structure Decision**: A new `git_cloner.py` utility handles the subprocess executions to keep CLI command files clean and decoupled.

## Complexity Tracking

No violations found. No new dependencies added.
