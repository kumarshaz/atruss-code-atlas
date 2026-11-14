import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from src.analyzers.code.base import SKIP_DIRS, compute_text_loc_metrics, iter_source_files

_CLASS_DEF_RE = re.compile(
    r"\b(?:public|internal|sealed|abstract)?\s*(?:partial\s+)?class\s+(\w+)(?:\s*:\s*([^{]+))?"
)
_MINIMAL_API_RE = re.compile(r"\bapp\.Map(Get|Post|Put|Delete|Patch)\s*\(\s*\"([^\"]+)\"")
_BRANCH_KEYWORD_RE = re.compile(r"\b(if|else\s+if|for|foreach|while|switch|case|catch|\?\?)\b")


def _parse_csproj(csproj_path: Path, repo_dir: Path) -> dict[str, Any] | None:
    try:
        tree = ET.parse(csproj_path)
        root = tree.getroot()
    except ET.ParseError:
        return None

    rel_path = str(csproj_path.relative_to(repo_dir)).replace("\\", "/")
    refs: list[str] = []
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        if tag == "ProjectReference":
            inc = elem.attrib.get("Include", "")
            if inc:
                refs.append(Path(inc.replace("\\", "/")).stem)
    return {
        "name": csproj_path.stem,
        "type": "MODULE",
        "file": rel_path,
        "ecosystem": ".net",
        "dependencies": sorted(set(refs)),
    }


def analyze_dotnet_structural(repo_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Extract .NET projects, controllers, Minimal APIs, services, DbContexts, and metrics."""
    components: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for csproj in sorted(repo_dir.rglob("*.csproj")):
        if any(part in SKIP_DIRS for part in csproj.relative_to(repo_dir).parts):
            continue
        mod = _parse_csproj(csproj, repo_dir)
        if mod:
            key = (mod["name"], mod["type"], mod["file"])
            if key not in seen:
                seen.add(key)
                components.append(mod)

    cs_files = iter_source_files(repo_dir, (".cs",))
    loc_metrics = compute_text_loc_metrics(cs_files, comment_prefixes=("//", "/*", "*"))
    file_texts: dict[str, str] = {}
    branch_counts: list[int] = []

    for cs_file in cs_files:
        rel_path = str(cs_file.relative_to(repo_dir)).replace("\\", "/")
        try:
            content = cs_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_texts[rel_path] = content
        branch_counts.append(1 + len(_BRANCH_KEYWORD_RE.findall(content)))

        for match in _CLASS_DEF_RE.finditer(content):
            cls_name = match.group(1)
            bases = match.group(2) or ""
            pre_snippet = content[max(0, match.start() - 250) : match.start()]
            last_brace = pre_snippet.rfind("}")
            if last_brace != -1:
                pre_snippet = pre_snippet[last_brace + 1 :]
            has_api_attr = "[ApiController]" in pre_snippet or "[Route(" in pre_snippet
            comp_type: str | None = None

            if has_api_attr or "ControllerBase" in bases or cls_name.endswith("Controller"):
                comp_type = "API_ROUTE"
            elif "DbContext" in bases or cls_name.endswith(("Repository", "DbContext")):
                comp_type = "DATA_ACCESS_LAYER"
            elif (
                "BackgroundService" in bases
                or "IHostedService" in bases
                or cls_name.endswith(("Service", "Handler"))
            ):
                comp_type = "SERVICE"

            if comp_type:
                key = (cls_name, comp_type, rel_path)
                if key not in seen:
                    seen.add(key)
                    components.append({
                        "name": cls_name,
                        "type": comp_type,
                        "file": rel_path,
                        "ecosystem": ".net",
                        "dependencies": [],
                    })

        for m in _MINIMAL_API_RE.finditer(content):
            verb, route = m.group(1).upper(), m.group(2)
            ep_name = f"{verb}_{route.strip('/').replace('/', '_') or 'root'}"
            key = (ep_name, "API_ROUTE", rel_path)
            if key not in seen:
                seen.add(key)
                components.append({
                    "name": ep_name,
                    "type": "API_ROUTE",
                    "file": rel_path,
                    "ecosystem": ".net",
                    "dependencies": [],
                })

    # Link constructor/field dependencies across discovered .NET components
    known_names = {c["name"] for c in components if c["type"] != "MODULE"}
    for comp in components:
        if comp["type"] == "MODULE":
            continue
        text = file_texts.get(comp["file"], "")
        deps = [
            name for name in sorted(known_names)
            if name != comp["name"] and re.search(rf"\bI?{re.escape(name)}\b", text)
        ]
        comp["dependencies"] = deps

    avg_cc = round(sum(branch_counts) / len(branch_counts), 2) if branch_counts else 0.0
    max_cc = max(branch_counts) if branch_counts else 0
    return components, {
        **loc_metrics,
        "avg_cyclomatic_complexity": avg_cc,
        "max_cyclomatic_complexity": max_cc,
        "component_count": len(components),
    }
