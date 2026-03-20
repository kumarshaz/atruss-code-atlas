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
