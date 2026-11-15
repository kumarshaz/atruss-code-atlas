import ast
import warnings
from pathlib import Path
from typing import Any

from src.analyzers.code.base import compute_text_loc_metrics, iter_source_files
from src.analyzers.code.treesitter_engine import analyze_repo_treesitter_metrics


def analyze_python_with_metrics(repo_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Use Python's built-in AST + polyglot tree-sitter AST engine to extract
    architectural components (API routes, CLI commands, services, data models)
    along with deterministic LoC, complexity, clone, dead-code, and import metrics.
    """
    py_files = iter_source_files(repo_dir, (".py",))
    loc_metrics = compute_text_loc_metrics(py_files, comment_prefixes=("#",))
    ts_metrics = analyze_repo_treesitter_metrics(repo_dir, (".py",))

    components: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
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
                    is_mock_patch = False
                    if isinstance(decorator, ast.Call):
                        if isinstance(decorator.func, ast.Attribute):
                            attr_name = decorator.func.attr
                            if (
                                attr_name == "patch"
                                and isinstance(decorator.func.value, ast.Name)
                                and decorator.func.value.id in ("mock", "unittest")
                            ):
                                is_mock_patch = True
                        elif isinstance(decorator.func, ast.Name):
                            attr_name = decorator.func.id
                            if attr_name == "patch":
                                is_mock_patch = True
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
                    if not is_mock_patch and attr_name in route_attrs:
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

    metrics = {
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
    return components, metrics


def analyze_python_ast(repo_dir: Path) -> list[dict[str, Any]]:
    """Uses Python built-in AST to extract routes, services, and data models."""
    components, _ = analyze_python_with_metrics(repo_dir)
    return components
