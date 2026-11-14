from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


class Ecosystem(str, Enum):
    PYTHON = "python"
    DOTNET = ".net"
    REACT_TS_JS = "react_ts_js"
    JAVA_SPRINGBOOT = "java_springboot"
    UNKNOWN = "unknown"


_DEFAULT_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "manifests" / "ecosystems.yaml"


@dataclass
class MonorepoModule:
    path: str
    ecosystem: Ecosystem
    display_language: str
    framework: str
    manifest_files: list[str] = field(default_factory=list)


@dataclass
class ClassificationResult:
    ecosystem: Ecosystem
    framework: str
    display_language: str = "Unknown"
    all_frameworks: list[str] = field(default_factory=list)
    deployable_types: list[str] = field(default_factory=list)
    technology_stack: str = "Traditional"
    signals: dict[str, bool] = field(default_factory=dict)
    documentation_priority: str = "P3"
    modules: list[MonorepoModule] = field(default_factory=list)


@lru_cache(maxsize=8)
def _load_manifest_cached(resolved_path: str, mtime_ns: int) -> dict[str, Any]:
    with open(resolved_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def load_ecosystems_manifest(manifest_path: Path | str | None = None) -> dict[str, Any]:
    """Load the declarative YAML classification manifest."""
    env_override = os.getenv("ATRUSS_ECOSYSTEMS_MANIFEST")
    path = Path(manifest_path or env_override or _DEFAULT_MANIFEST_PATH).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Ecosystems manifest not found at: {path}")
    stat = path.stat()
    return _load_manifest_cached(str(path), stat.st_mtime_ns)


def _normalize_paths(file_paths: list[str]) -> list[str]:
    return [p.replace("\\", "/").removeprefix("./") for p in file_paths if p]


def _matches_any(patterns: list[str], candidates: list[str]) -> bool:
    for pattern in patterns:
        regex = re.compile(pattern)
        if any(regex.search(item) for item in candidates):
            return True
    return False


def _detect_ecosystem_from_manifest(
    paths: list[str],
    manifest: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    """Score ecosystems against normalized paths using YAML rules."""
    ecosystems = sorted(
        manifest.get("ecosystems", []),
        key=lambda e: e.get("priority", 0),
        reverse=True,
    )

    scored: list[tuple[int, int, dict[str, Any]]] = []
    for eco in ecosystems:
        score = 0
        manifest_pats = eco.get("manifest_patterns", [])
        ext_pats = eco.get("extension_patterns", [])
        path_sigs = eco.get("path_signals", [])

        for p in paths:
            depth = p.count("/")
            if any(re.search(pat, p) for pat in manifest_pats):
                score += 30 if depth == 0 else 15
            elif any(re.search(pat, p) for pat in path_sigs):
                score += 10
            elif any(re.search(pat, p) for pat in ext_pats):
                score += 2

        if score > 0:
            scored.append((score, int(eco.get("priority", 0)), eco))

    if not scored:
        return None, []

    # Primary choice: prioritize manifest presence + root proximity, breaking ties by YAML priority.
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    matched_ecos = [item[2] for item in scored]
    return scored[0][2], matched_ecos


def _detect_frameworks_for_ecosystem(
    eco_cfg: dict[str, Any],
    paths: list[str],
    contents_corpus: list[str],
) -> list[str]:
    detected: list[str] = []
    for fw in eco_cfg.get("frameworks", []):
        name = fw.get("name")
        if not name:
            continue
        path_pats = fw.get("path_patterns", [])
        content_pats = fw.get("content_patterns", [])
        matched_path = _matches_any(path_pats, paths) if path_pats else False
        matched_content = _matches_any(content_pats, contents_corpus) if content_pats else False
        if matched_path or matched_content:
            detected.append(name)
    return detected


def _resolve_enum(eco_id: str) -> Ecosystem:
    try:
        return Ecosystem(eco_id)
    except ValueError:
        return Ecosystem.UNKNOWN


def detect_monorepo_modules(
    file_paths: list[str],
    file_contents: dict[str, str] | None = None,
    manifest_path: Path | str | None = None,
) -> list[MonorepoModule]:
    """Identify independent monorepo module units anchored by manifest files."""
    manifest = load_ecosystems_manifest(manifest_path)
    paths = _normalize_paths(file_paths)
    contents = {
        k.replace("\\", "/").removeprefix("./"): v for k, v in (file_contents or {}).items()
    }

    anchor_dirs: dict[str, list[str]] = {}
    all_manifest_pats = [
        (eco, pat)
        for eco in manifest.get("ecosystems", [])
        for pat in eco.get("manifest_patterns", [])
    ]

    for p in paths:
        for _eco, pat in all_manifest_pats:
            if re.search(pat, p):
                parent = str(Path(p).parent)
                module_dir = "." if parent in ("", ".") else parent
                anchor_dirs.setdefault(module_dir, []).append(p)
                break

    modules: list[MonorepoModule] = []
    for module_dir in sorted(anchor_dirs.keys()):
        if module_dir == ".":
            # Root files plus non-anchored subfiles
            sub_paths = paths
        else:
            prefix = f"{module_dir}/"
            sub_paths = [p[len(prefix):] for p in paths if p.startswith(prefix)]

        sub_contents = [
            v
            for k, v in contents.items()
            if module_dir == "." or k.startswith(f"{module_dir}/")
        ]

        primary_cfg, _ = _detect_ecosystem_from_manifest(sub_paths, manifest)
        if not primary_cfg:
            continue

        eco_enum = _resolve_enum(primary_cfg["id"])
        frameworks = _detect_frameworks_for_ecosystem(primary_cfg, sub_paths, sub_contents)
        modules.append(
            MonorepoModule(
                path=module_dir,
                ecosystem=eco_enum,
                display_language=primary_cfg.get("display_name", eco_enum.value),
                framework=frameworks[0] if frameworks else "Unknown",
                manifest_files=sorted(anchor_dirs[module_dir]),
            )
        )

    return modules


def classify_repository(
    file_paths: list[str],
    file_contents: dict[str, str] | None = None,
    manifest_path: Path | str | None = None,
    release_count: int = 0,
    fallback_language: str | None = None,
) -> ClassificationResult:
    """
    Classifies a repository using externalized Policy-as-Code YAML manifests.
    Computes ecosystem, sub-frameworks, monorepo modules, and 27-column discovery signals.
    """
    manifest = load_ecosystems_manifest(manifest_path)
    paths = _normalize_paths(file_paths)
    contents = {
        k.replace("\\", "/").removeprefix("./"): v for k, v in (file_contents or {}).items()
    }
    contents_corpus = list(contents.values())

    # 1. Evaluate discovery signals from YAML
    signal_rules = manifest.get("discovery_signals", {})
    signals: dict[str, bool] = {}
    for sig_name, sig_patterns in signal_rules.items():
        signals[sig_name] = _matches_any(sig_patterns, paths)

    # 2. Detect primary and secondary ecosystems
    primary_cfg, matched_ecos = _detect_ecosystem_from_manifest(paths, manifest)
    modules = detect_monorepo_modules(paths, contents, manifest_path=manifest_path)

    if primary_cfg:
        # Check PRD tie-break when multiple modules exist at equal manifest level
        eco_enum = _resolve_enum(primary_cfg["id"])
        display_language = primary_cfg.get("display_name", eco_enum.value)
    else:
        eco_enum = Ecosystem.UNKNOWN
        display_language = fallback_language or "Unknown"

    all_frameworks: list[str] = []
    for eco_cfg in matched_ecos:
        fws = _detect_frameworks_for_ecosystem(eco_cfg, paths, contents_corpus)
        for fw in fws:
            if fw not in all_frameworks:
                all_frameworks.append(fw)

    primary_framework = "Unknown"
    if primary_cfg:
        primary_fws = _detect_frameworks_for_ecosystem(primary_cfg, paths, contents_corpus)
        if primary_fws:
            primary_framework = primary_fws[0]
        elif modules:
            for mod in modules:
                if mod.ecosystem == eco_enum and mod.framework != "Unknown":
                    primary_framework = mod.framework
                    break

    # 3. Deployable types and technology stack
    deployable_map = manifest.get("deployable_mappings", {})
    deployable_types = [
        label for sig_key, label in deployable_map.items() if signals.get(sig_key, False)
    ]

    stack_map = manifest.get("stack_mappings", {})
    stack_tokens = [
        label for sig_key, label in stack_map.items() if signals.get(sig_key, False)
    ]
    if display_language != "Unknown" and display_language not in stack_tokens:
        stack_tokens.insert(0, display_language)
    tech_stack = ", ".join(stack_tokens) if stack_tokens else "Traditional"

    # 4. Documentation Priority (P1..P4)
    p1_min_releases = int(manifest.get("documentation_priority", {}).get("p1_min_releases", 3))
    has_pipeline = signals.get("HasPipeline", False)
    has_api_or_service = signals.get("HasAPI", False) or signals.get("HasService", False)
    has_infra = signals.get("HasDockerfile", False) or signals.get("HasKubernetes", False)

    if release_count > p1_min_releases or (has_pipeline and has_api_or_service):
        doc_priority = "P1"
    elif has_pipeline or (display_language != "Unknown" and has_infra):
        doc_priority = "P2"
    elif display_language != "Unknown":
        doc_priority = "P3"
    else:
        doc_priority = "P4"

    return ClassificationResult(
        ecosystem=eco_enum,
        framework=primary_framework,
        display_language=display_language,
        all_frameworks=all_frameworks,
        deployable_types=deployable_types,
        technology_stack=tech_stack,
        signals=signals,
        documentation_priority=doc_priority,
        modules=modules,
    )
