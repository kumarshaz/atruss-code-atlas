from pathlib import Path

import pytest

from src.analyzers.classification import (
    Ecosystem,
    classify_repository,
    detect_monorepo_modules,
)


@pytest.fixture
def mock_python_repo_files():
    return ["requirements.txt", "setup.py", ".github/workflows/pytest.yml"]


@pytest.fixture
def mock_dotnet_repo_files():
    return ["Project.sln", "src/Program.cs", ".github/workflows/dotnet.yml"]


def test_classify_python_ecosystem(mock_python_repo_files):
    result = classify_repository(mock_python_repo_files)
    assert result.ecosystem == Ecosystem.PYTHON
    assert result.framework == "Unknown"  # Until specific framework signal matches
    assert result.signals["HasPipeline"] is True
    assert result.signals["HasDockerfile"] is False


def test_classify_dotnet_ecosystem(mock_dotnet_repo_files):
    result = classify_repository(mock_dotnet_repo_files)
    assert result.ecosystem == Ecosystem.DOTNET
    assert result.display_language == ".NET"
    assert result.signals["HasPipeline"] is True


def test_classify_unknown_ecosystem():
    result = classify_repository(["random.md", "script.sh"])
    assert result.ecosystem == Ecosystem.UNKNOWN
    assert result.framework == "Unknown"
    assert result.documentation_priority == "P4"


def test_classify_nested_java_springboot_and_signals():
    files = [
        "services/orders/pom.xml",
        "services/orders/src/main/java/com/acme/OrdersApplication.java",
        "services/orders/src/main/java/com/acme/controllers/OrderController.java",
        "services/orders/src/main/resources/application.yml",
        "Dockerfile",
        "k8s/deployment.yaml",
        ".github/workflows/ci.yml",
    ]
    result = classify_repository(files)
    assert result.ecosystem == Ecosystem.JAVA_SPRINGBOOT
    assert result.framework == "Spring Boot"
    assert result.signals["HasAPI"] is True
    assert result.signals["HasDockerfile"] is True
    assert result.signals["HasKubernetes"] is True
    assert result.signals["HasPipeline"] is True
    assert result.documentation_priority == "P1"
    assert "Docker" in result.technology_stack
    assert "CI/CD" in result.technology_stack
    assert "Kubernetes" in result.technology_stack


def test_classify_react_ts_with_package_json_content():
    files = [
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/vite.config.ts",
        "frontend/src/components/App.tsx",
    ]
    contents = {
        "frontend/package.json": '{"dependencies": {"react": "^18.2.0", "vite": "^5.0.0"}}'
    }
    result = classify_repository(files, file_contents=contents)
    assert result.ecosystem == Ecosystem.REACT_TS_JS
    assert result.framework == "React (Vite)"
    assert result.signals["HasFrontend"] is True


def test_monorepo_module_detection():
    files = [
        "client/package.json",
        "client/src/App.tsx",
        "server/requirements.txt",
        "server/app.py",
        "infra/main.tf",
        ".github/workflows/deploy.yml",
    ]
    modules = detect_monorepo_modules(files)
    assert len(modules) >= 2
    module_ecos = {m.path: m.ecosystem for m in modules}
    assert module_ecos["client"] == Ecosystem.REACT_TS_JS
    assert module_ecos["server"] == Ecosystem.PYTHON

    overall = classify_repository(files)
    assert overall.ecosystem == Ecosystem.PYTHON  # Tie-break: Java > .NET > Python > JS/TS
    assert "Terraform" in overall.technology_stack


def test_policy_as_code_custom_yaml_manifest(tmp_path: Path):
    """Verify FR-001: adding a framework rule in YAML changes classification with zero Python edits."""
    custom_manifest = tmp_path / "custom_ecosystems.yaml"
    custom_manifest.write_text(
        """
version: "1.0"
ecosystems:
  - id: python
    display_name: "Python"
    priority: 80
    manifest_patterns:
      - "(^|/)pyproject\\\\.toml$"
    extension_patterns:
      - "\\\\.py$"
    path_signals: []
    frameworks:
      - name: "Litestar"
        path_patterns:
          - "(^|/)litestar_app\\\\.py$"
        content_patterns: []
discovery_signals:
  HasPipeline:
    - "\\\\.github/workflows/"
deployable_mappings: {}
stack_mappings: {}
documentation_priority:
  p1_min_releases: 3
""",
        encoding="utf-8",
    )
    result = classify_repository(
        ["pyproject.toml", "litestar_app.py"],
        manifest_path=custom_manifest,
    )
    assert result.ecosystem == Ecosystem.PYTHON
    assert result.framework == "Litestar"


@pytest.mark.asyncio
async def test_discover_handles_truncated_and_empty_trees(caplog):
    """Verify FR-002: GitHubClient flags truncated=True and discover falls back gracefully."""
    import logging

    import httpx

    from src.cli.commands.discover import _analyze_discovered_repo
    from src.core.http_client import GitHubClient

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/repos/acme/huge/git/trees/main":
            return httpx.Response(
                200,
                json={
                    "sha": "truncsha",
                    "truncated": True,
                    "tree": [{"type": "blob", "path": "README.md"}],
                },
            )
        if request.url.path == "/repos/acme/empty/git/trees/main":
            return httpx.Response(404, json={"message": "Not Found"})
        if request.url.path == "/repos/acme/empty/git/trees/master":
            return httpx.Response(409, json={"message": "Git Repository is empty."})
        return httpx.Response(404)

    logger = logging.getLogger("test_truncated_tree")
    with caplog.at_level(logging.WARNING, logger="test_truncated_tree"):
        async with GitHubClient(
            logger=logger, transport=httpx.MockTransport(handler)
        ) as client:
            trunc_item = await _analyze_discovered_repo(
                client,
                "acme",
                {
                    "id": 1,
                    "name": "huge",
                    "owner": {"login": "acme", "id": 10},
                    "default_branch": "main",
                    "language": "Python",
                },
                "2026-11-12",
                logger,
            )
            assert client.last_tree_truncated is True
            assert trunc_item.PrimaryLanguage == "Python"

            empty_item = await _analyze_discovered_repo(
                client,
                "acme",
                {
                    "id": 2,
                    "name": "empty",
                    "owner": {"login": "acme", "id": 10},
                    "default_branch": "main",
                    "language": "C#",
                },
                "2026-11-12",
                logger,
            )
            assert client.last_tree_truncated is False
            assert empty_item.PrimaryLanguage == "C#"

    assert any("truncated" in rec.message.lower() for rec in caplog.records)
