from pathlib import Path

from src.core.exporters.markdown_exporter import MarkdownArchiver
from src.models.artifacts import PortableArtifact


class MarkdownExporter:
    """Thin delegation wrapper to the canonical Markdown exporter in `src.core.exporters`."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        artifact: PortableArtifact,
        filename: str | None = None,
        include_frontmatter: bool = False,
    ) -> str:
        """Delegate PortableArtifact Markdown serialization to `MarkdownArchiver`."""
        return MarkdownArchiver.export_artifact_markdown(
            artifact=artifact,
            output_dir=self.output_dir,
            filename=filename,
            include_frontmatter=include_frontmatter,
        )
