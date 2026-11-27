# Atruss Code Atlas Benchmark Scorecard

- **Run ID**: `2026-11-27_15-20-13`
- **Mode**: `corpus` (seed `42`)
- **Window**: 2026-11-27T15:20:13Z -> 2026-11-27T15:20:53Z
- **Repositories Evaluated**: 13
- **Crash-Free Completion**: 13/13 (100.0%)
- **Classification Accuracy**: 13/13 (100.0%)
- **Pipeline Parse Rate**: 11/13 (84.62%)
- **Average Runtime / Repo**: 4.454s
- **SLA Compliance (<=180s)**: 13/13 (100.0%)
- **Anomalies Recorded**: 0

## Ecosystem Breakdown

| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |
| --- | ---: | ---: | ---: | ---: |
| .NET | 2 | 2 | 2/2 | 3.986s |
| Container / Helm / IaC | 1 | 1 | 1/1 | 0.815s |
| Elixir | 1 | 1 | 1/1 | 1.634s |
| Go | 1 | 1 | 1/1 | 1.116s |
| Java | 2 | 2 | 2/2 | 1.046s |
| JavaScript/TypeScript | 2 | 2 | 2/2 | 2.377s |
| PHP | 1 | 1 | 1/1 | 2.838s |
| Python | 1 | 1 | 1/1 | 31.505s |
| Ruby | 1 | 1 | 1/1 | 0.747s |
| Rust | 1 | 1 | 1/1 | 4.425s |

## Repository Results

| Repository | Expected | Detected | Framework | Workflows | Components | Status | Duration |
| --- | --- | --- | --- | ---: | ---: | --- | ---: |
| kumarshaz/atruss-code-atlas | Python | Python | Unknown | 4 | 44 | passed | 31.505s |
| dotnet/eShop | .NET | .NET | ASP.NET Core | 5 | 124 | passed | 5.685s |
| dotnet-architecture/eShopOnWeb | .NET | .NET | ASP.NET Core | 2 | 38 | passed | 2.288s |
| github-samples/pets-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Astro | 0 | 6 | passed | 1.374s |
| Azure-Samples/todo-nodejs-mongo-terraform | JavaScript/TypeScript | JavaScript/TypeScript | React (Vite) | 1 | 23 | passed | 3.379s |
| spring-projects/spring-petclinic | Java | Java | Spring Boot | 3 | 17 | passed | 1.377s |
| hamvocke/spring-testing | Java | Java | Spring Boot | 0 | 3 | passed | 0.716s |
| argoproj/notifications-engine | Go | Go | Go Service | 1 | 82 | passed | 1.116s |
| dani-garcia/vaultwarden | Rust | Rust | Axum / Actix / Rocket | 9 | 68 | passed | 4.425s |
| discourse/rails_failover | Ruby | Ruby | Ruby on Rails | 1 | 51 | passed | 0.747s |
| getsentry/sentry-php | PHP | PHP | Symfony | 5 | 251 | passed | 2.838s |
| PostHog/posthog-elixir | Elixir | Elixir | Elixir Mix | 8 | 96 | passed | 1.634s |
| nextcloud/docker | Container / Helm / IaC | Container / Helm / IaC | Docker Compose | 2 | 8 | passed | 0.815s |
