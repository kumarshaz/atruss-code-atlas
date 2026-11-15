import re
from pathlib import Path
from typing import Any

import yaml


def parse_workflow_yaml(yaml_content: str) -> dict[str, Any]:
    """Parse a GitHub Actions workflow YAML file safely."""
    try:
        data = yaml.safe_load(yaml_content)
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def extract_triggers(workflow: dict[str, Any]) -> list[str]:
    """
    Extract GitHub Actions trigger names from the `on:` key.
    Handles PyYAML YAML 1.1 parsing unquoted `on:` as boolean `True`.
    """
    raw_on = workflow.get("on", workflow.get(True))
    if raw_on is None:
        return []
    if isinstance(raw_on, str):
        return [raw_on]
    if isinstance(raw_on, list):
        return [str(item) for item in raw_on]
    if isinstance(raw_on, dict):
        return [str(k) for k in raw_on]
    return []


def extract_jobs_and_dependencies(
    workflow: dict[str, Any],
) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    """Extract jobs and their 'needs:' dependencies to build a DAG."""
    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, dict):
        return {}, []

    dependencies: list[tuple[str, str]] = []
    for job_id, job_data in jobs.items():
        if isinstance(job_data, dict):
            needs = job_data.get("needs", [])
            if isinstance(needs, str):
                needs = [needs]
            elif not isinstance(needs, list):
                needs = []
            for dep in needs:
                dependencies.append((str(dep), str(job_id)))

    return jobs, dependencies


def normalize_runner(runs_on: Any) -> str:
    """Convert GitHub Actions runs-on values into a deterministic display string."""
    if runs_on is None:
        return "unspecified"
    if isinstance(runs_on, str):
        return runs_on
    if isinstance(runs_on, list):
        return ", ".join(str(item) for item in runs_on)
    if isinstance(runs_on, dict):
        group = runs_on.get("group")
        labels = runs_on.get("labels")
        if group:
            return f"group:{group}"
        if labels:
            return f"labels:{labels}"
    return str(runs_on)


def extract_job_environment(job_data: dict[str, Any]) -> str | None:
    """Extract deployment environment name from a job definition if present."""
    env_cfg = job_data.get("environment")
    if isinstance(env_cfg, str) and env_cfg.strip():
        return env_cfg.strip()
    if isinstance(env_cfg, dict):
        name = env_cfg.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return None


def extract_job_details(job_id: str, job_data: dict[str, Any]) -> dict[str, Any]:
    """Extract normalized job metadata for DAG JSON serialization and Astro rendering."""
    needs = job_data.get("needs", [])
    if isinstance(needs, str):
        needs_list = [needs]
    elif isinstance(needs, list):
        needs_list = [str(n) for n in needs]
    else:
        needs_list = []

    steps = job_data.get("steps", [])
    steps_count = len(steps) if isinstance(steps, list) else 0

    return {
        "id": str(job_id),
        "name": str(job_data.get("name") or job_id),
        "runner": normalize_runner(job_data.get("runs-on")),
        "steps_count": steps_count,
        "needs": needs_list,
        "environment": extract_job_environment(job_data),
    }


def _scalar_key_name(node: yaml.Node) -> str:
    if isinstance(node, yaml.ScalarNode):
        val = str(node.value)
        if node.tag == "tag:yaml.org,2002:bool" and val.lower() in ("on", "true", "yes"):
            return "on" if val.lower() == "on" else val
        return val
    return ""


def _compute_node_end_line(key_node: yaml.Node, val_node: yaml.Node) -> int:
    start = key_node.start_mark.line + 1
    if isinstance(val_node, yaml.MappingNode) and val_node.value:
        last_k, last_v = val_node.value[-1]
        return max(start, _compute_node_end_line(last_k, last_v))
    if isinstance(val_node, yaml.SequenceNode) and val_node.value:
        last_item = val_node.value[-1]
        if isinstance(last_item, yaml.MappingNode) and last_item.value:
            last_k, last_v = last_item.value[-1]
            return max(start, _compute_node_end_line(last_k, last_v))
        end_line = last_item.end_mark.line
        if last_item.end_mark.column > 0:
            end_line += 1
        return max(start, end_line)
    end_line = val_node.end_mark.line
    if val_node.end_mark.column > 0 or end_line == key_node.start_mark.line:
        end_line += 1
    return max(start, end_line)


def _fallback_line_map(yaml_content: str) -> tuple[dict[str, int], dict[str, int]]:
    starts: dict[str, int] = {}
    ends: dict[str, int] = {}
    in_jobs = False
    jobs_indent: int | None = None
    current_job: str | None = None
    step_idx = 0

    for lineno, raw_line in enumerate(yaml_content.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent == 0:
            in_jobs = False
            current_job = None
            m = re.match(r"^['\"]?([A-Za-z0-9_.-]+)['\"]?\s*:", stripped)
            if m:
                key = m.group(1)
                starts[f"top:{key}"] = lineno
                ends[f"top:{key}"] = lineno
                if key == "jobs":
                    in_jobs = True
                    jobs_indent = None
            continue

        if in_jobs:
            if jobs_indent is None and not stripped.startswith("-"):
                m = re.match(r"^['\"]?([A-Za-z0-9_.-]+)['\"]?\s*:", stripped)
                if m:
                    jobs_indent = indent
            if jobs_indent is not None and indent == jobs_indent and not stripped.startswith("-"):
                m = re.match(r"^['\"]?([A-Za-z0-9_.-]+)['\"]?\s*:", stripped)
                if m:
                    current_job = m.group(1)
                    step_idx = 0
                    starts[f"job:{current_job}"] = lineno
                    ends[f"job:{current_job}"] = lineno
                    continue
            if current_job and stripped.startswith("-"):
                key = f"job:{current_job}:step:{step_idx}"
                starts[key] = lineno
                ends[key] = lineno
                step_idx += 1

    return dict(sorted(starts.items())), dict(sorted(ends.items()))


def _extract_workflow_line_spans(yaml_content: str) -> tuple[dict[str, int], dict[str, int]]:
    if not yaml_content or not yaml_content.strip():
        return {}, {}
    try:
        root = next(yaml.compose_all(yaml_content, Loader=yaml.SafeLoader), None)
    except yaml.YAMLError:
        return _fallback_line_map(yaml_content)

    if not isinstance(root, yaml.MappingNode):
        return {}, {}

    starts: dict[str, int] = {}
    ends: dict[str, int] = {}

    def _record(key: str, k_node: yaml.Node, v_node: yaml.Node) -> None:
        s_line = k_node.start_mark.line + 1
        e_line = _compute_node_end_line(k_node, v_node)
        starts[key] = s_line
        ends[key] = e_line

    for top_k, top_v in root.value:
        top_name = _scalar_key_name(top_k)
        if not top_name:
            continue
        _record(f"top:{top_name}", top_k, top_v)

        if top_name in ("on", "env") and isinstance(top_v, yaml.MappingNode):
            for sub_k, sub_v in top_v.value:
                sub_name = _scalar_key_name(sub_k)
                if sub_name:
                    _record(f"top:{top_name}:{sub_name}", sub_k, sub_v)

        elif top_name == "jobs" and isinstance(top_v, yaml.MappingNode):
            for job_k, job_v in top_v.value:
                job_id = _scalar_key_name(job_k)
                if not job_id:
                    continue
                _record(f"job:{job_id}", job_k, job_v)
                if not isinstance(job_v, yaml.MappingNode):
                    continue
                for jk, jv in job_v.value:
                    j_attr = _scalar_key_name(jk)
                    if not j_attr:
                        continue
                    _record(f"job:{job_id}:{j_attr}", jk, jv)
                    if j_attr == "env" and isinstance(jv, yaml.MappingNode):
                        for ek, ev in jv.value:
                            e_name = _scalar_key_name(ek)
                            if e_name:
                                _record(f"job:{job_id}:env:{e_name}", ek, ev)
                    elif j_attr == "steps" and isinstance(jv, yaml.SequenceNode):
                        for idx, step_node in enumerate(jv.value):
                            step_prefix = f"job:{job_id}:step:{idx}"
                            step_start = step_node.start_mark.line + 1
                            if isinstance(step_node, yaml.MappingNode) and step_node.value:
                                last_sk, last_sv = step_node.value[-1]
                                step_end = max(step_start, _compute_node_end_line(last_sk, last_sv))
                            else:
                                step_end = step_start
                            starts[step_prefix] = step_start
                            ends[step_prefix] = step_end
                            if not isinstance(step_node, yaml.MappingNode):
                                continue
                            for sk, sv in step_node.value:
                                s_attr = _scalar_key_name(sk)
                                if not s_attr:
                                    continue
                                _record(f"{step_prefix}:{s_attr}", sk, sv)
                                if s_attr in ("env", "with") and isinstance(sv, yaml.MappingNode):
                                    for mk, mv in sv.value:
                                        m_name = _scalar_key_name(mk)
                                        if m_name:
                                            _record(f"{step_prefix}:{s_attr}:{m_name}", mk, mv)

    return dict(sorted(starts.items())), dict(sorted(ends.items()))


def extract_workflow_line_map(yaml_content: str) -> dict[str, int]:
    """
    Compute 1-indexed YAML line numbers for top-level keys (`top:permissions`, `top:on`),
    jobs (`job:<job_id>`), and step indicators (`job:<job_id>:step:<idx>`, etc.).
    """
    starts, _ = _extract_workflow_line_spans(yaml_content)
    return starts


def extract_cross_workflow_references(
    workflow_id: str, workflow: dict[str, Any]
) -> list[dict[str, str]]:
    """
    Resolve cross-workflow dependencies from:
    - Reusable workflow calls (`jobs.<j>.uses: ./.github/workflows/...` or
      `org/repo/.github/workflows/...`) -> `edge_type: "workflow_call"`
    - `on.workflow_run.workflows` triggers -> `edge_type: "workflow_run"`
    """
    if not isinstance(workflow, dict):
        return []

    seen: set[tuple[str, str, str, str]] = set()
    refs: list[dict[str, str]] = []

    jobs = workflow.get("jobs", {})
    if isinstance(jobs, dict):
        for job_id, job_data in jobs.items():
            if not isinstance(job_data, dict):
                continue
            uses = job_data.get("uses")
            if isinstance(uses, str) and ".github/workflows/" in uses:
                target = uses.split("@", 1)[0].strip().replace("\\", "/").removeprefix("./")
                if target:
                    key = ("workflow_call", str(workflow_id), str(job_id), target)
                    if key not in seen:
                        seen.add(key)
                        refs.append(
                            {
                                "source_workflow": str(workflow_id),
                                "source_job": str(job_id),
                                "target_workflow": target,
                                "edge_type": "workflow_call",
                            }
                        )

    raw_on = workflow.get("on", workflow.get(True))
    if isinstance(raw_on, dict):
        wf_run = raw_on.get("workflow_run")
        if isinstance(wf_run, dict):
            upstream_wfs = wf_run.get("workflows", [])
            if isinstance(upstream_wfs, str):
                upstream_wfs = [upstream_wfs]
            if isinstance(upstream_wfs, list):
                for upstream in upstream_wfs:
                    upstream_name = str(upstream).strip()
                    if upstream_name:
                        key = ("workflow_run", upstream_name, "", str(workflow_id))
                        if key not in seen:
                            seen.add(key)
                            refs.append(
                                {
                                    "source_workflow": upstream_name,
                                    "source_job": "",
                                    "target_workflow": str(workflow_id),
                                    "edge_type": "workflow_run",
                                }
                            )

    refs.sort(
        key=lambda item: (
            item["edge_type"],
            item["source_workflow"],
            item["source_job"],
            item["target_workflow"],
        )
    )
    return refs


def discover_local_workflows(repo_dir: Path) -> list[tuple[str, str]]:
    """
    Recursively discover `.github/workflows/*.yml` and `*.yaml` files inside a local repository.
    Returns deterministic sorted pairs of `(relative_workflow_id, file_content)`.
    """
    workflow_files: list[Path] = []
    for workflows_dir in repo_dir.rglob("workflows"):
        if (
            workflows_dir.is_dir()
            and workflows_dir.parent.name == ".github"
            and ".git" not in workflows_dir.parts
            and "node_modules" not in workflows_dir.parts
        ):
            for ext in ("*.yml", "*.yaml"):
                workflow_files.extend(workflows_dir.glob(ext))

    unique_files = sorted(set(workflow_files), key=lambda p: str(p.relative_to(repo_dir)))
    results: list[tuple[str, str]] = []
    for wf_path in unique_files:
        try:
            content = wf_path.read_text(encoding="utf-8", errors="replace")
            rel_id = str(wf_path.relative_to(repo_dir)).replace("\\", "/")
            results.append((rel_id, content))
        except OSError:
            continue
    return results
