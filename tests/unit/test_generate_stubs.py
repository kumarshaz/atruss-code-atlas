import json
import subprocess
import time
from pathlib import Path


def run_generator(discovery_file: Path, output_dir: Path):
    script_path = Path(__file__).parent.parent.parent / "scripts" / "generate-report-stubs.py"
    return subprocess.run(
        [
            "python3",
            str(script_path),
            "--discovery",
            str(discovery_file),
            "--output",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_generate_stubs_creates_correct_structure(tmp_path: Path):
    discovery_data = [
        {
            "Organization": "org-alpha",
            "RepositoryName": "repo-one",
            "PrimaryLanguage": "Python",
            "FrameworkType": "Django",
            "HasPipeline": True,
            "HasDockerfile": False,
            "HasKubernetes": False,
            "HasAPI": True,
            "DocumentationPriority": "P1",
            "LastUpdate": "2026-03-30T00:00:00Z",
            "WebUrl": "https://github.com/org-alpha/repo-one",
        },
        {
            "Organization": "org-beta",
            "RepositoryName": "repo-two",
            "PrimaryLanguage": "TypeScript",
            "HasPipeline": False,
        },
    ]

    discovery_file = tmp_path / "repositories.json"
    discovery_file.write_text(json.dumps(discovery_data), encoding="utf-8")

    output_dir = tmp_path / "reports"
    # Pre-seed a legacy .md file to verify cleanup on .mdx regeneration
    (output_dir / "org-alpha").mkdir(parents=True)
    legacy_stub = output_dir / "org-alpha" / "repo-one.md"
    legacy_stub.write_text("legacy", encoding="utf-8")

    result = run_generator(discovery_file, output_dir)
    assert result.returncode == 0

    expected_file_1 = output_dir / "org-alpha" / "repo-one.mdx"
    expected_file_2 = output_dir / "org-beta" / "repo-two.mdx"
    assert expected_file_1.exists()
    assert expected_file_2.exists()
    assert not legacy_stub.exists()

    content_1 = expected_file_1.read_text(encoding="utf-8")
    assert 'title: "repo-one"' in content_1
    assert 'org: "org-alpha"' in content_1
    assert 'language: "Python"' in content_1
    assert "has_pipeline: true" in content_1
    assert "has_docker: false" in content_1

    assert "import RepoTabs from '../../../../components/RepoTabs.astro'" in content_1
    assert "import PipelineView from '../../../../components/PipelineView.astro'" in content_1
    arch_import = "import ArchitectureView from '../../../../components/ArchitectureView.astro'"
    assert arch_import in content_1
    assert "<RepoTabs " in content_1
    assert 'slot="discovery"' in content_1
    assert 'slot="pipeline"' in content_1
    assert 'slot="architecture"' in content_1
    assert "<PipelineView " in content_1
    assert "<ArchitectureView " in content_1


def test_generate_stubs_missing_file(tmp_path: Path):
    output_dir = tmp_path / "reports"
    result = run_generator(tmp_path / "nonexistent.json", output_dir)
    assert result.returncode != 0
    assert "Error" in result.stderr or "Error" in result.stdout


def test_generate_stubs_empty_json(tmp_path: Path):
    discovery_file = tmp_path / "empty.json"
    discovery_file.write_text("[]", encoding="utf-8")
    output_dir = tmp_path / "reports"

    result = run_generator(discovery_file, output_dir)
    assert result.returncode == 0
    mdx_files = list(output_dir.glob("**/*.mdx"))
    assert len(mdx_files) == 0


def test_generate_stubs_timing(tmp_path: Path):
    repos = [
        {
            "Organization": f"org-{i % 5}",
            "RepositoryName": f"repo-{i}",
            "PrimaryLanguage": "Python",
        }
        for i in range(100)
    ]
    discovery_file = tmp_path / "large.json"
    discovery_file.write_text(json.dumps(repos), encoding="utf-8")
    output_dir = tmp_path / "reports"

    start = time.time()
    result = run_generator(discovery_file, output_dir)
    duration = time.time() - start

    assert result.returncode == 0
    assert duration < 5.0
