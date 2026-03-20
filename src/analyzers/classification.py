from dataclasses import dataclass
from enum import Enum


class Ecosystem(str, Enum):
    PYTHON = "python"
    DOTNET = ".net"
    REACT_TS_JS = "react_ts_js"
    JAVA_SPRINGBOOT = "java_springboot"
    UNKNOWN = "unknown"

@dataclass
class ClassificationResult:
    ecosystem: Ecosystem
    framework: str

def classify_repository(file_paths: list[str]) -> ClassificationResult:
    """Classifies a repository based on the presence of manifest files."""

    if "requirements.txt" in file_paths or "pyproject.toml" in file_paths or "setup.py" in file_paths:
        return ClassificationResult(ecosystem=Ecosystem.PYTHON, framework="Unknown")

    for path in file_paths:
        if path.endswith(".sln") or path.endswith(".csproj") or path.endswith(".fsproj"):
            return ClassificationResult(ecosystem=Ecosystem.DOTNET, framework="Unknown")

    if "package.json" in file_paths:
        return ClassificationResult(ecosystem=Ecosystem.REACT_TS_JS, framework="Unknown")

    if "pom.xml" in file_paths or "build.gradle" in file_paths:
        return ClassificationResult(ecosystem=Ecosystem.JAVA_SPRINGBOOT, framework="Unknown")

    return ClassificationResult(ecosystem=Ecosystem.UNKNOWN, framework="Unknown")
