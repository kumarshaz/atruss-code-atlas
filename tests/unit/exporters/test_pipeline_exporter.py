import csv
import json
from pathlib import Path

from src.core.exporters.markdown_exporter import _render_pipeline_mermaid
from src.core.exporters.pipeline_exporter import TopologyArchiver
from src.core.utils.export_manager import ExportManager
from src.models.artifacts import PipelineWorkflow, PortableArtifact
from src.models.topology import TopologyNode, WorkflowRun


def test_pipeline_dag_edges_envelope(tmp_path: Path):
    """
    T011: Evaluates that internal DAG representations cleanly embed
    into the required JSON envelope arrays and strictly flattened CSV mappings.
    """
    manager = ExportManager(base_dir=str(tmp_path))
    archiver = TopologyArchiver(manager)

    nodes = [
        TopologyNode(
            repoId="234",
            repoName="my-repo",
            workflowId=99,
            workflowName="deploy-prd",
            environmentNames=["prod-west"],
            deploymentTargetId=44,
            deploymentTargetType="environment",
            deploymentTargetName="prod-west",
            linkageMethod="workflow-environment",
            resourceNames=["k8s-cluster"],
        )
    ]

    runs = [
        WorkflowRun(
            repo_name="my-repo",
            workflow_name="deploy-prd",
            target_env="prod-west",
            resource="k8s-cluster",
        )
    ]

    archiver.export(nodes, runs)

    json_path = manager.get_path("relationships", "pipeline_topology.json")
    csv_path = manager.get_path("relationships", "pipeline_topology.csv")

    assert json_path.exists()
    assert csv_path.exists()

    with open(json_path, encoding="utf-8") as jf:
        data = json.load(jf)
        assert data["count"] == 1
        assert data["items"][0]["linkageMethod"] == "workflow-environment"
        assert data["items"][0]["resourceNames"] == ["k8s-cluster"]

    with open(csv_path, encoding="utf-8", newline="") as cf:
        reader = csv.DictReader(cf)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["DeploymentTarget"] == "prod-west"


def test_repo_pipeline_astro_contract_and_latest_sync(tmp_path: Path):
    """Verify per-repo `pipelines/{org}-{repo}-pipeline.json` matches Astro PipelineView schema."""
    manager = ExportManager(base_dir=str(tmp_path))
    archiver = TopologyArchiver(manager)

    workflows = [
        {
            "id": "ci.yml",
            "name": "CI",
            "triggers": ["push"],
            "jobs": [
                {"id": "test", "name": "Test", "runner": "ubuntu-latest", "steps_count": 3, "needs": []},
                {"id": "deploy", "name": "Deploy", "runner": "ubuntu-latest", "steps_count": 2, "needs": ["test"]},
            ],
            "anti_patterns": [],
        }
    ]
    out_file = archiver.export_repo_pipeline(
        org="acme",
        repo="web-app",
        sha="deadbeef",
        workflows=workflows,
        analyzed_at="2026-11-12T00:00:00Z",
    )
    manager.publish_to_latest(["pipelines"])

    latest_file = tmp_path / "latest" / "pipelines" / "acme-web-app-pipeline.json"
    assert out_file.exists()
    assert latest_file.exists()

    parsed = json.loads(latest_file.read_text(encoding="utf-8"))
    assert parsed["analyzed_at"] == "2026-11-12T00:00:00Z"
    assert parsed["workflows"][0]["jobs"][1]["needs"] == ["test"]


def test_render_pipeline_mermaid_large_multi_workflow_tree():
    """Large multi-workflow repos render categorized TD overview trees."""
    artifact = PortableArtifact(
        repository="acme/big-ci",
        sha="deadbeef",
        ecosystem="python",
        pipelines=[
            PipelineWorkflow(
                name="CI Checks",
                triggers=["push", "pull_request"],
                jobs={"lint": {}, "test": {}},
            ),
            PipelineWorkflow(name="CodeQL Security", triggers=["push"], jobs={"analyze": {}}),
            PipelineWorkflow(
                name="Release Package",
                triggers=["release"],
                jobs={"build": {}, "publish": {}},
            ),
            PipelineWorkflow(name="Nightly Cron", triggers=["schedule"], jobs={"sweep": {}}),
            PipelineWorkflow(
                name="Docs Sync",
                triggers=["workflow_dispatch"],
                jobs={"docs": {}},
            ),
        ],
    )

    mermaid = _render_pipeline_mermaid(artifact)
    assert "graph TD;" in mermaid
    assert 'pipeline_root(["acme/big-ci (5 workflows)"])' in mermaid
    assert "CI & Verification" in mermaid
    assert "Security & Governance" in mermaid
    assert "Release & Deploy" in mermaid
    assert "Scheduled & Manual" in mermaid
    assert "subgraph" not in mermaid
