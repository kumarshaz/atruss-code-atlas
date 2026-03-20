from typing import Any

import networkx as nx


def find_untested_deployments(G: nx.DiGraph) -> list[str]:
    """Flags deployment jobs that don't depend on a test/build job."""
    findings = []

    # Simple heuristic: Any job named 'deploy' or 'publish' must have an upstream node.
    # In a full production system, we'd check if the upstream node is actually a 'test' job.
    for node in G.nodes:
        node_str = str(node).lower()
        if "deploy" in node_str or "publish" in node_str or "release" in node_str:
            upstream = list(G.predecessors(node))
            if not upstream:
                findings.append(
                    f"CRITICAL: Job '{node}' performs deployment but has no upstream test gates ('needs:' block is empty)."
                )
    return findings

def find_missing_caches(workflow_data: dict[str, Any]) -> list[str]:
    """Flags workflows that compile code but don't cache dependencies."""
    findings = []
    has_cache = False

    jobs = workflow_data.get("jobs", {})
    for job_id, job in jobs.items():
        steps = job.get("steps", [])
        for step in steps:
            uses = step.get("uses", "")
            if "actions/cache" in uses:
                has_cache = True

    if not has_cache:
        findings.append(
            "MEDIUM: Workflow lacks dependency caching via 'actions/cache'. Performance could be severely degraded."
        )

    return findings
