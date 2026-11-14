# Implementation Plan: Core Engine Unification, Policy-as-Code & Agentic Workflow Evaluation

**Branch**: `006-core-unification-and-eval` | **Date**: 2026-11-12 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/006-core-unification-and-eval/spec.md`

---

## 1. Summary

Unify the split-brain Python CLI and exporter architecture introduced across Iterations `003`–`005`, externalize all classification logic into `manifests/ecosystems.yaml` (Constitution Principle I), implement real pipeline DAG + anti-pattern extraction and 4-ecosystem structural code analysis (`.NET`, `Python`, `React/TS`, `Java Spring Boot`), replace all `pytest.skip()` placeholders with real tests, and build the **5-Gate Agentic Coding Workflow Validator** (`scripts/validate_agent_workflow.py`).

---

## 2. Technical Context

- **Language/Version**: Python 3.12+ (`.venv` inside WSL)
- **Primary Dependencies**: `typer`, `httpx`, `pydantic`, `pyyaml`, `networkx`, `radon`
- **Storage**: Deterministic local filesystem (`exports/{timestamp}/` + `exports/latest/` symlink/copy)
- **Testing**: `pytest`, `pytest-asyncio` (strict 0-skip enforcement)
- **Target Platform**: WSL Linux CLI, GitHub Actions CI, Google AI Pro Remote Agents
- **Performance Goals**: `< 3 minutes` per `< 500k LoC` repository; byte-for-byte deterministic JSON/Markdown outputs.

---

## 3. Constitution Check

- **I. Policy-as-Code & Extensibility**: **FIXED & ENFORCED**. Moving hardcoded rules from `src/analyzers/classification.py` into `manifests/ecosystems.yaml`.
- **II. Single Source of Truth for Reports**: **ENFORCED**. `exports/latest/` JSON files drive both Markdown generation and Astro build-time rendering.
- **III. Security & Privacy First**: **ENFORCED**. Dual-logger token masking (`src/core/auth.py`) retained; ephemeral clones cleaned up via context manager.
- **IV. Performance & Scalability**: **ENFORCED**. Dual-mode API tree inspection + shallow clone (`--depth 1`).
- **VI. Pipeline Visualization as a First-Class Feature**: **FIXED & ENFORCED**. Real `parser.py` + `dag_builder.py` + `heuristics.py` wired into `analyze_pipeline.py` outputting both per-repo DAG JSONs and aggregate topology files.
- **VII. Strict SDD & TDD**: **FIXED & ENFORCED**. Automated by `scripts/validate_agent_workflow.py`.
- **VIII. Standardized WSL Development Environment**: **ENFORCED**.

---

## 4. Project Structure & Target Modifications

```text
manifests/
└── ecosystems.yaml                          # [NEW] Declarative rules for 4 ecosystems + 27-col discovery signals

src/
├── models/
│   ├── artifacts.py                         # [MODIFY] Add PipelineDAG, WorkflowNode, AntiPattern models matching Astro
│   ├── discovery.py                         # [KEEP/EXTEND] 27-column DiscoveryManifestItem
│   └── topology.py                          # [KEEP] Aggregate org-level TopologyNode & WorkflowRun
├── analyzers/
│   ├── classification.py                    # [MODIFY] Load manifests/ecosystems.yaml; return ecosystem + 27-col flags
│   ├── pipeline/
│   │   ├── parser.py                        # [MODIFY] Support parsing both local .yml paths and raw YAML strings from API
│   │   ├── dag_builder.py                   # [MODIFY] Export structured jobs, needs edges, and triggers
│   │   └── heuristics.py                    # [MODIFY] Detect all 7 PRD anti-patterns with severity & message
│   └── code/
│       ├── orchestrator.py                  # [MODIFY] Route to all 4 ecosystem analyzers + compute LoC/complexity
│       ├── python_ast.py                    # [MODIFY] Enhance Python AST + Radon complexity metrics
│       ├── dotnet_structural.py             # [NEW] Extract .csproj, Controllers, Services, DbContext/Repositories
│       ├── js_ts_structural.py              # [NEW] Extract package.json, React/Next/Vite components, API routes
│       └── java_structural.py               # [NEW] Extract pom.xml/build.gradle, @RestController, @Service, @Repository
├── core/
│   ├── utils/
│   │   ├── export_manager.py                # [MODIFY] Manage exports/{timestamp}/ AND update exports/latest/
│   │   ├── git_cloner.py                    # [MODIFY] Add --depth 1 --single-branch shallow clone optimization
│   │   ├── json_exporter.py                 # [UNIFY] Delegate to canonical exporters
│   │   └── markdown_exporter.py             # [UNIFY] Delegate to canonical exporters
│   └── exporters/
│       ├── discovery_exporter.py            # [KEEP] Outputs repos/repositories.{json,csv,yaml}
│       ├── pipeline_exporter.py             # [MODIFY] Output BOTH pipelines/{org}-{repo}-pipeline.json AND relationships/
│       └── markdown_exporter.py             # [MODIFY] Output reports/{org}-{repo}-report.md (Arc42 + Mermaid)
└── cli/
    └── commands/
        ├── discover.py                      # [MODIFY] Fetch /git/trees?recursive=1 and apply YAML classification
        ├── analyze_pipeline.py              # [MODIFY] Support --from-discovery, --repos-file, --path; restore _analyze_repo_workflows
        └── analyze_code.py                  # [MODIFY] Support --from-discovery, --repos-file, --path; write to exports/latest/reports/

scripts/
├── generate-report-stubs.py                 # [KEEP] Generates Astro MDX stubs from repositories.json
└── validate_agent_workflow.py               # [NEW] 5-Gate Agentic Coding Workflow Evaluator

tests/
├── unit/                                    # [MODIFY] Fix test_cli_inputs.py; add unit tests for YAML manifest & 4 analyzers
└── integration/                             # [MODIFY] Fix test_todo_nodejs_mongo.py; replace all 5 pytest.skip files with real tests
```

---

## 5. Technical Design Details

### 5.1 Per-Repo Pipeline Schema (`exports/latest/pipelines/{org}-{repo}-pipeline.json`)
To satisfy `web/src/components/PipelineView.astro` without breaking `relationships/pipeline_topology.json`:
```json
{
  "org": "github-samples",
  "repository": "pets-workshop",
  "sha": "49000790c260bf6ab84a833f0ece3bc91d2afbe0",
  "analyzed_at": "2026-11-12T21:00:00Z",
  "workflows": [
    {
      "id": "ci.yml",
      "name": "CI Build & Deploy",
      "triggers": ["push", "pull_request"],
      "jobs": [
        { "id": "build", "name": "Build", "runner": "ubuntu-latest", "steps_count": 4, "needs": [] },
        { "id": "deploy", "name": "Deploy", "runner": "ubuntu-latest", "steps_count": 2, "needs": ["build"] }
      ],
      "anti_patterns": [
        {
          "type": "NO_TEST_GATE",
          "severity": "HIGH",
          "message": "Deploy job 'deploy' has no upstream test job in its needs: chain."
        }
      ]
    }
  ]
}
```

### 5.2 5-Gate Agentic Workflow Validator (`scripts/validate_agent_workflow.py`)
1. **Gate 1 (Traceability)**: Parses `spec.md` (`FR-XXX`, `US-XXX`), `plan.md`, and `tasks.md` (`TXXX`) to verify 100% requirement-to-task mapping.
2. **Gate 2 (AST Anti-Stub Audit)**: Uses Python's `ast` module to inspect `src/` and `tests/`. Flags any `pytest.skip`, `pytest.mark.skip`, empty test bodies (`pass` or `...`), or comments matching `Mock targeting behavior` / `TODO`.
3. **Gate 3 (Test Execution & 0-Skip Check)**: Runs `pytest --tb=short -q` via subprocess, parsing output to assert `failed == 0`, `errors == 0`, and `skipped == 0`.
4. **Gate 4 (Astro Contract Verification)**: Verifies that `exports/latest/repos/repositories.json`, `exports/latest/pipelines/*.json`, and `exports/latest/reports/*-report.md` match the exact keys expected by `AtlasSummary.astro`, `PipelineView.astro`, and `ArchitectureView.astro`.
5. **Gate 5 (Determinism Verification)**: Runs `_analyze_repo_workflows` and `_analyze_repo_code` twice on a fixture directory, normalizing timestamps and asserting identical SHA-256 digests.
