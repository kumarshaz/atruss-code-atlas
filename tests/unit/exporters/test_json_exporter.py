import pytest
import os
import json
from src.core.exporters.json_exporter import JSONExporter
from src.models.artifacts import DiscoveryManifestItem

def test_json_exporter_discovery(tmp_path):
    exporter = JSONExporter()
    manifest = [
        DiscoveryManifestItem(name="repo1", clone_url="https://r1", ecosystem="Python")
    ]
    
    out_file = tmp_path / "out.json"
    exporter.export_discovery(manifest, str(out_file))
    
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert isinstance(data, list)
    assert data[0]["name"] == "repo1"
