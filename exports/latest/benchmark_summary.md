# Atruss Code Atlas Benchmark Scorecard

- **Run ID**: `2026-11-28_14-22-07`
- **Mode**: `corpus` (seed `42`)
- **Window**: 2026-11-28T14:22:07Z -> 2026-11-28T14:23:13Z
- **Repositories Evaluated**: 13
- **Crash-Free Completion**: 13/13 (100.0%)
- **Classification Accuracy**: 13/13 (100.0%)
- **Pipeline Parse Rate**: 11/13 (84.62%)
- **Average Runtime / Repo**: 7.231s
- **SLA Compliance (<=180s)**: 13/13 (100.0%)
- **Anomalies Recorded**: 0

## Ecosystem Breakdown

| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |
| --- | ---: | ---: | ---: | ---: |
| .NET | 2 | 2 | 2/2 | 6.703s |
| Container / Helm / IaC | 1 | 1 | 1/1 | 1.299s |
| Elixir | 1 | 1 | 1/1 | 2.87s |
| Go | 1 | 1 | 1/1 | 1.769s |
| Java | 2 | 2 | 2/2 | 1.858s |
| JavaScript/TypeScript | 2 | 2 | 2/2 | 3.69s |
| PHP | 1 | 1 | 1/1 | 3.22s |
| Python | 1 | 1 | 1/1 | 52.964s |
| Ruby | 1 | 1 | 1/1 | 1.315s |
| Rust | 1 | 1 | 1/1 | 6.063s |

## Repository Results

| Repository | Expected | Detected | Framework | Workflows | Components | Status | Duration |
| --- | --- | --- | --- | ---: | ---: | --- | ---: |
| kumarshaz/atruss-code-atlas | Python | Python | Unknown | 4 | 44 | passed | 52.964s |
| dotnet/eShop | .NET | .NET | ASP.NET Core | 5 | 124 | passed | 9.647s |
| dotnet-architecture/eShopOnWeb | .NET | .NET | ASP.NET Core | 2 | 38 | passed | 3.758s |
| github-samples/pets-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Astro | 0 | 6 | passed | 2.176s |
| Azure-Samples/todo-nodejs-mongo-terraform | JavaScript/TypeScript | JavaScript/TypeScript | React (Vite) | 1 | 23 | passed | 5.203s |
| spring-projects/spring-petclinic | Java | Java | Spring Boot | 3 | 17 | passed | 2.47s |
| hamvocke/spring-testing | Java | Java | Spring Boot | 0 | 3 | passed | 1.246s |
| argoproj/notifications-engine | Go | Go | Go Service | 1 | 82 | passed | 1.769s |
| dani-garcia/vaultwarden | Rust | Rust | Axum / Actix / Rocket | 9 | 68 | passed | 6.063s |
| discourse/rails_failover | Ruby | Ruby | Ruby on Rails | 1 | 51 | passed | 1.315s |
| getsentry/sentry-php | PHP | PHP | Symfony | 5 | 251 | passed | 3.22s |
| PostHog/posthog-elixir | Elixir | Elixir | Elixir Mix | 8 | 96 | passed | 2.87s |
| nextcloud/docker | Container / Helm / IaC | Container / Helm / IaC | Docker Compose | 2 | 8 | passed | 1.299s |
