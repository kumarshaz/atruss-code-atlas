from dataclasses import dataclass, field
from typing import Optional, Any

@dataclass
class TopologyNode:
    repoId: str
    repoName: str
    workflowId: int
    workflowName: str
    environmentNames: list[str] = field(default_factory=list)
    deploymentTargetId: int = 0
    deploymentTargetType: str = ""
    deploymentTargetName: str = ""
    linkageMethod: str = ""
    iisConfig: Optional[str] = None
    k8sContext: Optional[str] = None
    resourceNames: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

@dataclass
class WorkflowRun:
    repo_name: str
    workflow_name: str
    target_env: str
    resource: str

    def to_csv_dict(self) -> dict[str, str]:
        return {
            "RepoName": self.repo_name,
            "WorkflowName": self.workflow_name,
            "DeploymentTarget": self.target_env,
            "DeploymentResource": self.resource
        }
