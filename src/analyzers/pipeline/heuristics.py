import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import networkx as nx
import yaml

from src.analyzers.pipeline.parser import _extract_workflow_line_spans, extract_triggers

_DEFAULT_RULES_PATH = Path(__file__).resolve().parents[3] / "manifests" / "pipeline-rules.yaml"
_DEFAULT_FILE_SOURCE = ".github/workflows/workflow.yml"

_DEPLOY_KEYWORDS = ("deploy", "publish", "release", "cd", "rollout", "promote")
_TEST_KEYWORDS = ("test", "pytest", "jest", "vitest", "junit", "spec", "check", "verify", "e2e")
_INSTALL_CMD_PATTERNS = (
    r"\bpip\s+install\b",
    r"\buv\s+(pip|sync)\b",
    r"\bpoetry\s+install\b",
    r"\bnpm\s+(ci|install)\b",
    r"\byarn\s+install\b",
    r"\bpnpm\s+install\b",
    r"\bdotnet\s+(restore|build|test)\b",
    r"\bmvn\b",
    r"\bgradle\b",
    r"\./gradlew\b",
)
_CACHE_SETUP_ACTIONS = (
    "actions/cache",
    "actions/setup-node",
    "actions/setup-python",
    "actions/setup-java",
    "actions/setup-dotnet",
    "actions/setup-go",
)
_SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(password|secret|api_key|access_token)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{12,}"),
)
_DEPLOY_ACTION_PREFIXES = (
    "actions/deploy-pages",
    "azure/",
    "aws-actions/",
    "google-github-actions/deploy",
    "docker/build-push-action",
)
_SHA40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_UNTRUSTED_GHA_EXPR_RE = re.compile(
    r"\$\{\{[^}]*\b(?:"
    r"github\.event\.issue\b"
    r"|github\.event\.pull_request\b"
    r"|github\.event\.comment\b"
    r"|github\.event\.review(?:_comment)?\b"
    r"|github\.event\.discussion\b"
    r"|github\.event\.pages\b"
    r"|github\.head_ref\b"
    r")[^}]*\}\}",
    re.IGNORECASE,
)
_GITHUB_ENV_PATH_WRITE_RE = re.compile(
    r"(?:>>?|tee(?:\s+-a)?)\s*['\"]?\$\{?GITHUB_(?:ENV|PATH)\}?['\"]?",
    re.IGNORECASE,
)
_GITHUB_ENV_PATH_TOKEN_RE = re.compile(r"['\"]?\$\{?GITHUB_(?:ENV|PATH)\}?['\"]?", re.IGNORECASE)
_SHELL_INTERPOLATION_RE = re.compile(r"\$\{\{|\$\(|`|\$[A-Za-z_0-9{]")
_CLOUD_LOGIN_PREFIXES = ("aws-actions/", "azure/login", "google-github-actions/auth")
_STATIC_CLOUD_WITH_KEYS = frozenset(
    {"aws-access-key-id", "aws-secret-access-key", "creds", "credentials_json"}
)
_STATIC_CLOUD_SECRET_RE = re.compile(
    r"secrets\.(?:"
    r"AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN"
    r"|AZURE_CREDENTIALS|AZURE_CLIENT_SECRET|ARM_CLIENT_SECRET"
    r"|GCP_SA_KEY|GCP_CREDENTIALS|GCP_SERVICE_ACCOUNT_KEY"
    r"|GOOGLE_CREDENTIALS|GOOGLE_APPLICATION_CREDENTIALS"
    r")\b",
    re.IGNORECASE,
)

_FALLBACK_RULES: tuple[dict[str, Any], ...] = (
    {
        "rule_id": "ATRUSS-PIPE-001",
        "type": "NO_TEST_GATE",
        "default_severity": "CRITICAL",
        "enabled": True,
        "remediation": "Add a 'needs:' dependency on a test job before deployment.",
    },
    {
        "rule_id": "ATRUSS-PIPE-002",
        "type": "NO_CACHE",
        "default_severity": "MEDIUM",
        "enabled": True,
        "remediation": "Enable setup-* caching or add an explicit actions/cache step.",
    },
    {
        "rule_id": "ATRUSS-PIPE-003",
        "type": "NO_ARTIFACT_HANDOFF",
        "default_severity": "MEDIUM",
        "enabled": True,
        "remediation": "Publish immutable artifacts with actions/upload-artifact before deploy.",
    },
    {
        "rule_id": "ATRUSS-PIPE-004",
        "type": "HARDCODED_SECRET",
        "default_severity": "CRITICAL",
        "enabled": True,
        "remediation": "Use GitHub Secrets or OIDC federation instead of literal credentials.",
    },
    {
        "rule_id": "ATRUSS-PIPE-005",
        "type": "SEQUENTIAL_ONLY",
        "default_severity": "LOW",
        "enabled": True,
        "remediation": "Parallelize independent lint, test, and scan jobs.",
    },
    {
        "rule_id": "ATRUSS-PIPE-006",
        "type": "UNFILTERED_MAIN_PUSH",
        "default_severity": "HIGH",
        "enabled": True,
        "remediation": "Restrict push triggers with explicit 'branches:' or 'tags:' filters.",
    },
    {
        "rule_id": "ATRUSS-PIPE-007",
        "type": "UNLABELED_SELF_HOSTED",
        "default_severity": "MEDIUM",
        "enabled": True,
        "remediation": "Add capability labels to 'self-hosted' runner targets.",
    },
    {
        "rule_id": "ATRUSS-PIPE-008",
        "type": "UNPINNED_ACTION",
        "default_severity": "HIGH",
        "enabled": True,
        "trusted_action_owners": ["actions"],
        "remediation": "Pin third-party actions to a full 40-character commit SHA.",
    },
    {
        "rule_id": "ATRUSS-PIPE-009",
        "type": "TEMPLATE_INJECTION",
        "default_severity": "CRITICAL",
        "enabled": True,
        "remediation": (
            "Pass untrusted context through step 'env:' and sanitize $GITHUB_ENV/$GITHUB_PATH."
        ),
    },
    {
        "rule_id": "ATRUSS-PIPE-010",
        "type": "PWN_REQUEST_RISK",
        "default_severity": "CRITICAL",
        "enabled": True,
        "remediation": "Do not check out untrusted PR head refs under pull_request_target.",
    },
    {
        "rule_id": "ATRUSS-PIPE-011",
        "type": "EXCESSIVE_PERMISSIONS",
        "default_severity": "HIGH",
        "enabled": True,
        "remediation": "Declare least-privilege 'permissions:' (e.g., contents: read).",
    },
    {
        "rule_id": "ATRUSS-PIPE-012",
        "type": "NO_TIMEOUT",
        "default_severity": "LOW",
        "enabled": True,
        "remediation": "Set explicit 'timeout-minutes:' on every job.",
    },
    {
        "rule_id": "ATRUSS-PIPE-013",
        "type": "ARTIFACT_CREDENTIAL_PERSISTENCE",
        "default_severity": "MEDIUM",
        "enabled": True,
        "remediation": "Set 'with: persist-credentials: false' on actions/checkout.",
    },
    {
        "rule_id": "ATRUSS-PIPE-014",
        "type": "STATIC_CLOUD_CREDENTIALS",
        "default_severity": "HIGH",
        "enabled": True,
        "remediation": "Use OIDC federation with 'permissions: id-token: write'.",
    },
)


@lru_cache(maxsize=8)
def _load_rules_cached(resolved_path: str, mtime_ns: int) -> dict[str, Any]:
    with open(resolved_path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data if isinstance(data, dict) else {}


def load_pipeline_rules(policy_path: Path | str | None = None) -> dict[str, Any]:
    """Load externalized Policy-as-Code pipeline rules from `manifests/pipeline-rules.yaml`."""
    env_override = os.getenv("ATRUSS_PIPELINE_RULES")
    target = Path(policy_path or env_override or _DEFAULT_RULES_PATH).resolve()
    if not target.exists():
        raise FileNotFoundError(f"Pipeline rules manifest not found at: {target}")
    stat = target.stat()
    return _load_rules_cached(str(target), stat.st_mtime_ns)


def _resolve_rule_registry(
    policy: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    rules_list = policy.get("rules")
    explicit_empty = isinstance(rules_list, list) and len(rules_list) == 0

    registry: dict[str, dict[str, Any]] = {}
    if not explicit_empty:
        for base in _FALLBACK_RULES:
            registry[base["type"]] = dict(base)

    if isinstance(rules_list, list):
        for entry in rules_list:
            if not isinstance(entry, dict):
                continue
            rule_type = str(entry.get("type", "")).strip()
            if not rule_type:
                continue
            merged = dict(registry.get(rule_type, {}))
            merged.update(entry)
            registry[rule_type] = merged

    top_owners = policy.get("trusted_action_owners")
    pipe_008 = registry.get("UNPINNED_ACTION", {})
    rule_owners = pipe_008.get("trusted_action_owners")

    if isinstance(rule_owners, list) and rule_owners != ["actions"]:
        chosen_owners = rule_owners
    elif isinstance(top_owners, list):
        chosen_owners = top_owners
    elif isinstance(rule_owners, list):
        chosen_owners = rule_owners
    else:
        chosen_owners = ["actions"]

    trusted_owners = {str(owner).strip().lower() for owner in chosen_owners if str(owner).strip()}
    return registry, trusted_owners


def _is_deploy_job(job_id: str, job_data: dict[str, Any]) -> bool:
    label = f"{job_id} {job_data.get('name', '')}".lower()
    if any(kw in label for kw in _DEPLOY_KEYWORDS):
        return True
    if job_data.get("environment"):
        return True
    for step in job_data.get("steps", []) if isinstance(job_data.get("steps"), list) else []:
        if not isinstance(step, dict):
            continue
        uses = str(step.get("uses", "")).lower()
        if any(prefix in uses for prefix in _DEPLOY_ACTION_PREFIXES):
            return True
    return False


def _is_test_job(job_id: str, job_data: dict[str, Any]) -> bool:
    label = f"{job_id} {job_data.get('name', '')}".lower()
    if any(kw in label for kw in _TEST_KEYWORDS):
        return True
    for step in job_data.get("steps", []) if isinstance(job_data.get("steps"), list) else []:
        if not isinstance(step, dict):
            continue
        run_cmd = str(step.get("run", "")).lower()
        test_cmds = (
            "pytest",
            "npm test",
            "dotnet test",
            "mvn test",
            "gradle test",
            "jest",
            "vitest",
        )
        if any(kw in run_cmd for kw in test_cmds):
            return True
    return False


def find_untested_deployments(G: nx.DiGraph) -> list[str]:
    """Flags deployment jobs that don't depend on an upstream test/build job."""
    findings: list[str] = []
    for node in G.nodes:
        node_data = dict(G.nodes[node])
        if _is_deploy_job(str(node), node_data):
            ancestors = nx.ancestors(G, node) if node in G else set()
            if not ancestors:
                findings.append(
                    f"CRITICAL: Job '{node}' performs deployment without upstream "
                    "test gates ('needs:' block is empty)."
                )
            else:
                has_test_ancestor = any(
                    _is_test_job(str(anc), dict(G.nodes[anc])) for anc in ancestors
                )
                if not has_test_ancestor and not _is_test_job(str(node), node_data):
                    findings.append(
                        f"HIGH: Job '{node}' performs deployment without an upstream "
                        "test job in its 'needs:' chain."
                    )
    return findings


def find_missing_caches(workflow_data: dict[str, Any]) -> list[str]:
    """Flags workflows that install/build dependencies without dependency caching."""
    findings: list[str] = []
    has_install_step = False
    has_cache = False

    jobs = workflow_data.get("jobs", {})
    if not isinstance(jobs, dict):
        return findings

    for _job_id, job in jobs.items():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps", [])
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", ""))
            with_cfg = step.get("with", {}) if isinstance(step.get("with"), dict) else {}
            if "actions/cache" in uses:
                has_cache = True
            if any(act in uses for act in _CACHE_SETUP_ACTIONS) and with_cfg.get("cache"):
                has_cache = True
            run_cmd = str(step.get("run", ""))
            if run_cmd and any(re.search(pat, run_cmd) for pat in _INSTALL_CMD_PATTERNS):
                has_install_step = True

    if has_install_step and not has_cache:
        findings.append(
            "MEDIUM: Workflow installs dependencies without 'actions/cache' "
            "or setup action caching."
        )

    return findings


def _find_first_install_line_keys(workflow_data: dict[str, Any]) -> tuple[str, ...]:
    jobs = workflow_data.get("jobs", {})
    if not isinstance(jobs, dict):
        return ("top:jobs",)
    for jid, job in jobs.items():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps", [])
        if not isinstance(steps, list):
            continue
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            run_cmd = str(step.get("run", ""))
            if run_cmd and any(re.search(pat, run_cmd) for pat in _INSTALL_CMD_PATTERNS):
                return (
                    f"job:{jid}:step:{idx}:run",
                    f"job:{jid}:step:{idx}",
                    f"job:{jid}",
                    "top:jobs",
                )
    return ("top:jobs",)


def _check_secret_exposure(
    workflow_data: dict[str, Any],
) -> list[tuple[tuple[str, ...], str]]:
    findings: list[tuple[tuple[str, ...], str]] = []

    def _scan_env(env_map: Any, scope: str, prefix: str, fallbacks: tuple[str, ...]) -> None:
        if not isinstance(env_map, dict):
            return
        for key, val in env_map.items():
            val_str = str(val)
            if "${{" in val_str:
                continue
            if any(p in val_str.lower() for p in ("example", "dummy", "placeholder", "changeme")):
                continue
            key_upper = str(key).upper()
            secret_tokens = ("SECRET", "TOKEN", "PASSWORD", "API_KEY", "PRIVATE_KEY")
            is_sensitive_key = any(t in key_upper for t in secret_tokens)
            line_keys = (f"{prefix}:{key}", prefix, *fallbacks)
            if is_sensitive_key and len(val_str.strip()) >= 8:
                findings.append(
                    (
                        line_keys,
                        f"Potential hardcoded credential in {scope} env '{key}'. "
                        "Use GitHub Secrets instead.",
                    )
                )
            elif any(pat.search(val_str) for pat in _SECRET_PATTERNS):
                findings.append(
                    (
                        line_keys,
                        f"Potential hardcoded token pattern in {scope} env '{key}'.",
                    )
                )

    _scan_env(workflow_data.get("env"), "workflow", "top:env", ())
    jobs = workflow_data.get("jobs", {})
    if isinstance(jobs, dict):
        for job_id, job in jobs.items():
            if not isinstance(job, dict):
                continue
            _scan_env(job.get("env"), f"job '{job_id}'", f"job:{job_id}:env", (f"job:{job_id}",))
            steps = job.get("steps", [])
            if not isinstance(steps, list):
                continue
            for idx, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                step_prefix = f"job:{job_id}:step:{idx}"
                _scan_env(
                    step.get("env"),
                    f"job '{job_id}' step",
                    f"{step_prefix}:env",
                    (step_prefix, f"job:{job_id}"),
                )
                run_str = str(step.get("run", ""))
                if "${{" not in run_str and any(pat.search(run_str) for pat in _SECRET_PATTERNS):
                    findings.append(
                        (
                            (f"{step_prefix}:run", step_prefix, f"job:{job_id}"),
                            f"Potential hardcoded secret detected in run script of job '{job_id}'.",
                        )
                    )
    return findings


_MULTILINE_BRACE_ENV_RE = re.compile(
    r"\{([^}]+)\}\s*>>?\s*['\"]?\$\{?GITHUB_(?:ENV|PATH)\}?['\"]?",
    re.DOTALL | re.IGNORECASE,
)
_HEREDOC_ENV_RE = re.compile(
    r"(?:>>?\s*['\"]?\$\{?GITHUB_(?:ENV|PATH)\}?['\"]?[^\n]*<<-?\s*['\"]?([A-Za-z0-9_]+)['\"]?"
    r"|<<-?\s*['\"]?([A-Za-z0-9_]+)['\"]?[^\n]*>>?\s*['\"]?\$\{?GITHUB_(?:ENV|PATH)\}?['\"]?)"
    r"\n(.*?)\n\s*(?:\1|\2)\b",
    re.DOTALL | re.IGNORECASE,
)


def _writes_untrusted_to_github_env_or_path(run_str: str) -> bool:
    if not _GITHUB_ENV_PATH_WRITE_RE.search(run_str):
        return False

    for line in run_str.splitlines():
        if _GITHUB_ENV_PATH_WRITE_RE.search(line):
            cleaned = _GITHUB_ENV_PATH_TOKEN_RE.sub("", line)
            if _SHELL_INTERPOLATION_RE.search(cleaned):
                return True

    for match in _MULTILINE_BRACE_ENV_RE.finditer(run_str):
        if _SHELL_INTERPOLATION_RE.search(match.group(1)):
            return True

    for match in _HEREDOC_ENV_RE.finditer(run_str):
        if _SHELL_INTERPOLATION_RE.search(match.group(3)):
            return True

    return False


def _is_write_all_permission(perms: Any) -> bool:
    return isinstance(perms, str) and perms.strip().lower() == "write-all"


def _is_least_privilege_permission(perms: Any) -> bool:
    if isinstance(perms, dict):
        return True
    return isinstance(perms, str) and perms.strip().lower() == "read-all"


def _has_id_token_write(wf_perms: Any, job_perms: Any) -> bool:
    effective = job_perms if job_perms is not None else wf_perms
    return isinstance(effective, dict) and str(effective.get("id-token", "")).strip().lower() == (
        "write"
    )


def _find_static_cloud_secret_key(env_map: Any) -> str | None:
    if not isinstance(env_map, dict):
        return None
    for key, val in env_map.items():
        if _STATIC_CLOUD_SECRET_RE.search(str(val)):
            return str(key)
    return None


def analyze_workflow_anti_patterns(
    workflow_data: dict[str, Any],
    G: nx.DiGraph,
    file_source: str | None = None,
    raw_yaml: str | None = None,
    policy_path: Path | str | None = None,
) -> list[dict[str, Any]]:
    """
    Evaluate all 14 Policy-as-Code CI/CD anti-patterns & supply-chain security rules
    (ATRUSS-PIPE-001 through ATRUSS-PIPE-014) for a parsed GitHub Actions workflow.
    Returns clean JSON-serializable finding dicts with line numbers and remediation.
    """
    policy = load_pipeline_rules(policy_path)
    registry, trusted_owners = _resolve_rule_registry(policy)

    if raw_yaml:
        start_map, end_map = _extract_workflow_line_spans(raw_yaml)
    else:
        start_map, end_map = {}, {}

    resolved_file = (
        file_source.strip()
        if isinstance(file_source, str) and file_source.strip()
        else _DEFAULT_FILE_SOURCE
    )

    def _resolve_span(*keys: str) -> tuple[int, int]:
        for key in keys:
            if key in start_map:
                s_line = max(1, int(start_map[key]))
                e_line = max(s_line, int(end_map.get(key, s_line)))
                return s_line, e_line
        return 1, 1

    results: list[dict[str, Any]] = []

    def _emit(
        rule_type: str,
        message: str,
        *line_keys: str,
        severity_override: str | None = None,
    ) -> None:
        rule = registry.get(rule_type)
        if not rule or not bool(rule.get("enabled", True)):
            return
        start_line, end_line = _resolve_span(*line_keys)
        severity = severity_override or str(rule.get("default_severity", "MEDIUM"))
        remediation = str(rule.get("remediation", "")).strip()
        results.append(
            {
                "rule_id": str(rule.get("rule_id", "")),
                "type": str(rule.get("type", rule_type)),
                "severity": severity,
                "message": message,
                "entity_type": "PIPELINE",
                "file_source": resolved_file,
                "start_line": start_line,
                "end_line": end_line,
                "remediation": remediation,
            }
        )

    jobs = workflow_data.get("jobs", {})
    if not isinstance(jobs, dict):
        jobs = {}

    # 1. ATRUSS-PIPE-001: No test gate before deploy
    pipe_001_default = str(registry.get("NO_TEST_GATE", {}).get("default_severity", "CRITICAL"))
    for msg in find_untested_deployments(G):
        if msg.startswith("CRITICAL"):
            sev = pipe_001_default
        else:
            sev = "HIGH" if pipe_001_default == "CRITICAL" else pipe_001_default
        match = re.search(r"Job '([^']+)'", msg)
        line_key = f"job:{match.group(1)}" if match else "top:jobs"
        _emit("NO_TEST_GATE", msg, line_key, "top:jobs", severity_override=sev)

    # 2. ATRUSS-PIPE-002: No dependency caching
    for msg in find_missing_caches(workflow_data):
        _emit("NO_CACHE", msg, *_find_first_install_line_keys(workflow_data))

    # 3. ATRUSS-PIPE-003: No artifact handoff when build + deploy jobs exist
    deploy_job_ids = [
        str(jid)
        for jid, jdata in jobs.items()
        if isinstance(jdata, dict) and _is_deploy_job(str(jid), jdata)
    ]
    has_deploy = bool(deploy_job_ids)
    has_upload = False
    for jdata in jobs.values():
        if not isinstance(jdata, dict):
            continue
        for step in jdata.get("steps", []) if isinstance(jdata.get("steps"), list) else []:
            if isinstance(step, dict):
                uses = str(step.get("uses", "")).lower()
                if (
                    "upload-artifact" in uses
                    or "upload-pages-artifact" in uses
                    or "build-push-action" in uses
                ):
                    has_upload = True
    if has_deploy and len(jobs) >= 2 and not has_upload:
        _emit(
            "NO_ARTIFACT_HANDOFF",
            "Workflow has build and deploy stages without artifact handoff "
            "(upload-artifact / container push).",
            f"job:{deploy_job_ids[0]}",
            "top:jobs",
        )

    # 4. ATRUSS-PIPE-004: Hardcoded secrets
    for line_keys, msg in _check_secret_exposure(workflow_data):
        _emit("HARDCODED_SECRET", msg, *line_keys)

    # 5. ATRUSS-PIPE-005: Fully sequential pipeline (>= 3 jobs in linear chain)
    if G.number_of_nodes() >= 3 and nx.is_directed_acyclic_graph(G):
        longest = nx.dag_longest_path_length(G)
        if G.number_of_edges() == G.number_of_nodes() - 1 and longest == G.number_of_nodes() - 1:
            _emit(
                "SEQUENTIAL_ONLY",
                f"Workflow executes {G.number_of_nodes()} jobs strictly sequentially "
                "with zero parallel branches.",
                "top:jobs",
            )

    # 6. ATRUSS-PIPE-006: No branch protection filter on deploy-capable push trigger
    raw_on = workflow_data.get("on", workflow_data.get(True))
    if has_deploy and isinstance(raw_on, dict) and "push" in raw_on:
        push_cfg = raw_on.get("push")
        no_filters = isinstance(push_cfg, dict) and not (
            push_cfg.get("branches") or push_cfg.get("tags")
        )
        if push_cfg is None or no_filters:
            _emit(
                "UNFILTERED_MAIN_PUSH",
                "Deployment workflow triggers on 'push' without branch or tag filters.",
                "top:on:push",
                "top:on",
            )
    elif has_deploy and (raw_on == "push" or (isinstance(raw_on, list) and "push" in raw_on)):
        _emit(
            "UNFILTERED_MAIN_PUSH",
            "Deployment workflow triggers on unfiltered 'push' event.",
            "top:on",
        )

    # 7. ATRUSS-PIPE-007: Unlabeled self-hosted runner
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        runs_on = jdata.get("runs-on")
        if runs_on == "self-hosted" or (isinstance(runs_on, list) and runs_on == ["self-hosted"]):
            _emit(
                "UNLABELED_SELF_HOSTED",
                f"Job '{jid}' targets 'self-hosted' without constraint labels.",
                f"job:{jid}:runs-on",
                f"job:{jid}",
            )

    # 8. ATRUSS-PIPE-008: Unpinned third-party actions
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        steps = jdata.get("steps", [])
        if not isinstance(steps, list):
            continue
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", "")).strip()
            if not uses or uses.startswith(("./", ".\\", "docker://")):
                continue
            if "@" in uses:
                action_part, ref = uses.rsplit("@", 1)
            else:
                action_part, ref = uses, ""
            owner = action_part.split("/", 1)[0].strip().lower() if "/" in action_part else ""
            if owner in trusted_owners:
                continue
            if not _SHA40_RE.fullmatch(ref.strip()):
                _emit(
                    "UNPINNED_ACTION",
                    f"Job '{jid}' step {idx + 1} uses unpinned action '{uses}'. "
                    "Pin to a 40-character commit SHA.",
                    f"job:{jid}:step:{idx}:uses",
                    f"job:{jid}:step:{idx}",
                    f"job:{jid}",
                )

    # 9. ATRUSS-PIPE-009: Template injection via untrusted context or $GITHUB_ENV/$GITHUB_PATH
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        steps = jdata.get("steps", [])
        if not isinstance(steps, list):
            continue
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            run_str = str(step.get("run", ""))
            if not run_str:
                continue
            has_untrusted_expr = bool(_UNTRUSTED_GHA_EXPR_RE.search(run_str))
            has_env_write = _writes_untrusted_to_github_env_or_path(run_str)
            if has_untrusted_expr or has_env_write:
                _emit(
                    "TEMPLATE_INJECTION",
                    f"Job '{jid}' step {idx + 1} interpolates untrusted event context "
                    "or writes untrusted data to $GITHUB_ENV/$GITHUB_PATH.",
                    f"job:{jid}:step:{idx}:run",
                    f"job:{jid}:step:{idx}",
                    f"job:{jid}",
                )

    # 10. ATRUSS-PIPE-010: Pwn request risk (pull_request_target + checkout PR head)
    triggers = extract_triggers(workflow_data)
    if "pull_request_target" in triggers:
        for jid, jdata in jobs.items():
            if not isinstance(jdata, dict):
                continue
            steps = jdata.get("steps", [])
            if not isinstance(steps, list):
                continue
            for idx, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                uses = str(step.get("uses", "")).lower()
                if "actions/checkout" not in uses:
                    continue
                with_cfg = step.get("with", {})
                if not isinstance(with_cfg, dict):
                    continue
                ref_val = str(with_cfg.get("ref", ""))
                if "github.event.pull_request.head" in ref_val or "github.head_ref" in ref_val:
                    _emit(
                        "PWN_REQUEST_RISK",
                        f"Job '{jid}' triggers on 'pull_request_target' and checks out "
                        f"untrusted PR head ref '{ref_val}'.",
                        f"job:{jid}:step:{idx}:with:ref",
                        f"job:{jid}:step:{idx}:uses",
                        f"job:{jid}:step:{idx}",
                        f"job:{jid}",
                        "top:on:pull_request_target",
                        "top:on",
                    )

    # 11. ATRUSS-PIPE-011: Excessive or omitted permissions
    if jobs:
        has_top_perms = (
            "permissions" in workflow_data and workflow_data.get("permissions") is not None
        )
        top_perms = workflow_data.get("permissions")
        if has_top_perms:
            if _is_write_all_permission(top_perms) or not _is_least_privilege_permission(
                top_perms
            ):
                _emit(
                    "EXCESSIVE_PERMISSIONS",
                    "Workflow grants overly broad 'permissions: write-all'. "
                    "Restrict to least-privilege permissions.",
                    "top:permissions",
                    "top:on",
                    "top:jobs",
                )
            for jid, jdata in jobs.items():
                if isinstance(jdata, dict) and _is_write_all_permission(jdata.get("permissions")):
                    _emit(
                        "EXCESSIVE_PERMISSIONS",
                        f"Job '{jid}' sets 'permissions: write-all'.",
                        f"job:{jid}:permissions",
                        f"job:{jid}",
                    )
        else:
            dict_jobs = [(jid, jd) for jid, jd in jobs.items() if isinstance(jd, dict)]
            offending: list[tuple[str, Any]] = []
            for jid, jdata in dict_jobs:
                jperms = jdata.get("permissions")
                if _is_write_all_permission(jperms) or not _is_least_privilege_permission(jperms):
                    offending.append((str(jid), jperms))
            if offending:
                all_omitted = len(offending) == len(dict_jobs) and not any(
                    _is_write_all_permission(jp) for _, jp in offending
                )
                if all_omitted:
                    _emit(
                        "EXCESSIVE_PERMISSIONS",
                        "Workflow omits explicit 'permissions:' block, inheriting default "
                        "GITHUB_TOKEN permissions.",
                        "top:on",
                        "top:jobs",
                    )
                else:
                    for jid, _ in offending:
                        _emit(
                            "EXCESSIVE_PERMISSIONS",
                            f"Job '{jid}' omits least-privilege 'permissions:' or sets write-all.",
                            f"job:{jid}:permissions",
                            f"job:{jid}",
                        )

    # 12. ATRUSS-PIPE-012: Missing timeout-minutes
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        if jdata.get("timeout-minutes") is None:
            _emit(
                "NO_TIMEOUT",
                f"Job '{jid}' omits 'timeout-minutes', risking 360-minute hung runners.",
                f"job:{jid}",
            )

    # 13. ATRUSS-PIPE-013: Artifact credential persistence
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        steps = jdata.get("steps", [])
        if not isinstance(steps, list):
            continue
        unsafe_checkout_idx: int | None = None
        has_upload_artifact = False
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", "")).lower()
            if "actions/checkout" in uses:
                with_cfg = step.get("with", {})
                persist = (
                    with_cfg.get("persist-credentials") if isinstance(with_cfg, dict) else None
                )
                is_disabled = (persist is False) or (
                    isinstance(persist, str) and persist.strip().lower() == "false"
                )
                if not is_disabled and unsafe_checkout_idx is None:
                    unsafe_checkout_idx = idx
            if "upload-artifact" in uses:
                has_upload_artifact = True
        if unsafe_checkout_idx is not None and has_upload_artifact:
            _emit(
                "ARTIFACT_CREDENTIAL_PERSISTENCE",
                f"Job '{jid}' runs actions/checkout without 'persist-credentials: false' "
                "and uploads build artifacts.",
                f"job:{jid}:step:{unsafe_checkout_idx}:uses",
                f"job:{jid}:step:{unsafe_checkout_idx}",
                f"job:{jid}",
            )

    # 14. ATRUSS-PIPE-014: Static cloud credentials / missing OIDC id-token: write
    wf_static_key = _find_static_cloud_secret_key(workflow_data.get("env"))
    if wf_static_key is not None:
        _emit(
            "STATIC_CLOUD_CREDENTIALS",
            f"Workflow env '{wf_static_key}' uses long-lived static cloud credentials. "
            "Prefer OIDC federation.",
            f"top:env:{wf_static_key}",
            "top:env",
        )

    top_perms = workflow_data.get("permissions")
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        job_static_key = _find_static_cloud_secret_key(jdata.get("env"))
        if job_static_key is not None:
            _emit(
                "STATIC_CLOUD_CREDENTIALS",
                f"Job '{jid}' env '{job_static_key}' uses static cloud credentials. "
                "Prefer OIDC federation.",
                f"job:{jid}:env:{job_static_key}",
                f"job:{jid}:env",
                f"job:{jid}",
            )

        has_oidc = _has_id_token_write(top_perms, jdata.get("permissions"))
        steps = jdata.get("steps", [])
        if not isinstance(steps, list):
            continue
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", "")).lower()
            is_cloud_login = any(prefix in uses for prefix in _CLOUD_LOGIN_PREFIXES)
            with_cfg = step.get("with", {})
            has_static_with = False
            if isinstance(with_cfg, dict):
                for wk, wv in with_cfg.items():
                    if str(wk).strip().lower() in _STATIC_CLOUD_WITH_KEYS:
                        has_static_with = True
                        break
                    if _STATIC_CLOUD_SECRET_RE.search(str(wv)):
                        has_static_with = True
                        break
            has_static_step_env = _find_static_cloud_secret_key(step.get("env")) is not None
            has_static_run = bool(_STATIC_CLOUD_SECRET_RE.search(str(step.get("run", ""))))

            if (
                (is_cloud_login and not has_oidc)
                or has_static_with
                or has_static_step_env
                or has_static_run
            ):
                _emit(
                    "STATIC_CLOUD_CREDENTIALS",
                    f"Job '{jid}' step {idx + 1} uses cloud authentication without OIDC "
                    "'id-token: write' or relies on static cloud keys.",
                    f"job:{jid}:step:{idx}:uses",
                    f"job:{jid}:step:{idx}:with",
                    f"job:{jid}:step:{idx}",
                    f"job:{jid}",
                )

    return results
