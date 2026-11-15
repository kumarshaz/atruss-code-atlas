import re
from collections import Counter, defaultdict
from typing import Any

MAX_DIRECT_COMPONENTS = 25
MAX_DIRECT_EDGES = 50
MAX_TOP_BRANCHES = 5
MAX_CHILD_BRANCHES = 3
MAX_CROSS_EDGES = 12
MAX_DETAIL_ROWS = 60

MERMAID_CLASS_DEFS = [
    "  classDef atlasRoot fill:#004882,stroke:#a3c9ff,stroke-width:2px,color:#d3e4ff",
    "  classDef atlasCategory fill:#212428,stroke:#E87A48,stroke-width:1.5px,color:#dfe3eb",
    "  classDef atlasWorkflow fill:#1b2026,stroke:#a3c9ff,stroke-width:1.5px,color:#dfe3eb",
    "  classDef atlasJob fill:#171c22,stroke:#8d9199,stroke-width:1px,color:#dfe3eb",
    "  classDef atlasTarget fill:#005227,stroke:#8bd99b,stroke-width:1.5px,color:#a7f6b6",
    "  classDef atlasAlert fill:#93000a,stroke:#ffb4ab,stroke-width:1.5px,color:#ffdad6",
    "  classDef atlasMore fill:#252a31,stroke:#8d9199,stroke-dasharray:4 4,color:#c3c6cf",
]


def _mermaid_safe_id(raw: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", raw)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"n_{cleaned}"
    return cleaned


def _mermaid_label(raw: str) -> str:
    """Escape characters that break quoted Mermaid node labels."""
    text = str(raw).replace('"', "'").replace("\n", " ").replace("\r", " ")
    return text.replace("[", "(").replace("]", ")")


def _dir_segments(file_path: str) -> tuple[str, ...]:
    """Return normalized directory segments for a component file path."""
    norm = str(file_path or "").replace("\\", "/").strip("/")
    if not norm:
        return ("(root)",)
    parts = [p for p in norm.split("/") if p]
    if len(parts) <= 1:
        return ("(root)",)
    return tuple(parts[:-1])


def _field(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _format_metric_value(value: Any) -> str:
    if isinstance(value, list):
        return f"{len(value)} entry(ies)"
    if isinstance(value, dict):
        return f"{len(value)} field(s)"
    return str(value)


def _collect_violating_pairs(
    fitness_violations: list[Any] | None,
) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    raw_pairs: set[tuple[str, str]] = set()
    id_pairs: set[tuple[str, str]] = set()
    for fv in fitness_violations or []:
        vtype = str(_field(fv, "type", "")).strip().upper()
        target_layer = str(_field(fv, "target_layer", "")).strip().upper()
        if vtype == "COMPLEXITY_THRESHOLD" or target_layer == "THRESHOLD":
            continue
        src = str(_field(fv, "source_component", "")).strip()
        dst = str(_field(fv, "target_component", "")).strip()
        if src and dst:
            raw_pairs.add((src, dst))
            id_pairs.add((_mermaid_safe_id(src), _mermaid_safe_id(dst)))
    return raw_pairs, id_pairs


def _render_top_level_tree(
    repo_name: str,
    components: list[dict[str, Any]],
    violating_pairs: tuple[set[tuple[str, str]], set[tuple[str, str]]] | None = None,
) -> tuple[list[str], dict[tuple[str, ...], list[dict[str, Any]]]]:
    """Build a bounded top-down Mermaid tree diagram grouped by top-level directories."""
    lines: list[str] = []
    edge_count = 0
    root_id = "repo_root"
    lines.append(
        f'    {root_id}(["{_mermaid_label(repo_name)} ({len(components)} components)"]):::atlasRoot'
    )

    # Find adaptive base depth if a single top folder contains >80% of all components
    all_segs = [_dir_segments(c.get("file", "")) for c in components]
    prefix_len = 1
    while prefix_len < 3:
        buckets_at_depth: dict[tuple[str, ...], int] = Counter(
            s[: min(prefix_len, len(s))] for s in all_segs
        )
        if len(buckets_at_depth) != 1:
            break
        only_key = next(iter(buckets_at_depth))
        has_deeper = any(len(s) > len(only_key) for s in all_segs)
        if not has_deeper:
            break
        prefix_len += 1

    top_groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for comp, segs in zip(components, all_segs, strict=True):
        key = segs[: min(prefix_len, len(segs))]
        top_groups[key].append(comp)

    ranked_top = sorted(
        top_groups.items(),
        key=lambda item: (-len(item[1]), "/".join(item[0])),
    )
    shown_top = ranked_top[:MAX_TOP_BRANCHES]
    tail_top = ranked_top[MAX_TOP_BRANCHES:]

    comp_to_node: dict[str, str] = {}
    for idx, (top_key, group_comps) in enumerate(shown_top):
        top_label = "/".join(top_key)
        top_id = f"dir_{idx}_{_mermaid_safe_id(top_label)}"

        # Skip intermediate single-child wrapper folders (e.g. src/specify_cli or src/openai)
        # so large single-package roots expand into their actual sub-modules.
        next_depth = len(top_key)
        split_depth = next_depth
        comp_segs = [_dir_segments(c.get("file", "")) for c in group_comps]
        while split_depth < 6:
            keys_at_d = {
                s[split_depth] if len(s) > split_depth else "(module root)" for s in comp_segs
            }
            if len(keys_at_d) > 1 or keys_at_d == {"(module root)"}:
                break
            if not any(len(s) > split_depth + 1 for s in comp_segs):
                break
            split_depth += 1

        child_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for comp, segs in zip(group_comps, comp_segs, strict=True):
            if len(segs) > split_depth:
                sub_name = "/".join(segs[next_depth : split_depth + 1])
            elif len(segs) > next_depth:
                sub_name = "/".join(segs[next_depth:])
            else:
                sub_name = "(module root)"
            child_groups[sub_name].append(comp)

        if len(group_comps) > 8 and len(child_groups) > 1:
            sg_id = f"sg_{top_id}"
            sg_lbl = f"{_mermaid_label(top_label)} ({len(group_comps)})"
            lines.append(f'    subgraph {sg_id}["{sg_lbl}"]')
            lines.append("      direction TB")
            lines.append(f'      {top_id}["{sg_lbl}"]:::atlasCategory')

            ranked_children = sorted(
                child_groups.items(),
                key=lambda item: (-len(item[1]), item[0]),
            )
            shown_children = ranked_children[:MAX_CHILD_BRANCHES]
            tail_children = ranked_children[MAX_CHILD_BRANCHES:]

            for c_idx, (child_name, child_comps) in enumerate(shown_children):
                child_id = f"sub_{idx}_{c_idx}_{_mermaid_safe_id(child_name)}"
                child_lbl = f"{_mermaid_label(child_name)} ({len(child_comps)})"
                lines.append(f'      {child_id}["{child_lbl}"]:::atlasWorkflow')
                lines.append(f"      {top_id} --> {child_id}")
                edge_count += 1
                for comp in child_comps:
                    comp_to_node.setdefault(comp["name"], child_id)

            if tail_children:
                tail_count = sum(len(items) for _, items in tail_children)
                tail_id = f"sub_{idx}_more"
                tail_lbl = f"+{len(tail_children)} more submodules ({tail_count})"
                lines.append(f'      {tail_id}["{tail_lbl}"]:::atlasMore')
                lines.append(f"      {top_id} --> {tail_id}")
                edge_count += 1
                for _, child_comps in tail_children:
                    for comp in child_comps:
                        comp_to_node.setdefault(comp["name"], tail_id)

            lines.append("    end")
            lines.append(f"    {root_id} --> {top_id}")
            edge_count += 1
        else:
            lines.append(
                f'    {top_id}["{_mermaid_label(top_label)} ({len(group_comps)})"]:::atlasCategory'
            )
            lines.append(f"    {root_id} --> {top_id}")
            edge_count += 1
            for comp in group_comps:
                comp_to_node.setdefault(comp["name"], top_id)

    if tail_top:
        other_count = sum(len(items) for _, items in tail_top)
        other_id = "dir_other_modules"
        lines.append(
            f'    {other_id}["+{len(tail_top)} more modules ({other_count})"]:::atlasMore'
        )
        lines.append(f"    {root_id} --> {other_id}")
        edge_count += 1
        for _, group_comps in tail_top:
            for comp in group_comps:
                comp_to_node.setdefault(comp["name"], other_id)

    raw_v_pairs, id_v_pairs = violating_pairs if violating_pairs else (set(), set())
    violating_cross_edges: set[tuple[str, str]] = set()

    # Roll up inter-module dependency edges between visible tree nodes
    cross_edges: Counter[tuple[str, str]] = Counter()
    for comp in components:
        src_name = str(comp.get("name", ""))
        src_node = comp_to_node.get(src_name)
        if not src_node:
            continue
        for dep in comp.get("dependencies", []):
            dst_node = comp_to_node.get(dep)
            if dst_node and dst_node != src_node:
                cross_edges[(src_node, dst_node)] += 1
                if (src_name, dep) in raw_v_pairs or (
                    _mermaid_safe_id(src_name),
                    _mermaid_safe_id(dep),
                ) in id_v_pairs:
                    violating_cross_edges.add((src_node, dst_node))

    violating_indices: list[int] = []
    for (src_node, dst_node), weight in sorted(
        cross_edges.items(),
        key=lambda item: (-item[1], item[0][0], item[0][1]),
    )[:MAX_CROSS_EDGES]:
        unit = "dep" if weight == 1 else "deps"
        lines.append(f'    {src_node} -.->|"{weight} {unit}"| {dst_node}')
        if (src_node, dst_node) in violating_cross_edges:
            violating_indices.append(edge_count)
        edge_count += 1

    for e_idx in violating_indices:
        lines.append(f"    linkStyle {e_idx} stroke:#ba1a1a,stroke-width:2px,stroke-dasharray: 5 5")

    return lines, top_groups


def render_horizon2_sections_markdown(
    *,
    scorecard: Any = None,
    fitness_violations: list[Any] | None = None,
    dependencies: list[Any] | None = None,
    vulnerabilities: list[Any] | None = None,
    secrets: list[Any] | None = None,
    code_to_cloud_edges: list[Any] | None = None,
    workspace_packages: list[Any] | None = None,
    observability: dict[str, Any] | None = None,
) -> list[str]:
    """
    Render progressive-disclosure Markdown sections for Horizon 2 artifacts:
    6-Dimension Scorecard, Architectural Fitness & Workspaces, Supply Chain / CVEs /
    Redacted Secrets, and Section 7 Code-to-Cloud Traceability + Observability.
    Returns an empty list when all Horizon 2 inputs are absent/disabled.
    """
    fv_list = list(fitness_violations or [])
    dep_list = list(dependencies or [])
    vuln_list = list(vulnerabilities or [])
    sec_list = list(secrets or [])
    c2c_list = list(code_to_cloud_edges or [])
    wp_list = list(workspace_packages or [])
    obs_enabled = isinstance(observability, dict) and bool(observability.get("enabled"))

    if not any([
        scorecard is not None,
        fv_list,
        dep_list,
        vuln_list,
        sec_list,
        c2c_list,
        wp_list,
        obs_enabled,
    ]):
        return []

    lines: list[str] = []

    if scorecard is not None:
        overall_grade = str(_field(scorecard, "overall_grade", "?"))
        overall_score = float(_field(scorecard, "overall_score", 0.0) or 0.0)
        tech_debt = float(_field(scorecard, "technical_debt_score", 0.0) or 0.0)
        rem_hours = float(_field(scorecard, "remediation_hours", 0.0) or 0.0)
        dimensions = _field(scorecard, "dimensions", {}) or {}

        lines.extend([
            "## 6-Dimension Repository Scorecard",
            "",
            f"- **Overall Grade**: `{overall_grade}` ({overall_score:.2f}/100)",
            f"- **Technical Debt Score**: {tech_debt:.2f}",
            f"- **Estimated Remediation Effort**: {rem_hours:.2f}h",
            "",
        ])
        if isinstance(dimensions, dict) and dimensions:
            lines.extend([
                "| Dimension | Grade | Score | Weight | Details |",
                "| :--- | :---: | :---: | :---: | :--- |",
            ])
            for dim_key in sorted(dimensions.keys()):
                dim = dimensions[dim_key]
                d_name = str(_field(dim, "name", dim_key))
                d_grade = str(_field(dim, "grade", "?"))
                d_score = float(_field(dim, "score", 0.0) or 0.0)
                d_weight = float(_field(dim, "weight", 0.0) or 0.0)
                d_details = str(_field(dim, "details", "")).replace("|", "/")
                lines.append(
                    f"| {d_name} | `{d_grade}` | {d_score:.2f} | {d_weight:.2f} | {d_details} |"
                )
            lines.append("")

    if fv_list or wp_list:
        lines.extend(["## Architecture Fitness & Workspace Boundaries", ""])
        if fv_list:
            sorted_fvs = sorted(
                fv_list,
                key=lambda v: (
                    str(_field(v, "rule_id", "")),
                    str(_field(v, "source_component", "")),
                    str(_field(v, "target_component", "")),
                    str(_field(v, "file_source", "") or ""),
                ),
            )
            for fv in sorted_fvs[:40]:
                sev = str(_field(fv, "severity", "HIGH")).upper()
                rid = str(_field(fv, "rule_id", ""))
                ftype = str(_field(fv, "type", "LAYER_VIOLATION"))
                msg = str(_field(fv, "message", ""))
                lines.append(f"- **[{sev}] `{rid}` ({ftype})**: {msg}")
            if len(sorted_fvs) > 40:
                lines.append(f"- ... (+{len(sorted_fvs) - 40} more fitness violations)")
            lines.append("")

        if wp_list:
            lines.append("### Workspace Packages")
            sorted_wps = sorted(
                wp_list,
                key=lambda w: (
                    str(_field(w, "ecosystem", "")),
                    str(_field(w, "path", "")),
                    str(_field(w, "name", "")),
                ),
            )
            for wp in sorted_wps[:40]:
                wname = str(_field(wp, "name", ""))
                wpath = str(_field(wp, "path", "."))
                weco = str(_field(wp, "ecosystem", ""))
                wmgr = str(_field(wp, "manager", ""))
                ideps = sorted(str(d) for d in (_field(wp, "internal_dependencies", []) or []))
                mgr_suffix = f", {wmgr}" if wmgr else ""
                dep_suffix = f" -> internal deps: `{', '.join(ideps)}`" if ideps else ""
                lines.append(f"- **{wname}** (`{wpath}`, {weco}{mgr_suffix}){dep_suffix}")
            lines.append("")

    if dep_list or vuln_list or sec_list:
        lines.extend([
            "## Supply Chain Dependencies, Vulnerabilities & Secrets",
            "",
            (
                f"- **Dependencies Parsed**: {len(dep_list)} | "
                f"**Vulnerabilities**: {len(vuln_list)} | "
                f"**Secrets**: {len(sec_list)}"
            ),
            "",
        ])
        if vuln_list:
            lines.append("### Known Vulnerabilities (OSV)")
            sorted_vulns = sorted(
                vuln_list,
                key=lambda v: (
                    str(_field(v, "severity", "MEDIUM")),
                    str(_field(v, "id", "")),
                    str(_field(v, "package", "")),
                    str(_field(v, "manifest_file", "")),
                ),
            )
            for v in sorted_vulns[:40]:
                sev = str(_field(v, "severity", "MEDIUM")).upper()
                vid = str(_field(v, "id", ""))
                pkg = str(_field(v, "package", ""))
                inst = str(_field(v, "installed_version", ""))
                fixed = str(_field(v, "fixed_version", "") or "none")
                reach = str(_field(v, "reachability", "UNREACHABLE_DORMANT"))
                lines.append(
                    f"- **[{sev}] `{vid}`** `{pkg}` `{inst}` (fixed: `{fixed}`, {reach})"
                )
            lines.append("")

        if sec_list:
            lines.append("### Secret Findings (Redacted)")
            sorted_secs = sorted(
                sec_list,
                key=lambda s: (
                    str(_field(s, "file_source", "")),
                    int(_field(s, "start_line", 1) or 1),
                    str(_field(s, "rule_id", "")),
                ),
            )
            for s in sorted_secs[:40]:
                sev = str(_field(s, "severity", "HIGH")).upper()
                rid = str(_field(s, "rule_id", "ATRUSS-SEC-001"))
                fsrc = str(_field(s, "file_source", ""))
                sline = int(_field(s, "start_line", 1) or 1)
                redacted = str(_field(s, "redacted_snippet", "") or "***REDACTED***")
                lines.append(
                    f"- **[{sev}] `{rid}`** at `{fsrc}:{sline}` (`{redacted}`)"
                )
            lines.append("")

        if dep_list:
            lines.append("### Inventory Sample")
            sorted_deps = sorted(
                dep_list,
                key=lambda d: (
                    0 if bool(_field(d, "is_direct", True)) else 1,
                    str(_field(d, "ecosystem", "")),
                    str(_field(d, "name", "")),
                    str(_field(d, "version", "")),
                ),
            )
            for d in sorted_deps[:30]:
                dname = str(_field(d, "name", ""))
                dver = str(_field(d, "version", ""))
                deco = str(_field(d, "ecosystem", ""))
                man = str(_field(d, "manifest_file", ""))
                ver_s = f"`{dver}`" if dver else "`*`"
                lines.append(f"- `{dname}` {ver_s} ({deco}, `{man}`)")
            if len(sorted_deps) > 30:
                lines.append(f"- ... (+{len(sorted_deps) - 30} more dependencies)")
            lines.append("")

    if c2c_list or obs_enabled:
        lines.extend(["## Section 7: Code-to-Cloud Deployment Traceability", ""])
        if c2c_list:
            from src.analyzers.traceability import render_code_to_cloud_mermaid
            from src.models.artifacts import CodeToCloudEdge

            edge_models: list[CodeToCloudEdge] = []
            for e in c2c_list:
                if isinstance(e, CodeToCloudEdge):
                    edge_models.append(e)
                elif isinstance(e, dict):
                    edge_models.append(CodeToCloudEdge(**e))
            mermaid_c2c = render_code_to_cloud_mermaid(edge_models)
            if mermaid_c2c:
                lines.extend(["```mermaid", mermaid_c2c, "```", ""])

            sorted_edges = sorted(
                edge_models,
                key=lambda e: (e.source_type, e.source, e.relationship, e.target_type, e.target),
            )
            for edge in sorted_edges[:40]:
                lines.append(
                    f"- `{edge.source}` ({edge.source_type}) --[{edge.relationship}]--> "
                    f"`{edge.target}` ({edge.target_type})"
                )
            lines.append("")

        if obs_enabled and isinstance(observability, dict):
            cov_pct = observability.get("coverage_percent")
            cov_str = f"{float(cov_pct):.2f}%" if cov_pct is not None else "unavailable"
            lines.extend([
                "### Runtime Observability & Coverage Overlay",
                (
                    f"- **Hot Paths**: {observability.get('hot_paths', 0)} | "
                    f"**Covered Static**: {observability.get('covered_static', 0)} | "
                    f"**Dead / Unobserved**: {observability.get('dead_unobserved', 0)} | "
                    f"**Coverage**: {cov_str}"
                ),
                "",
            ])

    return lines


def generate_arc42_markdown(
    repo_name: str,
    components: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
    ecosystem: str = "Unknown",
    framework: str = "Unknown",
    sha: str = "unknown",
    include_frontmatter: bool = True,
    *,
    scorecard: Any = None,
    fitness_violations: list[Any] | None = None,
    dependencies: list[Any] | None = None,
    vulnerabilities: list[Any] | None = None,
    secrets: list[Any] | None = None,
    code_to_cloud_edges: list[Any] | None = None,
    workspace_packages: list[Any] | None = None,
    observability: dict[str, Any] | None = None,
) -> str:
    """Generates an Arc42 compliant markdown string with bounded top-down Mermaid diagrams."""
    lines: list[str] = []
    if include_frontmatter:
        lines.extend([
            "---",
            f"title: Architecture — {repo_name}",
            f"description: Arc42 architectural summary for {repo_name} ({ecosystem})",
            "---",
            "",
        ])

    lines.extend([
        f"# Architecture: {repo_name}",
        "",
        "## Context",
        f"- **Repository**: `{repo_name}`",
        f"- **SHA**: `{sha}`",
        f"- **Ecosystem**: {ecosystem}",
        f"- **Framework**: {framework}",
        "",
    ])

    if metrics:
        lines.append("## Quality & Complexity Metrics")
        for key, value in sorted(metrics.items()):
            lines.append(f"- **{key}**: {_format_metric_value(value)}")
        lines.append("")

    lines.extend([
        "## Building Block View",
        "",
        "```mermaid",
        "graph TD;",
        *MERMAID_CLASS_DEFS,
    ])

    violating_pairs = _collect_violating_pairs(fitness_violations)
    raw_v_pairs, id_v_pairs = violating_pairs

    top_groups: dict[tuple[str, ...], list[dict[str, Any]]] | None = None
    total_raw_edges = sum(len(c.get("dependencies", [])) for c in components)

    if not components:
        lines.append("    Empty[No Architecture Components Detected]:::atlasMore")
    elif len(components) <= MAX_DIRECT_COMPONENTS and total_raw_edges <= MAX_DIRECT_EDGES:
        # Small repository: keep exact deduplicated component nodes and dependency edges
        name_to_id = {c["name"]: _mermaid_safe_id(c["name"]) for c in components}
        declared_ids: set[str] = set()
        edges_meta: dict[str, tuple[str, str, str, str]] = {}
        referenced_targets: set[str] = set()
        has_outgoing: set[str] = set()

        for c in components:
            src_name = str(c["name"])
            nid = name_to_id[src_name]
            if nid not in declared_ids:
                declared_ids.add(nid)
                ctype = c.get("type", "COMPONENT")
                lines.append(
                    f'    {nid}["{_mermaid_label(src_name)} : {_mermaid_label(ctype)}"]:::atlasJob'
                )
            for dep in c.get("dependencies", []):
                dep_str = str(dep)
                dep_id = name_to_id.get(dep_str, _mermaid_safe_id(dep_str))
                edge_line = f"    {nid} --> {dep_id}"
                if edge_line not in edges_meta:
                    edges_meta[edge_line] = (src_name, dep_str, nid, dep_id)
                has_outgoing.add(nid)
                referenced_targets.add(dep_id)

        edge_idx = 0
        # Anchor isolated unlinked nodes cleanly below a root node so TD layout stays vertical
        isolated = sorted(
            nid for nid in declared_ids if nid not in has_outgoing and nid not in referenced_targets
        )
        if len(declared_ids) > 4 and isolated:
            lines.append(f'    repo_root(["{_mermaid_label(repo_name)}"]):::atlasRoot')
            for nid in isolated:
                lines.append(f"    repo_root --> {nid}")
                edge_idx += 1

        violating_indices: list[int] = []
        for edge_line in sorted(edges_meta.keys()):
            src_name, dep_str, nid, dep_id = edges_meta[edge_line]
            lines.append(edge_line)
            if (src_name, dep_str) in raw_v_pairs or (nid, dep_id) in id_v_pairs:
                violating_indices.append(edge_idx)
            edge_idx += 1

        for v_idx in violating_indices:
            lines.append(
                f"    linkStyle {v_idx} stroke:#ba1a1a,stroke-width:2px,stroke-dasharray: 5 5"
            )
    else:
        tree_lines, top_groups = _render_top_level_tree(
            repo_name,
            components,
            violating_pairs=violating_pairs if (raw_v_pairs or id_v_pairs) else None,
        )
        lines.extend(tree_lines)

    lines.extend(["```", "", "## Component Details"])

    if len(components) > MAX_DETAIL_ROWS:
        if top_groups is None:
            _, top_groups = _render_top_level_tree(repo_name, components)
        lines.append("")
        lines.append(
            f"Showing top {MAX_DETAIL_ROWS} representative components out of {len(components)} "
            f"across {len(top_groups)} module group(s):"
        )
        lines.append("")
        for top_key, group_comps in sorted(
            top_groups.items(),
            key=lambda item: (-len(item[1]), "/".join(item[0])),
        )[:12]:
            type_counts = Counter(str(c.get("type", "COMPONENT")) for c in group_comps)
            summary_types = ", ".join(f"{k}: {v}" for k, v in type_counts.most_common(3))
            mod_name = "/".join(top_key)
            lines.append(
                f"- **Module `{mod_name}`** ({len(group_comps)} components — {summary_types})"
            )
        lines.append("")
        ranked = sorted(
            components,
            key=lambda c: (
                -len(c.get("dependencies", [])),
                str(c.get("name", "")),
                str(c.get("file", "")),
            ),
        )[:MAX_DETAIL_ROWS]
        for c in ranked:
            deps = ", ".join(c.get("dependencies", [])[:6])
            extra = (
                f" (+{len(c.get('dependencies', [])) - 6} more)"
                if len(c.get("dependencies", [])) > 6
                else ""
            )
            dep_suffix = f" (deps: {deps}{extra})" if deps else ""
            lines.append(
                f"- **{c['name']}** (`{c.get('file', 'unknown')}`): {c.get('type')}{dep_suffix}"
            )
    else:
        for c in components:
            deps = ", ".join(c.get("dependencies", []))
            dep_suffix = f" (deps: {deps})" if deps else ""
            lines.append(
                f"- **{c['name']}** (`{c.get('file', 'unknown')}`): {c.get('type')}{dep_suffix}"
            )

    h2_sections = render_horizon2_sections_markdown(
        scorecard=scorecard,
        fitness_violations=fitness_violations,
        dependencies=dependencies,
        vulnerabilities=vulnerabilities,
        secrets=secrets,
        code_to_cloud_edges=code_to_cloud_edges,
        workspace_packages=workspace_packages,
        observability=observability,
    )
    if h2_sections:
        lines.append("")
        lines.extend(h2_sections)

    return "\n".join(lines).rstrip("\n") + "\n"

