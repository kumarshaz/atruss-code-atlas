#!/usr/bin/env python3
"""
Local & Remote-Agent Orchestrator for Atruss Code Atlas Self-Healing Benchmark Loop.

Executes `atruss benchmark`, inspects `benchmark_summary.json` and `anomalies.json`,
reports actionable triage items grouped by analyzer stage, optionally runs the
5-Gate Agentic Workflow Validator, and rebuilds the Material Design 3 Astro site.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cli.commands.benchmark import (  # noqa: E402
    DEFAULT_CORPUS_PATH,
    execute_benchmark,
    load_replay_entries,
    sample_random_repositories,
    select_corpus_entries,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run stratified benchmark batch, triage anomalies, and optionally rebuild UI."
    )
    parser.add_argument("--corpus", default=None, help="Corpus ('popular-100') or JSON path")
    parser.add_argument("--limit", type=int, default=None, help="Max repositories to evaluate")
    parser.add_argument("--ecosystem", default=None, help="Optional ecosystem filter")
    parser.add_argument("--random-sample", type=int, default=None, help="Random sample size N")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic RNG seed")
    parser.add_argument("--replay", type=Path, default=None, help="Manifest or anomalies JSON path")
    parser.add_argument("--output-dir", default="exports", help="Exports base directory")
    parser.add_argument("--max-concurrent", type=int, default=4, help="Max concurrent workers")
    parser.add_argument("--timeout", type=float, default=180.0, help="Per-repo timeout (s)")
    parser.add_argument("--target-pass-rate", type=float, default=98.0, help="Minimum crash-free %")
    parser.add_argument(
        "--target-accuracy", type=float, default=90.0, help="Minimum classification accuracy %"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run scripts/validate_agent_workflow.py after benchmark",
    )
    parser.add_argument(
        "--rebuild-web",
        action="store_true",
        help="Run npm run build inside web/ after benchmark",
    )
    args = parser.parse_args()

    token = os.getenv("GH_TOKEN")
    mode = "corpus"
    corpus_name: str | None = args.corpus or "popular-100"

    if args.replay is not None:
        mode = "replay"
        entries, loaded_seed = load_replay_entries(args.replay)
        seed = loaded_seed if loaded_seed is not None else args.seed
        corpus_name = args.replay.name
        if args.limit:
            entries = entries[: args.limit]
    elif args.random_sample is not None:
        mode = "random-sample"
        seed = args.seed
        corpus_name = f"random-seed-{seed}"
        entries = asyncio.run(
            sample_random_repositories(
                count=args.random_sample,
                seed=seed,
                ecosystem=args.ecosystem,
                token=token,
            )
        )
    else:
        seed = args.seed
        corpus_path = (
            DEFAULT_CORPUS_PATH
            if not args.corpus or args.corpus == "popular-100"
            else Path(args.corpus)
        )
        entries = select_corpus_entries(corpus_path, ecosystem=args.ecosystem, limit=args.limit)

    summary, anomalies, latest_dir = asyncio.run(
        execute_benchmark(
            entries=entries,
            mode=mode,
            output_dir=args.output_dir,
            seed=seed,
            corpus_name=corpus_name,
            max_concurrent=args.max_concurrent,
            timeout=args.timeout,
            token=token,
        )
    )

    print("=== Atruss Self-Healing Benchmark Loop Scorecard ===")
    print(f"Run ID                 : {summary.run_id}")
    print(
        f"Repos                  : {summary.completed_repos}/{summary.total_repos} "
        f"({summary.crash_free_rate_pct}% crash-free)"
    )
    print(
        f"Classification Accuracy: {summary.classification_matched}/"
        f"{summary.classification_evaluated} ({summary.classification_accuracy_pct}%)"
    )
    print(
        f"SLA Compliance (<=180s): {summary.sla_compliant_count}/{summary.total_repos} "
        f"({summary.sla_compliance_pct}%)"
    )
    print(f"Anomalies              : {len(anomalies)} ({latest_dir / 'anomalies.json'})")

    if anomalies:
        stage_counts = Counter(a.stage for a in anomalies)
        print("Anomaly Breakdown      :", dict(stage_counts))
        for a in anomalies[:10]:
            print(f"  - [{a.stage}] {a.repo}: {a.message} -> {a.suggested_action}")

    exit_code = 0
    if summary.crash_free_rate_pct < args.target_pass_rate:
        print(
            f"THRESHOLD MISS: crash_free_rate_pct={summary.crash_free_rate_pct}% "
            f"< {args.target_pass_rate}%",
            file=sys.stderr,
        )
        exit_code = 1
    if (
        summary.classification_evaluated > 0
        and summary.classification_accuracy_pct < args.target_accuracy
    ):
        print(
            f"THRESHOLD MISS: classification_accuracy_pct="
            f"{summary.classification_accuracy_pct}% < {args.target_accuracy}%",
            file=sys.stderr,
        )
        exit_code = 1

    if args.validate:
        val_proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "validate_agent_workflow.py"),
                "--spec",
                "specs/008-public-github-100-benchmark",
                "--exports-dir",
                args.output_dir,
                "--output",
                str(Path(args.output_dir) / "latest" / "agent-eval-008-report.json"),
            ],
            cwd=REPO_ROOT,
            check=False,
        )
        if val_proc.returncode != 0:
            exit_code = val_proc.returncode

    if args.rebuild_web:
        web_proc = subprocess.run(["npm", "run", "build"], cwd=REPO_ROOT / "web", check=False)
        if web_proc.returncode != 0:
            exit_code = web_proc.returncode

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
