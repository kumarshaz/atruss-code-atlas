import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _yaml_quote(value: Any) -> str:
    return json.dumps(str(value))


def generate_stubs(discovery_path: Path, output_dir: Path) -> int:
    if not discovery_path.exists():
        print(f"Error: Discovery file {discovery_path} not found.", file=sys.stderr)
        return 1

    try:
        data = json.loads(discovery_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse {discovery_path}: {e}", file=sys.stderr)
        return 1

    items = data.get("items", []) if isinstance(data, dict) else data
    if not isinstance(items, list):
        print("Error: Expected a list of repositories.", file=sys.stderr)
        return 1

    for repo in items:
        if not isinstance(repo, dict):
            continue
        org = repo.get("Organization")
        repo_name = repo.get("RepositoryName")
        if not org or not repo_name:
            continue

        language = repo.get("PrimaryLanguage") or "Unknown"
        priority = repo.get("DocumentationPriority") or "P3"
        description = f"{org} / {language} / {priority}"

        org_dir = output_dir / str(org)
        org_dir.mkdir(parents=True, exist_ok=True)

        # Clean legacy .md stub if transitioning to .mdx
        legacy_md = org_dir / f"{repo_name}.md"
        if legacy_md.exists():
            legacy_md.unlink()

        mdx_file = org_dir / f"{repo_name}.mdx"

        frontmatter = [
            "---",
            f"title: {_yaml_quote(repo_name)}",
            f"description: {_yaml_quote(description)}",
            f"org: {_yaml_quote(org)}",
            f"repo_name: {_yaml_quote(repo_name)}",
            f"language: {_yaml_quote(language)}",
        ]

        if repo.get("FrameworkType"):
            frontmatter.append(f"framework: {_yaml_quote(repo.get('FrameworkType'))}")
        for key, fm_key in (
            ("HasPipeline", "has_pipeline"),
            ("HasDockerfile", "has_docker"),
            ("HasKubernetes", "has_kubernetes"),
            ("HasAPI", "has_api"),
        ):
            if repo.get(key) is not None:
                frontmatter.append(f"{fm_key}: {str(bool(repo.get(key))).lower()}")
        if priority:
            frontmatter.append(f"doc_priority: {_yaml_quote(priority)}")
        if repo.get("LastUpdate"):
            frontmatter.append(f"last_updated: {_yaml_quote(repo.get('LastUpdate'))}")
        if repo.get("WebUrl"):
            frontmatter.append(f"github_url: {_yaml_quote(repo.get('WebUrl'))}")
        frontmatter.append("---")

        tabs_attrs = [
            f"org={json.dumps(str(org))}",
            f"repo_name={json.dumps(str(repo_name))}",
            f"language={json.dumps(str(language))}",
            f"doc_priority={json.dumps(str(priority))}",
        ]
        if repo.get("FrameworkType"):
            tabs_attrs.append(f"framework={json.dumps(str(repo.get('FrameworkType')))}")
        if repo.get("LastUpdate"):
            tabs_attrs.append(f"last_updated={json.dumps(str(repo.get('LastUpdate')))}")
        if repo.get("WebUrl"):
            tabs_attrs.append(f"github_url={json.dumps(str(repo.get('WebUrl')))}")

        disc_attrs = [
            f"language={json.dumps(str(language))}",
            f"doc_priority={json.dumps(str(priority))}",
        ]
        for key, prop in (
            ("FrameworkType", "framework"),
            ("AllFrameworks", "all_frameworks"),
            ("DeployableTypes", "deployable_types"),
            ("TechnologyStack", "tech_stack"),
            ("DefaultBranch", "default_branch"),
            ("LastUpdate", "last_updated"),
            ("WebUrl", "github_url"),
        ):
            if repo.get(key):
                disc_attrs.append(f"{prop}={json.dumps(str(repo.get(key)))}")

        for key, prop in (
            ("HasPipeline", "has_pipeline"),
            ("HasDockerfile", "has_docker"),
            ("HasKubernetes", "has_kubernetes"),
            ("HasAPI", "has_api"),
            ("HasService", "has_service"),
            ("HasFrontend", "has_frontend"),
            ("HasDatabase", "has_database"),
        ):
            if repo.get(key) is not None:
                disc_attrs.append(f"{prop}={{{str(bool(repo.get(key))).lower()}}}")

        content_lines = [
            *frontmatter,
            "",
            "import RepoTabs from '../../../../components/RepoTabs.astro';",
            "import PipelineView from '../../../../components/PipelineView.astro';",
            "import ArchitectureView from '../../../../components/ArchitectureView.astro';",
            "import DiscoveryTable from '../../../../components/DiscoveryTable.astro';",
            "",
            f"<RepoTabs {' '.join(tabs_attrs)}>",
            '  <div slot="discovery">',
            f"    <DiscoveryTable {' '.join(disc_attrs)} />",
            "  </div>",
            '  <div slot="pipeline">',
            (
                f"    <PipelineView repo_name={json.dumps(str(repo_name))} "
                f"org={json.dumps(str(org))} />"
            ),
            "  </div>",
            '  <div slot="architecture">',
            (
                f"    <ArchitectureView repo_name={json.dumps(str(repo_name))} "
                f"org={json.dumps(str(org))} />"
            ),
            "  </div>",
            "</RepoTabs>",
            "",
        ]
        mdx_file.write_text("\n".join(content_lines), encoding="utf-8")

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate M3 tabbed Astro MDX report stubs from discovery JSON"
    )
    parser.add_argument("--discovery", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    raise SystemExit(generate_stubs(args.discovery, args.output))


if __name__ == "__main__":
    main()
