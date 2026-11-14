# Data Models: Atruss Astro Dashboard

## 1. Summary Metric (Dashboard Component)

This structure represents the aggregate data passed into the `AtlasSummary.astro` component from the underlying data JSON/YAML structures.

- **Entity**: `DashboardMetrics`
- **Fields**:
  - `totalRepositories` (Integer): Total number of repos discovered.
  - `totalPipelines` (Integer): Total CI/CD workflows identified.
  - `architecturalComplexity` (Float): An average composite score of AST cyclomatic complexity metric.
  - `criticalAntiPatterns` (Integer): Total number of pipeline or structural anti-patterns found across the org.
- **Validation Rules**:
  - Fields must be parsed correctly from `.json` and `.yaml` outputs in `/exports/latest/`. Fallbacks to `0` or `"N/A"` are permitted if data is entirely absent.

## 2. Report Link (Navigation State)

This structure represents a generated card pushing the user to the `src/content/docs/reports/` directories.

- **Entity**: `MarkdownReportLink`
- **Fields**:
  - `title` (String): e.g., 'Payment Service Architecture'
  - `href` (String): e.g., `/reports/payment-service/`
  - `category` (String): 'discovery' | 'pipeline' | 'architecture'
- **Relationships**:
  - Embedded as a list inside the `AtlasSummary` component to render the navigation cards.
