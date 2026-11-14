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
})


def iter_source_files(root_dir: Path, extensions: Iterable[str]) -> list[Path]:
    """Enumerate source files matching extensions while skipping build/vendor dirs."""
    ext_set = {e.lower() for e in extensions}
    matched: list[Path] = []
    for path in root_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root_dir).parts):
            continue
        if path.suffix.lower() in ext_set:
            matched.append(path)
    return sorted(matched, key=lambda p: str(p.relative_to(root_dir)))


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
