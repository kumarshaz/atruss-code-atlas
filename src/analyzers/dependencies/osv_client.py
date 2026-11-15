from __future__ import annotations

import json
import logging
import math
import os
import re
from pathlib import Path
from typing import Any

import httpx

from src.analyzers.dependencies.manifest_parser import SKIP_DIRS
from src.models.artifacts import DependencyRecord, VulnerabilityRecord

logger = logging.getLogger(__name__)

OSV_API_BASE = "https://api.osv.dev"
OSV_QUERYBATCH_PATH = "/v1/querybatch"
OSV_QUERYBATCH_URL = f"{OSV_API_BASE}{OSV_QUERYBATCH_PATH}"
MAX_OSV_BATCH_SIZE = 500

_VALID_SEVERITIES = frozenset({"CRITICAL", "HIGH", "MEDIUM", "LOW"})

_PYPI_IMPORT_ALIASES: dict[str, tuple[str, ...]] = {
    "pyyaml": ("yaml",),
    "pillow": ("pil",),
    "scikit-learn": ("sklearn",),
    "beautifulsoup4": ("bs4",),
    "python-dotenv": ("dotenv",),
    "pyjwt": ("jwt",),
    "psycopg2-binary": ("psycopg2",),
    "python-dateutil": ("dateutil",),
    "attrs": ("attr", "attrs"),
    "pycryptodome": ("Crypto",),
}

_SOURCE_EXTENSIONS: dict[str, frozenset[str]] = {
    "pypi": frozenset({".py", ".pyi"}),
    "npm": frozenset({".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}),
    "nuget": frozenset({".cs", ".fs", ".vb"}),
    "maven": frozenset({".java", ".kt", ".kts"}),
}

_CVSS3_METRICS: dict[str, dict[str, Any]] = {
    "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20},
    "AC": {"L": 0.77, "H": 0.44},
    "PR_U": {"N": 0.85, "L": 0.62, "H": 0.27},
    "PR_C": {"N": 0.85, "L": 0.68, "H": 0.50},
    "UI": {"N": 0.85, "R": 0.62},
    "CIA": {"N": 0.00, "L": 0.22, "H": 0.56},
}


def _cvss_roundup(value: float) -> float:
    int_input = round(value * 100000)
    if int_input % 10000 == 0:
        return int_input / 100000.0
    return (math.floor(int_input / 10000) + 1) / 10.0


def _parse_cvss_score(raw_score: Any) -> float | None:
    """Parse numeric CVSS score or compute CVSS v3.0/v3.1 base score from vector."""
    if isinstance(raw_score, int | float):
        return round(float(raw_score), 1)
    if not isinstance(raw_score, str):
        return None
    text = raw_score.strip()
    if not text:
        return None
    try:
        return round(float(text), 1)
    except ValueError:
        pass

    if not text.startswith("CVSS:3."):
        return None

    parts = text.split("/")[1:]
    metrics: dict[str, str] = {}
    for part in parts:
        if ":" in part:
            k, v = part.split(":", 1)
            metrics[k] = v

    scope = metrics.get("S")
    av = _CVSS3_METRICS["AV"].get(metrics.get("AV", ""))
    ac = _CVSS3_METRICS["AC"].get(metrics.get("AC", ""))
    pr_table = _CVSS3_METRICS["PR_C"] if scope == "C" else _CVSS3_METRICS["PR_U"]
    pr = pr_table.get(metrics.get("PR", ""))
    ui = _CVSS3_METRICS["UI"].get(metrics.get("UI", ""))
    c = _CVSS3_METRICS["CIA"].get(metrics.get("C", ""))
    i = _CVSS3_METRICS["CIA"].get(metrics.get("I", ""))
    a = _CVSS3_METRICS["CIA"].get(metrics.get("A", ""))

    if None in (av, ac, pr, ui, c, i, a) or scope not in {"U", "C"}:
        return None

    iss = 1.0 - ((1.0 - c) * (1.0 - i) * (1.0 - a))
    if iss <= 0:
        return 0.0

    impact = (
        6.42 * iss
        if scope == "U"
        else 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)
    )

    if impact <= 0:
        return 0.0

    exploitability = 8.22 * av * ac * pr * ui
    raw_base = impact + exploitability if scope == "U" else 1.08 * (impact + exploitability)
    return _cvss_roundup(min(raw_base, 10.0))


def _severity_from_cvss(score: float) -> str:
    if score >= 9.0:
        return "CRITICAL"
    if score >= 7.0:
        return "HIGH"
    if score >= 4.0:
        return "MEDIUM"
    return "LOW"


def _normalize_severity_label(raw: Any) -> str | None:
    if not isinstance(raw, str):
        return None
    upper = raw.strip().upper()
    if upper == "MODERATE":
        return "MEDIUM"
    if upper in _VALID_SEVERITIES:
        return upper
    return None


def _extract_severity_and_cvss(vuln: dict[str, Any]) -> tuple[str, float | None]:
    best_cvss: float | None = None
    for item in vuln.get("severity", []) or []:
        if not isinstance(item, dict):
            continue
        parsed = _parse_cvss_score(item.get("score"))
        if parsed is not None and (best_cvss is None or parsed > best_cvss):
            best_cvss = parsed

    db_sev = None
    for container_key in ("database_specific", "ecosystem_specific"):
        container = vuln.get(container_key)
        if isinstance(container, dict):
            db_sev = _normalize_severity_label(container.get("severity"))
            if db_sev:
                break

    if best_cvss is not None:
        return _severity_from_cvss(best_cvss), best_cvss
    if db_sev is not None:
        return db_sev, None
    return "MEDIUM", None


def _extract_fixed_version(vuln: dict[str, Any], dep: DependencyRecord) -> str | None:
    affected_list = vuln.get("affected", []) or []
    if not isinstance(affected_list, list):
        return None

    dep_name_low = dep.name.lower()
    matching_first: list[dict[str, Any]] = []
    others: list[dict[str, Any]] = []
    for item in affected_list:
        if not isinstance(item, dict):
            continue
        pkg = item.get("package", {})
        if isinstance(pkg, dict) and (
            pkg.get("purl") == dep.purl or str(pkg.get("name", "")).lower() == dep_name_low
        ):
            matching_first.append(item)
        else:
            others.append(item)

    for item in [*matching_first, *others]:
        for rng in item.get("ranges", []) or []:
            if not isinstance(rng, dict):
                continue
            for evt in rng.get("events", []) or []:
                if isinstance(evt, dict) and evt.get("fixed"):
                    return str(evt["fixed"]).strip()
    return None


def _extract_vuln_id(vuln: dict[str, Any]) -> str:
    raw_id = str(vuln.get("id") or "").strip()
    if raw_id:
        return raw_id
    for alias in vuln.get("aliases", []) or []:
        alias_str = str(alias).strip()
        if alias_str.startswith(("CVE-", "GHSA-", "MAL-")):
            return alias_str
    aliases = vuln.get("aliases", []) or []
    return str(aliases[0]).strip() if aliases else "OSV-UNKNOWN"


def _build_osv_query(dep: DependencyRecord) -> dict[str, Any] | None:
    if dep.purl:
        tail = dep.purl.rsplit("/", 1)[-1]
        has_purl_ver = "@" in tail
        if dep.version and not has_purl_ver:
            return {"package": {"purl": dep.purl}, "version": dep.version}
        return {"package": {"purl": dep.purl}}
    if dep.name and dep.ecosystem:
        query: dict[str, Any] = {
            "package": {"name": dep.name, "ecosystem": dep.ecosystem}
        }
        if dep.version:
            query["version"] = dep.version
        return query
    return None


def _cache_key(dep: DependencyRecord) -> str:
    if dep.purl:
        return dep.purl
    return f"{dep.ecosystem}:{dep.name}@{dep.version}"


class OSVBatchClient:
    """
    Batched OSV.dev `/v1/querybatch` client (<= 500 queries per POST) with injectable
    httpx transport, fast timeouts, graceful error handling, and local JSON cache fallback.
    """

    def __init__(
        self,
        *,
        transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None = None,
        timeout: float = 5.0,
        cache_path: Path | None = None,
        batch_size: int = MAX_OSV_BATCH_SIZE,
        base_url: str = OSV_API_BASE,
    ) -> None:
        self.transport = transport
        self.timeout = timeout
        self.cache_path = cache_path
        self.batch_size = min(max(1, batch_size), MAX_OSV_BATCH_SIZE)
        self.base_url = base_url.rstrip("/")
        self._sync_client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    def __enter__(self) -> OSVBatchClient:
        self._sync_client = self._create_sync_client()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None

    async def __aenter__(self) -> OSVBatchClient:
        self._async_client = self._create_async_client()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def _create_sync_client(self) -> httpx.Client:
        kwargs: dict[str, Any] = {"base_url": self.base_url, "timeout": self.timeout}
        if self.transport is not None:
            kwargs["transport"] = self.transport
        try:
            return httpx.Client(**kwargs)
        except (httpx.InvalidURL, ValueError):
            kwargs["trust_env"] = False
            return httpx.Client(**kwargs)

    def _create_async_client(self) -> httpx.AsyncClient:
        kwargs: dict[str, Any] = {"base_url": self.base_url, "timeout": self.timeout}
        if self.transport is not None:
            kwargs["transport"] = self.transport
        try:
            return httpx.AsyncClient(**kwargs)
        except (httpx.InvalidURL, ValueError):
            kwargs["trust_env"] = False
            return httpx.AsyncClient(**kwargs)

    def load_cache(self) -> dict[str, list[dict[str, Any]]]:
        if self.cache_path is None or not self.cache_path.exists():
            return {}
        try:
            data = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        if not isinstance(data, dict):
            return {}
        cleaned: dict[str, list[dict[str, Any]]] = {}
        for k, v in data.items():
            if isinstance(k, str) and isinstance(v, list):
                cleaned[k] = [item for item in v if isinstance(item, dict)]
        return cleaned

    def save_cache(self, cache: dict[str, list[dict[str, Any]]]) -> None:
        if self.cache_path is None:
            return
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            sorted_payload = {k: cache[k] for k in sorted(cache)}
            self.cache_path.write_text(
                json.dumps(sorted_payload, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            logger.warning("Failed to write OSV cache %s: %s", self.cache_path, exc)

    def _post_chunk_sync(
        self, client: httpx.Client, chunk: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        try:
            resp = client.post(OSV_QUERYBATCH_PATH, json={"queries": chunk})
            resp.raise_for_status()
            payload = resp.json()
        except (httpx.HTTPError, httpx.InvalidURL, ValueError, RuntimeError) as exc:
            logger.warning("OSV querybatch request failed: %s", exc)
            return [{} for _ in chunk]

        results = payload.get("results", []) if isinstance(payload, dict) else []
        if not isinstance(results, list):
            return [{} for _ in chunk]
        padded = [r if isinstance(r, dict) else {} for r in results[: len(chunk)]]
        while len(padded) < len(chunk):
            padded.append({})
        return padded

    async def _post_chunk_async(
        self, client: httpx.AsyncClient, chunk: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        try:
            resp = await client.post(OSV_QUERYBATCH_PATH, json={"queries": chunk})
            resp.raise_for_status()
            payload = resp.json()
        except (httpx.HTTPError, httpx.InvalidURL, ValueError, RuntimeError) as exc:
            logger.warning("OSV async querybatch request failed: %s", exc)
            return [{} for _ in chunk]

        results = payload.get("results", []) if isinstance(payload, dict) else []
        if not isinstance(results, list):
            return [{} for _ in chunk]
        padded = [r if isinstance(r, dict) else {} for r in results[: len(chunk)]]
        while len(padded) < len(chunk):
            padded.append({})
        return padded

    def query_batch(self, queries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Execute batched POST /v1/querybatch calls synchronously (<= 500 queries/POST)."""
        if not queries:
            return []
        all_results: list[dict[str, Any]] = []
        own_client = self._sync_client is None
        client = self._sync_client or self._create_sync_client()
        try:
            for start in range(0, len(queries), self.batch_size):
                chunk = queries[start : start + self.batch_size]
                all_results.extend(self._post_chunk_sync(client, chunk))
        finally:
            if own_client:
                client.close()
        return all_results

    async def aquery_batch(self, queries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Execute batched POST /v1/querybatch calls asynchronously (<= 500 queries/POST)."""
        if not queries:
            return []
        all_results: list[dict[str, Any]] = []
        own_client = self._async_client is None
        client = self._async_client or self._create_async_client()
        try:
            for start in range(0, len(queries), self.batch_size):
                chunk = queries[start : start + self.batch_size]
                all_results.extend(await self._post_chunk_async(client, chunk))
        finally:
            if own_client:
                await client.aclose()
        return all_results

    def query_dependencies(
        self,
        dependencies: list[DependencyRecord],
        *,
        enable_live: bool = False,
    ) -> dict[str, list[dict[str, Any]]]:
        """Query OSV for dependencies using cache and offline-safe network gating."""
        cache = self.load_cache()
        live_allowed = (
            self.transport is not None
            or enable_live
            or os.getenv("ATRUSS_ENABLE_LIVE_OSV") == "1"
        )

        keyed_queries: dict[str, dict[str, Any]] = {}
        for dep in dependencies:
            key = _cache_key(dep)
            if not key or key in cache or key in keyed_queries:
                continue
            q = _build_osv_query(dep)
            if q is not None:
                keyed_queries[key] = q

        if live_allowed and keyed_queries:
            keys = list(keyed_queries.keys())
            queries = [keyed_queries[k] for k in keys]
            results = self.query_batch(queries)
            updated = False
            for key, res in zip(keys, results, strict=True):
                vulns = res.get("vulns", [])
                if isinstance(vulns, list):
                    cache[key] = [v for v in vulns if isinstance(v, dict)]
                    updated = True
            if updated:
                self.save_cache(cache)

        return {
            _cache_key(dep): cache.get(_cache_key(dep), [])
            for dep in dependencies
            if _cache_key(dep)
        }


def _collect_reachability_corpora(
    repo_dir: Path | None,
) -> tuple[dict[str, list[str]], list[str]]:
    """Collect runtime source contents by extension and CI workflow lines."""
    runtime_by_ext: dict[str, list[str]] = {}
    ci_lines: list[str] = []
    if repo_dir is None or not repo_dir.exists() or not repo_dir.is_dir():
        return runtime_by_ext, ci_lines

    all_source_exts = frozenset().union(*_SOURCE_EXTENSIONS.values())

    for root, dirnames, filenames in os.walk(repo_dir):
        root_path = Path(root)
        rel_root = root_path.relative_to(repo_dir)
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)

        is_ci_dir = (
            len(rel_root.parts) >= 2
            and rel_root.parts[0] == ".github"
            and rel_root.parts[1] == "workflows"
        )

        for fname in sorted(filenames):
            fpath = root_path / fname
            if is_ci_dir and fpath.suffix.lower() in {".yml", ".yaml"}:
                try:
                    text = fpath.read_text(encoding="utf-8", errors="replace")
                    for line in text.splitlines():
                        if not re.match(r"^\s*-?\s*uses\s*:", line):
                            ci_lines.append(line)
                except OSError:
                    continue
                continue

            if rel_root.parts and rel_root.parts[0] == ".github":
                continue

            ext = fpath.suffix.lower()
            if ext in all_source_exts:
                try:
                    runtime_by_ext.setdefault(ext, []).append(
                        fpath.read_text(encoding="utf-8", errors="replace")
                    )
                except OSError:
                    continue

    return runtime_by_ext, ci_lines


def _maven_group_artifact(dep: DependencyRecord) -> tuple[str, str]:
    if ":" in dep.name:
        group, artifact = dep.name.split(":", 1)
        return group.strip(), artifact.strip()
    if dep.purl.startswith("pkg:maven/"):
        body = dep.purl.removeprefix("pkg:maven/").split("@", 1)[0]
        if "/" in body:
            group, artifact = body.split("/", 1)
            return group, artifact
    return "", dep.name


def _is_runtime_reachable(dep: DependencyRecord, runtime_by_ext: dict[str, list[str]]) -> bool:
    eco = dep.ecosystem.strip().lower()
    exts = _SOURCE_EXTENSIONS.get(eco, frozenset())
    texts = [txt for ext in exts for txt in runtime_by_ext.get(ext, ())]
    if not texts:
        return False

    if eco == "pypi":
        base = dep.name.strip().lower()
        candidates = {base, base.replace("-", "_"), base.replace(".", "_")}
        candidates.update(_PYPI_IMPORT_ALIASES.get(base.replace("_", "-"), ()))
        alts = "|".join(re.escape(c) for c in sorted(candidates) if c)
        import_re = re.compile(
            rf"(?:^\s*(?:import|from)\s+(?:{alts})(?:[\s.,]|$)|"
            rf"import_module\(\s*['\"](?:{alts})['\"])",
            re.MULTILINE | re.IGNORECASE,
        )
        return any(import_re.search(txt) for txt in texts)

    if eco == "npm":
        escaped = re.escape(dep.name.strip())
        npm_re = re.compile(
            rf"""(?:from\s+|require\s*\(\s*|import\s*\(\s*|import\s+)['"]{escaped}(?:/[^'"]*)?['"]"""
        )
        return any(npm_re.search(txt) for txt in texts)

    if eco == "nuget":
        escaped = re.escape(dep.name.strip())
        nuget_re = re.compile(
            rf"(?:using|Imports|open)\s+{escaped}(?:\s*;|\.|\s|$)|{escaped}\.",
            re.IGNORECASE,
        )
        return any(nuget_re.search(txt) for txt in texts)

    if eco == "maven":
        group, artifact = _maven_group_artifact(dep)
        patterns: list[str] = []
        if group:
            patterns.append(rf"import\s+(?:static\s+)?{re.escape(group)}\.")
        if artifact:
            art_pkg = re.escape(artifact.replace("-", "."))
            patterns.append(rf"import\s+(?:static\s+)?(?:[A-Za-z0-9_.]+\.)?{art_pkg}\b")
        if not patterns:
            return False
        maven_re = re.compile("|".join(patterns))
        return any(maven_re.search(txt) for txt in texts)

    return False


def _is_ci_reachable(dep: DependencyRecord, ci_lines: list[str]) -> bool:
    if not ci_lines:
        return False
    eco = dep.ecosystem.strip().lower()
    tokens: set[str] = {dep.name.strip()}
    if eco == "pypi":
        low = dep.name.strip().lower()
        tokens.update({low, low.replace("-", "_"), low.replace("_", "-")})
        tokens.update(_PYPI_IMPORT_ALIASES.get(low.replace("_", "-"), ()))
    elif eco == "maven":
        group, artifact = _maven_group_artifact(dep)
        if group:
            tokens.add(group)
        if artifact:
            tokens.add(artifact)

    ci_corpus = "\n".join(ci_lines)
    for tok in sorted(t for t in tokens if t):
        pat = re.compile(
            rf"(?<![A-Za-z0-9_./-]){re.escape(tok)}(?![A-Za-z0-9_.-])",
            re.IGNORECASE,
        )
        if pat.search(ci_corpus):
            return True
    return False


def _classify_reachability(
    dep: DependencyRecord,
    runtime_by_ext: dict[str, list[str]],
    ci_lines: list[str],
) -> str:
    if _is_runtime_reachable(dep, runtime_by_ext):
        return "REACHABLE_FROM_RUNTIME"
    if _is_ci_reachable(dep, ci_lines):
        return "REACHABLE_FROM_CI"
    return "UNREACHABLE_DORMANT"


def scan_dependencies_with_osv(
    dependencies: list[DependencyRecord],
    *,
    repo_dir: Path | None = None,
    transport: httpx.BaseTransport | None = None,
    cache_path: Path | None = None,
    enable_live: bool = False,
) -> list[VulnerabilityRecord]:
    """
    Scan parsed dependencies against OSV.dev batch API (or local cache when offline),
    classify reachability (`REACHABLE_FROM_CI`, `REACHABLE_FROM_RUNTIME`, `UNREACHABLE_DORMANT`),
    and populate `dep.vulnerability_ids`.
    """
    if not dependencies:
        return []

    live_enabled = enable_live or os.getenv("ATRUSS_ENABLE_LIVE_OSV") == "1"
    if transport is None and not live_enabled and cache_path is None:
        return []

    client = OSVBatchClient(transport=transport, cache_path=cache_path)
    vuln_map = client.query_dependencies(dependencies, enable_live=enable_live)

    runtime_by_ext, ci_lines = _collect_reachability_corpora(repo_dir)
    reachability_cache: dict[tuple[str, str], str] = {}
    records: list[VulnerabilityRecord] = []

    for dep in dependencies:
        key = _cache_key(dep)
        raw_vulns = vuln_map.get(key, [])
        if not raw_vulns:
            continue

        reach_key = (dep.ecosystem, dep.name)
        if reach_key not in reachability_cache:
            reachability_cache[reach_key] = _classify_reachability(
                dep, runtime_by_ext, ci_lines
            )
        reachability = reachability_cache[reach_key]

        dep_vuln_ids = list(dep.vulnerability_ids)
        seen_for_dep = set(dep_vuln_ids)

        for raw_vuln in raw_vulns:
            vuln_id = _extract_vuln_id(raw_vuln)
            severity, cvss_score = _extract_severity_and_cvss(raw_vuln)
            fixed_version = _extract_fixed_version(raw_vuln, dep)
            summary = str(raw_vuln.get("summary") or raw_vuln.get("details") or "").strip()
            if len(summary) > 300:
                summary = summary[:297].rstrip() + "..."

            if vuln_id not in seen_for_dep:
                seen_for_dep.add(vuln_id)
                dep_vuln_ids.append(vuln_id)

            records.append(
                VulnerabilityRecord(
                    id=vuln_id,
                    package=dep.name,
                    purl=dep.purl,
                    installed_version=dep.version,
                    fixed_version=fixed_version,
                    severity=severity,
                    cvss_score=cvss_score,
                    summary=summary,
                    reachability=reachability,
                    manifest_file=dep.manifest_file,
                    line=dep.line,
                )
            )

        dep.vulnerability_ids = sorted(set(dep_vuln_ids))

    return sorted(
        records,
        key=lambda v: (v.manifest_file, v.line, v.purl, v.id),
    )
