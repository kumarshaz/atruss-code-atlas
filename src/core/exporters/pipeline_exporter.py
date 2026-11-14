import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.core.utils.export_manager import ExportManager
from src.models.topology import TopologyNode, WorkflowRun


class TopologyArchiver:
    def __init__(self, manager: ExportManager):
        self.manager = manager

    def export_repo_pipeline(
        self,
        org: str,
        repo: str,
        sha: str,
        workflows: list[dict[str, Any]],
        analyzed_at: str | None = None,
    ) -> Path:
        """
        Exports per-repository pipeline DAG & anti-pattern JSON matching Astro's
        `PipelineView.astro` and `LeaderboardView.astro` schema:
        `exports/{timestamp}/pipelines/{org}-{repo}-pipeline.json`.
        """
        safe_org = org.replace("/", "_") if org else "local"
        safe_repo = repo.split("/")[-1].replace("/", "_")
        filename = f"{safe_org}-{safe_repo}-pipeline.json"
        json_path = self.manager.get_path("pipelines", filename)

        payload = {
            "org": safe_org,
            "repository": safe_repo,
            "sha": sha,
            "analyzed_at": analyzed_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "workflows": workflows,
        }
        with open(json_path, "w", encoding="utf-8") as pf:
            json.dump(payload, pf, indent=2)
        return json_path

    def export(self, nodes: list[TopologyNode], runs: list[WorkflowRun]) -> None:
        """
        Exports the aggregate pipeline topology JSON, YAML, and CSV into
        `exports/{timestamp}/relationships/pipeline_topology.*`.
        """
        node_dicts = [n.to_dict() for n in nodes]
        envelope = {
            "count": len(node_dicts),
            "items": node_dicts,
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
                fieldnames=[
                    "RepoName",
                    "WorkflowName",
                    "DeploymentTarget",
                    "DeploymentResource",
                ],
            )
            writer.writeheader()
            for run in runs:
                writer.writerow(run.to_csv_dict())
