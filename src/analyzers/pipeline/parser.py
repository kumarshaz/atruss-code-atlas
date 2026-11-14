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
