import pytest

from src.analyzers.pipeline.dag_builder import build_workflow_dag
from src.analyzers.pipeline.heuristics import find_untested_deployments


@pytest.fixture
def mock_dag_workflow():
    return {
        "jobs": {
            "build": {},
            "test": {"needs": "build"},
            "deploy_prod": {}
        }
    }

def test_dag_builder(mock_dag_workflow):
    G = build_workflow_dag(mock_dag_workflow)
    assert G.number_of_nodes() == 3
    assert G.number_of_edges() == 1
    assert ("build", "test") in G.edges

def test_anti_patterns(mock_dag_workflow):
    G = build_workflow_dag(mock_dag_workflow)
    findings = find_untested_deployments(G)
    assert len(findings) == 1
    assert "deploy_prod" in findings[0]
