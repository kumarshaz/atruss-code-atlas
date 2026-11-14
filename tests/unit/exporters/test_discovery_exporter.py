import json
import csv
from pathlib import Path
from src.core.utils.export_manager import ExportManager
from src.models.discovery import DiscoveryManifestItem

def test_dynamic_csv_and_json_columns(tmp_path: Path):
    """
    T007: Tests that dynamic key/value bindings operate seamlessly 
    from the domain model directly to structural formats.
    """
    from src.core.exporters.discovery_exporter import DiscoveryArchiver
    manager = ExportManager(base_dir=str(tmp_path))
    archiver = DiscoveryArchiver(manager)

    items = [
        DiscoveryManifestItem(
            Organization="TestOrg", Project="TestOrg", ProjectId="123",
            RepositoryName="test-repo", RepositoryId="456", DefaultBranch="main",
            CloneUrl="http", SshUrl="ssh", WebUrl="web", Size=10, IsDisabled=False,
            IsPrivate=True, LastUpdate="now", PrimaryLanguage="python",
            FrameworkType="backend", AllFrameworks="backend", DeployableTypes="svc",
            HasAPI=True, HasService=True, HasFrontend=False, HasDatabase=False,
            TechnologyStack="python", HasDockerfile=False, HasPipeline=True,
            HasKubernetes=False, DocumentationPriority="P1", AnalyzedDate="today"
        )
    ]

    archiver.export(items)

    csv_path = manager.get_path("repos", "repositories.csv")
    json_path = manager.get_path("repos", "repositories.json")

    assert csv_path.exists()
    assert json_path.exists()

    # JSON Validation
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["count"] == 1
        assert data["items"][0]["RepositoryName"] == "test-repo"

    # CSV Validation
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["Organization"] == "TestOrg"


def test_zero_length_structural_dumps(tmp_path: Path):
    """
    T007b: Test graceful empty generation preventing runtime exceptions.
    """
    from src.core.exporters.discovery_exporter import DiscoveryArchiver
    manager = ExportManager(base_dir=str(tmp_path))
    archiver = DiscoveryArchiver(manager)

    archiver.export([])

    csv_path = manager.get_path("repos", "repositories.csv")
    json_path = manager.get_path("repos", "repositories.json")

    assert csv_path.exists()
    assert json_path.exists()

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["count"] == 0
        assert data["items"] == []

    # CSV should still just have headers matching standard payload or fallback
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        # If no items, headers might drop or default
        reader = csv.reader(f)
        lines = list(reader)
        # Assuming we output empty file or just headers
        assert len(lines) <= 1
