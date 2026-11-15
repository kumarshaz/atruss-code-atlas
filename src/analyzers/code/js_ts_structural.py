import json
import re
from pathlib import Path
from typing import Any

from src.analyzers.code.base import SKIP_DIRS, compute_text_loc_metrics, iter_source_files
from src.analyzers.code.treesitter_engine import analyze_repo_treesitter_metrics

_ROUTE_RE = re.compile(
    r"\b(?:app|router|fastify|server)\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]"
)
_REACT_FN_RE = re.compile(r"\bexport\s+(?:default\s+)?(?:function|const)\s+([A-Z]\w*)\b")
_CLASS_RE = re.compile(r"\bclass\s+([A-Z]\w*)\b")
_IMPORT_RE = re.compile(r"(?:import\s+[^'\"]*from\s+|require\s*\(\s*)['\"](\.[^'\"]+)['\"]")


def analyze_js_ts_structural(repo_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Extract package.json modules, API routes, React UI components, services, and data models."""
    components: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for pkg_file in sorted(repo_dir.rglob("package.json")):
        if any(part in SKIP_DIRS for part in pkg_file.relative_to(repo_dir).parts):
            continue
        rel_path = str(pkg_file.relative_to(repo_dir)).replace("\\", "/")
        try:
            pkg = json.loads(pkg_file.read_text(encoding="utf-8", errors="replace"))
        except (json.JSONDecodeError, OSError):
            continue
        pkg_name = str(pkg.get("name") or pkg_file.parent.name or "js-module")
        key = (pkg_name, "MODULE", rel_path)
        if key not in seen:
            seen.add(key)
            components.append({
                "name": pkg_name,
                "type": "MODULE",
                "file": rel_path,
                "ecosystem": "react_ts_js",
                "dependencies": [],
            })

    js_exts = (".ts", ".tsx", ".js", ".jsx", ".mjs")
    src_files = iter_source_files(repo_dir, js_exts)
    loc_metrics = compute_text_loc_metrics(src_files, comment_prefixes=("//", "/*", "*"))
    ts_metrics = analyze_repo_treesitter_metrics(repo_dir, js_exts)
    file_to_component_names: dict[str, list[str]] = {}
    file_texts: dict[str, str] = {}

    for fpath in src_files:
        rel_path = str(fpath.relative_to(repo_dir)).replace("\\", "/")
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_texts[rel_path] = content

        # Next.js API route convention
        if (
            "/api/" in f"/{rel_path}"
            and fpath.stem in ("route", "index")
            or "pages/api/" in rel_path
        ):
            comp_name = f"API_{fpath.parent.name}_{fpath.stem}"
            key = (comp_name, "API_ROUTE", rel_path)
            if key not in seen:
                seen.add(key)
                components.append({
                    "name": comp_name,
                    "type": "API_ROUTE",
                    "file": rel_path,
                    "ecosystem": "react_ts_js",
                    "dependencies": [],
                })
                file_to_component_names.setdefault(rel_path, []).append(comp_name)

        # Express / Fastify routes
        for m in _ROUTE_RE.finditer(content):
            verb, route = m.group(1).upper(), m.group(2)
            comp_name = f"{verb}_{route.strip('/').replace('/', '_') or 'root'}"
            key = (comp_name, "API_ROUTE", rel_path)
            if key not in seen:
                seen.add(key)
                components.append({
                    "name": comp_name,
                    "type": "API_ROUTE",
                    "file": rel_path,
                    "ecosystem": "react_ts_js",
                    "dependencies": [],
                })
                file_to_component_names.setdefault(rel_path, []).append(comp_name)

        # React JSX/TSX UI Components
        if fpath.suffix.lower() in (".tsx", ".jsx") or "react" in content.lower():
            for m in _REACT_FN_RE.finditer(content):
                cname = m.group(1)
                key = (cname, "UI_COMPONENT", rel_path)
                if key not in seen:
                    seen.add(key)
                    components.append({
                        "name": cname,
                        "type": "UI_COMPONENT",
                        "file": rel_path,
                        "ecosystem": "react_ts_js",
                        "dependencies": [],
                    })
                    file_to_component_names.setdefault(rel_path, []).append(cname)

        # Services & Data Access classes
        for m in _CLASS_RE.finditer(content):
            cname = m.group(1)
            if cname.endswith(("Service", "Client", "Store", "Controller")):
                ctype = "API_ROUTE" if cname.endswith("Controller") else "SERVICE"
            elif (
                cname.endswith(("Model", "Schema", "Repository", "Entity"))
                or "mongoose.model" in content
            ):
                ctype = "DATA_ACCESS_LAYER"
            else:
                continue
            key = (cname, ctype, rel_path)
            if key not in seen:
                seen.add(key)
                components.append({
                    "name": cname,
                    "type": ctype,
                    "file": rel_path,
                    "ecosystem": "react_ts_js",
                    "dependencies": [],
                })
                file_to_component_names.setdefault(rel_path, []).append(cname)

    # Resolve local relative imports to component dependencies
    for comp in components:
        if comp["type"] == "MODULE":
            continue
        comp_file = Path(comp["file"])
        text = file_texts.get(comp["file"], "")
        deps: list[str] = []
        for m in _IMPORT_RE.finditer(text):
            rel_import = m.group(1)
            resolved_stem = str((comp_file.parent / rel_import).as_posix())
            # Match normalized path prefixes
            norm_parts = Path(resolved_stem).parts
            for target_file, target_names in file_to_component_names.items():
                if target_file == comp["file"]:
                    continue
                target_no_ext = target_file.rsplit(".", 1)[0]
                if target_no_ext.endswith(rel_import.lstrip("./")) or (
                    norm_parts and target_no_ext.endswith(norm_parts[-1])
                ):
                    for tname in target_names:
                        if tname != comp["name"] and tname not in deps:
                            deps.append(tname)
        comp["dependencies"] = sorted(deps)

    return components, {
        **loc_metrics,
        "avg_cyclomatic_complexity": ts_metrics["avg_cyclomatic_complexity"],
        "max_cyclomatic_complexity": ts_metrics["max_cyclomatic_complexity"],
        "component_count": len(components),
        "ast_engine": ts_metrics["ast_engine"],
        "avg_cognitive_complexity": ts_metrics["avg_cognitive_complexity"],
        "max_cognitive_complexity": ts_metrics["max_cognitive_complexity"],
        "duplication_pct": ts_metrics["duplication_pct"],
        "dead_code_count": ts_metrics["dead_code_count"],
        "dead_code_symbols": ts_metrics["dead_code_symbols"],
        "file_complexities": ts_metrics["file_complexities"],
        "import_edges": ts_metrics["import_edges"],
    }
