import json
import csv
import yaml
from pathlib import Path
from src.core.utils.export_manager import ExportManager
from src.models.topology import TopologyNode, WorkflowRun

class TopologyArchiver:
    def __init__(self, manager: ExportManager):
        self.manager = manager

    def export(self, nodes: list[TopologyNode], runs: list[WorkflowRun]) -> None:
        """
        Exports the extracted topologies directly natively mirroring the ADO-parity envelopes.
        """
        node_dicts = [n.to_dict() for n in nodes]
        envelope = {
            "count": len(node_dicts),
            "items": node_dicts
        }
        
        # 1. JSON
        json_path = self.manager.get_path("relationships", "pipeline_topology.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(envelope, jf, indent=2)

        # 2. YAML
        yaml_path = self.manager.get_path("relationships", "pipeline_topology.yaml")
        with open(yaml_path, "w", encoding="utf-8") as yf:
            yaml.dump(envelope, yf, default_flow_style=False, sort_keys=False)

        # 3. CSV
        csv_path = self.manager.get_path("relationships", "pipeline_topology.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as cf:
            writer = csv.DictWriter(
                cf, 
                fieldnames=["RepoName", "WorkflowName", "DeploymentTarget", "DeploymentResource"]
            )
            writer.writeheader()
            for run in runs:
                writer.writerow(run.to_csv_dict())
