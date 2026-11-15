from pathlib import Path

from src.analyzers.code import treesitter_engine
from src.analyzers.code.dotnet_structural import analyze_dotnet_structural
from src.analyzers.code.java_structural import analyze_java_structural
from src.analyzers.code.js_ts_structural import analyze_js_ts_structural
from src.analyzers.code.python_ast import analyze_python_with_metrics
from src.analyzers.code.treesitter_engine import (
    analyze_repo_treesitter_metrics,
    analyze_source_with_treesitter,
    detect_language,
    is_treesitter_available,
)


def test_treesitter_available_and_language_detection():
    assert is_treesitter_available() is True
    assert detect_language("app/routes.py") == "python"
    assert detect_language("OrderController.cs") == "c_sharp"
    assert detect_language("PetService.ts") == "typescript"
    assert detect_language("PetCard.tsx") == "tsx"
    assert detect_language("index.jsx") == "javascript"
    assert detect_language("PetController.java") == "java"
    assert detect_language("Main.kt") == "kotlin"
    assert detect_language("README.md") == "unknown"


def test_polyglot_cyclomatic_and_cognitive_complexity():
    py_code = """
def simple():
    return 1

def nested_logic(a, b, items):
    if a and b:
        for x in items:
            if x > 0:
                return x
    elif a or b:
        return 0
    return -1
"""
    py_res = analyze_source_with_treesitter("logic.py", py_code)
    assert py_res["ast_engine"] == "tree-sitter"
    py_funcs = {fn["name"]: fn for fn in py_res["functions"]}
    assert py_funcs["simple"]["cyclomatic_complexity"] == 1
    assert py_funcs["simple"]["cognitive_complexity"] == 0
    # if (+1) + and (+1) + for (+2) + if (+3) + elif (+1) + or (+1) = 9
    assert py_funcs["nested_logic"]["cognitive_complexity"] == 9
    assert py_funcs["nested_logic"]["cyclomatic_complexity"] == 7

    cs_code = """
public class Billing {
    public int SwitchHeavy(int code) {
        switch (code) {
            case 1: return 10;
            case 2: return 20;
            case 3: return 30;
            case 4: return 40;
            default: return 0;
        }
    }
    public int DeepNested(bool a, bool b) {
        if (a && b) {
            for (int i = 0; i < 3; i++) {
                var y = i > 1 ? 1 : 0;
            }
        } else if (a || b) {
            return 2;
        }
        return 0;
    }
}
"""
    cs_res = analyze_source_with_treesitter("Billing.cs", cs_code)
    assert cs_res["ast_engine"] == "tree-sitter"
    cs_funcs = {fn["name"]: fn for fn in cs_res["functions"]}
    # SonarSource Cognitive Complexity charges +1 for entire switch, vs +5 cyclomatic
    assert cs_funcs["SwitchHeavy"]["cognitive_complexity"] == 1
    assert cs_funcs["SwitchHeavy"]["cyclomatic_complexity"] == 5
    assert cs_funcs["DeepNested"]["cognitive_complexity"] == 9
    assert cs_funcs["DeepNested"]["cyclomatic_complexity"] == 7

    ts_code = """
export function evaluate(flag: boolean, items: number[]): number {
    try {
        if (flag && items.length > 0) {
            for (const n of items) {
                if (n > 5) {
                    return n;
                }
            }
        } else if (!flag) {
            return -1;
        }
    } catch (err) {
        return 0;
    }
    return 1;
}
"""
    ts_res = analyze_source_with_treesitter("eval.ts", ts_code)
    assert ts_res["ast_engine"] == "tree-sitter"
    assert ts_res["cognitive_complexity"] >= 9
    assert ts_res["cyclomatic_complexity"] >= 7

    java_code = """
public class Pricing {
    public int calc(boolean a, boolean b) {
        if (a && b) {
            for (int i = 0; i < 4; i++) {
                if (i == 2) {
                    return i;
                }
            }
        } else if (a || b) {
            return 1;
        }
        return 0;
    }
}
"""
    java_res = analyze_source_with_treesitter("Pricing.java", java_code)
    assert java_res["ast_engine"] == "tree-sitter"
    assert java_res["cognitive_complexity"] == 9
    assert java_res["cyclomatic_complexity"] == 7


def test_ast_clone_detection_across_files_and_functions(tmp_path: Path):
    file_a = tmp_path / "orders_a.py"
    file_b = tmp_path / "orders_b.py"
    # Type-2 clones: identical control flow and AST structure with renamed identifiers/literals
    file_a.write_text(
        "def compute_order_total(orders, tax_rate):\n"
        "    subtotal = 0\n"
        "    for item in orders:\n"
        "        if item.active and item.price > 10:\n"
        "            subtotal += item.price * 2\n"
        "    return subtotal + tax_rate\n",
        encoding="utf-8",
    )
    file_b.write_text(
        "def calculate_invoice_sum(lines, fee):\n"
        "    total_amt = 0\n"
        "    for entry in lines:\n"
        "        if entry.enabled and entry.cost > 99:\n"
        "            total_amt += entry.cost * 5\n"
        "    return total_amt + fee\n",
        encoding="utf-8",
    )

    m1 = analyze_repo_treesitter_metrics(tmp_path, (".py",))
    m2 = analyze_repo_treesitter_metrics(tmp_path, (".py",))
    assert m1 == m2
    assert m1["duplication_pct"] >= 90.0

    # Unique code only should yield 0.0% duplication
    unique_dir = tmp_path / "unique_repo"
    unique_dir.mkdir()
    (unique_dir / "small.py").write_text("def add(x, y):\n    return x + y\n", encoding="utf-8")
    m_unique = analyze_repo_treesitter_metrics(unique_dir, (".py",))
    assert m_unique["duplication_pct"] == 0.0

    # Intra-file duplicated functions (>= 15 AST tokens)
    intra_dir = tmp_path / "intra_repo"
    intra_dir.mkdir()
    (intra_dir / "dup.ts").write_text(
        "export function alpha(items: number[]) {\n"
        "  let acc = 0;\n"
        "  for (const x of items) {\n"
        "    if (x > 10) { acc += x * 2; }\n"
        "  }\n"
        "  return acc;\n"
        "}\n"
        "export function beta(rows: number[]) {\n"
        "  let total = 0;\n"
        "  for (const y of rows) {\n"
        "    if (y > 20) { total += y * 3; }\n"
        "  }\n"
        "  return total;\n"
        "}\n",
        encoding="utf-8",
    )
    m_intra = analyze_repo_treesitter_metrics(intra_dir, (".ts",))
    assert m_intra["duplication_pct"] > 50.0


def test_dead_code_detection_and_exclusions(tmp_path: Path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_service.py").write_text(
        "def test_something():\n    assert True\n",
        encoding="utf-8",
    )
    (tmp_path / "app.py").write_text(
        "from fastapi import APIRouter\n"
        "router = APIRouter()\n\n"
        "class PublicSchema:\n"
        "    def __init__(self):\n"
        "        self.ok = True\n"
        "    def _dead_private_method(self):\n"
        "        return 1\n\n"
        "@router.get('/items')\n"
        "def list_items():\n"
        "    return [_used_helper()]\n\n"
        "def _used_helper():\n"
        "    return 'ok'\n\n"
        "def unused_internal_helper():\n"
        "    return 42\n\n"
        "def main():\n"
        "    return list_items()\n",
        encoding="utf-8",
    )
    (tmp_path / "Widget.tsx").write_text(
        "export function PetCard() { return <div />; }\n"
        "export class PetStore { render() { return null; } }\n"
        "function unusedLocalHelper() { return 123; }\n",
        encoding="utf-8",
    )
    (tmp_path / "OrderController.cs").write_text(
        "[ApiController]\n"
        "public class OrderController : ControllerBase {\n"
        "    [HttpGet]\n"
        "    public void Get() {}\n"
        "    private void DeadCsHelper() {}\n"
        "}\n",
        encoding="utf-8",
    )
    (tmp_path / "PetController.java").write_text(
        "@RestController\n"
        "public class PetController {\n"
        "    @GetMapping\n"
        "    public String index() { return \"ok\"; }\n"
        "    private void deadJavaHelper() {}\n"
        "}\n",
        encoding="utf-8",
    )

    m = analyze_repo_treesitter_metrics(
        tmp_path, (".py", ".tsx", ".cs", ".java")
    )
    dead_names = {d["name"]: d for d in m["dead_code_symbols"]}
    assert m["dead_code_count"] == len(m["dead_code_symbols"])
    assert "unused_internal_helper" in dead_names
    assert "_dead_private_method" in dead_names
    assert "unusedLocalHelper" in dead_names
    assert "DeadCsHelper" in dead_names
    assert "deadJavaHelper" in dead_names

    # Excluded symbols must not appear
    for excluded in (
        "test_something",
        "__init__",
        "main",
        "list_items",
        "_used_helper",
        "PublicSchema",
        "PetCard",
        "PetStore",
        "OrderController",
        "Get",
        "PetController",
        "index",
    ):
        assert excluded not in dead_names

    # Deterministic sorting by (file, line, name)
    sort_keys = [(d["file"], d["line"], d["name"]) for d in m["dead_code_symbols"]]
    assert sort_keys == sorted(sort_keys)


def test_import_edges_and_confidence_scoring(tmp_path: Path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "PetService.ts").write_text(
        "export class PetService { list() { return []; } }\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "PetCard.tsx").write_text(
        "import React from 'react';\n"
        "import { PetService } from './PetService';\n"
        "import * as svcNS from './PetService';\n"
        "export function PetCard() { return new PetService(); }\n",
        encoding="utf-8",
    )

    metrics = analyze_repo_treesitter_metrics(tmp_path, (".ts", ".tsx"))
    edges = {
        (e["source_file"], e["target_symbol"]): e["confidence"]
        for e in metrics["import_edges"]
    }
    assert edges[("src/PetCard.tsx", "PetService")] == 1.0
    assert edges[("src/PetCard.tsx", "React")] == 0.5
    assert edges[("src/PetCard.tsx", "svcNS")] == 0.8


def test_treesitter_fallback_when_unavailable(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(treesitter_engine, "TREESITTER_AVAILABLE", False)
    assert is_treesitter_available() is False

    py_file = tmp_path / "svc.py"
    py_file.write_text(
        "import os\n"
        "def run(flag):\n"
        "    if flag:\n"
        "        for i in range(2):\n"
        "            if i > 0:\n"
        "                return i\n"
        "    return 0\n",
        encoding="utf-8",
    )
    ts_file = tmp_path / "svc.ts"
    ts_file.write_text(
        "import { Foo } from './Foo';\n"
        "export function check(a: boolean) {\n"
        "  if (a) {\n"
        "    return 1;\n"
        "  }\n"
        "  return 0;\n"
        "}\n",
        encoding="utf-8",
    )

    py_single = analyze_source_with_treesitter("svc.py", py_file.read_text(encoding="utf-8"))
    ts_single = analyze_source_with_treesitter("svc.ts", ts_file.read_text(encoding="utf-8"))
    assert py_single["ast_engine"] == "fallback"
    assert ts_single["ast_engine"] == "fallback"
    assert py_single["cyclomatic_complexity"] >= 4
    assert py_single["cognitive_complexity"] >= 6
    assert ts_single["cyclomatic_complexity"] >= 2

    repo_metrics = analyze_repo_treesitter_metrics(tmp_path, (".py", ".ts"))
    assert repo_metrics["ast_engine"] == "fallback"
    assert repo_metrics["max_cyclomatic_complexity"] >= 4


def test_structural_analyzers_expose_treesitter_metrics(tmp_path: Path):
    # Python repo
    py_dir = tmp_path / "py"
    py_dir.mkdir()
    (py_dir / "app.py").write_text(
        "class ItemService:\n"
        "    def run(self, x):\n"
        "        return 1 if x else 0\n",
        encoding="utf-8",
    )
    _, py_metrics = analyze_python_with_metrics(py_dir)

    # .NET repo
    cs_dir = tmp_path / "cs"
    cs_dir.mkdir()
    (cs_dir / "Api.cs").write_text(
        "public class OrderService { public int Calc(bool ok) { return ok ? 1 : 0; } }\n",
        encoding="utf-8",
    )
    _, cs_metrics = analyze_dotnet_structural(cs_dir)

    # JS/TS repo
    ts_dir = tmp_path / "ts"
    ts_dir.mkdir()
    (ts_dir / "Card.tsx").write_text(
        "export function Card(ok: boolean) { if (ok) { return 1; } return 0; }\n",
        encoding="utf-8",
    )
    _, ts_metrics = analyze_js_ts_structural(ts_dir)

    # Java repo
    java_dir = tmp_path / "java"
    java_dir.mkdir()
    (java_dir / "Svc.java").write_text(
        "@Service\npublic class Svc { public int m(boolean ok) { return ok ? 1 : 0; } }\n",
        encoding="utf-8",
    )
    _, java_metrics = analyze_java_structural(java_dir)

    required_keys = {
        "files_analyzed",
        "loc",
        "sloc",
        "avg_cyclomatic_complexity",
        "max_cyclomatic_complexity",
        "component_count",
        "ast_engine",
        "avg_cognitive_complexity",
        "max_cognitive_complexity",
        "duplication_pct",
        "dead_code_count",
        "dead_code_symbols",
        "file_complexities",
        "import_edges",
    }
    for m in (py_metrics, cs_metrics, ts_metrics, java_metrics):
        assert required_keys.issubset(m.keys())
        assert m["ast_engine"] == "tree-sitter"
        assert m["files_analyzed"] == 1
        assert len(m["file_complexities"]) == 1


def test_empty_repo_treesitter_metrics(tmp_path: Path):
    m = analyze_repo_treesitter_metrics(tmp_path, (".py", ".ts"))
    assert m["avg_cyclomatic_complexity"] == 0.0
    assert m["max_cyclomatic_complexity"] == 0
    assert m["avg_cognitive_complexity"] == 0.0
    assert m["max_cognitive_complexity"] == 0
    assert m["duplication_pct"] == 0.0
    assert m["dead_code_count"] == 0
    assert m["dead_code_symbols"] == []
    assert m["file_complexities"] == []
    assert m["import_edges"] == []
