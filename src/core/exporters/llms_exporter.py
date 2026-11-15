from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


def _safe_load_json(path: Path) -> Any:
    if not path.exists() or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return None


def _load_exports_snapshot(exports_latest_dir: Path) -> dict[str, Any]:
    root = Path(exports_latest_dir)

    repo_payload = _safe_load_json(root / "repos" / "repositories.json")
    if isinstance(repo_payload, dict):
        repo_items = [r for r in repo_payload.get("items", []) if isinstance(r, dict)]
    elif isinstance(repo_payload, list):
        repo_items = [r for r in repo_payload if isinstance(r, dict)]
    else:
        repo_items = []

    repos_by_key: dict[str, dict[str, Any]] = {}
    for item in repo_items:
        org = str(item.get("Organization", "")).strip()
        name = str(item.get("RepositoryName", item.get("name", ""))).strip()
        rid = str(item.get("RepositoryId", "")).strip()
        key = rid if "/" in rid else (f"{org}/{name}" if org and name else name)
        if key:
            repos_by_key[key] = item

    pipelines_by_key: dict[str, dict[str, Any]] = {}
    pipelines_dir = root / "pipelines"
    if pipelines_dir.is_dir():
        for pfile in sorted(pipelines_dir.glob("*-pipeline.json")):
            pdata = _safe_load_json(pfile)
            if not isinstance(pdata, dict):
                continue
            org = str(pdata.get("org", "")).strip()
            repo = str(pdata.get("repository", "")).strip()
            key = f"{org}/{repo}" if org and repo and "/" not in repo else (
                repo or pfile.stem.removesuffix("-pipeline")
            )
            pipelines_by_key[key] = pdata

    reports_by_key: dict[str, dict[str, Any]] = {}
    reports_dir = root / "reports"
    if reports_dir.is_dir():
        for rfile in sorted(reports_dir.glob("*-analysis.json")):
            rdata = _safe_load_json(rfile)
            if not isinstance(rdata, dict):
                continue
            key = str(rdata.get("repository", "")).strip() or rfile.stem.removesuffix("-analysis")
            reports_by_key[key] = rdata

    sboms_by_key: dict[str, dict[str, Any]] = {}
    sbom_dir = root / "sbom"
    if sbom_dir.is_dir():
        for sfile in sorted(sbom_dir.glob("*.cdx.json")):
            sdata = _safe_load_json(sfile)
            if not isinstance(sdata, dict):
                continue
            comp_name = str(
                sdata.get("metadata", {}).get("component", {}).get("name", "")
            ).strip()
            key = comp_name or sfile.name.removesuffix(".cdx.json")
            sboms_by_key[key] = sdata

    return {
        "repos": repos_by_key,
        "pipelines": pipelines_by_key,
        "reports": reports_by_key,
        "sboms": sboms_by_key,
    }


def _resolve_match(key: str, mapping: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if key in mapping:
        return mapping[key]
    short = key.split("/")[-1].lower()
    dash_key = key.replace("/", "-").lower()
    for mk, mv in mapping.items():
        mk_low = mk.lower()
        if mk_low == key.lower() or mk_low == dash_key or mk_low.split("/")[-1] == short:
            return mv
    return None


def build_llms_txt(exports_latest_dir: Path) -> str:
    """
    Build a concise deterministic `llms.txt` architectural index summarizing discovered
    repositories, ecosystems, scorecards, workflows, and SBOM artifacts (FR-029).
    """
    snap = _load_exports_snapshot(exports_latest_dir)
    repos: dict[str, dict[str, Any]] = snap["repos"]
    pipelines: dict[str, dict[str, Any]] = snap["pipelines"]
    reports: dict[str, dict[str, Any]] = snap["reports"]
    sboms: dict[str, dict[str, Any]] = snap["sboms"]

    all_keys = sorted(set(repos) | set(pipelines) | set(reports) | set(sboms))
    lang_counts: Counter[str] = Counter()
    for key in all_keys:
        inv = _resolve_match(key, repos) or {}
        rep = _resolve_match(key, reports) or {}
        lang = str(inv.get("PrimaryLanguage") or rep.get("ecosystem") or "Unknown")
        lang_counts[lang] += 1

    lang_summary = ", ".join(f"{k}: {v}" for k, v in sorted(lang_counts.items())) or "None"
    total_workflows = sum(
        len(p.get("workflows", []))
        for p in pipelines.values()
        if isinstance(p.get("workflows"), list)
    )

    lines: list[str] = [
        "# Atruss Code Atlas",
        "",
        (
            f"> Architectural & CI/CD observability index for {len(all_keys)} repositories "
            f"({lang_summary}); {total_workflows} workflow(s), {len(sboms)} CycloneDX SBOM(s)."
        ),
        "",
        "## Repositories",
        "",
    ]

    if not all_keys:
        lines.append("- No repositories exported yet.")
    else:
        for key in all_keys:
            inv = _resolve_match(key, repos) or {}
            rep = _resolve_match(key, reports) or {}
            pip = _resolve_match(key, pipelines) or {}
            sbom = _resolve_match(key, sboms)

            eco = str(inv.get("PrimaryLanguage") or rep.get("ecosystem") or "Unknown")
            fw = str(
                inv.get("FrameworkType")
                or (rep.get("metrics") or {}).get("framework")
                or "Unknown"
            )
            sc = rep.get("scorecard") if isinstance(rep.get("scorecard"), dict) else None
            grade_str = (
                f"Grade {sc.get('overall_grade', '?')} ({sc.get('overall_score', 0):.1f}/100)"
                if sc
                else "Not Scored"
            )
            if isinstance(pip.get("workflows"), list):
                wf_count = len(pip["workflows"])
            elif isinstance(rep.get("pipelines"), list):
                wf_count = len(rep["pipelines"])
            else:
                wf_count = 0
            comp_count = len(rep.get("architecture_components", []) or [])
            safe_slug = key.replace("/", "-")
            sbom_note = f", SBOM: `sbom/{safe_slug}.cdx.json`" if sbom else ""
            lines.append(
                f"- **{key}** ({eco} / {fw}) — {grade_str}, {comp_count} components, "
                f"{wf_count} workflows | Report: `reports/{safe_slug}-analysis.json`, "
                f"Pipeline: `pipelines/{safe_slug}-pipeline.json`{sbom_note}"
            )

    lines.extend([
        "",
        "## Context Artifacts",
        "",
        "- [Full Architectural Context](llms-full.txt): "
        "Detailed component boundaries, 6-D scorecards, CI/CD DAGs, CVEs, and Code-to-Cloud edges.",
        "- [Discovery Inventory](repos/repositories.json): 27-column repository catalog.",
        "- [Pipeline Topology](relationships/pipeline_topology.json): "
        "Cross-repository workflow and deployment target topology.",
        "",
        "## MCP Read-Only Tools (`atruss mcp`)",
        "",
        "- `list_repositories`, `get_repo_architecture`, `get_pipeline_dag`, "
        "`find_cross_repo_impacts`, `get_blast_radius`, `trace_entrypoint_chain`, "
        "`get_security_findings`, `query_antipatterns`, `get_repo_scorecard`, "
        "`check_boundary_violation`",
        "",
    ])
    return "\n".join(lines)


def build_llms_full_txt(exports_latest_dir: Path) -> str:
    """
    Build a detailed deterministic `llms-full.txt` context map containing architecture
    boundaries, scorecards, CI/CD workflows, dependencies/CVEs, and Code-to-Cloud edges (FR-029).
    """
    snap = _load_exports_snapshot(exports_latest_dir)
    repos: dict[str, dict[str, Any]] = snap["repos"]
    pipelines: dict[str, dict[str, Any]] = snap["pipelines"]
    reports: dict[str, dict[str, Any]] = snap["reports"]
    sboms: dict[str, dict[str, Any]] = snap["sboms"]

    all_keys = sorted(set(repos) | set(pipelines) | set(reports) | set(sboms))

    lines: list[str] = [
        "# Atruss Code Atlas — Full Architectural & Pipeline Context",
        "",
        f"Total Indexed Repositories: {len(all_keys)}",
        "",
    ]

    for key in all_keys:
        inv = _resolve_match(key, repos) or {}
        rep = _resolve_match(key, reports) or {}
        pip = _resolve_match(key, pipelines) or {}
        sbom = _resolve_match(key, sboms) or {}

        eco = str(inv.get("PrimaryLanguage") or rep.get("ecosystem") or "Unknown")
        fw = str(
            inv.get("FrameworkType")
            or (rep.get("metrics") or {}).get("framework")
            or "Unknown"
        )
        sha = str(rep.get("sha") or pip.get("sha") or "unknown")

        lines.extend([
            f"## Repository: {key}",
            f"- Ecosystem: {eco}",
            f"- Framework: {fw}",
            f"- SHA: `{sha}`",
        ])

        # 1. Scorecard
        sc = rep.get("scorecard")
        if isinstance(sc, dict):
            lines.extend([
                "",
                "### 6-Dimension Scorecard",
                (
                    f"- Overall: {sc.get('overall_grade', '?')} "
                    f"({sc.get('overall_score', 0.0)}/100), "
                    f"Technical Debt: {sc.get('technical_debt_score', 0.0)}, "
                    f"Remediation Hours: {sc.get('remediation_hours', 0.0)}h"
                ),
            ])
            dims = sc.get("dimensions") or {}
            for dim_key in sorted(dims.keys()):
                dim = dims[dim_key]
                if isinstance(dim, dict):
                    lines.append(
                        f"- {dim.get('name', dim_key)}: {dim.get('grade', '?')} "
                        f"({dim.get('score', 0.0)}) — {dim.get('details', '')}"
                    )

        # 2. Architecture Boundaries & Fitness Violations
        comps = [
            c for c in (rep.get("architecture_components") or []) if isinstance(c, dict)
        ]
        if comps:
            lines.extend(["", "### Architecture Components"])
            sorted_comps = sorted(
                comps,
                key=lambda c: (
                    str(c.get("type", "")),
                    str(c.get("name", "")),
                    str(c.get("file", "")),
                ),
            )
            for comp in sorted_comps[:80]:
                deps_str = ", ".join(sorted(str(d) for d in comp.get("dependencies", [])))
                dep_suffix = f" -> [{deps_str}]" if deps_str else ""
                lines.append(
                    f"- [{comp.get('type', 'COMPONENT')}] {comp.get('name', '')} "
                    f"(`{comp.get('file', '')}`){dep_suffix}"
                )
            if len(sorted_comps) > 80:
                lines.append(f"- ... ({len(sorted_comps) - 80} more components)")

        fvs = [v for v in (rep.get("fitness_violations") or []) if isinstance(v, dict)]
        if fvs:
            lines.extend(["", "### Architectural Fitness Violations"])
            for fv in sorted(
                fvs,
                key=lambda v: (str(v.get("rule_id", "")), str(v.get("source_component", ""))),
            ):
                lines.append(
                    f"- [{fv.get('severity', 'HIGH')}] {fv.get('rule_id', '')}: "
                    f"{fv.get('message', '')}"
                )

        # 3. Code-to-Cloud Edges
        c2c = [e for e in (rep.get("code_to_cloud_edges") or []) if isinstance(e, dict)]
        if c2c:
            lines.extend(["", "### Code-to-Cloud Traceability"])
            for edge in sorted(
                c2c,
                key=lambda e: (
                    str(e.get("source_type", "")),
                    str(e.get("source", "")),
                    str(e.get("relationship", "")),
                    str(e.get("target", "")),
                ),
            ):
                lines.append(
                    f"- {edge.get('source', '')} ({edge.get('source_type', '')}) "
                    f"--[{edge.get('relationship', '')}]--> "
                    f"{edge.get('target', '')} ({edge.get('target_type', '')})"
                )

        # 4. CI/CD Workflows
        workflows: list[dict[str, Any]] = []
        if isinstance(pip.get("workflows"), list):
            workflows.extend(w for w in pip["workflows"] if isinstance(w, dict))
        elif isinstance(rep.get("pipelines"), list):
            workflows.extend(w for w in rep["pipelines"] if isinstance(w, dict))

        if workflows:
            lines.extend(["", "### CI/CD Workflows"])
            for wf in sorted(workflows, key=lambda w: str(w.get("id") or w.get("name") or "")):
                wf_name = str(wf.get("name") or wf.get("id") or "workflow")
                triggers = ", ".join(str(t) for t in (wf.get("triggers") or []))
                aps = wf.get("anti_patterns") or []
                lines.append(
                    f"- Workflow `{wf_name}` (triggers: {triggers or 'none'}, "
                    f"anti-patterns: {len(aps)})"
                )
                raw_jobs = wf.get("jobs")
                if isinstance(raw_jobs, list):
                    for job in raw_jobs:
                        if isinstance(job, dict):
                            needs = ", ".join(str(n) for n in (job.get("needs") or []))
                            runner_lbl = job.get("runner", "unspecified")
                            lines.append(
                                f"  - Job `{job.get('id', '')}` on `{runner_lbl}`"
                                + (f" (needs: {needs})" if needs else "")
                            )
                elif isinstance(raw_jobs, dict):
                    for jid in sorted(raw_jobs.keys()):
                        jdata = raw_jobs[jid]
                        needs_val = jdata.get("needs", []) if isinstance(jdata, dict) else []
                        needs_list = (
                            [needs_val]
                            if isinstance(needs_val, str)
                            else list(needs_val or [])
                        )
                        needs = ", ".join(str(n) for n in needs_list)
                        lines.append(
                            f"  - Job `{jid}`" + (f" (needs: {needs})" if needs else "")
                        )
                for ap in aps:
                    if isinstance(ap, dict):
                        lines.append(
                            f"  - Finding [{ap.get('severity', 'MEDIUM')}] "
                            f"{ap.get('type', '')}: {ap.get('message', '')}"
                        )

        # 5. Dependencies, CVEs & Secrets (analysis.json + CycloneDX SBOM)
        deps = [d for d in (rep.get("dependencies") or []) if isinstance(d, dict)]
        vulns = [v for v in (rep.get("vulnerabilities") or []) if isinstance(v, dict)]
        secrets = [s for s in (rep.get("secrets") or []) if isinstance(s, dict)]
        sbom_comps = [c for c in (sbom.get("components") or []) if isinstance(c, dict)]
        sbom_vulns = [v for v in (sbom.get("vulnerabilities") or []) if isinstance(v, dict)]

        if deps or vulns or secrets or sbom_comps or sbom_vulns:
            lines.extend(["", "### Dependencies & Security"])
            dep_total = len(deps) or len(sbom_comps)
            lines.append(
                f"- Dependencies: {dep_total}, Vulnerabilities: {len(vulns) or len(sbom_vulns)}, "
                f"Secrets: {len(secrets)}"
            )
            for vuln in sorted(
                vulns, key=lambda v: (str(v.get("severity", "")), str(v.get("id", "")))
            ):
                lines.append(
                    f"  - [{vuln.get('severity', 'MEDIUM')}] {vuln.get('id', '')} in "
                    f"{vuln.get('package', '')} {vuln.get('installed_version', '')} "
                    f"(fixed: {vuln.get('fixed_version') or 'none'})"
                )
            if not vulns and sbom_vulns:
                for sv in sorted(sbom_vulns, key=lambda v: str(v.get("id", ""))):
                    ratings = sv.get("ratings") or [{}]
                    sev = str(ratings[0].get("severity", "medium")).upper() if ratings else "MEDIUM"
                    lines.append(
                        f"  - [{sev}] {sv.get('id', '')}: {sv.get('description', '')}"
                    )
            for sec in sorted(
                secrets, key=lambda s: (str(s.get("file_source", "")), int(s.get("start_line", 1)))
            ):
                lines.append(
                    f"  - Secret [{sec.get('severity', 'HIGH')}] {sec.get('rule_id', '')} "
                    f"at `{sec.get('file_source', '')}:{sec.get('start_line', 1)}`"
                )

        lines.append("")

    return "\n".join(lines)


def export_llms_context(
    exports_latest_dir: Path,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    """
    Generate and write deterministic `llms.txt` and `llms-full.txt` into `output_dir`
    (defaulting to `{exports_latest_dir}/llms/`) (FR-029).
    """
    latest_path = Path(exports_latest_dir)
    target_dir = Path(output_dir) if output_dir is not None else (latest_path / "llms")
    target_dir.mkdir(parents=True, exist_ok=True)

    llms_path = target_dir / "llms.txt"
    llms_full_path = target_dir / "llms-full.txt"

    llms_path.write_text(build_llms_txt(latest_path), encoding="utf-8")
    llms_full_path.write_text(build_llms_full_txt(latest_path), encoding="utf-8")
    return llms_path, llms_full_path
