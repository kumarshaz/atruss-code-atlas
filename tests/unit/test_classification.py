import pytest

from src.analyzers.classification import Ecosystem, classify_repository


@pytest.fixture
def mock_python_repo_files():
    return ["requirements.txt", "setup.py", ".github/workflows/pytest.yml"]

@pytest.fixture
def mock_dotnet_repo_files():
    return ["Project.sln", "src/Program.cs", ".github/workflows/dotnet.yml"]

def test_classify_python_ecosystem(mock_python_repo_files):
    result = classify_repository(mock_python_repo_files)
    assert result.ecosystem == Ecosystem.PYTHON
    assert result.framework == "Unknown" # Until specific parser runs

def test_classify_dotnet_ecosystem(mock_dotnet_repo_files):
    result = classify_repository(mock_dotnet_repo_files)
    assert result.ecosystem == Ecosystem.DOTNET

def test_classify_unknown_ecosystem():
    result = classify_repository(["random.md", "script.sh"])
    assert result.ecosystem == Ecosystem.UNKNOWN
