# Atruss Code Atlas Benchmark Scorecard

- **Run ID**: `2026-11-23_17-34-41`
- **Mode**: `corpus` (seed `42`)
- **Window**: 2026-11-23T17:34:41Z -> 2026-11-23T17:35:17Z
- **Repositories Evaluated**: 13
- **Crash-Free Completion**: 13/13 (100.0%)
- **Classification Accuracy**: 13/13 (100.0%)
- **Pipeline Parse Rate**: 11/13 (84.62%)
- **Average Runtime / Repo**: 5.205s
- **SLA Compliance (<=180s)**: 13/13 (100.0%)
- **Anomalies Recorded**: 0

## Ecosystem Breakdown

| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |
| --- | ---: | ---: | ---: | ---: |
| .NET | 2 | 2 | 2/2 | 4.863s |
| Container / Helm / IaC | 1 | 1 | 1/1 | 1.411s |
| Elixir | 1 | 1 | 1/1 | 2.591s |
| Go | 1 | 1 | 1/1 | 1.724s |
| Java | 2 | 2 | 2/2 | 1.78s |
| JavaScript/TypeScript | 2 | 2 | 2/2 | 3.151s |
| PHP | 1 | 1 | 1/1 | 2.54s |
| Python | 1 | 1 | 1/1 | 33.784s |
| Ruby | 1 | 1 | 1/1 | 1.269s |
| Rust | 1 | 1 | 1/1 | 4.761s |

## Repository Results

| Repository | Expected | Detected | Framework | Workflows | Components | Status | Duration |
| --- | --- | --- | --- | ---: | ---: | --- | ---: |
| kumarshaz/atruss-code-atlas | Python | Python | Unknown | 4 | 44 | passed | 33.784s |
| dotnet/eShop | .NET | .NET | ASP.NET Core | 4 | 124 | passed | 6.547s |
| dotnet-architecture/eShopOnWeb | .NET | .NET | ASP.NET Core | 2 | 38 | passed | 3.179s |
| github-samples/pets-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Astro | 0 | 6 | passed | 2.256s |
| Azure-Samples/todo-nodejs-mongo-terraform | JavaScript/TypeScript | JavaScript/TypeScript | React (Vite) | 1 | 23 | passed | 4.047s |
| spring-projects/spring-petclinic | Java | Java | Spring Boot | 3 | 17 | passed | 2.384s |
| hamvocke/spring-testing | Java | Java | Spring Boot | 0 | 3 | passed | 1.175s |
| argoproj/notifications-engine | Go | Go | Go Service | 1 | 82 | passed | 1.724s |
| dani-garcia/vaultwarden | Rust | Rust | Axum / Actix / Rocket | 9 | 68 | passed | 4.761s |
| discourse/rails_failover | Ruby | Ruby | Ruby on Rails | 1 | 51 | passed | 1.269s |
| getsentry/sentry-php | PHP | PHP | Symfony | 5 | 251 | passed | 2.54s |
| PostHog/posthog-elixir | Elixir | Elixir | Elixir Mix | 8 | 94 | passed | 2.591s |
| nextcloud/docker | Container / Helm / IaC | Container / Helm / IaC | Docker Compose | 2 | 8 | passed | 1.411s |
