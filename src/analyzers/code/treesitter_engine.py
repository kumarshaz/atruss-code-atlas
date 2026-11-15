from __future__ import annotations

import ast
import hashlib
import io
import re
import tokenize
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from src.analyzers.code.base import iter_source_files

try:
    import tree_sitter
    import tree_sitter_c_sharp
    import tree_sitter_java
    import tree_sitter_javascript
    import tree_sitter_python
    import tree_sitter_typescript

    TREESITTER_AVAILABLE = True
except ImportError:  # pragma: no cover
    tree_sitter = None  # type: ignore[assignment]
    tree_sitter_c_sharp = None  # type: ignore[assignment]
    tree_sitter_java = None  # type: ignore[assignment]
    tree_sitter_javascript = None  # type: ignore[assignment]
    tree_sitter_python = None  # type: ignore[assignment]
    tree_sitter_typescript = None  # type: ignore[assignment]
    TREESITTER_AVAILABLE = False


CLONE_MIN_TOKENS = 15
MAX_DEAD_CODE_SYMBOLS = 50
MAX_FILE_COMPLEXITIES = 25
MAX_IMPORT_EDGES = 100

_EXT_TO_LANG: dict[str, str] = {
    ".py": "python",
    ".cs": "c_sharp",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
}

_TS_SUPPORTED_LANGS = frozenset(
    {"python", "c_sharp", "typescript", "tsx", "javascript", "java"}
)

_TOKEN_SKIP_TYPES = frozenset({
    "comment",
    "line_comment",
    "block_comment",
    "import_statement",
    "import_from_statement",
    "import_declaration",
    "using_directive",
    "package_declaration",
})
_TOKEN_STRING_TYPES = frozenset({
    "string",
    "string_literal",
    "verbatim_string_literal",
    "interpolated_string_expression",
    "template_string",
    "character_literal",
})
_TOKEN_NUMBER_TYPES = frozenset({
    "integer",
    "float",
    "number",
    "integer_literal",
    "real_literal",
    "decimal_integer_literal",
    "hex_integer_literal",
    "float_literal",
})
_TOKEN_BOOL_TYPES = frozenset({"true", "false", "boolean_literal"})
_TOKEN_NULL_TYPES = frozenset({"none", "null_literal", "null", "undefined"})
_TOKEN_IDENT_TYPES = frozenset({
    "identifier",
    "type_identifier",
    "property_identifier",
    "field_identifier",
    "shorthand_property_identifier",
    "shorthand_property_identifier_pattern",
})

_LOOP_NODE_TYPES = frozenset({
    "for_statement",
    "for_in_statement",
    "foreach_statement",
    "enhanced_for_statement",
    "while_statement",
    "do_statement",
})
_SWITCH_NODE_TYPES = frozenset({
    "switch_statement",
    "switch_expression",
    "match_statement",
})
_CATCH_NODE_TYPES = frozenset({"catch_clause", "except_clause"})
_TERNARY_NODE_TYPES = frozenset({"conditional_expression", "ternary_expression"})
_CASE_NODE_TYPES = frozenset({
    "case_clause",
    "switch_case",
    "switch_section",
    "switch_block_statement_group",
})

_FUNC_NODE_TYPES = frozenset({
    "function_definition",
    "function_declaration",
    "generator_function_declaration",
    "method_declaration",
    "method_definition",
    "constructor_declaration",
    "local_function_statement",
})
_LAMBDA_NODE_TYPES = frozenset({
    "lambda",
    "lambda_expression",
    "arrow_function",
    "function_expression",
    "generator_function",
    "anonymous_method_expression",
})
_CLASS_NODE_TYPES = frozenset({
    "class_definition",
    "class_declaration",
    "interface_declaration",
    "record_declaration",
    "struct_declaration",
})

_ENDPOINT_OR_FRAMEWORK_DECORATORS = frozenset({
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "options",
    "head",
    "route",
    "api_route",
    "websocket",
    "command",
    "callback",
    "fixture",
    "property",
    "staticmethod",
    "classmethod",
    "abstractmethod",
    "override",
    "validator",
    "field_validator",
    "model_validator",
    "on_event",
    "middleware",
    "exception_handler",
    "task",
    "shared_task",
    "apicontroller",
    "httpget",
    "httppost",
    "httpput",
    "httpdelete",
    "httppatch",
    "restcontroller",
    "controller",
    "requestmapping",
    "getmapping",
    "postmapping",
    "putmapping",
    "deletemapping",
    "patchmapping",
    "service",
    "repository",
    "component",
    "bean",
    "configuration",
    "springbootapplication",
    "fact",
    "theory",
    "test",
    "api_view",
    "tool",
    "resource",
    "prompt",
    "listener",
    "event_handler",
    "scheduled",
})

_IGNORED_DEAD_NAMES = frozenset({"__init__", "main", "Main", "__main__"})
_TEST_DIR_PARTS = frozenset({"test", "tests", "__tests__", "spec", "specs"})


def is_treesitter_available() -> bool:
    """Return True when tree-sitter core and language grammars are available."""
    return bool(TREESITTER_AVAILABLE)


def detect_language(file_path: str) -> str:
    """Map a source file path extension to a canonical language identifier."""
    suffix = Path(file_path).suffix.lower()
    return _EXT_TO_LANG.get(suffix, "unknown")


@lru_cache(maxsize=8)
def _build_ts_language(language: str) -> Any | None:
    if not TREESITTER_AVAILABLE or tree_sitter is None:
        return None
    if language == "python":
        return tree_sitter.Language(tree_sitter_python.language())
    if language == "c_sharp":
        return tree_sitter.Language(tree_sitter_c_sharp.language())
    if language == "typescript":
        return tree_sitter.Language(tree_sitter_typescript.language_typescript())
    if language == "tsx":
        return tree_sitter.Language(tree_sitter_typescript.language_tsx())
    if language == "javascript":
        return tree_sitter.Language(tree_sitter_javascript.language())
    if language == "java":
        return tree_sitter.Language(tree_sitter_java.language())
    return None


def _get_parser(language: str) -> Any | None:
    if not TREESITTER_AVAILABLE or tree_sitter is None or language not in _TS_SUPPORTED_LANGS:
        return None
    ts_lang = _build_ts_language(language)
    if ts_lang is None:
        return None
    return tree_sitter.Parser(ts_lang)


def _node_text(node: Any, source_bytes: bytes) -> str:
    return source_bytes[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def _binary_operator_text(node: Any, source_bytes: bytes) -> str:
    for child in node.children:
        if not child.is_named:
            txt = _node_text(child, source_bytes).strip()
            if txt in ("&&", "||", "and", "or", "??", "??="):
                return txt
    return ""


def _is_non_default_case(node: Any, source_bytes: bytes) -> bool:
    if node.type == "case_clause":
        # Python match case: skip bare wildcard `case _:`
        for child in node.children:
            if child.type == "case_pattern" and _node_text(child, source_bytes).strip() == "_":
                return False
        return True
    if node.type == "switch_case":
        return True
    if node.type == "switch_section":
        for child in node.children:
            if not child.is_named and _node_text(child, source_bytes).strip() == "case":
                return True
            if child.type == "case_switch_label":
                return True
        return False
    if node.type == "switch_block_statement_group":
        for child in node.children:
            if child.type == "switch_label" and _node_text(child, source_bytes).lstrip().startswith(
                "case"
            ):
                return True
        return False
    return False


def _compute_cyclomatic_ts(
    node: Any,
    source_bytes: bytes,
    skip_nested_named_fns: bool = False,
    root_fn: Any = None,
) -> int:
    branches = 0

    def walk(cur: Any) -> None:
        nonlocal branches
        if skip_nested_named_fns and cur is not root_fn and cur.type in _FUNC_NODE_TYPES:
            return

        ntype = cur.type
        if ntype in (
            "if_statement",
            "elif_clause",
            "if_clause",
            *_LOOP_NODE_TYPES,
            *_CATCH_NODE_TYPES,
            *_TERNARY_NODE_TYPES,
        ) or (ntype in _CASE_NODE_TYPES and _is_non_default_case(cur, source_bytes)):
            branches += 1
        elif ntype in ("boolean_operator", "binary_expression", "assignment_expression"):
            op = _binary_operator_text(cur, source_bytes)
            if op in ("&&", "||", "and", "or", "??", "??="):
                branches += 1

        for child in cur.children:
            walk(child)

    walk(node)
    return 1 + branches


def _compute_cognitive_ts(node: Any, source_bytes: bytes, root_is_fn: bool = True) -> int:
    total = 0

    def walk(
        cur: Any,
        nesting: int,
        parent_bool_op: str | None = None,
        is_else_if: bool = False,
    ) -> None:
        nonlocal total
        ntype = cur.type

        if ntype == "if_statement":
            total += 1 if is_else_if else (1 + nesting)
            cond = cur.child_by_field_name("condition")
            cons = cur.child_by_field_name("consequence")
            alts = cur.children_by_field_name("alternative")
            if cond is not None:
                walk(cond, nesting, None, False)
            if cons is not None:
                walk(cons, nesting + 1, None, False)
            for alt in alts:
                if alt.type == "if_statement":
                    walk(alt, nesting, None, True)
                elif alt.type == "elif_clause":
                    total += 1
                    e_cond = alt.child_by_field_name("condition")
                    e_cons = alt.child_by_field_name("consequence")
                    if e_cond is not None:
                        walk(e_cond, nesting, None, False)
                    if e_cons is not None:
                        walk(e_cons, nesting + 1, None, False)
                elif alt.type == "else_clause":
                    named_kids = [c for c in alt.children if c.is_named]
                    if len(named_kids) == 1 and named_kids[0].type == "if_statement":
                        walk(named_kids[0], nesting, None, True)
                    else:
                        total += 1
                        for kid in named_kids:
                            walk(kid, nesting + 1, None, False)
                else:
                    total += 1
                    walk(alt, nesting + 1, None, False)
            return

        if ntype in _LOOP_NODE_TYPES or ntype in _SWITCH_NODE_TYPES or ntype in _CATCH_NODE_TYPES:
            total += 1 + nesting
            for child in cur.children:
                walk(child, nesting + 1, None, False)
            return

        if ntype in _TERNARY_NODE_TYPES:
            total += 1 + nesting
            for child in cur.children:
                walk(child, nesting + 1, None, False)
            return

        if ntype in ("boolean_operator", "binary_expression"):
            op = _binary_operator_text(cur, source_bytes)
            if op in ("&&", "||", "and", "or"):
                if op != parent_bool_op:
                    total += 1
                for child in cur.children:
                    walk(child, nesting, op, False)
                return

        if ntype == "parenthesized_expression":
            for child in cur.children:
                walk(child, nesting, parent_bool_op, False)
            return

        if ntype in ("break_statement", "continue_statement"):
            if any(c.type in ("identifier", "statement_identifier") for c in cur.children):
                total += 1
            return

        if ntype == "goto_statement":
            total += 1
            return

        if cur is not node and (ntype in _FUNC_NODE_TYPES or ntype in _LAMBDA_NODE_TYPES):
            next_nesting = nesting + 1 if root_is_fn else 0
            for child in cur.children:
                walk(child, next_nesting, None, False)
            return

        for child in cur.children:
            walk(child, nesting, None, False)

    if root_is_fn:
        for child in node.children:
            walk(child, 0, None, False)
    else:
        walk(node, 0, None, False)
    return total


def _extract_normalized_tokens_ts(root_node: Any, source_bytes: bytes) -> list[str]:
    tokens: list[str] = []

    def walk(node: Any) -> None:
        ntype = node.type
        if ntype in _TOKEN_SKIP_TYPES:
            return
        if node.is_named:
            if ntype in _TOKEN_STRING_TYPES:
                tokens.append("$STR")
                return
            if ntype in _TOKEN_NUMBER_TYPES:
                tokens.append("$NUM")
                return
            if ntype in _TOKEN_BOOL_TYPES:
                tokens.append("$BOOL")
                return
            if ntype in _TOKEN_NULL_TYPES:
                tokens.append("$NULL")
                return
            if ntype in _TOKEN_IDENT_TYPES:
                tokens.append("$ID")
                return
        if node.child_count == 0:
            raw = ntype.strip()
            if raw:
                tokens.append(raw)
            return
        for child in node.children:
            walk(child)

    walk(root_node)
    return tokens


def _decorator_names_from_node(node: Any, source_bytes: bytes, language: str) -> list[str]:
    names: list[str] = []
    if (
        language == "python"
        and node.parent is not None
        and node.parent.type == "decorated_definition"
    ):
        for sibling in node.parent.children:
            if sibling.type == "decorator":
                txt = _node_text(sibling, source_bytes).lstrip("@").strip()
                head = txt.split("(", 1)[0].strip()
                names.append(head.split(".")[-1].lower())
    elif language == "c_sharp":
        for child in node.children:
            if child.type == "attribute_list":
                for attr in child.children:
                    if attr.type == "attribute":
                        txt = _node_text(attr, source_bytes).split("(", 1)[0].strip()
                        names.append(txt.split(".")[-1].lower())
    elif language == "java":
        for child in node.children:
            if child.type == "modifiers":
                for sub in child.children:
                    if sub.type in ("marker_annotation", "annotation"):
                        txt = _node_text(sub, source_bytes).lstrip("@").split("(", 1)[0].strip()
                        names.append(txt.split(".")[-1].lower())
    elif language in ("typescript", "tsx", "javascript"):
        parent = node.parent
        candidates = [node]
        if parent is not None and parent.type == "export_statement":
            candidates.append(parent)
        for cand in candidates:
            for child in cand.children:
                if child.type == "decorator":
                    txt = _node_text(child, source_bytes).lstrip("@").split("(", 1)[0].strip()
                    names.append(txt.split(".")[-1].lower())
    return names


def _modifier_words(node: Any, source_bytes: bytes, language: str) -> set[str]:
    words: set[str] = set()
    if language == "c_sharp":
        for child in node.children:
            if child.type == "modifier":
                words.add(_node_text(child, source_bytes).strip().lower())
    elif language == "java":
        for child in node.children:
            if child.type == "modifiers":
                for sub in child.children:
                    if not sub.is_named or sub.type == "modifier":
                        words.add(_node_text(sub, source_bytes).strip().lower())
    elif language in ("typescript", "tsx", "javascript"):
        for child in node.children:
            if child.type == "accessibility_modifier":
                words.add(_node_text(child, source_bytes).strip().lower())
    return words


def _extract_python_all_exports(root_node: Any, source_bytes: bytes) -> set[str]:
    exported: set[str] = set()
    for child in root_node.children:
        if child.type == "expression_statement":
            for sub in child.children:
                if sub.type == "assignment":
                    left = sub.child_by_field_name("left")
                    right = sub.child_by_field_name("right")
                    if (
                        left is not None
                        and right is not None
                        and _node_text(left, source_bytes).strip() == "__all__"
                    ):
                        right_txt = _node_text(right, source_bytes)
                        for m in re.finditer(r"['\"]([A-Za-z_]\w*)['\"]", right_txt):
                            exported.add(m.group(1))
    return exported


def _extract_js_ts_explicit_exports(root_node: Any, source_bytes: bytes) -> set[str]:
    exported: set[str] = set()
    stack = [root_node]
    while stack:
        cur = stack.pop()
        if cur.type == "export_statement":
            for child in cur.children:
                if child.type == "export_clause":
                    for spec in child.children:
                        if spec.type == "export_specifier":
                            name_node = spec.child_by_field_name("name")
                            if name_node is not None:
                                exported.add(_node_text(name_node, source_bytes).strip())
                elif child.type in ("identifier", "type_identifier"):
                    exported.add(_node_text(child, source_bytes).strip())
        elif cur.type == "assignment_expression":
            left = cur.child_by_field_name("left")
            right = cur.child_by_field_name("right")
            if (
                left is not None
                and right is not None
                and _node_text(left, source_bytes)
                .strip()
                .startswith(("module.exports", "exports."))
            ):
                right_txt = _node_text(right, source_bytes)
                for m in re.finditer(r"\b([A-Za-z_$]\w*)\b", right_txt):
                    exported.add(m.group(1))
        stack.extend(cur.children)
    return exported


def _extract_imports_ts(root_node: Any, source_bytes: bytes, language: str) -> list[dict[str, Any]]:
    imports: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        ntype = node.type
        if language == "python":
            if ntype == "import_statement":
                line = node.start_point.row + 1
                for child in node.children:
                    if child.type == "dotted_name":
                        mod = _node_text(child, source_bytes).strip()
                        imports.append({
                            "module": mod,
                            "symbols": [mod.split(".")[-1]],
                            "line": line,
                            "is_relative": False,
                            "is_wildcard": False,
                        })
                    elif child.type == "aliased_import":
                        name_n = child.child_by_field_name("name")
                        if name_n is not None:
                            mod = _node_text(name_n, source_bytes).strip()
                            imports.append({
                                "module": mod,
                                "symbols": [mod.split(".")[-1]],
                                "line": line,
                                "is_relative": False,
                                "is_wildcard": False,
                            })
                return
            if ntype == "import_from_statement":
                line = node.start_point.row + 1
                mod_node = node.child_by_field_name("module_name")
                mod = _node_text(mod_node, source_bytes).strip() if mod_node is not None else ""
                is_rel = mod.startswith(".")
                is_wild = any(c.type == "wildcard_import" for c in node.children)
                syms: list[str] = []
                for name_n in node.children_by_field_name("name"):
                    if name_n.type == "aliased_import":
                        inner = name_n.child_by_field_name("name")
                        if inner is not None:
                            syms.append(_node_text(inner, source_bytes).strip())
                    else:
                        syms.append(_node_text(name_n, source_bytes).strip())
                imports.append({
                    "module": mod.lstrip("."),
                    "raw_module": mod,
                    "symbols": syms,
                    "line": line,
                    "is_relative": is_rel,
                    "is_wildcard": is_wild,
                })
                return
        elif language in ("typescript", "tsx", "javascript"):
            if ntype == "import_statement":
                line = node.start_point.row + 1
                src_node = node.child_by_field_name("source")
                mod = (
                    _node_text(src_node, source_bytes).strip().strip("'\"")
                    if src_node is not None
                    else ""
                )
                syms: list[str] = []
                is_wild = False
                for child in node.children:
                    if child.type == "import_clause":
                        stack = [child]
                        while stack:
                            c = stack.pop()
                            if c.type == "import_specifier":
                                nm = c.child_by_field_name("name")
                                if nm is not None:
                                    syms.append(_node_text(nm, source_bytes).strip())
                            elif c.type == "namespace_import":
                                is_wild = True
                                for sub in c.children:
                                    if sub.type == "identifier":
                                        syms.append(_node_text(sub, source_bytes).strip())
                            elif (
                                c.type == "identifier"
                                and c.parent
                                and c.parent.type == "import_clause"
                            ):
                                syms.append(_node_text(c, source_bytes).strip())
                            stack.extend(c.children)
                imports.append({
                    "module": mod,
                    "symbols": syms,
                    "line": line,
                    "is_relative": mod.startswith((".", "@/", "~/")),
                    "is_wildcard": is_wild,
                })
                return
            if ntype == "call_expression":
                fn_node = node.child_by_field_name("function")
                args_node = node.child_by_field_name("arguments")
                if (
                    fn_node is not None
                    and args_node is not None
                    and _node_text(fn_node, source_bytes).strip() == "require"
                ):
                    for arg in args_node.children:
                        if arg.type == "string":
                            mod = _node_text(arg, source_bytes).strip().strip("'\"")
                            imports.append({
                                "module": mod,
                                "symbols": [Path(mod).stem],
                                "line": node.start_point.row + 1,
                                "is_relative": mod.startswith((".", "@/", "~/")),
                                "is_wildcard": False,
                            })
        elif language == "c_sharp":
            if ntype == "using_directive":
                line = node.start_point.row + 1
                raw_using = _node_text(node, source_bytes).strip().rstrip(";")
                txt = raw_using.removeprefix("using").strip()
                if txt and not txt.startswith("static "):
                    imports.append({
                        "module": txt,
                        "symbols": [txt.split(".")[-1]],
                        "line": line,
                        "is_relative": False,
                        "is_wildcard": True,
                    })
                return
        elif language == "java" and ntype == "import_declaration":
            line = node.start_point.row + 1
            raw_imp = _node_text(node, source_bytes).strip().rstrip(";")
            raw = raw_imp.removeprefix("import").strip().removeprefix("static").strip()
            is_wild = raw.endswith(".*")
            mod = raw[:-2] if is_wild else raw
            imports.append({
                "module": mod,
                "symbols": [] if is_wild else [mod.split(".")[-1]],
                "line": line,
                "is_relative": False,
                "is_wildcard": is_wild,
            })
            return

        for child in node.children:
            walk(child)

    walk(root_node)
    return imports


def _is_exported_ts(
    node: Any,
    name: str,
    source_bytes: bytes,
    language: str,
    enclosing_class_exported: bool,
    explicit_exports: set[str],
) -> bool:
    if name in explicit_exports:
        return True
    if language == "python":
        if node.type in _CLASS_NODE_TYPES:
            return not name.startswith("_")
        # Public methods on a public Python class belong to the class's public API
        return bool(enclosing_class_exported and not name.startswith("_"))

    if language in ("typescript", "tsx", "javascript"):
        cur = node
        while cur is not None:
            if cur.type == "export_statement":
                return True
            if cur.type in ("program", "class_body", "statement_block"):
                break
            cur = cur.parent
        mods = _modifier_words(node, source_bytes, language)
        if "private" in mods or "protected" in mods:
            return False
        return bool(enclosing_class_exported and node.type == "method_definition")

    if language in ("c_sharp", "java"):
        mods = _modifier_words(node, source_bytes, language)
        if "private" in mods:
            return False
        if "public" in mods or "protected" in mods:
            if node.type in _CLASS_NODE_TYPES:
                return True
            if enclosing_class_exported:
                return True
        # Interface methods in Java/C# have no explicit public modifier
        return bool(
            node.parent is not None
            and node.parent.parent is not None
            and node.parent.parent.type == "interface_declaration"
        )

    return False


def _analyze_with_treesitter_parser(
    file_path: str, content: str, language: str, parser: Any
) -> dict[str, Any]:
    source_bytes = content.encode("utf-8", errors="replace")
    tree = parser.parse(source_bytes)
    root = tree.root_node

    explicit_exports: set[str] = set()
    if language == "python":
        explicit_exports = _extract_python_all_exports(root, source_bytes)
    elif language in ("typescript", "tsx", "javascript"):
        explicit_exports = _extract_js_ts_explicit_exports(root, source_bytes)

    functions: list[dict[str, Any]] = []
    classes: list[dict[str, Any]] = []
    declared_symbols: list[dict[str, Any]] = []
    decl_name_spans: set[tuple[int, int]] = set()

    def walk_decls(
        node: Any,
        fn_depth: int,
        class_exported: bool,
        enclosing_class_name: str | None,
    ) -> None:
        ntype = node.type

        if ntype in _CLASS_NODE_TYPES:
            name_node = node.child_by_field_name("name")
            if name_node is not None:
                cname = _node_text(name_node, source_bytes).strip()
                decl_name_spans.add((name_node.start_byte, name_node.end_byte))
                decs = _decorator_names_from_node(node, source_bytes, language)
                is_dec_ep = any(d in _ENDPOINT_OR_FRAMEWORK_DECORATORS for d in decs)
                is_exp = _is_exported_ts(
                    node, cname, source_bytes, language, class_exported, explicit_exports
                )
                cls_info = {
                    "name": cname,
                    "line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                    "is_exported": is_exp,
                    "is_decorated_endpoint": is_dec_ep,
                    "decorators": decs,
                }
                classes.append(cls_info)
                declared_symbols.append({
                    "name": cname,
                    "kind": "class",
                    "line": node.start_point.row + 1,
                    "is_exported": is_exp,
                    "is_decorated_endpoint": is_dec_ep,
                    "is_file_local": not is_exp and language != "python",
                })
                for child in node.children:
                    walk_decls(child, fn_depth, is_exp, cname)
                return

        if ntype in _FUNC_NODE_TYPES:
            name_node = node.child_by_field_name("name")
            if name_node is not None:
                fname = _node_text(name_node, source_bytes).strip()
                decl_name_spans.add((name_node.start_byte, name_node.end_byte))
                decs = _decorator_names_from_node(node, source_bytes, language)
                is_dec_ep = any(d in _ENDPOINT_OR_FRAMEWORK_DECORATORS for d in decs)
                is_exp = _is_exported_ts(
                    node, fname, source_bytes, language, class_exported, explicit_exports
                )
                is_ctor = enclosing_class_name is not None and fname == enclosing_class_name
                if ntype == "constructor_declaration" or (
                    language == "typescript" and fname == "constructor"
                ):
                    is_ctor = True
                is_nested = fn_depth > 0
                cc = _compute_cyclomatic_ts(
                    node, source_bytes, skip_nested_named_fns=True, root_fn=node
                )
                cog = _compute_cognitive_ts(node, source_bytes, root_is_fn=True)
                functions.append({
                    "name": fname,
                    "line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                    "cyclomatic_complexity": cc,
                    "cognitive_complexity": cog,
                    "is_exported": is_exp,
                    "is_decorated_endpoint": is_dec_ep,
                    "is_nested": is_nested,
                })
                mods = _modifier_words(node, source_bytes, language)
                is_file_local = (
                    "private" in mods
                    or ntype == "local_function_statement"
                    or (language in ("typescript", "tsx", "javascript") and not is_exp)
                    or (
                        language == "python"
                        and enclosing_class_name is not None
                        and fname.startswith("_")
                    )
                )
                if not is_ctor and not is_nested:
                    declared_symbols.append({
                        "name": fname,
                        "kind": "method" if enclosing_class_name else "function",
                        "line": node.start_point.row + 1,
                        "is_exported": is_exp,
                        "is_decorated_endpoint": is_dec_ep,
                        "is_file_local": is_file_local,
                    })
                for child in node.children:
                    walk_decls(child, fn_depth + 1, class_exported, enclosing_class_name)
                return

        # JS/TS arrow functions or function expressions assigned to variable_declarator
        if language in ("typescript", "tsx", "javascript") and ntype == "variable_declarator":
            val_node = node.child_by_field_name("value")
            name_node = node.child_by_field_name("name")
            if (
                name_node is not None
                and val_node is not None
                and val_node.type in ("arrow_function", "function_expression")
            ):
                fname = _node_text(name_node, source_bytes).strip()
                decl_name_spans.add((name_node.start_byte, name_node.end_byte))
                is_exp = _is_exported_ts(
                    node.parent if node.parent is not None else node,
                    fname,
                    source_bytes,
                    language,
                    class_exported,
                    explicit_exports,
                )
                is_nested = fn_depth > 0
                cc = _compute_cyclomatic_ts(
                    val_node, source_bytes, skip_nested_named_fns=True, root_fn=val_node
                )
                cog = _compute_cognitive_ts(val_node, source_bytes, root_is_fn=True)
                functions.append({
                    "name": fname,
                    "line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                    "cyclomatic_complexity": cc,
                    "cognitive_complexity": cog,
                    "is_exported": is_exp,
                    "is_decorated_endpoint": False,
                    "is_nested": is_nested,
                })
                if not is_nested:
                    declared_symbols.append({
                        "name": fname,
                        "kind": "function",
                        "line": node.start_point.row + 1,
                        "is_exported": is_exp,
                        "is_decorated_endpoint": False,
                        "is_file_local": not is_exp,
                    })
                for child in val_node.children:
                    walk_decls(child, fn_depth + 1, class_exported, enclosing_class_name)
                return

        for child in node.children:
            walk_decls(child, fn_depth, class_exported, enclosing_class_name)

    walk_decls(root, 0, False, None)

    # Collect referenced identifiers (excluding declaration name spans and import statements)
    ref_counts: Counter[str] = Counter()

    def walk_refs(node: Any) -> None:
        if node.type in (
            "import_statement",
            "import_from_statement",
            "import_declaration",
            "using_directive",
            "package_declaration",
        ):
            return
        if node.type in _TOKEN_IDENT_TYPES:
            span = (node.start_byte, node.end_byte)
            if span not in decl_name_spans:
                ident = _node_text(node, source_bytes).strip()
                if ident:
                    ref_counts[ident] += 1
            return
        for child in node.children:
            walk_refs(child)

    walk_refs(root)

    file_cc = _compute_cyclomatic_ts(root, source_bytes, skip_nested_named_fns=False)
    top_cog = sum(fn["cognitive_complexity"] for fn in functions if not fn.get("is_nested"))
    # Include top-level statements outside functions/classes if there are no functions
    if not functions:
        top_cog = _compute_cognitive_ts(root, source_bytes, root_is_fn=False)

    functions.sort(key=lambda fn: (fn["line"], fn["name"]))
    classes.sort(key=lambda cls: (cls["line"], cls["name"]))
    declared_symbols.sort(key=lambda sym: (sym["line"], sym["name"]))

    return {
        "file": file_path.replace("\\", "/"),
        "language": language,
        "ast_engine": "tree-sitter",
        "loc": len(content.splitlines()),
        "cyclomatic_complexity": file_cc,
        "cognitive_complexity": top_cog,
        "functions": functions,
        "classes": classes,
        "declared_symbols": declared_symbols,
        "referenced_identifiers": sorted(ref_counts.keys()),
        "reference_counts": dict(ref_counts),
        "imports": _extract_imports_ts(root, source_bytes, language),
        "tokens": _extract_normalized_tokens_ts(root, source_bytes),
    }


def _compute_python_ast_cognitive(node: ast.AST, root_is_fn: bool = True) -> int:
    total = 0

    def walk(cur: ast.AST, nesting: int, is_elif: bool = False) -> None:
        nonlocal total
        if isinstance(cur, ast.If):
            total += 1 if is_elif else (1 + nesting)
            walk(cur.test, nesting)
            for stmt in cur.body:
                walk(stmt, nesting + 1)
            if len(cur.orelse) == 1 and isinstance(cur.orelse[0], ast.If):
                walk(cur.orelse[0], nesting, is_elif=True)
            elif cur.orelse:
                total += 1
                for stmt in cur.orelse:
                    walk(stmt, nesting + 1)
            return
        if isinstance(cur, (ast.For, ast.AsyncFor, ast.While)):
            total += 1 + nesting
            for child in ast.iter_child_nodes(cur):
                walk(child, nesting + 1)
            return
        if isinstance(cur, ast.Try):
            for handler in cur.handlers:
                total += 1 + nesting
                for stmt in handler.body:
                    walk(stmt, nesting + 1)
            for stmt in cur.body:
                walk(stmt, nesting)
            for stmt in cur.orelse:
                walk(stmt, nesting)
            for stmt in cur.finalbody:
                walk(stmt, nesting)
            return
        if isinstance(cur, ast.IfExp):
            total += 1 + nesting
            for child in ast.iter_child_nodes(cur):
                walk(child, nesting + 1)
            return
        if isinstance(cur, ast.BoolOp):
            total += 1
            for val in cur.values:
                if isinstance(val, ast.BoolOp) and type(val.op) is type(cur.op):
                    for sub in val.values:
                        walk(sub, nesting)
                else:
                    walk(val, nesting)
            return
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) and cur is not node:
            next_nesting = nesting + 1 if root_is_fn else 0
            for child in ast.iter_child_nodes(cur):
                walk(child, next_nesting)
            return
        for child in ast.iter_child_nodes(cur):
            walk(child, nesting)

    if root_is_fn:
        for child in ast.iter_child_nodes(node):
            walk(child, 0)
    else:
        walk(node, 0)
    return total


def _compute_python_ast_cyclomatic(node: ast.AST, skip_nested_fns: bool = False) -> int:
    branches = 0

    def walk(cur: ast.AST) -> None:
        nonlocal branches
        if skip_nested_fns and cur is not node and isinstance(
            cur, (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            return
        if isinstance(
            cur, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)
        ):
            branches += 1
        elif isinstance(cur, ast.BoolOp):
            branches += max(1, len(cur.values) - 1)
        elif isinstance(cur, ast.comprehension):
            branches += len(cur.ifs)
        for child in ast.iter_child_nodes(cur):
            walk(child)

    walk(node)
    return 1 + branches


def _analyze_python_fallback(file_path: str, content: str) -> dict[str, Any]:
    functions: list[dict[str, Any]] = []
    classes: list[dict[str, Any]] = []
    declared_symbols: list[dict[str, Any]] = []
    imports: list[dict[str, Any]] = []
    ref_counts: Counter[str] = Counter()

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        return _analyze_brace_fallback(file_path, content, "python")

    all_exports: set[str] = set()
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            for tgt in stmt.targets:
                if (
                    isinstance(tgt, ast.Name)
                    and tgt.id == "__all__"
                    and isinstance(stmt.value, (ast.List, ast.Tuple, ast.Set))
                ):
                    for el in stmt.value.elts:
                        if isinstance(el, ast.Constant) and isinstance(el.value, str):
                            all_exports.add(el.value)

    def _dec_names(decs: list[ast.expr]) -> list[str]:
        out: list[str] = []
        for d in decs:
            if isinstance(d, ast.Call):
                d = d.func
            if isinstance(d, ast.Attribute):
                out.append(d.attr.lower())
            elif isinstance(d, ast.Name):
                out.append(d.id.lower())
        return out

    def walk_py(node: ast.AST, fn_depth: int, cls_exported: bool, cls_name: str | None) -> None:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "module": alias.name,
                    "symbols": [alias.name.split(".")[-1]],
                    "line": node.lineno,
                    "is_relative": False,
                    "is_wildcard": False,
                })
            return
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            is_wild = any(a.name == "*" for a in node.names)
            syms = [a.name for a in node.names if a.name != "*"]
            imports.append({
                "module": mod,
                "symbols": syms,
                "line": node.lineno,
                "is_relative": node.level > 0,
                "is_wildcard": is_wild,
            })
            return
        if isinstance(node, ast.ClassDef):
            decs = _dec_names(node.decorator_list)
            is_ep = any(d in _ENDPOINT_OR_FRAMEWORK_DECORATORS for d in decs)
            is_exp = not node.name.startswith("_") or node.name in all_exports
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno) or node.lineno,
                "is_exported": is_exp,
                "is_decorated_endpoint": is_ep,
                "decorators": decs,
            })
            declared_symbols.append({
                "name": node.name,
                "kind": "class",
                "line": node.lineno,
                "is_exported": is_exp,
                "is_decorated_endpoint": is_ep,
                "is_file_local": False,
            })
            for child in node.body:
                walk_py(child, fn_depth, is_exp, node.name)
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decs = _dec_names(node.decorator_list)
            is_ep = any(d in _ENDPOINT_OR_FRAMEWORK_DECORATORS for d in decs)
            is_exp = (node.name in all_exports) or (cls_exported and not node.name.startswith("_"))
            is_nested = fn_depth > 0
            cc = _compute_python_ast_cyclomatic(node, skip_nested_fns=True)
            cog = _compute_python_ast_cognitive(node, root_is_fn=True)
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno) or node.lineno,
                "cyclomatic_complexity": cc,
                "cognitive_complexity": cog,
                "is_exported": is_exp,
                "is_decorated_endpoint": is_ep,
                "is_nested": is_nested,
            })
            if not is_nested:
                declared_symbols.append({
                    "name": node.name,
                    "kind": "method" if cls_name else "function",
                    "line": node.lineno,
                    "is_exported": is_exp,
                    "is_decorated_endpoint": is_ep,
                    "is_file_local": cls_name is not None and node.name.startswith("_"),
                })
            for child in node.body:
                walk_py(child, fn_depth + 1, cls_exported, cls_name)
            return
        for child in ast.iter_child_nodes(node):
            walk_py(child, fn_depth, cls_exported, cls_name)

    walk_py(tree, 0, False, None)

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            ref_counts[node.id] += 1
        elif isinstance(node, ast.Attribute):
            ref_counts[node.attr] += 1

    tokens: list[str] = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(content).readline):
            if tok.type in (
                tokenize.COMMENT,
                tokenize.NL,
                tokenize.NEWLINE,
                tokenize.INDENT,
                tokenize.DEDENT,
                tokenize.ENCODING,
                tokenize.ENDMARKER,
            ):
                continue
            if tok.type == tokenize.STRING:
                tokens.append("$STR")
            elif tok.type == tokenize.NUMBER:
                tokens.append("$NUM")
            elif tok.type == tokenize.NAME:
                if tok.string in ("True", "False"):
                    tokens.append("$BOOL")
                elif tok.string == "None":
                    tokens.append("$NULL")
                elif tok.string in (
                    "def",
                    "class",
                    "if",
                    "elif",
                    "else",
                    "for",
                    "in",
                    "while",
                    "return",
                    "and",
                    "or",
                    "not",
                    "try",
                    "except",
                    "import",
                    "from",
                    "as",
                    "with",
                    "pass",
                    "break",
                    "continue",
                ):
                    tokens.append(tok.string)
                else:
                    tokens.append("$ID")
            else:
                tokens.append(tok.string)
    except tokenize.TokenError:
        pass

    file_cc = _compute_python_ast_cyclomatic(tree, skip_nested_fns=False)
    top_cog = sum(fn["cognitive_complexity"] for fn in functions if not fn.get("is_nested"))
    if not functions:
        top_cog = _compute_python_ast_cognitive(tree, root_is_fn=False)

    return {
        "file": file_path.replace("\\", "/"),
        "language": "python",
        "ast_engine": "fallback",
        "loc": len(content.splitlines()),
        "cyclomatic_complexity": file_cc,
        "cognitive_complexity": top_cog,
        "functions": sorted(functions, key=lambda fn: (fn["line"], fn["name"])),
        "classes": sorted(classes, key=lambda cls: (cls["line"], cls["name"])),
        "declared_symbols": sorted(declared_symbols, key=lambda sym: (sym["line"], sym["name"])),
        "referenced_identifiers": sorted(ref_counts.keys()),
        "reference_counts": dict(ref_counts),
        "imports": imports,
        "tokens": tokens,
    }


_FALLBACK_KEYWORDS = frozenset({
    "if",
    "else",
    "for",
    "foreach",
    "while",
    "switch",
    "case",
    "catch",
    "try",
    "return",
    "class",
    "interface",
    "function",
    "const",
    "let",
    "var",
    "export",
    "import",
    "from",
    "public",
    "private",
    "protected",
    "internal",
    "static",
    "async",
    "await",
    "new",
    "void",
    "in",
    "of",
})
_FALLBACK_TOKEN_RE = re.compile(
    r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\b\d+(?:\.\d+)?\b|[A-Za-z_]\w*|&&|\|\||\?\?|[{}()[\].,:;+-/*=<>!]+'
)
_FALLBACK_BRANCH_RE = re.compile(
    r"\b(if|else\s+if|for|foreach|while|switch|case|catch)\b|&&|\|\||\?\?|\?"
)
_FALLBACK_IMPORT_RE = re.compile(
    r"(?:import\s+(?:[^;'\"]+from\s+)?['\"]([^'\"]+)['\"]|"
    r"using\s+([\w.]+)\s*;|"
    r"import\s+([\w.*]+)\s*;)"
)


def _analyze_brace_fallback(file_path: str, content: str, language: str) -> dict[str, Any]:
    lines = content.splitlines()
    branch_count = len(_FALLBACK_BRANCH_RE.findall(content))
    file_cc = 1 + branch_count

    cog_total = 0
    brace_depth = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("//", "#", "/*", "*")):
            continue
        open_b = stripped.count("{")
        close_b = stripped.count("}")
        eff_depth = max(0, brace_depth - 1)
        if re.match(r"^(else\s+if|else)\b", stripped):
            cog_total += 1
        elif re.match(r"^(if|for|foreach|while|switch|catch)\b", stripped):
            cog_total += 1 + eff_depth
        cog_total += len(re.findall(r"&&|\|\|", stripped))
        brace_depth = max(0, brace_depth + open_b - close_b)

    imports: list[dict[str, Any]] = []
    for idx, line in enumerate(lines, start=1):
        m = _FALLBACK_IMPORT_RE.search(line)
        if m:
            mod = m.group(1) or m.group(2) or m.group(3) or ""
            imports.append({
                "module": mod.rstrip(".*"),
                "symbols": [mod.rstrip(".*").split(".")[-1]],
                "line": idx,
                "is_relative": mod.startswith((".", "@/", "~/")),
                "is_wildcard": mod.endswith(".*") or language == "c_sharp",
            })

    tokens: list[str] = []
    ident_counts: Counter[str] = Counter()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("//", "#", "/*", "*", "import ", "using ")):
            continue
        for tok in _FALLBACK_TOKEN_RE.findall(stripped):
            if tok.startswith(('"', "'")):
                tokens.append("$STR")
            elif tok[0].isdigit():
                tokens.append("$NUM")
            elif tok in ("true", "false"):
                tokens.append("$BOOL")
            elif tok in ("null", "undefined", "None"):
                tokens.append("$NULL")
            elif tok in _FALLBACK_KEYWORDS or not tok[0].isalpha() and tok[0] != "_":
                tokens.append(tok)
            else:
                tokens.append("$ID")
                ident_counts[tok] += 1

    return {
        "file": file_path.replace("\\", "/"),
        "language": language,
        "ast_engine": "fallback",
        "loc": len(lines),
        "cyclomatic_complexity": file_cc,
        "cognitive_complexity": cog_total,
        "functions": [],
        "classes": [],
        "declared_symbols": [],
        "referenced_identifiers": sorted(ident_counts.keys()),
        "reference_counts": dict(ident_counts),
        "imports": imports,
        "tokens": tokens,
    }


def analyze_source_with_treesitter(file_path: str, content: str) -> dict[str, Any]:
    """
    Parse a source file with tree-sitter (or clean AST/regex fallback) and compute
    cyclomatic complexity, SonarSource cognitive complexity, normalized AST tokens,
    declared symbols, referenced identifiers, and imports.
    """
    language = detect_language(file_path)
    parser = _get_parser(language)
    if parser is not None:
        return _analyze_with_treesitter_parser(file_path, content, language, parser)
    if language == "python":
        return _analyze_python_fallback(file_path, content)
    return _analyze_brace_fallback(file_path, content, language)


def _is_test_file(rel_path: str) -> bool:
    norm = rel_path.replace("\\", "/").lower()
    parts = norm.split("/")
    if any(p in _TEST_DIR_PARTS for p in parts[:-1]):
        return True
    fname = parts[-1]
    if fname == "conftest.py" or fname.startswith("test_") or fname.endswith("_test.py"):
        return True
    if ".test." in fname or ".spec." in fname:
        return True
    return fname.endswith(("test.java", "tests.java", "test.cs", "tests.cs", "spec.cs"))


def _compute_clone_duplication_pct(file_tokens_list: list[list[str]]) -> float:
    window_map: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for f_idx, tokens in enumerate(file_tokens_list):
        if len(tokens) < CLONE_MIN_TOKENS:
            continue
        for pos in range(len(tokens) - CLONE_MIN_TOKENS + 1):
            window = "\x1f".join(tokens[pos : pos + CLONE_MIN_TOKENS])
            digest = hashlib.sha256(window.encode("utf-8")).hexdigest()[:16]
            window_map[digest].append((f_idx, pos))

    cloned_indices: list[set[int]] = [set() for _ in file_tokens_list]
    for occs in window_map.values():
        if len(occs) < 2:
            continue
        by_file: dict[int, list[int]] = defaultdict(list)
        for f_idx, pos in occs:
            by_file[f_idx].append(pos)
        is_cross_file = len(by_file) >= 2
        is_non_overlapping_same_file = any(
            positions[-1] - positions[0] >= CLONE_MIN_TOKENS for positions in by_file.values()
        )
        if not (is_cross_file or is_non_overlapping_same_file):
            continue
        for f_idx, pos in occs:
            cloned_indices[f_idx].update(range(pos, pos + CLONE_MIN_TOKENS))

    total_tokens = sum(len(t) for t in file_tokens_list)
    if total_tokens == 0:
        return 0.0
    cloned_tokens = sum(len(s) for s in cloned_indices)
    return round(min(100.0, (cloned_tokens / total_tokens) * 100.0), 2)


def _resolve_import_edges(
    file_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    # Build indexes of internal files, module stems, and declared symbol names
    file_set = {res["file"] for res in file_results}
    no_ext_set = {res["file"].rsplit(".", 1)[0] for res in file_results}
    stem_to_files: dict[str, set[str]] = defaultdict(set)
    symbol_to_files: dict[str, set[str]] = defaultdict(set)

    for res in file_results:
        fpath = res["file"]
        stem = Path(fpath).stem
        stem_to_files[stem].add(fpath)
        no_ext = fpath.rsplit(".", 1)[0]
        dotted = no_ext.replace("/", ".")
        stem_to_files[dotted].add(fpath)
        if dotted.endswith(".__init__"):
            stem_to_files[dotted.removesuffix(".__init__")].add(fpath)
        for sym in res.get("declared_symbols", []):
            symbol_to_files[sym["name"]].add(fpath)

    edge_conf: dict[tuple[str, str], float] = {}

    def _record(src: str, target: str, conf: float) -> None:
        if not target:
            return
        key = (src, target)
        if conf > edge_conf.get(key, 0.0):
            edge_conf[key] = conf

    for res in file_results:
        src_file = res["file"]
        src_dir = Path(src_file).parent

        for imp in res.get("imports", []):
            mod = str(imp.get("module", "")).strip()
            syms: list[str] = list(imp.get("symbols", []))
            is_rel = bool(imp.get("is_relative", False))
            is_wild = bool(imp.get("is_wildcard", False))

            # Check if module resolves to an internal repo file
            resolved_internal = False
            if is_rel:
                if mod:
                    candidate = (src_dir / mod.lstrip("./")).as_posix()
                    if any(
                        f == candidate
                        or f.startswith(candidate + ".")
                        or f.endswith("/" + mod.lstrip("./"))
                        for f in no_ext_set | file_set
                    ):
                        resolved_internal = True
                elif syms:
                    for sym in syms:
                        candidate = (src_dir / sym).as_posix()
                        if any(
                            f == candidate or f.startswith(candidate + "/")
                            for f in no_ext_set
                        ):
                            resolved_internal = True
                            break
            if not resolved_internal and mod:
                mod_norm = mod.replace("/", ".")
                if mod_norm in stem_to_files or mod_norm.split(".")[-1] in stem_to_files:
                    resolved_internal = True
            if not resolved_internal and any(s in symbol_to_files for s in syms):
                resolved_internal = True

            if syms:
                for sym in syms:
                    if is_wild:
                        conf = 0.8 if resolved_internal else 0.5
                    elif resolved_internal and (sym in symbol_to_files or is_rel):
                        conf = 1.0
                    elif resolved_internal:
                        conf = 0.8
                    else:
                        conf = 0.5
                    _record(src_file, sym, conf)
            elif mod:
                conf = 0.8 if resolved_internal else 0.5
                _record(src_file, mod.split(".")[-1] or mod, conf)

        # Detect same-package / same-namespace cross-file symbol references without explicit import
        for ident in res.get("referenced_identifiers", []):
            decl_files = symbol_to_files.get(ident)
            if decl_files and any(df != src_file for df in decl_files):
                _record(src_file, ident, 0.8)

    edges = [
        {"source_file": src, "target_symbol": tgt, "confidence": conf}
        for (src, tgt), conf in edge_conf.items()
    ]
    edges.sort(key=lambda e: (e["source_file"], e["target_symbol"], -e["confidence"]))
    return edges[:MAX_IMPORT_EDGES]


def analyze_repo_treesitter_metrics(
    repo_dir: Path, extensions: tuple[str, ...]
) -> dict[str, Any]:
    """
    Analyze matching source files in `repo_dir` via tree-sitter (with clean fallback)
    and return unified polyglot complexity, clone duplication, dead-code, and import metrics.
    """
    src_files = iter_source_files(repo_dir, extensions)
    if not src_files:
        return {
            "ast_engine": "tree-sitter" if is_treesitter_available() else "fallback",
            "avg_cyclomatic_complexity": 0.0,
            "max_cyclomatic_complexity": 0,
            "avg_cognitive_complexity": 0.0,
            "max_cognitive_complexity": 0,
            "duplication_pct": 0.0,
            "dead_code_count": 0,
            "dead_code_symbols": [],
            "file_complexities": [],
            "import_edges": [],
        }

    file_results: list[dict[str, Any]] = []
    used_treesitter = False
    for fpath in src_files:
        rel_path = str(fpath.relative_to(repo_dir)).replace("\\", "/")
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        parsed = analyze_source_with_treesitter(rel_path, content)
        if parsed["ast_engine"] == "tree-sitter":
            used_treesitter = True
        file_results.append(parsed)

    if not file_results:
        return {
            "ast_engine": "tree-sitter" if is_treesitter_available() else "fallback",
            "avg_cyclomatic_complexity": 0.0,
            "max_cyclomatic_complexity": 0,
            "avg_cognitive_complexity": 0.0,
            "max_cognitive_complexity": 0,
            "duplication_pct": 0.0,
            "dead_code_count": 0,
            "dead_code_symbols": [],
            "file_complexities": [],
            "import_edges": [],
        }

    cc_units: list[int] = []
    cog_units: list[int] = []
    file_complexities: list[dict[str, Any]] = []

    for res in file_results:
        top_fns = [fn for fn in res["functions"] if not fn.get("is_nested")]
        if top_fns:
            for fn in res["functions"]:
                cc_units.append(int(fn["cyclomatic_complexity"]))
            for fn in top_fns:
                cog_units.append(int(fn["cognitive_complexity"]))
        else:
            cc_units.append(int(res["cyclomatic_complexity"]))
            cog_units.append(int(res["cognitive_complexity"]))

        file_complexities.append({
            "file": res["file"],
            "loc": int(res["loc"]),
            "cyclomatic": int(res["cyclomatic_complexity"]),
            "cognitive": int(res["cognitive_complexity"]),
        })

    avg_cc = round(sum(cc_units) / len(cc_units), 2) if cc_units else 0.0
    max_cc = max(cc_units) if cc_units else 0
    avg_cog = round(sum(cog_units) / len(cog_units), 2) if cog_units else 0.0
    max_cog = max(cog_units) if cog_units else 0

    duplication_pct = _compute_clone_duplication_pct([res["tokens"] for res in file_results])

    # Build repo-wide reference counts (non-declaration identifier usages + explicit imports)
    repo_ref_counts: Counter[str] = Counter()
    file_ref_counts: dict[str, Counter[str]] = {}
    for res in file_results:
        fc = Counter(res.get("reference_counts", {}))
        file_ref_counts[res["file"]] = fc
        repo_ref_counts.update(fc)
        for imp in res.get("imports", []):
            for sym in imp.get("symbols", []):
                repo_ref_counts[sym] += 1

    dead_symbols: list[dict[str, Any]] = []
    for res in file_results:
        rel_path = res["file"]
        if _is_test_file(rel_path):
            continue
        local_refs = file_ref_counts.get(rel_path, Counter())
        for sym in res.get("declared_symbols", []):
            name = sym["name"]
            if (
                name in _IGNORED_DEAD_NAMES
                or (name.startswith("__") and name.endswith("__"))
                or name.startswith("test_")
                or sym.get("is_decorated_endpoint")
                or sym.get("is_exported")
            ):
                continue
            refs = (
                local_refs.get(name, 0)
                if sym.get("is_file_local")
                else repo_ref_counts.get(name, 0)
            )
            if refs == 0:
                dead_symbols.append({
                    "name": name,
                    "file": rel_path,
                    "line": int(sym["line"]),
                })

    dead_symbols.sort(key=lambda item: (item["file"], item["line"], item["name"]))
    file_complexities.sort(
        key=lambda item: (-item["cognitive"], -item["cyclomatic"], -item["loc"], item["file"])
    )
    import_edges = _resolve_import_edges(file_results)

    return {
        "ast_engine": "tree-sitter" if used_treesitter else "fallback",
        "avg_cyclomatic_complexity": avg_cc,
        "max_cyclomatic_complexity": max_cc,
        "avg_cognitive_complexity": avg_cog,
        "max_cognitive_complexity": max_cog,
        "duplication_pct": duplication_pct,
        "dead_code_count": len(dead_symbols),
        "dead_code_symbols": dead_symbols[:MAX_DEAD_CODE_SYMBOLS],
        "file_complexities": file_complexities[:MAX_FILE_COMPLEXITIES],
        "import_edges": import_edges,
    }
