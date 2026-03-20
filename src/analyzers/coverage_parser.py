import re
from pathlib import Path


def parse_pytest_coverage(report_content: str) -> float | None:
    """Parse a standard pytest-cov terminal report to extract TOTAL percentage."""
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", report_content)
    if match:
        return float(match.group(1))
    return None

def parse_jacoco_coverage(report_content: str) -> float | None:
    """Parse jacoco XML heuristically."""
    # Finding the overall instruction counters at the end of the file generally
    match = re.search(r'<counter type="INSTRUCTION" missed="(\d+)" covered="(\d+)"/>', report_content)
    if match:
        missed = int(match.group(1))
        covered = int(match.group(2))
        total = missed + covered
        return round((covered / total) * 100, 2) if total > 0 else 0.0
    return None

def analyze_coverage_report(report_path: Path) -> dict[str, any]:
    """Loads a coverage artifact and routes it to the specific regex engine."""
    content = report_path.read_text(encoding="utf-8")

    cov = parse_pytest_coverage(content)
    if cov is not None:
        return {"runner": "pytest-cov", "coverage_percent": cov, "file": report_path.name}

    cov = parse_jacoco_coverage(content)
    if cov is not None:
        return {"runner": "jacoco", "coverage_percent": cov, "file": report_path.name}

    return {"runner": "unknown", "coverage_percent": 0.0, "file": report_path.name}
