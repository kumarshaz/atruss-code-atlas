from pathlib import Path
from src.models.artifacts import PortableArtifact

class MarkdownExporter:
    """Exports structured PortableArtifact objects securely to human-readable Markdown docs-as-code."""
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_mermaid_dag(self, artifact: PortableArtifact) -> str:
        """Generates a Mermaid graph from the pipeline DAG structures."""
        lines = ["```mermaid", "graph TD;"]
        
        for pipeline in artifact.pipelines:
            pl_name = pipeline.name or "Unnamed"
            lines.append(f'  subgraph {pl_name}')
            for job_name, job_data in pipeline.jobs.items():
                lines.append(f'    {job_name}["{job_name}"]')
            lines.append("  end")
        
        lines.append("```")
        return "\n".join(lines)
    
    def export(self, artifact: PortableArtifact) -> str:
        """Serializes the artifact bounding deterministic formatting."""
        safe_repo = artifact.repository.replace("/", "_").replace("\\", "_")
        filename = f"{safe_repo}_{artifact.sha}_report.md"
        
        target_path = self.output_dir / filename
        
        md_content = f"""# Repository Architecture Analysis: {artifact.repository}

## Metadata
- **SHA**: `{artifact.sha}`
- **Primary Ecosystem**: {artifact.ecosystem}

## Quality Metrics
"""
        for key, value in artifact.metrics.items():
            md_content += f"- **{key}**: {value}\n"
            
        md_content += "\n## CI/CD Pipeline Topology\n\n"
        md_content += self._generate_mermaid_dag(artifact)
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        return str(target_path)
