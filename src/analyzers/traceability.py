from __future__ import annotations

import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from src.analyzers.code.base import SKIP_DIRS
from src.analyzers.pipeline.parser import (
    discover_local_workflows,
    extract_job_environment,
    parse_workflow_yaml,
)
from src.models.artifacts import CodeToCloudEdge, WorkspacePackage

_CODE_MANIFEST_NAMES = frozenset({
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
})

_DOCKER_BUILD_FILE_RE = re.compile(r"(?:-f|--file)\s+([^\s;|&]+)")
_DOCKER_BUILD_RE = re.compile(r"\bdocker\s+build(?:x\s+build)?\b")
_DEPLOY_CMD_RE = re.compile(
    r"\b(?:kubectl\s+apply|helm\s+(?:upgrade|install)|terraform\s+apply|az\s+deployment|"
    r"aws\s+(?:ecs|s3|lambda|cloudformation)|docker\s+push|fly\s+deploy|gcloud\s+\S+\s+deploy)\b",
    re.IGNORECASE,
)


def _norm_rel(raw: str) -> str:
    cleaned = str(raw or "").strip().replace("\\", "/")
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    cleaned = cleaned.strip("/")
    return cleaned or "."


def _iter_repo_files(repo_dir: Path) -> list[Path]:
    if not repo_dir.exists() or not repo_dir.is_dir():
        return []
    matched: list[Path] = []
    for root, dirnames, filenames in os.walk(repo_dir):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        root_path = Path(root)
        for fname in sorted(filenames):
            matched.append(root_path / fname)
    return matched


def _discover_code_modules(
    repo_dir: Path,
    files: list[Path],
    modules: list[dict[str, Any]] | None,
    workspace_packages: list[WorkspacePackage] | None,
) -> list[dict[str, str]]:
    """
    Return normalized deterministic module descriptors:
    [{"id": <display/canonical id>, "dir": <rel dir or '.'>, "name": <short name>}]
    """
    by_dir: dict[str, dict[str, str]] = {}

    if workspace_packages:
        for pkg in workspace_packages:
            rel_dir = _norm_rel(pkg.path)
            mod_id = pkg.path if rel_dir != "." else (pkg.name or repo_dir.name)
            by_dir[rel_dir] = {
                "id": _norm_rel(mod_id) if rel_dir != "." else mod_id,
                "dir": rel_dir,
                "name": pkg.name or Path(rel_dir).name or repo_dir.name,
            }

    if modules:
        for mod in modules:
            if not isinstance(mod, dict):
                continue
            rel_dir = _norm_rel(str(mod.get("path", ".")))
            if rel_dir in by_dir:
                continue
            mod_id = rel_dir if rel_dir != "." else repo_dir.name
            by_dir[rel_dir] = {
                "id": mod_id,
                "dir": rel_dir,
                "name": Path(rel_dir).name if rel_dir != "." else repo_dir.name,
            }

    for fpath in files:
        low = fpath.name.lower()
        if low in _CODE_MANIFEST_NAMES or low.endswith(".csproj"):
            rel_parent = fpath.parent.relative_to(repo_dir).as_posix()
            rel_dir = "." if rel_parent in ("", ".") else _norm_rel(rel_parent)
            if rel_dir in by_dir:
                continue
            if rel_dir == ".":
                mod_id = fpath.stem if low.endswith(".csproj") else repo_dir.name
                mod_name = mod_id
            else:
                mod_id = rel_dir
                mod_name = fpath.stem if low.endswith(".csproj") else Path(rel_dir).name
            by_dir[rel_dir] = {"id": mod_id, "dir": rel_dir, "name": mod_name}

    return [by_dir[k] for k in sorted(by_dir.keys())]


def _discover_containers_and_iac(
    repo_dir: Path,
    files: list[Path],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    contents: dict[str, str] = {}
    seen: set[str] = set()

    for fpath in files:
        rel = fpath.relative_to(repo_dir).as_posix()
        rel_low = rel.lower()
        name_low = fpath.name.lower()
        parts_low = [p.lower() for p in Path(rel).parts]

        kind: str | None = None
        if (
            name_low == "dockerfile"
            or name_low.startswith("dockerfile.")
            or (name_low.startswith("docker-compose") and name_low.endswith((".yml", ".yaml")))
        ):
            kind = "container"
        elif (
            len(parts_low) >= 2
            and parts_low[0] in {"k8s", "kubernetes", "helm"}
            and name_low.endswith((".yml", ".yaml"))
        ) or name_low.endswith((".tf", ".bicep")):
            kind = "iac"

        if kind and rel not in seen:
            seen.add(rel)
            artifacts.append({
                "path": rel,
                "dir": "." if "/" not in rel else rel.rsplit("/", 1)[0],
                "type": kind,
                "name": fpath.name,
            })
            try:
                contents[rel] = fpath.read_text(encoding="utf-8", errors="replace")[:16384]
            except OSError:
                contents[rel] = ""
        elif (
            rel_low.endswith((".yml", ".yaml"))
            and ".github" not in parts_low
            and any(p in {"k8s", "kubernetes"} for p in parts_low)
            and rel not in seen
        ):
            seen.add(rel)
            artifacts.append({
                "path": rel,
                "dir": "." if "/" not in rel else rel.rsplit("/", 1)[0],
                "type": "iac",
                "name": fpath.name,
            })
            try:
                contents[rel] = fpath.read_text(encoding="utf-8", errors="replace")[:16384]
            except OSError:
                contents[rel] = ""

    artifacts.sort(key=lambda a: a["path"])
    return artifacts, contents


def _match_modules_for_path(
    target_path: str,
    modules: list[dict[str, str]],
) -> list[dict[str, str]]:
    norm = _norm_rel(target_path)
    exact_matches: list[dict[str, str]] = []
    prefix_matches: list[dict[str, str]] = []

    for mod in modules:
        mdir = mod["dir"]
        if mdir == ".":
            continue
        if norm == mdir or norm.startswith(f"{mdir}/"):
            exact_matches.append(mod)
        elif mdir.startswith(f"{norm}/"):
            prefix_matches.append(mod)

    if exact_matches:
        # Prefer deepest matching directory
        max_len = max(len(m["dir"]) for m in exact_matches)
        return [m for m in exact_matches if len(m["dir"]) == max_len]
    if prefix_matches:
        return prefix_matches
    if norm == ".":
        root_mods = [m for m in modules if m["dir"] == "."]
        if root_mods:
            return root_mods
    return []


def _extract_workflows_for_traceability(
    repo_dir: Path,
    pipelines: list[Any] | None,
) -> list[tuple[str, dict[str, Any]]]:
    entries: list[tuple[str, dict[str, Any]]] = []
    seen_ids: set[str] = set()

    if pipelines:
        for idx, wf in enumerate(pipelines):
            if isinstance(wf, dict):
                wf_id = str(wf.get("path") or wf.get("id") or wf.get("name") or f"wf_{idx}")
                jobs = wf.get("jobs", {})
            else:
                wf_id = str(
                    getattr(wf, "path", None)
                    or getattr(wf, "id", None)
                    or getattr(wf, "name", None)
                    or f"wf_{idx}"
                )
                jobs = getattr(wf, "jobs", {})
            if isinstance(jobs, dict) and jobs:
                has_steps = any(
                    isinstance(j, dict) and "steps" in j for j in jobs.values()
                )
                if has_steps:
                    entries.append((wf_id, {"jobs": jobs}))
                    seen_ids.add(Path(wf_id).name)

    for rel_id, content in discover_local_workflows(repo_dir):
        if Path(rel_id).name in seen_ids and entries:
            continue
        parsed = parse_workflow_yaml(content)
        if parsed and isinstance(parsed.get("jobs"), dict):
            entries.append((rel_id, parsed))

    entries.sort(key=lambda item: item[0])
    return entries


def _detect_deploy_targets(job_data: dict[str, Any]) -> list[str]:
    targets: list[str] = []
    env_name = extract_job_environment(job_data)
    if env_name:
        targets.append(env_name)

    steps = job_data.get("steps", [])
    if not isinstance(steps, list):
        return targets

    for step in steps:
        if not isinstance(step, dict):
            continue
        uses = str(step.get("uses", "")).lower()
        run_cmd = str(step.get("run", "")).lower()

        if ("deploy-pages" in uses or "upload-pages-artifact" in uses) and (
            "github-pages" not in targets
        ):
            targets.append("github-pages")
        if ("azure/" in uses or "az deployment" in run_cmd or "az webapp" in run_cmd) and (
            "azure" not in targets
        ):
            targets.append("azure")
        if (
            "aws-actions/amazon-ecs" in uses
            or "aws-actions/aws-cloudformation" in uses
            or "aws ecs" in run_cmd
            or "aws s3" in run_cmd
            or "aws lambda" in run_cmd
        ) and "aws" not in targets:
            targets.append("aws")
        if (
            "k8s-deploy" in uses
            or "deploy-gke" in uses
            or "kubectl " in run_cmd
            or "helm " in run_cmd
        ) and "kubernetes" not in targets:
            targets.append("kubernetes")
        if (
            "google-github-actions/deploy" in uses or "gcloud run deploy" in run_cmd
        ) and "gcp" not in targets:
            targets.append("gcp")

    return targets


def _is_deploy_oriented_job(job_id: str, job_data: dict[str, Any]) -> bool:
    if extract_job_environment(job_data):
        return True
    label = f"{job_id} {job_data.get('name', '')}".lower()
    if any(kw in label for kw in ("deploy", "release", "publish", "rollout", "cd")):
        return True
    steps = job_data.get("steps", [])
    if isinstance(steps, list):
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", "")).lower()
            run_cmd = str(step.get("run", ""))
            if any(
                tok in uses
                for tok in ("deploy", "azure/", "aws-actions/", "google-github-actions/deploy")
            ) or _DEPLOY_CMD_RE.search(run_cmd):
                return True
    return False


def extract_code_to_cloud_traceability(
    repo_dir: Path,
    modules: list[dict[str, Any]] | None = None,
    workspace_packages: list[WorkspacePackage] | None = None,
    pipelines: list[Any] | None = None,
) -> list[CodeToCloudEdge]:
    """
    Correlate code modules, container/IaC build artifacts, CI/CD workflow jobs,
    and runtime deployment environments into CodeToCloudEdge records (FR-026).
    """
    files = _iter_repo_files(repo_dir)
    code_modules = _discover_code_modules(repo_dir, files, modules, workspace_packages)
    artifacts, artifact_contents = _discover_containers_and_iac(repo_dir, files)
    workflows = _extract_workflows_for_traceability(repo_dir, pipelines)

    edges: dict[tuple[str, str, str, str, str], CodeToCloudEdge] = {}

    def _add_edge(
        source: str,
        source_type: str,
        target: str,
        target_type: str,
        relationship: str,
    ) -> None:
        if not source or not target or source == target:
            return
        key = (source, source_type, target, target_type, relationship)
        if key not in edges:
            edges[key] = CodeToCloudEdge(
                source=source,
                source_type=source_type,
                target=target,
                target_type=target_type,
                relationship=relationship,
            )

    artifact_by_path = {art["path"]: art for art in artifacts}
    linked_artifacts_to_modules: set[str] = set()

    # 1. Link Code Modules -> Containers / IaC (`PACKAGED_BY`)
    for art in artifacts:
        art_path = art["path"]
        art_dir = art["dir"]
        content = artifact_contents.get(art_path, "")

        # Directory proximity match
        matched_mods = _match_modules_for_path(art_dir, code_modules)
        for mod in matched_mods:
            _add_edge(mod["id"], "code_module", art_path, art["type"], "PACKAGED_BY")
            linked_artifacts_to_modules.add(art_path)

        # Docker-compose build contexts
        if art["name"].lower().startswith("docker-compose"):
            try:
                compose_data = yaml.safe_load(content)
            except yaml.YAMLError:
                compose_data = None
            if isinstance(compose_data, dict) and isinstance(compose_data.get("services"), dict):
                for svc_cfg in compose_data["services"].values():
                    if not isinstance(svc_cfg, dict):
                        continue
                    build_cfg = svc_cfg.get("build")
                    ctx = ""
                    if isinstance(build_cfg, str):
                        ctx = build_cfg
                    elif isinstance(build_cfg, dict):
                        ctx = str(build_cfg.get("context", ""))
                    if ctx:
                        for mod in _match_modules_for_path(ctx, code_modules):
                            _add_edge(
                                mod["id"], "code_module", art_path, art["type"], "PACKAGED_BY"
                            )
                            linked_artifacts_to_modules.add(art_path)

        # Dockerfile COPY / path / name references
        if art["type"] == "container":
            for mod in code_modules:
                if mod["dir"] != "." and (
                    mod["dir"] in content or mod["name"] in content
                ):
                    _add_edge(mod["id"], "code_module", art_path, art["type"], "PACKAGED_BY")
                    linked_artifacts_to_modules.add(art_path)

        # IaC (k8s / tf / bicep) referencing module names or containers
        if art["type"] == "iac":
            low_content = content.lower()
            for mod in code_modules:
                mod_tok = mod["name"].lower()
                dir_tok = mod["dir"].lower()
                if (mod_tok and mod_tok in low_content) or (
                    dir_tok != "." and dir_tok in low_content
                ):
                    _add_edge(mod["id"], "code_module", art_path, "iac", "PACKAGED_BY")
                    linked_artifacts_to_modules.add(art_path)
            for container_art in artifacts:
                if container_art["type"] != "container":
                    continue
                c_parent = Path(container_art["path"]).parent.name.lower()
                if container_art["path"].lower() in low_content or (
                    c_parent and c_parent != "." and c_parent in low_content
                ):
                    _add_edge(
                        container_art["path"], "container", art_path, "iac", "PACKAGED_BY"
                    )

        # Fallback if a single code module exists and artifact wasn't explicitly bound
        if art_path not in linked_artifacts_to_modules and len(code_modules) == 1:
            _add_edge(
                code_modules[0]["id"], "code_module", art_path, art["type"], "PACKAGED_BY"
            )
            linked_artifacts_to_modules.add(art_path)

    # 2. Link Code Modules & Containers/IaC -> CI/CD Jobs -> Runtime Environments
    wf_basenames = [Path(wf_id).name for wf_id, _ in workflows]
    dup_basenames = {name for name in wf_basenames if wf_basenames.count(name) > 1}

    for wf_id, wf_data in workflows:
        wf_label = wf_id if Path(wf_id).name in dup_basenames else Path(wf_id).name
        jobs = wf_data.get("jobs", {})
        if not isinstance(jobs, dict):
            continue

        job_defaults = wf_data.get("defaults", {})
        wf_workdir = ""
        if isinstance(job_defaults, dict) and isinstance(job_defaults.get("run"), dict):
            wf_workdir = str(job_defaults["run"].get("working-directory", ""))

        for job_id, job_data in sorted(jobs.items(), key=lambda kv: str(kv[0])):
            if not isinstance(job_data, dict):
                continue
            job_node = f"{wf_label}#{job_id}"
            is_deploy = _is_deploy_oriented_job(str(job_id), job_data)
            job_rel = "DEPLOYED_BY" if is_deploy else "BUILT_BY"

            local_defaults = job_data.get("defaults", {})
            job_workdir = wf_workdir
            if isinstance(local_defaults, dict) and isinstance(local_defaults.get("run"), dict):
                job_workdir = str(local_defaults["run"].get("working-directory", "") or job_workdir)

            matched_any_for_job = False

            if job_workdir:
                for mod in _match_modules_for_path(job_workdir, code_modules):
                    _add_edge(mod["id"], "code_module", job_node, "ci_job", job_rel)
                    matched_any_for_job = True

            steps = job_data.get("steps", [])
            if isinstance(steps, list):
                for step in steps:
                    if not isinstance(step, dict):
                        continue

                    step_wd = str(step.get("working-directory", "") or "")
                    if step_wd:
                        for mod in _match_modules_for_path(step_wd, code_modules):
                            _add_edge(mod["id"], "code_module", job_node, "ci_job", job_rel)
                            matched_any_for_job = True
                        for art in artifacts:
                            norm_wd = _norm_rel(step_wd)
                            if art["dir"] == norm_wd or art["path"].startswith(f"{norm_wd}/"):
                                _add_edge(art["path"], art["type"], job_node, "ci_job", job_rel)
                                matched_any_for_job = True

                    with_cfg = step.get("with", {})
                    if isinstance(with_cfg, dict):
                        ctx = str(with_cfg.get("context", "") or "")
                        dfile = str(
                            with_cfg.get("file", "") or with_cfg.get("dockerfile", "") or ""
                        )
                        if ctx:
                            norm_ctx = _norm_rel(ctx)
                            for mod in _match_modules_for_path(norm_ctx, code_modules):
                                _add_edge(
                                    mod["id"], "code_module", job_node, "ci_job", job_rel
                                )
                                matched_any_for_job = True
                            candidate_df = (
                                "Dockerfile" if norm_ctx == "." else f"{norm_ctx}/Dockerfile"
                            )
                            if candidate_df in artifact_by_path:
                                art = artifact_by_path[candidate_df]
                                _add_edge(
                                    art["path"], art["type"], job_node, "ci_job", "BUILT_BY"
                                )
                                matched_any_for_job = True
                        if dfile:
                            norm_df = _norm_rel(dfile)
                            if norm_df in artifact_by_path:
                                art = artifact_by_path[norm_df]
                                _add_edge(
                                    art["path"], art["type"], job_node, "ci_job", "BUILT_BY"
                                )
                                matched_any_for_job = True
                            df_dir = "." if "/" not in norm_df else norm_df.rsplit("/", 1)[0]
                            for mod in _match_modules_for_path(df_dir, code_modules):
                                _add_edge(
                                    mod["id"], "code_module", norm_df, "container", "PACKAGED_BY"
                                )
                                if not ctx:
                                    _add_edge(
                                        mod["id"], "code_module", job_node, "ci_job", job_rel
                                    )
                                matched_any_for_job = True

                    run_cmd = str(step.get("run", "") or "")
                    if run_cmd:
                        # Check explicit Dockerfile -f references in docker build commands
                        if _DOCKER_BUILD_RE.search(run_cmd):
                            for fmatch in _DOCKER_BUILD_FILE_RE.finditer(run_cmd):
                                norm_df = _norm_rel(fmatch.group(1))
                                if norm_df in artifact_by_path:
                                    art = artifact_by_path[norm_df]
                                    _add_edge(
                                        art["path"], art["type"], job_node, "ci_job", "BUILT_BY"
                                    )
                                    matched_any_for_job = True
                            # Trailing docker build context token (e.g. `docker build ./apps/api`)
                            tokens = run_cmd.split()
                            for tok in tokens:
                                norm_tok = _norm_rel(tok)
                                for mod in _match_modules_for_path(norm_tok, code_modules):
                                    _add_edge(
                                        mod["id"], "code_module", job_node, "ci_job", "BUILT_BY"
                                    )
                                    matched_any_for_job = True

                        # Match any module directory or artifact path mentioned in run command
                        for mod in code_modules:
                            if mod["dir"] != "." and mod["dir"] in run_cmd:
                                _add_edge(
                                    mod["id"], "code_module", job_node, "ci_job", job_rel
                                )
                                matched_any_for_job = True
                        for art in artifacts:
                            if art["path"] in run_cmd or (
                                art["dir"] != "." and f"{art['dir']}/" in run_cmd
                            ):
                                _add_edge(
                                    art["path"], art["type"], job_node, "ci_job", job_rel
                                )
                                matched_any_for_job = True

            # Single-module fallback when job builds/tests/deploys without subdir flags
            if not matched_any_for_job and len(code_modules) == 1:
                _add_edge(code_modules[0]["id"], "code_module", job_node, "ci_job", job_rel)
                if is_deploy:
                    for art in artifacts:
                        _add_edge(art["path"], art["type"], job_node, "ci_job", "DEPLOYED_BY")

            # Link CI Job -> Runtime Environments (`DEPLOYS_TO`)
            for env_target in _detect_deploy_targets(job_data):
                _add_edge(job_node, "ci_job", env_target, "environment", "DEPLOYS_TO")

    return sorted(
        edges.values(),
        key=lambda e: (e.source_type, e.source, e.relationship, e.target_type, e.target),
    )


def _sanitize_mermaid_id(prefix: str, raw: str, used_ids: set[str]) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", raw)
    base = f"{prefix}_{cleaned}" if cleaned else f"{prefix}_node"
    if base[0].isdigit():
        base = f"n_{base}"
    candidate = base
    counter = 2
    while candidate in used_ids:
        candidate = f"{base}_{counter}"
        counter += 1
    used_ids.add(candidate)
    return candidate


def _sanitize_mermaid_label(raw: str) -> str:
    return (
        str(raw)
        .replace('"', "'")
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("[", "(")
        .replace("]", ")")
    )


def render_code_to_cloud_mermaid(edges: list[CodeToCloudEdge]) -> str:
    """
    Render a deterministic Mermaid flowchart LR across up to 4 subgraphs:
    Code Modules, Build Artifacts / Containers, CI/CD Jobs, Runtime Environments.
    Returns '' if edges is empty.
    """
    if not edges:
        return ""

    sorted_edges = sorted(
        edges,
        key=lambda e: (e.source_type, e.source, e.relationship, e.target_type, e.target),
    )

    def _bucket_for_type(node_type: str) -> str:
        low = node_type.strip().lower()
        if low == "code_module":
            return "code_modules"
        if low in {"container", "iac", "artifact"}:
            return "build_artifacts"
        if low == "ci_job":
            return "ci_jobs"
        return "runtime_envs"

    buckets: dict[str, list[str]] = defaultdict(list)
    seen_nodes: dict[tuple[str, str], str] = {}
    used_ids: set[str] = set()

    for edge in sorted_edges:
        for name, ntype in ((edge.source, edge.source_type), (edge.target, edge.target_type)):
            bucket = _bucket_for_type(ntype)
            key = (bucket, name)
            if key not in seen_nodes:
                prefix = {
                    "code_modules": "mod",
                    "build_artifacts": "art",
                    "ci_jobs": "job",
                    "runtime_envs": "env",
                }[bucket]
                seen_nodes[key] = _sanitize_mermaid_id(prefix, name, used_ids)
                buckets[bucket].append(name)

    subgraph_specs = [
        ("code_modules", "Code Modules"),
        ("build_artifacts", "Build Artifacts / Containers"),
        ("ci_jobs", "CI/CD Jobs"),
        ("runtime_envs", "Runtime Environments"),
    ]

    lines: list[str] = ["flowchart LR"]
    for bucket_key, title in subgraph_specs:
        nodes = sorted(buckets.get(bucket_key, []))
        if not nodes:
            continue
        lines.append(f'    subgraph {bucket_key}["{title}"]')
        for node_name in nodes:
            nid = seen_nodes[(bucket_key, node_name)]
            lines.append(f'        {nid}["{_sanitize_mermaid_label(node_name)}"]')
        lines.append("    end")

    for edge in sorted_edges:
        src_bucket = _bucket_for_type(edge.source_type)
        dst_bucket = _bucket_for_type(edge.target_type)
        src_id = seen_nodes[(src_bucket, edge.source)]
        dst_id = seen_nodes[(dst_bucket, edge.target)]
        lines.append(f"    {src_id} -->|{edge.relationship}| {dst_id}")

    return "\n".join(lines)
