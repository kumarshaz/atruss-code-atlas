from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_GRADE_RANK: dict[str, int] = {"A": 5, "B": 4, "C": 3, "D": 2, "F": 1}
_HIGH_SEVERITIES: frozenset[str] = frozenset({"CRITICAL", "HIGH"})
_NUMERIC_METRIC_KEYS: tuple[str, ...] = (
    "files_analyzed",
    "loc",
    "sloc",
    "component_count",
    "avg_cyclomatic_complexity",
    "max_cyclomatic_complexity",
    "avg_cognitive_complexity",
    "max_cognitive_complexity",
    "duplication_pct",
    "dead_code_count",
)


def resolve_snapshot_dir(path: Path) -> Path:
    """Resolve an archival snapshot path, descending into `latest/` if passed a root exports dir."""
    if (
        (path / "latest").is_dir()
        and not (path / "repos").exists()
        and not (path / "reports").exists()
    ):
        return path / "latest"
    return path


def _safe_load_json(path: Path) -> Any:
    if not path.exists() or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return None


def _load_repo_inventory(snapshot_dir: Path) -> dict[str, dict[str, Any]]:
    payload = _safe_load_json(snapshot_dir / "repos" / "repositories.json")
    if isinstance(payload, dict):
        items = payload.get("items", [])
    elif isinstance(payload, list):
        items = payload
    else:
        items = []

    inventory: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        org = str(item.get("Organization", "")).strip()
        name = str(item.get("RepositoryName", item.get("name", ""))).strip()
        repo_id = str(item.get("RepositoryId", "")).strip()
        if "/" in repo_id:
            key = repo_id
        elif org and name:
            key = f"{org}/{name}"
        else:
            key = name or repo_id
        if key:
            inventory[key] = item
    return inventory


def _load_pipeline_snapshots(snapshot_dir: Path) -> dict[str, dict[str, Any]]:
    pipelines_dir = snapshot_dir / "pipelines"
    result: dict[str, dict[str, Any]] = {}
    if not pipelines_dir.is_dir():
        return result

    for pfile in sorted(pipelines_dir.glob("*-pipeline.json")):
        data = _safe_load_json(pfile)
        if not isinstance(data, dict):
            continue
        org = str(data.get("org", "")).strip()
        repo = str(data.get("repository", "")).strip()
        if org and repo and "/" not in repo:
            key = f"{org}/{repo}"
        elif repo:
            key = repo
        else:
            key = pfile.stem.removesuffix("-pipeline")
        result[key] = data
    return result


def _load_report_snapshots(snapshot_dir: Path) -> dict[str, dict[str, Any]]:
    reports_dir = snapshot_dir / "reports"
    result: dict[str, dict[str, Any]] = {}
    if not reports_dir.is_dir():
        return result

    for rfile in sorted(reports_dir.glob("*-analysis.json")):
        data = _safe_load_json(rfile)
        if not isinstance(data, dict):
            continue
        repo = str(data.get("repository", "")).strip()
        if not repo:
            repo = rfile.stem.removesuffix("-analysis")
        result[repo] = data
    return result


def _extract_pipeline_jobs_and_aps(
    repo_key: str,
    pipeline_data: dict[str, Any] | None,
    report_data: dict[str, Any] | None,
) -> tuple[set[tuple[str, str]], dict[tuple[str, str, str], dict[str, Any]]]:
    jobs_set: set[tuple[str, str]] = set()
    aps_map: dict[tuple[str, str, str], dict[str, Any]] = {}

    workflows: list[dict[str, Any]] = []
    if isinstance(pipeline_data, dict) and isinstance(pipeline_data.get("workflows"), list):
        workflows.extend(wf for wf in pipeline_data["workflows"] if isinstance(wf, dict))
    if isinstance(report_data, dict) and isinstance(report_data.get("pipelines"), list):
        workflows.extend(wf for wf in report_data["pipelines"] if isinstance(wf, dict))

    for wf in workflows:
        wf_name = str(wf.get("id") or wf.get("path") or wf.get("name") or "workflow")
        raw_jobs = wf.get("jobs")
        if isinstance(raw_jobs, list):
            for job in raw_jobs:
                if isinstance(job, dict) and job.get("id"):
                    jobs_set.add((wf_name, str(job["id"])))
        elif isinstance(raw_jobs, dict):
            for jid in raw_jobs:
                jobs_set.add((wf_name, str(jid)))

        for ap in wf.get("anti_patterns", []) if isinstance(wf.get("anti_patterns"), list) else []:
            if not isinstance(ap, dict):
                continue
            ap_type = str(ap.get("type", ""))
            ap_msg = str(ap.get("message", ""))
            ap_sev = str(ap.get("severity", "MEDIUM")).upper()
            dedup_key = (wf_name, ap_type, ap_msg)
            aps_map[dedup_key] = {
                "repository": repo_key,
                "workflow": wf_name,
                "rule_id": str(ap.get("rule_id", "")),
                "type": ap_type,
                "severity": ap_sev,
                "message": ap_msg,
            }

    return jobs_set, aps_map


def _index_components(
    repo_key: str, report: dict[str, Any] | None
) -> dict[tuple[str, str, str], dict[str, Any]]:
    comps: dict[tuple[str, str, str], dict[str, Any]] = {}
    if not isinstance(report, dict):
        return comps
    for comp in report.get("architecture_components", []) or []:
        if not isinstance(comp, dict):
            continue
        name = str(comp.get("name", ""))
        ctype = str(comp.get("type", ""))
        fpath = str(comp.get("file", ""))
        key = (name, ctype, fpath)
        comps[key] = {
            "repository": repo_key,
            "name": name,
            "type": ctype,
            "file": fpath,
        }
    return comps


def _index_fitness_violations(
    repo_key: str,
    report: dict[str, Any] | None,
) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    out: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    if not isinstance(report, dict):
        return out
    for fv in report.get("fitness_violations", []) or []:
        if not isinstance(fv, dict):
            continue
        rule_id = str(fv.get("rule_id", ""))
        src = str(fv.get("source_component", ""))
        dst = str(fv.get("target_component", ""))
        ftype = str(fv.get("type", ""))
        sev = str(fv.get("severity", "HIGH")).upper()
        key = (rule_id, ftype, src, dst)
        out[key] = {
            "repository": repo_key,
            "rule_id": rule_id,
            "type": ftype,
            "severity": sev,
            "source_component": src,
            "target_component": dst,
            "message": str(fv.get("message", "")),
        }
    return out


def _index_vulnerabilities(
    repo_key: str,
    report: dict[str, Any] | None,
) -> dict[tuple[str, str, str], dict[str, Any]]:
    out: dict[tuple[str, str, str], dict[str, Any]] = {}
    if not isinstance(report, dict):
        return out
    for vuln in report.get("vulnerabilities", []) or []:
        if not isinstance(vuln, dict):
            continue
        vid = str(vuln.get("id", ""))
        purl = str(vuln.get("purl", ""))
        pkg = str(vuln.get("package", ""))
        sev = str(vuln.get("severity", "MEDIUM")).upper()
        key = (vid, purl, pkg)
        out[key] = {
            "repository": repo_key,
            "id": vid,
            "package": pkg,
            "purl": purl,
            "severity": sev,
            "summary": str(vuln.get("summary", "")),
        }
    return out


def _index_secrets(
    repo_key: str,
    report: dict[str, Any] | None,
) -> dict[tuple[str, str, int], dict[str, Any]]:
    out: dict[tuple[str, str, int], dict[str, Any]] = {}
    if not isinstance(report, dict):
        return out
    for sec in report.get("secrets", []) or []:
        if not isinstance(sec, dict):
            continue
        rule_id = str(sec.get("rule_id", ""))
        fpath = str(sec.get("file_source", ""))
        line = int(sec.get("start_line", 1) or 1)
        sev = str(sec.get("severity", "HIGH")).upper()
        key = (rule_id, fpath, line)
        out[key] = {
            "repository": repo_key,
            "rule_id": rule_id,
            "type": str(sec.get("type", "HARDCODED_SECRET")),
            "severity": sev,
            "file_source": fpath,
            "start_line": line,
            "message": str(sec.get("message", "")),
        }
    return out


def _grade_dropped(from_grade: str, to_grade: str) -> bool:
    return _GRADE_RANK.get(to_grade.upper(), 0) < _GRADE_RANK.get(from_grade.upper(), 0)


def compute_drift_report(baseline_dir: Path, target_dir: Path) -> dict[str, Any]:
    """
    Compare two archival export snapshots (baseline vs. target) across inventory,
    pipeline topologies/anti-patterns, architecture components, fitness violations,
    metrics, vulnerabilities/secrets, and 6-Dimension scorecards (FR-027).
    """
    base_dir = resolve_snapshot_dir(Path(baseline_dir))
    tgt_dir = resolve_snapshot_dir(Path(target_dir))

    base_inv = _load_repo_inventory(base_dir)
    tgt_inv = _load_repo_inventory(tgt_dir)

    added_repos = sorted(k for k in tgt_inv if k not in base_inv)
    removed_repos = sorted(k for k in base_inv if k not in tgt_inv)
    changed_repos: list[dict[str, Any]] = []
    for repo_key in sorted(set(base_inv) & set(tgt_inv)):
        b_item = base_inv[repo_key]
        t_item = tgt_inv[repo_key]
        diffs: dict[str, dict[str, Any]] = {}
        for field_name in ("PrimaryLanguage", "FrameworkType", "DocumentationPriority"):
            b_val = b_item.get(field_name)
            t_val = t_item.get(field_name)
            if b_val != t_val:
                diffs[field_name] = {"from": b_val, "to": t_val}
        if diffs:
            changed_repos.append({"repository": repo_key, "changes": diffs})

    base_pipes = _load_pipeline_snapshots(base_dir)
    tgt_pipes = _load_pipeline_snapshots(tgt_dir)
    base_reports = _load_report_snapshots(base_dir)
    tgt_reports = _load_report_snapshots(tgt_dir)

    all_pipe_repos = sorted(set(base_pipes) | set(tgt_pipes) | set(base_reports) | set(tgt_reports))
    added_jobs: list[dict[str, str]] = []
    removed_jobs: list[dict[str, str]] = []
    new_antipatterns: list[dict[str, Any]] = []
    resolved_antipatterns: list[dict[str, Any]] = []

    for repo_key in all_pipe_repos:
        b_jobs, b_aps = _extract_pipeline_jobs_and_aps(
            repo_key, base_pipes.get(repo_key), base_reports.get(repo_key)
        )
        t_jobs, t_aps = _extract_pipeline_jobs_and_aps(
            repo_key, tgt_pipes.get(repo_key), tgt_reports.get(repo_key)
        )
        for wf_name, jid in sorted(t_jobs - b_jobs):
            added_jobs.append({"repository": repo_key, "workflow": wf_name, "job": jid})
        for wf_name, jid in sorted(b_jobs - t_jobs):
            removed_jobs.append({"repository": repo_key, "workflow": wf_name, "job": jid})
        for ap_key in sorted(set(t_aps) - set(b_aps)):
            new_antipatterns.append(t_aps[ap_key])
        for ap_key in sorted(set(b_aps) - set(t_aps)):
            resolved_antipatterns.append(b_aps[ap_key])

    all_report_repos = sorted(set(base_reports) | set(tgt_reports))
    added_components: list[dict[str, Any]] = []
    removed_components: list[dict[str, Any]] = []
    new_fitness: list[dict[str, Any]] = []
    resolved_fitness: list[dict[str, Any]] = []
    new_vulns: list[dict[str, Any]] = []
    resolved_vulns: list[dict[str, Any]] = []
    new_secrets: list[dict[str, Any]] = []
    resolved_secrets: list[dict[str, Any]] = []
    metric_deltas: dict[str, dict[str, dict[str, float]]] = {}
    scorecard_transitions: dict[str, dict[str, Any]] = {}

    regressions: list[dict[str, Any]] = []

    for repo_key in all_report_repos:
        b_rep = base_reports.get(repo_key)
        t_rep = tgt_reports.get(repo_key)

        b_comps = _index_components(repo_key, b_rep)
        t_comps = _index_components(repo_key, t_rep)
        for ckey in sorted(set(t_comps) - set(b_comps)):
            added_components.append(t_comps[ckey])
        for ckey in sorted(set(b_comps) - set(t_comps)):
            removed_components.append(b_comps[ckey])

        b_fit = _index_fitness_violations(repo_key, b_rep)
        t_fit = _index_fitness_violations(repo_key, t_rep)
        for fkey in sorted(set(t_fit) - set(b_fit)):
            new_fitness.append(t_fit[fkey])
        for fkey in sorted(set(b_fit) - set(t_fit)):
            resolved_fitness.append(b_fit[fkey])

        b_vuln = _index_vulnerabilities(repo_key, b_rep)
        t_vuln = _index_vulnerabilities(repo_key, t_rep)
        for vkey in sorted(set(t_vuln) - set(b_vuln)):
            new_vulns.append(t_vuln[vkey])
        for vkey in sorted(set(b_vuln) - set(t_vuln)):
            resolved_vulns.append(b_vuln[vkey])

        b_sec = _index_secrets(repo_key, b_rep)
        t_sec = _index_secrets(repo_key, t_rep)
        for skey in sorted(set(t_sec) - set(b_sec)):
            new_secrets.append(t_sec[skey])
        for skey in sorted(set(b_sec) - set(t_sec)):
            resolved_secrets.append(b_sec[skey])

        if isinstance(b_rep, dict) and isinstance(t_rep, dict):
            b_metrics = b_rep.get("metrics") or {}
            t_metrics = t_rep.get("metrics") or {}
            repo_m_deltas: dict[str, dict[str, float]] = {}
            for mkey in _NUMERIC_METRIC_KEYS:
                if mkey in b_metrics or mkey in t_metrics:
                    b_val = float(b_metrics.get(mkey, 0.0) or 0.0)
                    t_val = float(t_metrics.get(mkey, 0.0) or 0.0)
                    delta = round(t_val - b_val, 2)
                    if delta != 0.0:
                        repo_m_deltas[mkey] = {"from": b_val, "to": t_val, "delta": delta}
            if repo_m_deltas:
                metric_deltas[repo_key] = repo_m_deltas

            b_sc = b_rep.get("scorecard")
            t_sc = t_rep.get("scorecard")
            if isinstance(b_sc, dict) and isinstance(t_sc, dict):
                b_overall_score = float(b_sc.get("overall_score", 0.0) or 0.0)
                t_overall_score = float(t_sc.get("overall_score", 0.0) or 0.0)
                b_overall_grade = str(b_sc.get("overall_grade", ""))
                t_overall_grade = str(t_sc.get("overall_grade", ""))
                b_debt = float(b_sc.get("technical_debt_score", 0.0) or 0.0)
                t_debt = float(t_sc.get("technical_debt_score", 0.0) or 0.0)
                debt_delta = round(t_debt - b_debt, 2)

                dim_transitions: dict[str, dict[str, Any]] = {}
                b_dims = b_sc.get("dimensions") or {}
                t_dims = t_sc.get("dimensions") or {}
                for dim_key in sorted(set(b_dims) & set(t_dims)):
                    bd = b_dims[dim_key]
                    td = t_dims[dim_key]
                    if not isinstance(bd, dict) or not isinstance(td, dict):
                        continue
                    b_dg = str(bd.get("grade", ""))
                    t_dg = str(td.get("grade", ""))
                    b_ds = float(bd.get("score", 0.0) or 0.0)
                    t_ds = float(td.get("score", 0.0) or 0.0)
                    d_delta = round(t_ds - b_ds, 2)
                    if b_dg != t_dg or d_delta != 0.0:
                        dim_transitions[dim_key] = {
                            "from": b_dg,
                            "to": t_dg,
                            "from_score": b_ds,
                            "to_score": t_ds,
                            "delta": d_delta,
                        }
                    if b_dg and t_dg and _grade_dropped(b_dg, t_dg):
                        regressions.append({
                            "repository": repo_key,
                            "category": "scorecard_dimension",
                            "dimension": dim_key,
                            "severity": "HIGH",
                            "message": (
                                f"Scorecard dimension '{dim_key}' dropped from {b_dg} to {t_dg} "
                                f"({d_delta:+.2f})."
                            ),
                        })

                if b_overall_grade and t_overall_grade and _grade_dropped(
                    b_overall_grade, t_overall_grade
                ):
                    regressions.append({
                        "repository": repo_key,
                        "category": "scorecard_overall",
                        "severity": "HIGH",
                        "message": (
                            f"Overall scorecard grade dropped from {b_overall_grade} to "
                            f"{t_overall_grade} ({t_overall_score - b_overall_score:+.2f})."
                        ),
                    })

                if debt_delta > 5.0:
                    regressions.append({
                        "repository": repo_key,
                        "category": "technical_debt",
                        "severity": "HIGH",
                        "message": (
                            f"Technical debt score increased by {debt_delta:.2f} "
                            f"({b_debt:.2f} -> {t_debt:.2f})."
                        ),
                    })

                scorecard_transitions[repo_key] = {
                    "overall": {
                        "from": b_overall_grade,
                        "to": t_overall_grade,
                        "from_score": b_overall_score,
                        "to_score": t_overall_score,
                        "delta": round(t_overall_score - b_overall_score, 2),
                    },
                    "technical_debt": {
                        "from": b_debt,
                        "to": t_debt,
                        "delta": debt_delta,
                    },
                    "dimensions": dim_transitions,
                }

    # Check high/critical new findings for regressions
    for ap in new_antipatterns:
        if ap["severity"] in _HIGH_SEVERITIES:
            regressions.append({
                "repository": ap["repository"],
                "category": "pipeline_antipattern",
                "severity": ap["severity"],
                "message": (
                    f"New {ap['severity']} pipeline anti-pattern {ap['type']} "
                    f"in {ap['workflow']}."
                ),
            })

    for fv in new_fitness:
        if fv["severity"] in _HIGH_SEVERITIES:
            regressions.append({
                "repository": fv["repository"],
                "category": "fitness_violation",
                "severity": fv["severity"],
                "message": (
                    f"New {fv['severity']} fitness violation {fv['rule_id']}: "
                    f"{fv['source_component']} -> {fv['target_component']}."
                ),
            })

    for vuln in new_vulns:
        if vuln["severity"] in _HIGH_SEVERITIES:
            regressions.append({
                "repository": vuln["repository"],
                "category": "vulnerability",
                "severity": vuln["severity"],
                "message": (
                    f"New {vuln['severity']} vulnerability {vuln['id']} ({vuln['package']})."
                ),
            })

    for sec in new_secrets:
        if sec["severity"] in _HIGH_SEVERITIES:
            regressions.append({
                "repository": sec["repository"],
                "category": "secret",
                "severity": sec["severity"],
                "message": (
                    f"New {sec['severity']} secret {sec['rule_id']} in {sec['file_source']}."
                ),
            })

    regressions.sort(
        key=lambda r: (r["repository"], r["category"], r["severity"], r["message"])
    )
    has_regression = len(regressions) > 0

    summary: dict[str, Any] = {
        "baseline_dir": str(base_dir),
        "target_dir": str(tgt_dir),
        "added_repos_count": len(added_repos),
        "removed_repos_count": len(removed_repos),
        "changed_repos_count": len(changed_repos),
        "added_components_count": len(added_components),
        "removed_components_count": len(removed_components),
        "added_jobs_count": len(added_jobs),
        "removed_jobs_count": len(removed_jobs),
        "new_antipatterns_count": len(new_antipatterns),
        "resolved_antipatterns_count": len(resolved_antipatterns),
        "new_fitness_violations_count": len(new_fitness),
        "resolved_fitness_violations_count": len(resolved_fitness),
        "new_vulnerabilities_count": len(new_vulns),
        "resolved_vulnerabilities_count": len(resolved_vulns),
        "new_secrets_count": len(new_secrets),
        "resolved_secrets_count": len(resolved_secrets),
        "regressions_count": len(regressions),
    }

    return {
        "has_regression": has_regression,
        "summary": summary,
        "regressions": regressions,
        "inventory": {
            "added": added_repos,
            "removed": removed_repos,
            "changed": changed_repos,
        },
        "pipelines": {
            "added_jobs": added_jobs,
            "removed_jobs": removed_jobs,
            "new_antipatterns": new_antipatterns,
            "resolved_antipatterns": resolved_antipatterns,
        },
        "architecture": {
            "added_components": added_components,
            "removed_components": removed_components,
            "new_fitness_violations": new_fitness,
            "resolved_fitness_violations": resolved_fitness,
            "new_vulnerabilities": new_vulns,
            "resolved_vulnerabilities": resolved_vulns,
            "new_secrets": new_secrets,
            "resolved_secrets": resolved_secrets,
            "metric_deltas": metric_deltas,
        },
        "scorecard_transitions": scorecard_transitions,
    }


def render_drift_markdown(report: dict[str, Any]) -> str:
    """Render a deterministic Markdown summary of a compute_drift_report() output."""
    summary = report.get("summary", {})
    has_reg = bool(report.get("has_regression", False))
    status_label = "REGRESSION DETECTED" if has_reg else "NO REGRESSIONS"

    lines: list[str] = [
        "# Architectural & Pipeline Drift Report",
        "",
        f"- **Gate Status**: `{status_label}`",
        f"- **Baseline**: `{summary.get('baseline_dir', '')}`",
        f"- **Target**: `{summary.get('target_dir', '')}`",
        f"- **Regressions Count**: {summary.get('regressions_count', 0)}",
        "",
        "## Summary Counts",
        "",
        "| Dimension | Added / New | Removed / Resolved |",
        "| :--- | :---: | :---: |",
        (
            f"| Repositories | {summary.get('added_repos_count', 0)} "
            f"| {summary.get('removed_repos_count', 0)} |"
        ),
        (
            f"| Architecture Components | {summary.get('added_components_count', 0)} "
            f"| {summary.get('removed_components_count', 0)} |"
        ),
        (
            f"| Pipeline Jobs | {summary.get('added_jobs_count', 0)} "
            f"| {summary.get('removed_jobs_count', 0)} |"
        ),
        (
            f"| Pipeline Anti-Patterns | {summary.get('new_antipatterns_count', 0)} "
            f"| {summary.get('resolved_antipatterns_count', 0)} |"
        ),
        (
            f"| Fitness Violations | {summary.get('new_fitness_violations_count', 0)} "
            f"| {summary.get('resolved_fitness_violations_count', 0)} |"
        ),
        (
            f"| Vulnerabilities | {summary.get('new_vulnerabilities_count', 0)} "
            f"| {summary.get('resolved_vulnerabilities_count', 0)} |"
        ),
        (
            f"| Secrets | {summary.get('new_secrets_count', 0)} "
            f"| {summary.get('resolved_secrets_count', 0)} |"
        ),
        "",
    ]

    regressions = report.get("regressions", [])
    lines.append("## Regressions")
    lines.append("")
    if regressions:
        for reg in regressions:
            lines.append(
                f"- **[{reg.get('severity', 'HIGH')}]** `{reg.get('repository', '')}` "
                f"({reg.get('category', '')}): {reg.get('message', '')}"
            )
    else:
        lines.append("- None detected.")
    lines.append("")

    transitions = report.get("scorecard_transitions", {})
    if transitions:
        lines.append("## Scorecard Transitions")
        lines.append("")
        for repo_key, trans in sorted(transitions.items()):
            ov = trans.get("overall", {})
            debt = trans.get("technical_debt", {})
            lines.append(
                f"- **{repo_key}**: Overall `{ov.get('from', '?')}` -> `{ov.get('to', '?')}` "
                f"(score delta `{ov.get('delta', 0.0):+.2f}`, "
                f"debt delta `{debt.get('delta', 0.0):+.2f}`)"
            )
            for dim_k, dim_v in sorted((trans.get("dimensions") or {}).items()):
                lines.append(
                    f"  - `{dim_k}`: `{dim_v.get('from', '?')}` -> `{dim_v.get('to', '?')}` "
                    f"(`{dim_v.get('delta', 0.0):+.2f}`)"
                )
        lines.append("")

    return "\n".join(lines)
