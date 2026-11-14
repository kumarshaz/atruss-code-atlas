# Data Model: Full Astro UI Extension (Feature 006)

## DiscoveryRepository

Source: `exports/latest/repos/repositories.json` (`items[]`)

| Field | Type | Notes |
|---|---|---|
| `Organization` | string | GitHub org slug (used as folder name) |
| `Project` | string | Same as org for GitHub |
| `RepositoryName` | string | Repo slug (used as file name) |
| `RepositoryId` | string | Numeric GitHub ID |
| `DefaultBranch` | string | e.g., `main` |
| `CloneUrl` | string | HTTPS clone URL |
| `WebUrl` | string | GitHub web URL |
| `Size` | number | Size in KB |
| `IsDisabled` | boolean | Archived/disabled flag |
| `IsPrivate` | boolean | Visibility flag |
| `LastUpdate` | string | ISO 8601 timestamp |
| `PrimaryLanguage` | string | Detected primary language or `"Unknown"` |
| `FrameworkType` | string | Detected framework or `"Unknown"` |
| `HasAPI` | boolean | Has API surface |
| `HasService` | boolean | Has service definitions |
| `HasFrontend` | boolean | Has frontend code |
| `HasDatabase` | boolean | Has database access |
| `TechnologyStack` | string | Comma-separated stack |
| `HasDockerfile` | boolean | Has a Dockerfile |
| `HasPipeline` | boolean | Has `.github/workflows/` |
| `HasKubernetes` | boolean | Has k8s manifests |
| `DocumentationPriority` | string | `P1`, `P2`, or `P3` |
| `AnalyzedDate` | string | ISO 8601 or empty if not analyzed |

---

## RepoStub (Generated Markdown Frontmatter)

Emitted by `scripts/generate-report-stubs.py` to `web/src/content/docs/reports/{org}/{repo}.md`.

| Frontmatter Key | Maps From | Type | Required |
|---|---|---|---|
| `title` | `RepositoryName` | string | ✅ |
| `description` | `{org} / {language} / {priority}` | string | ✅ |
| `org` | `Organization` | string | ✅ |
| `repo_name` | `RepositoryName` | string | ✅ |
| `language` | `PrimaryLanguage` | string | ✅ |
| `framework` | `FrameworkType` | string | optional |
| `has_pipeline` | `HasPipeline` | boolean | optional |
| `has_docker` | `HasDockerfile` | boolean | optional |
| `has_kubernetes` | `HasKubernetes` | boolean | optional |
| `has_api` | `HasAPI` | boolean | optional |
| `doc_priority` | `DocumentationPriority` | string | optional |
| `last_updated` | `LastUpdate` | string | optional |
| `github_url` | `WebUrl` | string (URL) | optional |

**Validation**: All keys are made optional in the Zod `docsSchema` extension to be resilient to partial data.

---

## PipelineWorkflow

Source: `exports/latest/pipelines/{repo}-pipeline.json` (Phase B)

```json
{
  "repo_name": "string",
  "org": "string",
  "analyzed_at": "ISO 8601",
  "workflows": [
    {
      "name": "filename.yml",
      "trigger": ["push", "pull_request"],
      "jobs": [
        { "id": "string", "name": "string", "needs": ["job-id"] }
      ],
      "anti_patterns": [
        { "type": "NO_TEST_GATE | UNMASKED_SECRET | MISSING_CACHE", "severity": "HIGH | MEDIUM | LOW", "message": "string" }
      ]
    }
  ]
}
```

---

## ArchitectureReport

Source: `exports/latest/reports/{repo}-report.md` (Phase C)

Raw Arc42 Markdown file with embedded triple-backtick mermaid blocks. Consumed directly by `ArchitectureView.astro` via `Astro.glob()`.

---

## OrgMaturityScore

Computed at build time from `DiscoveryRepository[]` grouped by `Organization`.

| Field | Type | Derivation |
|---|---|---|
| `org` | string | `Organization` key |
| `total_repos` | number | `count(items)` for org |
| `repos_with_pipeline` | number | `count(HasPipeline === true)` |
| `repos_with_docker` | number | `count(HasDockerfile === true)` |
| `pipeline_coverage_pct` | number | `(repos_with_pipeline / total_repos) × 100` |
| `maturity_score` | number (0–100) | See formula in plan.md R-005 |
