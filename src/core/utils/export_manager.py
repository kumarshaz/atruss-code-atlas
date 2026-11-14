import shutil
from datetime import datetime
from pathlib import Path

STANDARD_EXPORT_MODULES = (
    "repos",
    "pipelines",
    "runners",
    "environments",
    "relationships",
    "reports",
)


class ExportManager:
    """
    Handles deterministic hierarchical export structures:
    exports/{timestamp}/{module}/... and synchronizes exports/latest/{module}/...
    """

    def __init__(self, base_dir: str = "exports", timestamp: str | None = None):
        self.root_dir = Path(base_dir)
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.base_path = self.root_dir / self.timestamp
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Create the archival module directories."""
        for folder in STANDARD_EXPORT_MODULES:
            (self.base_path / folder).mkdir(parents=True, exist_ok=True)

    def get_path(self, module: str, filename: str) -> Path:
        """Get a Path for a given module and filename inside the timestamped run."""
        target = self.base_path / module / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        return target

    def publish_to_latest(self, modules: list[str] | None = None) -> Path:
        """
        Sync exported modules into `{base_dir}/latest/{module}/` while preserving
        artifacts from other phases already present in `latest/`.
        """
        latest_dir = self.root_dir / "latest"

        # Materialize legacy symlinks so multi-step CLI runs accumulate cleanly.
        if latest_dir.is_symlink():
            old_target = latest_dir.resolve()
            latest_dir.unlink()
            latest_dir.mkdir(parents=True, exist_ok=True)
            if old_target.exists() and old_target.is_dir():
                for mod in STANDARD_EXPORT_MODULES:
                    src_mod = old_target / mod
                    dst_mod = latest_dir / mod
                    dst_mod.mkdir(parents=True, exist_ok=True)
                    if src_mod.exists():
                        for item in src_mod.iterdir():
                            if item.is_file():
                                shutil.copy2(item, dst_mod / item.name)
        else:
            latest_dir.mkdir(parents=True, exist_ok=True)

        for folder in STANDARD_EXPORT_MODULES:
            (latest_dir / folder).mkdir(parents=True, exist_ok=True)

        target_modules = modules if modules is not None else list(STANDARD_EXPORT_MODULES)
        for mod in target_modules:
            src_mod = self.base_path / mod
            dst_mod = latest_dir / mod
            dst_mod.mkdir(parents=True, exist_ok=True)
            if not src_mod.exists():
                continue
            for item in src_mod.iterdir():
                if item.is_file():
                    shutil.copy2(item, dst_mod / item.name)
                elif item.is_dir():
                    shutil.copytree(item, dst_mod / item.name, dirs_exist_ok=True)

        return latest_dir
