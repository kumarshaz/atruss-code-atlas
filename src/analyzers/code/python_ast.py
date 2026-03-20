from pathlib import Path


def analyze_python_ast(repo_dir: Path) -> list[dict]:
    """Uses Python built-in AST to extract routes and models."""
    import ast

    components = []

    for py_file in repo_dir.rglob("*.py"):
        if ".venv" in py_file.parts or "venv" in py_file.parts:
            continue

        try:
            with open(py_file, encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(py_file))

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "Base":
                            components.append({
                                "name": node.name,
                                "type": "DATA_ACCESS_LAYER",
                                "file": str(py_file.name),
                                "dependencies": []
                            })
                elif isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Attribute):
                                if decorator.func.attr in ["get", "post", "put", "delete", "command"]:
                                    components.append({
                                        "name": node.name,
                                        "type": "API_ROUTE" if "command" not in decorator.func.attr else "CLI_COMMAND",
                                        "file": str(py_file.name),
                                        "dependencies": []
                                    })
        except SyntaxError:
            pass
        except Exception:
            pass

    return components
