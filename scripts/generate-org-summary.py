from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.exporters.org_summary_exporter import (  # noqa: E402
    build_org_summary,
    export_org_summary,
    grade_from_score,
    normalize_slug,
)

__all__ = [
    "build_org_summary",
    "export_org_summary",
    "grade_from_score",
    "normalize_slug",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-compute orgs-summary.json for Astro portal")
    parser.add_argument("--exports-dir", default="exports/latest", help="Path to exports/latest")
    parser.add_argument(
        "--output",
        default="exports/latest/orgs-summary.json",
        help="Output JSON file path",
    )
    args = parser.parse_args()
    out_path, summary = export_org_summary(Path(args.exports_dir), Path(args.output))
    print(f"Generated {out_path} ({len(summary)} orgs)")


if __name__ == "__main__":
    main()
