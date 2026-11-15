from __future__ import annotations

import io
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, BinaryIO, TextIO

import networkx as nx
import typer

from src.analyzers.code.fitness_engine import (
    compute_component_blast_radius,
    evaluate_architecture_fitness,
)
from src.analyzers.drift import resolve_snapshot_dir
from src.analyzers.pipeline.dag_builder import (
    build_cross_workflow_dag,
    build_workflow_dag,
    compute_blast_radius,
)
from src.analyzers.scorecard import SECURITY_PIPELINE_ANTIPATTERNS, compute_repository_scorecard

app = typer.Typer()

MCP_PROTOCOL_VERSION = "2024-11-05"

_TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "list_repositories",
        "description": (
            "List indexed repositories from exports/latest with optional ecosystem and "
            "organization filters."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "ecosystem": {"type": "string", "description": "Filter by language/ecosystem"},
                "organization": {"type": "string", "description": "Filter by organization"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "get_repo_architecture",
        "description": (
            "Retrieve structural architecture components, complexity metrics, fitness "
            "violations, and Code-to-Cloud edges for a repository."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Repository name or org/repo"},
            },
            "required": ["repository"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_pipeline_dag",
        "description": "Retrieve CI/CD workflow DAGs, jobs, triggers, and anti-patterns.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Repository name or org/repo"},
            },
            "required": ["repository"],
            "additionalProperties": False,
        },
    },
    {
        "name": "find_cross_repo_impacts",
        "description": (
            "Find cross-repository workflow_call/workflow_run links, shared packages, "
            "and deployment target impacts for a repository, workflow, or package."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Repository, workflow path, package name, or environment",
                },
            },
            "required": ["target"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_blast_radius",
        "description": (
            "Compute PageRank, betweenness centrality, and transitive blast radius for "
            "code components and/or pipeline jobs."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Repository name or org/repo"},
                "target_node": {
                    "type": "string",
                    "description": "Optional component or pipeline job identifier",
                },
                "scope": {
                    "type": "string",
                    "enum": ["auto", "code", "pipeline"],
                    "description": "Graph scope to evaluate",
                },
            },
            "required": ["repository"],
            "additionalProperties": False,
        },
    },
    {
        "name": "trace_entrypoint_chain",
        "description": (
            "Trace dependency chains from API routes, CLI commands, or UI entrypoints "
            "to downstream services, data layers, and cloud environments."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Repository name or org/repo"},
                "entrypoint": {
                    "type": "string",
                    "description": "Optional specific entrypoint component name",
                },
            },
            "required": ["repository"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_security_findings",
        "description": (
            "Query CVE vulnerabilities, secret findings, and CI/CD supply-chain security "
            "anti-patterns across repositories."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Optional repository filter"},
                "severity": {
                    "type": "string",
                    "description": "Optional severity filter (CRITICAL|HIGH|MEDIUM|LOW)",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "query_antipatterns",
        "description": (
            "Query CI/CD pipeline anti-patterns and architectural fitness violations across "
            "indexed repositories."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Optional repository filter"},
                "rule_id": {
                    "type": "string",
                    "description": "Optional rule ID (e.g. ATRUSS-PIPE-008)",
                },
                "type": {"type": "string", "description": "Optional anti-pattern type code"},
                "severity": {"type": "string", "description": "Optional severity filter"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "get_repo_scorecard",
        "description": (
            "Retrieve or compute the 6-Dimension A-F Scorecard and Technical Debt Score "
            "for a repository."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Repository name or org/repo"},
            },
            "required": ["repository"],
            "additionalProperties": False,
        },
    },
    {
        "name": "check_boundary_violation",
        "description": (
            "Evaluate architectural layer boundary rules and circular dependencies for a "
            "repository, optionally simulating a proposed component dependency edge."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "repository": {"type": "string", "description": "Repository name or org/repo"},
                "source_component": {"type": "string", "description": "Optional source component"},
                "target_component": {"type": "string", "description": "Optional target component"},
                "source_layer": {"type": "string", "description": "Optional source layer"},
                "target_layer": {"type": "string", "description": "Optional target layer"},
                "policy_path": {
                    "type": "string",
                    "description": "Optional custom policy YAML path",
                },
            },
            "required": ["repository"],
            "additionalProperties": False,
        },
    },
]


def _safe_load_json(path: Path) -> Any:
    if not path.exists() or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return None


def _build_component_digraph(
    components: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
) -> nx.DiGraph:
    G = nx.DiGraph()
    comp_by_name: dict[str, dict[str, Any]] = {}
    file_to_non_module: dict[str, list[dict[str, Any]]] = defaultdict(list)

    sorted_comps = sorted(
        (c for c in components if isinstance(c, dict)),
        key=lambda c: (
            0 if c.get("type") != "MODULE" else 1,
            str(c.get("name", "")),
            str(c.get("file", "")),
        ),
    )

    for comp in sorted_comps:
        name = str(comp.get("name", "")).strip()
        if not name:
            continue
        layer = str(comp.get("layer") or comp.get("type") or "").strip()
        fpath = str(comp.get("file") or "").replace("\\", "/")
        line = int(comp.get("line", 1) or 1)
        if name not in comp_by_name:
            comp_by_name[name] = comp
            G.add_node(name, layer=layer, type=comp.get("type", layer), file=fpath, line=line)
        if fpath and comp.get("type") != "MODULE":
            file_to_non_module[fpath].append(comp)

    for comp in sorted_comps:
        src_name = str(comp.get("name", "")).strip()
        if not src_name or src_name not in G:
            continue
        for dep in comp.get("dependencies", []) or []:
            dep_name = str(dep).strip()
            if dep_name in comp_by_name and dep_name != src_name:
                G.add_edge(src_name, dep_name)

    if isinstance(metrics, dict) and isinstance(metrics.get("import_edges"), list):
        for edge in metrics["import_edges"]:
            if not isinstance(edge, dict):
                continue
            src_file = str(edge.get("source_file", "")).replace("\\", "/")
            tgt_sym = str(edge.get("target_symbol", "")).strip()
            src_comps = file_to_non_module.get(src_file, [])
            if len(src_comps) == 1 and tgt_sym in comp_by_name:
                src_name = str(src_comps[0]["name"])
                tgt_file = str(comp_by_name[tgt_sym].get("file", "")).replace("\\", "/")
                if tgt_sym != src_name and tgt_file != src_file:
                    G.add_edge(src_name, tgt_sym)

    return G


class AtrussMCPServer:
    """
    Pure-Python, read-only stdio JSON-RPC 2.0 Model Context Protocol (MCP) server
    backed by static export artifacts in `exports/latest/` (FR-029).
    """

    def __init__(self, exports_dir: Path | str):
        self.exports_dir = resolve_snapshot_dir(Path(exports_dir))

    def _load_index(self) -> dict[str, Any]:
        root = self.exports_dir
        repo_payload = _safe_load_json(root / "repos" / "repositories.json")
        if isinstance(repo_payload, dict):
            inv_items = [i for i in repo_payload.get("items", []) if isinstance(i, dict)]
        elif isinstance(repo_payload, list):
            inv_items = [i for i in repo_payload if isinstance(i, dict)]
        else:
            inv_items = []

        repos_inv: dict[str, dict[str, Any]] = {}
        for item in inv_items:
            org = str(item.get("Organization", "")).strip()
            name = str(item.get("RepositoryName", item.get("name", ""))).strip()
            rid = str(item.get("RepositoryId", "")).strip()
            key = rid if "/" in rid else (f"{org}/{name}" if org and name else name)
            if key:
                repos_inv[key] = item

        reports: dict[str, dict[str, Any]] = {}
        reports_dir = root / "reports"
        if reports_dir.is_dir():
            for rfile in sorted(reports_dir.glob("*-analysis.json")):
                rdata = _safe_load_json(rfile)
                if isinstance(rdata, dict):
                    key = str(rdata.get("repository", "")).strip() or rfile.stem.removesuffix(
                        "-analysis"
                    )
                    reports[key] = rdata

        pipelines: dict[str, dict[str, Any]] = {}
        pipelines_dir = root / "pipelines"
        if pipelines_dir.is_dir():
            for pfile in sorted(pipelines_dir.glob("*-pipeline.json")):
                pdata = _safe_load_json(pfile)
                if isinstance(pdata, dict):
                    org = str(pdata.get("org", "")).strip()
                    repo = str(pdata.get("repository", "")).strip()
                    key = f"{org}/{repo}" if org and repo and "/" not in repo else (
                        repo or pfile.stem.removesuffix("-pipeline")
                    )
                    pipelines[key] = pdata

        topology = _safe_load_json(root / "relationships" / "pipeline_topology.json")
        return {
            "inventory": repos_inv,
            "reports": reports,
            "pipelines": pipelines,
            "topology": topology if isinstance(topology, dict) else {},
        }

    def _match_repo_key(self, query: str, mapping: dict[str, Any]) -> str | None:
        cleaned = query.strip().lower()
        if not cleaned:
            return None
        for key in sorted(mapping.keys()):
            if key.lower() == cleaned or key.replace("/", "-").lower() == cleaned:
                return key
        short_q = cleaned.split("/")[-1]
        for key in sorted(mapping.keys()):
            if key.split("/")[-1].lower() == short_q:
                return key
        return None

    def _tool_list_repositories(self, args: dict[str, Any]) -> dict[str, Any]:
        idx = self._load_index()
        inv = idx["inventory"]
        reports = idx["reports"]
        pipelines = idx["pipelines"]

        eco_filter = str(args.get("ecosystem") or "").strip().lower()
        org_filter = str(args.get("organization") or "").strip().lower()

        all_keys = sorted(set(inv) | set(reports) | set(pipelines))
        entries: list[dict[str, Any]] = []
        for key in all_keys:
            inv_key = self._match_repo_key(key, inv)
            rep_key = self._match_repo_key(key, reports)
            pip_key = self._match_repo_key(key, pipelines)

            inv_item = inv.get(inv_key, {}) if inv_key else {}
            rep_item = reports.get(rep_key, {}) if rep_key else {}
            pip_item = pipelines.get(pip_key, {}) if pip_key else {}

            org = str(
                inv_item.get("Organization")
                or pip_item.get("org")
                or (key.split("/", 1)[0] if "/" in key else "local")
            )
            eco = str(inv_item.get("PrimaryLanguage") or rep_item.get("ecosystem") or "Unknown")
            fw = str(
                inv_item.get("FrameworkType")
                or (rep_item.get("metrics") or {}).get("framework")
                or "Unknown"
            )
            if eco_filter and eco_filter not in eco.lower():
                continue
            if org_filter and org_filter != org.lower():
                continue

            sc = rep_item.get("scorecard") if isinstance(rep_item.get("scorecard"), dict) else None
            entries.append({
                "repository": key,
                "organization": org,
                "ecosystem": eco,
                "framework": fw,
                "component_count": len(rep_item.get("architecture_components") or []),
                "workflow_count": len(pip_item.get("workflows") or []),
                "overall_grade": sc.get("overall_grade") if sc else None,
                "overall_score": sc.get("overall_score") if sc else None,
            })

        return {"count": len(entries), "repositories": entries}

    def _tool_get_repo_architecture(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_q = str(args.get("repository", "")).strip()
        idx = self._load_index()
        reports = idx["reports"]
        matched = self._match_repo_key(repo_q, reports)
        if not matched:
            return {
                "found": False,
                "repository": repo_q,
                "error": f"Architecture report not found for '{repo_q}'.",
                "available_repositories": sorted(reports.keys()),
            }
        rep = reports[matched]
        return {
            "found": True,
            "repository": rep.get("repository", matched),
            "sha": rep.get("sha", "unknown"),
            "ecosystem": rep.get("ecosystem", "Unknown"),
            "metrics": rep.get("metrics", {}),
            "architecture_components": rep.get("architecture_components", []),
            "fitness_violations": rep.get("fitness_violations", []),
            "code_to_cloud_edges": rep.get("code_to_cloud_edges", []),
            "workspace_packages": rep.get("workspace_packages", []),
            "observability": rep.get("observability", {}),
        }

    def _tool_get_pipeline_dag(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_q = str(args.get("repository", "")).strip()
        idx = self._load_index()
        pipelines = idx["pipelines"]
        reports = idx["reports"]

        p_key = self._match_repo_key(repo_q, pipelines)
        if p_key:
            pdata = pipelines[p_key]
            return {
                "found": True,
                "repository": f"{pdata.get('org', '')}/{pdata.get('repository', '')}".strip("/"),
                "sha": pdata.get("sha", "unknown"),
                "workflows": pdata.get("workflows", []),
            }
        r_key = self._match_repo_key(repo_q, reports)
        if r_key and reports[r_key].get("pipelines"):
            rep = reports[r_key]
            return {
                "found": True,
                "repository": rep.get("repository", r_key),
                "sha": rep.get("sha", "unknown"),
                "workflows": rep.get("pipelines", []),
            }
        return {
            "found": False,
            "repository": repo_q,
            "error": f"Pipeline data not found for '{repo_q}'.",
            "available_repositories": sorted(set(pipelines) | set(reports)),
        }

    def _tool_find_cross_repo_impacts(self, args: dict[str, Any]) -> dict[str, Any]:
        target = str(args.get("target", "")).strip()
        target_low = target.lower()
        idx = self._load_index()

        all_wfs: list[dict[str, Any]] = []
        for repo_key, pdata in sorted(idx["pipelines"].items()):
            for wf in pdata.get("workflows", []) or []:
                if not isinstance(wf, dict):
                    continue
                wf_copy = dict(wf)
                wf_id = str(wf.get("path") or wf.get("id") or wf.get("name") or "")
                wf_copy["path"] = f"{repo_key}:{wf_id}" if wf_id else repo_key
                all_wfs.append(wf_copy)

        cross_edges: list[dict[str, Any]] = []
        if all_wfs:
            _g_cross, resolved_edges = build_cross_workflow_dag(all_wfs)
            for edge in resolved_edges:
                hay = (
                    f"{edge.get('source_workflow', '')} "
                    f"{edge.get('target_workflow', '')}"
                ).lower()
                if not target_low or target_low in hay:
                    cross_edges.append(edge)

        dependent_repos: set[str] = set()
        shared_packages: list[dict[str, str]] = []
        for repo_key, rep in sorted(idx["reports"].items()):
            for dep in rep.get("dependencies", []) or []:
                if not isinstance(dep, dict):
                    continue
                d_name = str(dep.get("name", ""))
                d_purl = str(dep.get("purl", ""))
                if target_low in d_name.lower() or target_low in d_purl.lower():
                    dependent_repos.add(repo_key)
                    shared_packages.append({
                        "repository": repo_key,
                        "package": d_name,
                        "version": str(dep.get("version", "")),
                        "manifest_file": str(dep.get("manifest_file", "")),
                    })
            for wp in rep.get("workspace_packages", []) or []:
                if not isinstance(wp, dict):
                    continue
                if target_low in str(wp.get("name", "")).lower() or any(
                    target_low in str(d).lower() for d in wp.get("internal_dependencies", []) or []
                ):
                    dependent_repos.add(repo_key)

        topo_matches: list[dict[str, Any]] = []
        for node in idx["topology"].get("items", []) or []:
            if not isinstance(node, dict):
                continue
            hay = json.dumps(node, sort_keys=True).lower()
            if target_low in hay:
                topo_matches.append(node)
                if node.get("repoName"):
                    dependent_repos.add(str(node["repoName"]))

        return {
            "target": target,
            "dependent_repositories": sorted(dependent_repos),
            "cross_workflow_edges": cross_edges,
            "shared_packages": shared_packages,
            "topology_matches": topo_matches,
        }

    def _tool_get_blast_radius(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_q = str(args.get("repository", "")).strip()
        target_node = args.get("target_node")
        scope = str(args.get("scope", "auto") or "auto").strip().lower()

        idx = self._load_index()
        rep_key = self._match_repo_key(repo_q, idx["reports"])
        pip_key = self._match_repo_key(repo_q, idx["pipelines"])

        if not rep_key and not pip_key:
            return {
                "found": False,
                "repository": repo_q,
                "error": f"Repository '{repo_q}' not found in exports.",
            }

        code_result: dict[str, Any] | None = None
        if rep_key and scope in {"auto", "code"}:
            rep = idx["reports"][rep_key]
            g_code = _build_component_digraph(
                rep.get("architecture_components", []) or [],
                metrics=rep.get("metrics") or {},
            )
            if g_code.number_of_nodes() > 0 or scope == "code":
                code_result = compute_component_blast_radius(
                    g_code, target_node=str(target_node) if target_node is not None else None
                )

        pipe_result: dict[str, Any] | None = None
        if scope in {"auto", "pipeline"}:
            workflows: list[dict[str, Any]] = []
            if pip_key:
                workflows = [
                    w for w in idx["pipelines"][pip_key].get("workflows", []) if isinstance(w, dict)
                ]
            elif rep_key:
                workflows = [
                    w for w in idx["reports"][rep_key].get("pipelines", []) if isinstance(w, dict)
                ]

            if workflows:
                g_pipe = nx.DiGraph()
                for wf in workflows:
                    raw_jobs = wf.get("jobs")
                    if isinstance(raw_jobs, dict):
                        wf_g = build_workflow_dag(wf)
                        for n, ndata in wf_g.nodes(data=True):
                            g_pipe.add_node(str(n), **ndata)
                        for u, v in wf_g.edges():
                            g_pipe.add_edge(str(u), str(v))
                    elif isinstance(raw_jobs, list):
                        for job in raw_jobs:
                            if not isinstance(job, dict) or not job.get("id"):
                                continue
                            jid = str(job["id"])
                            g_pipe.add_node(jid, **job)
                        for job in raw_jobs:
                            if not isinstance(job, dict) or not job.get("id"):
                                continue
                            jid = str(job["id"])
                            needs = job.get("needs", [])
                            if isinstance(needs, str):
                                needs = [needs]
                            for dep in needs if isinstance(needs, list) else []:
                                if str(dep) in g_pipe:
                                    g_pipe.add_edge(str(dep), jid)
                pipe_result = compute_blast_radius(
                    g_pipe, target_node=str(target_node) if target_node is not None else None
                )

        response: dict[str, Any] = {
            "found": True,
            "repository": rep_key or pip_key,
            "scope": scope,
        }
        if target_node is not None:
            response["target_node"] = str(target_node)
        if code_result is not None:
            response["code_blast_radius"] = code_result
            if scope == "code" or (
                target_node is not None and code_result.get("target_found")
            ):
                response["blast_radius_count"] = code_result.get("blast_radius_count", 0)
                response["blast_radius_pct"] = code_result.get("blast_radius_pct", 0.0)
        if pipe_result is not None:
            response["pipeline_blast_radius"] = pipe_result
            if scope == "pipeline" or (
                "blast_radius_count" not in response
                and target_node is not None
                and str(target_node) in (pipe_result.get("downstream_impact") or {})
            ):
                response["blast_radius_count"] = pipe_result.get("blast_radius_count", 0)
                response["blast_radius_pct"] = pipe_result.get("blast_radius_pct", 0.0)
        return response

    def _tool_trace_entrypoint_chain(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_q = str(args.get("repository", "")).strip()
        ep_filter = str(args.get("entrypoint") or "").strip().lower()
        idx = self._load_index()
        rep_key = self._match_repo_key(repo_q, idx["reports"])
        if not rep_key:
            return {
                "found": False,
                "repository": repo_q,
                "error": f"Architecture report not found for '{repo_q}'.",
            }

        rep = idx["reports"][rep_key]
        components = rep.get("architecture_components", []) or []
        g_code = _build_component_digraph(components, metrics=rep.get("metrics") or {})

        entrypoint_types = {"API_ROUTE", "CLI_COMMAND", "UI_COMPONENT"}
        entrypoints = [
            n
            for n in sorted(g_code.nodes())
            if (
                str(g_code.nodes[n].get("type", "")) in entrypoint_types
                or (ep_filter and ep_filter in n.lower())
            )
            and (not ep_filter or ep_filter in n.lower())
        ]

        chains: list[dict[str, Any]] = []
        for ep in entrypoints:
            # BFS shortest paths from entrypoint to downstream components
            queue: deque[list[str]] = deque([[ep]])
            visited: set[str] = {ep}
            paths: list[list[str]] = []
            while queue:
                path = queue.popleft()
                curr = path[-1]
                succs = sorted(g_code.successors(curr))
                unvisited_succs = [s for s in succs if s not in visited]
                if not unvisited_succs and len(path) > 1:
                    paths.append(path)
                for nxt in unvisited_succs:
                    visited.add(nxt)
                    queue.append([*path, nxt])
            reachable = sorted(nx.descendants(g_code, ep))
            chains.append({
                "entrypoint": ep,
                "type": g_code.nodes[ep].get("type", ""),
                "file": g_code.nodes[ep].get("file", ""),
                "reachable_components": reachable,
                "paths": paths or [[ep]],
            })

        return {
            "found": True,
            "repository": rep.get("repository", rep_key),
            "entrypoints_count": len(chains),
            "chains": chains,
            "code_to_cloud_edges": rep.get("code_to_cloud_edges", []),
        }

    def _tool_get_security_findings(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_filter = str(args.get("repository") or "").strip().lower()
        sev_filter = str(args.get("severity") or "").strip().upper()
        idx = self._load_index()

        findings: list[dict[str, Any]] = []

        for rep_key, rep in sorted(idx["reports"].items()):
            if (
                repo_filter
                and repo_filter not in rep_key.lower()
                and repo_filter != rep_key.split("/")[-1].lower()
            ):
                continue
            for v in rep.get("vulnerabilities", []) or []:
                if not isinstance(v, dict):
                    continue
                sev = str(v.get("severity", "MEDIUM")).upper()
                if sev_filter and sev != sev_filter:
                    continue
                findings.append({
                    "repository": rep_key,
                    "category": "vulnerability",
                    "rule_id": str(v.get("id", "ATRUSS-CVE")),
                    "severity": sev,
                    "package": v.get("package", ""),
                    "fixed_version": v.get("fixed_version"),
                    "file_source": v.get("manifest_file", ""),
                    "line": v.get("line", 1),
                    "message": v.get("summary", ""),
                })
            for sec in rep.get("secrets", []) or []:
                if not isinstance(sec, dict):
                    continue
                sev = str(sec.get("severity", "HIGH")).upper()
                if sev_filter and sev != sev_filter:
                    continue
                findings.append({
                    "repository": rep_key,
                    "category": "secret",
                    "rule_id": str(sec.get("rule_id", "ATRUSS-SEC-001")),
                    "severity": sev,
                    "file_source": sec.get("file_source", ""),
                    "line": sec.get("start_line", 1),
                    "message": sec.get("message", ""),
                })

        for pip_key, pdata in sorted(idx["pipelines"].items()):
            if (
                repo_filter
                and repo_filter not in pip_key.lower()
                and repo_filter != pip_key.split("/")[-1].lower()
            ):
                continue
            for wf in pdata.get("workflows", []) or []:
                if not isinstance(wf, dict):
                    continue
                for ap in wf.get("anti_patterns", []) or []:
                    if not isinstance(ap, dict):
                        continue
                    ap_type = str(ap.get("type", "")).upper()
                    if ap_type not in SECURITY_PIPELINE_ANTIPATTERNS:
                        continue
                    sev = str(ap.get("severity", "HIGH")).upper()
                    if sev_filter and sev != sev_filter:
                        continue
                    findings.append({
                        "repository": pip_key,
                        "category": "pipeline_security",
                        "rule_id": str(ap.get("rule_id", "")),
                        "type": ap_type,
                        "severity": sev,
                        "file_source": ap.get("file_source") or wf.get("id", ""),
                        "line": ap.get("start_line", 1),
                        "message": ap.get("message", ""),
                    })

        findings.sort(
            key=lambda f: (f["repository"], f["severity"], f["category"], f["rule_id"])
        )
        return {"count": len(findings), "findings": findings}

    def _tool_query_antipatterns(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_filter = str(args.get("repository") or "").strip().lower()
        rule_filter = str(args.get("rule_id") or "").strip().upper()
        type_filter = str(args.get("type") or "").strip().upper()
        sev_filter = str(args.get("severity") or "").strip().upper()
        idx = self._load_index()

        items: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str, str, int]] = set()

        def _maybe_add(entry: dict[str, Any]) -> None:
            if (
                repo_filter
                and repo_filter not in entry["repository"].lower()
                and repo_filter != entry["repository"].split("/")[-1].lower()
            ):
                return
            if rule_filter and entry["rule_id"].upper() != rule_filter:
                return
            if type_filter and entry["type"].upper() != type_filter:
                return
            if sev_filter and entry["severity"].upper() != sev_filter:
                return
            dedup = (
                entry["repository"],
                entry["rule_id"],
                entry["type"],
                entry["message"],
                int(entry.get("start_line", 1) or 1),
            )
            if dedup not in seen:
                seen.add(dedup)
                items.append(entry)

        for pip_key, pdata in sorted(idx["pipelines"].items()):
            for wf in pdata.get("workflows", []) or []:
                if not isinstance(wf, dict):
                    continue
                for ap in wf.get("anti_patterns", []) or []:
                    if not isinstance(ap, dict):
                        continue
                    _maybe_add({
                        "repository": pip_key,
                        "source": "pipeline",
                        "workflow": str(wf.get("id") or wf.get("name") or ""),
                        "rule_id": str(ap.get("rule_id", "")),
                        "type": str(ap.get("type", "")),
                        "severity": str(ap.get("severity", "MEDIUM")).upper(),
                        "file_source": str(ap.get("file_source") or wf.get("id") or ""),
                        "start_line": int(ap.get("start_line", 1) or 1),
                        "message": str(ap.get("message", "")),
                    })

        for rep_key, rep in sorted(idx["reports"].items()):
            for wf in rep.get("pipelines", []) or []:
                if not isinstance(wf, dict):
                    continue
                for ap in wf.get("anti_patterns", []) or []:
                    if not isinstance(ap, dict):
                        continue
                    _maybe_add({
                        "repository": rep_key,
                        "source": "pipeline",
                        "workflow": str(wf.get("id") or wf.get("name") or ""),
                        "rule_id": str(ap.get("rule_id", "")),
                        "type": str(ap.get("type", "")),
                        "severity": str(ap.get("severity", "MEDIUM")).upper(),
                        "file_source": str(ap.get("file_source") or wf.get("id") or ""),
                        "start_line": int(ap.get("start_line", 1) or 1),
                        "message": str(ap.get("message", "")),
                    })
            for fv in rep.get("fitness_violations", []) or []:
                if not isinstance(fv, dict):
                    continue
                _maybe_add({
                    "repository": rep_key,
                    "source": "architecture",
                    "workflow": "",
                    "rule_id": str(fv.get("rule_id", "")),
                    "type": str(fv.get("type", "")),
                    "severity": str(fv.get("severity", "HIGH")).upper(),
                    "file_source": str(fv.get("file_source") or ""),
                    "start_line": int(fv.get("start_line", 1) or 1),
                    "message": str(fv.get("message", "")),
                })

        items.sort(key=lambda i: (i["repository"], i["rule_id"], i["type"], i["start_line"]))
        return {"count": len(items), "antipatterns": items}

    def _tool_get_repo_scorecard(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_q = str(args.get("repository", "")).strip()
        idx = self._load_index()
        rep_key = self._match_repo_key(repo_q, idx["reports"])
        pip_key = self._match_repo_key(repo_q, idx["pipelines"])

        if not rep_key and not pip_key:
            return {
                "found": False,
                "repository": repo_q,
                "error": f"Repository '{repo_q}' not found in exports.",
            }

        rep = idx["reports"].get(rep_key, {}) if rep_key else {}
        if isinstance(rep.get("scorecard"), dict):
            return {
                "found": True,
                "repository": rep.get("repository", rep_key),
                "scorecard": rep["scorecard"],
            }

        pipes = (
            idx["pipelines"][pip_key].get("workflows", [])
            if pip_key
            else rep.get("pipelines", [])
        )
        computed = compute_repository_scorecard(
            metrics=rep.get("metrics") or {},
            components=rep.get("architecture_components") or [],
            pipelines=pipes,
            dependencies=rep.get("dependencies") or [],
            vulnerabilities=rep.get("vulnerabilities") or [],
            secrets=rep.get("secrets") or [],
            fitness_violations=rep.get("fitness_violations") or [],
        )
        return {
            "found": True,
            "repository": rep.get("repository", rep_key or pip_key),
            "scorecard": computed.model_dump(),
        }

    def _tool_check_boundary_violation(self, args: dict[str, Any]) -> dict[str, Any]:
        repo_q = str(args.get("repository", "")).strip()
        policy_path = args.get("policy_path")
        idx = self._load_index()
        rep_key = self._match_repo_key(repo_q, idx["reports"])

        if not rep_key:
            return {
                "found": False,
                "repository": repo_q,
                "error": f"Architecture report not found for '{repo_q}'.",
            }

        rep = idx["reports"][rep_key]
        base_components = [
            dict(c) for c in (rep.get("architecture_components") or []) if isinstance(c, dict)
        ]
        metrics = rep.get("metrics") or {}
        existing_violations, existing_summary = evaluate_architecture_fitness(
            base_components, metrics=metrics, policy_path=policy_path
        )

        src_comp = str(args.get("source_component") or "").strip()
        dst_comp = str(args.get("target_component") or "").strip()
        src_layer = str(args.get("source_layer") or "").strip()
        dst_layer = str(args.get("target_layer") or "").strip()

        if src_comp and dst_comp:
            sim_components = [dict(c) for c in base_components]
            by_name = {c.get("name"): c for c in sim_components}
            if src_comp not in by_name:
                new_src = {
                    "name": src_comp,
                    "type": src_layer or "SERVICE",
                    "file": f"{src_comp}.py",
                    "dependencies": [dst_comp],
                }
                sim_components.append(new_src)
            else:
                deps = list(by_name[src_comp].get("dependencies") or [])
                if dst_comp not in deps:
                    deps.append(dst_comp)
                by_name[src_comp]["dependencies"] = deps
                if src_layer:
                    by_name[src_comp]["type"] = src_layer

            if dst_comp not in by_name:
                sim_components.append({
                    "name": dst_comp,
                    "type": dst_layer or "DATA_ACCESS_LAYER",
                    "file": f"{dst_comp}.py",
                    "dependencies": [],
                })
            elif dst_layer:
                by_name[dst_comp]["type"] = dst_layer

            sim_violations, sim_summary = evaluate_architecture_fitness(
                sim_components, metrics=metrics, policy_path=policy_path
            )
            existing_sigs = {
                (v.rule_id, v.source_component, v.target_component) for v in existing_violations
            }
            introduced = [
                v.model_dump()
                for v in sim_violations
                if (v.rule_id, v.source_component, v.target_component) not in existing_sigs
            ]
            return {
                "found": True,
                "repository": rep.get("repository", rep_key),
                "passed": sim_summary["passed"],
                "candidate_edge": f"{src_comp} -> {dst_comp}",
                "candidate_violated": len(introduced) > 0,
                "new_violations": introduced,
                "existing_violations": [v.model_dump() for v in existing_violations],
                "violation_count": sim_summary["violation_count"],
            }

        return {
            "found": True,
            "repository": rep.get("repository", rep_key),
            "passed": existing_summary["passed"],
            "violation_count": existing_summary["violation_count"],
            "violations": [v.model_dump() for v in existing_violations],
        }

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        args = arguments if isinstance(arguments, dict) else {}
        dispatch = {
            "list_repositories": self._tool_list_repositories,
            "get_repo_architecture": self._tool_get_repo_architecture,
            "get_pipeline_dag": self._tool_get_pipeline_dag,
            "find_cross_repo_impacts": self._tool_find_cross_repo_impacts,
            "get_blast_radius": self._tool_get_blast_radius,
            "trace_entrypoint_chain": self._tool_trace_entrypoint_chain,
            "get_security_findings": self._tool_get_security_findings,
            "query_antipatterns": self._tool_query_antipatterns,
            "get_repo_scorecard": self._tool_get_repo_scorecard,
            "check_boundary_violation": self._tool_check_boundary_violation,
        }
        handler = dispatch.get(name)
        if handler is None:
            raise KeyError(f"Unknown MCP tool: {name}")
        return handler(args)

    def handle_message(self, msg: dict[str, Any]) -> dict[str, Any] | None:
        if not isinstance(msg, dict):
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Invalid Request"},
            }

        req_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params") if isinstance(msg.get("params"), dict) else {}

        if not isinstance(method, str) or not method:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": "Invalid Request: missing method"},
            }

        # Notifications without an `id` do not receive a JSON-RPC response
        if method.startswith("notifications/") and req_id is None:
            return None

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": MCP_PROTOCOL_VERSION,
                    "capabilities": {
                        "tools": {"listChanged": False},
                    },
                    "serverInfo": {
                        "name": "atruss-code-atlas",
                        "version": "0.1.0",
                    },
                },
            }

        if method in {"notifications/initialized", "initialized", "ping"}:
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": _TOOL_DEFINITIONS},
            }

        if method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments") or {}
            if not isinstance(tool_name, str) or not tool_name:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": "Invalid params: missing tool name"},
                }
            try:
                payload = self.call_tool(tool_name, tool_args)
            except KeyError as exc:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": str(exc)},
                }
            except Exception as exc:
                err_payload = {"error": str(exc)}
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(err_payload, indent=2)}],
                        "structuredContent": err_payload,
                        "isError": True,
                    },
                }

            is_error = payload.get("found") is False
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(payload, indent=2)}],
                    "structuredContent": payload,
                    "isError": is_error,
                },
            }

        if req_id is None:
            return None

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }

    @staticmethod
    def _read_framed_message(stdin: TextIO | BinaryIO) -> tuple[str | None, bool]:
        while True:
            raw_line = stdin.readline()
            if not raw_line:
                return None, False
            is_bytes = isinstance(raw_line, (bytes, bytearray))
            line_str = (
                bytes(raw_line).decode("utf-8", errors="replace") if is_bytes else str(raw_line)
            )
            if line_str.strip():
                break

        if line_str.lower().startswith("content-length:"):
            try:
                content_length = int(line_str.split(":", 1)[1].strip())
            except ValueError:
                return "", True

            while True:
                hdr = stdin.readline()
                if not hdr:
                    break
                hdr_str = (
                    bytes(hdr).decode("utf-8", errors="replace")
                    if isinstance(hdr, (bytes, bytearray))
                    else str(hdr)
                )
                if hdr_str.strip() == "":
                    break

            if is_bytes:
                buf = bytearray()
                while len(buf) < content_length:
                    chunk = stdin.read(content_length - len(buf))
                    if not chunk:
                        break
                    if isinstance(chunk, str):
                        buf.extend(chunk.encode("utf-8"))
                    else:
                        buf.extend(chunk)
                return buf.decode("utf-8", errors="replace"), True

            text_buf: list[str] = []
            remaining = content_length
            while remaining > 0:
                chunk = stdin.read(remaining)
                if not chunk:
                    break
                chunk_str = (
                    bytes(chunk).decode("utf-8", errors="replace")
                    if isinstance(chunk, (bytes, bytearray))
                    else str(chunk)
                )
                text_buf.append(chunk_str)
                remaining -= len(chunk_str)
            return "".join(text_buf), True

        return line_str.strip(), False

    @staticmethod
    def _write_framed_message(
        stdout: TextIO | BinaryIO,
        payload: dict[str, Any],
        use_content_length: bool,
    ) -> None:
        serialized = json.dumps(payload)
        is_text_out = isinstance(stdout, io.TextIOBase)
        if use_content_length:
            body_bytes = serialized.encode("utf-8")
            header = f"Content-Length: {len(body_bytes)}\r\n\r\n"
            if is_text_out:
                stdout.write(header + serialized)  # type: ignore[arg-type]
            else:
                stdout.write(header.encode("ascii") + body_bytes)  # type: ignore[arg-type]
        else:
            if is_text_out:
                stdout.write(serialized + "\n")  # type: ignore[arg-type]
            else:
                stdout.write((serialized + "\n").encode("utf-8"))  # type: ignore[arg-type]
        stdout.flush()

    def serve_stdio(
        self,
        stdin: TextIO | BinaryIO | None = None,
        stdout: TextIO | BinaryIO | None = None,
    ) -> None:
        in_stream: TextIO | BinaryIO = (
            stdin if stdin is not None else getattr(sys.stdin, "buffer", sys.stdin)
        )
        out_stream: TextIO | BinaryIO = (
            stdout if stdout is not None else getattr(sys.stdout, "buffer", sys.stdout)
        )

        while True:
            raw_body, use_content_length = self._read_framed_message(in_stream)
            if raw_body is None:
                break
            if not raw_body:
                self._write_framed_message(
                    out_stream,
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error: empty payload"},
                    },
                    use_content_length,
                )
                continue

            try:
                msg = json.loads(raw_body)
            except json.JSONDecodeError as exc:
                self._write_framed_message(
                    out_stream,
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": f"Parse error: {exc}"},
                    },
                    use_content_length,
                )
                continue

            response = self.handle_message(msg)
            if response is not None:
                self._write_framed_message(out_stream, response, use_content_length)


_EXPORTS_DIR_OPT = typer.Option(
    Path("exports/latest"),
    "--exports-dir",
    help="Path to archival exports directory (e.g. exports/latest)",
)
_TRANSPORT_OPT = typer.Option(
    "stdio",
    "--transport",
    help="MCP transport protocol (stdio)",
)


@app.command("mcp")
def mcp(
    exports_dir: Path = _EXPORTS_DIR_OPT,
    transport: str = _TRANSPORT_OPT,
) -> None:
    """Run the read-only Atruss Code Atlas Model Context Protocol (MCP) server (FR-029)."""
    if transport.strip().lower() != "stdio":
        typer.echo(
            f"Error: Unsupported MCP transport '{transport}'. Only 'stdio' is supported.",
            err=True,
        )
        raise typer.Exit(1)
    server = AtrussMCPServer(exports_dir)
    server.serve_stdio()
