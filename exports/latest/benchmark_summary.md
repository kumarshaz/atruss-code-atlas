# Atruss Code Atlas Benchmark Scorecard

- **Run ID**: `2026-11-26_15-29-01`
- **Mode**: `corpus` (seed `42`)
- **Window**: 2026-11-26T15:29:01Z -> 2026-11-26T15:29:43Z
- **Repositories Evaluated**: 13
- **Crash-Free Completion**: 13/13 (100.0%)
- **Classification Accuracy**: 13/13 (100.0%)
- **Pipeline Parse Rate**: 11/13 (84.62%)
- **Average Runtime / Repo**: 4.949s
- **SLA Compliance (<=180s)**: 13/13 (100.0%)
- **Anomalies Recorded**: 0

## Ecosystem Breakdown

| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |
| --- | ---: | ---: | ---: | ---: |
| .NET | 2 | 2 | 2/2 | 4.639s |
| Container / Helm / IaC | 1 | 1 | 1/1 | 1.175s |
| Elixir | 1 | 1 | 1/1 | 2.272s |
| Go | 1 | 1 | 1/1 | 1.22s |
| Java | 2 | 2 | 2/2 | 1.738s |
| JavaScript/TypeScript | 2 | 2 | 2/2 | 2.862s |
| PHP | 1 | 1 | 1/1 | 2.504s |
| Python | 1 | 1 | 1/1 | 33.216s |
| Ruby | 1 | 1 | 1/1 | 0.941s |
| Rust | 1 | 1 | 1/1 | 4.528s |

## Repository Results

| Repository | Expected | Detected | Framework | Workflows | Components | Status | Duration |
| --- | --- | --- | --- | ---: | ---: | --- | ---: |
| kumarshaz/atruss-code-atlas | Python | Python | Unknown | 4 | 44 | passed | 33.216s |
| dotnet/eShop | .NET | .NET | ASP.NET Core | 5 | 124 | passed | 6.467s |
| dotnet-architecture/eShopOnWeb | .NET | .NET | ASP.NET Core | 2 | 38 | passed | 2.811s |
| github-samples/pets-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Astro | 0 | 6 | passed | 1.987s |
| Azure-Samples/todo-nodejs-mongo-terraform | JavaScript/TypeScript | JavaScript/TypeScript | React (Vite) | 1 | 23 | passed | 3.736s |
| spring-projects/spring-petclinic | Java | Java | Spring Boot | 3 | 17 | passed | 2.576s |
| hamvocke/spring-testing | Java | Java | Spring Boot | 0 | 3 | passed | 0.899s |
| argoproj/notifications-engine | Go | Go | Go Service | 1 | 82 | passed | 1.22s |
| dani-garcia/vaultwarden | Rust | Rust | Axum / Actix / Rocket | 9 | 68 | passed | 4.528s |
| discourse/rails_failover | Ruby | Ruby | Ruby on Rails | 1 | 51 | passed | 0.941s |
| getsentry/sentry-php | PHP | PHP | Symfony | 5 | 251 | passed | 2.504s |
| PostHog/posthog-elixir | Elixir | Elixir | Elixir Mix | 8 | 96 | passed | 2.272s |
| nextcloud/docker | Container / Helm / IaC | Container / Helm / IaC | Docker Compose | 2 | 8 | passed | 1.175s |
