from __future__ import annotations

import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import yaml

from src.models.artifacts import DependencyRecord

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]

SKIP_DIRS = frozenset({
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "__pycache__",
    "bin",
    "obj",
    "target",
    ".next",
    ".astro",
    ".pytest_cache",
    ".ruff_cache",
})

_GRADLE_CONFIGS = frozenset({
    "implementation",
    "api",
    "compileOnly",
    "runtimeOnly",
    "testImplementation",
    "testRuntimeOnly",
    "testCompileOnly",
    "annotationProcessor",
    "kapt",
    "classpath",
    "compile",
    "testCompile",
    "debugImplementation",
    "releaseImplementation",
})

_GRADLE_STRING_RE = re.compile(
    r"""^\s*(?P<cfg>[A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\s*|\s+)['"](?P<coord>[^'"]+)['"]\s*\)?"""
)
_GRADLE_MAP_RE = re.compile(
    r"""^\s*(?P<cfg>[A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\s*|\s+)(?P<args>.*group\s*[:=].*name\s*[:=].*)$"""
)
_GRADLE_VAR_RE = re.compile(
    r"""^\s*(?:def|val|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*['"]([^'"]+)['"]"""
)
_GRADLE_EXT_ENTRY_RE = re.compile(
    r"""^\s*(?:extra\[['"]|set\(['"]|)([A-Za-z_][A-Za-z0-9_]*)(?:['"]\])?\s*=\s*['"]([^'"]+)['"]"""
)


def _normalize_pypi_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name.strip()).lower()


def build_purl(ecosystem: str, name: str, version: str = "", group: str = "") -> str:
    """Build a canonical Package URL (PURL) for PyPI, npm, NuGet, or Maven."""
    eco_lower = ecosystem.strip().lower()
    clean_name = name.strip()
    clean_ver = version.strip()

    if eco_lower == "pypi":
        base = f"pkg:pypi/{_normalize_pypi_name(clean_name)}"
    elif eco_lower == "npm":
        if clean_name.startswith("@") and "/" in clean_name:
            scope, pkg = clean_name.split("/", 1)
            base = f"pkg:npm/%40{scope[1:]}/{pkg}"
        else:
            base = f"pkg:npm/{clean_name}"
    elif eco_lower == "nuget":
        base = f"pkg:nuget/{clean_name}"
    elif eco_lower == "maven":
        clean_group = group.strip()
        base = f"pkg:maven/{clean_group}/{clean_name}" if clean_group else f"pkg:maven/{clean_name}"
    elif eco_lower == "composer" and "/" in clean_name:
        vendor, pkg = clean_name.split("/", 1)
        base = f"pkg:composer/{vendor.lower()}/{pkg.lower()}"
    elif eco_lower == "golang":
        base = f"pkg:golang/{clean_name}"
    elif eco_lower in {"cargo", "gem", "hex"}:
        base = f"pkg:{eco_lower}/{clean_name}"
    else:
        base = f"pkg:{eco_lower}/{clean_name}"

    return f"{base}@{clean_ver}" if clean_ver else base


def _clean_version(raw: str) -> str:
    """Extract a concrete version string from common version range expressions."""
    val = raw.strip().strip("\"'")
    if not val:
        return ""
    lowered = val.lower()
    if lowered in {"*", "latest", "any", "x"} or lowered.startswith((
        "workspace:",
        "file:",
        "link:",
        "portal:",
        "git+",
        "git:",
        "http://",
        "https://",
        "ssh://",
        "github:",
    )):
        return ""
    if val.startswith("npm:"):
        _head, sep, tail = val.rpartition("@")
        val = tail if sep else ""
        if not val:
            return ""
    # Handle NuGet bracketed ranges like [13.0.3, ) or [1.0.0]
    if val.startswith(("[", "(")) and val.endswith(("]", ")")):
        inner = val.strip("[]()").split(",", 1)[0].strip()
        val = inner
    # Handle space-delimited OR ranges (e.g. ">=1.0.0 <2.0.0" or "1.x || 2.x")
    if "||" in val:
        val = val.split("||", 1)[0].strip()
    if "," in val:
        clauses = [c.strip() for c in val.split(",") if c.strip()]
        chosen = ""
        for prefix in ("===", "==", "~=", ">=", "<=", ">", "<"):
            for clause in clauses:
                if clause.startswith(prefix):
                    chosen = clause
                    break
            if chosen:
                break
        val = chosen or clauses[0]
    val = re.sub(r"^(?:~>|===|==|~=|>=|<=|!=|>|<|\^|~|=)+\s*", "", val).strip()
    if " " in val:
        val = val.split()[0]

    val = re.sub(r"^(?:~>|===|==|~=|>=|<=|!=|>|<|\^|~|=)+\s*", "", val).strip()
    val = re.sub(r"^v(?=\d)", "", val)
    if not val or "*" in val or "${" in val or not re.match(r"^[0-9A-Za-z][0-9A-Za-z.+_-]*$", val):
        return ""
    return val


def _parse_pep508(spec: str) -> tuple[str, str] | None:
    """Parse a PEP 508 dependency specifier into (package_name, cleaned_version)."""
    clean = spec.split(";", 1)[0].strip()
    # Strip pip CLI flags appended on requirement lines (e.g., --hash=...)
    clean = re.sub(r"\s+--[A-Za-z0-9_-]+(?:=\S+|\s+\S+)?", "", clean).strip()
    if not clean:
        return None

    direct_ref = re.match(
        r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?\s*@\s*\S+",
        clean,
    )
    if direct_ref:
        return direct_ref.group(1), ""

    match = re.match(
        r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?\s*(.*)$",
        clean,
    )
    if not match:
        return None
    name = match.group(1)
    ver_raw = match.group(2).strip()
    version = _clean_version(ver_raw) if ver_raw else ""
    return name, version


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _parse_requirements_txt(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []

    records: list[DependencyRecord] = []
    lines = text.splitlines()
    idx = 0
    while idx < len(lines):
        start_line = idx + 1
        raw_line = lines[idx]
        idx += 1

        # Handle line continuations
        combined = raw_line
        while combined.rstrip().endswith("\\") and idx < len(lines):
            combined = combined.rstrip()[:-1] + " " + lines[idx].strip()
            idx += 1

        # Strip comments (keep #egg= inside URLs)
        stripped = combined.strip()
        if not stripped or stripped.startswith("#"):
            continue

        egg_match = re.search(r"#egg=([A-Za-z0-9][A-Za-z0-9._-]*)", stripped)
        if not egg_match:
            stripped = re.sub(r"(?:^|\s)#.*$", "", stripped).strip()
        if not stripped:
            continue

        if stripped.startswith(("-e ", "--editable ")):
            if egg_match:
                name = egg_match.group(1)
                records.append(
                    DependencyRecord(
                        name=name,
                        version="",
                        ecosystem="PyPI",
                        purl=build_purl("PyPI", name),
                        manifest_file=rel_path,
                        line=start_line,
                        is_direct=True,
                    )
                )
            continue

        if stripped.startswith("-"):
            continue

        if egg_match and ("://" in stripped or stripped.startswith("git+")):
            name = egg_match.group(1)
            records.append(
                DependencyRecord(
                    name=name,
                    version="",
                    ecosystem="PyPI",
                    purl=build_purl("PyPI", name),
                    manifest_file=rel_path,
                    line=start_line,
                    is_direct=True,
                )
            )
            continue

        parsed = _parse_pep508(stripped)
        if not parsed:
            continue
        name, version = parsed
        records.append(
            DependencyRecord(
                name=name,
                version=version,
                ecosystem="PyPI",
                purl=build_purl("PyPI", name, version),
                manifest_file=rel_path,
                line=start_line,
                is_direct=True,
            )
        )
    return records


def _parse_pyproject_toml_fallback(text: str) -> dict[str, Any]:
    """Lightweight line-based TOML dependency fallback when tomllib is unavailable."""
    project_deps: list[str] = []
    optional_deps: dict[str, list[str]] = {}
    dep_groups: dict[str, list[str]] = {}
    poetry_deps: dict[str, str] = {}
    poetry_dev_deps: dict[str, str] = {}

    section = ""
    active_list_key = ""
    in_multiline_list = False

    for raw_line in text.splitlines():
        line = re.sub(r"\s+#.*$", "", raw_line).strip()
        if not line or line.startswith("#"):
            continue

        header_match = re.match(r"^\[([^\[\]]+)\]$", line)
        if header_match:
            section = header_match.group(1).strip()
            active_list_key = ""
            in_multiline_list = False
            continue

        if in_multiline_list:
            for item in re.findall(r"""['"]([^'"]+)['"]""", line):
                if section == "project" and active_list_key == "dependencies":
                    project_deps.append(item)
                elif section == "project.optional-dependencies" and active_list_key:
                    optional_deps.setdefault(active_list_key, []).append(item)
                elif section == "dependency-groups" and active_list_key:
                    dep_groups.setdefault(active_list_key, []).append(item)
            if "]" in line:
                in_multiline_list = False
                active_list_key = ""
            continue

        kv_match = re.match(r"""^([A-Za-z0-9_.-]+)\s*=\s*(.+)$""", line)
        if not kv_match:
            continue
        key, val = kv_match.group(1).strip(), kv_match.group(2).strip()

        if section in {"project", "project.optional-dependencies", "dependency-groups"} and (
            val.startswith("[")
        ):
            items = re.findall(r"""['"]([^'"]+)['"]""", val)
            if section == "project" and key == "dependencies":
                project_deps.extend(items)
            elif section == "project.optional-dependencies":
                optional_deps.setdefault(key, []).extend(items)
            elif section == "dependency-groups":
                dep_groups.setdefault(key, []).extend(items)
            if not val.endswith("]"):
                in_multiline_list = True
                active_list_key = key
            continue

        if section == "tool.poetry.dependencies":
            ver_m = re.search(r"""version\s*=\s*['"]([^'"]+)['"]""", val)
            poetry_deps[key] = ver_m.group(1) if ver_m else val.strip("\"'")
        elif section == "tool.poetry.dev-dependencies" or (
            section.startswith("tool.poetry.group.") and section.endswith(".dependencies")
        ):
            ver_m = re.search(r"""version\s*=\s*['"]([^'"]+)['"]""", val)
            poetry_dev_deps[key] = ver_m.group(1) if ver_m else val.strip("\"'")

    return {
        "project": {
            "dependencies": project_deps,
            "optional-dependencies": optional_deps,
        },
        "dependency-groups": dep_groups,
        "tool": {
            "poetry": {
                "dependencies": poetry_deps,
                "dev-dependencies": poetry_dev_deps,
            }
        },
    }


def _find_pyproject_dep_line(lines: list[str], pkg_name: str, preferred_sections: set[str]) -> int:
    norm_pat = re.escape(pkg_name).replace(r"\-", r"[-_.]")
    quoted_re = re.compile(
        rf"""['"]{norm_pat}(?:\[[^\]]*\])?\s*(?:[=<>!~;@'"]|$)""",
        re.IGNORECASE,
    )
    key_re = re.compile(rf"""^\s*['"]?{norm_pat}['"]?\s*=""", re.IGNORECASE)
    meta_key_re = re.compile(
        r"^\s*(?:name|version|description|readme|license|requires-python|"
        r"authors|maintainers|keywords|classifiers)\s*=",
        re.IGNORECASE,
    )
    current_section = ""
    fallback_line = 0

    for idx, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        header = re.match(r"^\[([^\[\]]+)\]", stripped)
        if header:
            current_section = header.group(1).strip()
            continue
        if stripped.startswith("#"):
            continue
        if current_section == "project" and meta_key_re.match(stripped) and not (
            stripped.lower().startswith("dependencies")
        ):
            continue
        if quoted_re.search(raw_line) or key_re.match(raw_line):
            if current_section in preferred_sections:
                return idx
            if fallback_line == 0:
                fallback_line = idx
    return fallback_line or 1


def _extract_poetry_dep_version(spec: Any) -> str:
    if isinstance(spec, str):
        return _clean_version(spec)
    if isinstance(spec, dict):
        return _clean_version(str(spec.get("version", "")))
    if isinstance(spec, list) and spec:
        first = spec[0]
        if isinstance(first, dict):
            return _clean_version(str(first.get("version", "")))
    return ""


def _collect_pyproject_direct_names(data: dict[str, Any]) -> set[str]:
    direct: set[str] = set()
    project = data.get("project", {})
    if isinstance(project, dict):
        for item in project.get("dependencies", []) or []:
            if isinstance(item, str):
                parsed = _parse_pep508(item)
                if parsed:
                    direct.add(_normalize_pypi_name(parsed[0]))
        opt = project.get("optional-dependencies", {}) or {}
        if isinstance(opt, dict):
            for group_items in opt.values():
                for item in group_items or []:
                    if isinstance(item, str):
                        parsed = _parse_pep508(item)
                        if parsed:
                            direct.add(_normalize_pypi_name(parsed[0]))

    dep_groups = data.get("dependency-groups", {}) or {}
    if isinstance(dep_groups, dict):
        for group_items in dep_groups.values():
            for item in group_items or []:
                if isinstance(item, str):
                    parsed = _parse_pep508(item)
                    if parsed:
                        direct.add(_normalize_pypi_name(parsed[0]))

    poetry = (data.get("tool") or {}).get("poetry", {})
    if isinstance(poetry, dict):
        for sec_key in ("dependencies", "dev-dependencies"):
            sec = poetry.get(sec_key, {}) or {}
            if isinstance(sec, dict):
                for name in sec:
                    if name.lower() != "python":
                        direct.add(_normalize_pypi_name(name))
        groups = poetry.get("group", {}) or {}
        if isinstance(groups, dict):
            for grp in groups.values():
                if isinstance(grp, dict):
                    for name in grp.get("dependencies", {}) or {}:
                        if name.lower() != "python":
                            direct.add(_normalize_pypi_name(name))
    return direct


def _load_pyproject_data(path: Path) -> dict[str, Any]:
    text = _safe_read_text(path)
    if not text:
        return {}
    if tomllib is not None:
        try:
            loaded = tomllib.loads(text)
            if isinstance(loaded, dict):
                return loaded
        except Exception:
            pass
    return _parse_pyproject_toml_fallback(text)


def _parse_pyproject_toml(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []

    data: dict[str, Any] = {}
    if tomllib is not None:
        try:
            loaded = tomllib.loads(text)
            if isinstance(loaded, dict):
                data = loaded
        except Exception:
            data = _parse_pyproject_toml_fallback(text)
    else:
        data = _parse_pyproject_toml_fallback(text)

    lines = text.splitlines()
    records: list[DependencyRecord] = []
    seen_names: set[str] = set()

    def _add(name: str, version: str, sections: set[str]) -> None:
        norm = _normalize_pypi_name(name)
        if not norm or norm == "python" or norm in seen_names:
            return
        seen_names.add(norm)
        line_no = _find_pyproject_dep_line(lines, name, sections)
        records.append(
            DependencyRecord(
                name=name,
                version=version,
                ecosystem="PyPI",
                purl=build_purl("PyPI", name, version),
                manifest_file=rel_path,
                line=line_no,
                is_direct=True,
            )
        )

    project = data.get("project", {})
    if isinstance(project, dict):
        for item in project.get("dependencies", []) or []:
            if isinstance(item, str):
                parsed = _parse_pep508(item)
                if parsed:
                    _add(parsed[0], parsed[1], {"project"})

        opt = project.get("optional-dependencies", {}) or {}
        if isinstance(opt, dict):
            for group_items in opt.values():
                for item in group_items or []:
                    if isinstance(item, str):
                        parsed = _parse_pep508(item)
                        if parsed:
                            _add(parsed[0], parsed[1], {"project.optional-dependencies"})

    dep_groups = data.get("dependency-groups", {}) or {}
    if isinstance(dep_groups, dict):
        for group_items in dep_groups.values():
            for item in group_items or []:
                if isinstance(item, str):
                    parsed = _parse_pep508(item)
                    if parsed:
                        _add(parsed[0], parsed[1], {"dependency-groups"})

    poetry = (data.get("tool") or {}).get("poetry", {})
    if isinstance(poetry, dict):
        for sec_name, sec_set in (
            ("dependencies", {"tool.poetry.dependencies"}),
            ("dev-dependencies", {"tool.poetry.dev-dependencies"}),
        ):
            sec = poetry.get(sec_name, {}) or {}
            if isinstance(sec, dict):
                for pkg_name, spec in sec.items():
                    _add(pkg_name, _extract_poetry_dep_version(spec), sec_set)

        groups = poetry.get("group", {}) or {}
        if isinstance(groups, dict):
            for grp_name, grp_data in groups.items():
                if isinstance(grp_data, dict):
                    deps = grp_data.get("dependencies", {}) or {}
                    if isinstance(deps, dict):
                        sec_tag = f"tool.poetry.group.{grp_name}.dependencies"
                        for pkg_name, spec in deps.items():
                            _add(pkg_name, _extract_poetry_dep_version(spec), {sec_tag})

    return records


def _parse_lock_toml_fallback(text: str) -> list[dict[str, Any]]:
    """Fallback parser for [[package]] TOML lockfiles (uv.lock / poetry.lock)."""
    packages: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "[[package]]":
            if current is not None:
                packages.append(current)
            current = {}
            continue
        if current is None:
            continue
        if stripped.startswith("[") and not stripped.startswith("[["):
            continue
        kv = re.match(r"""^([A-Za-z0-9_-]+)\s*=\s*(.+)$""", stripped)
        if kv:
            k, v = kv.group(1), kv.group(2).strip()
            if k in {"name", "version", "license"}:
                current[k] = v.strip("\"'")
            elif k == "source" and ("virtual" in v or "editable" in v):
                current["source"] = {"virtual": "."}
    if current is not None:
        packages.append(current)
    return packages


def _find_package_block_lines(text: str) -> dict[tuple[str, str], int]:
    """Map (normalized_name, version) -> 1-indexed line of `name = "..."` inside [[package]]."""
    line_map: dict[tuple[str, str], int] = {}
    in_pkg = False
    pkg_name = ""
    pkg_name_line = 0
    pkg_version = ""

    def _flush() -> None:
        if pkg_name and pkg_name_line:
            key = (_normalize_pypi_name(pkg_name), pkg_version)
            line_map.setdefault(key, pkg_name_line)

    for idx, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped == "[[package]]":
            _flush()
            in_pkg = True
            pkg_name = ""
            pkg_name_line = 0
            pkg_version = ""
            continue
        if not in_pkg:
            continue
        if stripped.startswith("[") and not stripped.startswith("[["):
            continue
        name_m = re.match(r"""^name\s*=\s*['"]([^'"]+)['"]""", stripped)
        if name_m and not pkg_name:
            pkg_name = name_m.group(1)
            pkg_name_line = idx
            continue
        ver_m = re.match(r"""^version\s*=\s*['"]([^'"]+)['"]""", stripped)
        if ver_m and not pkg_version:
            pkg_version = ver_m.group(1)

    _flush()
    return line_map


def _sibling_pypi_direct_names(lock_path: Path) -> set[str]:
    direct: set[str] = set()
    pyproject = lock_path.parent / "pyproject.toml"
    if pyproject.exists():
        direct.update(_collect_pyproject_direct_names(_load_pyproject_data(pyproject)))
    for req_file in sorted(lock_path.parent.glob("requirements*.txt")):
        for rec in _parse_requirements_txt(req_file, req_file.name):
            direct.add(_normalize_pypi_name(rec.name))
    return direct


def _parse_python_lockfile(path: Path, rel_path: str, *, is_uv: bool) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []

    packages: list[dict[str, Any]] = []
    if tomllib is not None:
        try:
            loaded = tomllib.loads(text)
            if isinstance(loaded, dict) and isinstance(loaded.get("package"), list):
                packages = [p for p in loaded["package"] if isinstance(p, dict)]
        except Exception:
            packages = _parse_lock_toml_fallback(text)
    else:
        packages = _parse_lock_toml_fallback(text)

    direct_names = _sibling_pypi_direct_names(path)

    if is_uv:
        for pkg in packages:
            source = pkg.get("source")
            if isinstance(source, dict) and (
                source.get("virtual") == "." or source.get("editable") == "."
            ):
                for dep_item in pkg.get("dependencies", []) or []:
                    if isinstance(dep_item, dict) and dep_item.get("name"):
                        direct_names.add(_normalize_pypi_name(str(dep_item["name"])))
                dev_deps = pkg.get("dev-dependencies", {})
                if isinstance(dev_deps, dict):
                    for grp_items in dev_deps.values():
                        for dep_item in grp_items or []:
                            if isinstance(dep_item, dict) and dep_item.get("name"):
                                direct_names.add(_normalize_pypi_name(str(dep_item["name"])))
                elif isinstance(dev_deps, list):
                    for dep_item in dev_deps:
                        if isinstance(dep_item, dict) and dep_item.get("name"):
                            direct_names.add(_normalize_pypi_name(str(dep_item["name"])))

    line_map = _find_package_block_lines(text)
    records: list[DependencyRecord] = []

    for pkg in packages:
        source = pkg.get("source")
        if is_uv and isinstance(source, dict) and (
            source.get("virtual") == "." or source.get("editable") == "."
        ):
            continue
        name = str(pkg.get("name") or "").strip()
        if not name:
            continue
        version = str(pkg.get("version") or "").strip()
        raw_license = pkg.get("license")
        license_val = (
            str(raw_license).strip()
            if isinstance(raw_license, str) and raw_license
            else None
        )
        norm = _normalize_pypi_name(name)
        line_no = line_map.get((norm, version), 1)
        records.append(
            DependencyRecord(
                name=name,
                version=version,
                ecosystem="PyPI",
                purl=build_purl("PyPI", name, version),
                manifest_file=rel_path,
                line=line_no,
                is_direct=norm in direct_names,
                license=license_val,
            )
        )
    return records


def _extract_json_object_lines(text: str, section_keys: set[str]) -> dict[tuple[str, str], int]:
    """Find 1-indexed line numbers for top-level keys inside named JSON sections."""
    results: dict[tuple[str, str], int] = {}
    active_section: str | None = None
    brace_depth = 0
    section_start_re = re.compile(r'^\s*"([^"]+)"\s*:\s*\{')
    entry_re = re.compile(r'^\s*"([^"]+)"\s*:')

    for idx, line in enumerate(text.splitlines(), start=1):
        if active_section is None:
            sec_m = section_start_re.match(line)
            if sec_m and sec_m.group(1) in section_keys and not line.rstrip().endswith("}"):
                active_section = sec_m.group(1)
                brace_depth = line.count("{") - line.count("}")
                if brace_depth <= 0:
                    active_section = None
            continue

        if brace_depth == 1:
            ent_m = entry_re.match(line)
            if ent_m:
                results.setdefault((active_section, ent_m.group(1)), idx)

        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            active_section = None
            brace_depth = 0
    return results


def _read_package_lock_licenses(lock_path: Path) -> dict[str, str]:
    """Read per-package license metadata from sibling package-lock.json when available."""
    if not lock_path.exists():
        return {}
    text = _safe_read_text(lock_path)
    if not text:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    licenses: dict[str, str] = {}
    packages = data.get("packages")
    if isinstance(packages, dict):
        for key, info in packages.items():
            if not key.startswith("node_modules/") or not isinstance(info, dict):
                continue
            pkg_name = key.rsplit("node_modules/", 1)[-1]
            lic = info.get("license")
            if isinstance(lic, str) and lic.strip():
                licenses.setdefault(pkg_name, lic.strip())
    return licenses


def _parse_package_json(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, dict):
        return []

    sibling_licenses = _read_package_lock_licenses(path.parent / "package-lock.json")
    line_map = _extract_json_object_lines(text, {"dependencies", "devDependencies"})
    records: list[DependencyRecord] = []
    seen: set[str] = set()

    for section in ("dependencies", "devDependencies"):
        deps = data.get(section)
        if not isinstance(deps, dict):
            continue
        for pkg_name, raw_spec in deps.items():
            if not isinstance(pkg_name, str) or pkg_name in seen:
                continue
            seen.add(pkg_name)

            lic: str | None = None
            if isinstance(raw_spec, dict):
                version = _clean_version(str(raw_spec.get("version", "")))
                raw_lic = raw_spec.get("license")
                if isinstance(raw_lic, str) and raw_lic.strip():
                    lic = raw_lic.strip()
            else:
                version = _clean_version(str(raw_spec))

            if lic is None:
                lic = sibling_licenses.get(pkg_name)

            line_no = line_map.get((section, pkg_name), 1)
            records.append(
                DependencyRecord(
                    name=pkg_name,
                    version=version,
                    ecosystem="npm",
                    purl=build_purl("npm", pkg_name, version),
                    manifest_file=rel_path,
                    line=line_no,
                    is_direct=True,
                    license=lic,
                )
            )
    return records


def _sibling_npm_direct_names(lock_path: Path) -> set[str]:
    direct: set[str] = set()
    pkg_json = lock_path.parent / "package.json"
    if not pkg_json.exists():
        return direct
    try:
        data = json.loads(_safe_read_text(pkg_json) or "{}")
    except json.JSONDecodeError:
        return direct
    if isinstance(data, dict):
        for sec in ("dependencies", "devDependencies", "optionalDependencies"):
            deps = data.get(sec)
            if isinstance(deps, dict):
                direct.update(str(k) for k in deps)
    return direct


def _normalize_npm_license(raw_lic: Any) -> str | None:
    if isinstance(raw_lic, str) and raw_lic.strip():
        return raw_lic.strip()
    if isinstance(raw_lic, list):
        parts = [str(x).strip() for x in raw_lic if isinstance(x, str) and x.strip()]
        return " OR ".join(parts) if parts else None
    if isinstance(raw_lic, dict):
        val = raw_lic.get("type") or raw_lic.get("name")
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def _parse_package_lock_json(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, dict):
        return []

    lines = text.splitlines()
    direct_names = _sibling_npm_direct_names(path)
    records: list[DependencyRecord] = []

    packages = data.get("packages")
    if isinstance(packages, dict) and packages:
        root_entry = packages.get("")
        has_root_deps = False
        if isinstance(root_entry, dict):
            for sec in ("dependencies", "devDependencies", "optionalDependencies"):
                sec_map = root_entry.get(sec)
                if isinstance(sec_map, dict) and sec_map:
                    has_root_deps = True
                    direct_names.update(str(k) for k in sec_map)

        key_line_map = _extract_json_object_lines(text, {"packages"})
        for pkg_key, info in packages.items():
            if not pkg_key or not isinstance(info, dict):
                continue
            if info.get("link") is True and not info.get("version"):
                continue
            if "node_modules/" in pkg_key:
                pkg_name = pkg_key.rsplit("node_modules/", 1)[-1]
            else:
                pkg_name = str(info.get("name") or pkg_key)

            version = _clean_version(str(info.get("version") or ""))
            lic = _normalize_npm_license(info.get("license"))
            if has_root_deps or direct_names:
                is_direct = pkg_key == f"node_modules/{pkg_name}" and pkg_name in direct_names
            else:
                is_direct = pkg_key.count("node_modules/") == 1

            line_no = key_line_map.get(("packages", pkg_key), 0)
            if line_no == 0:
                pat = f'"{pkg_key}"'
                line_no = next(
                    (idx for idx, line in enumerate(lines, start=1) if pat in line),
                    1,
                )

            records.append(
                DependencyRecord(
                    name=pkg_name,
                    version=version,
                    ecosystem="npm",
                    purl=build_purl("npm", pkg_name, version),
                    manifest_file=rel_path,
                    line=line_no,
                    is_direct=is_direct,
                    license=lic,
                )
            )
        return records

    # Lockfile v1 nested dependencies dict
    top_deps = data.get("dependencies")
    if not isinstance(top_deps, dict):
        return []

    def _find_key_line(key: str, start_from: int = 1) -> int:
        pat = re.compile(rf'^\s*"{re.escape(key)}"\s*:')
        for idx in range(start_from, len(lines) + 1):
            if pat.match(lines[idx - 1]):
                return idx
        return 1

    def _walk_v1(deps_dict: dict[str, Any], depth: int, search_start: int) -> None:
        for pkg_name, info in deps_dict.items():
            if not isinstance(info, dict):
                continue
            line_no = _find_key_line(pkg_name, search_start)
            version = _clean_version(str(info.get("version") or ""))
            is_direct = depth == 0 and (not direct_names or pkg_name in direct_names)
            records.append(
                DependencyRecord(
                    name=pkg_name,
                    version=version,
                    ecosystem="npm",
                    purl=build_purl("npm", pkg_name, version),
                    manifest_file=rel_path,
                    line=line_no,
                    is_direct=is_direct,
                    license=_normalize_npm_license(info.get("license")),
                )
            )
            nested = info.get("dependencies")
            if isinstance(nested, dict):
                _walk_v1(nested, depth + 1, line_no)

    _walk_v1(top_deps, 0, 1)
    return records


def _parse_pnpm_package_key(raw_key: str) -> tuple[str, str] | None:
    """Parse pnpm-lock.yaml package keys across v5/v6/v9 formats."""
    key = raw_key.strip().strip("'\"")
    if not key:
        return None
    # Strip peer dependency suffix like (supports-color@7.2.1) or _react@18.2.0
    if "(" in key:
        key = key.split("(", 1)[0]
    if "_" in key and "@" in key and key.startswith("/"):
        # v5 peer suffix like /@scope/pkg/1.0.0_peer@2.0.0
        key = key.split("_", 1)[0]

    trimmed = key.lstrip("/")
    if not trimmed:
        return None

    # v6/v9 style: pkg@1.2.3 or @scope/pkg@1.2.3
    at_idx = trimmed.rfind("@")
    if at_idx > 0:
        name = trimmed[:at_idx]
        ver = _clean_version(trimmed[at_idx + 1 :])
        return name, ver

    # v5 style: /pkg/1.2.3 or /@scope/pkg/1.2.3
    parts = trimmed.split("/")
    if trimmed.startswith("@") and len(parts) >= 3:
        name = f"{parts[0]}/{parts[1]}"
        ver = _clean_version(parts[2])
        return name, ver
    if not trimmed.startswith("@") and len(parts) >= 2:
        name = parts[0]
        ver = _clean_version(parts[1])
        return name, ver

    return None


def _parse_pnpm_lock_yaml(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []

    direct_names = _sibling_npm_direct_names(path)
    direct_versions: dict[str, str] = {}

    def _collect_direct_map(container: dict[str, Any]) -> None:
        for sec in ("dependencies", "devDependencies", "optionalDependencies"):
            sec_map = container.get(sec)
            if isinstance(sec_map, dict):
                for pkg_name, spec in sec_map.items():
                    direct_names.add(str(pkg_name))
                    if isinstance(spec, dict) and spec.get("version"):
                        ver = _clean_version(str(spec["version"]).split("(", 1)[0])
                        if ver:
                            direct_versions.setdefault(str(pkg_name), ver)
                    elif isinstance(spec, str):
                        ver = _clean_version(spec.split("(", 1)[0])
                        if ver:
                            direct_versions.setdefault(str(pkg_name), ver)

    _collect_direct_map(data)
    importers = data.get("importers")
    if isinstance(importers, dict):
        for imp_data in importers.values():
            if isinstance(imp_data, dict):
                _collect_direct_map(imp_data)

    lines = text.splitlines()

    def _find_yaml_key_line(key: str) -> int:
        quoted_or_plain = re.compile(rf"""^\s*['"]?{re.escape(key)}['"]?\s*:""")
        for idx, line in enumerate(lines, start=1):
            if quoted_or_plain.match(line):
                return idx
        return 1

    records: list[DependencyRecord] = []
    packages = data.get("packages")
    if isinstance(packages, dict) and packages:
        for raw_key, info in packages.items():
            parsed = _parse_pnpm_package_key(str(raw_key))
            if not parsed:
                continue
            pkg_name, ver = parsed
            if not ver and isinstance(info, dict) and info.get("version"):
                ver = _clean_version(str(info["version"]))
            lic = (
                _normalize_npm_license(info.get("license"))
                if isinstance(info, dict)
                else None
            )
            records.append(
                DependencyRecord(
                    name=pkg_name,
                    version=ver,
                    ecosystem="npm",
                    purl=build_purl("npm", pkg_name, ver),
                    manifest_file=rel_path,
                    line=_find_yaml_key_line(str(raw_key)),
                    is_direct=pkg_name in direct_names,
                    license=lic,
                )
            )
        return records

    for pkg_name in sorted(direct_names):
        ver = direct_versions.get(pkg_name, "")
        records.append(
            DependencyRecord(
                name=pkg_name,
                version=ver,
                ecosystem="npm",
                purl=build_purl("npm", pkg_name, ver),
                manifest_file=rel_path,
                line=_find_yaml_key_line(pkg_name),
                is_direct=True,
            )
        )
    return records


def _local_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse_csproj(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []

    lines = text.splitlines()
    search_cursor = 0
    records: list[DependencyRecord] = []

    for elem in root.iter():
        if _local_tag(elem.tag) != "PackageReference":
            continue
        pkg_name = (elem.attrib.get("Include") or elem.attrib.get("Update") or "").strip()
        if not pkg_name:
            continue
        raw_ver = elem.attrib.get("Version", "")
        if not raw_ver:
            for child in elem:
                if _local_tag(child.tag) == "Version" and child.text:
                    raw_ver = child.text.strip()
                    break
        version = _clean_version(raw_ver)

        line_no = 1
        pat = re.compile(
            rf"""PackageReference[^>]*\b(?:Include|Update)\s*=\s*['"]{re.escape(pkg_name)}['"]"""
        )
        for idx in range(search_cursor, len(lines)):
            if pat.search(lines[idx]):
                line_no = idx + 1
                search_cursor = idx + 1
                break
        else:
            for idx, line in enumerate(lines, start=1):
                if pkg_name in line and "PackageReference" in line:
                    line_no = idx
                    break

        records.append(
            DependencyRecord(
                name=pkg_name,
                version=version,
                ecosystem="NuGet",
                purl=build_purl("NuGet", pkg_name, version),
                manifest_file=rel_path,
                line=line_no,
                is_direct=True,
            )
        )
    return records


def _parse_packages_lock_json(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, dict):
        return []

    deps_root = data.get("dependencies")
    if not isinstance(deps_root, dict):
        return []

    lines = text.splitlines()
    merged: dict[tuple[str, str], DependencyRecord] = {}

    for _tfm, tfm_deps in deps_root.items():
        if not isinstance(tfm_deps, dict):
            continue
        for pkg_name, info in tfm_deps.items():
            if not isinstance(info, dict):
                continue
            pkg_type = str(info.get("type") or "").strip().lower()
            if pkg_type == "project":
                continue
            raw_ver = str(info.get("resolved") or info.get("requested") or "")
            version = _clean_version(raw_ver)
            is_direct = pkg_type == "direct"
            key = (pkg_name, version)
            if key in merged:
                if is_direct:
                    merged[key].is_direct = True
                continue

            pat = re.compile(rf'^\s*"{re.escape(pkg_name)}"\s*:')
            line_no = next(
                (idx for idx, line in enumerate(lines, start=1) if pat.match(line)),
                1,
            )
            merged[key] = DependencyRecord(
                name=pkg_name,
                version=version,
                ecosystem="NuGet",
                purl=build_purl("NuGet", pkg_name, version),
                manifest_file=rel_path,
                line=line_no,
                is_direct=is_direct,
            )

    return list(merged.values())


def _resolve_maven_props(value: str, props: dict[str, str]) -> str:
    resolved = value.strip()
    for _ in range(4):
        if "${" not in resolved:
            break
        resolved = re.sub(
            r"\$\{([^}]+)\}",
            lambda m: props.get(m.group(1).strip(), m.group(0)),
            resolved,
        )
    return resolved


def _find_pom_dependency_lines(text: str) -> list[int]:
    """Return 1-indexed start lines of <dependency> elements outside <dependencyManagement>."""
    lines = text.splitlines()
    dep_lines: list[int] = []
    in_dep_mgmt = False
    for idx, line in enumerate(lines, start=1):
        if "<dependencyManagement" in line:
            in_dep_mgmt = True
        if "</dependencyManagement>" in line:
            in_dep_mgmt = False
        if not in_dep_mgmt and re.search(r"<dependency(?:\s|>|$)", line):
            dep_lines.append(idx)
    return dep_lines


def _parse_pom_xml(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []

    props: dict[str, str] = {}
    for child in root:
        tag = _local_tag(child.tag)
        if tag == "version" and child.text:
            props["project.version"] = child.text.strip()
        elif tag == "groupId" and child.text:
            props["project.groupId"] = child.text.strip()
        elif tag == "properties":
            for prop_el in child:
                if prop_el.text:
                    props[_local_tag(prop_el.tag)] = prop_el.text.strip()

    managed_versions: dict[tuple[str, str], str] = {}
    for child in root:
        if _local_tag(child.tag) == "dependencyManagement":
            for sub in child:
                if _local_tag(sub.tag) == "dependencies":
                    for dep_el in sub:
                        if _local_tag(dep_el.tag) != "dependency":
                            continue
                        g = a = v = ""
                        for field_el in dep_el:
                            ft = _local_tag(field_el.tag)
                            if ft == "groupId" and field_el.text:
                                g = _resolve_maven_props(field_el.text, props)
                            elif ft == "artifactId" and field_el.text:
                                a = _resolve_maven_props(field_el.text, props)
                            elif ft == "version" and field_el.text:
                                v = _resolve_maven_props(field_el.text, props)
                        if g and a and v:
                            managed_versions[(g, a)] = v

    dep_block_lines = _find_pom_dependency_lines(text)
    lines = text.splitlines()
    records: list[DependencyRecord] = []
    dep_idx = 0

    for child in root:
        if _local_tag(child.tag) != "dependencies":
            continue
        for dep_el in child:
            if _local_tag(dep_el.tag) != "dependency":
                continue
            g = a = v = ""
            for field_el in dep_el:
                ft = _local_tag(field_el.tag)
                if ft == "groupId" and field_el.text:
                    g = _resolve_maven_props(field_el.text, props)
                elif ft == "artifactId" and field_el.text:
                    a = _resolve_maven_props(field_el.text, props)
                elif ft == "version" and field_el.text:
                    v = _resolve_maven_props(field_el.text, props)

            if not v and g and a:
                v = managed_versions.get((g, a), "")

            line_no = dep_block_lines[dep_idx] if dep_idx < len(dep_block_lines) else 1
            dep_idx += 1

            if not g or not a:
                continue

            # Refine line_no if dep_block_lines missed due to formatting
            if line_no == 1 and lines:
                aid_tag = f"<artifactId>{a}</artifactId>"
                line_no = next(
                    (idx for idx, ln in enumerate(lines, start=1) if aid_tag in ln),
                    1,
                )

            version = _clean_version(v) if v else ""
            full_name = f"{g}:{a}"
            records.append(
                DependencyRecord(
                    name=full_name,
                    version=version,
                    ecosystem="Maven",
                    purl=build_purl("Maven", a, version, group=g),
                    manifest_file=rel_path,
                    line=line_no,
                    is_direct=True,
                )
            )
    return records


def _strip_c_comments_preserve_lines(text: str) -> str:
    """Replace /* ... */ and // ... comments with spaces while keeping line numbers intact."""
    out: list[str] = []
    i = 0
    n = len(text)
    in_quote: str | None = None
    while i < n:
        ch = text[i]
        if in_quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == in_quote:
                in_quote = None
            i += 1
            continue
        if ch in {"'", '"'}:
            in_quote = ch
            out.append(ch)
            i += 1
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                end = n
            else:
                end += 2
            segment = text[i:end]
            out.append("".join("\n" if c == "\n" else " " for c in segment))
            i = end
            continue
        if text.startswith("//", i):
            end = text.find("\n", i + 2)
            if end == -1:
                end = n
            out.append(" " * (end - i))
            i = end
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _resolve_gradle_vars(value: str, variables: dict[str, str]) -> str:
    resolved = re.sub(
        r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}",
        lambda m: variables.get(m.group(1), m.group(0)),
        value,
    )
    resolved = re.sub(
        r"\$([A-Za-z_][A-Za-z0-9_]*)",
        lambda m: variables.get(m.group(1), m.group(0)),
        resolved,
    )
    return resolved


def _parse_gradle(path: Path, rel_path: str) -> list[DependencyRecord]:
    raw_text = _safe_read_text(path)
    if not raw_text:
        return []
    text = _strip_c_comments_preserve_lines(raw_text)
    lines = text.splitlines()

    variables: dict[str, str] = {}
    for line in lines:
        for pat in (_GRADLE_VAR_RE, _GRADLE_EXT_ENTRY_RE):
            m = pat.match(line)
            if m:
                variables[m.group(1)] = m.group(2)

    records: list[DependencyRecord] = []
    for idx, line in enumerate(lines, start=1):
        str_m = _GRADLE_STRING_RE.match(line)
        if str_m and str_m.group("cfg") in _GRADLE_CONFIGS:
            coord = _resolve_gradle_vars(str_m.group("coord"), variables)
            parts = coord.split(":")
            if len(parts) >= 2 and parts[0] and parts[1]:
                group_id, artifact_id = parts[0].strip(), parts[1].strip()
                raw_ver = parts[2].strip() if len(parts) >= 3 else ""
                version = _clean_version(raw_ver) if raw_ver else ""
                records.append(
                    DependencyRecord(
                        name=f"{group_id}:{artifact_id}",
                        version=version,
                        ecosystem="Maven",
                        purl=build_purl("Maven", artifact_id, version, group=group_id),
                        manifest_file=rel_path,
                        line=idx,
                        is_direct=True,
                    )
                )
            continue

        map_m = _GRADLE_MAP_RE.match(line)
        if map_m and map_m.group("cfg") in _GRADLE_CONFIGS:
            args = map_m.group("args")
            g_m = re.search(r"""group\s*[:=]\s*['"]([^'"]+)['"]""", args)
            a_m = re.search(r"""name\s*[:=]\s*['"]([^'"]+)['"]""", args)
            v_m = re.search(r"""version\s*[:=]\s*['"]([^'"]+)['"]""", args)
            if g_m and a_m:
                group_id = _resolve_gradle_vars(g_m.group(1), variables).strip()
                artifact_id = _resolve_gradle_vars(a_m.group(1), variables).strip()
                raw_ver = _resolve_gradle_vars(v_m.group(1), variables).strip() if v_m else ""
                version = _clean_version(raw_ver) if raw_ver else ""
                records.append(
                    DependencyRecord(
                        name=f"{group_id}:{artifact_id}",
                        version=version,
                        ecosystem="Maven",
                        purl=build_purl("Maven", artifact_id, version, group=group_id),
                        manifest_file=rel_path,
                        line=idx,
                        is_direct=True,
                    )
                )
    return records


def _parse_go_mod(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    records: list[DependencyRecord] = []
    in_require = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        if line.startswith("require ("):
            in_require = True
            continue
        if in_require and line == ")":
            in_require = False
            continue
        if line.startswith("require "):
            body = line[len("require ") :].strip()
        elif in_require:
            body = line
        else:
            body = ""
        if not body:
            continue
        parts = body.split()
        if len(parts) >= 2:
            mod, ver = parts[0], parts[1].lstrip("v")
            is_direct = "// indirect" not in raw
            records.append(
                DependencyRecord(
                    ecosystem="golang",
                    name=mod,
                    version=ver,
                    purl=build_purl("golang", mod, ver),
                    manifest_file=rel_path,
                    line=lineno,
                    is_direct=is_direct,
                )
            )
    return records


def _parse_cargo_toml(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text or tomllib is None:
        return []
    try:
        data = tomllib.loads(text)
    except Exception:
        return []
    if not isinstance(data, dict):
        return []
    lines = text.splitlines()
    records: list[DependencyRecord] = []
    for section in ("dependencies", "dev-dependencies", "build-dependencies"):
        deps = data.get(section)
        if not isinstance(deps, dict):
            continue
        is_direct = section == "dependencies"
        for name, spec in deps.items():
            if isinstance(spec, str):
                raw_ver = spec
            elif isinstance(spec, dict):
                raw_ver = spec.get("version", "")
            else:
                raw_ver = ""
            ver = _clean_version(str(raw_ver))
            lineno = 1
            pat = re.compile(rf"^\s*{re.escape(str(name))}\s*=")
            for idx, line in enumerate(lines, start=1):
                if pat.match(line):
                    lineno = idx
                    break
            records.append(
                DependencyRecord(
                    ecosystem="cargo",
                    name=str(name),
                    version=ver,
                    purl=build_purl("cargo", str(name), ver),
                    manifest_file=rel_path,
                    line=lineno,
                    is_direct=is_direct,
                )
            )
    return records


def _parse_cargo_lock(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text or tomllib is None:
        return []
    try:
        data = tomllib.loads(text)
    except Exception:
        return []
    pkgs = data.get("package") if isinstance(data, dict) else None
    if not isinstance(pkgs, list):
        return []
    records: list[DependencyRecord] = []
    for idx, pkg in enumerate(pkgs, start=1):
        if not isinstance(pkg, dict):
            continue
        name = str(pkg.get("name") or "").strip()
        ver = str(pkg.get("version") or "").strip()
        if not name:
            continue
        records.append(
            DependencyRecord(
                ecosystem="cargo",
                name=name,
                version=ver,
                purl=build_purl("cargo", name, ver),
                manifest_file=rel_path,
                line=idx,
                is_direct=False,
            )
        )
    return records


def _parse_gemfile(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    gem_re = re.compile(r"""^\s*gem\s+['"]([^'"]+)['"](?:\s*,\s*['"]([^'"]+)['"])?""")
    records: list[DependencyRecord] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = gem_re.match(line)
        if not m:
            continue
        name = m.group(1).strip()
        ver = _clean_version(m.group(2) or "")
        records.append(
            DependencyRecord(
                ecosystem="gem",
                name=name,
                version=ver,
                purl=build_purl("gem", name, ver),
                manifest_file=rel_path,
                line=lineno,
                is_direct=True,
            )
        )
    return records


def _parse_composer_json(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, dict):
        return []
    lines = text.splitlines()
    records: list[DependencyRecord] = []
    for section, is_direct in (("require", True), ("require-dev", False)):
        deps = data.get(section)
        if not isinstance(deps, dict):
            continue
        for name, raw_ver in deps.items():
            if name == "php" or name.startswith("ext-"):
                continue
            ver = _clean_version(str(raw_ver))
            lineno = 1
            for idx, line in enumerate(lines, start=1):
                if f'"{name}"' in line:
                    lineno = idx
                    break
            records.append(
                DependencyRecord(
                    ecosystem="composer",
                    name=name,
                    version=ver,
                    purl=build_purl("composer", name, ver),
                    manifest_file=rel_path,
                    line=lineno,
                    is_direct=is_direct,
                )
            )
    return records


def _parse_mix_exs(path: Path, rel_path: str) -> list[DependencyRecord]:
    text = _safe_read_text(path)
    if not text:
        return []
    dep_re = re.compile(r"""\{\s*:([a-zA-Z0-9_]+)\s*,\s*["']([^"']+)["']""")
    records: list[DependencyRecord] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in dep_re.finditer(line):
            name = m.group(1)
            ver = _clean_version(m.group(2))
            records.append(
                DependencyRecord(
                    ecosystem="hex",
                    name=name,
                    version=ver,
                    purl=build_purl("hex", name, ver),
                    manifest_file=rel_path,
                    line=lineno,
                    is_direct=True,
                )
            )
    return records


def _iter_manifest_files(repo_dir: Path) -> list[Path]:
    matched: list[Path] = []
    for root, dirnames, filenames in os.walk(repo_dir):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        root_path = Path(root)
        for fname in sorted(filenames):
            fpath = root_path / fname
            low = fname.lower()
            if (
                (low.startswith("requirements") and low.endswith(".txt"))
                or low in {
                    "pyproject.toml",
                    "uv.lock",
                    "poetry.lock",
                    "package.json",
                    "package-lock.json",
                    "pnpm-lock.yaml",
                    "packages.lock.json",
                    "pom.xml",
                    "build.gradle",
                    "build.gradle.kts",
                    "go.mod",
                    "cargo.toml",
                    "cargo.lock",
                    "gemfile",
                    "composer.json",
                    "mix.exs",
                }
                or low.endswith(".csproj")
            ):
                matched.append(fpath)
    return matched


def parse_repository_dependencies(repo_dir: Path) -> list[DependencyRecord]:
    """
    Parse direct and transitive dependency manifests and lockfiles across Python,
    JS/TS, .NET, Java, Go, Rust, Ruby, PHP, and Elixir repositories with exact
    1-indexed line numbers and PURLs.
    """
    if not repo_dir.exists() or not repo_dir.is_dir():
        return []

    records: list[DependencyRecord] = []
    for fpath in _iter_manifest_files(repo_dir):
        rel_path = fpath.relative_to(repo_dir).as_posix()
        low = fpath.name.lower()

        if low.startswith("requirements") and low.endswith(".txt"):
            records.extend(_parse_requirements_txt(fpath, rel_path))
        elif low == "pyproject.toml":
            records.extend(_parse_pyproject_toml(fpath, rel_path))
        elif low == "uv.lock":
            records.extend(_parse_python_lockfile(fpath, rel_path, is_uv=True))
        elif low == "poetry.lock":
            records.extend(_parse_python_lockfile(fpath, rel_path, is_uv=False))
        elif low == "package.json":
            records.extend(_parse_package_json(fpath, rel_path))
        elif low == "package-lock.json":
            records.extend(_parse_package_lock_json(fpath, rel_path))
        elif low == "pnpm-lock.yaml":
            records.extend(_parse_pnpm_lock_yaml(fpath, rel_path))
        elif low.endswith(".csproj"):
            records.extend(_parse_csproj(fpath, rel_path))
        elif low == "packages.lock.json":
            records.extend(_parse_packages_lock_json(fpath, rel_path))
        elif low == "pom.xml":
            records.extend(_parse_pom_xml(fpath, rel_path))
        elif low in {"build.gradle", "build.gradle.kts"}:
            records.extend(_parse_gradle(fpath, rel_path))
        elif low == "go.mod":
            records.extend(_parse_go_mod(fpath, rel_path))
        elif low == "cargo.toml":
            records.extend(_parse_cargo_toml(fpath, rel_path))
        elif low == "cargo.lock":
            records.extend(_parse_cargo_lock(fpath, rel_path))
        elif low == "gemfile":
            records.extend(_parse_gemfile(fpath, rel_path))
        elif low == "composer.json":
            records.extend(_parse_composer_json(fpath, rel_path))
        elif low == "mix.exs":
            records.extend(_parse_mix_exs(fpath, rel_path))

    # Deduplicate exact (manifest_file, line, purl) collisions while sorting deterministically
    unique: dict[tuple[str, int, str], DependencyRecord] = {}
    for rec in records:
        key = (rec.manifest_file, rec.line, rec.purl)
        if key not in unique:
            unique[key] = rec

    return sorted(unique.values(), key=lambda d: (d.manifest_file, d.line, d.purl))
