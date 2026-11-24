#!/usr/bin/env python3
"""
Detect whether staged changes under `exports/latest/` reflect semantic repository,
pipeline, security, or scorecard updates rather than pure run-timestamp noise.

Exits with 0 when semantic changes are present (should commit/deploy), or 1 when
staged diffs are purely wall-clock/run-metadata churn.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_IGNORED_VOLATILE_FILES = frozenset({
    "exports/latest/benchmark_summary.json",
    "exports/latest/benchmark_summary.md",
    "exports/latest/catalog-history.json",
    "exports/latest/anomalies.json",
    "exports/latest/repos/repositories.csv",
    "exports/latest/repos/repositories.yaml",
    "exports/latest/drift/drift_report.md",
})


def _git_output(repo_root: Path, *args: str) -> str | None:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def _load_json_safe(raw: str | None) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _strip_repo_timestamps(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    items = payload.get("items")
    if not isinstance(items, list):
        return payload
    cleaned = [
        {k: v for k, v in item.items() if k not in {"LastUpdate", "AnalyzedDate"}}
        if isinstance(item, dict)
        else item
        for item in items
    ]
    return {"count": payload.get("count"), "items": cleaned}


def _strip_pipeline_timestamp(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    return {k: v for k, v in payload.items() if k != "analyzed_at"}


def _drift_has_changes(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return True
    summary = payload.get("summary")
    if isinstance(summary, dict):
        for key, val in summary.items():
            if key in {"baseline_dir", "target_dir"}:
                continue
            if isinstance(val, (int, float)) and val > 0:
                return True
    arch = payload.get("architecture")
    if isinstance(arch, dict) and arch.get("metric_deltas"):
        return True
    return bool(payload.get("scorecard_transitions"))


def _manifest_shas_changed(head_payload: Any, curr_payload: Any) -> bool:
    if not isinstance(head_payload, dict) or not isinstance(curr_payload, dict):
        return True
    head_entries = head_payload.get("entries") or []
    curr_entries = curr_payload.get("entries") or []
    head_shas = {
        str(e.get("full_name", "")): e.get("pinned_sha")
        for e in head_entries
        if isinstance(e, dict) and e.get("full_name")
    }
    for entry in curr_entries:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("full_name", ""))
        if name in head_shas and head_shas[name] != entry.get("pinned_sha"):
            return True
    return False


def has_semantic_export_changes(repo_root: Path) -> bool:
    """Return True if staged diffs in `exports/latest/` contain non-volatile changes."""
    diff_out = _git_output(
        repo_root,
        "diff",
        "--cached",
        "--name-status",
        "--",
        "exports/latest/",
    )
    if not diff_out or not diff_out.strip():
        return False

    for line in diff_out.strip().splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0][0]
        rel_path = parts[-1].replace("\\", "/")

        if rel_path == "exports/latest/drift/drift_report.json":
            curr_file = repo_root / rel_path
            curr_data = _load_json_safe(
                curr_file.read_text(encoding="utf-8") if curr_file.exists() else None
            )
            if _drift_has_changes(curr_data):
                return True
            continue

        if rel_path in _IGNORED_VOLATILE_FILES:
            continue

        if status != "M":
            return True

        head_raw = _git_output(repo_root, "show", f"HEAD:{rel_path}")
        curr_file = repo_root / rel_path
        curr_raw = curr_file.read_text(encoding="utf-8") if curr_file.exists() else None

        if rel_path == "exports/latest/repos/repositories.json":
            if _strip_repo_timestamps(_load_json_safe(head_raw)) != _strip_repo_timestamps(
                _load_json_safe(curr_raw)
            ):
                return True
            continue

        if rel_path.startswith("exports/latest/pipelines/") and rel_path.endswith("-pipeline.json"):
            if _strip_pipeline_timestamp(_load_json_safe(head_raw)) != _strip_pipeline_timestamp(
                _load_json_safe(curr_raw)
            ):
                return True
            continue

        if rel_path == "exports/latest/benchmark_manifest.json":
            if _manifest_shas_changed(_load_json_safe(head_raw), _load_json_safe(curr_raw)):
                return True
            continue

        return True

    return False


def main() -> int:
    changed = has_semantic_export_changes(Path.cwd())
    if changed:
        print("Semantic changes detected in staged exports/latest/.")
        return 0
    print("Only volatile run timestamps changed in staged exports/latest/.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
