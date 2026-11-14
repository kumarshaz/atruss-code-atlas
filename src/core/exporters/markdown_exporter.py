from collections import defaultdict
from pathlib import Path

from src.core.services.report_generator import (
    _mermaid_label,
    _mermaid_safe_id,
    generate_arc42_markdown,
)
from src.core.utils.export_manager import ExportManager
from src.models.artifacts import PortableArtifact
from src.models.topology import TopologyNode, WorkflowRun

MAX_DETAILED_WORKFLOWS = 3
MAX_DETAILED_JOBS = 18
MAX_OVERVIEW_WORKFLOWS = 8


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
    lines = ["```mermaid", "graph TD;"]

    if not artifact.pipelines:
        lines.append("  NoWorkflows[No Workflows Detected]")
        lines.append("```")
        return "\n".join(lines)

    total_jobs = sum(len(p.jobs) for p in artifact.pipelines)
    if len(artifact.pipelines) > MAX_DETAILED_WORKFLOWS or total_jobs > MAX_DETAILED_JOBS:
        # Render Top-Level Pipeline Tree so large repositories remain crisp and vertical (TD)
        repo_id = "pipeline_root"
        repo_lbl = f"{_mermaid_label(artifact.repository)} ({len(artifact.pipelines)} workflows)"
        lines.append(f'  {repo_id}(["{repo_lbl}"])')
        grouped: dict[str, list[tuple[int, str, int]]] = defaultdict(list)
        for wf_idx, pipeline in enumerate(artifact.pipelines):
            pl_name = pipeline.name or f"Workflow {wf_idx + 1}"
            raw_triggers = getattr(pipeline, "triggers", None)
            triggers = list(raw_triggers) if isinstance(raw_triggers, list) else []
            group = _classify_workflow_group(pl_name, triggers)
            grouped[group].append((wf_idx, pl_name, len(pipeline.jobs)))

        emitted_wfs = 0
        omitted = 0
        show_categories_only = len(artifact.pipelines) > 5 and len(grouped) > 1
        for g_idx, (group_name, entries) in enumerate(
            sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0]))
        ):
            grp_id = f"grp_{g_idx}_{_mermaid_safe_id(group_name)}"
            total_cat_jobs = sum(job_count for _, _, job_count in entries)
            cat_lbl = (
                f"{_mermaid_label(group_name)} "
                f"({len(entries)} workflows · {total_cat_jobs} jobs)"
            )
            lines.append(f'  {grp_id}["{cat_lbl}"]')
            lines.append(f"  {repo_id} --> {grp_id}")
            if show_categories_only:
                continue
            for wf_idx, pl_name, job_count in entries:
                if emitted_wfs >= MAX_OVERVIEW_WORKFLOWS:
                    omitted += 1
                    continue
                wf_node = f"wf_{wf_idx}_{_mermaid_safe_id(pl_name)}"
                lines.append(f'  {wf_node}["{_mermaid_label(pl_name)} ({job_count} jobs)"]')
                lines.append(f"  {grp_id} --> {wf_node}")
                emitted_wfs += 1

        if omitted > 0:
            lines.append(f'  wf_more["+{omitted} more workflows"]')
            lines.append(f"  {repo_id} --> wf_more")

        lines.append("```")
        return "\n".join(lines)

    repo_id = "pipeline_root"
    if len(artifact.pipelines) > 1:
        lines.append(f'  {repo_id}(["{_mermaid_label(artifact.repository)}"])')

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
            lines.append(f'    {safe_job}["{_mermaid_label(str(job_name))}"]')
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
            lines.append(f'    {entry_id}(["Trigger: {_mermaid_label(pl_name)}"])')
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
            sections.append(f"- **{key}**: {value}")

        if artifact.architecture_components:
            sections.append("")
            sections.append(
                generate_arc42_markdown(
                    artifact.repository,
                    artifact.architecture_components,
                    metrics=None,
                    ecosystem=artifact.ecosystem,
                    sha=artifact.sha,
                    include_frontmatter=False,
                )
            )

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

        # Build strict 3-subgraphs with ASCII-safe node IDs
        lines.append("    subgraph Workflows")
        lines.append("        direction TB")
        unique_workflows: set[str] = set()
        for r in runs:
            wid = _mermaid_safe_id(f"wf_{r.repo_name}_{r.workflow_name}")
            if wid not in unique_workflows:
                wf_lbl = f"{_mermaid_label(r.workflow_name)} ({_mermaid_label(r.repo_name)})"
                lines.append(f'        {wid}["{wf_lbl}"]')
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
                lines.append(f'        {tid}["{_mermaid_label(r.target_env)}"]')
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
                lines.append(f'        {resid}["{_mermaid_label(r.resource)}"]')
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
