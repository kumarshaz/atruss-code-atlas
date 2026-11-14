import pytest
import os
from src.core.exporters.csv_exporter import CSVExporter
from src.models.artifacts import DiscoveryManifestItem

def test_csv_exporter_discovery(tmp_path):
    exporter = CSVExporter()
    manifest = [
        DiscoveryManifestItem(name="repo1", clone_url="https://r1", ecosystem="Python"),
        DiscoveryManifestItem(name="repo2", clone_url="https://r2", ecosystem="JS")
    ]
    
    out_file = tmp_path / "out.csv"
    exporter.export_discovery(manifest, str(out_file))
    
    # Asserting file existence and expected generic rows
    assert out_file.exists()
    content = out_file.read_text()
    assert "repo1" in content
    assert "Python" in content
    assert "JS" in content
