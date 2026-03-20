from typing import Any

import networkx as nx

from src.analyzers.pipeline.parser import extract_jobs_and_dependencies


def build_workflow_dag(workflow_data: dict[str, Any]) -> nx.DiGraph:
    """Builds a Directed Acyclic Graph (DAG) for a pipeline workflow."""

    G = nx.DiGraph()
    jobs, dependencies = extract_jobs_and_dependencies(workflow_data)

    # Add Nodes
    for job_id, job_metadata in jobs.items():
        G.add_node(job_id, **(job_metadata if isinstance(job_metadata, dict) else {}))

    # Add Edges
    for upstream, downstream in dependencies:
        if upstream in G.nodes and downstream in G.nodes:
            G.add_edge(upstream, downstream)

    return G

def get_dag_metrics(G: nx.DiGraph) -> dict[str, Any]:
    """Extract topology metrics from the workflow graph."""
    try:
        is_dag = nx.is_directed_acyclic_graph(G)
        longest_path = nx.dag_longest_path_length(G) if is_dag else -1
    except Exception:
        is_dag = False
        longest_path = -1

    return {
        "node_count": G.number_of_nodes(),
        "edge_count": G.number_of_edges(),
        "is_valid_dag": is_dag,
        "max_depth": longest_path
    }
