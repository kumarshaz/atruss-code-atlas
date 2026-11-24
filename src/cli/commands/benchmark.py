from __future__ import annotations

import asyncio
import csv
import json
import os
import random
import shutil
import sys
import tempfile
import time
import traceback
from collections import Counter, defaultdict
from collections.abc import Awaitable, Callable
from contextlib import redirect_stdout
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import typer

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.orchestrator import _collect_repo_files_and_contents
from src.analyzers.drift import compute_drift_report, render_drift_markdown
from src.analyzers.pipeline.parser import discover_local_workflows
from src.cli.commands.analyze_code import _analyze_repo_code, _get_git_sha
from src.cli.commands.analyze_pipeline import _analyze_workflows_from_contents
from src.core.auth import setup_secure_logging
from src.core.exporters.discovery_exporter import DiscoveryArchiver
from src.core.exporters.llms_exporter import export_llms_context
from src.core.exporters.markdown_exporter import MarkdownArchiver
from src.core.exporters.org_summary_exporter import export_org_summary
from src.core.exporters.pipeline_exporter import TopologyArchiver
from src.core.exporters.sarif_exporter import export_sarif_report
from src.core.exporters.sbom_exporter import export_cyclonedx_sbom
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
        "go": "go",
        "golang": "go",
        "rust": "rust",
        "rs": "rust",
        "ruby": "ruby",
        "rb": "ruby",
        "rails": "ruby",
        "php": "php",
        "elixir": "elixir",
        "ex": "elixir",
        "infra": "infra_devops",
        "infra_devops": "infra_devops",
        "devops": "infra_devops",
        "helm": "infra_devops",
        "docker": "infra_devops",
    }
    if cleaned in aliases:
        return aliases[cleaned]
    if raw in DISPLAY_TO_ECOSYSTEM_KEY:
        return DISPLAY_TO_ECOSYSTEM_KEY[raw]
    raise typer.BadParameter(
        f"Unsupported ecosystem filter '{raw}'. Choose from: "
        "python, .net, react_ts_js, java_springboot, go, rust, ruby, php, elixir, infra_devops"
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

    # Stratified round-robin slice across ecosystems
    buckets: dict[str, list[CorpusEntry]] = defaultdict(list)
    for entry in entries:
        buckets[entry.ecosystem_key].append(entry)

    selected: list[CorpusEntry] = []
    eco_order = [
        "python",
        ".net",
        "react_ts_js",
        "java_springboot",
        "go",
        "rust",
        "ruby",
        "php",
        "elixir",
        "infra_devops",
    ]
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
    *,
    enable_live_osv: bool = False,
    osv_transport: httpx.BaseTransport | None = None,
    osv_cache_path: Path | None = None,
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
        code_artifact = _analyze_repo_code(
            repo_path,
            entry.full_name,
            enable_live_osv=enable_live_osv,
            osv_transport=osv_transport,
            osv_cache_path=osv_cache_path,
        )
        if code_artifact is not None and code_artifact.sha == "unknown" and sha != "unknown":
            code_artifact = code_artifact.model_copy(update={"sha": sha})
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
    *,
    enable_live_osv: bool = False,
    osv_transport: httpx.BaseTransport | None = None,
    osv_cache_path: Path | None = None,
) -> dict[str, Any]:
    if override_path is not None:
        return await asyncio.to_thread(
            _analyze_cloned_repo_sync,
            override_path,
            entry,
            analyzed_date,
            enable_live_osv=enable_live_osv,
            osv_transport=osv_transport,
            osv_cache_path=osv_cache_path,
        )

    async with GitCloner.clone_async(
        entry.clone_url,
        token=token,
        branch=entry.pinned_ref,
        sha=entry.pinned_sha,
        timeout=timeout,
    ) as cloned_dir:
        return await asyncio.to_thread(
            _analyze_cloned_repo_sync,
            Path(cloned_dir),
            entry,
            analyzed_date,
            enable_live_osv=enable_live_osv,
            osv_transport=osv_transport,
            osv_cache_path=osv_cache_path,
        )


async def _run_single_repo(
    entry: CorpusEntry,
    semaphore: asyncio.Semaphore,
    timeout: float,
    token: str | None,
    analyzed_date: str,
    local_repo_resolver: Callable[[CorpusEntry], Awaitable[Path | None] | Path | None]
    | None = None,
    *,
    enable_live_osv: bool = False,
    osv_transport: httpx.BaseTransport | None = None,
    osv_cache_path: Path | None = None,
) -> dict[str, Any]:
    async with semaphore:
        t0 = time.perf_counter()
        try:
            override_path: Path | None = None
            if local_repo_resolver is not None:
                maybe = local_repo_resolver(entry)
                override_path = await maybe if asyncio.iscoroutine(maybe) else maybe

            payload = await asyncio.wait_for(
                _execute_with_clone(
                    entry,
                    token,
                    timeout,
                    analyzed_date,
                    override_path,
                    enable_live_osv=enable_live_osv,
                    osv_transport=osv_transport,
                    osv_cache_path=osv_cache_path,
                ),
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
    for sub in ("repos", "pipelines", "relationships", "reports", "sbom", "sarif", "drift", "llms"):
        target = latest / sub
        if target.exists() and target.is_dir():
            shutil.rmtree(target)


def _serialize_outcome(outcome: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "result": outcome["result"].model_dump(),
        "anomalies": [a.model_dump() for a in outcome.get("anomalies", [])],
    }
    if "discovery_item" in outcome:
        payload["discovery_item"] = asdict(outcome["discovery_item"])
    if "astro_workflows" in outcome:
        payload["astro_workflows"] = outcome["astro_workflows"]
    if "topo_nodes" in outcome:
        payload["topo_nodes"] = [asdict(n) for n in outcome["topo_nodes"]]
    if "wf_runs" in outcome:
        payload["wf_runs"] = [asdict(w) for w in outcome["wf_runs"]]
    if outcome.get("code_artifact") is not None:
        payload["code_artifact"] = outcome["code_artifact"].model_dump()
    return payload


def _deserialize_outcome(raw: dict[str, Any]) -> dict[str, Any]:
    outcome: dict[str, Any] = {
        "result": BenchmarkRepoResult.model_validate(raw["result"]),
        "anomalies": [AnomalyRecord.model_validate(a) for a in raw.get("anomalies", [])],
    }
    if "discovery_item" in raw:
        outcome["discovery_item"] = DiscoveryManifestItem(**raw["discovery_item"])
    if "astro_workflows" in raw:
        outcome["astro_workflows"] = raw["astro_workflows"]
    if "topo_nodes" in raw:
        outcome["topo_nodes"] = [TopologyNode(**n) for n in raw["topo_nodes"]]
    if "wf_runs" in raw:
        outcome["wf_runs"] = [WorkflowRun(**w) for w in raw["wf_runs"]]
    if raw.get("code_artifact") is not None:
        outcome["code_artifact"] = PortableArtifact.model_validate(raw["code_artifact"])
    return outcome


def _parse_worker_stdout(raw_stdout: bytes) -> dict[str, Any]:
    text = raw_stdout.decode("utf-8").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        for line in reversed(text.splitlines()):
            candidate = line.strip()
            if candidate.startswith("{"):
                return json.loads(candidate)
        raise


def _run_worker_from_stdin() -> None:
    req = json.loads(sys.stdin.read())
    entry = CorpusEntry.model_validate(req["entry"])
    timeout = float(req["timeout"])
    analyzed_date = str(req["analyzed_date"])
    token = os.getenv("GH_TOKEN") or req.get("token")
    enable_live_osv = bool(req.get("enable_live_osv", False))
    raw_cache = req.get("osv_cache_path")
    osv_cache_path = Path(raw_cache) if raw_cache else None
    sem = asyncio.Semaphore(1)
    # Keep typer.echo/library logs on stderr so child stdout emits clean JSON only.
    with redirect_stdout(sys.stderr):
        outcome = asyncio.run(
            _run_single_repo(
                entry,
                semaphore=sem,
                timeout=timeout,
                token=token,
                analyzed_date=analyzed_date,
                enable_live_osv=enable_live_osv,
                osv_cache_path=osv_cache_path,
            )
        )
    sys.stdout.write(json.dumps(_serialize_outcome(outcome)))
    sys.stdout.flush()


async def _run_single_repo_subprocess(
    entry: CorpusEntry,
    *,
    semaphore: asyncio.Semaphore,
    timeout: float,
    token: str | None,
    analyzed_date: str,
    enable_live_osv: bool = False,
    osv_cache_path: Path | None = None,
) -> dict[str, Any]:
    req_bytes = json.dumps(
        {
            "entry": entry.model_dump(),
            "timeout": timeout,
            "analyzed_date": analyzed_date,
            "token": token,
            "enable_live_osv": enable_live_osv,
            "osv_cache_path": str(osv_cache_path) if osv_cache_path else None,
        }
    ).encode("utf-8")

    async with semaphore:
        t0 = time.perf_counter()
        worker_cmd = (
            "from src.cli.commands.benchmark import _run_worker_from_stdin; "
            "_run_worker_from_stdin()"
        )
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-c",
            worker_cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=req_bytes),
                timeout=timeout + 10.0,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            duration = round(time.perf_counter() - t0, 3)
            tmp_atlas = Path(os.environ.get("TMPDIR", "/tmp")) / "atruss_code_atlas"
            if tmp_atlas.exists():
                for d in tmp_atlas.iterdir():
                    if d.is_dir() and (time.time() - d.stat().st_mtime) > timeout:
                        shutil.rmtree(d, ignore_errors=True)
            res = BenchmarkRepoResult(
                full_name=entry.full_name,
                org=entry.org,
                repo=entry.name,
                clone_url=entry.clone_url,
                resolved_sha=entry.pinned_sha or "unknown",
                expected_ecosystem=entry.expected_ecosystem,
                status="timeout",
                duration_seconds=duration,
                within_sla=False,
                error=f"Hard subprocess timeout after {timeout:.1f}s",
                stage_failed="timeout",
            )
            anom = AnomalyRecord(
                repo=entry.full_name,
                sha=entry.pinned_sha or "unknown",
                stage="timeout",
                error_type="TimeoutError",
                message=f"Subprocess exceeded {timeout:.1f}s SLA",
                expected_ecosystem=entry.expected_ecosystem,
                suggested_action="Increase --timeout or optimize large monorepo scan",
                timestamp=_utc_iso(),
            )
            return {"result": res, "anomalies": [anom]}

        if proc.returncode == 0 and stdout:
            try:
                return _deserialize_outcome(_parse_worker_stdout(stdout))
            except Exception as exc:
                err_msg = f"Worker payload decode failed: {exc}"
        else:
            err_msg = stderr.decode("utf-8", errors="replace").strip()[-400:] or (
                f"Worker exited with code {proc.returncode}"
            )

        duration = round(time.perf_counter() - t0, 3)
        res = BenchmarkRepoResult(
            full_name=entry.full_name,
            org=entry.org,
            repo=entry.name,
            clone_url=entry.clone_url,
            resolved_sha=entry.pinned_sha or "unknown",
            expected_ecosystem=entry.expected_ecosystem,
            status="failed",
            duration_seconds=duration,
            within_sla=duration <= timeout,
            error=err_msg,
            stage_failed="worker",
        )
        anom = AnomalyRecord(
            repo=entry.full_name,
            sha=entry.pinned_sha or "unknown",
            stage="worker",
            error_type="WorkerProcessError",
            message=err_msg,
            expected_ecosystem=entry.expected_ecosystem,
            suggested_action="Inspect benchmark logs or re-run with --isolated",
            timestamp=_utc_iso(),
        )
        return {"result": res, "anomalies": [anom]}


def _merge_discovery_items(
    existing_latest: Path,
    fresh_items: list[DiscoveryManifestItem],
) -> list[DiscoveryManifestItem]:
    """Upsert fresh discovery items into existing `exports/latest/repos/repositories.json`."""
    repos_json = existing_latest / "repos" / "repositories.json"
    if not repos_json.exists():
        return fresh_items

    try:
        raw_payload = json.loads(repos_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fresh_items

    raw_items = (
        raw_payload.get("items", raw_payload) if isinstance(raw_payload, dict) else raw_payload
    )
    if not isinstance(raw_items, list):
        return fresh_items

    valid_fields = set(DiscoveryManifestItem.__dataclass_fields__.keys())
    fresh_by_key: dict[str, DiscoveryManifestItem] = {}
    for item in fresh_items:
        key = (item.RepositoryId or f"{item.Organization}/{item.RepositoryName}").strip().lower()
        fresh_by_key[key] = item

    merged: list[DiscoveryManifestItem] = []
    seen_keys: set[str] = set()
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        org = str(raw.get("Organization", "")).strip()
        name = str(raw.get("RepositoryName", "")).strip()
        rid = str(raw.get("RepositoryId", "")).strip()
        key = (rid if "/" in rid else (f"{org}/{name}" if org and name else rid or name)).lower()
        if not key or key in seen_keys:
            continue
        seen_keys.add(key)
        if key in fresh_by_key:
            merged.append(fresh_by_key[key])
        else:
            filtered = {k: v for k, v in raw.items() if k in valid_fields}
            try:
                merged.append(DiscoveryManifestItem(**filtered))
            except TypeError:
                continue

    remaining = [
        item
        for key, item in fresh_by_key.items()
        if key not in seen_keys
    ]
    remaining.sort(key=lambda d: (d.Organization.lower(), d.RepositoryName.lower()))
    merged.extend(remaining)
    return merged


def _merge_pipeline_topology(
    existing_latest: Path,
    refreshed_repo_names: set[str],
    fresh_nodes: list[TopologyNode],
    fresh_runs: list[WorkflowRun],
) -> tuple[list[TopologyNode], list[WorkflowRun]]:
    """Preserve untouched repositories in `pipeline_topology.*` during `--merge-latest`."""
    refreshed_low = {name.strip().lower() for name in refreshed_repo_names if name.strip()}
    preserved_nodes: list[TopologyNode] = []
    preserved_runs: list[WorkflowRun] = []

    topo_json = existing_latest / "relationships" / "pipeline_topology.json"
    if topo_json.exists():
        try:
            payload = json.loads(topo_json.read_text(encoding="utf-8"))
            items = payload.get("items", payload) if isinstance(payload, dict) else payload
            if isinstance(items, list):
                valid_fields = set(TopologyNode.__dataclass_fields__.keys())
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    rname = str(item.get("repoName", "")).strip().lower()
                    rid = str(item.get("repoId", "")).strip().lower()
                    if rname in refreshed_low or rid in refreshed_low:
                        continue
                    filtered = {k: v for k, v in item.items() if k in valid_fields}
                    try:
                        preserved_nodes.append(TopologyNode(**filtered))
                    except TypeError:
                        continue
        except (OSError, json.JSONDecodeError):
            pass

    topo_csv = existing_latest / "relationships" / "pipeline_topology.csv"
    if topo_csv.exists():
        try:
            with open(topo_csv, encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    rname = str(row.get("RepoName", "")).strip()
                    if not rname or rname.lower() in refreshed_low:
                        continue
                    preserved_runs.append(
                        WorkflowRun(
                            repo_name=rname,
                            workflow_name=str(row.get("WorkflowName", "")),
                            target_env=str(row.get("DeploymentTarget", "")),
                            resource=str(row.get("DeploymentResource", "")),
                        )
                    )
        except OSError:
            pass

    return preserved_nodes + fresh_nodes, preserved_runs + fresh_runs


def _existing_pipeline_analyzed_at(
    existing_latest: Path,
    org: str,
    repo: str,
    sha: str,
    workflows: list[dict[str, Any]],
) -> str | None:
    """Reuse existing `analyzed_at` when `--merge-latest` sees identical pipeline SHA & DAG."""
    safe_org = org.replace("/", "_") if org else "local"
    safe_repo = repo.split("/")[-1].replace("/", "_")
    pfile = existing_latest / "pipelines" / f"{safe_org}-{safe_repo}-pipeline.json"
    if not pfile.exists():
        return None
    try:
        existing = json.loads(pfile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        isinstance(existing, dict)
        and existing.get("sha") == sha
        and existing.get("workflows") == workflows
        and isinstance(existing.get("analyzed_at"), str)
    ):
        return existing["analyzed_at"]
    return None


def _build_portfolio_history_snapshot(latest_dir: Path) -> dict[str, Any] | None:
    """Build portfolio scorecard snapshot from all merged `reports/*-analysis.json` files."""
    reports_dir = latest_dir / "reports"
    if not reports_dir.is_dir():
        return None
    repos_sc_summary: dict[str, dict[str, Any]] = {}
    scorecard_total = 0.0
    total_vulns = 0
    total_fitness = 0
    total_secrets = 0
    for rfile in sorted(reports_dir.glob("*-analysis.json")):
        try:
            data = json.loads(rfile.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        sc = data.get("scorecard")
        if not isinstance(sc, dict) or sc.get("overall_score") is None:
            continue
        repo_key = str(data.get("repository") or rfile.stem.removesuffix("-analysis"))
        overall_score = float(sc.get("overall_score", 0.0) or 0.0)
        scorecard_total += overall_score
        vulns = data.get("vulnerabilities") or []
        fitness = data.get("fitness_violations") or []
        secrets = data.get("secrets") or []
        total_vulns += len(vulns)
        total_fitness += len(fitness)
        total_secrets += len(secrets)
        repos_sc_summary[repo_key] = {
            "overall_score": overall_score,
            "overall_grade": sc.get("overall_grade", "N/A"),
            "technical_debt_score": float(sc.get("technical_debt_score", 0.0) or 0.0),
            "vulnerabilities_count": len(vulns),
            "fitness_violations_count": len(fitness),
            "secrets_count": len(secrets),
        }
    if not repos_sc_summary:
        return None
    return {
        "command": "benchmark",
        "repo_count": len(repos_sc_summary),
        "average_overall_score": round(scorecard_total / len(repos_sc_summary), 2),
        "total_vulnerabilities": total_vulns,
        "total_fitness_violations": total_fitness,
        "total_secrets": total_secrets,
        "repos": repos_sc_summary,
    }


def _capture_drift_baseline(
    output_dir: Path,
    clean_latest: bool,
    diff_baseline: Path | str | None,
    diff_previous: bool,
) -> tuple[Path | None, tempfile.TemporaryDirectory[str] | None, str | None]:
    """Snapshot an existing `latest/` baseline before cleanup if drift computation is enabled."""
    latest_existing = output_dir / "latest"
    snapshot_subdirs = ("repos", "pipelines", "relationships", "reports", "sbom", "sarif", "llms")
    if diff_baseline is not None:
        cand_base = Path(diff_baseline)
        if cand_base.exists():
            if clean_latest and latest_existing.exists() and cand_base.resolve() in (
                latest_existing.resolve(),
                output_dir.resolve(),
            ):
                temp_ctx = tempfile.TemporaryDirectory(prefix="atruss_bench_base_")
                snap_root = Path(temp_ctx.name)
                for sub in snapshot_subdirs:
                    src_sub = latest_existing / sub
                    if src_sub.exists():
                        shutil.copytree(src_sub, snap_root / sub, dirs_exist_ok=True)
                return snap_root, temp_ctx, str(diff_baseline)
            return cand_base, None, str(diff_baseline)

    if diff_previous and latest_existing.exists() and any(
        (latest_existing / sub).exists() for sub in ("repos", "reports", "pipelines")
    ):
        temp_ctx = tempfile.TemporaryDirectory(prefix="atruss_bench_prev_")
        snap_root = Path(temp_ctx.name)
        for sub in snapshot_subdirs:
            src_sub = latest_existing / sub
            if src_sub.exists():
                shutil.copytree(src_sub, snap_root / sub, dirs_exist_ok=True)
        return snap_root, temp_ctx, f"{output_dir.as_posix().rstrip('/')}/latest (previous)"

    return None, None, None


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
    checkpoint_dir: Path | str | None = None,
    resume: bool = True,
    isolated: bool = False,
    enable_live_osv: bool = False,
    osv_transport: httpx.BaseTransport | None = None,
    osv_cache_path: Path | None = None,
    diff_baseline: Path | str | None = None,
    diff_previous: bool = False,
) -> tuple[BenchmarkSummary, list[AnomalyRecord], Path]:
    """
    Execute the fault-isolated 3-stage benchmark across `entries` and publish
    Astro-compatible artifacts, `orgs-summary.json`, optional `drift_report.{json,md}`,
    `benchmark_manifest.json`, `benchmark_summary.{json,md}`, and `anomalies.json`.
    Supports optional per-repo checkpointing (`checkpoint_dir`, `resume`), memory-isolated
    subprocess execution (`isolated`), live OSV queries (`enable_live_osv`), and drift comparison.
    """
    logger = setup_secure_logging(Path(log_dir) / "benchmark.log", token)
    started_at = _utc_iso()
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    analyzed_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    ckpt_root = Path(checkpoint_dir) if checkpoint_dir is not None else None
    if ckpt_root is not None:
        ckpt_root.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Starting %s benchmark for %d repositories "
        "(concurrency=%d, timeout=%.1fs, isolated=%s, live_osv=%s)",
        mode,
        len(entries),
        max_concurrent,
        timeout,
        isolated and local_repo_resolver is None,
        enable_live_osv,
    )

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _run_or_load(idx: int, entry: CorpusEntry) -> dict[str, Any]:
        ckpt_file: Path | None = None
        if ckpt_root is not None:
            slug = f"{entry.org}__{entry.name}".replace("/", "_")
            ckpt_file = ckpt_root / f"{idx:04d}_{slug}.json"
            if resume and ckpt_file.exists():
                return _deserialize_outcome(json.loads(ckpt_file.read_text(encoding="utf-8")))

        if isolated and local_repo_resolver is None:
            outcome = await _run_single_repo_subprocess(
                entry,
                semaphore=semaphore,
                timeout=timeout,
                token=token,
                analyzed_date=analyzed_date,
                enable_live_osv=enable_live_osv,
                osv_cache_path=osv_cache_path,
            )
        else:
            outcome = await _run_single_repo(
                entry,
                semaphore=semaphore,
                timeout=timeout,
                token=token,
                analyzed_date=analyzed_date,
                local_repo_resolver=local_repo_resolver,
                enable_live_osv=enable_live_osv,
                osv_transport=osv_transport,
                osv_cache_path=osv_cache_path,
            )

        if ckpt_file is not None:
            ckpt_file.write_text(json.dumps(_serialize_outcome(outcome)), encoding="utf-8")
        return outcome

    temp_baseline_ctx: tempfile.TemporaryDirectory[str] | None = None
    try:
        resolved_diff_baseline, temp_baseline_ctx, baseline_label = _capture_drift_baseline(
            Path(output_dir),
            clean_latest=clean_latest,
            diff_baseline=diff_baseline,
            diff_previous=diff_previous,
        )

        outcomes = await asyncio.gather(
            *(_run_or_load(idx, entry) for idx, entry in enumerate(entries))
        )

        results: list[BenchmarkRepoResult] = []
        anomalies: list[AnomalyRecord] = []
        discovery_items: list[DiscoveryManifestItem] = []
        all_nodes: list[TopologyNode] = []
        all_runs: list[WorkflowRun] = []
        refreshed_pipe_names: set[str] = set()
        existing_latest = Path(output_dir) / "latest"

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
                existing_ts = (
                    _existing_pipeline_analyzed_at(
                        existing_latest,
                        entry.org,
                        entry.name,
                        res.resolved_sha,
                        outcome["astro_workflows"],
                    )
                    if not clean_latest
                    else None
                )
                topo_archiver.export_repo_pipeline(
                    org=entry.org,
                    repo=entry.name,
                    sha=res.resolved_sha,
                    workflows=outcome["astro_workflows"],
                    analyzed_at=existing_ts,
                )
                if res.stage_failed != "analyze-pipeline":
                    refreshed_pipe_names.add(entry.name)
                    refreshed_pipe_names.add(entry.full_name)
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
                export_cyclonedx_sbom(
                    art.repository,
                    art.sha,
                    art.dependencies,
                    art.vulnerabilities,
                    output_path=manager.get_path("sbom", f"{safe_prefix}.cdx.json"),
                )
                export_sarif_report(
                    art,
                    output_path=manager.get_path("sarif", f"{safe_prefix}.sarif.json"),
                    repo_name=art.repository,
                )

        if not clean_latest:
            discovery_items = _merge_discovery_items(existing_latest, discovery_items)
            all_nodes, all_runs = _merge_pipeline_topology(
                existing_latest,
                refreshed_pipe_names,
                all_nodes,
                all_runs,
            )

        DiscoveryArchiver(manager).export(discovery_items)
        topo_archiver.export(all_nodes, all_runs)
        MarkdownArchiver(manager).export(all_nodes, all_runs)
        latest_dir = manager.publish_to_latest()
        export_llms_context(latest_dir, output_dir=manager.base_path / "llms")
        manager.publish_to_latest(modules=["llms"])

        if resolved_diff_baseline is not None:
            target_label = f"{Path(output_dir).as_posix().rstrip('/')}/latest"
            drift_report = compute_drift_report(
                resolved_diff_baseline,
                latest_dir,
                baseline_label=baseline_label,
                target_label=target_label,
            )
            drift_json = json.dumps(drift_report, indent=2) + "\n"
            drift_md = render_drift_markdown(drift_report)
            manager.get_path("drift", "drift_report.json").write_text(
                drift_json, encoding="utf-8"
            )
            manager.get_path("drift", "drift_report.md").write_text(drift_md, encoding="utf-8")
            manager.publish_to_latest(modules=["drift"])

        orgs_summary_latest, _ = export_org_summary(
            latest_dir, output_path=latest_dir / "orgs-summary.json"
        )
        shutil.copy2(orgs_summary_latest, manager.base_path / "orgs-summary.json")
    finally:
        if temp_baseline_ctx is not None:
            temp_baseline_ctx.cleanup()

    history_payload = (
        _build_portfolio_history_snapshot(latest_dir) if not clean_latest else None
    )
    if history_payload is None:
        scored_arts = [
            o["code_artifact"]
            for o in outcomes
            if o.get("code_artifact") is not None and o["code_artifact"].scorecard is not None
        ]
        avg_sc = (
            round(
                sum(a.scorecard.overall_score for a in scored_arts if a.scorecard)
                / len(scored_arts),
                2,
            )
            if scored_arts
            else 0.0
        )
        repos_sc_summary = {
            a.repository: {
                "overall_score": a.scorecard.overall_score if a.scorecard else 0.0,
                "overall_grade": a.scorecard.overall_grade if a.scorecard else "N/A",
                "technical_debt_score": a.scorecard.technical_debt_score if a.scorecard else 0.0,
                "vulnerabilities_count": len(a.vulnerabilities),
                "fitness_violations_count": len(a.fitness_violations),
                "secrets_count": len(a.secrets),
            }
            for a in scored_arts
        }
        history_payload = {
            "command": "benchmark",
            "repo_count": len(results),
            "average_overall_score": avg_sc,
            "total_vulnerabilities": sum(len(a.vulnerabilities) for a in scored_arts),
            "total_fitness_violations": sum(len(a.fitness_violations) for a in scored_arts),
            "total_secrets": sum(len(a.secrets) for a in scored_arts),
            "repos": repos_sc_summary,
        }
    manager.append_catalog_history(history_payload)

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
        help="Limit number of repositories (uses stratified balance across all 10 ecosystems)",
    ),
    ecosystem: str | None = typer.Option(
        None,
        "--ecosystem",
        help=(
            "Filter by ecosystem (python, .net, react_ts_js, java_springboot, "
            "go, rust, ruby, php, elixir, infra_devops)"
        ),
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
    checkpoint_dir: str | None = typer.Option(
        None,
        "--checkpoint-dir",
        help="Directory to store per-repo checkpoints for automated resume",
    ),
    resume: bool = typer.Option(
        True,
        "--resume/--no-resume",
        help="Skip repositories that already have checkpoints in --checkpoint-dir",
    ),
    isolated: bool = typer.Option(
        False,
        "--isolated/--no-isolated",
        help="Run each repository in a memory-isolated subprocess with hard timeout enforcement",
    ),
    live_osv: bool = typer.Option(
        False,
        "--live-osv/--no-live-osv",
        help="Enable live OSV.dev batch vulnerability queries during code analysis",
    ),
    osv_cache_path: str | None = typer.Option(
        None,
        "--osv-cache-path",
        help="Optional shared JSON cache file for OSV.dev lookups across isolated workers",
    ),
    clean_latest: bool = typer.Option(
        True,
        "--clean-latest/--merge-latest",
        help="Replace exports/latest/ or merge/upsert this batch into existing exports/latest/",
    ),
    diff_baseline: str | None = typer.Option(
        None,
        "--diff-baseline",
        help="Optional baseline archival snapshot directory for drift_report.{json,md}",
    ),
    diff_previous: bool = typer.Option(
        False,
        "--diff-previous/--no-diff-previous",
        help="Compare against existing exports/latest snapshot before replacement and emit drift",
    ),
) -> None:
    """
    Run stratified public GitHub benchmarks (`popular-100`, `--random-sample`, or `--replay`),
    capturing classification accuracy, pipeline DAGs, Arc42 reports, and `anomalies.json`.
    """
    if not corpus and not corpus_file and random_sample is None and not replay:
        typer.echo(
            "Error: Specify --corpus popular-100, --corpus-file <path>, "
            "--random-sample <N>, or --replay <manifest.json>",
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
        target_corpus_path = (
            Path(corpus_file)
            if corpus_file
            else (DEFAULT_CORPUS_PATH if corpus == "popular-100" else Path(str(corpus)))
        )
        corpus_name = Path(corpus_file).name if corpus_file else str(corpus)
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
            checkpoint_dir=checkpoint_dir,
            resume=resume,
            isolated=isolated,
            enable_live_osv=live_osv,
            osv_cache_path=Path(osv_cache_path) if osv_cache_path else None,
            clean_latest=clean_latest,
            diff_baseline=diff_baseline,
            diff_previous=diff_previous,
        )
    )

    typer.echo(
        f"Benchmark ({mode}) finished: {summary.completed_repos}/{summary.total_repos} crash-free "
        f"({summary.crash_free_rate_pct}%), classification={summary.classification_accuracy_pct}%, "
        f"anomalies={len(anomalies)}, exports={latest_dir}"
    )
