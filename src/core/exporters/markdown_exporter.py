from collections import defaultdict
from pathlib import Path

from src.core.services.report_generator import (
    MERMAID_CLASS_DEFS,
    _format_metric_value,
    _mermaid_label,
    _mermaid_safe_id,
    generate_arc42_markdown,
    render_horizon2_sections_markdown,
)
from src.core.utils.export_manager import ExportManager
from src.models.artifacts import PortableArtifact
from src.models.topology import TopologyNode, WorkflowRun

MAX_DETAILED_WORKFLOWS = 3
MAX_DETAILED_JOBS = 18
MAX_OVERVIEW_WORKFLOWS = 10
MAX_OVERVIEW_JOBS_PER_WF = 3
MAX_OVERVIEW_JOBS_TOTAL = 16


def _classify_workflow_group(wf_name: str, triggers: list[str]) -> str:
    """Assign a workflow to a concise top-level pipeline tier for tree summarization."""
    hay = f"{wf_name} {' '.join(triggers)}".lower()
    if any(k in hay for k in ("release", "publish", "deploy", "tag", "pages")):
        return "Release & Deploy"
    if any(
        k in hay for k in ("security", "codeql", "secret", "audit", "dependabot", "stale", "lock")
    ):
        return "Security & Governance"
    if any(k in hay for k in ("schedule", "nightly", "cron", "workflow_dispatch")):
        return "Scheduled & Manual"
    if any(
        k in hay for k in ("test", "ci", "lint", "build", "check", "pr", "pull_request", "push")
    ):
        return "CI & Verification"
    return "Automation & Other"


def _render_pipeline_mermaid(artifact: PortableArtifact) -> str:
    """Generate a bounded top-down (TD) Mermaid flowchart from an artifact's pipelines."""
    lines = ["```mermaid", "graph TD;", *MERMAID_CLASS_DEFS]

    if not artifact.pipelines:
        lines.append("  NoWorkflows[No Workflows Detected]:::atlasMore")
        lines.append("```")
        return "\n".join(lines)

    total_jobs = sum(len(p.jobs) for p in artifact.pipelines)
    if len(artifact.pipelines) > MAX_DETAILED_WORKFLOWS or total_jobs > MAX_DETAILED_JOBS:
        # Render Top-Level Pipeline Tree with representative workflows & key jobs so large repos
        # remain crisp, vertical (TD), and informative instead of collapsing to bare category boxes.
        repo_id = "pipeline_root"
        repo_lbl = f"{_mermaid_label(artifact.repository)} ({len(artifact.pipelines)} workflows)"
        lines.append(f'  {repo_id}(["{repo_lbl}"]):::atlasRoot')
        grouped: dict[str, list[tuple[int, str, dict[str, object]]]] = defaultdict(list)
        for wf_idx, pipeline in enumerate(artifact.pipelines):
            pl_name = pipeline.name or f"Workflow {wf_idx + 1}"
            raw_triggers = getattr(pipeline, "triggers", None)
            triggers = list(raw_triggers) if isinstance(raw_triggers, list) else []
            group = _classify_workflow_group(pl_name, triggers)
            jobs_dict = pipeline.jobs if isinstance(pipeline.jobs, dict) else {}
            grouped[group].append((wf_idx, pl_name, jobs_dict))

        sorted_groups = sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0]))
        # Pick up to MAX_OVERVIEW_WORKFLOWS round-robin across categories
        ranked_queues = [
            sorted(entries, key=lambda e: (-len(e[2]), e[1]))
            for _, entries in sorted_groups
        ]
        selected_wf_ids: set[int] = set()
        while len(selected_wf_ids) < MAX_OVERVIEW_WORKFLOWS:
            progressed = False
            for q in ranked_queues:
                if q and len(selected_wf_ids) < MAX_OVERVIEW_WORKFLOWS:
                    wf_idx, _, _ = q.pop(0)
                    selected_wf_ids.add(wf_idx)
                    progressed = True
            if not progressed:
                break

        emitted_jobs_total = 0
        omitted = 0
        for g_idx, (group_name, entries) in enumerate(sorted_groups):
            grp_id = f"grp_{g_idx}_{_mermaid_safe_id(group_name)}"
            total_cat_jobs = sum(len(jobs_dict) for _, _, jobs_dict in entries)
            cat_lbl = (
                f"{_mermaid_label(group_name)} "
                f"({len(entries)} workflows · {total_cat_jobs} jobs)"
            )
            lines.append(f'  {grp_id}["{cat_lbl}"]:::atlasCategory')
            lines.append(f"  {repo_id} --> {grp_id}")

            for wf_idx, pl_name, jobs_dict in entries:
                if wf_idx not in selected_wf_ids:
                    omitted += 1
                    continue
                wf_node = f"wf_{wf_idx}_{_mermaid_safe_id(pl_name)}"
                wf_lbl = f"{_mermaid_label(pl_name)} ({len(jobs_dict)} jobs)"
                lines.append(f'  {wf_node}["{wf_lbl}"]:::atlasWorkflow')
                lines.append(f"  {grp_id} --> {wf_node}")

                if jobs_dict and emitted_jobs_total < MAX_OVERVIEW_JOBS_TOTAL:
                    rem_budget = MAX_OVERVIEW_JOBS_TOTAL - emitted_jobs_total
                    budget = min(MAX_OVERVIEW_JOBS_PER_WF, rem_budget)
                    job_items = list(jobs_dict.items())[:budget]
                    job_id_map: dict[str, str] = {}
                    for j_name, _ in job_items:
                        j_id = f"job_{wf_idx}_{_mermaid_safe_id(str(j_name))}"
                        job_id_map[str(j_name)] = j_id
                        lines.append(f'  {j_id}["{_mermaid_label(str(j_name))}"]:::atlasJob')
                        emitted_jobs_total += 1
                    for j_name, j_data in job_items:
                        j_id = job_id_map[str(j_name)]
                        needs: list[str] = []
                        if isinstance(j_data, dict):
                            raw_needs = j_data.get("needs", [])
                            if isinstance(raw_needs, str):
                                needs = [raw_needs]
                            elif isinstance(raw_needs, list):
                                needs = [str(n) for n in raw_needs]
                        linked = False
                        for need in needs:
                            if need in job_id_map:
                                lines.append(f"  {job_id_map[need]} --> {j_id}")
                                linked = True
                        if not linked:
                            lines.append(f"  {wf_node} --> {j_id}")

        if omitted > 0:
            lines.append(f'  wf_more["+{omitted} more workflows"]:::atlasMore')
            lines.append(f"  {repo_id} --> wf_more")

        lines.append("```")
        return "\n".join(lines)

    repo_id = "pipeline_root"
    if len(artifact.pipelines) > 1:
        lines.append(f'  {repo_id}(["{_mermaid_label(artifact.repository)}"]):::atlasRoot')

    for wf_idx, pipeline in enumerate(artifact.pipelines):
        pl_name = pipeline.name or "Unnamed"
        safe_pl = f"{_mermaid_safe_id(pl_name)}_{wf_idx}"
        lines.append(f'  subgraph {safe_pl}["{_mermaid_label(pl_name)}"]')
        lines.append("    direction TB")
        entry_id = f"wf_entry_{wf_idx}"
        root_jobs: list[str] = []

        for job_name, job_data in pipeline.jobs.items():
            clean_job = _mermaid_safe_id(str(job_name))
            safe_job = f"{wf_idx}_{clean_job}"
            lines.append(f'    {safe_job}["{_mermaid_label(str(job_name))}"]:::atlasJob')
            needs: list[str] = []
            if isinstance(job_data, dict):
                raw_needs = job_data.get("needs", [])
                if isinstance(raw_needs, str):
                    needs = [raw_needs]
                elif isinstance(raw_needs, list):
                    needs = [str(n) for n in raw_needs]
            if needs:
                for need in needs:
                    safe_need = f"{wf_idx}_{_mermaid_safe_id(need)}"
                    lines.append(f"    {safe_need} --> {safe_job}")
            else:
                root_jobs.append(safe_job)

        if len(root_jobs) > 2:
            lines.append(f'    {entry_id}(["Trigger: {_mermaid_label(pl_name)}"]):::atlasWorkflow')
            for root_job in root_jobs:
                lines.append(f"    {entry_id} --> {root_job}")
            if len(artifact.pipelines) > 1:
                lines.append("  end")
                lines.append(f"  {repo_id} --> {entry_id}")
                continue
        lines.append("  end")
        if len(artifact.pipelines) > 1 and root_jobs:
            lines.append(f"  {repo_id} --> {root_jobs[0]}")

    lines.append("```")
    return "\n".join(lines)


class MarkdownArchiver:
    """Canonical Markdown exporter for aggregate topology and per-repo Arc42 reports."""

    def __init__(self, manager: ExportManager):
        self.manager = manager

    @staticmethod
    def export_artifact_markdown(
        artifact: PortableArtifact,
        output_dir: Path | str,
        filename: str | None = None,
        include_frontmatter: bool = False,
    ) -> str:
        """Render and write a per-repo Arc42 + Mermaid report to `output_dir`."""
        target_dir = Path(output_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        safe_repo = artifact.repository.replace("/", "_").replace("\\", "_")
        target_name = filename or f"{safe_repo}_{artifact.sha}_report.md"
        target_path = target_dir / target_name
        target_path.parent.mkdir(parents=True, exist_ok=True)

        sections: list[str] = []
        if include_frontmatter:
            sections.extend([
                "---",
                f"title: Architecture — {artifact.repository}",
                f"description: Arc42 and Pipeline report for {artifact.repository}",
                "---",
                "",
            ])

        sections.extend([
            f"# Repository Architecture Analysis: {artifact.repository}",
            "",
            "## Metadata",
            f"- **SHA**: `{artifact.sha}`",
            f"- **Primary Ecosystem**: {artifact.ecosystem}",
            "",
            "## Quality Metrics",
        ])
        for key, value in sorted(artifact.metrics.items()):
            sections.append(f"- **{key}**: {_format_metric_value(value)}")

        if artifact.architecture_components:
            sections.append("")
            sections.append(
                generate_arc42_markdown(
                    artifact.repository,
                    artifact.architecture_components,
                    metrics=None,
                    ecosystem=artifact.ecosystem,
                    framework=str(artifact.metrics.get("framework", "Unknown")),
                    sha=artifact.sha,
                    include_frontmatter=False,
                    scorecard=artifact.scorecard,
                    fitness_violations=artifact.fitness_violations,
                    dependencies=artifact.dependencies,
                    vulnerabilities=artifact.vulnerabilities,
                    secrets=artifact.secrets,
                    code_to_cloud_edges=artifact.code_to_cloud_edges,
                    workspace_packages=artifact.workspace_packages,
                    observability=artifact.observability,
                )
            )
        else:
            h2_lines = render_horizon2_sections_markdown(
                scorecard=artifact.scorecard,
                fitness_violations=artifact.fitness_violations,
                dependencies=artifact.dependencies,
                vulnerabilities=artifact.vulnerabilities,
                secrets=artifact.secrets,
                code_to_cloud_edges=artifact.code_to_cloud_edges,
                workspace_packages=artifact.workspace_packages,
                observability=artifact.observability,
            )
            if h2_lines:
                sections.append("")
                sections.extend(h2_lines)

        sections.extend([
            "",
            "## CI/CD Pipeline Topology",
            "",
            _render_pipeline_mermaid(artifact),
            "",
        ])

        target_path.write_text("\n".join(sections), encoding="utf-8")
        return str(target_path)

    def export(self, nodes: list[TopologyNode], runs: list[WorkflowRun]) -> None:
        """
        Compresses the pipeline outputs into the strict 3-subgraph Mermaid representation.
        """
        md_path = self.manager.get_path("reports", "pipeline_architecture.md")

        lines = [
            "---",
            "title: Aggregate Pipeline Architecture Report",
            "description: Cross-repository workflow dependency map generated by Atruss Code Atlas",
            "---",
            "",
            "# Pipeline Architecture Report",
            "",
            "## Dependencies Map",
        ]
        lines.append("```mermaid")
        lines.append("flowchart TD")
        lines.extend(MERMAID_CLASS_DEFS)

        # Build strict 3-subgraphs with ASCII-safe node IDs
        lines.append("    subgraph Workflows")
        lines.append("        direction TB")
        unique_workflows: set[str] = set()
        for r in runs:
            wid = _mermaid_safe_id(f"wf_{r.repo_name}_{r.workflow_name}")
            if wid not in unique_workflows:
                wf_lbl = f"{_mermaid_label(r.workflow_name)} ({_mermaid_label(r.repo_name)})"
                lines.append(f'        {wid}["{wf_lbl}"]:::atlasWorkflow')
                unique_workflows.add(wid)
        lines.append("    end")

        lines.append("    subgraph Targets")
        lines.append("        direction TB")
        unique_targets: set[str] = set()
        for r in runs:
            if not r.target_env:
                continue
            tid = _mermaid_safe_id(f"tgt_{r.target_env}")
            if tid not in unique_targets:
                lines.append(f'        {tid}["{_mermaid_label(r.target_env)}"]:::atlasTarget')
                unique_targets.add(tid)
        lines.append("    end")

        lines.append("    subgraph Resources")
        lines.append("        direction TB")
        unique_resources: set[str] = set()
        for r in runs:
            if not r.resource:
                continue
            resid = _mermaid_safe_id(f"res_{r.resource}")
            if resid not in unique_resources:
                lines.append(f'        {resid}["{_mermaid_label(r.resource)}"]:::atlasCategory')
                unique_resources.add(resid)
        lines.append("    end")

        lines.append("")
        seen_edges: set[str] = set()
        for r in runs:
            wid = _mermaid_safe_id(f"wf_{r.repo_name}_{r.workflow_name}")
            tid = _mermaid_safe_id(f"tgt_{r.target_env}") if r.target_env else ""
            resid = _mermaid_safe_id(f"res_{r.resource}") if r.resource else ""

            if tid:
                edge_deploy = f"    {wid} -->|deploy| {tid}"
                if edge_deploy not in seen_edges:
                    lines.append(edge_deploy)
                    seen_edges.add(edge_deploy)
                if resid:
                    edge_host = f"    {tid} -->|host| {resid}"
                    if edge_host not in seen_edges:
                        lines.append(edge_host)
                        seen_edges.add(edge_host)

        lines.append("```")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
