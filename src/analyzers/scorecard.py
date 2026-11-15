from __future__ import annotations

from pathlib import Path
from typing import Any

from src.models.artifacts import (
    DependencyRecord,
    FitnessViolation,
    RepositoryScorecard,
    ScorecardDimension,
    SecretFinding,
    VulnerabilityRecord,
)

SECURITY_PIPELINE_ANTIPATTERNS: frozenset[str] = frozenset({
    "HARDCODED_SECRET",
    "UNPINNED_ACTION",
    "TEMPLATE_INJECTION",
    "PWN_REQUEST_RISK",
    "EXCESSIVE_PERMISSIONS",
    "ARTIFACT_CREDENTIAL_PERSISTENCE",
    "STATIC_CLOUD_CREDENTIALS",
})

_LOCKFILE_NAMES: frozenset[str] = frozenset({
    "uv.lock",
    "poetry.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "packages.lock.json",
    "cargo.lock",
    "go.sum",
    "pipfile.lock",
    "gemfile.lock",
    "gradle.lockfile",
})

_MANIFEST_NAMES: frozenset[str] = frozenset({
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "cargo.toml",
    "go.mod",
})

_TEST_KEYWORDS: tuple[str, ...] = (
    "test",
    "pytest",
    "jest",
    "vitest",
    "junit",
    "spec",
    "check",
    "verify",
    "e2e",
)

_TEST_RUN_TOKENS: tuple[str, ...] = (
    "pytest",
    "npm test",
    "pnpm test",
    "yarn test",
    "dotnet test",
    "mvn test",
    "gradle test",
    "jest",
    "vitest",
    "go test",
    "cargo test",
)

DIMENSION_WEIGHTS: dict[str, tuple[str, float]] = {
    "code_quality": ("Code Quality", 0.20),
    "security": ("Security", 0.20),
    "maintainability": ("Maintainability", 0.15),
    "test_coverage": ("Test Coverage", 0.15),
    "dependency_health": ("Dependency Health", 0.15),
    "pipeline_health": ("Pipeline Health", 0.15),
}


def score_to_grade(score: float) -> str:
    """Convert a 0-100 score into an A-F letter grade per PRD Section 6.3."""
    if score >= 90.0:
        return "A"
    if score >= 80.0:
        return "B"
    if score >= 70.0:
        return "C"
    if score >= 60.0:
        return "D"
    return "F"


def _clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, float(value))), 2)


def _attr_or_key(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _extract_anti_patterns(pipeline: Any) -> list[dict[str, Any]]:
    raw_aps = _attr_or_key(pipeline, "anti_patterns", []) or []
    normalized: list[dict[str, Any]] = []
    for ap in raw_aps:
        if isinstance(ap, dict):
            normalized.append(ap)
        elif hasattr(ap, "model_dump"):
            normalized.append(ap.model_dump())
        else:
            normalized.append({
                "rule_id": str(getattr(ap, "rule_id", "")),
                "type": str(getattr(ap, "type", "")),
                "severity": str(getattr(ap, "severity", "MEDIUM")),
                "message": str(getattr(ap, "message", "")),
            })
    return normalized


def _pipeline_has_test_job(pipelines: list[Any]) -> bool:
    for wf in pipelines:
        wf_name = str(_attr_or_key(wf, "name", "") or _attr_or_key(wf, "id", "")).lower()
        if "test" in wf_name and not _attr_or_key(wf, "jobs", None):
            return True

        jobs = _attr_or_key(wf, "jobs", None)
        job_entries: list[tuple[str, dict[str, Any]]] = []
        if isinstance(jobs, dict):
            for jid, jdata in jobs.items():
                job_entries.append((str(jid), jdata if isinstance(jdata, dict) else {}))
        elif isinstance(jobs, list):
            for jdata in jobs:
                if isinstance(jdata, dict):
                    job_entries.append((str(jdata.get("id", "")), jdata))

        job_nodes = _attr_or_key(wf, "job_nodes", None)
        if isinstance(job_nodes, list):
            for jdata in job_nodes:
                if isinstance(jdata, dict):
                    job_entries.append((str(jdata.get("id", "")), jdata))

        for jid, jdata in job_entries:
            label = f"{jid} {jdata.get('name', '')}".lower()
            if any(kw in label for kw in _TEST_KEYWORDS):
                return True
            steps = jdata.get("steps", [])
            if isinstance(steps, list):
                for step in steps:
                    if not isinstance(step, dict):
                        continue
                    run_cmd = str(step.get("run", "")).lower()
                    if any(tok in run_cmd for tok in _TEST_RUN_TOKENS):
                        return True
    return False


def _pipeline_has_parallelism(pipelines: list[Any]) -> bool:
    for wf in pipelines:
        dag_metrics = _attr_or_key(wf, "dag_metrics", None)
        if isinstance(dag_metrics, dict):
            if dag_metrics.get("has_parallelism"):
                return True
            node_count = int(dag_metrics.get("node_count", 0) or 0)
            max_depth = int(dag_metrics.get("max_depth", 0) or 0)
            is_valid = dag_metrics.get("is_valid_dag", True)
            if is_valid and node_count >= 2 and max_depth < node_count - 1:
                return True

        jobs = _attr_or_key(wf, "jobs", None)
        if isinstance(jobs, dict) and len(jobs) >= 2:
            roots = 0
            fan_out_parents: dict[str, int] = {}
            for _jid, jdata in jobs.items():
                needs = jdata.get("needs", []) if isinstance(jdata, dict) else []
                if isinstance(needs, str):
                    needs_list = [needs]
                elif isinstance(needs, list):
                    needs_list = [str(n) for n in needs]
                else:
                    needs_list = []
                if not needs_list:
                    roots += 1
                for dep in needs_list:
                    fan_out_parents[dep] = fan_out_parents.get(dep, 0) + 1
            if roots >= 2 or any(cnt >= 2 for cnt in fan_out_parents.values()):
                return True
        elif isinstance(jobs, list) and len(jobs) >= 2:
            roots = 0
            fan_out_parents = {}
            for jdata in jobs:
                if not isinstance(jdata, dict):
                    continue
                needs = jdata.get("needs", [])
                needs_list = (
                    [needs]
                    if isinstance(needs, str)
                    else ([str(n) for n in needs] if isinstance(needs, list) else [])
                )
                if not needs_list:
                    roots += 1
                for dep in needs_list:
                    fan_out_parents[dep] = fan_out_parents.get(dep, 0) + 1
            if roots >= 2 or any(cnt >= 2 for cnt in fan_out_parents.values()):
                return True

        job_nodes = _attr_or_key(wf, "job_nodes", None)
        if isinstance(job_nodes, list) and len(job_nodes) >= 2:
            roots = sum(
                1 for j in job_nodes if isinstance(j, dict) and not j.get("needs")
            )
            if roots >= 2:
                return True
    return False


def _has_test_files(components: list[dict[str, Any]], metrics: dict[str, Any]) -> bool:
    if int(metrics.get("test_file_count", 0) or 0) > 0 or bool(metrics.get("has_tests", False)):
        return True
    for comp in components:
        fpath = str(comp.get("file", "")).replace("\\", "/").lower()
        name = str(comp.get("name", "")).lower()
        if (
            "/test" in fpath
            or fpath.startswith("test")
            or "/__tests__/" in fpath
            or ".test." in fpath
            or ".spec." in fpath
            or "_test." in fpath
            or "tests/" in fpath
            or name.startswith("test_")
        ):
            return True
    return False


def _severity_penalty(severity: str, mapping: dict[str, float], default: float) -> float:
    return mapping.get(str(severity).strip().upper(), default)


def compute_repository_scorecard(
    metrics: dict[str, Any] | None = None,
    components: list[dict[str, Any]] | None = None,
    pipelines: list[Any] | None = None,
    dependencies: list[DependencyRecord] | None = None,
    vulnerabilities: list[VulnerabilityRecord] | None = None,
    secrets: list[SecretFinding] | None = None,
    fitness_violations: list[FitnessViolation] | None = None,
    coverage_percent: float | None = None,
) -> RepositoryScorecard:
    """
    Compute the deterministic 6-Dimension A-F Repository Scorecard and Technical Debt
    Score per PRD Section 6.3.
    """
    m = metrics or {}
    comps = components or []
    pipes = pipelines or []
    deps = dependencies or []
    vulns = vulnerabilities or []
    sec_findings = secrets or []
    fitness = fitness_violations or []

    # 1. Code Quality (0.20)
    avg_cc = float(m.get("avg_cyclomatic_complexity", 0.0) or 0.0)
    max_cc = float(m.get("max_cyclomatic_complexity", 0.0) or 0.0)
    dup_pct = max(0.0, float(m.get("duplication_pct", 0.0) or 0.0))
    dead_cnt = max(0, int(m.get("dead_code_count", 0) or 0))

    cq_penalty = 0.0
    if avg_cc > 3.0:
        cq_penalty += min(30.0, (avg_cc - 3.0) * 4.0)
    if max_cc > 15.0:
        cq_penalty += min(25.0, (max_cc - 15.0) * 1.5)
    if dup_pct > 0.0:
        cq_penalty += min(25.0, dup_pct * 1.5)
    if dead_cnt > 0:
        cq_penalty += min(20.0, dead_cnt * 2.0)
    cq_score = _clamp_score(100.0 - cq_penalty)
    cq_details = (
        f"avg_cc={avg_cc:.2f}, max_cc={max_cc:.0f}, "
        f"duplication={dup_pct:.2f}%, dead_code={dead_cnt}"
    )

    # 2. Security (0.20)
    vuln_penalties = {"CRITICAL": 25.0, "HIGH": 15.0, "MEDIUM": 7.0, "LOW": 2.0}
    secret_penalties = {"CRITICAL": 25.0, "HIGH": 18.0, "MEDIUM": 10.0, "LOW": 5.0}
    pipe_sec_penalties = {"CRITICAL": 20.0, "HIGH": 12.0, "MEDIUM": 6.0, "LOW": 2.0}

    all_aps: list[dict[str, Any]] = []
    for wf in pipes:
        all_aps.extend(_extract_anti_patterns(wf))

    sec_aps = [
        ap for ap in all_aps
        if str(ap.get("type", "")).strip().upper() in SECURITY_PIPELINE_ANTIPATTERNS
    ]
    op_aps = [
        ap for ap in all_aps
        if str(ap.get("type", "")).strip().upper() not in SECURITY_PIPELINE_ANTIPATTERNS
    ]

    sec_penalty = 0.0
    for v in vulns:
        sev = str(_attr_or_key(v, "severity", "MEDIUM"))
        sec_penalty += _severity_penalty(sev, vuln_penalties, 7.0)
    for s in sec_findings:
        sev = str(_attr_or_key(s, "severity", "HIGH"))
        sec_penalty += _severity_penalty(sev, secret_penalties, 18.0)
    for ap in sec_aps:
        sev = str(ap.get("severity", "MEDIUM"))
        sec_penalty += _severity_penalty(sev, pipe_sec_penalties, 6.0)
    sec_score = _clamp_score(100.0 - sec_penalty)
    sec_details = (
        f"vulnerabilities={len(vulns)}, secrets={len(sec_findings)}, "
        f"pipeline_security_findings={len(sec_aps)}"
    )

    # 3. Maintainability (0.15)
    avg_cog = float(m.get("avg_cognitive_complexity", 0.0) or 0.0)
    max_cog = float(m.get("max_cognitive_complexity", 0.0) or 0.0)
    file_complexities = m.get("file_complexities") or []
    oversized_files = 0
    if isinstance(file_complexities, list):
        for fc in file_complexities:
            if isinstance(fc, dict) and int(fc.get("loc", 0) or 0) > 500:
                oversized_files += 1

    fit_penalties = {"CRITICAL": 18.0, "HIGH": 12.0, "MEDIUM": 6.0, "LOW": 2.0}
    maint_penalty = 0.0
    if avg_cog > 5.0:
        maint_penalty += min(25.0, (avg_cog - 5.0) * 3.0)
    if max_cog > 20.0:
        maint_penalty += min(25.0, (max_cog - 20.0) * 1.5)
    for fv in fitness:
        sev = str(_attr_or_key(fv, "severity", "HIGH"))
        maint_penalty += _severity_penalty(sev, fit_penalties, 12.0)
    if oversized_files > 0:
        maint_penalty += min(20.0, oversized_files * 5.0)
    maint_score = _clamp_score(100.0 - maint_penalty)
    maint_details = (
        f"avg_cognitive={avg_cog:.2f}, max_cognitive={max_cog:.0f}, "
        f"fitness_violations={len(fitness)}, oversized_files={oversized_files}"
    )

    # 4. Test Coverage (0.15)
    resolved_cov = coverage_percent if coverage_percent is not None else m.get("coverage_percent")
    has_ci_tests = _pipeline_has_test_job(pipes)
    has_tests = _has_test_files(comps, m)

    if resolved_cov is not None:
        base_cov = max(0.0, min(100.0, float(resolved_cov)))
        cov_score = _clamp_score(base_cov + (5.0 if has_ci_tests else 0.0))
        cov_details = f"coverage={base_cov:.2f}%, ci_test_job={has_ci_tests}"
    else:
        cov_score = 70.0 if (has_ci_tests or has_tests) else 40.0
        cov_details = (
            f"coverage=unavailable, ci_test_job={has_ci_tests}, test_files_detected={has_tests}"
        )

    # 5. Dependency Health (0.15)
    if not deps:
        if vulns:
            dep_score = _clamp_score(90.0 - min(60.0, len(vulns) * 15.0))
            dep_details = f"dependencies=0, external_vulnerabilities={len(vulns)}"
        else:
            dep_score = 90.0
            dep_details = "dependencies=0 (no manifests parsed)"
    else:
        dep_penalty = 0.0
        manifest_names = {
            Path(str(_attr_or_key(d, "manifest_file", ""))).name.lower()
            for d in deps
            if _attr_or_key(d, "manifest_file", "")
        }
        has_lockfile = any(name in _LOCKFILE_NAMES for name in manifest_names)
        has_manifest = any(
            name in _MANIFEST_NAMES
            or (name.startswith("requirements") and name.endswith(".txt"))
            or name.endswith(".csproj")
            for name in manifest_names
        )
        missing_lockfile = has_manifest and not has_lockfile and not bool(m.get("has_lockfile"))
        if missing_lockfile:
            dep_penalty += 15.0

        outdated_count = sum(1 for d in deps if bool(_attr_or_key(d, "is_outdated", False)))
        outdated_ratio = outdated_count / len(deps)
        dep_penalty += outdated_ratio * 35.0

        vuln_purls = {
            str(_attr_or_key(v, "purl", ""))
            for v in vulns
            if _attr_or_key(v, "purl", "")
        }
        vuln_pkgs = {
            str(_attr_or_key(v, "package", "")).lower()
            for v in vulns
            if _attr_or_key(v, "package", "")
        }
        vuln_dep_count = 0
        for d in deps:
            d_vids = _attr_or_key(d, "vulnerability_ids", []) or []
            d_purl = str(_attr_or_key(d, "purl", ""))
            d_name = str(_attr_or_key(d, "name", "")).lower()
            if d_vids or (d_purl and d_purl in vuln_purls) or (d_name and d_name in vuln_pkgs):
                vuln_dep_count += 1
        if vuln_dep_count == 0 and vulns:
            vuln_dep_count = min(len(deps), len(vulns))
        vuln_ratio = vuln_dep_count / len(deps)
        dep_penalty += vuln_ratio * 50.0

        dep_score = _clamp_score(100.0 - dep_penalty)
        dep_details = (
            f"dependencies={len(deps)}, outdated={outdated_count}, "
            f"vulnerable={vuln_dep_count}, has_lockfile={has_lockfile}"
        )

    # 6. Pipeline Health (0.15)
    if not pipes:
        pipe_score = 40.0
        pipe_details = "workflows=0"
    else:
        op_penalties = {"CRITICAL": 20.0, "HIGH": 12.0, "MEDIUM": 6.0, "LOW": 3.0}
        pipe_penalty = sum(
            _severity_penalty(str(ap.get("severity", "MEDIUM")), op_penalties, 6.0)
            for ap in op_aps
        )
        has_parallel = _pipeline_has_parallelism(pipes)
        bonus = 5.0 if has_parallel else 0.0
        pipe_score = _clamp_score(100.0 - pipe_penalty + bonus)
        pipe_details = (
            f"workflows={len(pipes)}, operational_antipatterns={len(op_aps)}, "
            f"parallel_branches={has_parallel}"
        )

    raw_dimensions = {
        "code_quality": (cq_score, cq_details),
        "security": (sec_score, sec_details),
        "maintainability": (maint_score, maint_details),
        "test_coverage": (cov_score, cov_details),
        "dependency_health": (dep_score, dep_details),
        "pipeline_health": (pipe_score, pipe_details),
    }

    dimensions: dict[str, ScorecardDimension] = {}
    for key, (dim_name, weight) in DIMENSION_WEIGHTS.items():
        dim_score, dim_details = raw_dimensions[key]
        dimensions[key] = ScorecardDimension(
            name=dim_name,
            score=dim_score,
            grade=score_to_grade(dim_score),
            weight=weight,
            details=dim_details,
        )

    overall_score = _clamp_score(sum(d.score * d.weight for d in dimensions.values()))
    overall_grade = score_to_grade(overall_score)
    technical_debt_score = _clamp_score(100.0 - overall_score)

    # Deterministic remediation effort estimation (hours)
    ap_effort_map = {"CRITICAL": 2.0, "HIGH": 1.5, "MEDIUM": 1.0, "LOW": 0.5}
    vuln_effort_map = {"CRITICAL": 4.0, "HIGH": 2.0, "MEDIUM": 1.0, "LOW": 0.5}
    fit_effort_map = {"CRITICAL": 4.0, "HIGH": 2.5, "MEDIUM": 1.5, "LOW": 0.5}

    remediation_hours = 0.0
    for v in vulns:
        remediation_hours += _severity_penalty(
            str(_attr_or_key(v, "severity", "MEDIUM")), vuln_effort_map, 1.0
        )
    remediation_hours += len(sec_findings) * 2.0
    for fv in fitness:
        remediation_hours += _severity_penalty(
            str(_attr_or_key(fv, "severity", "HIGH")), fit_effort_map, 1.5
        )
    for ap in all_aps:
        remediation_hours += _severity_penalty(
            str(ap.get("severity", "MEDIUM")), ap_effort_map, 1.0
        )
    remediation_hours += dead_cnt * 0.25 + (dup_pct / 5.0) + oversized_files * 1.5
    remediation_hours += technical_debt_score * 0.25
    remediation_hours = round(max(0.0, remediation_hours), 2)

    return RepositoryScorecard(
        overall_score=overall_score,
        overall_grade=overall_grade,
        technical_debt_score=technical_debt_score,
        remediation_hours=remediation_hours,
        dimensions=dimensions,
    )
