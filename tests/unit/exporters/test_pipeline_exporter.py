import json
import csv
from pathlib import Path
from src.core.utils.export_manager import ExportManager
from src.models.topology import TopologyNode, WorkflowRun
from src.core.exporters.pipeline_exporter import TopologyArchiver

def test_pipeline_dag_edges_envelope(tmp_path: Path):
    """
    T011: Evaluates that internal DAG representations cleanly embed
    into the required JSON envelope arrays and strictly flattened CSV mappings.
    """
    manager = ExportManager(base_dir=str(tmp_path))
    archiver = TopologyArchiver(manager)
    
    nodes = [
        TopologyNode(
            repoId="234", repoName="my-repo", workflowId=99, workflowName="deploy-prd",
            environmentNames=["prod-west"], deploymentTargetId=44, 
            deploymentTargetType="environment", deploymentTargetName="prod-west",
            linkageMethod="workflow-environment", resourceNames=["k8s-cluster"]
        )
    ]
    
    runs = [
        WorkflowRun(repo_name="my-repo", workflow_name="deploy-prd", target_env="prod-west", resource="k8s-cluster")
    ]
    
    archiver.export(nodes, runs)
    
    json_path = manager.get_path("relationships", "pipeline_topology.json")
    csv_path = manager.get_path("relationships", "pipeline_topology.csv")
    
    assert json_path.exists()
    assert csv_path.exists()
    
    with open(json_path, "r", encoding="utf-8") as jf:
        data = json.load(jf)
        assert data["count"] == 1
        assert data["items"][0]["linkageMethod"] == "workflow-environment"
        assert data["items"][0]["resourceNames"] == ["k8s-cluster"]
        
    with open(csv_path, "r", encoding="utf-8", newline="") as cf:
        reader = csv.DictReader(cf)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["DeploymentTarget"] == "prod-west"
