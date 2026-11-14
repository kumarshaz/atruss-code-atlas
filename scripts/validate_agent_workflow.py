#!/usr/bin/env python3
"""
5-Gate Agentic Coding Workflow Validator for Atruss Code Atlas.

Enforces:
  Gate 1: Spec -> Plan -> Task Traceability (FR/SC coverage & artifact existence)
  Gate 2: AST Anti-Stub & Anti-Skip Audit across src/ and tests/
  Gate 3: Full Pytest Execution Gate (0 failures, 0 errors, 0 skips)
  Gate 4: Python-to-Astro Schema Contract Verification
  Gate 5: SHA-256 Determinism Verification

Outputs a structured scorecard JSON report (default: exports/latest/agent-eval-report.json).
"""

from __future__ import annotations

import argparse
import ast
import asyncio
import base64
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import tokenize
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from typer.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.analyzers.code.orchestrator import orchestrate_full_analysis  # noqa: E402
from src.cli.commands.analyze_code import app as analyze_code_app  # noqa: E402
from src.cli.commands.analyze_pipeline import (  # noqa: E402
    _analyze_repo_workflows,
    execute_pipeline_analysis,
)
from src.cli.commands.discover import execute_discovery  # noqa: E402
from src.core.services.report_generator import generate_arc42_markdown  # noqa: E402

REQUIRED_DISCOVERY_FIELDS = {
    "Organization",
    "Project",
    "ProjectId",
    "RepositoryName",
    "RepositoryId",
    "DefaultBranch",
    "CloneUrl",
    "SshUrl",
    "WebUrl",
    "Size",
    "IsDisabled",
    "IsPrivate",
    "LastUpdate",
    "PrimaryLanguage",
    "FrameworkType",
    "AllFrameworks",
    "DeployableTypes",
    "HasAPI",
    "HasService",
    "HasFrontend",
    "HasDatabase",
    "TechnologyStack",
    "HasDockerfile",
    "HasPipeline",
    "HasKubernetes",
    "DocumentationPriority",
    "AnalyzedDate",
}


@dataclass
class GateResult:
    gate: str
    passed: bool
    summary: str
    details: dict[str, Any] = field(default_factory=dict)


def _run_gate_1_traceability(spec_dir: Path, repo_root: Path) -> GateResult:
    spec_path = spec_dir / "spec.md"
    plan_path = spec_dir / "plan.md"
    tasks_path = spec_dir / "tasks.md"

    missing_docs = [
        p.name for p in (spec_path, plan_path, tasks_path) if not p.exists()
    ]
    if missing_docs:
        return GateResult(
            gate="Gate 1: Spec-Plan-Task Traceability",
            passed=False,
            summary=f"Missing SpecKit documents: {', '.join(missing_docs)}",
            details={"missing_docs": missing_docs},
        )

    spec_text = spec_path.read_text(encoding="utf-8")
    plan_text = plan_path.read_text(encoding="utf-8")
    tasks_text = tasks_path.read_text(encoding="utf-8")

    spec_frs = sorted(set(re.findall(r"\bFR-\d+\b", spec_text)))
    spec_scs = sorted(set(re.findall(r"\bSC-\d+\b", spec_text)))
    task_ids = sorted(set(re.findall(r"\bT\d{3}\b", tasks_text)))
    mapped_frs = sorted(set(re.findall(r"\bFR-\d+\b", tasks_text)))
    mapped_scs = sorted(set(re.findall(r"\bSC-\d+\b", tasks_text)))

    unmapped_frs = [fr for fr in spec_frs if fr not in mapped_frs]

    # Verify concrete backticked repo file paths referenced in plan.md exist on disk
    candidate_paths = set(
        re.findall(
            r"`((?:src|manifests|scripts|tests|web)/[A-Za-z0-9_./-]+\.(?:py|yaml|yml|json|md|astro|toml))`",
            plan_text,
        )
    )
    missing_targets = sorted(
        rel for rel in candidate_paths
        if "{" not in rel and "*" not in rel and not (repo_root / rel).exists()
    )

    checked_tasks = len(re.findall(r"^- \[[xX]\] T\d{3}\b", tasks_text, flags=re.MULTILINE))
    passed = len(unmapped_frs) == 0 and len(missing_targets) == 0 and len(task_ids) > 0

    return GateResult(
        gate="Gate 1: Spec-Plan-Task Traceability",
        passed=passed,
        summary=(
            f"Mapped {len(mapped_frs)}/{len(spec_frs)} FRs across {len(task_ids)} tasks "
            f"({checked_tasks}/{len(task_ids)} checked); missing targets={len(missing_targets)}"
        ),
        details={
            "spec_frs": spec_frs,
            "mapped_frs": mapped_frs,
            "unmapped_frs": unmapped_frs,
            "spec_scs": spec_scs,
            "mapped_scs": mapped_scs,
            "total_tasks": len(task_ids),
            "checked_tasks": checked_tasks,
            "verified_plan_targets": sorted(candidate_paths),
            "missing_plan_targets": missing_targets,
        },
    )


def _is_empty_stub_body(stmts: list[ast.stmt]) -> bool:
    """Return True if a function body contains only docstrings/pass/Ellipsis/return None."""
    effective = stmts
    if (
        effective
        and isinstance(effective[0], ast.Expr)
        and isinstance(effective[0].value, ast.Constant)
        and isinstance(effective[0].value.value, str)
    ):
        effective = effective[1:]

    if not effective:
        return True

    for stmt in effective:
        if isinstance(stmt, ast.Pass):
            continue
        if (
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Constant)
            and stmt.value.value is Ellipsis
        ):
            continue
        if isinstance(stmt, ast.Return) and stmt.value is None:
            continue
        return False
    return True


def _run_gate_2_anti_stub_audit(repo_root: Path) -> GateResult:
    violations: list[dict[str, Any]] = []
    files_scanned = 0

    for root_name in ("src", "tests"):
        root_dir = repo_root / root_name
        if not root_dir.exists():
            continue
        for py_file in sorted(root_dir.rglob("*.py")):
            if "__pycache__" in py_file.parts:
                continue
            files_scanned += 1
            rel_path = str(py_file.relative_to(repo_root)).replace("\\", "/")
            source = py_file.read_text(encoding="utf-8", errors="replace")

            try:
                for tok in tokenize.generate_tokens(io.StringIO(source).readline):
                    if tok.type == tokenize.COMMENT:
                        if "Mock targeting behavior" in tok.string:
                            violations.append({
                                "file": rel_path,
                                "line": tok.start[0],
                                "rule": "NO_MOCK_TARGETING_COMMENT",
                                "message": (
                                    "Found disallowed '# Mock targeting behavior' placeholder."
                                ),
                            })
                        if re.search(r"\bTODO\b", tok.string):
                            violations.append({
                                "file": rel_path,
                                "line": tok.start[0],
                                "rule": "NO_TODO_COMMENT",
                                "message": f"Found disallowed TODO comment: {tok.string.strip()}",
                            })
            except tokenize.TokenError:
                pass

            try:
                tree = ast.parse(source, filename=rel_path)
            except SyntaxError as exc:
                violations.append({
                    "file": rel_path,
                    "line": exc.lineno or 1,
                    "rule": "SYNTAX_ERROR",
                    "message": str(exc),
                })
                continue

            for node in ast.walk(tree):
                # Check pytest.skip(...) calls
                if isinstance(node, ast.Call):
                    func = node.func
                    if (
                        isinstance(func, ast.Attribute)
                        and func.attr in ("skip", "xfail")
                        and isinstance(func.value, ast.Name)
                        and func.value.id == "pytest"
                    ):
                        violations.append({
                            "file": rel_path,
                            "line": node.lineno,
                            "rule": "NO_PYTEST_SKIP",
                            "message": f"Disallowed pytest.{func.attr}() call.",
                        })

                # Check @pytest.mark.skip / skipif decorators & empty test stubs
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for dec in node.decorator_list:
                        dec_name = ast.unparse(dec) if hasattr(ast, "unparse") else ""
                        if "mark.skip" in dec_name:
                            violations.append({
                                "file": rel_path,
                                "line": node.lineno,
                                "rule": "NO_SKIP_DECORATOR",
                                "message": f"Disallowed skip decorator @{dec_name} on {node.name}.",
                            })
                    is_empty_test = (
                        root_name == "tests"
                        and node.name.startswith("test_")
                        and _is_empty_stub_body(node.body)
                    )
                    if is_empty_test:
                        violations.append({
                            "file": rel_path,
                            "line": node.lineno,
                            "rule": "NO_EMPTY_TEST_STUB",
                            "message": f"Empty stub body in test function '{node.name}'.",
                        })

    passed = len(violations) == 0
    return GateResult(
        gate="Gate 2: AST Anti-Stub & Anti-Skip Audit",
        passed=passed,
        summary=(
            f"Scanned {files_scanned} Python files under src/ & tests/; "
            f"violations={len(violations)}"
        ),
        details={"files_scanned": files_scanned, "violations": violations},
    )


def _run_gate_3_pytest(repo_root: Path) -> GateResult:
    cmd = [sys.executable, "-m", "pytest", "tests/", "--strict-markers", "-v"]
    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    combined = f"{proc.stdout}\n{proc.stderr}"

    def _extract_count(label: str) -> int:
        matches = re.findall(rf"(\d+)\s+{label}\b", combined)
        return int(matches[-1]) if matches else 0

    passed_cnt = _extract_count("passed")
    failed_cnt = _extract_count("failed")
    error_cnt = _extract_count("error") + _extract_count("errors")
    skipped_cnt = _extract_count("skipped")
    warning_cnt = _extract_count("warning") + _extract_count("warnings")

    passed = (
        proc.returncode == 0
        and passed_cnt > 0
        and failed_cnt == 0
        and error_cnt == 0
        and skipped_cnt == 0
    )

    return GateResult(
        gate="Gate 3: Full Pytest Execution (0-Skip)",
        passed=passed,
        summary=(
            f"exit={proc.returncode}, passed={passed_cnt}, failed={failed_cnt}, "
            f"errors={error_cnt}, skipped={skipped_cnt}, warnings={warning_cnt}"
        ),
        details={
            "returncode": proc.returncode,
            "passed": passed_cnt,
            "failed": failed_cnt,
            "errors": error_cnt,
            "skipped": skipped_cnt,
            "warnings": warning_cnt,
        },
    )


def _validate_discovery_payload(data: Any) -> list[str]:
    errs: list[str] = []
    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list) or not items:
        return ["Discovery repositories.json must contain a non-empty 'items' list"]
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            errs.append(f"Discovery item[{idx}] is not a JSON object")
            continue
        missing = sorted(REQUIRED_DISCOVERY_FIELDS - set(item.keys()))
        if missing:
            errs.append(f"Discovery item[{idx}] missing keys: {missing}")
    return errs


def _validate_pipeline_payload(data: Any, label: str) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return [f"{label}: payload is not a JSON object"]
    if "analyzed_at" not in data or not isinstance(data.get("workflows"), list):
        return [f"{label}: missing required keys 'analyzed_at' or 'workflows'"]
    for idx, wf in enumerate(data["workflows"]):
        if not isinstance(wf, dict):
            errs.append(f"{label}: workflow[{idx}] is not an object")
            continue
        for req in ("id", "name", "triggers", "jobs", "anti_patterns"):
            if req not in wf:
                errs.append(f"{label}: workflow[{idx}] missing '{req}'")
        for jidx, job in enumerate(wf.get("jobs", [])):
            for jreq in ("id", "name", "runner", "steps_count", "needs"):
                if jreq not in job:
                    errs.append(f"{label}: workflow[{idx}].jobs[{jidx}] missing '{jreq}'")
        for aidx, ap in enumerate(wf.get("anti_patterns", [])):
            for areq in ("type", "severity", "message"):
                if areq not in ap:
                    errs.append(f"{label}: workflow[{idx}].anti_patterns[{aidx}] missing '{areq}'")
    return errs


def _run_gate_4_astro_contracts(exports_dir: Path) -> GateResult:
    errors: list[str] = []
    validated_files: list[str] = []

    # 1. Always execute an isolated end-to-end sandbox run and verify every Astro schema contract
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        sandbox_exports = tmp_path / "exports"
        sandbox_logs = tmp_path / "logs"

        wf_yaml = (
            "name: Contract CI\n"
            "on:\n"
            "  push:\n"
            "    branches: [main]\n"
            "jobs:\n"
            "  build:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - uses: actions/setup-python@v5\n"
            "        with:\n"
            "          cache: pip\n"
            "      - run: pip install -r requirements.txt\n"
            "  deploy:\n"
            "    needs: build\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: echo deploy\n"
        )
        b64_wf = base64.b64encode(wf_yaml.encode("utf-8")).decode("ascii")

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/orgs/contract-org/repos":
                return httpx.Response(
                    200,
                    json=[
                        {
                            "id": 999,
                            "name": "atlas-sample",
                            "owner": {"login": "contract-org", "id": 11},
                            "default_branch": "main",
                            "clone_url": "https://github.com/contract-org/atlas-sample.git",
                            "language": "Python",
                        }
                    ],
                )
            if request.url.path == "/repos/contract-org/atlas-sample/git/trees/main":
                return httpx.Response(
                    200,
                    json={
                        "sha": "contractsha1",
                        "tree": [
                            {"path": "pyproject.toml", "type": "blob"},
                            {"path": "app.py", "type": "blob"},
                            {"path": ".github/workflows/ci.yml", "type": "blob"},
                        ],
                    },
                )
            ci_contents = "/repos/contract-org/atlas-sample/contents/.github/workflows/ci.yml"
            if request.url.path == ci_contents:
                return httpx.Response(
                    200,
                    json={"encoding": "base64", "content": b64_wf},
                )
            return httpx.Response(404, json={"message": "Not Found"})

        async def _run_pipeline() -> None:
            transport = httpx.MockTransport(handler)
            await execute_discovery(
                org="contract-org",
                base_dir=str(sandbox_exports),
                log_dir=str(sandbox_logs),
                include_archived=False,
                max_concurrent=1,
                exclude_repo_names=[],
                exclude_repo_patterns=[],
                dry_run=False,
                transport=transport,
            )
            await execute_pipeline_analysis(
                from_discovery=str(sandbox_exports / "latest" / "repos" / "repositories.json"),
                output_dir=str(sandbox_exports),
                transport=httpx.MockTransport(handler),
            )

        asyncio.run(_run_pipeline())

        sample_repo = tmp_path / "atlas-sample"
        sample_repo.mkdir()
        (sample_repo / "pyproject.toml").write_text(
            "[project]\nname='atlas-sample'\n", encoding="utf-8"
        )
        (sample_repo / "app.py").write_text(
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n"
            "@app.get('/health')\n"
            "def health(): return 'ok'\n",
            encoding="utf-8",
        )

        runner = CliRunner()
        res = runner.invoke(
            analyze_code_app,
            ["--path", str(sample_repo), "--exports-dir", str(sandbox_exports)],
        )
        if res.exit_code != 0:
            errors.append(f"Sandbox analyze-code failed: {res.output}")

        latest = sandbox_exports / "latest"
        disc_file = latest / "repos" / "repositories.json"
        if not disc_file.exists():
            errors.append("Sandbox missing latest/repos/repositories.json")
        else:
            errors.extend(
                _validate_discovery_payload(json.loads(disc_file.read_text(encoding="utf-8")))
            )
            validated_files.append("sandbox:repos/repositories.json")

        pipe_file = latest / "pipelines" / "contract-org-atlas-sample-pipeline.json"
        if not pipe_file.exists():
            errors.append(
                "Sandbox missing latest/pipelines/contract-org-atlas-sample-pipeline.json"
            )
        else:
            errors.extend(
                _validate_pipeline_payload(
                    json.loads(pipe_file.read_text(encoding="utf-8")),
                    "sandbox:pipelines/contract-org-atlas-sample-pipeline.json",
                )
            )
            validated_files.append("sandbox:pipelines/contract-org-atlas-sample-pipeline.json")

        topo_file = latest / "relationships" / "pipeline_topology.json"
        if not topo_file.exists():
            errors.append("Sandbox missing latest/relationships/pipeline_topology.json")
        else:
            json.loads(topo_file.read_text(encoding="utf-8"))
            validated_files.append("sandbox:relationships/pipeline_topology.json")

        md_file = latest / "reports" / "local-atlas-sample-report.md"
        analysis_file = latest / "reports" / "local-atlas-sample-analysis.json"
        if not md_file.exists() or not analysis_file.exists():
            errors.append(
                "Sandbox missing latest/reports/local-atlas-sample-{report.md,analysis.json}"
            )
        else:
            md_text = md_file.read_text(encoding="utf-8")
            if not md_text.startswith("---\ntitle: ") or "```mermaid" not in md_text:
                errors.append(
                    "Sandbox Arc42 markdown missing YAML frontmatter 'title:' or Mermaid block"
                )
            art_json = json.loads(analysis_file.read_text(encoding="utf-8"))
            for key in ("repository", "sha", "ecosystem", "architecture_components", "metrics"):
                if key not in art_json:
                    errors.append(f"Sandbox analysis JSON missing '{key}'")
            validated_files.append("sandbox:reports/local-atlas-sample-report.md")
            validated_files.append("sandbox:reports/local-atlas-sample-analysis.json")

    # 2. Validate existing workspace exports/latest files if present
    ws_latest = exports_dir / "latest"
    if (ws_latest / "repos" / "repositories.json").exists():
        errors.extend(
            _validate_discovery_payload(
                json.loads((ws_latest / "repos" / "repositories.json").read_text(encoding="utf-8"))
            )
        )
        validated_files.append("workspace:repos/repositories.json")

    pipe_dir = ws_latest / "pipelines"
    for pf in sorted(pipe_dir.glob("*-pipeline.json")) if pipe_dir.exists() else []:
        errors.extend(
            _validate_pipeline_payload(
                json.loads(pf.read_text(encoding="utf-8")),
                f"workspace:pipelines/{pf.name}",
            )
        )
        validated_files.append(f"workspace:pipelines/{pf.name}")

    rep_dir = ws_latest / "reports"
    for mf in sorted(rep_dir.glob("*-report.md")) if rep_dir.exists() else []:
        text = mf.read_text(encoding="utf-8")
        if not text.startswith("---\ntitle: ") or "```mermaid" not in text:
            errors.append(
                f"workspace:reports/{mf.name} missing YAML frontmatter 'title:' or Mermaid block"
            )
        validated_files.append(f"workspace:reports/{mf.name}")

    passed = len(errors) == 0 and len(validated_files) > 0
    return GateResult(
        gate="Gate 4: Python-to-Astro Schema Contract",
        passed=passed,
        summary=f"Validated {len(validated_files)} contract artifacts; errors={len(errors)}",
        details={"validated_files": validated_files, "errors": errors},
    )


def _digest(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _run_gate_5_determinism() -> GateResult:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "det-repo"
        (repo / ".github" / "workflows").mkdir(parents=True)
        (repo / "services").mkdir(parents=True)

        (repo / "pyproject.toml").write_text("[project]\nname='det-repo'\n", encoding="utf-8")
        (repo / "services" / "api.py").write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n"
            "@router.get('/items')\n"
            "def list_items(active: bool = True):\n"
            "    return ['a'] if active else []\n",
            encoding="utf-8",
        )
        (repo / ".github" / "workflows" / "ci.yml").write_text(
            "name: Det CI\non:\n  pull_request:\njobs:\n  test:\n"
            "    runs-on: ubuntu-latest\n    steps:\n      - run: pytest\n",
            encoding="utf-8",
        )

        hashes: list[dict[str, str]] = []
        for _ in range(2):
            code_res = orchestrate_full_analysis(repo)
            pipe_art = _analyze_repo_workflows(repo, "det-repo")
            md = generate_arc42_markdown(
                "det-repo",
                code_res.components,
                metrics=code_res.metrics,
                ecosystem=code_res.ecosystem,
                framework=code_res.framework,
                sha="deterministic000",
            )
            hashes.append({
                "components_sha256": _digest(json.dumps(code_res.components, sort_keys=True)),
                "metrics_sha256": _digest(json.dumps(code_res.metrics, sort_keys=True)),
                "pipeline_sha256": _digest(pipe_art.model_dump_json(indent=2)),
                "markdown_sha256": _digest(md),
            })

    mismatches = [k for k in hashes[0] if hashes[0][k] != hashes[1][k]]
    passed = len(mismatches) == 0
    return GateResult(
        gate="Gate 5: SHA-256 Determinism Check",
        passed=passed,
        summary="All 4 artifact SHA-256 digests matched across repeated runs"
        if passed
        else f"Digest mismatches: {', '.join(mismatches)}",
        details={"run_1": hashes[0], "run_2": hashes[1], "mismatches": mismatches},
    )


def evaluate(
    spec_dir: Path, exports_dir: Path, output_path: Path, repo_root: Path = REPO_ROOT
) -> int:
    gates = [
        _run_gate_1_traceability(spec_dir, repo_root),
        _run_gate_2_anti_stub_audit(repo_root),
        _run_gate_3_pytest(repo_root),
        _run_gate_4_astro_contracts(exports_dir),
        _run_gate_5_determinism(),
    ]

    passed_count = sum(1 for g in gates if g.passed)
    total_gates = len(gates)
    ratio = passed_count / total_gates
    if passed_count == total_gates:
        grade = "A"
    elif ratio >= 0.8:
        grade = "B"
    elif ratio >= 0.6:
        grade = "C"
    else:
        grade = "F"

    rel_spec_dir = (
        str(spec_dir.relative_to(repo_root)).replace("\\", "/")
        if spec_dir.is_relative_to(repo_root)
        else str(spec_dir)
    )
    report = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "spec_dir": rel_spec_dir,
        "grade": grade,
        "passed_gates": passed_count,
        "total_gates": total_gates,
        "all_passed": passed_count == total_gates,
        "gates": [asdict(g) for g in gates],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"=== Atruss 5-Gate Agentic Workflow Evaluation (Grade: {grade}) ===")
    for g in gates:
        status = "PASS" if g.passed else "FAIL"
        print(f"[{status}] {g.gate}: {g.summary}")
    print(f"Report written to: {output_path}")

    return 0 if passed_count == total_gates else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Atruss 5-Gate Agentic Coding Workflow Validator")
    parser.add_argument(
        "--spec",
        default="specs/006-core-unification-and-eval",
        help="Path to the SpecKit feature directory containing spec.md, plan.md, tasks.md",
    )
    parser.add_argument(
        "--exports-dir",
        default="exports",
        help="Path to archival exports base directory",
    )
    parser.add_argument(
        "--output",
        default="exports/latest/agent-eval-report.json",
        help="Path to write JSON evaluation scorecard",
    )
    args = parser.parse_args()

    spec_dir = Path(args.spec)
    if not spec_dir.is_absolute():
        spec_dir = REPO_ROOT / spec_dir

    exports_dir = Path(args.exports_dir)
    if not exports_dir.is_absolute():
        exports_dir = REPO_ROOT / exports_dir

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    raise SystemExit(evaluate(spec_dir, exports_dir, output_path))


if __name__ == "__main__":
    main()
