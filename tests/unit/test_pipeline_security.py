import hashlib
import json
from pathlib import Path

import networkx as nx
import pytest

from src.analyzers.pipeline.dag_builder import (
    build_cross_workflow_dag,
    build_workflow_dag,
    build_workflow_graph_payload,
    compute_blast_radius,
)
from src.analyzers.pipeline.heuristics import (
    analyze_workflow_anti_patterns,
    load_pipeline_rules,
)
from src.analyzers.pipeline.parser import (
    extract_cross_workflow_references,
    extract_workflow_line_map,
    parse_workflow_yaml,
)

PINNED_SHA = "a81bbbf8298c0fa03ea29cdc473d45769f953675"


def _analyze_raw(
    raw_yaml: str,
    file_source: str | None = ".github/workflows/security.yml",
    policy_path: Path | None = None,
) -> list[dict]:
    parsed = parse_workflow_yaml(raw_yaml)
    dag = build_workflow_dag(parsed)
    return analyze_workflow_anti_patterns(
        parsed,
        dag,
        file_source=file_source,
        raw_yaml=raw_yaml,
        policy_path=policy_path,
    )


def test_pipeline_rules_manifest_contains_all_14_rules():
    policy = load_pipeline_rules()
    assert policy["trusted_action_owners"] == ["actions"]
    rules = policy["rules"]
    assert len(rules) == 14
    rule_ids = [r["rule_id"] for r in rules]
    assert rule_ids == [f"ATRUSS-PIPE-{i:03d}" for i in range(1, 15)]
    for rule in rules:
        assert rule["enabled"] is True
        assert rule["default_severity"] in {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
        assert rule["description"].strip()
        assert rule["remediation"].strip()


def test_pipe_008_unpinned_action_detection_and_skips():
    raw_yaml = f"""
name: Action Pinning Check
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - uses: ./.github/actions/local-helper
      - uses: docker://alpine:3.20
      - uses: third-party/pinned-action@{PINNED_SHA}
      - uses: third-party/floating-tag@v2
      - uses: github/codeql-action/init@v3
"""
    findings = _analyze_raw(raw_yaml)
    unpinned = [f for f in findings if f["type"] == "UNPINNED_ACTION"]
    assert len(unpinned) == 2
    assert all(f["rule_id"] == "ATRUSS-PIPE-008" for f in unpinned)
    assert all(f["severity"] == "HIGH" for f in unpinned)
    assert "third-party/floating-tag@v2" in unpinned[0]["message"]
    assert "github/codeql-action/init@v3" in unpinned[1]["message"]
    assert unpinned[0]["start_line"] < unpinned[1]["start_line"]


def test_pipe_008_custom_policy_trusted_owner_and_disable(tmp_path: Path):
    raw_yaml = """
name: Custom Policy Test
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: my-trusted-org/internal-step@v1
"""
    custom_policy = tmp_path / "custom-rules.yaml"
    custom_policy.write_text(
        """
version: "1.0"
trusted_action_owners:
  - "actions"
  - "my-trusted-org"
rules:
  - rule_id: "ATRUSS-PIPE-008"
    type: "UNPINNED_ACTION"
    default_severity: "HIGH"
    enabled: true
    remediation: "Pin third-party actions."
""",
        encoding="utf-8",
    )
    assert _analyze_raw(raw_yaml, policy_path=custom_policy) == []

    disabled_policy = tmp_path / "disabled-rules.yaml"
    disabled_policy.write_text(
        """
version: "1.0"
rules:
  - rule_id: "ATRUSS-PIPE-008"
    type: "UNPINNED_ACTION"
    default_severity: "HIGH"
    enabled: false
    remediation: "Disabled."
""",
        encoding="utf-8",
    )
    findings = _analyze_raw(raw_yaml, policy_path=disabled_policy)
    assert all(f["type"] != "UNPINNED_ACTION" for f in findings)


@pytest.mark.parametrize(
    "run_snippet",
    [
        'echo "Issue: ${{ github.event.issue.title }}"',
        'echo "PR: ${{ github.event.pull_request.body }}"',
        'echo "Comment: ${{ github.event.comment.body }}"',
        'echo "Review: ${{ github.event.review.body }}"',
        'echo "Discussion: ${{ github.event.discussion.title }}"',
        'echo "Head: ${{ github.head_ref }}"',
        'echo "VAR=$UNTRUSTED_VAL" >> $GITHUB_ENV',
        'echo "${{ inputs.custom_path }}" >> "$GITHUB_PATH"',
    ],
)
def test_pipe_009_template_injection_contexts_and_env_writes(run_snippet: str):
    raw_yaml = f"""
name: Injection Test
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: |
          {run_snippet}
"""
    findings = _analyze_raw(raw_yaml)
    inj = [f for f in findings if f["type"] == "TEMPLATE_INJECTION"]
    assert len(inj) == 1
    assert inj[0]["rule_id"] == "ATRUSS-PIPE-009"
    assert inj[0]["severity"] == "CRITICAL"


def test_pipe_009_allows_safe_env_indirection_and_static_github_env():
    raw_yaml = """
name: Safe Context Handling
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  safe:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Safe indirection
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: |
          echo "PR Title: $PR_TITLE"
          echo "NODE_ENV=production" >> "$GITHUB_ENV"
"""
    findings = _analyze_raw(raw_yaml)
    assert findings == []


def test_pipe_010_pwn_request_risk():
    risky_yaml = """
name: Pwn Request
on:
  pull_request_target:
    types: [opened, synchronize]
permissions:
  contents: read
jobs:
  pr_check:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
"""
    findings = _analyze_raw(risky_yaml)
    pwn = [f for f in findings if f["type"] == "PWN_REQUEST_RISK"]
    assert len(pwn) == 1
    assert pwn[0]["rule_id"] == "ATRUSS-PIPE-010"
    assert pwn[0]["severity"] == "CRITICAL"

    safe_yaml = """
name: Safe PR Target
on:
  pull_request_target:
    types: [opened]
permissions:
  contents: read
jobs:
  label:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
"""
    assert _analyze_raw(safe_yaml) == []


def test_pipe_011_excessive_permissions():
    omitted_yaml = """
name: Omitted Perms
on:
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo ok
"""
    findings_omitted = _analyze_raw(omitted_yaml)
    assert any(
        f["rule_id"] == "ATRUSS-PIPE-011"
        and f["type"] == "EXCESSIVE_PERMISSIONS"
        and f["severity"] == "HIGH"
        for f in findings_omitted
    )

    write_all_yaml = """
name: Write All Perms
on:
  pull_request:
    branches: [main]
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo ok
"""
    findings_write_all = _analyze_raw(write_all_yaml)
    assert any(f["type"] == "EXCESSIVE_PERMISSIONS" for f in findings_write_all)

    read_all_yaml = """
name: Read All Perms
on:
  pull_request:
    branches: [main]
permissions: read-all
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo ok
"""
    assert _analyze_raw(read_all_yaml) == []


def test_pipe_012_no_timeout():
    no_timeout_yaml = """
name: Missing Timeout
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  hang:
    runs-on: ubuntu-latest
    steps:
      - run: echo waiting
"""
    findings = _analyze_raw(no_timeout_yaml)
    assert len(findings) == 1
    assert findings[0]["rule_id"] == "ATRUSS-PIPE-012"
    assert findings[0]["type"] == "NO_TIMEOUT"
    assert findings[0]["severity"] == "LOW"


def test_pipe_013_artifact_credential_persistence():
    unsafe_yaml = """
name: Credential Persistence
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  package:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - run: echo build > dist.txt
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist.txt
"""
    findings = _analyze_raw(unsafe_yaml)
    assert len(findings) == 1
    assert findings[0]["rule_id"] == "ATRUSS-PIPE-013"
    assert findings[0]["type"] == "ARTIFACT_CREDENTIAL_PERSISTENCE"
    assert findings[0]["severity"] == "MEDIUM"


def test_pipe_014_static_cloud_credentials_and_clean_oidc_immunity():
    missing_oidc_yaml = f"""
name: Cloud Without OIDC
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  cloud_test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: aws-actions/configure-aws-credentials@{PINNED_SHA}
        with:
          aws-region: us-east-1
      - uses: azure/login@{PINNED_SHA}
      - uses: google-github-actions/auth@{PINNED_SHA}
"""
    findings = _analyze_raw(missing_oidc_yaml)
    cloud_findings = [f for f in findings if f["type"] == "STATIC_CLOUD_CREDENTIALS"]
    assert len(cloud_findings) == 3
    assert all(f["rule_id"] == "ATRUSS-PIPE-014" for f in cloud_findings)
    assert all(f["severity"] == "HIGH" for f in cloud_findings)

    static_key_with_oidc_yaml = f"""
name: Static Secret Keys
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
  id-token: write
jobs:
  cloud_test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: aws-actions/configure-aws-credentials@{PINNED_SHA}
        with:
          aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
          aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
          aws-region: us-east-1
"""
    static_findings = _analyze_raw(static_key_with_oidc_yaml)
    assert any(f["type"] == "STATIC_CLOUD_CREDENTIALS" for f in static_findings)

    clean_oidc_yaml = f"""
name: Clean SHA-Pinned OIDC Pipeline
on:
  push:
    branches: [main]
permissions:
  contents: read
  id-token: write
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          cache: pip
      - run: pytest
      - uses: actions/upload-artifact@v4
  deploy:
    needs: test
    runs-on: ubuntu-latest
    timeout-minutes: 15
    environment: production
    steps:
      - uses: actions/download-artifact@v4
      - uses: aws-actions/configure-aws-credentials@{PINNED_SHA}
        with:
          role-to-assume: ${{{{ secrets.AWS_ROLE_ARN }}}}
          aws-region: us-east-1
      - uses: third-party/oidc-deploy@{PINNED_SHA}
"""
    assert _analyze_raw(clean_oidc_yaml) == []


def test_finding_metadata_line_mapping_and_json_serializability():
    raw_yaml = """name: Metadata Check
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: third-party/unpinned@main
      - run: echo "${{ github.event.issue.title }}"
"""
    line_map = extract_workflow_line_map(raw_yaml)
    assert line_map["top:on"] == 2
    assert line_map["job:build"] == 4
    assert line_map["job:build:step:1:uses"] == 8
    assert line_map["job:build:step:2:run"] == 9

    parsed = parse_workflow_yaml(raw_yaml)
    dag = build_workflow_dag(parsed)
    findings = analyze_workflow_anti_patterns(parsed, dag, raw_yaml=raw_yaml)
    assert findings
    for item in findings:
        assert item["rule_id"].startswith("ATRUSS-PIPE-")
        assert item["entity_type"] == "PIPELINE"
        assert item["file_source"] == ".github/workflows/workflow.yml"
        assert isinstance(item["start_line"], int) and item["start_line"] >= 1
        assert isinstance(item["end_line"], int) and item["end_line"] >= item["start_line"]
        assert isinstance(item["remediation"], str) and item["remediation"]

    unpinned = next(f for f in findings if f["type"] == "UNPINNED_ACTION")
    assert unpinned["start_line"] == 8
    injection = next(f for f in findings if f["type"] == "TEMPLATE_INJECTION")
    assert injection["start_line"] == 9

    # Malformed YAML line-map fallback should not raise
    broken_map = extract_workflow_line_map("jobs:\n  build:\n    bad: [unclosed\n")
    assert broken_map["job:build"] == 2

    # Clean JSON serialization
    serialized = json.dumps(findings)
    assert json.loads(serialized) == findings


def test_extract_cross_workflow_references_and_cross_workflow_dag():
    ci_yaml = """
name: CI
on:
  push:
    branches: [main]
jobs:
  call-build:
    uses: ./.github/workflows/reusable-build.yml
  call-scan:
    uses: acme-org/shared-sec/.github/workflows/codeql.yml@v2
"""
    reusable_yaml = """
name: Reusable Build
on:
  workflow_call:
jobs:
  compile:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo compile
"""
    deploy_yaml = """
name: Deploy
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
jobs:
  ship:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - run: echo ship
"""
    ci_parsed = parse_workflow_yaml(ci_yaml)
    reusable_parsed = parse_workflow_yaml(reusable_yaml)
    deploy_parsed = parse_workflow_yaml(deploy_yaml)

    ci_refs = extract_cross_workflow_references(".github/workflows/ci.yml", ci_parsed)
    assert ci_refs == [
        {
            "source_workflow": ".github/workflows/ci.yml",
            "source_job": "call-build",
            "target_workflow": ".github/workflows/reusable-build.yml",
            "edge_type": "workflow_call",
        },
        {
            "source_workflow": ".github/workflows/ci.yml",
            "source_job": "call-scan",
            "target_workflow": "acme-org/shared-sec/.github/workflows/codeql.yml",
            "edge_type": "workflow_call",
        },
    ]

    deploy_refs = extract_cross_workflow_references(".github/workflows/deploy.yml", deploy_parsed)
    assert deploy_refs == [
        {
            "source_workflow": "CI",
            "source_job": "",
            "target_workflow": ".github/workflows/deploy.yml",
            "edge_type": "workflow_run",
        }
    ]

    ci_payload, _ = build_workflow_graph_payload(".github/workflows/ci.yml", ci_parsed)
    reusable_payload, _ = build_workflow_graph_payload(
        ".github/workflows/reusable-build.yml", reusable_parsed
    )
    deploy_payload, _ = build_workflow_graph_payload(".github/workflows/deploy.yml", deploy_parsed)

    assert "cross_workflow_edges" in ci_payload
    assert "blast_radius" in ci_payload

    cross_dag, edges = build_cross_workflow_dag([deploy_payload, ci_payload, reusable_payload])
    assert (".github/workflows/ci.yml", ".github/workflows/reusable-build.yml") in cross_dag.edges
    assert (".github/workflows/ci.yml", ".github/workflows/deploy.yml") in cross_dag.edges
    assert (
        ".github/workflows/ci.yml",
        "acme-org/shared-sec/.github/workflows/codeql.yml",
    ) in cross_dag.edges
    assert len(edges) == 3


def test_compute_blast_radius_pure_python_and_determinism():
    empty_res = compute_blast_radius(nx.DiGraph(), target_node="missing")
    assert empty_res["pagerank"] == {}
    assert empty_res["betweenness_centrality"] == {}
    assert empty_res["blast_radius_count"] == 0
    assert empty_res["blast_radius_pct"] == 0.0

    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("build", "test"),
            ("build", "lint"),
            ("test", "package"),
            ("lint", "package"),
            ("package", "deploy"),
        ]
    )

    full = compute_blast_radius(G)
    assert set(full["pagerank"].keys()) == {"build", "test", "lint", "package", "deploy"}
    assert abs(sum(full["pagerank"].values()) - 1.0) < 1e-4
    assert full["betweenness_centrality"]["package"] > 0.0
    assert full["max_blast_radius"] == 4
    assert full["downstream_impact"]["build"] == ["deploy", "lint", "package", "test"]

    targeted = compute_blast_radius(G, target_node="build")
    assert targeted["target_node"] == "build"
    assert targeted["downstream_nodes"] == ["deploy", "lint", "package", "test"]
    assert targeted["upstream_nodes"] == []
    assert targeted["blast_radius_count"] == 4
    assert targeted["blast_radius_pct"] == 100.0

    missing = compute_blast_radius(G, target_node="nonexistent")
    assert missing["downstream_nodes"] == []
    assert missing["blast_radius_count"] == 0

    # Deterministic SHA-256 across repeated runs
    digest_a = hashlib.sha256(json.dumps(full, sort_keys=True).encode("utf-8")).hexdigest()
    digest_b = hashlib.sha256(
        json.dumps(compute_blast_radius(G), sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert digest_a == digest_b

    # Cyclic graph resilience in pure-Python PageRank + betweenness
    cyclic = nx.DiGraph()
    cyclic.add_edges_from([("a", "b"), ("b", "c"), ("c", "a")])
    cyclic_res = compute_blast_radius(cyclic, target_node="a")
    assert cyclic_res["downstream_nodes"] == ["b", "c"]
    assert abs(sum(cyclic_res["pagerank"].values()) - 1.0) < 1e-4


def test_permissions_dict_and_multi_cloud_oidc_and_finding_determinism():
    dict_write_yaml = f"""
name: Dict Permissions And Multi-Cloud OIDC
on:
  pull_request:
    branches: [main]
permissions:
  contents: write
  id-token: write
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: pytest
      - uses: actions/upload-artifact@v4
  deploy_multi:
    needs: test
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/download-artifact@v4
      - uses: azure/login@{PINNED_SHA}
        with:
          client-id: ${{{{ secrets.AZURE_CLIENT_ID }}}}
          tenant-id: ${{{{ secrets.AZURE_TENANT_ID }}}}
          subscription-id: ${{{{ secrets.AZURE_SUBSCRIPTION_ID }}}}
      - uses: google-github-actions/auth@{PINNED_SHA}
        with:
          workload_identity_provider: projects/123/locations/global/workloadIdentityPools/gh
          service_account: deploy@proj.iam.gserviceaccount.com
"""
    assert _analyze_raw(dict_write_yaml) == []

    job_write_all_and_static_cloud = f"""
name: Job Write-All And Static Multi-Cloud
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
  id-token: write
jobs:
  risky_cloud:
    permissions: write-all
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: azure/login@{PINNED_SHA}
        with:
          creds: ${{{{ secrets.AZURE_CREDENTIALS }}}}
      - uses: google-github-actions/auth@{PINNED_SHA}
        with:
          credentials_json: ${{{{ secrets.GCP_SA_KEY }}}}
"""
    findings_a = _analyze_raw(job_write_all_and_static_cloud)
    findings_b = _analyze_raw(job_write_all_and_static_cloud)
    types = [f["type"] for f in findings_a]
    assert types.count("EXCESSIVE_PERMISSIONS") == 1
    assert types.count("STATIC_CLOUD_CREDENTIALS") == 2

    hash_a = hashlib.sha256(json.dumps(findings_a, sort_keys=True).encode("utf-8")).hexdigest()
    hash_b = hashlib.sha256(json.dumps(findings_b, sort_keys=True).encode("utf-8")).hexdigest()
    assert hash_a == hash_b
