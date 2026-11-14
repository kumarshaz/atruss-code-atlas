import pytest

from src.analyzers.pipeline.dag_builder import (
    build_workflow_dag,
    build_workflow_graph_payload,
)
from src.analyzers.pipeline.heuristics import (
    analyze_workflow_anti_patterns,
    find_untested_deployments,
)
from src.analyzers.pipeline.parser import extract_triggers, parse_workflow_yaml


@pytest.fixture
def mock_dag_workflow():
    return {
        "jobs": {
            "build": {},
            "test": {"needs": "build"},
            "deploy_prod": {},
        }
    }


def test_dag_builder(mock_dag_workflow):
    G = build_workflow_dag(mock_dag_workflow)
    assert G.number_of_nodes() == 3
    assert G.number_of_edges() == 1
    assert ("build", "test") in G.edges


def test_anti_patterns(mock_dag_workflow):
    G = build_workflow_dag(mock_dag_workflow)
    findings = find_untested_deployments(G)
    assert len(findings) == 1
    assert "deploy_prod" in findings[0]


def test_pyyaml_on_boolean_key_and_all_seven_antipatterns():
    raw_yaml = """
name: Risky Pipeline
on: push
jobs:
  build:
    runs-on: self-hosted
    steps:
      - run: npm install
  lint:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
  deploy:
    needs: lint
    runs-on: ubuntu-latest
    environment: production
    env:
      API_KEY: "supersecretliteralvalue123"
    steps:
      - run: echo deploy
"""
    parsed = parse_workflow_yaml(raw_yaml)
    assert extract_triggers(parsed) == ["push"]

    payload, G = build_workflow_graph_payload(".github/workflows/risky.yml", parsed)
    assert payload["triggers"] == ["push"]
    assert len(payload["jobs"]) == 3

    anti_patterns = analyze_workflow_anti_patterns(parsed, G)
    types = {ap["type"] for ap in anti_patterns}
    assert "NO_TEST_GATE" in types
    assert "NO_CACHE" in types
    assert "NO_ARTIFACT_HANDOFF" in types
    assert "HARDCODED_SECRET" in types
    assert "SEQUENTIAL_ONLY" in types
    assert "UNFILTERED_MAIN_PUSH" in types
    assert "UNLABELED_SELF_HOSTED" in types


def test_setup_action_cache_prevents_false_positive():
    raw_yaml = """
name: Clean Pipeline
on:
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"
      - run: npm ci && npm test
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"
      - run: npm run build
      - uses: actions/upload-artifact@v4
  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
"""
    parsed = parse_workflow_yaml(raw_yaml)
    _, G = build_workflow_graph_payload(".github/workflows/clean.yml", parsed)
    anti_patterns = analyze_workflow_anti_patterns(parsed, G)
    assert anti_patterns == []
