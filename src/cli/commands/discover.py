
import typer

from src.analyzers.classification import classify_repository
from src.core.services.github_api import GitHubClient

app = typer.Typer()

@app.command("discover")
def discover(
    org: str = typer.Option(..., "--org", help="GitHub organization name"),
    token: str | None = typer.Option(None, "--token", help="GitHub Personal Access Token"),
    format: str = typer.Option("table", "--format", help="Output format: table or json")
):
    """Discover and classify repositories across a GitHub organization."""
    client = GitHubClient(token=token)

    typer.echo(f"Discovering repositories for organization: {org}...")
    try:
        repos = client.get_organization_repositories(org)
    except Exception as e:
        typer.echo(f"Error fetching repositories: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Found {len(repos)} repositories. Running classification...")

    results = []
    for repo in repos:
        name = repo["name"]
        default_branch = repo.get("default_branch", "main")
        clone_url = repo.get("clone_url", "")

        try:
            tree_paths = client.get_repository_tree(org, name, default_branch)
            classification = classify_repository(tree_paths)
            results.append({
                "name": name,
                "ecosystem": classification.ecosystem.value,
                "framework": classification.framework,
                "clone_url": clone_url
            })
        except Exception as e:
            typer.echo(f"Warning: Failed to scan tree for {name}: {e}", err=True)
            results.append({
                "name": name,
                "ecosystem": "error",
                "framework": "error",
                "clone_url": clone_url
            })

    if format == "json":
        import json
        typer.echo(json.dumps(results, indent=2))
    else:
        typer.echo("\n--- Results ---")
        for res in results:
            typer.echo(f"{res['name']:<30} | {res['ecosystem']:<15} | {res['framework']}")
