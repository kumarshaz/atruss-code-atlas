from pathlib import Path

from src.analyzers.classification import Ecosystem, classify_repository
from src.analyzers.code.orchestrator import orchestrate_full_analysis
from src.analyzers.dependencies.manifest_parser import build_purl, parse_repository_dependencies


def test_classify_go_rust_ruby_php_elixir_and_infra_repos():
    go_res = classify_repository(["go.mod", "cmd/server/main.go", "internal/api/routes.go"])
    assert go_res.ecosystem == Ecosystem.GO
    assert go_res.display_language == "Go"

    rust_res = classify_repository(["Cargo.toml", "src/main.rs", "Dockerfile"])
    assert rust_res.ecosystem == Ecosystem.RUST
    assert rust_res.display_language == "Rust"
    assert rust_res.signals["HasDockerfile"] is True

    ruby_res = classify_repository(
        ["Gemfile", "config/routes.rb", "app/controllers/home_controller.rb"]
    )
    assert ruby_res.ecosystem == Ecosystem.RUBY
    assert ruby_res.display_language == "Ruby"
    assert ruby_res.framework == "Ruby on Rails"

    php_res = classify_repository(["composer.json", "artisan", "app/Http/Kernel.php"])
    assert php_res.ecosystem == Ecosystem.PHP
    assert php_res.display_language == "PHP"

    elixir_res = classify_repository(["mix.exs", "lib/app_web/router.ex"])
    assert elixir_res.ecosystem == Ecosystem.ELIXIR
    assert elixir_res.display_language == "Elixir"

    infra_res = classify_repository(["charts/app/Chart.yaml", "docker-compose.yml", "main.tf"])
    assert infra_res.ecosystem == Ecosystem.INFRA_DEVOPS
    assert infra_res.display_language == "Container / Helm / IaC"


def test_parse_multi_ecosystem_manifests_and_purls(tmp_path: Path):
    (tmp_path / "go.mod").write_text(
        "module example.com/app\n\ngo 1.22\n\nrequire (\n"
        "\tgithub.com/gin-gonic/gin v1.9.1\n"
        "\tgolang.org/x/sys v0.18.0 // indirect\n)\n",
        encoding="utf-8",
    )
    (tmp_path / "Cargo.toml").write_text(
        '[package]\nname = "demo"\nversion = "0.1.0"\n\n'
        '[dependencies]\naxum = "0.7.5"\ntokio = { version = "^1.37.0" }\n',
        encoding="utf-8",
    )
    (tmp_path / "Gemfile").write_text(
        "source 'https://rubygems.org'\ngem 'rails', '~> 7.1.3'\n",
        encoding="utf-8",
    )
    (tmp_path / "composer.json").write_text(
        '{"require": {"php": "^8.2", "laravel/framework": "^11.0"}}\n',
        encoding="utf-8",
    )
    (tmp_path / "mix.exs").write_text(
        'defp deps do\n  [{:phoenix, "~> 1.7.11"}]\nend\n',
        encoding="utf-8",
    )

    deps = parse_repository_dependencies(tmp_path)
    purls = {d.purl for d in deps}

    assert build_purl("golang", "github.com/gin-gonic/gin", "1.9.1") in purls
    assert build_purl("cargo", "axum", "0.7.5") in purls
    assert build_purl("gem", "rails", "7.1.3") in purls
    assert build_purl("composer", "laravel/framework", "11.0") in purls
    assert build_purl("hex", "phoenix", "1.7.11") in purls


def test_orchestrate_full_analysis_on_go_service(tmp_path: Path):
    (tmp_path / "go.mod").write_text(
        "module example.com/svc\nrequire github.com/gin-gonic/gin v1.9.1\n",
        encoding="utf-8",
    )
    (tmp_path / "main.go").write_text(
        "package main\nfunc main() {\n\tprintln(\"hello\")\n}\n",
        encoding="utf-8",
    )
    (tmp_path / "Dockerfile").write_text("FROM golang:1.22\n", encoding="utf-8")

    result = orchestrate_full_analysis(tmp_path)
    assert result.ecosystem == "Go"
    assert result.metrics["files_analyzed"] == 1
    assert result.metrics["loc"] == 4
    assert len(result.dependencies) == 1
    assert result.scorecard is not None
