import os
import json
from pathlib import Path
from src.models.artifacts import PortableArtifact

class JSONExporter:
    """Exports structured PortableArtifact objects securely to the filesystem."""
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def export(self, artifact: PortableArtifact) -> str:
        """Serializes the artifact bounding deterministic strings."""
        safe_repo = artifact.repository.replace("/", "_").replace("\\", "_")
        filename = f"{safe_repo}_{artifact.sha}_analysis.json"
        
        target_path = self.output_dir / filename
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(artifact.model_dump_json(indent=2))
            
        return str(target_path)
