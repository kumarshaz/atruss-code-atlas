import ast
import warnings
from pathlib import Path
from typing import Any

from radon.complexity import cc_visit

from src.analyzers.code.base import compute_text_loc_metrics, iter_source_files


def analyze_python_with_metrics(repo_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Use Python's built-in AST + Radon cyclomatic complexity to extract
    architectural components (API routes, CLI commands, services, data models)
    along with deterministic LoC and complexity metrics.
    """
    py_files = iter_source_files(repo_dir, (".py",))
    loc_metrics = compute_text_loc_metrics(py_files, comment_prefixes=("#",))

    components: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    complexities: list[int] = []
    file_imports: dict[str, list[str]] = {}

    for py_file in py_files:
        rel_path = str(py_file.relative_to(repo_dir)).replace("\\", "/")
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                tree = ast.parse(source, filename=rel_path)
        except (SyntaxError, OSError):
            continue

        # Radon cyclomatic complexity
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                for block in cc_visit(source):
                    complexities.append(int(block.complexity))
        except Exception:
            pass

        imported_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_names.append(node.module.split(".")[-1])
                for alias in node.names:
                    imported_names.append(alias.name)
            elif isinstance(node, ast.ClassDef):
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        base_names.append(base.attr)

                comp_type: str | None = None
                if any(b in ("Base", "BaseModel", "Model", "SQLModel") for b in base_names):
                    comp_type = "DATA_ACCESS_LAYER"
                elif node.name.endswith(("Service", "Manager", "Exporter", "Archiver", "Analyzer")):
                    comp_type = "SERVICE"

                if comp_type:
                    key = (node.name, comp_type, rel_path)
                    if key not in seen:
                        seen.add(key)
                        components.append({
                            "name": node.name,
                            "type": comp_type,
                            "file": rel_path,
                            "ecosystem": "python",
                            "dependencies": [],
                        })
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for decorator in node.decorator_list:
                    attr_name = ""
                    if isinstance(decorator, ast.Call):
                        if isinstance(decorator.func, ast.Attribute):
                            attr_name = decorator.func.attr
                        elif isinstance(decorator.func, ast.Name):
                            attr_name = decorator.func.id
                    elif isinstance(decorator, ast.Attribute):
                        attr_name = decorator.attr

                    route_attrs = (
                        "get",
                        "post",
                        "put",
                        "delete",
                        "patch",
                        "route",
                        "api_route",
                        "command",
                    )
                    if attr_name in route_attrs:
                        comp_type = "CLI_COMMAND" if attr_name == "command" else "API_ROUTE"
                        key = (node.name, comp_type, rel_path)
                        if key not in seen:
                            seen.add(key)
                            components.append({
                                "name": node.name,
                                "type": comp_type,
                                "file": rel_path,
                                "ecosystem": "python",
                                "dependencies": [],
                            })

        file_imports[rel_path] = imported_names

    # Wire dependencies between discovered Python components based on imported symbols
    known_names = {c["name"] for c in components}
    for comp in components:
        imps = file_imports.get(comp["file"], [])
        deps = sorted({imp for imp in imps if imp in known_names and imp != comp["name"]})
        comp["dependencies"] = deps

    avg_cc = round(sum(complexities) / len(complexities), 2) if complexities else 0.0
    max_cc = max(complexities) if complexities else 0
    metrics = {
        **loc_metrics,
        "avg_cyclomatic_complexity": avg_cc,
        "max_cyclomatic_complexity": max_cc,
        "component_count": len(components),
    }
    return components, metrics


def analyze_python_ast(repo_dir: Path) -> list[dict[str, Any]]:
    """Uses Python built-in AST to extract routes, services, and data models."""
    components, _ = analyze_python_with_metrics(repo_dir)
    return components
