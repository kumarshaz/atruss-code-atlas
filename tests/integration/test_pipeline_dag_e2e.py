import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.analyzers.pipeline.dag_builder import build_workflow_graph_payload
from src.analyzers.pipeline.heuristics import analyze_workflow_anti_patterns
from src.analyzers.pipeline.parser import parse_workflow_yaml
from src.cli.commands.analyze_pipeline import app as pipeline_app


@pytest.mark.integration
def test_tr_dag_workflow_e2e_and_antipattern_detection(tmp_path: Path):
    """TR-DAG E2E: reconstructs GitHub Actions DAG, detects all 7 anti-patterns, and runs analyze-pipeline CLI."""
    repo_dir = tmp_path / "sample-repo"
    wf_dir = repo_dir / ".github" / "workflows"
    wf_dir.mkdir(parents=True)

    clean_yml = """
name: Clean CI
on:
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          cache: pip
      - run: pip install -r requirements.txt
      - uses: actions/upload-artifact@v4
  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - run: pytest
  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
      - run: echo "deploying cleanly"
"""
    risky_yml = """
name: Risky CD
on: push
jobs:
  build:
    runs-on: self-hosted
    steps:
      - run: pip install -r requirements.txt
  package:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "packaging without artifact upload"
  deploy:
    needs: package
    runs-on: ubuntu-latest
    environment: production
    env:
      SECRET_TOKEN: "ghp_1234567890abcdefghij1234567890"
    steps:
      - run: echo "deploying without test"
"""
    (wf_dir / "clean.yml").write_text(clean_yml, encoding="utf-8")
    (wf_dir / "risky.yml").write_text(risky_yml, encoding="utf-8")

    parsed_clean = parse_workflow_yaml(clean_yml)
    clean_payload, clean_dag = build_workflow_graph_payload(".github/workflows/clean.yml", parsed_clean)
    assert len(clean_payload["jobs"]) == 3
    assert set(clean_dag.edges) == {("build", "test"), ("build", "deploy"), ("test", "deploy")}
    assert analyze_workflow_anti_patterns(parsed_clean, clean_dag) == []

    parsed_risky = parse_workflow_yaml(risky_yml)
    _risky_payload, risky_dag = build_workflow_graph_payload(".github/workflows/risky.yml", parsed_risky)
    risky_types = {ap["type"] for ap in analyze_workflow_anti_patterns(parsed_risky, risky_dag)}
    assert {
        "NO_TEST_GATE",
        "NO_CACHE",
        "NO_ARTIFACT_HANDOFF",
        "HARDCODED_SECRET",
        "SEQUENTIAL_ONLY",
        "UNFILTERED_MAIN_PUSH",
        "UNLABELED_SELF_HOSTED",
    }.issubset(risky_types)

    out_dir = tmp_path / "pipeline-out"
    runner = CliRunner()
    res = runner.invoke(pipeline_app, ["--path", str(repo_dir), "--output-dir", str(out_dir)])
    assert res.exit_code == 0, res.output

    exported = json.loads(
        (out_dir / "latest" / "pipelines" / "local-sample-repo-pipeline.json").read_text(encoding="utf-8")
    )
    assert len(exported["workflows"]) == 2
    assert (out_dir / "latest" / "relationships" / "pipeline_topology.json").exists()
    assert (out_dir / "sample-repo_unknown_analysis.json").exists()
