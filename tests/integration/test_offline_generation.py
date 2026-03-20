import pytest
import os
import json
from src.core.utils.json_exporter import JSONExporter
from src.models.artifacts import PortableArtifact

def test_json_exporter_offline_dump(tmp_path):
    """Test generating Portable Artifact strictly offline without databases."""
    artifact = PortableArtifact(
        repository="test/repo",
        sha="abcdef123456",
        ecosystem="PYTHON",
        metrics={"coverage": 80.5},
        pipelines=[],
        architecture_components=[]
    )
    
    exporter = JSONExporter(output_dir=str(tmp_path))
    output_path = exporter.export(artifact)
    
    assert os.path.exists(output_path)
    with open(output_path, "r") as f:
        data = json.load(f)
        assert data["repository"] == "test/repo"
        assert data["sha"] == "abcdef123456"

def test_markdown_exporter_offline_dump(tmp_path):
    """Test generating Portable Markdown Arc42 report offline."""
    from src.core.utils.markdown_exporter import MarkdownExporter
    
    artifact = PortableArtifact(
        repository="test/repo",
        sha="abcdef123456",
        ecosystem="PYTHON",
        metrics={"coverage": 80.5},
        pipelines=[],
        architecture_components=[]
    )
    
    exporter = MarkdownExporter(output_dir=str(tmp_path))
    output_path = exporter.export(artifact)
    
    assert os.path.exists(output_path)
    with open(output_path, "r") as f:
        content = f.read()
        assert "Repository Architecture Analysis: test/repo" in content
        assert "```mermaid" in content
