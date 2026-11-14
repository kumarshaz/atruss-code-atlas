from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

ECOSYSTEM_KEY_TO_DISPLAY: dict[str, str] = {
    "python": "Python",
    ".net": ".NET",
    "react_ts_js": "JavaScript/TypeScript",
    "java_springboot": "Java",
}

DISPLAY_TO_ECOSYSTEM_KEY: dict[str, str] = {v: k for k, v in ECOSYSTEM_KEY_TO_DISPLAY.items()}


class CorpusEntry(BaseModel):
    """Catalog entry representing a target public GitHub repository for benchmarking."""

    org: str
    name: str
    full_name: str
    url: str
    clone_url: str
    expected_ecosystem: str
    ecosystem_key: Literal["python", ".net", "react_ts_js", "java_springboot"]
    expected_pipeline: bool = True
    expected_framework: str | None = None
    pinned_ref: str = "main"
    pinned_sha: str | None = None
    estimated_size_mb: float = Field(default=20.0, gt=0.0, lt=250.0)
    estimated_loc: int = Field(default=50000, gt=0, lt=500000)
    star_tier: Literal["popular", "100..1000", "1000..10000", ">10000"] = "popular"
    stars: int = Field(default=0, ge=0)
    is_golden_fixture: bool = False
    tags: list[str] = Field(default_factory=list)

    @field_validator("full_name")
    @classmethod
    def _validate_full_name(cls, value: str) -> str:
        if "/" not in value or value.startswith("/") or value.endswith("/"):
            raise ValueError(f"full_name must be '<org>/<repo>', got: {value!r}")
        return value


class BenchmarkRepoResult(BaseModel):
    """Per-repository execution metrics and pass/fail status from `atruss benchmark`."""

    full_name: str
    org: str
    repo: str
    clone_url: str
    resolved_sha: str = "unknown"
    expected_ecosystem: str | None = None
    detected_ecosystem: str = "Unknown"
    detected_framework: str = "Unknown"
    classification_matched: bool | None = None
    has_pipeline: bool = False
    workflow_count: int = 0
    component_count: int = 0
    status: Literal["passed", "failed", "timeout"] = "passed"
    duration_seconds: float = 0.0
    within_sla: bool = True
    error: str | None = None
    stage_failed: str | None = None


class AnomalyRecord(BaseModel):
    """Structured failure/mismatch record emitted to `exports/latest/anomalies.json`."""

    repo: str
    sha: str = "unknown"
    stage: Literal[
        "clone",
        "discover",
        "analyze-pipeline",
        "analyze-code",
        "timeout",
        "classification",
    ]
    error_type: str
    message: str
    traceback: str = ""
    expected_ecosystem: str | None = None
    detected_ecosystem: str | None = None
    suggested_action: str = ""
    timestamp: str


class BenchmarkManifest(BaseModel):
    """Deterministic replay manifest mapping corpus or sampled GitHub targets and SHAs."""

    schema_version: str = "1.0"
    generated_at: str
    mode: Literal["corpus", "random-sample", "replay"]
    seed: int | None = None
    corpus_name: str | None = None
    total_entries: int
    entries: list[CorpusEntry] = Field(default_factory=list)


class BenchmarkSummary(BaseModel):
    """Aggregate benchmark scorecard emitted to `benchmark_summary.json` and `.md`."""

    run_id: str
    mode: str
    seed: int | None = None
    started_at: str
    completed_at: str
    total_repos: int
    completed_repos: int
    failed_repos: int
    timeout_repos: int
    crash_free_rate_pct: float
    classification_evaluated: int
    classification_matched: int
    classification_accuracy_pct: float
    pipeline_repos_with_workflows: int
    pipeline_parse_success_pct: float
    avg_runtime_seconds: float
    sla_compliant_count: int
    sla_compliance_pct: float
    ecosystem_breakdown: dict[str, dict[str, Any]] = Field(default_factory=dict)
    results: list[BenchmarkRepoResult] = Field(default_factory=list)
