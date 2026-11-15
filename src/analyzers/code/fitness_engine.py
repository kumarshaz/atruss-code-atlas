from __future__ import annotations

import fnmatch
import json
import os
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

import networkx as nx
import yaml

from src.analyzers.code.base import SKIP_DIRS
from src.models.artifacts import FitnessViolation, WorkspacePackage

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


_DEFAULT_POLICY_PATH = (
    Path(__file__).resolve().parents[3] / "manifests" / "architecture-rules.yaml"
)


@lru_cache(maxsize=8)
def _load_rules_cached(resolved_path: str, mtime_ns: int) -> dict[str, Any]:
    with open(resolved_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_architecture_rules(policy_path: Path | str | None = None) -> dict[str, Any]:
    """Load declarative architectural fitness rules from YAML manifest or `--policy` override."""
    env_override = os.getenv("ATRUSS_ARCHITECTURE_RULES")
    path = Path(policy_path or env_override or _DEFAULT_POLICY_PATH).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Architecture rules manifest not found at: {path}")
    stat = path.stat()
    return _load_rules_cached(str(path), stat.st_mtime_ns)


def _pure_python_pagerank(
    G: nx.DiGraph,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-6,
) -> dict[str, float]:
    """
    Deterministic pure-Python power-iteration PageRank.
    Avoids scipy/numpy runtime dependencies.
    """
    nodes = sorted(G.nodes())
    n = len(nodes)
    if n == 0:
        return {}

    ranks = {u: 1.0 / n for u in nodes}
    out_degrees = {u: G.out_degree(u) for u in nodes}
    predecessors = {v: sorted(G.predecessors(v)) for v in nodes}
    dangling_nodes = [u for u in nodes if out_degrees[u] == 0]

    for _ in range(max_iter):
        dangling_sum = alpha * sum(ranks[u] for u in dangling_nodes) / n
        base = (1.0 - alpha) / n + dangling_sum
        new_ranks: dict[str, float] = {}
        diff = 0.0
        for v in nodes:
            score = base
            for u in predecessors[v]:
                score += alpha * ranks[u] / out_degrees[u]
            new_ranks[v] = score
            diff += abs(score - ranks[v])
        ranks = new_ranks
        if diff < n * tol:
            break

    total = sum(ranks.values()) or 1.0
    return {u: round(ranks[u] / total, 6) for u in nodes}


def compute_component_blast_radius(
    G: nx.DiGraph, target_node: str | None = None
) -> dict[str, Any]:
    """
    Compute component PageRank (pure-Python power iteration), NetworkX betweenness
    centrality, and transitive blast-radius dependents for the dependency graph.
    """
    nodes = sorted(G.nodes())
    pagerank = _pure_python_pagerank(G)
    raw_betweenness = nx.betweenness_centrality(G, normalized=True) if nodes else {}
    betweenness = {u: round(float(raw_betweenness.get(u, 0.0)), 6) for u in nodes}

    ranked_nodes = [
        {
            "node": u,
            "pagerank": pagerank[u],
            "betweenness": betweenness[u],
            "in_degree": int(G.in_degree(u)),
            "out_degree": int(G.out_degree(u)),
            "blast_radius_count": len(nx.ancestors(G, u)),
        }
        for u in nodes
    ]
    ranked_nodes.sort(
        key=lambda item: (
            -item["pagerank"],
            -item["betweenness"],
            -item["blast_radius_count"],
            item["node"],
        )
    )

    result: dict[str, Any] = {
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "pagerank": pagerank,
        "betweenness_centrality": betweenness,
        "ranked_nodes": ranked_nodes,
    }

    if target_node is not None:
        if target_node in G:
            impacted = sorted(nx.ancestors(G, target_node))
            direct_deps = sorted(G.predecessors(target_node))
            transitive_deps = sorted(nx.descendants(G, target_node))
            denom = max(1, G.number_of_nodes() - 1)
            pct = round((len(impacted) / denom) * 100.0, 2) if G.number_of_nodes() > 1 else 0.0
            result.update({
                "target_node": target_node,
                "target_found": True,
                "blast_radius_count": len(impacted),
                "blast_radius_pct": pct,
                "impacted_nodes": impacted,
                "direct_dependents": direct_deps,
                "transitive_dependencies": transitive_deps,
                "target_pagerank": pagerank.get(target_node, 0.0),
                "target_betweenness": betweenness.get(target_node, 0.0),
            })
        else:
            result.update({
                "target_node": target_node,
                "target_found": False,
                "blast_radius_count": 0,
                "blast_radius_pct": 0.0,
                "impacted_nodes": [],
                "direct_dependents": [],
                "transitive_dependencies": [],
                "target_pagerank": 0.0,
                "target_betweenness": 0.0,
            })

    return result


def _canonicalize_cycle(cycle: list[str]) -> tuple[str, ...]:
    if not cycle:
        return ()
    min_idx = min(range(len(cycle)), key=lambda i: cycle[i])
    rotated = cycle[min_idx:] + cycle[:min_idx]
    return tuple(rotated)


def _build_component_graph(
    components: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
) -> nx.DiGraph:
    G = nx.DiGraph()
    comp_by_name: dict[str, dict[str, Any]] = {}
    file_to_non_module: dict[str, list[dict[str, Any]]] = defaultdict(list)

    sorted_comps = sorted(
        components,
        key=lambda c: (
            0 if c.get("type") != "MODULE" else 1,
            str(c.get("name", "")),
            str(c.get("file", "")),
        ),
    )

    for comp in sorted_comps:
        name = str(comp.get("name", "")).strip()
        if not name:
            continue
        layer = str(comp.get("layer") or comp.get("type") or "").strip()
        fpath = str(comp.get("file") or "").replace("\\", "/")
        line = int(comp.get("line", 1) or 1)
        if name not in comp_by_name:
            comp_by_name[name] = comp
            G.add_node(name, layer=layer, type=comp.get("type", layer), file=fpath, line=line)
        if fpath and comp.get("type") != "MODULE":
            file_to_non_module[fpath].append(comp)

    for comp in sorted_comps:
        src_name = str(comp.get("name", "")).strip()
        if not src_name or src_name not in G:
            continue
        for dep in comp.get("dependencies", []):
            dep_name = str(dep).strip()
            if dep_name in comp_by_name and dep_name != src_name:
                G.add_edge(src_name, dep_name)

    # Bridge single-component file import_edges when explicit dependencies omit cross-file imports
    if metrics and isinstance(metrics.get("import_edges"), list):
        for edge in metrics["import_edges"]:
            if not isinstance(edge, dict):
                continue
            src_file = str(edge.get("source_file", "")).replace("\\", "/")
            tgt_sym = str(edge.get("target_symbol", "")).strip()
            src_comps = file_to_non_module.get(src_file, [])
            if len(src_comps) == 1 and tgt_sym in comp_by_name:
                src_name = str(src_comps[0]["name"])
                tgt_file = str(comp_by_name[tgt_sym].get("file", "")).replace("\\", "/")
                if tgt_sym != src_name and tgt_file != src_file:
                    G.add_edge(src_name, tgt_sym)

    return G


def evaluate_architecture_fitness(
    components: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
    policy_path: Path | str | None = None,
) -> tuple[list[FitnessViolation], dict[str, Any]]:
    """
    Evaluate declarative architecture fitness rules (layer boundaries, circular
    dependencies, complexity/duplication thresholds) and compute blast-radius metrics.
    """
    rules = load_architecture_rules(policy_path)
    G = _build_component_graph(components, metrics=metrics)

    violations: list[FitnessViolation] = []
    present_layers = {str(G.nodes[n].get("layer", "")) for n in G.nodes()}
    sorted_edges = sorted(G.edges(), key=lambda e: (e[0], e[1]))

    # 1. Layer boundary rules
    for idx, rule in enumerate(rules.get("layer_rules", []), start=1):
        when_present = rule.get("when_layer_present")
        if when_present and when_present not in present_layers:
            continue
        rule_id = str(rule.get("rule_id") or f"ATRUSS-ARCH-{idx:03d}")
        rule_type = str(rule.get("type") or "LAYER_VIOLATION")
        severity = str(rule.get("severity") or "HIGH")
        src_layer = str(rule.get("source_layer") or "")
        dst_layer = str(rule.get("forbidden_target_layer") or "")
        base_msg = str(
            rule.get("message") or f"{src_layer} cannot directly depend on {dst_layer}."
        )

        for src, dst in sorted_edges:
            s_layer = str(G.nodes[src].get("layer", ""))
            t_layer = str(G.nodes[dst].get("layer", ""))
            if s_layer == src_layer and t_layer == dst_layer:
                violations.append(
                    FitnessViolation(
                        rule_id=rule_id,
                        type=rule_type,
                        severity=severity,
                        message=f"{base_msg} ({src} -> {dst})",
                        source_component=src,
                        target_component=dst,
                        source_layer=s_layer,
                        target_layer=t_layer,
                        file_source=G.nodes[src].get("file") or None,
                        start_line=int(G.nodes[src].get("line", 1) or 1),
                        end_line=int(G.nodes[src].get("line", 1) or 1),
                    )
                )

    # Optional explicit forbidden_edges support for custom policies
    for idx, edge_rule in enumerate(rules.get("forbidden_edges", []), start=1):
        if not isinstance(edge_rule, dict):
            continue
        r_src = str(edge_rule.get("source") or edge_rule.get("from") or "")
        r_dst = str(edge_rule.get("target") or edge_rule.get("to") or "")
        if not r_src or not r_dst:
            continue
        rule_id = str(edge_rule.get("rule_id") or f"ATRUSS-EDGE-{idx:03d}")
        severity = str(edge_rule.get("severity") or "HIGH")
        for src, dst in sorted_edges:
            s_layer = str(G.nodes[src].get("layer", ""))
            t_layer = str(G.nodes[dst].get("layer", ""))
            if (src == r_src or s_layer == r_src) and (dst == r_dst or t_layer == r_dst):
                violations.append(
                    FitnessViolation(
                        rule_id=rule_id,
                        type=str(edge_rule.get("type") or "LAYER_VIOLATION"),
                        severity=severity,
                        message=str(
                            edge_rule.get("message")
                            or f"Forbidden dependency {r_src} -> {r_dst} ({src} -> {dst})"
                        ),
                        source_component=src,
                        target_component=dst,
                        source_layer=s_layer,
                        target_layer=t_layer,
                        file_source=G.nodes[src].get("file") or None,
                        start_line=int(G.nodes[src].get("line", 1) or 1),
                        end_line=int(G.nodes[src].get("line", 1) or 1),
                    )
                )

    # 2. Circular dependency detection
    cycle_count = 0
    if rules.get("forbid_circular_dependencies", True) and G.number_of_edges() > 0:
        canonical_cycles = sorted({_canonicalize_cycle(c) for c in nx.simple_cycles(G) if c})
        cycle_count = len(canonical_cycles)
        cycle_cfg = rules.get("cycle_rule", {})
        c_rule_id = str(cycle_cfg.get("rule_id") or "ATRUSS-ARCH-004")
        c_type = str(cycle_cfg.get("type") or "CIRCULAR_DEPENDENCY")
        c_sev = str(cycle_cfg.get("severity") or "HIGH")
        c_msg = str(
            cycle_cfg.get("message") or "Circular dependency detected between components."
        )
        for cycle in canonical_cycles[:50]:
            src = cycle[0]
            dst = cycle[1 % len(cycle)]
            cycle_chain = " -> ".join([*cycle, cycle[0]])
            violations.append(
                FitnessViolation(
                    rule_id=c_rule_id,
                    type=c_type,
                    severity=c_sev,
                    message=f"{c_msg} ({cycle_chain})",
                    source_component=src,
                    target_component=dst,
                    source_layer=str(G.nodes[src].get("layer", "")),
                    target_layer=str(G.nodes[dst].get("layer", "")),
                    file_source=G.nodes[src].get("file") or None,
                    start_line=int(G.nodes[src].get("line", 1) or 1),
                    end_line=int(G.nodes[src].get("line", 1) or 1),
                )
            )

    # 3. Complexity and duplication thresholds
    thresholds = rules.get("thresholds", {})
    if metrics and isinstance(thresholds, dict):
        thresh_cfg = rules.get("threshold_rule", {})
        t_rule_id = str(thresh_cfg.get("rule_id") or "ATRUSS-ARCH-005")
        t_type = str(thresh_cfg.get("type") or "COMPLEXITY_THRESHOLD")
        t_sev = str(thresh_cfg.get("severity") or "MEDIUM")

        file_complexities = metrics.get("file_complexities") or []
        top_file = (
            str(file_complexities[0]["file"])
            if isinstance(file_complexities, list) and file_complexities
            else None
        )

        threshold_checks = [
            ("max_cyclomatic_complexity", "max_cyclomatic_complexity"),
            ("max_cognitive_complexity", "max_cognitive_complexity"),
            ("max_duplication_pct", "duplication_pct"),
        ]
        for limit_key, metric_key in threshold_checks:
            if limit_key not in thresholds:
                continue
            limit_val = float(thresholds[limit_key])
            raw_val = metrics.get(metric_key)
            if raw_val is None and limit_key != metric_key:
                raw_val = metrics.get(limit_key)
            if raw_val is None:
                continue
            actual_val = float(raw_val)
            if actual_val > limit_val:
                violations.append(
                    FitnessViolation(
                        rule_id=t_rule_id,
                        type=t_type,
                        severity=t_sev,
                        message=(
                            f"Repository {metric_key} ({actual_val}) exceeds policy "
                            f"threshold ({limit_val})."
                        ),
                        source_component=top_file or "repository",
                        target_component=metric_key,
                        source_layer="REPOSITORY",
                        target_layer="THRESHOLD",
                        file_source=top_file,
                    )
                )

    violations.sort(
        key=lambda v: (
            v.rule_id,
            v.source_component,
            v.target_component,
            v.file_source or "",
            v.start_line,
        )
    )

    by_type = dict(sorted(Counter(v.type for v in violations).items()))
    by_severity = dict(sorted(Counter(v.severity for v in violations).items()))
    blast_radius = compute_component_blast_radius(G)

    summary: dict[str, Any] = {
        "policy_version": str(rules.get("version", "1.0")),
        "passed": len(violations) == 0,
        "violation_count": len(violations),
        "violations_by_type": by_type,
        "violations_by_severity": by_severity,
        "cycle_count": cycle_count,
        "require_test_gate_before_deploy": bool(
            rules.get("require_test_gate_before_deploy", True)
        ),
        "blast_radius": blast_radius,
    }
    return violations, summary


def _expand_workspace_globs(
    repo_dir: Path,
    raw_patterns: list[str],
    extra_excludes: list[str] | None = None,
) -> list[Path]:
    positives: list[str] = []
    negations: list[str] = list(extra_excludes or [])
    for pat in raw_patterns:
        cleaned = str(pat).strip()
        if not cleaned:
            continue
        if cleaned.startswith("!"):
            negations.append(cleaned[1:].strip().lstrip("./").rstrip("/"))
        else:
            positives.append(cleaned.lstrip("./").rstrip("/"))

    matched: dict[str, Path] = {}
    for pat in positives:
        if not pat or pat == ".":
            candidates = [repo_dir]
        else:
            try:
                candidates = list(repo_dir.glob(pat))
            except ValueError:
                candidates = []
        for cand in candidates:
            if not cand.is_dir():
                continue
            rel = (
                "."
                if cand == repo_dir
                else str(cand.relative_to(repo_dir)).replace("\\", "/")
            )
            if rel != "." and any(part in SKIP_DIRS for part in Path(rel).parts):
                continue
            if any(
                fnmatch.fnmatch(rel, neg) or fnmatch.fnmatch(rel, f"{neg}/*")
                for neg in negations
                if neg
            ):
                continue
            matched[rel] = cand

    return [matched[k] for k in sorted(matched.keys())]


def _read_toml_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if tomllib is not None:
        try:
            return tomllib.loads(text)
        except Exception:
            return {}
    return {}


def _parse_toml_workspace_fallback(text: str, section_header: str) -> tuple[list[str], list[str]]:
    in_section = False
    section_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_section = stripped == section_header
            continue
        if in_section:
            section_lines.append(line)
    block = "\n".join(section_lines)
    members_m = re.search(r"members\s*=\s*\[([^\]]*)\]", block, re.DOTALL)
    exclude_m = re.search(r"exclude\s*=\s*\[([^\]]*)\]", block, re.DOTALL)
    members = re.findall(r"['\"]([^'\"]+)['\"]", members_m.group(1)) if members_m else []
    excludes = re.findall(r"['\"]([^'\"]+)['\"]", exclude_m.group(1)) if exclude_m else []
    return members, excludes


def _normalize_py_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.strip()).lower()


def _extract_py_dep_name(spec: str) -> str:
    m = re.match(r"^\s*([A-Za-z0-9_.-]+)", spec)
    return m.group(1) if m else ""


def _parse_go_work(go_work_path: Path) -> list[str]:
    text = go_work_path.read_text(encoding="utf-8", errors="replace")
    cleaned_lines = [line.split("//", 1)[0] for line in text.splitlines()]
    cleaned = "\n".join(cleaned_lines)

    paths: list[str] = []
    for block_match in re.finditer(r"\buse\s*\(([^)]*)\)", cleaned, re.DOTALL):
        for token in block_match.group(1).splitlines():
            tok = token.strip().strip('"').strip("'")
            if tok:
                paths.append(tok)

    stripped_blocks = re.sub(r"\buse\s*\([^)]*\)", "", cleaned, flags=re.DOTALL)
    for line_match in re.finditer(r"^\s*use\s+([^\s()]+)", stripped_blocks, re.MULTILINE):
        tok = line_match.group(1).strip().strip('"').strip("'")
        if tok:
            paths.append(tok)

    return sorted(set(paths))


def _parse_go_mod(go_mod_path: Path) -> tuple[str, list[str]]:
    text = go_mod_path.read_text(encoding="utf-8", errors="replace")
    cleaned_lines = [line.split("//", 1)[0] for line in text.splitlines()]
    cleaned = "\n".join(cleaned_lines)

    mod_m = re.search(r"^\s*module\s+(\S+)", cleaned, re.MULTILINE)
    mod_name = mod_m.group(1).strip() if mod_m else go_mod_path.parent.name

    requires: list[str] = []
    for block_m in re.finditer(r"\brequire\s*\(([^)]*)\)", cleaned, re.DOTALL):
        for line in block_m.group(1).splitlines():
            parts = line.strip().split()
            if parts:
                requires.append(parts[0])
    stripped_blocks = re.sub(r"\brequire\s*\([^)]*\)", "", cleaned, flags=re.DOTALL)
    for line_m in re.finditer(r"^\s*require\s+(\S+)", stripped_blocks, re.MULTILINE):
        requires.append(line_m.group(1).strip())
    for rep_m in re.finditer(r"^\s*replace\s+(\S+)\s*=>", stripped_blocks, re.MULTILINE):
        requires.append(rep_m.group(1).strip())

    return mod_name, sorted(set(requires))


def discover_workspace_packages(repo_dir: Path) -> list[WorkspacePackage]:
    """
    Discover internal monorepo workspace packages and cross-package dependencies
    across pnpm, npm/yarn, Turborepo, Nx, Cargo, Go workspaces, and uv workspaces.
    """
    packages_by_key: dict[tuple[str, str], WorkspacePackage] = {}
    raw_js_deps: dict[tuple[str, str], set[str]] = defaultdict(set)

    # Track JS workspace globs across pnpm-workspace.yaml, package.json, turbo.json, nx.json
    js_patterns: list[str] = []
    js_manager = ""

    pnpm_ws = repo_dir / "pnpm-workspace.yaml"
    if pnpm_ws.exists():
        try:
            data = yaml.safe_load(pnpm_ws.read_text(encoding="utf-8", errors="replace")) or {}
            if isinstance(data, dict) and isinstance(data.get("packages"), list):
                js_patterns.extend(str(p) for p in data["packages"])
                js_manager = "pnpm"
        except yaml.YAMLError:
            pass

    root_pkg = repo_dir / "package.json"
    if root_pkg.exists():
        try:
            pkg_json = json.loads(root_pkg.read_text(encoding="utf-8", errors="replace"))
        except (json.JSONDecodeError, OSError):
            pkg_json = {}
        workspaces = pkg_json.get("workspaces") if isinstance(pkg_json, dict) else None
        ws_list: list[str] = []
        if isinstance(workspaces, list):
            ws_list = [str(w) for w in workspaces]
        elif isinstance(workspaces, dict) and isinstance(workspaces.get("packages"), list):
            ws_list = [str(w) for w in workspaces["packages"]]
        if ws_list:
            js_patterns.extend(ws_list)
            if not js_manager:
                js_manager = "yarn" if (repo_dir / "yarn.lock").exists() else "npm"

    turbo_json = repo_dir / "turbo.json"
    if turbo_json.exists():
        if not js_patterns:
            js_patterns.extend(["apps/*", "packages/*", "libs/*", "services/*"])
        if not js_manager:
            js_manager = "turborepo"

    nx_json_path = repo_dir / "nx.json"
    nx_layout_dirs: list[str] = []
    if nx_json_path.exists():
        if not js_manager:
            js_manager = "nx"
        try:
            nx_data = json.loads(nx_json_path.read_text(encoding="utf-8", errors="replace"))
            if isinstance(nx_data, dict) and isinstance(nx_data.get("workspaceLayout"), dict):
                apps_dir = nx_data["workspaceLayout"].get("appsDir")
                libs_dir = nx_data["workspaceLayout"].get("libsDir")
                if apps_dir:
                    nx_layout_dirs.append(f"{str(apps_dir).strip('/')}/*")
                if libs_dir:
                    nx_layout_dirs.append(f"{str(libs_dir).strip('/')}/*")
        except (json.JSONDecodeError, OSError):
            pass
        if not nx_layout_dirs:
            nx_layout_dirs = ["apps/*", "libs/*", "packages/*"]
        js_patterns.extend(nx_layout_dirs)

    # Expand JS/TS workspace directories
    if js_patterns:
        for pkg_dir in _expand_workspace_globs(repo_dir, js_patterns):
            if pkg_dir == repo_dir:
                continue
            rel_path = str(pkg_dir.relative_to(repo_dir)).replace("\\", "/")
            pkg_json_file = pkg_dir / "package.json"
            proj_json_file = pkg_dir / "project.json"
            if not pkg_json_file.exists() and not proj_json_file.exists():
                continue
            pkg_name = pkg_dir.name
            dep_names: set[str] = set()
            if pkg_json_file.exists():
                try:
                    pdata = json.loads(pkg_json_file.read_text(encoding="utf-8", errors="replace"))
                    if isinstance(pdata, dict):
                        if pdata.get("name"):
                            pkg_name = str(pdata["name"])
                        for sec in (
                            "dependencies",
                            "devDependencies",
                            "peerDependencies",
                            "optionalDependencies",
                        ):
                            sec_map = pdata.get(sec)
                            if isinstance(sec_map, dict):
                                dep_names.update(str(k) for k in sec_map)
                except (json.JSONDecodeError, OSError):
                    pass
            if proj_json_file.exists():
                try:
                    raw_nx = proj_json_file.read_text(encoding="utf-8", errors="replace")
                    nx_proj = json.loads(raw_nx)
                    if isinstance(nx_proj, dict):
                        if nx_proj.get("name") and not pkg_json_file.exists():
                            pkg_name = str(nx_proj["name"])
                        for imp in nx_proj.get("implicitDependencies", []):
                            imp_str = str(imp).strip()
                            if imp_str and not imp_str.startswith("!"):
                                dep_names.add(imp_str)
                except (json.JSONDecodeError, OSError):
                    pass
            key = ("react_ts_js", rel_path)
            packages_by_key[key] = WorkspacePackage(
                name=pkg_name,
                path=rel_path,
                ecosystem="react_ts_js",
                manager=js_manager or "npm",
            )
            raw_js_deps[key].update(dep_names)

    # Scan nested Nx project.json files if nx.json exists
    if nx_json_path.exists():
        for proj_file in sorted(repo_dir.rglob("project.json")):
            if any(part in SKIP_DIRS for part in proj_file.relative_to(repo_dir).parts):
                continue
            pkg_dir = proj_file.parent
            if pkg_dir == repo_dir:
                continue
            rel_path = str(pkg_dir.relative_to(repo_dir)).replace("\\", "/")
            key = ("react_ts_js", rel_path)
            if key in packages_by_key:
                continue
            try:
                nx_proj = json.loads(proj_file.read_text(encoding="utf-8", errors="replace"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(nx_proj, dict):
                continue
            pkg_name = str(nx_proj.get("name") or pkg_dir.name)
            dep_names = {
                str(imp).strip()
                for imp in nx_proj.get("implicitDependencies", [])
                if str(imp).strip() and not str(imp).strip().startswith("!")
            }
            packages_by_key[key] = WorkspacePackage(
                name=pkg_name,
                path=rel_path,
                ecosystem="react_ts_js",
                manager="nx",
            )
            raw_js_deps[key].update(dep_names)

    # Resolve internal JS/TS dependencies
    js_name_set = {
        pkg.name for (eco, _), pkg in packages_by_key.items() if eco == "react_ts_js"
    }
    for key, pkg in packages_by_key.items():
        if key[0] == "react_ts_js":
            pkg.internal_dependencies = sorted(
                d for d in raw_js_deps.get(key, set()) if d in js_name_set and d != pkg.name
            )

    # 5. Cargo workspace ([workspace] in Cargo.toml)
    cargo_toml = repo_dir / "Cargo.toml"
    if cargo_toml.exists():
        cargo_data = _read_toml_file(cargo_toml)
        ws_section = cargo_data.get("workspace") if isinstance(cargo_data, dict) else None
        if isinstance(ws_section, dict):
            c_members = [str(m) for m in ws_section.get("members", [])]
            c_excludes = [str(e) for e in ws_section.get("exclude", [])]
        else:
            c_members, c_excludes = _parse_toml_workspace_fallback(
                cargo_toml.read_text(encoding="utf-8", errors="replace"), "[workspace]"
            )
        if c_members:
            cargo_deps: dict[tuple[str, str], set[str]] = defaultdict(set)
            for member_dir in _expand_workspace_globs(repo_dir, c_members, c_excludes):
                member_toml = member_dir / "Cargo.toml"
                if not member_toml.exists():
                    continue
                rel_path = (
                    "."
                    if member_dir == repo_dir
                    else str(member_dir.relative_to(repo_dir)).replace("\\", "/")
                )
                mdata = _read_toml_file(member_toml)
                pkg_meta = mdata.get("package", {}) if isinstance(mdata, dict) else {}
                pkg_name = str(pkg_meta.get("name") or member_dir.name)
                deps: set[str] = set()
                for dep_sec in ("dependencies", "dev-dependencies", "build-dependencies"):
                    sec_val = mdata.get(dep_sec) if isinstance(mdata, dict) else None
                    if isinstance(sec_val, dict):
                        for dep_k, dep_v in sec_val.items():
                            if isinstance(dep_v, dict) and dep_v.get("package"):
                                deps.add(str(dep_v["package"]))
                            else:
                                deps.add(str(dep_k))
                key = ("rust", rel_path)
                packages_by_key[key] = WorkspacePackage(
                    name=pkg_name,
                    path=rel_path,
                    ecosystem="rust",
                    manager="cargo",
                )
                cargo_deps[key] = deps
            rust_names = {p.name for (eco, _), p in packages_by_key.items() if eco == "rust"}
            for key, pkg in packages_by_key.items():
                if key[0] == "rust":
                    pkg.internal_dependencies = sorted(
                        d for d in cargo_deps.get(key, set()) if d in rust_names and d != pkg.name
                    )

    # 6. Go workspace (go.work)
    go_work = repo_dir / "go.work"
    if go_work.exists():
        go_uses = _parse_go_work(go_work)
        go_deps: dict[tuple[str, str], list[str]] = {}
        for mod_rel in go_uses:
            mod_dir = (repo_dir / mod_rel).resolve()
            if not mod_dir.exists() or not mod_dir.is_dir():
                continue
            try:
                rel_path = (
                    "."
                    if mod_dir == repo_dir.resolve()
                    else str(mod_dir.relative_to(repo_dir.resolve())).replace("\\", "/")
                )
            except ValueError:
                continue
            go_mod = mod_dir / "go.mod"
            if go_mod.exists():
                mod_name, reqs = _parse_go_mod(go_mod)
            else:
                mod_name, reqs = mod_dir.name, []
            key = ("go", rel_path)
            packages_by_key[key] = WorkspacePackage(
                name=mod_name,
                path=rel_path,
                ecosystem="go",
                manager="go",
            )
            go_deps[key] = reqs
        go_names = {p.name for (eco, _), p in packages_by_key.items() if eco == "go"}
        for key, pkg in packages_by_key.items():
            if key[0] == "go":
                pkg.internal_dependencies = sorted(
                    d for d in go_deps.get(key, []) if d in go_names and d != pkg.name
                )

    # 7. uv Python workspace ([tool.uv.workspace] in pyproject.toml)
    pyproject = repo_dir / "pyproject.toml"
    if pyproject.exists():
        py_data = _read_toml_file(pyproject)
        uv_ws = (
            py_data.get("tool", {}).get("uv", {}).get("workspace")
            if isinstance(py_data, dict)
            else None
        )
        if isinstance(uv_ws, dict):
            uv_members = [str(m) for m in uv_ws.get("members", [])]
            uv_excludes = [str(e) for e in uv_ws.get("exclude", [])]
        else:
            uv_members, uv_excludes = _parse_toml_workspace_fallback(
                pyproject.read_text(encoding="utf-8", errors="replace"),
                "[tool.uv.workspace]",
            )
        if uv_members:
            uv_deps: dict[tuple[str, str], set[str]] = defaultdict(set)
            for member_dir in _expand_workspace_globs(repo_dir, uv_members, uv_excludes):
                member_py = member_dir / "pyproject.toml"
                if not member_py.exists():
                    continue
                rel_path = (
                    "."
                    if member_dir == repo_dir
                    else str(member_dir.relative_to(repo_dir)).replace("\\", "/")
                )
                mdata = _read_toml_file(member_py)
                proj = mdata.get("project", {}) if isinstance(mdata, dict) else {}
                pkg_name = str(
                    proj.get("name")
                    or mdata.get("tool", {}).get("poetry", {}).get("name")
                    or member_dir.name
                )
                deps: set[str] = set()
                for spec in proj.get("dependencies", []):
                    dep_name = _extract_py_dep_name(str(spec))
                    if dep_name:
                        deps.add(dep_name)
                uv_sources = mdata.get("tool", {}).get("uv", {}).get("sources", {})
                if isinstance(uv_sources, dict):
                    deps.update(str(k) for k in uv_sources)
                key = ("python", rel_path)
                packages_by_key[key] = WorkspacePackage(
                    name=pkg_name,
                    path=rel_path,
                    ecosystem="python",
                    manager="uv",
                )
                uv_deps[key] = deps

            norm_to_name = {
                _normalize_py_name(pkg.name): pkg.name
                for (eco, _), pkg in packages_by_key.items()
                if eco == "python"
            }
            for key, pkg in packages_by_key.items():
                if key[0] == "python":
                    resolved_deps = set()
                    for dep in uv_deps.get(key, set()):
                        target_name = norm_to_name.get(_normalize_py_name(dep))
                        if target_name and target_name != pkg.name:
                            resolved_deps.add(target_name)
                    pkg.internal_dependencies = sorted(resolved_deps)

    return sorted(packages_by_key.values(), key=lambda p: (p.path, p.name, p.ecosystem))
