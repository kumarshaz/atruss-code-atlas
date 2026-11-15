from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def grade_from_score(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def normalize_slug(segment: str) -> str:
    return segment.strip().lower().lstrip(".").replace(".", "")


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_org_summary(exports_dir: Path) -> list[dict[str, Any]]:
    repos_path = exports_dir / "repos" / "repositories.json"
    if not repos_path.exists():
        return []
    raw_repos = _load_json(repos_path)
    repos = raw_repos.get("items", raw_repos) if isinstance(raw_repos, dict) else raw_repos
    if not isinstance(repos, list):
        return []

    org_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in repos:
        if isinstance(r, dict) and r.get("Organization"):
            org_map[str(r["Organization"])].append(r)

    pipeline_dir = exports_dir / "pipelines"
    reports_dir = exports_dir / "reports"
    summaries: list[dict[str, Any]] = []

    for org, org_repos in org_map.items():
        total_repos = len(org_repos)
        repos_with_pipeline = sum(1 for r in org_repos if r.get("HasPipeline"))
        repos_with_docker = sum(1 for r in org_repos if r.get("HasDockerfile"))
        pipeline_coverage_pct = (repos_with_pipeline / total_repos * 100.0) if total_repos else 0.0

        score = pipeline_coverage_pct * 0.6
        if repos_with_pipeline > 0:
            clean = 0
            evaluated = 0
            for r in org_repos:
                if not r.get("HasPipeline"):
                    continue
                rname = str(r.get("RepositoryName", ""))
                pdata = None
                for cand in (
                    pipeline_dir / f"{org}-{rname}-pipeline.json",
                    pipeline_dir / f"local-{rname}-pipeline.json",
                    pipeline_dir / f"{rname}-pipeline.json",
                ):
                    if cand.exists():
                        pdata = _load_json(cand)
                        break
                if not isinstance(pdata, dict) or not isinstance(pdata.get("workflows"), list):
                    continue
                evaluated += 1
                ap_count = sum(
                    len(wf.get("anti_patterns", []))
                    for wf in pdata["workflows"]
                    if isinstance(wf, dict) and isinstance(wf.get("anti_patterns"), list)
                )
                if ap_count == 0:
                    clean += 1
            if evaluated > 0:
                score += (clean / evaluated) * 40.0
        else:
            score = 0.0

        scorecard_sum = 0.0
        scorecard_count = 0
        cve_count = 0
        fitness_count = 0
        h2_analyzed = 0
        best_repo: dict[str, Any] | None = None
        best_repo_score = -1.0
        lang_counts: Counter[str] = Counter()
        safe_org = org.replace("/", "_")

        for r in org_repos:
            lang = str(r.get("PrimaryLanguage") or "").strip()
            if lang and lang != "Unknown":
                lang_counts[lang] += 1
            rname = str(r.get("RepositoryName", ""))
            aj = None
            for cand in (
                reports_dir / f"{org}-{rname}-analysis.json",
                reports_dir / f"{safe_org}-{rname}-analysis.json",
                reports_dir / f"local-{rname}-analysis.json",
                reports_dir / f"{rname}-analysis.json",
            ):
                if cand.exists():
                    aj = _load_json(cand)
                    break
            if not isinstance(aj, dict):
                continue
            repo_sc = -1.0
            sc = aj.get("scorecard")
            if isinstance(sc, dict) and isinstance(sc.get("overall_score"), (int, float)):
                repo_sc = float(sc["overall_score"])
                scorecard_sum += repo_sc
                scorecard_count += 1
            name_bonus = 1000.0 if rname.lower() == org.lower() else 0.0
            if repo_sc + name_bonus > best_repo_score:
                best_repo_score = repo_sc + name_bonus
                best_repo = r
            if isinstance(aj.get("vulnerabilities"), list):
                cve_count += len(aj["vulnerabilities"])
                h2_analyzed += 1
            if isinstance(aj.get("fitness_violations"), list):
                fitness_count += len(aj["fitness_violations"])
                h2_analyzed += 1

        fallback_repo = best_repo or next(
            (r for r in org_repos if str(r.get("RepositoryName", "")).lower() == org.lower()),
            org_repos[0] if org_repos else None,
        )
        primary_repo_name = str(fallback_repo.get("RepositoryName", "")) if fallback_repo else ""
        primary_repo_slug = (
            f"/reports/{normalize_slug(org)}/{normalize_slug(primary_repo_name)}/"
            if primary_repo_name
            else ""
        )
        primary_ecosystem = lang_counts.most_common(1)[0][0] if lang_counts else ""
        avg_scorecard = round(scorecard_sum / scorecard_count) if scorecard_count > 0 else None

        summaries.append({
            "org": org,
            "total_repos": total_repos,
            "repos_with_pipeline": repos_with_pipeline,
            "repos_with_docker": repos_with_docker,
            "pipeline_coverage_pct": round(pipeline_coverage_pct, 2),
            "maturity_score": round(min(100.0, max(0.0, score)), 2),
            "avg_scorecard": avg_scorecard,
            "avg_grade": grade_from_score(avg_scorecard) if avg_scorecard is not None else None,
            "open_cves": cve_count if h2_analyzed > 0 else None,
            "fitness_alerts": fitness_count if h2_analyzed > 0 else None,
            "primary_repo_name": primary_repo_name,
            "primary_repo_slug": primary_repo_slug,
            "primary_ecosystem": primary_ecosystem,
        })

    summaries.sort(key=lambda item: -item["maturity_score"])
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-compute orgs-summary.json for Astro portal")
    parser.add_argument("--exports-dir", default="exports/latest", help="Path to exports/latest")
    parser.add_argument(
        "--output",
        default="exports/latest/orgs-summary.json",
        help="Output JSON file path",
    )
    args = parser.parse_args()
    exports_dir = Path(args.exports_dir)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    summary = build_org_summary(exports_dir)
    out_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {out_path} ({len(summary)} orgs)")


if __name__ == "__main__":
    main()
