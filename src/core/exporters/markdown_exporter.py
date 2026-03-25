from pathlib import Path
from src.core.utils.export_manager import ExportManager
from src.models.topology import TopologyNode, WorkflowRun

class MarkdownArchiver:
    def __init__(self, manager: ExportManager):
        self.manager = manager

    def export(self, nodes: list[TopologyNode], runs: list[WorkflowRun]) -> None:
        """
        Compresses the pipeline outputs into the strict 3-subgraph Mermaid representation.
        """
        md_path = self.manager.get_path("reports", "pipeline_architecture.md")
        
        lines = []
        lines.append("# Pipeline Architecture Report")
        lines.append("")
        lines.append("## Dependencies Map")
        lines.append("```mermaid")
        lines.append("flowchart TD")
        
        # Build strict 3-subgraphs 
        # 1. Workflows
        lines.append("    subgraph Workflows")
        unique_workflows = set()
        for r in runs:
            wid = r.workflow_name.replace(" ", "_").replace("-", "_").replace(".", "_")
            if wid not in unique_workflows:
                lines.append(f"        {wid}[\"{r.workflow_name} ({r.repo_name})\"]")
                unique_workflows.add(wid)
        lines.append("    end")
        
        # 2. Targets
        lines.append("    subgraph Targets")
        unique_targets = set()
        for r in runs:
            if not r.target_env: continue
            tid = r.target_env.replace(" ", "_").replace("-", "_")
            if tid not in unique_targets:
                lines.append(f"        {tid}[\"{r.target_env}\"]")
                unique_targets.add(tid)
        lines.append("    end")

        # 3. Resources
        lines.append("    subgraph Resources")
        unique_resources = set()
        for r in runs:
            if not r.resource: continue
            resid = r.resource.replace(" ", "_").replace("-", "_")
            if resid not in unique_resources:
                lines.append(f"        {resid}[\"{r.resource}\"]")
                unique_resources.add(resid)
        lines.append("    end")
        
        # Edges
        lines.append("")
        for r in runs:
            wid = r.workflow_name.replace(" ", "_").replace("-", "_").replace(".", "_")
            tid = r.target_env.replace(" ", "_").replace("-", "_")
            resid = r.resource.replace(" ", "_").replace("-", "_")
            
            if tid:
                lines.append(f"    {wid} -->|deploy| {tid}")
                if resid:
                    lines.append(f"    {tid} -->|host| {resid}")
                    
        lines.append("```")
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
