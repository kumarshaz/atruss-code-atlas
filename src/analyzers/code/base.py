import os
from collections.abc import Iterable
from pathlib import Path

SKIP_DIRS = frozenset({
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "bin",
    "obj",
    "target",
    "dist",
    "build",
    ".next",
    ".astro",
    ".pytest_cache",
    ".ruff_cache",
    "vendor",
})


def iter_source_files(root_dir: Path, extensions: Iterable[str]) -> list[Path]:
    """Enumerate source files matching extensions while pruning build/vendor/git dirs."""
    ext_set = {e.lower() for e in extensions}
    matched: list[Path] = []
    for root, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        root_path = Path(root)
        for fname in sorted(filenames):
            fpath = root_path / fname
            if fpath.suffix.lower() in ext_set:
                matched.append(fpath)
    return matched


def compute_text_loc_metrics(
    files: list[Path],
    comment_prefixes: tuple[str, ...] = ("#", "//", "/*", "*"),
) -> dict[str, int]:
    """Compute files_analyzed, total loc, and non-blank/non-comment sloc deterministically."""
    total_loc = 0
    total_sloc = 0
    for fpath in files:
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        total_loc += len(lines)
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith(comment_prefixes):
                total_sloc += 1
    return {
        "files_analyzed": len(files),
        "loc": total_loc,
        "sloc": total_sloc,
    }
