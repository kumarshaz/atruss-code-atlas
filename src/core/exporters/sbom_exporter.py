from __future__ import annotations

import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any

from src.models.artifacts import DependencyRecord, VulnerabilityRecord

_CDX_SEVERITIES = frozenset({"critical", "high", "medium", "low", "info", "none", "unknown"})
_SPDX_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+-]*$")


def _deterministic_serial_number(
    repo_name: str,
    sha: str,
    dependencies: list[DependencyRecord],
) -> str:
    """Compute a deterministic CycloneDX URN UUID from SHA-256 of repo + sha + sorted PURLs."""
    sorted_purls = sorted({d.purl for d in dependencies if d.purl})
    seed = "|".join([repo_name, sha, *sorted_purls])
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    deterministic_uuid = uuid.UUID(bytes=digest[:16], version=4)
    return f"urn:uuid:{deterministic_uuid}"


def _component_bom_ref(dep: DependencyRecord) -> str:
    if dep.purl:
        return dep.purl
    ver = f"@{dep.version}" if dep.version else ""
    return f"pkg:{dep.ecosystem.lower()}/{dep.name}{ver}"


def _license_entry(raw_license: str) -> dict[str, Any]:
    cleaned = raw_license.strip()
    if _SPDX_ID_RE.match(cleaned):
        return {"license": {"id": cleaned}}
    return {"license": {"name": cleaned}}


def _cdx_severity(raw_severity: str) -> str:
    low = raw_severity.strip().lower()
    if low == "moderate":
        return "medium"
    return low if low in _CDX_SEVERITIES else "unknown"


def build_cyclonedx_sbom(
    repo_name: str,
    sha: str,
    dependencies: list[DependencyRecord],
    vulnerabilities: list[VulnerabilityRecord],
) -> dict[str, Any]:
    """
    Build a deterministic CycloneDX v1.6 JSON BOM dictionary from parsed dependencies
    and OSV vulnerability findings without wall-clock timestamps.
    """
    safe_sha = sha or "unknown"
    root_ref = (
        f"pkg:github/{repo_name}@{safe_sha}"
        if "/" in repo_name
        else f"app:{repo_name}@{safe_sha}"
    )

    grouped: dict[str, dict[str, Any]] = {}
    sorted_deps = sorted(
        dependencies,
        key=lambda d: (d.purl, d.name, d.version, d.manifest_file, d.line),
    )
    for dep in sorted_deps:
        ref = _component_bom_ref(dep)
        existing = grouped.get(ref)
        if existing is None:
            grouped[ref] = {
                "ref": ref,
                "name": dep.name,
                "version": dep.version,
                "ecosystem": dep.ecosystem,
                "purl": dep.purl,
                "is_direct": dep.is_direct,
                "license": dep.license,
                "manifests": {dep.manifest_file} if dep.manifest_file else set(),
            }
        else:
            existing["is_direct"] = existing["is_direct"] or dep.is_direct
            if not existing["version"] and dep.version:
                existing["version"] = dep.version
            if not existing["license"] and dep.license:
                existing["license"] = dep.license
            if dep.manifest_file:
                existing["manifests"].add(dep.manifest_file)

    components: list[dict[str, Any]] = []
    direct_refs: list[str] = []
    all_refs: list[str] = []

    for ref in sorted(grouped):
        item = grouped[ref]
        all_refs.append(ref)
        if item["is_direct"]:
            direct_refs.append(ref)

        comp: dict[str, Any] = {
            "type": "library",
            "bom-ref": ref,
            "name": item["name"],
        }
        if item["version"]:
            comp["version"] = item["version"]
        if item["purl"]:
            comp["purl"] = item["purl"]
        comp["scope"] = "required" if item["is_direct"] else "optional"
        if item["license"]:
            comp["licenses"] = [_license_entry(item["license"])]
        comp["properties"] = [
            {"name": "atruss:ecosystem", "value": item["ecosystem"]},
            {"name": "atruss:is_direct", "value": "true" if item["is_direct"] else "false"},
            {
                "name": "atruss:manifest_files",
                "value": ",".join(sorted(item["manifests"])),
            },
        ]
        components.append(comp)

    dep_graph: list[dict[str, Any]] = [
        {"ref": root_ref, "dependsOn": sorted(direct_refs)},
        *[{"ref": ref, "dependsOn": []} for ref in sorted(all_refs)],
    ]

    cdx_vulns: list[dict[str, Any]] = []
    seen_vulns: set[tuple[str, str]] = set()
    for vuln in sorted(
        vulnerabilities,
        key=lambda v: (v.id, v.purl, v.manifest_file, v.line),
    ):
        target_ref = vuln.purl if vuln.purl in grouped else (
            vuln.purl or f"pkg:unknown/{vuln.package}"
        )
        dedup_key = (vuln.id, target_ref)
        if dedup_key in seen_vulns:
            continue
        seen_vulns.add(dedup_key)

        rating: dict[str, Any] = {"severity": _cdx_severity(vuln.severity)}
        if vuln.cvss_score is not None:
            rating["score"] = vuln.cvss_score
            rating["method"] = "CVSSv3"

        affect_entry: dict[str, Any] = {"ref": target_ref}
        if vuln.installed_version:
            affect_entry["versions"] = [
                {"version": vuln.installed_version, "status": "affected"}
            ]

        props: list[dict[str, str]] = [
            {"name": "atruss:reachability", "value": vuln.reachability},
        ]
        if vuln.fixed_version:
            props.append({"name": "atruss:fixed_version", "value": vuln.fixed_version})
        if vuln.manifest_file:
            props.append({"name": "atruss:manifest_file", "value": vuln.manifest_file})

        vuln_obj: dict[str, Any] = {
            "id": vuln.id,
            "source": {
                "name": "OSV",
                "url": f"https://osv.dev/vulnerability/{vuln.id}",
            },
            "ratings": [rating],
            "affects": [affect_entry],
            "properties": props,
        }
        if vuln.summary:
            vuln_obj["description"] = vuln.summary
        if vuln.fixed_version:
            vuln_obj["recommendation"] = (
                f"Upgrade {vuln.package} to version {vuln.fixed_version} or later."
            )
        cdx_vulns.append(vuln_obj)

    return {
        "$schema": "http://cyclonedx.org/schema/bom-1.6.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": _deterministic_serial_number(repo_name, safe_sha, dependencies),
        "version": 1,
        "metadata": {
            "tools": {
                "components": [
                    {
                        "type": "application",
                        "name": "atruss-code-atlas",
                        "version": "0.1.0",
                    }
                ]
            },
            "component": {
                "type": "application",
                "bom-ref": root_ref,
                "name": repo_name,
                "version": safe_sha,
            },
        },
        "components": components,
        "dependencies": dep_graph,
        "vulnerabilities": cdx_vulns,
    }


def export_cyclonedx_sbom(
    repo_name: str,
    sha: str,
    dependencies: list[DependencyRecord],
    vulnerabilities: list[VulnerabilityRecord],
    output_path: Path | str | None = None,
    *,
    output_dir: Path | str | None = None,
) -> Path:
    """
    Serialize a deterministic CycloneDX v1.6 SBOM JSON artifact to `output_path`
    (or `{output_dir}/{safe_repo}.cdx.json` when a directory is supplied).
    """
    sbom = build_cyclonedx_sbom(repo_name, sha, dependencies, vulnerabilities)
    safe_repo = repo_name.replace("/", "-").replace("\\", "-")

    if output_path is not None:
        target = Path(output_path)
        if target.suffix.lower() != ".json":
            target = target / f"{safe_repo}.cdx.json"
    elif output_dir is not None:
        target = Path(output_dir) / f"{safe_repo}.cdx.json"
    else:
        target = Path("exports") / "sbom" / f"{safe_repo}.cdx.json"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(sbom, indent=2) + "\n", encoding="utf-8")
    return target


class SBOMExporter:
    """Thin wrapper around CycloneDX v1.6 SBOM builder and JSON file exporter."""

    def build(
        self,
        repo_name: str,
        sha: str,
        dependencies: list[DependencyRecord],
        vulnerabilities: list[VulnerabilityRecord],
    ) -> dict[str, Any]:
        return build_cyclonedx_sbom(repo_name, sha, dependencies, vulnerabilities)

    def export(
        self,
        repo_name: str,
        sha: str,
        dependencies: list[DependencyRecord],
        vulnerabilities: list[VulnerabilityRecord],
        output_path: Path | str,
    ) -> Path:
        return export_cyclonedx_sbom(repo_name, sha, dependencies, vulnerabilities, output_path)
