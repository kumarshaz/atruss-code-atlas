from dataclasses import dataclass
from typing import Any

@dataclass
class DiscoveryManifestItem:
    """
    Dynamic representation mapped to Github payloads.
    Provides generic `to_dict()` ensuring dynamic CSV bindings.
    """
    Organization: str
    Project: str
    ProjectId: str
    RepositoryName: str
    RepositoryId: str
    DefaultBranch: str
    CloneUrl: str
    SshUrl: str
    WebUrl: str
    Size: int
    IsDisabled: bool
    IsPrivate: bool
    LastUpdate: str
    PrimaryLanguage: str
    FrameworkType: str
    AllFrameworks: str
    DeployableTypes: str
    HasAPI: bool
    HasService: bool
    HasFrontend: bool
    HasDatabase: bool
    TechnologyStack: str
    HasDockerfile: bool
    HasPipeline: bool
    HasKubernetes: bool
    DocumentationPriority: str
    AnalyzedDate: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
