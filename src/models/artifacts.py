from typing import Any

from pydantic import BaseModel, Field


class AntiPatternFinding(BaseModel):
    rule_id: str = ""
    type: str
    severity: str
    message: str
    entity_type: str = "PIPELINE"
    file_source: str | None = None
    start_line: int = 1
    end_line: int = 1
    remediation: str | None = None


class FitnessViolation(BaseModel):
    rule_id: str
    type: str
    severity: str
    message: str
    source_component: str
    target_component: str
    source_layer: str = ""
    target_layer: str = ""
    file_source: str | None = None
    start_line: int = 1
    end_line: int = 1


class WorkspacePackage(BaseModel):
    name: str
    path: str
    ecosystem: str
    manager: str = ""
    internal_dependencies: list[str] = Field(default_factory=list)


class CrossWorkflowEdge(BaseModel):
    source_workflow: str
    source_job: str = ""
    target_workflow: str
    edge_type: str = "workflow_call"


class DependencyRecord(BaseModel):
    name: str
    version: str = ""
    ecosystem: str
    purl: str
    manifest_file: str
    line: int = 1
    is_direct: bool = True
    license: str | None = None
    is_outdated: bool = False
    latest_version: str | None = None
    vulnerability_ids: list[str] = Field(default_factory=list)


class VulnerabilityRecord(BaseModel):
    id: str
    package: str
    purl: str
    installed_version: str = ""
    fixed_version: str | None = None
    severity: str = "MEDIUM"
    cvss_score: float | None = None
    summary: str = ""
    reachability: str = "UNREACHABLE_DORMANT"
    manifest_file: str = ""
    line: int = 1


class SecretFinding(BaseModel):
    rule_id: str = "ATRUSS-SEC-001"
    type: str = "HARDCODED_SECRET"
    severity: str = "HIGH"
    file_source: str
    start_line: int = 1
    end_line: int = 1
    redacted_snippet: str = ""
    entropy: float = 0.0
    message: str = ""


class ScorecardDimension(BaseModel):
    name: str
    score: float
    grade: str
    weight: float
    details: str = ""


class RepositoryScorecard(BaseModel):
    overall_score: float
    overall_grade: str
    technical_debt_score: float
    remediation_hours: float = 0.0
    dimensions: dict[str, ScorecardDimension] = Field(default_factory=dict)


class CodeToCloudEdge(BaseModel):
    source: str
    source_type: str
    target: str
    target_type: str
    relationship: str


class PipelineWorkflow(BaseModel):
    id: str | None = None
    path: str | None = None
    name: str | None = None
    triggers: list[str] = Field(default_factory=list)
    jobs: dict[str, dict[str, Any]] = Field(default_factory=dict)
    job_nodes: list[dict[str, Any]] = Field(default_factory=list)
    dag_metrics: dict[str, Any] = Field(default_factory=dict)
    findings: list[str] = Field(default_factory=list)
    anti_patterns: list[dict[str, Any]] = Field(default_factory=list)
    cross_workflow_edges: list[dict[str, Any]] = Field(default_factory=list)
    blast_radius: dict[str, Any] = Field(default_factory=dict)


class PortableArtifact(BaseModel):
    repository: str
    sha: str
    ecosystem: str
    metrics: dict[str, Any] = Field(default_factory=dict)
    pipelines: list[PipelineWorkflow] = Field(default_factory=list)
    architecture_components: list[dict[str, Any]] = Field(default_factory=list)
    scorecard: RepositoryScorecard | None = None
    dependencies: list[DependencyRecord] = Field(default_factory=list)
    vulnerabilities: list[VulnerabilityRecord] = Field(default_factory=list)
    secrets: list[SecretFinding] = Field(default_factory=list)
    fitness_violations: list[FitnessViolation] = Field(default_factory=list)
    code_to_cloud_edges: list[CodeToCloudEdge] = Field(default_factory=list)
    workspace_packages: list[WorkspacePackage] = Field(default_factory=list)
    observability: dict[str, Any] = Field(default_factory=dict)


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
