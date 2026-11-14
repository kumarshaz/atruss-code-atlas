import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from src.analyzers.code.base import SKIP_DIRS, compute_text_loc_metrics, iter_source_files

_ANN_CLASS_RE = re.compile(
    r"((?:@\w+(?:\([^)]*\))?\s*)+)\s*(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+)*(?:class|interface)\s+(\w+)",
    re.MULTILINE,
)
_BRANCH_RE = re.compile(r"\b(if|else\s+if|for|while|switch|case|catch)\b")


def _parse_pom(pom_path: Path, repo_dir: Path) -> dict[str, Any] | None:
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
    except ET.ParseError:
        return None
    rel_path = str(pom_path.relative_to(repo_dir)).replace("\\", "/")
    artifact_id = pom_path.parent.name
    for child in root:
        if child.tag.split("}")[-1] == "artifactId" and child.text:
            artifact_id = child.text.strip()
            break
    return {
        "name": artifact_id,
        "type": "MODULE",
        "file": rel_path,
        "ecosystem": "java_springboot",
        "dependencies": [],
    }


def analyze_java_structural(repo_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Extract Maven/Gradle modules and Spring Boot Controllers, Services, and Repositories."""
    components: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for pom in sorted(repo_dir.rglob("pom.xml")):
        if any(part in SKIP_DIRS for part in pom.relative_to(repo_dir).parts):
            continue
        mod = _parse_pom(pom, repo_dir)
        if mod:
            key = (mod["name"], mod["type"], mod["file"])
            if key not in seen:
                seen.add(key)
                components.append(mod)

    java_files = iter_source_files(repo_dir, (".java", ".kt"))
    loc_metrics = compute_text_loc_metrics(java_files, comment_prefixes=("//", "/*", "*"))
    file_texts: dict[str, str] = {}
    complexities: list[int] = []

    for jfile in java_files:
        rel_path = str(jfile.relative_to(repo_dir)).replace("\\", "/")
        try:
            content = jfile.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_texts[rel_path] = content
        complexities.append(1 + len(_BRANCH_RE.findall(content)))

        for match in _ANN_CLASS_RE.finditer(content):
            annotations = match.group(1)
            cls_name = match.group(2)
            comp_type: str | None = None

            if any(a in annotations for a in ("@RestController", "@Controller", "@RequestMapping")):
                comp_type = "API_ROUTE"
            elif "@Service" in annotations:
                comp_type = "SERVICE"
            elif any(a in annotations for a in ("@Repository", "@Entity")):
                comp_type = "DATA_ACCESS_LAYER"
            elif "@SpringBootApplication" in annotations or "@Configuration" in annotations:
                comp_type = "CONFIG"

            if comp_type:
                key = (cls_name, comp_type, rel_path)
                if key not in seen:
                    seen.add(key)
                    components.append({
                        "name": cls_name,
                        "type": comp_type,
                        "file": rel_path,
                        "ecosystem": "java_springboot",
                        "dependencies": [],
                    })

    known_names = {c["name"] for c in components if c["type"] != "MODULE"}
    for comp in components:
        if comp["type"] == "MODULE":
            continue
        text = file_texts.get(comp["file"], "")
        deps = [
            name for name in sorted(known_names)
            if name != comp["name"] and re.search(rf"\b{re.escape(name)}\b", text)
        ]
        comp["dependencies"] = deps

    avg_cc = round(sum(complexities) / len(complexities), 2) if complexities else 0.0
    max_cc = max(complexities) if complexities else 0
    return components, {
        **loc_metrics,
        "avg_cyclomatic_complexity": avg_cc,
        "max_cyclomatic_complexity": max_cc,
        "component_count": len(components),
    }
