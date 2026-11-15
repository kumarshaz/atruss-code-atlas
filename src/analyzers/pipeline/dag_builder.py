from pathlib import Path
from typing import Any

import networkx as nx

from src.analyzers.pipeline.parser import (
    extract_cross_workflow_references,
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


def _pure_python_pagerank(
    G: nx.DiGraph,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-6,
) -> dict[str, float]:
    """Compute PageRank iteratively in pure Python without numpy or scipy dependencies."""
    node_count = G.number_of_nodes()
    if node_count == 0:
        return {}

    nodes = sorted(G.nodes(), key=str)
    rank: dict[Any, float] = {node: 1.0 / node_count for node in nodes}

    for _ in range(max_iter):
        prev_rank = rank
        dangling_mass = sum(prev_rank[n] for n in nodes if G.out_degree(n) == 0)
        base_score = (1.0 - alpha) / node_count + (alpha * dangling_mass / node_count)
        next_rank: dict[Any, float] = {node: base_score for node in nodes}

        for u in nodes:
            out_deg = G.out_degree(u)
            if out_deg > 0:
                share = alpha * prev_rank[u] / out_deg
                for v in sorted(G.successors(u), key=str):
                    next_rank[v] += share

        diff = sum(abs(next_rank[n] - prev_rank[n]) for n in nodes)
        rank = next_rank
        if diff < node_count * tol:
            break

    return {str(node): round(float(rank[node]), 6) for node in nodes}


def compute_blast_radius(G: nx.DiGraph, target_node: str | None = None) -> dict[str, Any]:
    """
    Compute pure-Python centrality (betweenness centrality + iterative PageRank)
    and downstream blast-radius reachability metrics for a workflow or cross-workflow DAG.
    """
    nodes = sorted(G.nodes(), key=str)
    if nodes:
        raw_betweenness = nx.betweenness_centrality(G)
        betweenness = {str(n): round(float(raw_betweenness.get(n, 0.0)), 6) for n in nodes}
    else:
        betweenness = {}

    pagerank = _pure_python_pagerank(G)
    downstream_impact: dict[str, list[str]] = {
        str(n): sorted(str(desc) for desc in nx.descendants(G, n)) for n in nodes
    }

    critical_nodes = sorted(
        (str(n) for n in nodes),
        key=lambda key: (
            -(betweenness.get(key, 0.0) + pagerank.get(key, 0.0)),
            -len(downstream_impact.get(key, [])),
            key,
        ),
    )

    result: dict[str, Any] = {
        "betweenness_centrality": betweenness,
        "pagerank": pagerank,
        "downstream_impact": downstream_impact,
        "critical_nodes": critical_nodes,
        "max_blast_radius": max((len(v) for v in downstream_impact.values()), default=0),
    }

    if target_node is not None:
        if target_node in G:
            downstream_nodes = sorted(str(d) for d in nx.descendants(G, target_node))
            upstream_nodes = sorted(str(a) for a in nx.ancestors(G, target_node))
        else:
            downstream_nodes = []
            upstream_nodes = []
        total_others = G.number_of_nodes() - 1
        pct = round((len(downstream_nodes) / total_others) * 100.0, 2) if total_others > 0 else 0.0
        result["target_node"] = str(target_node)
        result["downstream_nodes"] = downstream_nodes
        result["upstream_nodes"] = upstream_nodes
        result["blast_radius_count"] = len(downstream_nodes)
        result["blast_radius_pct"] = pct

    return result


def build_cross_workflow_dag(
    workflows: list[dict[str, Any]],
) -> tuple[nx.DiGraph, list[dict[str, Any]]]:
    """
    Build a cross-workflow Directed Graph linking workflows via reusable `workflow_call`
    references and `workflow_run` triggers.
    Returns `(G, resolved_edges)` with deterministic node and edge ordering.
    """
    G = nx.DiGraph()
    by_exact: dict[str, str] = {}
    by_name: dict[str, str] = {}
    by_name_lower: dict[str, str] = {}
    basename_counts: dict[str, list[str]] = {}
    raw_edges: list[dict[str, str]] = []

    normalized_entries: list[tuple[str, dict[str, Any]]] = []
    for wf in workflows:
        if not isinstance(wf, dict):
            continue
        raw_id = str(
            wf.get("path") or wf.get("workflow_id") or wf.get("id") or wf.get("name") or ""
        ).strip()
        if not raw_id:
            continue
        wf_id = raw_id.replace("\\", "/").removeprefix("./")
        normalized_entries.append((wf_id, wf))

    normalized_entries.sort(key=lambda item: item[0])

    for wf_id, wf in normalized_entries:
        wf_name = str(wf.get("name") or Path(wf_id).name)
        G.add_node(
            wf_id,
            id=str(wf.get("id") or Path(wf_id).name),
            path=wf_id,
            name=wf_name,
            external=False,
        )
        by_exact[wf_id] = wf_id
        if wf_name not in by_name:
            by_name[wf_name] = wf_id
        if wf_name.lower() not in by_name_lower:
            by_name_lower[wf_name.lower()] = wf_id
        basename_counts.setdefault(Path(wf_id).name, []).append(wf_id)

        if isinstance(wf.get("cross_workflow_edges"), list):
            for edge in wf["cross_workflow_edges"]:
                if isinstance(edge, dict):
                    raw_edges.append(
                        {
                            "source_workflow": str(edge.get("source_workflow", wf_id)),
                            "source_job": str(edge.get("source_job", "")),
                            "target_workflow": str(edge.get("target_workflow", "")),
                            "edge_type": str(edge.get("edge_type", "workflow_call")),
                        }
                    )
        else:
            raw_wf_obj = wf.get("workflow") if isinstance(wf.get("workflow"), dict) else None
            if raw_wf_obj is None and isinstance(wf.get("data"), dict):
                raw_wf_obj = wf["data"]
            if raw_wf_obj is None:
                raw_wf_obj = wf
            raw_edges.extend(extract_cross_workflow_references(wf_id, raw_wf_obj))

    by_basename: dict[str, str] = {
        bname: ids[0] for bname, ids in basename_counts.items() if len(ids) == 1
    }

    def _resolve_ref(ref: str) -> str:
        clean = ref.strip().replace("\\", "/").removeprefix("./")
        if clean in by_exact:
            return by_exact[clean]
        if ref.strip() in by_name:
            return by_name[ref.strip()]
        if ref.strip().lower() in by_name_lower:
            return by_name_lower[ref.strip().lower()]
        if clean in by_basename:
            return by_basename[clean]
        return clean

    seen_edges: set[tuple[str, str, str, str]] = set()
    resolved_edges: list[dict[str, Any]] = []

    for edge in raw_edges:
        src_raw = edge.get("source_workflow", "")
        dst_raw = edge.get("target_workflow", "")
        if not src_raw or not dst_raw:
            continue
        src = _resolve_ref(src_raw)
        dst = _resolve_ref(dst_raw)
        source_job = str(edge.get("source_job", ""))
        edge_type = str(edge.get("edge_type", "workflow_call"))

        if src not in G:
            G.add_node(src, id=Path(src).name, path=src, name=Path(src).name, external=True)
        if dst not in G:
            G.add_node(dst, id=Path(dst).name, path=dst, name=Path(dst).name, external=True)

        dedup_key = (edge_type, src, source_job, dst)
        if dedup_key not in seen_edges:
            seen_edges.add(dedup_key)
            G.add_edge(src, dst, edge_type=edge_type, source_job=source_job)
            resolved_edges.append(
                {
                    "source_workflow": src,
                    "source_job": source_job,
                    "target_workflow": dst,
                    "edge_type": edge_type,
                }
            )

    resolved_edges.sort(
        key=lambda item: (
            item["edge_type"],
            item["source_workflow"],
            item["source_job"],
            item["target_workflow"],
        )
    )
    return G, resolved_edges


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
        "cross_workflow_edges": extract_cross_workflow_references(workflow_id, workflow_data),
        "blast_radius": compute_blast_radius(G),
    }
    return payload, G
