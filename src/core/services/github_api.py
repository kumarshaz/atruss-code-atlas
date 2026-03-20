import os
from typing import Any

import requests

GITHUB_API_URL = "https://api.github.com"

class GitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def get_organization_repositories(self, org_name: str) -> list[dict[str, Any]]:
        """Fetch all repositories for a given organization."""
        url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
        repos = []
        page = 1

        while True:
            response = requests.get(url, headers=self.headers, params={"per_page": 100, "page": page})
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1

        return repos

    def get_repository_tree(self, owner: str, repo: str, default_branch: str = "main") -> list[str]:
        """Fetch the flat file tree for a repository to run classification."""
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
        response = requests.get(url, headers=self.headers)

        # Fallback to master if default branch might be master locally defined incorrectly
        if response.status_code == 404 and default_branch == "main":
            return self.get_repository_tree(owner, repo, "master")

        response.raise_for_status()
        tree_data = response.json().get("tree", [])
        return [item["path"] for item in tree_data if item["type"] == "blob"]

    def get_workflow_run_log(self, owner: str, repo: str, run_id: int) -> str:
        """Fetch the logs for a specific workflow run to extract coverage metrics."""
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        return ""
