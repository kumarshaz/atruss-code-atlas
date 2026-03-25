from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PipelineWorkflow(BaseModel):
    name: str | None
    jobs: dict[str, dict]
    dag_metrics: dict[str, Any]
    findings: List[str]

class PortableArtifact(BaseModel):
    repository: str
    sha: str
    ecosystem: str
    metrics: Dict[str, Any]
    pipelines: List[PipelineWorkflow]
    architecture_components: List[dict]

class HarnessFixture(BaseModel):
    repo_url: str
    pinned_sha: str
    expected_modules: List[str]

class DiscoveryManifestItem(BaseModel):
    name: str # The repository name
    clone_url: str # The clone URI
    ecosystem: str # Detected ecosystem (e.g. Python, Node.js)

class Node(BaseModel):
    node_id: str
    name: str
    ecosystem_type: str = "pipeline"

class Edge(BaseModel):
    source: str # node_id
    target: str # node_id
    relationship: str = "needs"

class PipelineDAG(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
