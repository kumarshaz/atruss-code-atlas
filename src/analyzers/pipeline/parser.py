from typing import Any

import yaml


def parse_workflow_yaml(yaml_content: str) -> dict[str, Any]:
    """Parse a GitHub Actions workflow YAML file."""
    try:
        # Safe load to prevent execution attacks
        data = yaml.safe_load(yaml_content)
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}

def extract_jobs_and_dependencies(workflow: dict[str, Any]) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    """Extract jobs and their 'needs:' dependencies to build a DAG."""
    jobs = workflow.get("jobs", {})
    dependencies = []

    for job_id, job_data in jobs.items():
        if isinstance(job_data, dict):
            needs = job_data.get("needs", [])
            if isinstance(needs, str):
                needs = [needs]
            for dep in needs:
                dependencies.append((dep, job_id))  # Source upstream -> Target downstream

    return jobs, dependencies
