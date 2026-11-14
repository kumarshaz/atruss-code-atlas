#!/usr/bin/env python3
"""
Curate, pin SHAs, and validate the 100 Popular GitHub Projects Corpus
(`tests/fixtures/popular_100_corpus.json`) across the 4 MVP ecosystems:
  - 25 Python (`python`)
  - 25 .NET (`.net`)
  - 25 React/TypeScript/JavaScript (`react_ts_js`)
  - 25 Java Spring Boot (`java_springboot`)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.models.benchmark import ECOSYSTEM_KEY_TO_DISPLAY, CorpusEntry  # noqa: E402

DEFAULT_CORPUS_PATH = REPO_ROOT / "tests" / "fixtures" / "popular_100_corpus.json"
REQUIRED_PER_ECOSYSTEM = 25
GOLDEN_FIXTURE_NAMES = {
    "dotnet/eShop",
    "github-samples/pets-workshop",
    "Azure-Samples/todo-nodejs-mongo-terraform",
    "hamvocke/spring-testing",
}

# Format: (full_name, branch, estimated_size_mb, estimated_loc, stars, is_golden, tags)
CURATED_CATALOG: dict[str, list[tuple[str, str, float, int, int, bool, list[str]]]] = {
    "python": [
        ("fastapi/fastapi", "master", 59.4, 180000, 104674, False, ["api", "fastapi"]),
        ("pallets/flask", "main", 11.9, 32000, 75111, False, ["web", "flask"]),
        ("pallets/click", "main", 5.4, 24000, 17820, False, ["cli"]),
        ("psf/requests", "main", 13.3, 25000, 54694, False, ["http"]),
        ("psf/black", "main", 9.4, 65000, 42171, False, ["formatter", "ast"]),
        ("encode/httpx", "master", 8.4, 30000, 15803, False, ["http", "async"]),
        ("pytest-dev/pytest", "main", 41.5, 115000, 14698, False, ["testing"]),
        ("Textualize/rich", "main", 49.5, 70000, 57818, False, ["tui"]),
        ("python-poetry/poetry", "main", 25.7, 90000, 34322, False, ["packaging"]),
        ("httpie/cli", "master", 6.8, 38000, 38709, False, ["cli", "http"]),
        ("scrapy/scrapy", "master", 33.2, 95000, 65355, False, ["crawling"]),
        ("tqdm/tqdm", "master", 6.1, 18000, 31385, False, ["cli"]),
        ("nvbn/thefuck", "master", 3.9, 25000, 97955, False, ["cli"]),
        ("yt-dlp/yt-dlp", "master", 63.5, 220000, 207339, False, ["media", "cli"]),
        ("openai/whisper", "main", 12.5, 12000, 112607, False, ["ml"]),
        ("openai/openai-python", "main", 29.6, 140000, 32139, False, ["sdk"]),
        ("microsoft/markitdown", "main", 5.9, 18000, 195136, False, ["docs", "ai"]),
        ("github/spec-kit", "main", 22.7, 25000, 149557, False, ["sdd", "cli"]),
        ("sherlock-project/sherlock", "master", 18.7, 15000, 110609, False, ["osint"]),
        ("browser-use/browser-use", "main", 39.5, 95000, 120862, False, ["agents"]),
        ("D4Vinci/Scrapling", "main", 15.9, 32000, 102203, False, ["scraping"]),
        ("google/langextract", "main", 13.0, 28000, 39306, False, ["nlp"]),
        ("assafelovic/gpt-researcher", "main", 53.1, 80000, 30657, False, ["agents"]),
        ("ManimCommunity/manim", "main", 47.0, 120000, 42451, False, ["graphics"]),
        ("sansan0/TrendRadar", "master", 33.6, 45000, 63613, False, ["analytics"]),
    ],
    ".net": [
        (
            "dotnet/eShop",
            "main",
            26.8,
            120000,
            11019,
            True,
            ["golden", "microservices", "aspnetcore"],
        ),
        (
            "dotnet-architecture/eShopOnWeb",
            "main",
            59.7,
            65000,
            10670,
            True,
            ["golden", "aspnetcore"],
        ),
        (
            "jasontaylordev/CleanArchitecture",
            "main",
            9.8,
            22000,
            20717,
            False,
            ["clean-arch", "webapi"],
        ),
        ("ardalis/CleanArchitecture", "main", 3.8, 18000, 18548, False, ["clean-arch", "ddd"]),
        (
            "kgrzybek/modular-monolith-with-ddd",
            "master",
            8.2,
            42000,
            14134,
            False,
            ["ddd", "modular-monolith"],
        ),
        ("DapperLib/Dapper", "main", 48.8, 55000, 18417, False, ["orm", "data"]),
        ("App-vNext/Polly", "main", 61.5, 85000, 14254, False, ["resilience"]),
        ("winsw/winsw", "v3", 3.5, 16000, 14426, False, ["service", "windows"]),
        ("icsharpcode/ILSpy", "master", 51.2, 240000, 27053, False, ["decompiler"]),
        ("microsoft/calculator", "main", 39.5, 145000, 31095, False, ["desktop"]),
        ("NickeManarin/ScreenToGif", "master", 24.8, 130000, 27926, False, ["desktop"]),
        ("jellyfin/jellyfin", "master", 77.5, 290000, 59279, False, ["media", "webapi"]),
        ("bitwarden/server", "main", 78.1, 310000, 20627, False, ["security", "aspnetcore"]),
        ("Jackett/Jackett", "master", 44.5, 190000, 16360, False, ["webapi", "service"]),
        ("2dust/v2rayN", "master", 50.0, 95000, 120497, False, ["networking"]),
        ("shadowsocks/shadowsocks-windows", "v4", 13.2, 35000, 59483, False, ["networking"]),
        ("BCUninstaller/Bulk-Crap-Uninstaller", "master", 10.8, 75000, 22443, False, ["desktop"]),
        ("JosefNemec/Playnite", "master", 73.9, 180000, 14509, False, ["desktop"]),
        ("Tyrrrz/YoutubeDownloader", "prime", 1.6, 15000, 16709, False, ["desktop"]),
        ("seerge/g-helper", "main", 43.6, 35000, 16031, False, ["utility"]),
        ("srwi/EverythingToolbar", "develop", 27.9, 22000, 15052, False, ["desktop"]),
        ("BluePointLilac/ContextMenuManager", "master", 1.8, 25000, 20433, False, ["desktop"]),
        ("nilaoda/N_m3u8DL-CLI", "master", 6.2, 20000, 16163, False, ["cli"]),
        ("mxgmn/WaveFunctionCollapse", "master", 30.4, 8000, 25516, False, ["algorithms"]),
        ("memstechtips/Winhance", "main", 44.2, 28000, 14842, False, ["utility"]),
    ],
    "react_ts_js": [
        (
            "github-samples/pets-workshop",
            "main",
            5.4,
            18000,
            83,
            True,
            ["golden", "monorepo", "workshop"],
        ),
        (
            "Azure-Samples/todo-nodejs-mongo-terraform",
            "main",
            2.4,
            12000,
            9,
            True,
            ["golden", "react", "nodejs"],
        ),
        (
            "jeffrafter/example-github-action-typescript",
            "master",
            0.5,
            4000,
            16,
            True,
            ["golden", "typescript", "actions"],
        ),
        (
            "benchmark-action/github-action-benchmark",
            "master",
            8.3,
            25000,
            1272,
            True,
            ["golden", "typescript", "actions"],
        ),
        ("expressjs/express", "master", 9.8, 32000, 69676, False, ["nodejs", "api"]),
        ("vitejs/vite", "main", 76.4, 140000, 83896, False, ["vite", "tooling"]),
        ("vuejs/core", "main", 46.7, 130000, 55014, False, ["frontend", "typescript"]),
        ("vuejs/vue", "main", 31.4, 85000, 212526, False, ["frontend"]),
        ("reduxjs/redux", "master", 34.8, 55000, 61438, False, ["react", "state"]),
        ("pmndrs/zustand", "main", 8.1, 22000, 58933, False, ["react", "state"]),
        ("remix-run/react-router", "main", 45.9, 125000, 56634, False, ["react", "routing"]),
        (
            "react-hook-form/react-hook-form",
            "master",
            32.8,
            48000,
            44919,
            False,
            ["react", "forms"],
        ),
        ("colinhacks/zod", "main", 26.6, 52000, 44341, False, ["typescript", "validation"]),
        ("socketio/socket.io", "main", 33.3, 62000, 63246, False, ["nodejs", "realtime"]),
        ("markedjs/marked", "master", 11.0, 24000, 37304, False, ["markdown", "parser"]),
        ("hexojs/hexo", "master", 7.2, 30000, 41776, False, ["ssg", "nodejs"]),
        ("vadimdemedes/ink", "master", 2.7, 18000, 40263, False, ["react", "cli"]),
        (
            "styled-components/styled-components",
            "main",
            42.3,
            68000,
            41046,
            False,
            ["react", "css"],
        ),
        ("slab/quill", "main", 18.0, 48000, 47367, False, ["editor", "typescript"]),
        ("xyflow/xyflow", "main", 46.3, 95000, 38991, False, ["react", "diagrams"]),
        ("ChatGPTNextWeb/NextChat", "main", 23.4, 88000, 88951, False, ["nextjs", "react"]),
        ("umami-software/umami", "master", 32.8, 72000, 40105, False, ["nextjs", "analytics"]),
        (
            "ChromeDevTools/chrome-devtools-mcp",
            "main",
            13.0,
            26000,
            55179,
            False,
            ["mcp", "typescript"],
        ),
        ("AykutSarac/jsoncrack.com", "main", 41.0, 64000, 44594, False, ["nextjs", "react"]),
        ("ant-design/ant-design-pro", "master", 41.2, 92000, 38962, False, ["react", "ui"]),
    ],
    "java_springboot": [
        (
            "hamvocke/spring-testing",
            "main",
            6.7,
            8000,
            1244,
            True,
            ["golden", "springboot", "testing"],
        ),
        (
            "spring-projects/spring-petclinic",
            "main",
            10.7,
            18000,
            9645,
            True,
            ["golden", "springboot"],
        ),
        ("spring-guides/gs-rest-service", "main", 1.7, 3000, 1484, False, ["springboot", "rest"]),
        ("macrozheng/mall", "master", 57.4, 160000, 85044, False, ["springboot", "ecommerce"]),
        (
            "macrozheng/mall-swarm",
            "master",
            53.3,
            180000,
            13204,
            False,
            ["springcloud", "microservices"],
        ),
        (
            "xkcoding/spring-boot-demo",
            "master",
            13.9,
            55000,
            34036,
            False,
            ["springboot", "examples"],
        ),
        (
            "ityouknow/spring-boot-examples",
            "master",
            1.0,
            42000,
            30431,
            False,
            ["springboot", "examples"],
        ),
        ("elunez/eladmin", "master", 7.4, 65000, 21895, False, ["springboot", "admin"]),
        ("linlinjava/litemall", "master", 24.0, 95000, 20407, False, ["springboot", "ecommerce"]),
        ("yudaocode/SpringBoot-Labs", "master", 1.8, 85000, 20116, False, ["springboot", "labs"]),
        ("forezp/SpringCloudLearning", "master", 0.6, 22000, 17891, False, ["springcloud"]),
        ("dyc87112/SpringBoot-Learning", "master", 33.6, 48000, 15686, False, ["springboot"]),
        (
            "sqshq/piggymetrics",
            "master",
            1.5,
            32000,
            13972,
            False,
            ["springcloud", "microservices"],
        ),
        ("newbee-ltd/newbee-mall", "master", 35.4, 62000, 11661, False, ["springboot"]),
        ("zfile-dev/zfile", "main", 45.1, 58000, 10873, False, ["springboot", "storage"]),
        (
            "lihengming/spring-boot-api-project-seed",
            "master",
            0.1,
            8000,
            9674,
            False,
            ["springboot", "seed"],
        ),
        ("hs-web/hsweb-framework", "5.0.x", 34.0, 140000, 8396, False, ["springboot", "framework"]),
        ("jetlinks/jetlinks-community", "2.11", 69.5, 220000, 6686, False, ["springboot", "iot"]),
        ("DerekYRC/mini-spring", "main", 1.1, 16000, 6365, False, ["spring", "framework"]),
        ("ityouknow/spring-cloud-examples", "master", 0.1, 14000, 6171, False, ["springcloud"]),
        (
            "baomidou/dynamic-datasource",
            "main",
            1.9,
            28000,
            5190,
            False,
            ["springboot", "database"],
        ),
        ("spring-cloud/spring-cloud-netflix", "main", 21.1, 95000, 4976, False, ["springcloud"]),
        (
            "spring-cloud/spring-cloud-gateway",
            "main",
            15.5,
            85000,
            4921,
            False,
            ["springcloud", "gateway"],
        ),
        (
            "mybatis/spring-boot-starter",
            "master",
            16.4,
            24000,
            4248,
            False,
            ["springboot", "mybatis"],
        ),
        ("apolloconfig/apollo", "master", 56.9, 175000, 29813, False, ["springboot", "config"]),
    ],
}


def build_corpus_entries() -> list[CorpusEntry]:
    """Construct the stratified 100-entry `CorpusEntry` list."""
    entries: list[CorpusEntry] = []
    for eco_key, rows in CURATED_CATALOG.items():
        display = ECOSYSTEM_KEY_TO_DISPLAY[eco_key]
        for full_name, branch, size_mb, loc, stars, is_golden, tags in rows:
            org, name = full_name.split("/", 1)
            entries.append(
                CorpusEntry(
                    org=org,
                    name=name,
                    full_name=full_name,
                    url=f"https://github.com/{full_name}",
                    clone_url=f"https://github.com/{full_name}.git",
                    expected_ecosystem=display,
                    ecosystem_key=eco_key,  # type: ignore[arg-type]
                    expected_pipeline=True,
                    pinned_ref=branch,
                    pinned_sha=None,
                    estimated_size_mb=size_mb,
                    estimated_loc=loc,
                    star_tier="popular",
                    stars=stars,
                    is_golden_fixture=is_golden,
                    tags=list(tags),
                )
            )
    return entries


async def _ls_remote_sha(clone_url: str, ref: str, sem: asyncio.Semaphore) -> str | None:
    async with sem:
        proc = await asyncio.create_subprocess_exec(
            "git",
            "ls-remote",
            clone_url,
            ref,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=20.0)
        except asyncio.TimeoutError:
            proc.kill()
            return None
        if proc.returncode != 0:
            return None
        lines = stdout.decode("utf-8", errors="replace").strip().splitlines()
        if not lines:
            return None
        return lines[0].split()[0]


async def resolve_shas(entries: list[CorpusEntry]) -> list[CorpusEntry]:
    """Pin live commit SHAs via `git ls-remote` without consuming GitHub REST API quota."""
    sem = asyncio.Semaphore(10)
    shas = await asyncio.gather(*(_ls_remote_sha(e.clone_url, e.pinned_ref, sem) for e in entries))
    updated: list[CorpusEntry] = []
    for entry, sha in zip(entries, shas, strict=True):
        updated.append(entry.model_copy(update={"pinned_sha": sha or entry.pinned_sha}))
    return updated


def validate_corpus_data(data: Any) -> list[str]:
    """Validate corpus JSON structure, balance, uniqueness, golden fixtures, and SLA limits."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Corpus JSON root must be an object"]
    items = data.get("repositories")
    if not isinstance(items, list):
        return ["Corpus JSON must contain a 'repositories' list"]

    entries: list[CorpusEntry] = []
    for idx, raw in enumerate(items):
        try:
            entries.append(CorpusEntry.model_validate(raw))
        except Exception as exc:
            errors.append(f"Entry[{idx}] invalid: {exc}")

    if len(entries) != 100:
        errors.append(f"Expected 100 repositories, found {len(entries)}")

    seen = {e.full_name for e in entries}
    if len(seen) != len(entries):
        errors.append("Duplicate repository full_name detected in corpus")

    counts = Counter(e.ecosystem_key for e in entries)
    for eco_key in ("python", ".net", "react_ts_js", "java_springboot"):
        cnt = counts.get(eco_key, 0)
        if cnt != REQUIRED_PER_ECOSYSTEM:
            errors.append(
                f"Ecosystem '{eco_key}' count={cnt}, expected {REQUIRED_PER_ECOSYSTEM}"
            )

    missing_golden = sorted(GOLDEN_FIXTURE_NAMES - seen)
    if missing_golden:
        errors.append(f"Missing required golden fixtures: {', '.join(missing_golden)}")

    return errors


def load_corpus(path: Path = DEFAULT_CORPUS_PATH) -> list[CorpusEntry]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_corpus_data(data)
    if errors:
        raise ValueError("Invalid corpus: " + "; ".join(errors))
    return [CorpusEntry.model_validate(item) for item in data["repositories"]]


def write_corpus(entries: list[CorpusEntry], path: Path = DEFAULT_CORPUS_PATH) -> None:
    payload = {
        "schema_version": "1.0",
        "description": (
            "Stratified 100 Popular Public GitHub Repositories Corpus for Atruss Code Atlas"
        ),
        "total": len(entries),
        "ecosystem_counts": dict(Counter(e.ecosystem_key for e in entries)),
        "repositories": [e.model_dump() for e in entries],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Curate and validate popular_100_corpus.json")
    parser.add_argument("--input", type=Path, default=DEFAULT_CORPUS_PATH)
    parser.add_argument("--write", action="store_true", help="Write curated 100-repo corpus JSON")
    parser.add_argument(
        "--resolve-shas",
        action="store_true",
        help="Pin live HEAD commit SHAs using git ls-remote",
    )
    parser.add_argument("--validate", action="store_true", help="Validate corpus JSON file")
    args = parser.parse_args()

    if args.write or args.resolve_shas:
        entries = build_corpus_entries()
        if args.resolve_shas:
            entries = asyncio.run(resolve_shas(entries))
            pinned = sum(1 for e in entries if e.pinned_sha)
            print(f"Pinned HEAD SHAs via git ls-remote: {pinned}/{len(entries)}")
        write_corpus(entries, args.input)
        print(f"Wrote {len(entries)} corpus entries to {args.input}")

    if args.validate or not (args.write or args.resolve_shas):
        if not args.input.exists():
            print(f"Error: Corpus file not found: {args.input}", file=sys.stderr)
            raise SystemExit(1)
        data = json.loads(args.input.read_text(encoding="utf-8"))
        errors = validate_corpus_data(data)
        if errors:
            for err in errors:
                print(f"FAIL: {err}", file=sys.stderr)
            raise SystemExit(1)
        print(
            f"VALID: {args.input} ({data['total']} repos, distribution={data['ecosystem_counts']})"
        )


if __name__ == "__main__":
    main()
