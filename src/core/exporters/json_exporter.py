import json
from pathlib import Path
from typing import Any

from src.models.artifacts import PortableArtifact

from .base_exporter import BaseExporter


class JSONExporter(BaseExporter):
    """Canonical JSON exporter for discovery, topology, and portable analysis artifacts."""

    def export_discovery(self, manifest: list[Any], output_path: str) -> None:
        data = [item.model_dump() for item in manifest]
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def export_pipeline(self, dag: Any, output_path: str) -> None:
        data = dag.model_dump()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def export_artifact(self, artifact: PortableArtifact, output_dir: Path | str) -> str:
        """Serialize a PortableArtifact deterministically to `output_dir`."""
        target_dir = Path(output_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        safe_repo = artifact.repository.replace("/", "_").replace("\\", "_")
        target_path = target_dir / f"{safe_repo}_{artifact.sha}_analysis.json"
        target_path.write_text(artifact.model_dump_json(indent=2), encoding="utf-8")
        return str(target_path)
