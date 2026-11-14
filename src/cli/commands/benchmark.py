from __future__ import annotations

import asyncio
import json
import random
import shutil
import time
import traceback
from collections import Counter, defaultdict
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import typer

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.orchestrator import _collect_repo_files_and_contents
from src.analyzers.pipeline.parser import discover_local_workflows
from src.cli.commands.analyze_code import _analyze_repo_code, _get_git_sha
from src.cli.commands.analyze_pipeline import _analyze_workflows_from_contents
from src.core.auth import setup_secure_logging
from src.core.exporters.discovery_exporter import DiscoveryArchiver
from src.core.exporters.markdown_exporter import MarkdownArchiver
from src.core.exporters.pipeline_exporter import TopologyArchiver
from src.core.http_client import GitHubClient
from src.core.utils.export_manager import ExportManager
from src.core.utils.git_cloner import GitCloner
from src.core.utils.markdown_exporter import MarkdownExporter
from src.models.artifacts import PortableArtifact
from src.models.benchmark import (
    DISPLAY_TO_ECOSYSTEM_KEY,
    ECOSYSTEM_KEY_TO_DISPLAY,
    AnomalyRecord,
    BenchmarkManifest,
    BenchmarkRepoResult,
    BenchmarkSummary,
    CorpusEntry,
)
from src.models.discovery import DiscoveryManifestItem
from src.models.topology import TopologyNode, WorkflowRun

app = typer.Typer()

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CORPUS_PATH = REPO_ROOT / "tests" / "fixtures" / "popular_100_corpus.json"

STAR_BUCKETS: tuple[tuple[str, str], ...] = (
    ("100..1000", "stars:100..1000"),
    ("1000..10000", "stars:1000..10000"),
    (">10000", "stars:>10000"),
)

ECOSYSTEM_SEARCH_LANG: dict[str, str] = {
    "python": "language:Python",
    ".net": "language:C#",
    "react_ts_js": "language:TypeScript",
    "java_springboot": "language:Java",
}


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_ecosystem_filter(raw: str | None) -> str | None:
    if not raw:
        return None
    cleaned = raw.strip().lower()
    aliases = {
        "python": "python",
        "py": "python",
        ".net": ".net",
        "dotnet": ".net",
        "csharp": ".net",
        "c#": ".net",
        "react_ts_js": "react_ts_js",
        "js": "react_ts_js",
        "ts": "react_ts_js",
        "js_ts": "react_ts_js",
        "javascript": "react_ts_js",
        "typescript": "react_ts_js",
        "javascript/typescript": "react_ts_js",
        "react": "react_ts_js",
        "nodejs": "react_ts_js",
        "java": "java_springboot",
        "java_springboot": "java_springboot",
        "springboot": "java_springboot",
        "spring-boot": "java_springboot",
    }
    if cleaned in aliases:
        return aliases[cleaned]
    if raw in DISPLAY_TO_ECOSYSTEM_KEY:
        return DISPLAY_TO_ECOSYSTEM_KEY[raw]
    raise typer.BadParameter(
        f"Unsupported ecosystem filter '{raw}'. Choose from: "
        "python, .net, react_ts_js, java_springboot"
    )


def select_corpus_entries(
    corpus_path: Path,
    ecosystem: str | None = None,
    limit: int | None = None,
) -> list[CorpusEntry]:
    """Load corpus JSON and perform optional ecosystem filtering or stratified slicing."""
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")

    raw = json.loads(corpus_path.read_text(encoding="utf-8"))
    items = raw.get("repositories", raw) if isinstance(raw, dict) else raw
    entries = [CorpusEntry.model_validate(item) for item in items]

    eco_key = _normalize_ecosystem_filter(ecosystem)
    if eco_key:
        entries = [e for e in entries if e.ecosystem_key == eco_key]
        return entries[:limit] if limit else entries

    if not limit or limit >= len(entries):
        return entries

    # Stratified round-robin slice across ecosystems (`--limit 12` hits 3 per ecosystem)
    buckets: dict[str, list[CorpusEntry]] = defaultdict(list)
    for entry in entries:
        buckets[entry.ecosystem_key].append(entry)

    selected: list[CorpusEntry] = []
    eco_order = ["python", ".net", "react_ts_js", "java_springboot"]
    for extra in buckets:
        if extra not in eco_order:
            eco_order.append(extra)

    idx = 0
    while len(selected) < limit:
        added_in_round = False
        for key in eco_order:
            bucket = buckets.get(key, [])
            if idx < len(bucket):
                selected.append(bucket[idx])
                added_in_round = True
                if len(selected) >= limit:
                    break
        if not added_in_round:
            break
        idx += 1

    return selected


def _star_tier_for_count(stars: int, default_tier: str) -> str:
    if stars > 10000:
        return ">10000"
    if stars >= 1000:
        return "1000..10000"
    if stars >= 100:
        return "100..1000"
    return default_tier


async def _ls_remote_head_sha(clone_url: str, branch: str) -> str | None:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "ls-remote",
        clone_url,
        branch,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=15.0)
    except asyncio.TimeoutError:
        proc.kill()
        return None
    if proc.returncode != 0:
        return None
    lines = stdout.decode("utf-8", errors="replace").strip().splitlines()
    return lines[0].split()[0] if lines else None


async def sample_random_repositories(
    count: int,
    seed: int = 42,
    ecosystem: str | None = None,
    token: str | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
    logger: Any = None,
) -> list[CorpusEntry]:
    """
    Dynamically sample `count` public GitHub repositories stratified across ecosystems
    and star tiers (`100..1000`, `1000..10000`, `>10000`) using a deterministic RNG seed.
    """
    rng = random.Random(seed)
    eco_key = _normalize_ecosystem_filter(ecosystem)
    eco_keys = [eco_key] if eco_key else ["python", ".net", "react_ts_js", "java_springboot"]

    # Build deterministic slot targets: (eco_key, (tier_label, tier_query))
    slots: list[tuple[str, tuple[str, str]]] = []
    tiers_shuffled = list(STAR_BUCKETS)
    for i in range(count):
        e_key = eco_keys[i % len(eco_keys)]
        tier = tiers_shuffled[(i // len(eco_keys)) % len(tiers_shuffled)]
        slots.append((e_key, tier))
    rng.shuffle(slots)

    # Deduplicate (eco_key, tier) queries to respect GitHub Search rate limits
    pools: dict[tuple[str, str], list[dict[str, Any]]] = {}
    unique_queries = sorted({(e_key, tier_label, tier_q) for e_key, (tier_label, tier_q) in slots})

    async with GitHubClient(
        token=token, max_concurrent=2, logger=logger, transport=transport
    ) as client:
        for e_key, tier_label, tier_q in unique_queries:
            lang_q = ECOSYSTEM_SEARCH_LANG[e_key]
            q = f"{lang_q} {tier_q} size:<200000 archived:false"
            page = 1 if transport is not None else rng.randint(1, 3)
            try:
                resp = await client.get(
                    "/search/repositories",
                    params={
                        "q": q,
                        "sort": "stars",
                        "order": "desc",
                        "per_page": 30,
                        "page": page,
                    },
                )
                items = resp.get("items", []) if isinstance(resp, dict) else []
                if not items and page > 1:
                    resp = await client.get(
                        "/search/repositories",
                        params={
                            "q": q,
                            "sort": "stars",
                            "order": "desc",
                            "per_page": 30,
                            "page": 1,
                        },
                    )
                    items = resp.get("items", []) if isinstance(resp, dict) else []
            except Exception as exc:
                if logger:
                    logger.warning("GitHub search failed for %s (%s): %s", e_key, tier_label, exc)
                items = []

            eligible = [
                it
                for it in items
                if isinstance(it, dict)
                and it.get("full_name")
                and not it.get("archived", False)
                and int(it.get("size", 1024)) < 250 * 1024
            ]
            rng.shuffle(eligible)
            pools[(e_key, tier_label)] = eligible

    # Select unique repositories per slot with fallback across tiers of same ecosystem
    seen_names: set[str] = set()
    sampled: list[CorpusEntry] = []

    for e_key, (tier_label, _tier_q) in slots:
        candidate: dict[str, Any] | None = None
        candidate_tiers = [tier_label] + [t[0] for t in STAR_BUCKETS if t[0] != tier_label]
        for t_lbl in candidate_tiers:
            for item in pools.get((e_key, t_lbl), []):
                fn = str(item["full_name"])
                if fn not in seen_names:
                    candidate = item
                    seen_names.add(fn)
                    break
            if candidate is not None:
                break

        if candidate is None:
            continue

        full_name = str(candidate["full_name"])
        org, name = full_name.split("/", 1)
        branch = str(candidate.get("default_branch") or "main")
        clone_url = str(candidate.get("clone_url") or f"https://github.com/{full_name}.git")
        html_url = str(candidate.get("html_url") or f"https://github.com/{full_name}")
        size_kb = max(100, int(candidate.get("size") or 1024))
        size_mb = min(249.0, round(size_kb / 1024.0, 2))
        stars = int(candidate.get("stargazers_count") or 0)
        resolved_sha = candidate.get("pinned_sha") or candidate.get("sha")
        if not resolved_sha and transport is None:
            resolved_sha = await _ls_remote_head_sha(clone_url, branch)

        sampled.append(
            CorpusEntry(
                org=org,
                name=name,
                full_name=full_name,
                url=html_url,
                clone_url=clone_url,
                expected_ecosystem=ECOSYSTEM_KEY_TO_DISPLAY[e_key],
                ecosystem_key=e_key,  # type: ignore[arg-type]
                expected_pipeline=True,
                pinned_ref=branch,
                pinned_sha=resolved_sha,
                estimated_size_mb=max(0.1, size_mb),
                estimated_loc=min(490000, max(1000, size_kb * 10)),
                star_tier=_star_tier_for_count(stars, tier_label),  # type: ignore[arg-type]
                stars=stars,
                is_golden_fixture=False,
                tags=["random-sample", f"seed-{seed}"],
            )
        )

    return sampled


def load_replay_entries(replay_path: Path) -> tuple[list[CorpusEntry], int | None]:
    """
    Load entries from a saved `benchmark_manifest.json`, `anomalies.json`,
    or `benchmark_summary.json` for deterministic replay.
    """
    if not replay_path.exists():
        raise FileNotFoundError(f"Replay file not found: {replay_path}")

    payload = json.loads(replay_path.read_text(encoding="utf-8"))

    # Case 1: BenchmarkManifest format
    if isinstance(payload, dict) and isinstance(payload.get("entries"), list):
        manifest = BenchmarkManifest.model_validate(payload)
        return manifest.entries, manifest.seed

    # Case 2: BenchmarkSummary format -> extract failed/timeout entries or all entries
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        summary = BenchmarkSummary.model_validate(payload)
        targets = [r for r in summary.results if r.status != "passed"] or summary.results
        entries: list[CorpusEntry] = []
        for res in targets:
            eco_display = res.expected_ecosystem or res.detected_ecosystem or "Python"
            eco_key = DISPLAY_TO_ECOSYSTEM_KEY.get(eco_display, "python")
            entries.append(
                CorpusEntry(
                    org=res.org,
                    name=res.repo,
                    full_name=res.full_name,
                    url=f"https://github.com/{res.full_name}",
                    clone_url=res.clone_url or f"https://github.com/{res.full_name}.git",
                    expected_ecosystem=ECOSYSTEM_KEY_TO_DISPLAY[eco_key],
                    ecosystem_key=eco_key,  # type: ignore[arg-type]
                    pinned_sha=None if res.resolved_sha == "unknown" else res.resolved_sha,
                )
            )
        return entries, summary.seed

    # Case 3: anomalies.json format (list or dict with "anomalies")
    raw_anomalies = (
        payload.get("anomalies", [])
        if isinstance(payload, dict)
        else (payload if isinstance(payload, list) else [])
    )
    entries = []
    seen: set[str] = set()
    for item in raw_anomalies:
        if not isinstance(item, dict) or not item.get("repo"):
            continue
        full_name = str(item["repo"])
        if full_name in seen or "/" not in full_name:
            continue
        seen.add(full_name)
        org, name = full_name.split("/", 1)
        eco_display = item.get("expected_ecosystem") or item.get("detected_ecosystem") or "Python"
        eco_key = DISPLAY_TO_ECOSYSTEM_KEY.get(eco_display, "python")
        sha = item.get("sha")
        entries.append(
            CorpusEntry(
                org=org,
                name=name,
                full_name=full_name,
                url=f"https://github.com/{full_name}",
                clone_url=f"https://github.com/{full_name}.git",
                expected_ecosystem=ECOSYSTEM_KEY_TO_DISPLAY[eco_key],
                ecosystem_key=eco_key,  # type: ignore[arg-type]
                pinned_sha=None if not sha or sha == "unknown" else str(sha),
            )
        )
    return entries, None


def _compute_dir_size_kb(repo_dir: Path) -> int:
    total = 0
    for f in repo_dir.rglob("*"):
        if ".git" in f.parts:
            continue
        if f.is_file():
            try:
                total += f.stat().st_size
            except OSError:
                continue
    return max(1, total // 1024)


def _analyze_cloned_repo_sync(
    repo_path: Path,
    entry: CorpusEntry,
    analyzed_date: str,
) -> dict[str, Any]:
    """
    Execute Stage 1 (Discover), Stage 2 (Pipeline DAG), and Stage 3 (Arc42 Code AST)
    synchronously on a local repository checkout.
    """
    sha = _get_git_sha(repo_path)
    if sha == "unknown" and entry.pinned_sha:
        sha = entry.pinned_sha

    # Stage 1: Local tree classification (Discover)
    all_files, manifest_contents = _collect_repo_files_and_contents(repo_path)
    fallback_lang = entry.expected_ecosystem if entry.expected_ecosystem else "Unknown"
    cls_result = classify_repository(all_files, file_contents=manifest_contents)
    detected_eco = (
        cls_result.display_language if cls_result.ecosystem != Ecosystem.UNKNOWN else "Unknown"
    )

    discovery_item = DiscoveryManifestItem(
        Organization=entry.org,
        Project=entry.org,
        ProjectId=entry.org,
        RepositoryName=entry.name,
        RepositoryId=entry.full_name,
        DefaultBranch=entry.pinned_ref,
        CloneUrl=entry.clone_url,
        SshUrl=f"git@github.com:{entry.full_name}.git",
        WebUrl=entry.url,
        Size=_compute_dir_size_kb(repo_path),
        IsDisabled=False,
        IsPrivate=False,
        LastUpdate=_utc_iso(),
        PrimaryLanguage=detected_eco if detected_eco != "Unknown" else fallback_lang,
        FrameworkType=cls_result.framework,
        AllFrameworks="; ".join(cls_result.all_frameworks),
        DeployableTypes="; ".join(cls_result.deployable_types),
        HasAPI=cls_result.signals.get("HasAPI", False),
        HasService=cls_result.signals.get("HasService", False),
        HasFrontend=cls_result.signals.get("HasFrontend", False),
        HasDatabase=cls_result.signals.get("HasDatabase", False),
        TechnologyStack=cls_result.technology_stack,
        HasDockerfile=cls_result.signals.get("HasDockerfile", False),
        HasPipeline=cls_result.signals.get("HasPipeline", False),
        HasKubernetes=cls_result.signals.get("HasKubernetes", False),
        DocumentationPriority=cls_result.documentation_priority,
        AnalyzedDate=analyzed_date,
    )

    anomalies: list[AnomalyRecord] = []

    classification_matched: bool | None = None
    if entry.expected_ecosystem:
        classification_matched = detected_eco == entry.expected_ecosystem
        if not classification_matched:
            anomalies.append(
                AnomalyRecord(
                    repo=entry.full_name,
                    sha=sha,
                    stage="classification",
                    error_type="ClassificationMismatch",
                    message=(
                        f"Expected ecosystem '{entry.expected_ecosystem}', "
                        f"but detected '{detected_eco}' (framework={cls_result.framework})."
                    ),
                    expected_ecosystem=entry.expected_ecosystem,
                    detected_ecosystem=detected_eco,
                    suggested_action=(
                        "Inspect root/subdir manifest anchors in manifests/ecosystems.yaml"
                    ),
                    timestamp=_utc_iso(),
                )
            )

    # Stage 2: Pipeline DAG & anti-patterns
    astro_wfs: list[dict[str, Any]] = []
    topo_nodes: list[TopologyNode] = []
    wf_runs: list[WorkflowRun] = []
    stage_error: str | None = None
    stage_failed: str | None = None
    try:
        wf_entries = discover_local_workflows(repo_path)
        _, astro_wfs, topo_nodes, wf_runs = _analyze_workflows_from_contents(
            entry.full_name, sha, wf_entries
        )
    except Exception as exc:
        stage_error = str(exc)
        stage_failed = "analyze-pipeline"
        anomalies.append(
            AnomalyRecord(
                repo=entry.full_name,
                sha=sha,
                stage="analyze-pipeline",
                error_type=type(exc).__name__,
                message=str(exc),
                traceback=traceback.format_exc(),
                expected_ecosystem=entry.expected_ecosystem,
                detected_ecosystem=detected_eco,
                suggested_action=(
                    "Write failing workflow test in tests/unit/ and patch src/analyzers/pipeline/"
                ),
                timestamp=_utc_iso(),
            )
        )

    # Stage 3: Structural Code Analysis & Arc42 Report
    code_artifact: PortableArtifact | None = None
    try:
        code_artifact = _analyze_repo_code(repo_path, entry.full_name)
    except Exception as exc:
        stage_error = stage_error or str(exc)
        stage_failed = stage_failed or "analyze-code"
        anomalies.append(
            AnomalyRecord(
                repo=entry.full_name,
                sha=sha,
                stage="analyze-code",
                error_type=type(exc).__name__,
                message=str(exc),
                traceback=traceback.format_exc(),
                expected_ecosystem=entry.expected_ecosystem,
                detected_ecosystem=detected_eco,
                suggested_action=(
                    "Write failing AST test in tests/unit/ and patch src/analyzers/code/"
                ),
                timestamp=_utc_iso(),
            )
        )

    return {
        "sha": sha,
        "detected_eco": detected_eco,
        "detected_framework": cls_result.framework,
        "classification_matched": classification_matched,
        "discovery_item": discovery_item,
        "astro_workflows": astro_wfs,
        "topo_nodes": topo_nodes,
        "wf_runs": wf_runs,
        "code_artifact": code_artifact,
        "anomalies": anomalies,
        "stage_failed": stage_failed,
        "stage_error": stage_error,
    }


async def _execute_with_clone(
    entry: CorpusEntry,
    token: str | None,
    timeout: float,
    analyzed_date: str,
    override_path: Path | None,
) -> dict[str, Any]:
    if override_path is not None:
        return await asyncio.to_thread(
            _analyze_cloned_repo_sync, override_path, entry, analyzed_date
        )

    async with GitCloner.clone_async(
        entry.clone_url,
        token=token,
        branch=entry.pinned_ref,
        sha=entry.pinned_sha,
        timeout=timeout,
    ) as cloned_dir:
        return await asyncio.to_thread(
            _analyze_cloned_repo_sync, Path(cloned_dir), entry, analyzed_date
        )


async def _run_single_repo(
    entry: CorpusEntry,
    semaphore: asyncio.Semaphore,
    timeout: float,
    token: str | None,
    analyzed_date: str,
    local_repo_resolver: Callable[[CorpusEntry], Awaitable[Path | None] | Path | None]
    | None = None,
) -> dict[str, Any]:
    async with semaphore:
        t0 = time.perf_counter()
        try:
            override_path: Path | None = None
            if local_repo_resolver is not None:
                maybe = local_repo_resolver(entry)
                override_path = await maybe if asyncio.iscoroutine(maybe) else maybe

            payload = await asyncio.wait_for(
                _execute_with_clone(entry, token, timeout, analyzed_date, override_path),
                timeout=timeout,
            )
            duration = round(time.perf_counter() - t0, 3)
            within_sla = duration <= timeout
            failed = payload["stage_failed"] is not None
            comp_count = (
                len(payload["code_artifact"].architecture_components)
                if payload["code_artifact"] is not None
                else 0
            )
            wf_count = len(payload["astro_workflows"])
            return {
                "result": BenchmarkRepoResult(
                    full_name=entry.full_name,
                    org=entry.org,
                    repo=entry.name,
                    clone_url=entry.clone_url,
                    resolved_sha=payload["sha"],
                    expected_ecosystem=entry.expected_ecosystem,
                    detected_ecosystem=payload["detected_eco"],
                    detected_framework=payload["detected_framework"],
                    classification_matched=payload["classification_matched"],
                    has_pipeline=bool(payload["discovery_item"].HasPipeline or wf_count > 0),
                    workflow_count=wf_count,
                    component_count=comp_count,
                    status="failed" if failed else "passed",
                    duration_seconds=duration,
                    within_sla=within_sla,
                    error=payload["stage_error"],
                    stage_failed=payload["stage_failed"],
                ),
                "anomalies": payload["anomalies"],
                "discovery_item": payload["discovery_item"],
                "astro_workflows": payload["astro_workflows"],
                "topo_nodes": payload["topo_nodes"],
                "wf_runs": payload["wf_runs"],
                "code_artifact": payload["code_artifact"],
            }
        except asyncio.TimeoutError:
            duration = round(time.perf_counter() - t0, 3)
            msg = f"Repository exceeded {timeout:.0f}s SLA circuit breaker."
            anomaly = AnomalyRecord(
                repo=entry.full_name,
                sha=entry.pinned_sha or "unknown",
                stage="timeout",
                error_type="TimeoutError",
                message=msg,
                expected_ecosystem=entry.expected_ecosystem,
                suggested_action=(
                    "Skip non-source asset directories or optimize AST traversal for large files."
                ),
                timestamp=_utc_iso(),
            )
            return {
                "result": BenchmarkRepoResult(
                    full_name=entry.full_name,
                    org=entry.org,
                    repo=entry.name,
                    clone_url=entry.clone_url,
                    resolved_sha=entry.pinned_sha or "unknown",
                    expected_ecosystem=entry.expected_ecosystem,
                    status="timeout",
                    duration_seconds=duration,
                    within_sla=False,
                    error=msg,
                    stage_failed="timeout",
                ),
                "anomalies": [anomaly],
            }
        except Exception as exc:
            duration = round(time.perf_counter() - t0, 3)
            msg = str(exc)
            stage = "clone" if "clone" in msg.lower() else "discover"
            anomaly = AnomalyRecord(
                repo=entry.full_name,
                sha=entry.pinned_sha or "unknown",
                stage=stage,  # type: ignore[arg-type]
                error_type=type(exc).__name__,
                message=msg,
                traceback=traceback.format_exc(),
                expected_ecosystem=entry.expected_ecosystem,
                suggested_action=(
                    "Inspect clone availability, default branch, or file parser edge case."
                ),
                timestamp=_utc_iso(),
            )
            return {
                "result": BenchmarkRepoResult(
                    full_name=entry.full_name,
                    org=entry.org,
                    repo=entry.name,
                    clone_url=entry.clone_url,
                    resolved_sha=entry.pinned_sha or "unknown",
                    expected_ecosystem=entry.expected_ecosystem,
                    status="failed",
                    duration_seconds=duration,
                    within_sla=duration <= timeout,
                    error=msg,
                    stage_failed=stage,
                ),
                "anomalies": [anomaly],
            }


def _render_benchmark_markdown(summary: BenchmarkSummary, anomalies: list[AnomalyRecord]) -> str:
    lines = [
        "# Atruss Code Atlas Benchmark Scorecard",
        "",
        f"- **Run ID**: `{summary.run_id}`",
        f"- **Mode**: `{summary.mode}`"
        + (f" (seed `{summary.seed}`)" if summary.seed is not None else ""),
        f"- **Window**: {summary.started_at} -> {summary.completed_at}",
        f"- **Repositories Evaluated**: {summary.total_repos}",
        (
            f"- **Crash-Free Completion**: {summary.completed_repos}/"
            f"{summary.total_repos} ({summary.crash_free_rate_pct}%)"
        ),
        (
            f"- **Classification Accuracy**: {summary.classification_matched}/"
            f"{summary.classification_evaluated} ({summary.classification_accuracy_pct}%)"
        ),
        (
            f"- **Pipeline Parse Rate**: {summary.pipeline_repos_with_workflows}/"
            f"{summary.total_repos} ({summary.pipeline_parse_success_pct}%)"
        ),
        f"- **Average Runtime / Repo**: {summary.avg_runtime_seconds}s",
        (
            f"- **SLA Compliance (<=180s)**: {summary.sla_compliant_count}/"
            f"{summary.total_repos} ({summary.sla_compliance_pct}%)"
        ),
        f"- **Anomalies Recorded**: {len(anomalies)}",
        "",
        "## Ecosystem Breakdown",
        "",
        "| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for eco, stats in sorted(summary.ecosystem_breakdown.items()):
        lines.append(
            f"| {eco} | {stats['total']} | {stats['passed']} | "
            f"{stats['matched']}/{stats['total']} | {stats['avg_seconds']}s |"
        )

    lines.extend(
        [
            "",
            "## Repository Results",
            "",
            "| Repository | Expected | Detected | Framework "
            "| Workflows | Components | Status | Duration |",
            "| --- | --- | --- | --- | ---: | ---: | --- | ---: |",
        ]
    )
    for r in summary.results:
        lines.append(
            f"| {r.full_name} | {r.expected_ecosystem or '-'} | {r.detected_ecosystem} | "
            f"{r.detected_framework} | {r.workflow_count} | {r.component_count} "
            f"| {r.status} | {r.duration_seconds}s |"
        )
    return "\n".join(lines) + "\n"


def _clear_latest_artifact_dirs(exports_root: Path) -> None:
    """Clear stale module dirs under `exports/latest/` before publishing a fresh batch."""
    latest = exports_root / "latest"
    if not latest.exists():
        return
    for sub in ("repos", "pipelines", "relationships", "reports"):
        target = latest / sub
        if target.exists() and target.is_dir():
            shutil.rmtree(target)


async def execute_benchmark(
    entries: list[CorpusEntry],
    mode: str,
    output_dir: str = "exports",
    log_dir: str = "logs",
    seed: int | None = None,
    corpus_name: str | None = None,
    max_concurrent: int = 4,
    timeout: float = 180.0,
    token: str | None = None,
    clean_latest: bool = True,
    local_repo_resolver: Callable[[CorpusEntry], Awaitable[Path | None] | Path | None]
    | None = None,
) -> tuple[BenchmarkSummary, list[AnomalyRecord], Path]:
    """
    Execute the fault-isolated 3-stage benchmark across `entries` and publish
    Astro-compatible artifacts, `benchmark_manifest.json`, `benchmark_summary.{json,md}`,
    and `anomalies.json`.
    """
    logger = setup_secure_logging(Path(log_dir) / "benchmark.log", token)
    started_at = _utc_iso()
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    analyzed_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    logger.info(
        "Starting %s benchmark for %d repositories (concurrency=%d, timeout=%.1fs)",
        mode,
        len(entries),
        max_concurrent,
        timeout,
    )

    semaphore = asyncio.Semaphore(max_concurrent)
    outcomes = await asyncio.gather(
        *(
            _run_single_repo(
                entry,
                semaphore=semaphore,
                timeout=timeout,
                token=token,
                analyzed_date=analyzed_date,
                local_repo_resolver=local_repo_resolver,
            )
            for entry in entries
        )
    )

    results: list[BenchmarkRepoResult] = []
    anomalies: list[AnomalyRecord] = []
    discovery_items: list[DiscoveryManifestItem] = []
    all_nodes: list[TopologyNode] = []
    all_runs: list[WorkflowRun] = []

    manager = ExportManager(base_dir=output_dir, timestamp=run_ts)
    if clean_latest:
        _clear_latest_artifact_dirs(Path(output_dir))

    topo_archiver = TopologyArchiver(manager)
    reports_dir = manager.base_path / "reports"
    md_exporter = MarkdownExporter(str(reports_dir))

    manifest_entries: list[CorpusEntry] = []
    for entry, outcome in zip(entries, outcomes, strict=True):
        res: BenchmarkRepoResult = outcome["result"]
        results.append(res)
        anomalies.extend(outcome.get("anomalies", []))

        pinned_sha = res.resolved_sha if res.resolved_sha != "unknown" else entry.pinned_sha
        manifest_entries.append(entry.model_copy(update={"pinned_sha": pinned_sha}))

        if "discovery_item" in outcome:
            discovery_items.append(outcome["discovery_item"])

        if "astro_workflows" in outcome:
            topo_archiver.export_repo_pipeline(
                org=entry.org,
                repo=entry.name,
                sha=res.resolved_sha,
                workflows=outcome["astro_workflows"],
            )
        all_nodes.extend(outcome.get("topo_nodes", []))
        all_runs.extend(outcome.get("wf_runs", []))

        art: PortableArtifact | None = outcome.get("code_artifact")
        if art is not None:
            safe_prefix = f"{entry.org}-{entry.name}"
            (reports_dir / f"{safe_prefix}-analysis.json").write_text(
                art.model_dump_json(indent=2), encoding="utf-8"
            )
            md_exporter.export(
                art,
                filename=f"{safe_prefix}-report.md",
                include_frontmatter=True,
            )

    DiscoveryArchiver(manager).export(discovery_items)
    topo_archiver.export(all_nodes, all_runs)
    MarkdownArchiver(manager).export(all_nodes, all_runs)
    latest_dir = manager.publish_to_latest()

    total = len(results)
    completed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    timed_out = sum(1 for r in results if r.status == "timeout")
    eval_cls = [r for r in results if r.classification_matched is not None]
    matched_cls = sum(1 for r in eval_cls if r.classification_matched)
    with_wf = sum(1 for r in results if r.workflow_count > 0)
    sla_ok = sum(1 for r in results if r.within_sla)
    avg_rt = round(sum(r.duration_seconds for r in results) / total, 3) if total else 0.0

    eco_groups: dict[str, list[BenchmarkRepoResult]] = defaultdict(list)
    for r in results:
        key = r.expected_ecosystem or r.detected_ecosystem or "Unknown"
        eco_groups[key].append(r)

    eco_breakdown: dict[str, dict[str, Any]] = {}
    for eco, grp in sorted(eco_groups.items()):
        eco_breakdown[eco] = {
            "total": len(grp),
            "passed": sum(1 for g in grp if g.status == "passed"),
            "matched": sum(1 for g in grp if g.classification_matched),
            "avg_seconds": round(sum(g.duration_seconds for g in grp) / len(grp), 3),
        }

    summary = BenchmarkSummary(
        run_id=run_ts,
        mode=mode,
        seed=seed,
        started_at=started_at,
        completed_at=_utc_iso(),
        total_repos=total,
        completed_repos=completed,
        failed_repos=failed,
        timeout_repos=timed_out,
        crash_free_rate_pct=round((completed / total) * 100, 2) if total else 0.0,
        classification_evaluated=len(eval_cls),
        classification_matched=matched_cls,
        classification_accuracy_pct=round((matched_cls / len(eval_cls)) * 100, 2)
        if eval_cls
        else 0.0,
        pipeline_repos_with_workflows=with_wf,
        pipeline_parse_success_pct=round((with_wf / total) * 100, 2) if total else 0.0,
        avg_runtime_seconds=avg_rt,
        sla_compliant_count=sla_ok,
        sla_compliance_pct=round((sla_ok / total) * 100, 2) if total else 0.0,
        ecosystem_breakdown=eco_breakdown,
        results=results,
    )

    manifest = BenchmarkManifest(
        generated_at=_utc_iso(),
        mode=mode,  # type: ignore[arg-type]
        seed=seed,
        corpus_name=corpus_name,
        total_entries=len(manifest_entries),
        entries=manifest_entries,
    )

    summary_json = summary.model_dump_json(indent=2)
    summary_md = _render_benchmark_markdown(summary, anomalies)
    manifest_json = manifest.model_dump_json(indent=2)
    anomalies_payload = {
        "run_id": run_ts,
        "count": len(anomalies),
        "stage_counts": dict(Counter(a.stage for a in anomalies)),
        "anomalies": [a.model_dump() for a in anomalies],
    }
    anomalies_json = json.dumps(anomalies_payload, indent=2)

    for dest_root in (manager.base_path, latest_dir):
        (dest_root / "benchmark_summary.json").write_text(summary_json, encoding="utf-8")
        (dest_root / "benchmark_summary.md").write_text(summary_md, encoding="utf-8")
        (dest_root / "benchmark_manifest.json").write_text(manifest_json, encoding="utf-8")
        (dest_root / "anomalies.json").write_text(anomalies_json, encoding="utf-8")

    return summary, anomalies, latest_dir


@app.command("benchmark")
def benchmark(
    corpus: str | None = typer.Option(
        None,
        "--corpus",
        help="Corpus identifier ('popular-100') or path to corpus JSON",
    ),
    limit: int | None = typer.Option(
        None,
        "--limit",
        min=1,
        help="Limit number of repositories (uses stratified balance across all 4 ecosystems)",
    ),
    ecosystem: str | None = typer.Option(
        None,
        "--ecosystem",
        help="Filter by ecosystem (python, .net, react_ts_js, java_springboot)",
    ),
    random_sample: int | None = typer.Option(
        None,
        "--random-sample",
        min=1,
        help="Sample N random public GitHub repositories across star tiers via Search API",
    ),
    seed: int = typer.Option(42, "--seed", help="Deterministic seed for random sampling"),
    replay: str | None = typer.Option(
        None,
        "--replay",
        help="Path to benchmark_manifest.json or anomalies.json for deterministic replay",
    ),
    output_dir: str = typer.Option("exports", "--output-dir", help="Exports base directory"),
    log_path: str = typer.Option("logs", "--log-path", help="Directory for benchmark logs"),
    max_concurrent: int = typer.Option(4, "--max-concurrent", min=1, help="Max concurrent workers"),
    timeout: float = typer.Option(180.0, "--timeout", min=1.0, help="Per-repo timeout in seconds"),
    token: str | None = typer.Option(
        None, "--token", envvar="GH_TOKEN", help="GitHub PAT (optional for public repos)"
    ),
    corpus_file: str | None = typer.Option(
        None, "--corpus-file", help="Custom path to popular_100_corpus.json"
    ),
) -> None:
    """
    Run stratified public GitHub benchmarks (`popular-100`, `--random-sample`, or `--replay`),
    capturing classification accuracy, pipeline DAGs, Arc42 reports, and `anomalies.json`.
    """
    if not corpus and random_sample is None and not replay:
        typer.echo(
            "Error: Specify --corpus popular-100, --random-sample <N>, or --replay <manifest.json>",
            err=True,
        )
        raise typer.Exit(1)

    if replay:
        mode = "replay"
        entries, loaded_seed = load_replay_entries(Path(replay))
        effective_seed = loaded_seed if loaded_seed is not None else seed
        if ecosystem:
            eco_key = _normalize_ecosystem_filter(ecosystem)
            entries = [e for e in entries if e.ecosystem_key == eco_key]
        if limit:
            entries = entries[:limit]
        corpus_name = Path(replay).name
    elif random_sample is not None:
        mode = "random-sample"
        effective_seed = seed
        corpus_name = f"random-seed-{seed}"
        entries = asyncio.run(
            sample_random_repositories(
                count=random_sample,
                seed=seed,
                ecosystem=ecosystem,
                token=token,
            )
        )
    else:
        mode = "corpus"
        effective_seed = seed
        corpus_name = str(corpus)
        target_corpus_path = (
            Path(corpus_file)
            if corpus_file
            else (DEFAULT_CORPUS_PATH if corpus == "popular-100" else Path(str(corpus)))
        )
        entries = select_corpus_entries(target_corpus_path, ecosystem=ecosystem, limit=limit)

    if not entries:
        typer.echo("Error: Zero repositories matched the benchmark selection criteria.", err=True)
        raise typer.Exit(1)

    summary, anomalies, latest_dir = asyncio.run(
        execute_benchmark(
            entries=entries,
            mode=mode,
            output_dir=output_dir,
            log_dir=log_path,
            seed=effective_seed,
            corpus_name=corpus_name,
            max_concurrent=max_concurrent,
            timeout=timeout,
            token=token,
        )
    )

    typer.echo(
        f"Benchmark ({mode}) finished: {summary.completed_repos}/{summary.total_repos} crash-free "
        f"({summary.crash_free_rate_pct}%), classification={summary.classification_accuracy_pct}%, "
        f"anomalies={len(anomalies)}, exports={latest_dir}"
    )
