from typing import Any

from pydantic import BaseModel, Field


class PipelineWorkflow(BaseModel):
    id: str | None = None
    name: str | None = None
    triggers: list[str] = Field(default_factory=list)
    jobs: dict[str, dict[str, Any]] = Field(default_factory=dict)
    job_nodes: list[dict[str, Any]] = Field(default_factory=list)
    dag_metrics: dict[str, Any] = Field(default_factory=dict)
    findings: list[str] = Field(default_factory=list)
    anti_patterns: list[dict[str, str]] = Field(default_factory=list)


class PortableArtifact(BaseModel):
    repository: str
    sha: str
    ecosystem: str
    metrics: dict[str, Any] = Field(default_factory=dict)
    pipelines: list[PipelineWorkflow] = Field(default_factory=list)
    architecture_components: list[dict[str, Any]] = Field(default_factory=list)


class HarnessFixture(BaseModel):
    repo_url: str
    pinned_sha: str
    expected_modules: list[str] = Field(default_factory=list)


class DiscoveryManifestItem(BaseModel):
    name: str  # The repository name
    clone_url: str  # The clone URI
    ecosystem: str  # Detected ecosystem (e.g. Python, Node.js)


class Node(BaseModel):
    node_id: str
    name: str
    ecosystem_type: str = "pipeline"


class Edge(BaseModel):
    source: str  # node_id
    target: str  # node_id
    relationship: str = "needs"


class PipelineDAG(BaseModel):
    nodes: list[Node]
    edges: list[Edge]
