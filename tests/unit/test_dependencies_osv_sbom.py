from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import httpx
import pytest

from src.analyzers.dependencies import (
    OSVBatchClient,
    parse_repository_dependencies,
    scan_dependencies_with_osv,
    scan_repository_secrets,
    shannon_entropy,
)
from src.analyzers.dependencies.manifest_parser import _parse_pyproject_toml_fallback
from src.core.exporters.sbom_exporter import build_cyclonedx_sbom, export_cyclonedx_sbom
from src.models.artifacts import DependencyRecord, VulnerabilityRecord


def test_parse_python_manifests_and_lockfiles(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text(
        "# Core dependencies\n"
        "requests==2.31.0\n"
        "uvicorn[standard]>=0.29.0; python_version >= '3.10'\n"
        "-r requirements-dev.txt\n"
        "Flask==3.0.2 # inline comment\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements-dev.txt").write_text(
        "pytest==8.1.1\n",
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        '[project]\n'
        'name = "demo-service"\n'
        'description = "Uses fastapi internally"\n'
        'dependencies = [\n'
        '  "fastapi>=0.110.0",\n'
        '  "typing_extensions==4.10.0",\n'
        ']\n'
        '\n'
        '[project.optional-dependencies]\n'
        'dev = ["ruff>=0.3.4"]\n',
        encoding="utf-8",
    )
    (tmp_path / "uv.lock").write_text(
        'version = 1\n'
        '\n'
        '[[package]]\n'
        'name = "demo-service"\n'
        'version = "0.1.0"\n'
        'source = { virtual = "." }\n'
        'dependencies = [\n'
        '  { name = "fastapi" },\n'
        ']\n'
        '\n'
        '[[package]]\n'
        'name = "anyio"\n'
        'version = "4.3.0"\n'
        'source = { registry = "https://pypi.org/simple" }\n'
        '\n'
        '[[package]]\n'
        'name = "fastapi"\n'
        'version = "0.110.0"\n'
        'source = { registry = "https://pypi.org/simple" }\n',
        encoding="utf-8",
    )
    (tmp_path / "poetry.lock").write_text(
        '[[package]]\n'
        'name = "urllib3"\n'
        'version = "2.2.1"\n',
        encoding="utf-8",
    )
    # Must be ignored by SKIP_DIRS
    ignored_venv = tmp_path / ".venv"
    ignored_venv.mkdir()
    (ignored_venv / "requirements.txt").write_text("malicious-ignored==9.9.9\n", encoding="utf-8")

    deps = parse_repository_dependencies(tmp_path)
    assert all(".venv" not in d.manifest_file for d in deps)

    by_key = {(d.manifest_file, d.name): d for d in deps}

    req = by_key[("requirements.txt", "requests")]
    assert req.line == 2
    assert req.version == "2.31.0"
    assert req.purl == "pkg:pypi/requests@2.31.0"
    assert req.is_direct is True
    assert req.ecosystem == "PyPI"

    uvi = by_key[("requirements.txt", "uvicorn")]
    assert uvi.line == 3
    assert uvi.version == "0.29.0"
    assert uvi.purl == "pkg:pypi/uvicorn@0.29.0"

    flask = by_key[("requirements.txt", "Flask")]
    assert flask.line == 5
    assert flask.purl == "pkg:pypi/flask@3.0.2"

    assert by_key[("requirements-dev.txt", "pytest")].line == 1

    fastapi_pyproj = by_key[("pyproject.toml", "fastapi")]
    assert fastapi_pyproj.line == 5
    assert fastapi_pyproj.purl == "pkg:pypi/fastapi@0.110.0"

    typing_ext = by_key[("pyproject.toml", "typing_extensions")]
    assert typing_ext.line == 6
    assert typing_ext.purl == "pkg:pypi/typing-extensions@4.10.0"

    assert by_key[("pyproject.toml", "ruff")].line == 10

    uv_fastapi = by_key[("uv.lock", "fastapi")]
    assert uv_fastapi.is_direct is True
    assert uv_fastapi.line == 17
    assert uv_fastapi.purl == "pkg:pypi/fastapi@0.110.0"

    uv_anyio = by_key[("uv.lock", "anyio")]
    assert uv_anyio.is_direct is False
    assert uv_anyio.line == 12
    assert uv_anyio.purl == "pkg:pypi/anyio@4.3.0"

    assert ("uv.lock", "demo-service") not in by_key

    poetry_urllib3 = by_key[("poetry.lock", "urllib3")]
    assert poetry_urllib3.is_direct is False
    assert poetry_urllib3.line == 2
    assert poetry_urllib3.purl == "pkg:pypi/urllib3@2.2.1"

    # Verify deterministic ordering (manifest_file, line, purl)
    keys = [(d.manifest_file, d.line, d.purl) for d in deps]
    assert keys == sorted(keys)


def test_pyproject_toml_fallback_parser() -> None:
    toml_text = (
        '[project]\n'
        'name = "fallback-demo"\n'
        'dependencies = [\n'
        '  "httpx>=0.27.0",\n'
        '  "pydantic==2.7.1"\n'
        ']\n'
        '\n'
        '[tool.poetry.dependencies]\n'
        'python = "^3.11"\n'
        'pyyaml = "^6.0.1"\n'
    )
    parsed = _parse_pyproject_toml_fallback(toml_text)
    assert parsed["project"]["dependencies"] == ["httpx>=0.27.0", "pydantic==2.7.1"]
    assert parsed["tool"]["poetry"]["dependencies"]["pyyaml"] == "^6.0.1"


def test_parse_js_dotnet_and_java_manifests(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "name": "web-app",
                "license": "Apache-2.0",
                "dependencies": {
                    "express": "^4.18.2",
                    "@babel/core": "~7.24.0",
                },
                "devDependencies": {
                    "vitest": "1.6.0",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (tmp_path / "package-lock.json").write_text(
        json.dumps(
            {
                "name": "web-app",
                "lockfileVersion": 3,
                "packages": {
                    "": {
                        "name": "web-app",
                        "dependencies": {"express": "^4.18.2"},
                    },
                    "node_modules/express": {
                        "version": "4.18.2",
                        "license": "MIT",
                    },
                    "node_modules/ms": {
                        "version": "2.1.3",
                        "license": "MIT",
                    },
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (tmp_path / "pnpm-lock.yaml").write_text(
        "lockfileVersion: '9.0'\n"
        "importers:\n"
        "  .:\n"
        "    dependencies:\n"
        "      express:\n"
        "        specifier: ^4.18.2\n"
        "        version: 4.18.2\n"
        "packages:\n"
        "  express@4.18.2:\n"
        "    resolution: {integrity: sha512-abc}\n"
        "  debug@4.3.4(supports-color@7.2.1):\n"
        "    resolution: {integrity: sha512-def}\n",
        encoding="utf-8",
    )

    dotnet_dir = tmp_path / "api"
    dotnet_dir.mkdir()
    (dotnet_dir / "OrderApi.csproj").write_text(
        '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
        '  <ItemGroup>\n'
        '    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />\n'
        '    <PackageReference Include="Serilog">\n'
        '      <Version>3.1.1</Version>\n'
        '    </PackageReference>\n'
        '  </ItemGroup>\n'
        '</Project>\n',
        encoding="utf-8",
    )
    (dotnet_dir / "packages.lock.json").write_text(
        json.dumps(
            {
                "version": 1,
                "dependencies": {
                    "net8.0": {
                        "Newtonsoft.Json": {"type": "Direct", "resolved": "13.0.3"},
                        "System.Text.Encodings.Web": {
                            "type": "Transitive",
                            "resolved": "8.0.0",
                        },
                    }
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    java_dir = tmp_path / "billing"
    java_dir.mkdir()
    (java_dir / "pom.xml").write_text(
        '<project xmlns="http://maven.apache.org/POM/4.0.0">\n'
        '  <properties>\n'
        '    <jackson.version>2.15.2</jackson.version>\n'
        '  </properties>\n'
        '  <dependencies>\n'
        '    <dependency>\n'
        '      <groupId>com.fasterxml.jackson.core</groupId>\n'
        '      <artifactId>jackson-databind</artifactId>\n'
        '      <version>${jackson.version}</version>\n'
        '    </dependency>\n'
        '  </dependencies>\n'
        '</project>\n',
        encoding="utf-8",
    )
    (java_dir / "build.gradle.kts").write_text(
        'dependencies {\n'
        '    implementation("org.springframework.boot:spring-boot-starter-web:3.2.4")\n'
        '}\n',
        encoding="utf-8",
    )

    # Skipped dirs must never appear
    nm = tmp_path / "node_modules" / "evil"
    nm.mkdir(parents=True)
    (nm / "package.json").write_text('{"dependencies":{"bad":"1.0.0"}}', encoding="utf-8")
    obj_dir = dotnet_dir / "obj"
    obj_dir.mkdir()
    (obj_dir / "packages.lock.json").write_text(
        '{"dependencies":{"net8.0":{"Ignored":{"type":"Direct","resolved":"1.0.0"}}}}',
        encoding="utf-8",
    )

    deps = parse_repository_dependencies(tmp_path)
    by_key = {(d.manifest_file, d.name): d for d in deps}

    pkg_exp = by_key[("package.json", "express")]
    assert pkg_exp.purl == "pkg:npm/express@4.18.2"
    assert pkg_exp.is_direct is True
    assert pkg_exp.license == "MIT"
    assert pkg_exp.line == 5

    babel = by_key[("package.json", "@babel/core")]
    assert babel.purl == "pkg:npm/%40babel/core@7.24.0"
    assert babel.line == 6

    lock_exp = by_key[("package-lock.json", "express")]
    assert lock_exp.is_direct is True
    assert lock_exp.license == "MIT"

    lock_ms = by_key[("package-lock.json", "ms")]
    assert lock_ms.is_direct is False
    assert lock_ms.license == "MIT"

    pnpm_debug = by_key[("pnpm-lock.yaml", "debug")]
    assert pnpm_debug.purl == "pkg:npm/debug@4.3.4"
    assert pnpm_debug.is_direct is False

    csproj_json = by_key[("api/OrderApi.csproj", "Newtonsoft.Json")]
    assert csproj_json.purl == "pkg:nuget/Newtonsoft.Json@13.0.3"
    assert csproj_json.line == 3

    csproj_serilog = by_key[("api/OrderApi.csproj", "Serilog")]
    assert csproj_serilog.purl == "pkg:nuget/Serilog@3.1.1"
    assert csproj_serilog.line == 4

    nupkg_trans = by_key[("api/packages.lock.json", "System.Text.Encodings.Web")]
    assert nupkg_trans.is_direct is False

    pom_jackson = by_key[("billing/pom.xml", "com.fasterxml.jackson.core:jackson-databind")]
    assert pom_jackson.purl == "pkg:maven/com.fasterxml.jackson.core/jackson-databind@2.15.2"
    assert pom_jackson.line == 6

    gradle_boot = by_key[
        ("billing/build.gradle.kts", "org.springframework.boot:spring-boot-starter-web")
    ]
    assert (
        gradle_boot.purl
        == "pkg:maven/org.springframework.boot/spring-boot-starter-web@3.2.4"
    )
    assert gradle_boot.line == 2


def test_osv_offline_default_never_hits_network(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_if_called(*args: object, **kwargs: object) -> object:
        raise AssertionError("Network call must not occur when offline!")

    monkeypatch.delenv("ATRUSS_ENABLE_LIVE_OSV", raising=False)
    monkeypatch.setattr(httpx.Client, "post", fail_if_called)

    deps = [
        DependencyRecord(
            name="requests",
            version="2.31.0",
            ecosystem="PyPI",
            purl="pkg:pypi/requests@2.31.0",
            manifest_file="requirements.txt",
            line=1,
        )
    ]
    vulns = scan_dependencies_with_osv(deps, repo_dir=tmp_path)
    assert vulns == []
    assert deps[0].vulnerability_ids == []


def test_osv_scan_severity_reachability_and_cache(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        "import requests\n\ndef fetch():\n    return requests.get('https://example.org')\n",
        encoding="utf-8",
    )
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "ci.yml").write_text(
        "name: CI\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - run: pytest -v\n",
        encoding="utf-8",
    )

    deps = [
        DependencyRecord(
            name="requests",
            version="2.31.0",
            ecosystem="PyPI",
            purl="pkg:pypi/requests@2.31.0",
            manifest_file="requirements.txt",
            line=2,
        ),
        DependencyRecord(
            name="pytest",
            version="7.4.0",
            ecosystem="PyPI",
            purl="pkg:pypi/pytest@7.4.0",
            manifest_file="requirements-dev.txt",
            line=1,
        ),
        DependencyRecord(
            name="dormant-lib",
            version="0.9.0",
            ecosystem="PyPI",
            purl="pkg:pypi/dormant-lib@0.9.0",
            manifest_file="requirements.txt",
            line=5,
        ),
    ]

    captured_requests: list[dict[str, object]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/querybatch"
        body = json.loads(request.content.decode("utf-8"))
        captured_requests.append(body)
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "vulns": [
                            {
                                "id": "GHSA-9wx4-h78v-vm56",
                                "aliases": ["CVE-2024-35195"],
                                "summary": "Session verify setting persistence issue",
                                "severity": [
                                    {
                                        "type": "CVSS_V3",
                                        "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                                    }
                                ],
                                "affected": [
                                    {
                                        "package": {"purl": "pkg:pypi/requests@2.31.0"},
                                        "ranges": [
                                            {
                                                "type": "ECOSYSTEM",
                                                "events": [
                                                    {"introduced": "0"},
                                                    {"fixed": "2.32.0"},
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            }
                        ]
                    },
                    {
                        "vulns": [
                            {
                                "id": "CVE-2024-99999",
                                "summary": "CI runner argument injection",
                                "database_specific": {"severity": "MODERATE"},
                                "affected": [
                                    {
                                        "ranges": [
                                            {
                                                "type": "ECOSYSTEM",
                                                "events": [{"fixed": "8.0.0"}],
                                            }
                                        ]
                                    }
                                ],
                            }
                        ]
                    },
                    {
                        "vulns": [
                            {
                                "id": "MAL-2024-1111",
                                "summary": "Dormant supply chain package",
                                "database_specific": {"severity": "HIGH"},
                            }
                        ]
                    },
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    cache_path = tmp_path / "cache" / "osv.json"
    vulns = scan_dependencies_with_osv(
        deps,
        repo_dir=tmp_path,
        transport=transport,
        cache_path=cache_path,
    )

    assert len(captured_requests) == 1
    assert len(vulns) == 3
    assert cache_path.exists()

    by_id = {v.id: v for v in vulns}

    req_vuln = by_id["GHSA-9wx4-h78v-vm56"]
    assert req_vuln.severity == "CRITICAL"
    assert req_vuln.cvss_score == 9.8
    assert req_vuln.fixed_version == "2.32.0"
    assert req_vuln.reachability == "REACHABLE_FROM_RUNTIME"
    assert req_vuln.manifest_file == "requirements.txt"
    assert req_vuln.line == 2
    assert deps[0].vulnerability_ids == ["GHSA-9wx4-h78v-vm56"]

    ci_vuln = by_id["CVE-2024-99999"]
    assert ci_vuln.severity == "MEDIUM"
    assert ci_vuln.fixed_version == "8.0.0"
    assert ci_vuln.reachability == "REACHABLE_FROM_CI"
    assert deps[1].vulnerability_ids == ["CVE-2024-99999"]

    mal_vuln = by_id["MAL-2024-1111"]
    assert mal_vuln.severity == "HIGH"
    assert mal_vuln.reachability == "UNREACHABLE_DORMANT"
    assert deps[2].vulnerability_ids == ["MAL-2024-1111"]

    # Offline run using persisted cache must return identical findings with no network
    deps_copy = [d.model_copy(update={"vulnerability_ids": []}) for d in deps]
    cached_vulns = scan_dependencies_with_osv(
        deps_copy,
        repo_dir=tmp_path,
        transport=None,
        cache_path=cache_path,
    )
    assert [v.model_dump() for v in cached_vulns] == [v.model_dump() for v in vulns]
    assert deps_copy[0].vulnerability_ids == ["GHSA-9wx4-h78v-vm56"]


@pytest.mark.asyncio
async def test_osv_batching_limit_async_and_graceful_errors() -> None:
    batch_sizes: list[int] = []

    def batch_handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8"))
        queries = body["queries"]
        batch_sizes.append(len(queries))
        return httpx.Response(200, json={"results": [{} for _ in queries]})

    client = OSVBatchClient(transport=httpx.MockTransport(batch_handler))
    queries = [{"package": {"purl": f"pkg:pypi/pkg-{i}@1.0.0"}} for i in range(1050)]
    results = await client.aquery_batch(queries)
    assert batch_sizes == [500, 500, 50]
    assert len(results) == 1050

    # Graceful fallback on HTTP 503 and ConnectError
    def error_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "unavailable"})

    deps = [
        DependencyRecord(
            name="requests",
            version="2.31.0",
            ecosystem="PyPI",
            purl="pkg:pypi/requests@2.31.0",
            manifest_file="requirements.txt",
            line=1,
        )
    ]
    assert scan_dependencies_with_osv(deps, transport=httpx.MockTransport(error_handler)) == []

    def raise_connect(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline", request=request)

    assert scan_dependencies_with_osv(deps, transport=httpx.MockTransport(raise_connect)) == []


def test_secret_scanner_detection_gitignore_placeholders_and_redaction(tmp_path: Path) -> None:
    assert shannon_entropy("") == 0.0
    assert shannon_entropy("aaaaaaaaaaaaaaaaaaaa") == 0.0
    high_ent_token = "xK9mP2vQ" + "8wR5tY7nB4cZ1jF6hL3dS0aG"
    assert shannon_entropy(high_ent_token) > 4.5

    (tmp_path / ".gitignore").write_text(
        ".env.local\n"
        "ignored_secrets/\n"
        "*.bak\n"
        "!keep.bak\n",
        encoding="utf-8",
    )

    ignored_dir = tmp_path / "ignored_secrets"
    ignored_dir.mkdir()
    aws_key = "AKIA" + "9X8W7V6U5T4S3R2Q"
    gh_pat = "ghp_" + "AbCdEfGhIjKlMnOpQrStUvWxYz123456"
    fg_pat = "github_pat_" + "11AAAAAA0000000000_AbCdEfGhIjKlMnOpQrStUvWxYz12345"
    sk_key = "sk-" + "9X8W7V6U5T4S3R2Q1P0O9N8M7L6K5J"

    (ignored_dir / "prod.py").write_text(f'AWS_KEY = "{aws_key}"\n', encoding="utf-8")
    (tmp_path / ".env.local").write_text(f"API_SECRET={high_ent_token}\n", encoding="utf-8")
    (tmp_path / "skip.bak").write_text(f'TOKEN = "{gh_pat}"\n', encoding="utf-8")
    (tmp_path / "keep.bak").write_text(f'TOKEN = "{gh_pat}"\n', encoding="utf-8")

    # Lockfiles and binaries must be ignored even if containing high-entropy hashes
    (tmp_path / "package-lock.json").write_text(
        json.dumps({"integrity": f'"{high_ent_token}"', "secret_key": f'"{high_ent_token}"'}),
        encoding="utf-8",
    )
    (tmp_path / "image.bin").write_bytes(b"\x00\x01\x02" + aws_key.encode("utf-8"))

    aws_ex = "AKIA" + "IOSFODNN7EXAMPLE"
    dummy_gh = "ghp_" + "dummy0000000000000000000000000"
    pem_begin = "-----BEGIN " + "RSA PRIVATE KEY-----\n"
    pem_end = "-----END " + "RSA PRIVATE KEY-----\n"
    (tmp_path / "config.py").write_text(
        "# Real secrets\n"
        f'AWS_ACCESS_KEY_ID = "{aws_key}"\n'
        f'GH_TOKEN = "{fg_pat}"\n'
        f'OPENAI_API_KEY = "{sk_key}"\n'
        f'SIGNING_SECRET = "{high_ent_token}"\n'
        # Placeholders and low-entropy strings must be ignored
        f'AWS_EXAMPLE = "{aws_ex}"\n'
        f'DUMMY_TOKEN = "{dummy_gh}"\n'
        'API_KEY = "placeholder_value_9X8W7V6U5T4S3R2Q"\n'
        'ADMIN_PASSWORD = "changeme_super_secret_123456789"\n'
        'test_token = "aB3cD6eF9gH2iJ5kL8mN1oP4qR7sT0uV"\n'
        'LOW_ENTROPY_KEY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n',
        encoding="utf-8",
    )
    (tmp_path / "cert.pem").write_text(
        pem_begin
        + "MIIEowIBAAKCAQEA7p9xK9mP2vQ8wR5tY7nB4cZ1jF6hL3dS0aG\n"
        + pem_end,
        encoding="utf-8",
    )

    findings = scan_repository_secrets(tmp_path)
    assert len(findings) == 6

    files_found = {f.file_source for f in findings}
    assert ".env.local" not in files_found
    assert "ignored_secrets/prod.py" not in files_found
    assert "skip.bak" not in files_found
    assert "package-lock.json" not in files_found
    assert "image.bin" not in files_found
    assert "keep.bak" in files_found
    assert "config.py" in files_found
    assert "cert.pem" in files_found

    # Ensure raw secrets are NEVER exposed in redacted_snippet or message
    raw_secrets = [aws_key, gh_pat, fg_pat, sk_key, high_ent_token]
    for finding in findings:
        for secret in raw_secrets:
            assert secret not in finding.redacted_snippet
            assert secret[-10:] not in finding.redacted_snippet
            assert secret not in finding.message
        assert finding.start_line >= 1
        assert finding.end_line >= finding.start_line

    cert_finding = next(f for f in findings if f.file_source == "cert.pem")
    assert cert_finding.start_line == 1
    assert cert_finding.end_line == 3
    assert cert_finding.type == "PRIVATE_KEY"

    cfg_findings = [f for f in findings if f.file_source == "config.py"]
    assert [f.start_line for f in cfg_findings] == [2, 3, 4, 5]
    assert cfg_findings[3].type == "HIGH_ENTROPY_SECRET"
    assert cfg_findings[3].entropy > 4.5

    sort_keys = [
        (f.file_source, f.start_line, f.end_line, f.rule_id, f.redacted_snippet)
        for f in findings
    ]
    assert sort_keys == sorted(sort_keys)


def test_cyclonedx_16_sbom_schema_and_sha256_determinism(tmp_path: Path) -> None:
    deps = [
        DependencyRecord(
            name="requests",
            version="2.31.0",
            ecosystem="PyPI",
            purl="pkg:pypi/requests@2.31.0",
            manifest_file="requirements.txt",
            line=1,
            is_direct=True,
            license="Apache-2.0",
            vulnerability_ids=["GHSA-9wx4-h78v-vm56"],
        ),
        DependencyRecord(
            name="urllib3",
            version="2.2.1",
            ecosystem="PyPI",
            purl="pkg:pypi/urllib3@2.2.1",
            manifest_file="uv.lock",
            line=10,
            is_direct=False,
        ),
    ]
    vulns = [
        VulnerabilityRecord(
            id="GHSA-9wx4-h78v-vm56",
            package="requests",
            purl="pkg:pypi/requests@2.31.0",
            installed_version="2.31.0",
            fixed_version="2.32.0",
            severity="CRITICAL",
            cvss_score=9.8,
            summary="Verify persistence issue",
            reachability="REACHABLE_FROM_RUNTIME",
            manifest_file="requirements.txt",
            line=1,
        )
    ]

    sbom_a = build_cyclonedx_sbom("acme/pet-api", "deadbeef1234", deps, vulns)
    sbom_b = build_cyclonedx_sbom("acme/pet-api", "deadbeef1234", list(reversed(deps)), vulns)

    assert sbom_a["bomFormat"] == "CycloneDX"
    assert sbom_a["specVersion"] == "1.6"
    assert sbom_a["version"] == 1
    assert re.match(
        r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        sbom_a["serialNumber"],
    )
    assert sbom_a["metadata"]["component"]["name"] == "acme/pet-api"
    assert sbom_a["metadata"]["component"]["version"] == "deadbeef1234"
    assert len(sbom_a["components"]) == 2
    assert sbom_a["components"][0]["licenses"] == [{"license": {"id": "Apache-2.0"}}]
    assert len(sbom_a["vulnerabilities"]) == 1
    assert sbom_a["vulnerabilities"][0]["ratings"][0]["severity"] == "critical"
    assert sbom_a["vulnerabilities"][0]["ratings"][0]["score"] == 9.8
    assert sbom_a["vulnerabilities"][0]["affects"][0]["ref"] == "pkg:pypi/requests@2.31.0"

    # Gate 5 SHA-256 determinism regardless of call time or input order
    sha_a = hashlib.sha256(json.dumps(sbom_a, indent=2).encode("utf-8")).hexdigest()
    sha_b = hashlib.sha256(json.dumps(sbom_b, indent=2).encode("utf-8")).hexdigest()
    assert sha_a == sha_b

    out_file = export_cyclonedx_sbom(
        "acme/pet-api",
        "deadbeef1234",
        deps,
        vulns,
        tmp_path / "sbom" / "pet-api.cdx.json",
    )
    assert out_file.exists()
    loaded = json.loads(out_file.read_text(encoding="utf-8"))
    assert loaded == sbom_a

    out_dir_file = export_cyclonedx_sbom(
        "acme/pet-api",
        "deadbeef1234",
        deps,
        vulns,
        tmp_path / "sbom_dir",
    )
    assert out_dir_file.name == "acme-pet-api.cdx.json"
    assert json.loads(out_dir_file.read_text(encoding="utf-8")) == sbom_a


def test_additional_manifest_edge_cases(tmp_path: Path) -> None:
    # Poetry + PEP 735 dependency-groups
    py_dir = tmp_path / "py_poetry"
    py_dir.mkdir()
    (py_dir / "pyproject.toml").write_text(
        '[tool.poetry.dependencies]\n'
        'python = "^3.11"\n'
        'httpx = "^0.27.0"\n'
        '\n'
        '[tool.poetry.group.dev.dependencies]\n'
        'pytest = "^8.1.1"\n'
        '\n'
        '[dependency-groups]\n'
        'lint = ["ruff>=0.3.4"]\n',
        encoding="utf-8",
    )

    # package-lock v1 + pnpm v5 scoped package
    js_dir = tmp_path / "js_legacy"
    js_dir.mkdir()
    (js_dir / "package-lock.json").write_text(
        json.dumps(
            {
                "name": "legacy-ui",
                "lockfileVersion": 1,
                "dependencies": {
                    "lodash": {
                        "version": "4.17.21",
                        "dependencies": {
                            "nested-helper": {"version": "1.0.0"},
                        },
                    }
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (js_dir / "pnpm-lock.yaml").write_text(
        "lockfileVersion: 5.4\n"
        "dependencies:\n"
        "  '@angular/core': 17.3.0\n"
        "packages:\n"
        "  /@angular/core/17.3.0:\n"
        "    resolution: {integrity: sha512-xyz}\n"
        "  /tslib/2.6.2:\n"
        "    resolution: {integrity: sha512-uvw}\n",
        encoding="utf-8",
    )

    # Maven dependencyManagement + Groovy build.gradle map & var notation
    jvm_dir = tmp_path / "jvm"
    jvm_dir.mkdir()
    (jvm_dir / "pom.xml").write_text(
        "<project>\n"
        "  <dependencyManagement>\n"
        "    <dependencies>\n"
        "      <dependency>\n"
        "        <groupId>org.apache.commons</groupId>\n"
        "        <artifactId>commons-lang3</artifactId>\n"
        "        <version>3.14.0</version>\n"
        "      </dependency>\n"
        "    </dependencies>\n"
        "  </dependencyManagement>\n"
        "  <dependencies>\n"
        "    <dependency>\n"
        "      <groupId>org.apache.commons</groupId>\n"
        "      <artifactId>commons-lang3</artifactId>\n"
        "    </dependency>\n"
        "  </dependencies>\n"
        "</project>\n",
        encoding="utf-8",
    )
    (jvm_dir / "build.gradle").write_text(
        "def guavaVer = '33.1.0-jre'\n"
        "dependencies {\n"
        "    implementation \"com.google.guava:guava:${guavaVer}\"\n"
        "    testImplementation group: 'junit', name: 'junit', version: '4.13.2'\n"
        "}\n",
        encoding="utf-8",
    )

    deps = parse_repository_dependencies(tmp_path)
    by_key = {(d.manifest_file, d.name): d for d in deps}

    assert by_key[("py_poetry/pyproject.toml", "httpx")].version == "0.27.0"
    assert by_key[("py_poetry/pyproject.toml", "pytest")].version == "8.1.1"
    assert by_key[("py_poetry/pyproject.toml", "ruff")].version == "0.3.4"
    assert ("py_poetry/pyproject.toml", "python") not in by_key

    assert by_key[("js_legacy/package-lock.json", "lodash")].is_direct is True
    assert by_key[("js_legacy/package-lock.json", "nested-helper")].is_direct is False
    angular = by_key[("js_legacy/pnpm-lock.yaml", "@angular/core")]
    assert angular.purl == "pkg:npm/%40angular/core@17.3.0"
    assert angular.is_direct is True
    assert by_key[("js_legacy/pnpm-lock.yaml", "tslib")].is_direct is False

    pom_dep = by_key[("jvm/pom.xml", "org.apache.commons:commons-lang3")]
    assert pom_dep.version == "3.14.0"
    assert pom_dep.line == 12
    assert by_key[("jvm/build.gradle", "com.google.guava:guava")].version == "33.1.0-jre"
    assert by_key[("jvm/build.gradle", "junit:junit")].version == "4.13.2"


def test_multi_ecosystem_reachability_and_sync_batch_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "index.ts").write_text(
        "import express from 'express';\nexport const app = express();\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "OrderService.cs").write_text(
        "using Newtonsoft.Json;\npublic class OrderService {}\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "App.java").write_text(
        "import com.fasterxml.jackson.databind.ObjectMapper;\npublic class App {}\n",
        encoding="utf-8",
    )

    deps = [
        DependencyRecord(
            name="express",
            version="4.18.2",
            ecosystem="npm",
            purl="pkg:npm/express@4.18.2",
            manifest_file="package.json",
            line=3,
        ),
        DependencyRecord(
            name="Newtonsoft.Json",
            version="13.0.3",
            ecosystem="NuGet",
            purl="pkg:nuget/Newtonsoft.Json@13.0.3",
            manifest_file="App.csproj",
            line=4,
        ),
        DependencyRecord(
            name="com.fasterxml.jackson.core:jackson-databind",
            version="2.15.2",
            ecosystem="Maven",
            purl="pkg:maven/com.fasterxml.jackson.core/jackson-databind@2.15.2",
            manifest_file="pom.xml",
            line=8,
        ),
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "vulns": [
                            {
                                "id": f"CVE-2024-000{idx}",
                                "severity": [{"type": "CVSS_V3", "score": "7.5"}],
                            }
                        ]
                    }
                    for idx, _ in enumerate(body["queries"], start=1)
                ]
            },
        )

    vulns = scan_dependencies_with_osv(
        deps,
        repo_dir=tmp_path,
        transport=httpx.MockTransport(handler),
    )
    assert len(vulns) == 3
    assert all(v.reachability == "REACHABLE_FROM_RUNTIME" for v in vulns)
    assert all(v.severity == "HIGH" and v.cvss_score == 7.5 for v in vulns)

    # Verify sync OSVBatchClient context manager & chunking <= 500
    chunk_sizes: list[int] = []

    def chunk_handler(request: httpx.Request) -> httpx.Response:
        q = json.loads(request.content.decode("utf-8"))["queries"]
        chunk_sizes.append(len(q))
        return httpx.Response(200, json={"results": [{} for _ in q]})

    with OSVBatchClient(transport=httpx.MockTransport(chunk_handler)) as client:
        res = client.query_batch(
            [{"package": {"purl": f"pkg:npm/pkg-{i}@1.0.0"}} for i in range(520)]
        )
    assert chunk_sizes == [500, 20]
    assert len(res) == 520

    # Verify ATRUSS_ENABLE_LIVE_OSV=1 triggers live client path cleanly (mocked post)
    called_urls: list[str] = []

    def fake_post(self: httpx.Client, url: str, **kwargs: object) -> httpx.Response:
        called_urls.append(url)
        return httpx.Response(
            200,
            json={"results": [{"vulns": []}]},
            request=httpx.Request("POST", "https://api.osv.dev/v1/querybatch"),
        )

    monkeypatch.setenv("ATRUSS_ENABLE_LIVE_OSV", "1")
    monkeypatch.setattr(httpx.Client, "post", fake_post)
    assert scan_dependencies_with_osv([deps[0]], repo_dir=tmp_path) == []
    assert called_urls == ["/v1/querybatch"]


def test_secret_scanner_nested_gitignore_and_env_unquoted(tmp_path: Path) -> None:
    sub = tmp_path / "services"
    sub.mkdir()
    (sub / ".gitignore").write_text("local_only.env\n", encoding="utf-8")
    unquoted_secret = "mN8pQ3rS" + "6tU9vW2xY5zA8bC1dE4fG7hJ"
    (sub / "local_only.env").write_text(f"API_SECRET={unquoted_secret}\n", encoding="utf-8")
    (sub / "prod.env").write_text(f"API_SECRET={unquoted_secret}\n", encoding="utf-8")
    ec_begin = "-----BEGIN " + "EC PRIVATE KEY-----\n"
    ec_end = "-----END " + "EC PRIVATE KEY-----\n"
    (sub / "ec.key").write_text(
        ec_begin
        + "MHQCAQEEIBa7xK9mP2vQ8wR5tY7nB4cZ1\n"
        + ec_end,
        encoding="utf-8",
    )

    findings = scan_repository_secrets(tmp_path)
    files = {f.file_source for f in findings}
    assert "services/local_only.env" not in files
    assert "services/prod.env" in files
    assert "services/ec.key" in files
    for finding in findings:
        assert unquoted_secret not in finding.redacted_snippet
