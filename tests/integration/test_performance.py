import time
from pathlib import Path

import pytest

from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.cli.commands.analyze_pipeline import _analyze_repo_workflows
from src.core.services.report_generator import generate_arc42_markdown


@pytest.mark.integration
@pytest.mark.benchmark
def test_tr_perf_medium_monorepo_sla_and_determinism(tmp_path: Path):
    """TR-PERF E2E: benchmark analysis under NFR SLA (<180s budget) with byte-identical determinism."""
    repo = tmp_path / "scale-monorepo"
    py_dir = repo / "services" / "api"
    ts_dir = repo / "apps" / "portal" / "src"
    wf_dir = repo / ".github" / "workflows"
    py_dir.mkdir(parents=True)
    ts_dir.mkdir(parents=True)
    wf_dir.mkdir(parents=True)

    (py_dir / "requirements.txt").write_text("fastapi\n", encoding="utf-8")
    for idx in range(15):
        (py_dir / f"service_{idx}.py").write_text(
            f"class Domain{idx}Service:\n"
            f"    def compute(self, x: int) -> int:\n"
            f"        return x + {idx} if x > 0 else 0\n",
            encoding="utf-8",
        )

    (repo / "apps" / "portal" / "package.json").write_text(
        '{"name": "portal-ui", "dependencies": {"react": "^18.0.0"}}',
        encoding="utf-8",
    )
    for idx in range(15):
        (ts_dir / f"Widget{idx}.tsx").write_text(
            f"export const Widget{idx} = () => <div>Widget {idx}</div>;\n",
            encoding="utf-8",
        )

    for idx in range(3):
        (wf_dir / f"ci_{idx}.yml").write_text(
            f"name: CI {idx}\non:\n  pull_request:\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: pytest\n",
            encoding="utf-8",
        )

    start = time.perf_counter()
    res1 = orchestrate_full_analysis(repo)
    pipe1 = _analyze_repo_workflows(repo, "scale-monorepo")
    md1 = generate_arc42_markdown(
        "scale-monorepo",
        res1.components,
        metrics=res1.metrics,
        ecosystem=res1.ecosystem,
        framework=res1.framework,
    )
    elapsed = time.perf_counter() - start

    assert elapsed < 30.0, f"Exceeded benchmark SLA: {elapsed:.2f}s"
    assert res1.metrics["files_analyzed"] >= 30
    assert len(res1.components) >= 30
    assert len(pipe1.pipelines) == 3

    res2 = orchestrate_full_analysis(repo)
    pipe2 = _analyze_repo_workflows(repo, "scale-monorepo")
    md2 = generate_arc42_markdown(
        "scale-monorepo",
        res2.components,
        metrics=res2.metrics,
        ecosystem=res2.ecosystem,
        framework=res2.framework,
    )

    assert res1.components == res2.components
    assert res1.metrics == res2.metrics
    assert pipe1.model_dump_json() == pipe2.model_dump_json()
    assert md1 == md2
