import pytest
import os
from src.core.exporters.yaml_exporter import YAMLExporter
from src.models.artifacts import DiscoveryManifestItem

def test_yaml_exporter_discovery(tmp_path):
    exporter = YAMLExporter()
    manifest = [
        DiscoveryManifestItem(name="repo1", clone_url="https://r1", ecosystem="Python")
    ]
    
    out_file = tmp_path / "out.yaml"
    exporter.export_discovery(manifest, str(out_file))
    
    assert out_file.exists()
    content = out_file.read_text()
    assert "repo1" in content
