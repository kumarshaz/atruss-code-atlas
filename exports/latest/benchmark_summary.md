# Atruss Code Atlas Benchmark Scorecard

- **Run ID**: `2026-11-25_15-48-39`
- **Mode**: `corpus` (seed `42`)
- **Window**: 2026-11-25T15:48:39Z -> 2026-11-25T15:49:22Z
- **Repositories Evaluated**: 13
- **Crash-Free Completion**: 13/13 (100.0%)
- **Classification Accuracy**: 13/13 (100.0%)
- **Pipeline Parse Rate**: 11/13 (84.62%)
- **Average Runtime / Repo**: 4.734s
- **SLA Compliance (<=180s)**: 13/13 (100.0%)
- **Anomalies Recorded**: 0

## Ecosystem Breakdown

| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |
| --- | ---: | ---: | ---: | ---: |
| .NET | 2 | 2 | 2/2 | 4.538s |
| Container / Helm / IaC | 1 | 1 | 1/1 | 0.888s |
| Elixir | 1 | 1 | 1/1 | 1.846s |
| Go | 1 | 1 | 1/1 | 1.424s |
| Java | 2 | 2 | 2/2 | 1.22s |
| JavaScript/TypeScript | 2 | 2 | 2/2 | 2.76s |
| PHP | 1 | 1 | 1/1 | 2.508s |
| Python | 1 | 1 | 1/1 | 32.648s |
| Ruby | 1 | 1 | 1/1 | 1.038s |
| Rust | 1 | 1 | 1/1 | 4.159s |

## Repository Results

| Repository | Expected | Detected | Framework | Workflows | Components | Status | Duration |
| --- | --- | --- | --- | ---: | ---: | --- | ---: |
| kumarshaz/atruss-code-atlas | Python | Python | Unknown | 4 | 44 | passed | 32.648s |
| dotnet/eShop | .NET | .NET | ASP.NET Core | 5 | 124 | passed | 6.459s |
| dotnet-architecture/eShopOnWeb | .NET | .NET | ASP.NET Core | 2 | 38 | passed | 2.617s |
| github-samples/pets-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Astro | 0 | 6 | passed | 1.881s |
| Azure-Samples/todo-nodejs-mongo-terraform | JavaScript/TypeScript | JavaScript/TypeScript | React (Vite) | 1 | 23 | passed | 3.64s |
| spring-projects/spring-petclinic | Java | Java | Spring Boot | 3 | 17 | passed | 1.521s |
| hamvocke/spring-testing | Java | Java | Spring Boot | 0 | 3 | passed | 0.919s |
| argoproj/notifications-engine | Go | Go | Go Service | 1 | 82 | passed | 1.424s |
| dani-garcia/vaultwarden | Rust | Rust | Axum / Actix / Rocket | 9 | 68 | passed | 4.159s |
| discourse/rails_failover | Ruby | Ruby | Ruby on Rails | 1 | 51 | passed | 1.038s |
| getsentry/sentry-php | PHP | PHP | Symfony | 5 | 251 | passed | 2.508s |
| PostHog/posthog-elixir | Elixir | Elixir | Elixir Mix | 8 | 95 | passed | 1.846s |
| nextcloud/docker | Container / Helm / IaC | Container / Helm / IaC | Docker Compose | 2 | 8 | passed | 0.888s |
