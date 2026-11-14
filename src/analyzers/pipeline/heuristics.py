import re
from typing import Any

import networkx as nx

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


def _check_secret_exposure(workflow_data: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def _scan_env(env_map: Any, scope: str) -> None:
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
            if is_sensitive_key and len(val_str.strip()) >= 8:
                findings.append({
                    "type": "HARDCODED_SECRET",
                    "severity": "CRITICAL",
                    "message": (
                        f"Potential hardcoded credential in {scope} env '{key}'. "
                        "Use GitHub Secrets instead."
                    ),
                })
            elif any(pat.search(val_str) for pat in _SECRET_PATTERNS):
                findings.append({
                    "type": "HARDCODED_SECRET",
                    "severity": "CRITICAL",
                    "message": f"Potential hardcoded token pattern in {scope} env '{key}'.",
                })

    _scan_env(workflow_data.get("env"), "workflow")
    jobs = workflow_data.get("jobs", {})
    if isinstance(jobs, dict):
        for job_id, job in jobs.items():
            if not isinstance(job, dict):
                continue
            _scan_env(job.get("env"), f"job '{job_id}'")
            for step in job.get("steps", []) if isinstance(job.get("steps"), list) else []:
                if not isinstance(step, dict):
                    continue
                _scan_env(step.get("env"), f"job '{job_id}' step")
                run_str = str(step.get("run", ""))
                if "${{" not in run_str and any(pat.search(run_str) for pat in _SECRET_PATTERNS):
                    findings.append({
                        "type": "HARDCODED_SECRET",
                        "severity": "CRITICAL",
                        "message": (
                            f"Potential hardcoded secret detected in run script of job '{job_id}'."
                        ),
                    })
    return findings


def analyze_workflow_anti_patterns(
    workflow_data: dict[str, Any], G: nx.DiGraph
) -> list[dict[str, str]]:
    """
    Evaluate all 7 PRD §5 anti-patterns for a parsed GitHub Actions workflow.
    Returns structured dicts `{type, severity, message}` for Astro UI badges and JSON exports.
    """
    results: list[dict[str, str]] = []
    jobs = workflow_data.get("jobs", {})
    if not isinstance(jobs, dict):
        jobs = {}

    # 1. No test gate before deploy
    for msg in find_untested_deployments(G):
        sev = "CRITICAL" if msg.startswith("CRITICAL") else "HIGH"
        results.append({"type": "NO_TEST_GATE", "severity": sev, "message": msg})

    # 2. No dependency caching
    for msg in find_missing_caches(workflow_data):
        results.append({"type": "NO_CACHE", "severity": "MEDIUM", "message": msg})

    # 3. No artifact handoff when build + deploy jobs exist
    has_deploy = any(
        _is_deploy_job(str(jid), jdata)
        for jid, jdata in jobs.items()
        if isinstance(jdata, dict)
    )
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
        results.append({
            "type": "NO_ARTIFACT_HANDOFF",
            "severity": "MEDIUM",
            "message": (
                "Workflow has build and deploy stages without artifact handoff "
                "(upload-artifact / container push)."
            ),
        })

    # 4. Hardcoded secrets
    results.extend(_check_secret_exposure(workflow_data))

    # 5. Fully sequential pipeline (>= 3 jobs in linear chain)
    if G.number_of_nodes() >= 3 and nx.is_directed_acyclic_graph(G):
        longest = nx.dag_longest_path_length(G)
        if G.number_of_edges() == G.number_of_nodes() - 1 and longest == G.number_of_nodes() - 1:
            results.append({
                "type": "SEQUENTIAL_ONLY",
                "severity": "LOW",
                "message": (
                    f"Workflow executes {G.number_of_nodes()} jobs strictly sequentially "
                    "with zero parallel branches."
                ),
            })

    # 6. No branch protection filter on deploy-capable push trigger
    raw_on = workflow_data.get("on", workflow_data.get(True))
    if has_deploy and isinstance(raw_on, dict) and "push" in raw_on:
        push_cfg = raw_on.get("push")
        no_filters = isinstance(push_cfg, dict) and not (
            push_cfg.get("branches") or push_cfg.get("tags")
        )
        if push_cfg is None or no_filters:
            results.append({
                "type": "UNFILTERED_MAIN_PUSH",
                "severity": "HIGH",
                "message": "Deployment workflow triggers on 'push' without branch or tag filters.",
            })
    elif has_deploy and (raw_on == "push" or (isinstance(raw_on, list) and "push" in raw_on)):
        results.append({
            "type": "UNFILTERED_MAIN_PUSH",
            "severity": "HIGH",
            "message": "Deployment workflow triggers on unfiltered 'push' event.",
        })

    # 7. Unlabeled self-hosted runner
    for jid, jdata in jobs.items():
        if not isinstance(jdata, dict):
            continue
        runs_on = jdata.get("runs-on")
        if runs_on == "self-hosted" or (isinstance(runs_on, list) and runs_on == ["self-hosted"]):
            results.append({
                "type": "UNLABELED_SELF_HOSTED",
                "severity": "MEDIUM",
                "message": f"Job '{jid}' targets 'self-hosted' without constraint labels.",
            })

    return results
