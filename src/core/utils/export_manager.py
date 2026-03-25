import os
from datetime import datetime
from pathlib import Path

class ExportManager:
    """
    Handles deterministic hierarchical export structures: exports/{timestamp}/{module}/...
    """
    def __init__(self, base_dir: str = "exports"):
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.base_path = Path(base_dir) / self.timestamp
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Create the 8-phase topological bounds."""
        folders = [
            "repos",
            "pipelines",
            "runners",
            "environments",
            "relationships",
            "reports"
        ]
        for f in folders:
            (self.base_path / f).mkdir(parents=True, exist_ok=True)

    def get_path(self, module: str, filename: str) -> Path:
        """Get an absolute Path for a given module and file."""
        target = self.base_path / module / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        return target
