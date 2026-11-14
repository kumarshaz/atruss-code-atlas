from pathlib import Path

from src.core.exporters.json_exporter import JSONExporter as CanonicalJSONExporter
from src.models.artifacts import PortableArtifact


class JSONExporter:
    """Thin delegation wrapper to the canonical JSONExporter in `src.core.exporters`."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._canonical = CanonicalJSONExporter()

    def export(self, artifact: PortableArtifact) -> str:
        """Delegate PortableArtifact JSON serialization to the canonical exporter."""
        return self._canonical.export_artifact(artifact, self.output_dir)
