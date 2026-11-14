from pathlib import Path

from typer.testing import CliRunner

from src.analyzers.code.dotnet_structural import analyze_dotnet_structural
from src.analyzers.code.java_structural import analyze_java_structural
from src.analyzers.code.js_ts_structural import analyze_js_ts_structural
from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.analyzers.code.python_ast import analyze_python_with_metrics
from src.cli.commands.analyze_code import app as analyze_code_app
from src.core.services.report_generator import generate_arc42_markdown


def test_arc42_generation():
    components = [
        {"name": "api_gateway", "type": "API_ROUTE", "dependencies": ["database"]},
        {"name": "database", "type": "DATA_ACCESS_LAYER", "dependencies": []},
    ]
    markdown = generate_arc42_markdown("TestRepo", components)

    assert "# Architecture: TestRepo" in markdown
    assert "## Building Block View" in markdown
    assert "```mermaid" in markdown
    assert "graph TD;" in markdown
    assert "api_gateway --> database" in markdown


def test_arc42_frontmatter_and_mermaid_sanitization():
    components = [
        {"name": "GET_/api/v1/pets", "type": "API_ROUTE", "dependencies": ["Pets.Service"]},
        {"name": "Pets.Service", "type": "SERVICE", "dependencies": []},
    ]
    md_with_fm = generate_arc42_markdown(
        "acme/pets",
        components,
        metrics={"files_analyzed": 2, "loc": 40, "sloc": 32},
        ecosystem="TypeScript/React",
        framework="Next.js",
        sha="abc1234",
        include_frontmatter=True,
    )
    assert md_with_fm.startswith("---\ntitle: Architecture — acme/pets\n")
    assert "## Quality & Complexity Metrics" in md_with_fm
    assert "- **files_analyzed**: 2" in md_with_fm
    assert "GET__api_v1_pets --> Pets_Service" in md_with_fm

    md_no_fm = generate_arc42_markdown("acme/pets", components, include_frontmatter=False)
    assert not md_no_fm.startswith("---")


def test_python_ast_with_metrics(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='py-svc'\n", encoding="utf-8")
    (tmp_path / "models.py").write_text(
        "from pydantic import BaseModel\n\nclass PetModel(BaseModel):\n    name: str\n",
        encoding="utf-8",
    )
    (tmp_path / "routes.py").write_text(
        "from fastapi import APIRouter\n"
        "from models import PetModel\n"
        "router = APIRouter()\n\n"
        "@router.get('/pets')\n"
        "def list_pets(flag: bool = False):\n"
        "    if flag:\n"
        "        return []\n"
        "    return [PetModel.__name__]\n",
        encoding="utf-8",
    )

    components, metrics = analyze_python_with_metrics(tmp_path)
    names = {c["name"]: c for c in components}
    assert "PetModel" in names and names["PetModel"]["type"] == "DATA_ACCESS_LAYER"
    assert "list_pets" in names and names["list_pets"]["type"] == "API_ROUTE"
    assert "PetModel" in names["list_pets"]["dependencies"]
    assert metrics["files_analyzed"] == 2
    assert metrics["loc"] > 0
    assert metrics["avg_cyclomatic_complexity"] >= 1.0


def test_dotnet_structural_analyzer(tmp_path: Path):
    (tmp_path / "OrderApi.csproj").write_text(
        '<Project Sdk="Microsoft.NET.Sdk.Web">\n'
        '  <ItemGroup><ProjectReference Include="../OrderCore/OrderCore.csproj" /></ItemGroup>\n'
        '</Project>\n',
        encoding="utf-8",
    )
    (tmp_path / "OrderController.cs").write_text(
        "[ApiController]\n"
        "public class OrderController : ControllerBase {\n"
        "    private readonly OrderService _svc;\n"
        "    public void Get() { if (true) {} }\n"
        "}\n"
        "public class OrderService {}\n"
        "public class OrderDbContext : DbContext {}\n"
        'app.MapGet("/health", () => "ok");\n',
        encoding="utf-8",
    )

    components, metrics = analyze_dotnet_structural(tmp_path)
    by_name = {c["name"]: c for c in components}
    assert by_name["OrderApi"]["type"] == "MODULE"
    assert "OrderCore" in by_name["OrderApi"]["dependencies"]
    assert by_name["OrderController"]["type"] == "API_ROUTE"
    assert "OrderService" in by_name["OrderController"]["dependencies"]
    assert by_name["OrderService"]["type"] == "SERVICE"
    assert by_name["OrderDbContext"]["type"] == "DATA_ACCESS_LAYER"
    assert any(c["type"] == "API_ROUTE" and "health" in c["name"] for c in components)
    assert metrics["files_analyzed"] == 1
    assert metrics["loc"] > 0


def test_js_ts_structural_analyzer(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        '{"name": "pets-web", "dependencies": {"react": "^18.0.0", "next": "^14.0.0"}}',
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "PetService.ts").write_text(
        "export class PetService {\n  fetchAll() { return []; }\n}\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "PetCard.tsx").write_text(
        "import { PetService } from './PetService';\n"
        "export function PetCard() { return null; }\n",
        encoding="utf-8",
    )
    api_dir = tmp_path / "src" / "app" / "api" / "pets"
    api_dir.mkdir(parents=True)
    (api_dir / "route.ts").write_text(
        "export async function GET() { return new Response('ok'); }\n",
        encoding="utf-8",
    )

    components, metrics = analyze_js_ts_structural(tmp_path)
    by_name = {c["name"]: c for c in components}
    assert by_name["pets-web"]["type"] == "MODULE"
    assert by_name["PetCard"]["type"] == "UI_COMPONENT"
    assert by_name["PetService"]["type"] == "SERVICE"
    assert "PetService" in by_name["PetCard"]["dependencies"]
    assert any(c["type"] == "API_ROUTE" for c in components)
    assert metrics["files_analyzed"] == 3


def test_java_structural_analyzer(tmp_path: Path):
    (tmp_path / "pom.xml").write_text(
        "<project><artifactId>pet-clinic</artifactId>"
        "<dependencies><dependency><artifactId>spring-boot-starter-web</artifactId></dependency></dependencies>"
        "</project>",
        encoding="utf-8",
    )
    java_dir = tmp_path / "src" / "main" / "java" / "com" / "acme"
    java_dir.mkdir(parents=True)
    (java_dir / "PetRepository.java").write_text(
        "@Repository\npublic interface PetRepository {}\n",
        encoding="utf-8",
    )
    (java_dir / "PetService.java").write_text(
        "@Service\npublic class PetService {\n    private final PetRepository repo;\n}\n",
        encoding="utf-8",
    )
    (java_dir / "PetController.java").write_text(
        "@RestController\npublic class PetController {\n    private final PetService svc;\n}\n",
        encoding="utf-8",
    )

    components, metrics = analyze_java_structural(tmp_path)
    by_name = {c["name"]: c for c in components}
    assert by_name["pet-clinic"]["type"] == "MODULE"
    assert by_name["PetController"]["type"] == "API_ROUTE"
    assert "PetService" in by_name["PetController"]["dependencies"]
    assert by_name["PetService"]["type"] == "SERVICE"
    assert "PetRepository" in by_name["PetService"]["dependencies"]
    assert by_name["PetRepository"]["type"] == "DATA_ACCESS_LAYER"
    assert metrics["files_analyzed"] == 3


def test_monorepo_orchestrator_and_cli_exports_frontmatter(tmp_path: Path):
    repo_dir = tmp_path / "polyglot-app"
    backend = repo_dir / "services" / "api"
    frontend = repo_dir / "apps" / "web"
    backend.mkdir(parents=True)
    frontend.mkdir(parents=True)

    (backend / "requirements.txt").write_text("fastapi\n", encoding="utf-8")
    (backend / "main.py").write_text(
        "from fastapi import FastAPI\napp = FastAPI()\n"
        "@app.get('/ping')\ndef ping(): return 'pong'\n",
        encoding="utf-8",
    )
    (frontend / "package.json").write_text(
        '{"name": "web-ui", "dependencies": {"react": "^18.0.0"}}',
        encoding="utf-8",
    )
    (frontend / "App.tsx").write_text("export const App = () => null;\n", encoding="utf-8")

    result = orchestrate_full_analysis(repo_dir)
    comp_names = {c["name"] for c in result.components}
    assert "ping" in comp_names
    assert "App" in comp_names
    assert len(result.modules) == 2
    assert result.metrics["files_analyzed"] >= 2

    exports_dir = tmp_path / "exports"
    runner = CliRunner()
    res = runner.invoke(
        analyze_code_app,
        ["--path", str(repo_dir), "--exports-dir", str(exports_dir)],
    )
    assert res.exit_code == 0, res.output
    md_file = exports_dir / "latest" / "reports" / "local-polyglot-app-report.md"
    json_file = exports_dir / "latest" / "reports" / "local-polyglot-app-analysis.json"
    assert md_file.exists()
    assert json_file.exists()
    assert md_file.read_text(encoding="utf-8").startswith("---\ntitle: Architecture")


def test_arc42_large_repo_top_level_tree_traversal():
    """Large repos (>25 components) emit bounded TD directory trees cleanly."""
    components = []
    submodules = ["api", "auth", "db", "models", "cli"]
    for i in range(80):
        sub = submodules[i % len(submodules)]
        dep = f"Comp_{i - 1}" if i > 0 and i % 4 == 0 else ""
        components.append(
            {
                "name": f"Comp_{i}",
                "type": "SERVICE" if i % 2 == 0 else "DATA_ACCESS_LAYER",
                "file": f"src/acme_pkg/{sub}/mod_{i // 5}.py",
                "dependencies": [dep] if dep else [],
            }
        )

    markdown = generate_arc42_markdown("acme/huge", components, ecosystem="python")

    assert "graph TD;" in markdown
    assert 'repo_root(["acme/huge (80 components)"])' in markdown
    assert "## Building Block View" in markdown
    # Compresses single-child src/acme_pkg wrapper directly to its module groups
    assert "src/acme_pkg/api (16)" in markdown
    assert "src/acme_pkg/auth (16)" in markdown
    # Keeps Component Details section bounded at MAX_DETAIL_ROWS (60)
    expected_hdr = "Showing top 60 representative components out of 80 across 5 module group(s):"
    assert expected_hdr in markdown
    detail_bullets = [line for line in markdown.splitlines() if line.startswith("- **Comp_")]
    assert len(detail_bullets) == 60
    # Ensures Mermaid payload stays compact well below Mermaid's maxTextSize (50k)
    mermaid_segment = markdown.split("```mermaid", 1)[1].split("```", 1)[0]
    assert len(mermaid_segment) < 5000
