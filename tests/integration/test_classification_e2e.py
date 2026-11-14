from pathlib import Path

import pytest

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.orchestrator import orchestrate_full_analysis


@pytest.mark.integration
def test_tr_cls_multi_ecosystem_e2e_classification(tmp_path: Path):
    """TR-CLS E2E: validates YAML policy classification and priority tie-breaking across all 4 ecosystems."""
    py_cls = classify_repository(
        [
            "pyproject.toml",
            "app/main.py",
            "app/routers/pets.py",
            "app/models.py",
            "Dockerfile",
            ".github/workflows/ci.yml",
        ],
        file_contents={"pyproject.toml": "[project]\ndependencies = ['fastapi', 'sqlalchemy']\n"},
    )
    assert py_cls.ecosystem == Ecosystem.PYTHON
    assert py_cls.framework == "FastAPI"
    assert py_cls.signals["HasAPI"] is True
    assert py_cls.signals["HasDatabase"] is True
    assert py_cls.signals["HasDockerfile"] is True
    assert py_cls.signals["HasPipeline"] is True

    dotnet_cls = classify_repository(
        ["src/Orders.Api/Orders.Api.csproj", "src/Orders.Api/Controllers/OrderController.cs"],
        file_contents={
            "src/Orders.Api/Orders.Api.csproj": '<PackageReference Include="Microsoft.EntityFrameworkCore" />'
        },
    )
    assert dotnet_cls.ecosystem == Ecosystem.DOTNET
    assert dotnet_cls.display_language == ".NET"
    assert "ASP.NET Core" in dotnet_cls.all_frameworks

    react_cls = classify_repository(
        ["package.json", "tsconfig.json", "src/components/App.tsx", "k8s/deployment.yaml"],
        file_contents={
            "package.json": '{"dependencies": {"react": "^18.0.0", "next": "^14.0.0", "prisma": "^5.0.0"}}'
        },
    )
    assert react_cls.ecosystem == Ecosystem.REACT_TS_JS
    assert react_cls.framework == "Next.js"
    assert react_cls.signals["HasFrontend"] is True
    assert react_cls.signals["HasKubernetes"] is True

    # Polyglot tie-break: Java > .NET > Python > JS/TS
    poly_dir = tmp_path / "poly"
    (poly_dir / "backend").mkdir(parents=True)
    (poly_dir / "frontend").mkdir(parents=True)
    (poly_dir / "backend" / "pom.xml").write_text(
        "<project><artifactId>core-api</artifactId>"
        "<dependencies><dependency><artifactId>spring-boot-starter-web</artifactId></dependency></dependencies>"
        "</project>",
        encoding="utf-8",
    )
    (poly_dir / "frontend" / "package.json").write_text(
        '{"name": "ui", "dependencies": {"react": "^18.2.0"}}',
        encoding="utf-8",
    )
    result = orchestrate_full_analysis(poly_dir)
    assert result.ecosystem == "Java"
    assert len(result.modules) == 2
