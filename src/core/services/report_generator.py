import re
from collections import Counter, defaultdict
from typing import Any

MAX_DIRECT_COMPONENTS = 25
MAX_DIRECT_EDGES = 50
MAX_TOP_BRANCHES = 5
MAX_CHILD_BRANCHES = 3
MAX_CROSS_EDGES = 12
MAX_DETAIL_ROWS = 60


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


def _render_top_level_tree(
    repo_name: str,
    components: list[dict[str, Any]],
) -> tuple[list[str], dict[tuple[str, ...], list[dict[str, Any]]]]:
    """Build a bounded top-down Mermaid tree diagram grouped by top-level directories."""
    lines: list[str] = []
    root_id = "repo_root"
    lines.append(f'    {root_id}(["{_mermaid_label(repo_name)} ({len(components)} components)"])')

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
        lines.append(f'    {top_id}["{_mermaid_label(top_label)} ({len(group_comps)})"]')
        lines.append(f"    {root_id} --> {top_id}")

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
            ranked_children = sorted(
                child_groups.items(),
                key=lambda item: (-len(item[1]), item[0]),
            )
            shown_children = ranked_children[:MAX_CHILD_BRANCHES]
            tail_children = ranked_children[MAX_CHILD_BRANCHES:]

            for c_idx, (child_name, child_comps) in enumerate(shown_children):
                child_id = f"sub_{idx}_{c_idx}_{_mermaid_safe_id(child_name)}"
                lines.append(f'    {child_id}["{_mermaid_label(child_name)} ({len(child_comps)})"]')
                lines.append(f"    {top_id} --> {child_id}")
                for comp in child_comps:
                    comp_to_node.setdefault(comp["name"], child_id)

            if tail_children:
                tail_count = sum(len(items) for _, items in tail_children)
                tail_id = f"sub_{idx}_more"
                lines.append(
                    f'    {tail_id}["+{len(tail_children)} more submodules ({tail_count})"]'
                )
                lines.append(f"    {top_id} --> {tail_id}")
                for _, child_comps in tail_children:
                    for comp in child_comps:
                        comp_to_node.setdefault(comp["name"], tail_id)
        else:
            for comp in group_comps:
                comp_to_node.setdefault(comp["name"], top_id)

    if tail_top:
        other_count = sum(len(items) for _, items in tail_top)
        other_id = "dir_other_modules"
        lines.append(f'    {other_id}["+{len(tail_top)} more modules ({other_count})"]')
        lines.append(f"    {root_id} --> {other_id}")
        for _, group_comps in tail_top:
            for comp in group_comps:
                comp_to_node.setdefault(comp["name"], other_id)

    # Roll up inter-module dependency edges between visible tree nodes
    cross_edges: Counter[tuple[str, str]] = Counter()
    for comp in components:
        src_node = comp_to_node.get(comp["name"])
        if not src_node:
            continue
        for dep in comp.get("dependencies", []):
            dst_node = comp_to_node.get(dep)
            if dst_node and dst_node != src_node:
                cross_edges[(src_node, dst_node)] += 1

    for (src_node, dst_node), weight in sorted(
        cross_edges.items(),
        key=lambda item: (-item[1], item[0][0], item[0][1]),
    )[:MAX_CROSS_EDGES]:
        unit = "dep" if weight == 1 else "deps"
        lines.append(f'    {src_node} -.->|"{weight} {unit}"| {dst_node}')

    return lines, top_groups


def generate_arc42_markdown(
    repo_name: str,
    components: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
    ecosystem: str = "Unknown",
    framework: str = "Unknown",
    sha: str = "unknown",
    include_frontmatter: bool = True,
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
            lines.append(f"- **{key}**: {value}")
        lines.append("")

    lines.extend([
        "## Building Block View",
        "",
        "```mermaid",
        "graph TD;",
    ])

    top_groups: dict[tuple[str, ...], list[dict[str, Any]]] | None = None
    total_raw_edges = sum(len(c.get("dependencies", [])) for c in components)

    if not components:
        lines.append("    Empty[No Architecture Components Detected]")
    elif len(components) <= MAX_DIRECT_COMPONENTS and total_raw_edges <= MAX_DIRECT_EDGES:
        # Small repository: keep exact deduplicated component nodes and dependency edges
        name_to_id = {c["name"]: _mermaid_safe_id(c["name"]) for c in components}
        declared_ids: set[str] = set()
        edges: set[str] = set()
        referenced_targets: set[str] = set()
        has_outgoing: set[str] = set()

        for c in components:
            nid = name_to_id[c["name"]]
            if nid not in declared_ids:
                declared_ids.add(nid)
                ctype = c.get("type", "COMPONENT")
                lines.append(f'    {nid}["{_mermaid_label(c["name"])} : {_mermaid_label(ctype)}"]')
            for dep in c.get("dependencies", []):
                dep_id = name_to_id.get(dep, _mermaid_safe_id(dep))
                edges.add(f"    {nid} --> {dep_id}")
                has_outgoing.add(nid)
                referenced_targets.add(dep_id)

        # Anchor isolated unlinked nodes cleanly below a root node so TD layout stays vertical
        isolated = sorted(
            nid for nid in declared_ids if nid not in has_outgoing and nid not in referenced_targets
        )
        if len(declared_ids) > 4 and isolated:
            lines.append(f'    repo_root(["{_mermaid_label(repo_name)}"])')
            for nid in isolated:
                lines.append(f"    repo_root --> {nid}")

        for edge in sorted(edges):
            lines.append(edge)
    else:
        tree_lines, top_groups = _render_top_level_tree(repo_name, components)
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

    return "\n".join(lines) + "\n"
