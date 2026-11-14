from pathlib import Path
from typing import Any

import networkx as nx

from src.analyzers.pipeline.parser import (
    extract_job_details,
    extract_jobs_and_dependencies,
    extract_triggers,
)


def build_workflow_dag(workflow_data: dict[str, Any]) -> nx.DiGraph:
    """Builds a Directed Acyclic Graph (DAG) for a pipeline workflow."""
    G = nx.DiGraph()
    jobs, dependencies = extract_jobs_and_dependencies(workflow_data)

    for job_id, job_metadata in jobs.items():
        G.add_node(job_id, **(job_metadata if isinstance(job_metadata, dict) else {}))

    for upstream, downstream in dependencies:
        if upstream in G.nodes and downstream in G.nodes:
            G.add_edge(upstream, downstream)

    return G


def get_dag_metrics(G: nx.DiGraph) -> dict[str, Any]:
    """Extract topology metrics from the workflow graph."""
    try:
        is_dag = nx.is_directed_acyclic_graph(G)
        longest_path = nx.dag_longest_path_length(G) if is_dag and G.number_of_nodes() > 0 else 0
    except Exception:
        is_dag = False
        longest_path = -1

    return {
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "is_valid_dag": is_dag,
        "max_depth": longest_path,
    }


def build_workflow_graph_payload(
    workflow_id: str, workflow_data: dict[str, Any]
) -> tuple[dict[str, Any], nx.DiGraph]:
    """Build structured workflow payload compatible with Astro PipelineView and NetworkX DAG."""
    G = build_workflow_dag(workflow_data)
    jobs, _ = extract_jobs_and_dependencies(workflow_data)
    triggers = extract_triggers(workflow_data)

    job_items: list[dict[str, Any]] = []
    for jid, jdata in jobs.items():
        if isinstance(jdata, dict):
            job_items.append(extract_job_details(str(jid), jdata))
        else:
            job_items.append(
                {
                    "id": str(jid),
                    "name": str(jid),
                    "runner": "unspecified",
                    "steps_count": 0,
                    "needs": [],
                    "environment": None,
                }
            )

    wf_name = str(workflow_data.get("name") or Path(workflow_id).name)
    payload = {
        "id": Path(workflow_id).name,
        "path": workflow_id,
        "name": wf_name,
        "triggers": triggers,
        "jobs": job_items,
        "dag_metrics": get_dag_metrics(G),
    }
    return payload, G
