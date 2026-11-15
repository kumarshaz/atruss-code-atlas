from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.models.artifacts import PortableArtifact

SARIF_SCHEMA_URL = (
    "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/"
    "sarif-schema-2.1.0.json"
)

_PIPELINE_TYPE_TO_RULE: dict[str, tuple[str, str]] = {
    "NO_TEST_GATE": (
        "ATRUSS-PIPE-001",
        "Deployment job executes without an upstream test gate in its needs chain.",
    ),
    "NO_CACHE": (
        "ATRUSS-PIPE-002",
        "Workflow installs dependencies without caching configured.",
    ),
    "NO_ARTIFACT_HANDOFF": (
        "ATRUSS-PIPE-003",
        "Multi-job build and deploy workflow lacks artifact handoff.",
    ),
    "HARDCODED_SECRET": (
        "ATRUSS-PIPE-004",
        "Potential hardcoded credential detected in workflow definition.",
    ),
    "SEQUENTIAL_ONLY": (
        "ATRUSS-PIPE-005",
        "Workflow chains jobs strictly sequentially with no parallel branches.",
    ),
    "UNFILTERED_MAIN_PUSH": (
        "ATRUSS-PIPE-006",
        "Deployment workflow triggers on push without branch or tag filters.",
    ),
    "UNLABELED_SELF_HOSTED": (
        "ATRUSS-PIPE-007",
        "Job targets self-hosted runner without constraint labels.",
    ),
    "UNPINNED_ACTION": (
        "ATRUSS-PIPE-008",
        "Third-party GitHub Action is not pinned to a 40-character commit SHA.",
    ),
    "TEMPLATE_INJECTION": (
        "ATRUSS-PIPE-009",
        "Workflow run block interpolates untrusted event context or writes to GITHUB_ENV/PATH.",
    ),
    "PWN_REQUEST_RISK": (
        "ATRUSS-PIPE-010",
        "Workflow triggers on pull_request_target and checks out untrusted PR head ref.",
    ),
    "EXCESSIVE_PERMISSIONS": (
        "ATRUSS-PIPE-011",
        "Workflow grants write-all or omits least-privilege permissions.",
    ),
    "NO_TIMEOUT": (
        "ATRUSS-PIPE-012",
        "Job omits timeout-minutes configuration.",
    ),
    "ARTIFACT_CREDENTIAL_PERSISTENCE": (
        "ATRUSS-PIPE-013",
        "actions/checkout persists git credentials in job that uploads artifacts.",
    ),
    "STATIC_CLOUD_CREDENTIALS": (
        "ATRUSS-PIPE-014",
        "Cloud authentication uses static keys instead of OIDC id-token federation.",
    ),
}

_ARCH_RULE_DESCRIPTIONS: dict[str, str] = {
    "ATRUSS-ARCH-001": "API_ROUTE directly depends on DATA_ACCESS_LAYER bypassing SERVICE.",
    "ATRUSS-ARCH-002": "UI_COMPONENT directly depends on DATA_ACCESS_LAYER.",
    "ATRUSS-ARCH-003": "DOMAIN directly depends on INFRASTRUCTURE.",
    "ATRUSS-ARCH-004": "Circular dependency detected between architectural components.",
    "ATRUSS-ARCH-005": "Code quality metric exceeds configured architectural threshold.",
}

_SEC_RULE_DESCRIPTIONS: dict[str, str] = {
    "ATRUSS-SEC-001": "Potential hardcoded AWS Access Key ID detected.",
    "ATRUSS-SEC-002": "Potential hardcoded GitHub Personal Access Token detected.",
    "ATRUSS-SEC-003": "Potential hardcoded API secret key detected.",
    "ATRUSS-SEC-004": "Private key material header detected.",
    "ATRUSS-SEC-005": "High-entropy credential candidate detected.",
}


def _map_severity_to_sarif_level(severity: str) -> str:
    sev = str(severity or "").strip().upper()
    if sev in {"CRITICAL", "HIGH", "ERROR"}:
        return "error"
    if sev in {"MEDIUM", "MODERATE", "WARNING"}:
        return "warning"
    return "note"


def _norm_uri(raw: str | None, fallback: str) -> str:
    val = str(raw or "").strip().replace("\\", "/")
    while val.startswith("./"):
        val = val[2:]
    return val or fallback


def _get_field(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def build_sarif_report(
    artifacts: PortableArtifact | list[PortableArtifact],
    findings: list[dict[str, Any]] | None = None,
    repo_name: str | None = None,
) -> dict[str, Any]:
    """
    Build a deterministic OASIS SARIF v2.1.0 report across pipeline anti-patterns,
    architectural fitness violations, secret findings, vulnerabilities, and explicit
    finding dicts without wall-clock timestamps (FR-028).
    """
    artifact_list = [artifacts] if isinstance(artifacts, PortableArtifact) else list(artifacts)

    rules_meta: dict[str, dict[str, Any]] = {}
    results_dedup: dict[tuple[str, int, int, str, str], dict[str, Any]] = {}

    def _register_rule(
        rule_id: str,
        name: str,
        description: str,
        level: str,
        category: str,
        remediation: str = "",
    ) -> None:
        if rule_id in rules_meta:
            return
        rule_obj: dict[str, Any] = {
            "id": rule_id,
            "name": name,
            "shortDescription": {"text": description or name},
            "defaultConfiguration": {"level": level},
            "properties": {"tags": ["atruss", category]},
        }
        if remediation:
            rule_obj["help"] = {"text": remediation}
        rules_meta[rule_id] = rule_obj

    def _add_result(
        rule_id: str,
        rule_name: str,
        rule_desc: str,
        severity: str,
        message: str,
        uri: str,
        start_line: int,
        end_line: int,
        category: str,
        remediation: str = "",
        repository: str = "",
    ) -> None:
        safe_start = max(1, int(start_line or 1))
        safe_end = max(safe_start, int(end_line or safe_start))
        safe_uri = _norm_uri(uri, "repository")
        level = _map_severity_to_sarif_level(severity)
        _register_rule(rule_id, rule_name, rule_desc, level, category, remediation=remediation)

        dedup_key = (safe_uri, safe_start, safe_end, rule_id, message)
        if dedup_key in results_dedup:
            return
        props: dict[str, Any] = {
            "severity": str(severity or "MEDIUM").upper(),
            "category": category,
        }
        if repository:
            props["repository"] = repository
        if remediation:
            props["remediation"] = remediation

        results_dedup[dedup_key] = {
            "ruleId": rule_id,
            "level": level,
            "message": {"text": message},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": safe_uri,
                            "uriBaseId": "%SRCROOT%",
                        },
                        "region": {
                            "startLine": safe_start,
                            "endLine": safe_end,
                        },
                    }
                }
            ],
            "properties": props,
        }

    for artifact in artifact_list:
        art_repo = repo_name or artifact.repository

        # 1. Pipeline anti-patterns (ATRUSS-PIPE-001..014)
        for wf in artifact.pipelines:
            wf_fallback = (
                _get_field(wf, "path")
                or (f".github/workflows/{_get_field(wf, 'id')}" if _get_field(wf, "id") else None)
                or ".github/workflows/workflow.yml"
            )
            for ap in _get_field(wf, "anti_patterns", []) or []:
                ap_type = str(_get_field(ap, "type", "PIPELINE_ANTIPATTERN"))
                mapped_id, mapped_desc = _PIPELINE_TYPE_TO_RULE.get(
                    ap_type, ("ATRUSS-PIPE-000", ap_type)
                )
                rule_id = str(_get_field(ap, "rule_id", "") or mapped_id)
                sev = str(_get_field(ap, "severity", "MEDIUM")).upper()
                msg = str(_get_field(ap, "message", ap_type))
                uri = _norm_uri(_get_field(ap, "file_source"), str(wf_fallback))
                s_line = int(_get_field(ap, "start_line", 1) or 1)
                e_line = int(_get_field(ap, "end_line", s_line) or s_line)
                remediation = str(_get_field(ap, "remediation", "") or "")
                _add_result(
                    rule_id=rule_id,
                    rule_name=ap_type,
                    rule_desc=mapped_desc,
                    severity=sev,
                    message=msg,
                    uri=uri,
                    start_line=s_line,
                    end_line=e_line,
                    category="pipeline",
                    remediation=remediation,
                    repository=art_repo,
                )

        # 2. Architectural fitness violations (ATRUSS-ARCH-001..005)
        for fv in artifact.fitness_violations:
            rule_id = str(_get_field(fv, "rule_id", "") or "ATRUSS-ARCH-001")
            ftype = str(_get_field(fv, "type", "LAYER_VIOLATION"))
            sev = str(_get_field(fv, "severity", "HIGH")).upper()
            msg = str(_get_field(fv, "message", ftype))
            uri = _norm_uri(_get_field(fv, "file_source"), "architecture")
            s_line = int(_get_field(fv, "start_line", 1) or 1)
            e_line = int(_get_field(fv, "end_line", s_line) or s_line)
            desc = _ARCH_RULE_DESCRIPTIONS.get(rule_id, ftype)
            _add_result(
                rule_id=rule_id,
                rule_name=ftype,
                rule_desc=desc,
                severity=sev,
                message=msg,
                uri=uri,
                start_line=s_line,
                end_line=e_line,
                category="architecture",
                repository=art_repo,
            )

        # 3. Hardcoded secrets (ATRUSS-SEC-001..005)
        for sec in artifact.secrets:
            rule_id = str(_get_field(sec, "rule_id", "") or "ATRUSS-SEC-001")
            sec_type = str(_get_field(sec, "type", "HARDCODED_SECRET"))
            sev = str(_get_field(sec, "severity", "HIGH")).upper()
            base_msg = str(_get_field(sec, "message", "") or f"Secret detected ({sec_type}).")
            redacted = str(_get_field(sec, "redacted_snippet", "") or "")
            msg = f"{base_msg} Snippet: {redacted}" if redacted else base_msg
            uri = _norm_uri(_get_field(sec, "file_source"), "repository")
            s_line = int(_get_field(sec, "start_line", 1) or 1)
            e_line = int(_get_field(sec, "end_line", s_line) or s_line)
            desc = _SEC_RULE_DESCRIPTIONS.get(rule_id, sec_type)
            _add_result(
                rule_id=rule_id,
                rule_name=sec_type,
                rule_desc=desc,
                severity=sev,
                message=msg,
                uri=uri,
                start_line=s_line,
                end_line=e_line,
                category="secret",
                remediation="Remove hardcoded credential and use secret management.",
                repository=art_repo,
            )

        # 4. Dependency vulnerabilities (ATRUSS-CVE / vuln.id)
        for vuln in artifact.vulnerabilities:
            vid = str(_get_field(vuln, "id", "") or "ATRUSS-CVE")
            pkg = str(_get_field(vuln, "package", ""))
            installed = str(_get_field(vuln, "installed_version", ""))
            fixed = str(_get_field(vuln, "fixed_version", "") or "")
            sev = str(_get_field(vuln, "severity", "MEDIUM")).upper()
            summary = str(_get_field(vuln, "summary", "") or f"Vulnerable package {pkg}")
            msg = f"[{vid}] {pkg} {installed}: {summary}".strip()
            remediation = f"Upgrade {pkg} to {fixed}." if fixed else ""
            uri = _norm_uri(_get_field(vuln, "manifest_file"), "dependencies")
            line_no = int(_get_field(vuln, "line", 1) or 1)
            _add_result(
                rule_id=vid,
                rule_name=f"VULNERABILITY_{vid}",
                rule_desc=f"Known vulnerability {vid} affecting {pkg or 'dependency'}.",
                severity=sev,
                message=msg,
                uri=uri,
                start_line=line_no,
                end_line=line_no,
                category="vulnerability",
                remediation=remediation,
                repository=art_repo,
            )

    # 5. Optional explicit finding dicts
    for item in findings or []:
        if not isinstance(item, dict):
            continue
        f_type = str(item.get("type", "FINDING"))
        fallback_id = _PIPELINE_TYPE_TO_RULE.get(f_type, ("ATRUSS-FINDING", f_type))[0]
        rule_id = str(item.get("rule_id") or fallback_id)
        sev = str(item.get("severity", "MEDIUM")).upper()
        msg = str(item.get("message", f_type))
        uri = _norm_uri(item.get("file_source") or item.get("uri"), "repository")
        s_line = int(item.get("start_line", 1) or 1)
        e_line = int(item.get("end_line", s_line) or s_line)
        remediation = str(item.get("remediation", "") or "")
        _add_result(
            rule_id=rule_id,
            rule_name=f_type,
            rule_desc=str(item.get("description") or f_type),
            severity=sev,
            message=msg,
            uri=uri,
            start_line=s_line,
            end_line=e_line,
            category=str(item.get("category", "finding")).lower(),
            remediation=remediation,
            repository=str(item.get("repository") or repo_name or ""),
        )

    sorted_rules = [rules_meta[k] for k in sorted(rules_meta.keys())]
    sorted_results = [results_dedup[k] for k in sorted(results_dedup.keys())]

    return {
        "$schema": SARIF_SCHEMA_URL,
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "atruss-code-atlas",
                        "version": "0.1.0",
                        "informationUri": "https://github.com/kumarshaz/atruss-code-atlas",
                        "rules": sorted_rules,
                    }
                },
                "results": sorted_results,
            }
        ],
    }


def export_sarif_report(
    artifacts: PortableArtifact | list[PortableArtifact],
    output_path: Path | str | None = None,
    *,
    output_dir: Path | str | None = None,
    findings: list[dict[str, Any]] | None = None,
    repo_name: str | None = None,
) -> Path:
    """
    Serialize an OASIS SARIF v2.1.0 report deterministically to `output_path`
    or `{output_dir}/{safe_repo}.sarif.json`.
    """
    artifact_list = [artifacts] if isinstance(artifacts, PortableArtifact) else list(artifacts)
    resolved_name = repo_name or (artifact_list[0].repository if artifact_list else "repository")
    safe_repo = resolved_name.replace("/", "-").replace("\\", "-")

    sarif_payload = build_sarif_report(artifacts, findings=findings, repo_name=repo_name)

    if output_path is not None:
        target = Path(output_path)
        if not target.suffix:
            target = target / f"{safe_repo}.sarif.json"
    elif output_dir is not None:
        target = Path(output_dir) / f"{safe_repo}.sarif.json"
    else:
        target = Path("exports") / "sarif" / f"{safe_repo}.sarif.json"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(sarif_payload, indent=2) + "\n", encoding="utf-8")
    return target
