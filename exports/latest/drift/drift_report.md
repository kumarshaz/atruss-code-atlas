# Architectural & Pipeline Drift Report

- **Gate Status**: `REGRESSION DETECTED`
- **Baseline**: `/tmp/atruss_bench_prev_6b1pa9ci`
- **Target**: `exports/latest`
- **Regressions Count**: 61

## Summary Counts

| Dimension | Added / New | Removed / Resolved |
| :--- | :---: | :---: |
| Repositories | 0 | 307 |
| Architecture Components | 17 | 36851 |
| Pipeline Jobs | 2 | 4575 |
| Pipeline Anti-Patterns | 2 | 7558 |
| Fitness Violations | 3 | 874 |
| Vulnerabilities | 649 | 0 |
| Secrets | 33 | 1418 |

## Regressions

- **[HIGH]** `Azure-Samples/todo-nodejs-mongo-terraform` (scorecard_overall): Overall scorecard grade dropped from D to F (-3.58).
- **[HIGH]** `PostHog/posthog-elixir` (scorecard_dimension): Scorecard dimension 'security' dropped from B to F (-88.00).
- **[HIGH]** `PostHog/posthog-elixir` (scorecard_overall): Overall scorecard grade dropped from B to D (-18.14).
- **[HIGH]** `PostHog/posthog-elixir` (technical_debt): Technical debt score increased by 18.14 (12.90 -> 31.04).
- **[HIGH]** `argoproj/notifications-engine` (technical_debt): Technical debt score increased by 5.78 (21.70 -> 27.48).
- **[HIGH]** `dani-garcia/vaultwarden` (secret): New HIGH secret ATRUSS-SEC-005 in .env.template.
- **[HIGH]** `dani-garcia/vaultwarden` (secret): New HIGH secret ATRUSS-SEC-005 in src/static/scripts/datatables.js.
- **[HIGH]** `discourse/rails_failover` (scorecard_dimension): Scorecard dimension 'dependency_health' dropped from A to B (-13.64).
- **[HIGH]** `discourse/rails_failover` (scorecard_overall): Overall scorecard grade dropped from C to D (-10.05).
- **[HIGH]** `discourse/rails_failover` (technical_debt): Technical debt score increased by 10.05 (20.25 -> 30.30).
- **[HIGH]** `dotnet-architecture/eShopOnWeb` (scorecard_dimension): Scorecard dimension 'dependency_health' dropped from B to C (-5.84).
- **[HIGH]** `dotnet-architecture/eShopOnWeb` (scorecard_dimension): Scorecard dimension 'security' dropped from D to F (-64.00).
- **[HIGH]** `dotnet-architecture/eShopOnWeb` (scorecard_overall): Overall scorecard grade dropped from C to F (-13.68).
- **[HIGH]** `dotnet-architecture/eShopOnWeb` (technical_debt): Technical debt score increased by 13.68 (27.30 -> 40.98).
- **[HIGH]** `dotnet/eShop` (technical_debt): Technical debt score increased by 8.38 (47.95 -> 56.33).
- **[HIGH]** `getsentry/sentry-php` (scorecard_overall): Overall scorecard grade dropped from C to D (-10.51).
- **[HIGH]** `getsentry/sentry-php` (technical_debt): Technical debt score increased by 10.51 (22.59 -> 33.10).
- **[HIGH]** `github-samples/pets-workshop` (scorecard_dimension): Scorecard dimension 'security' dropped from A to F (-100.00).
- **[HIGH]** `github-samples/pets-workshop` (scorecard_overall): Overall scorecard grade dropped from B to D (-20.31).
- **[HIGH]** `github-samples/pets-workshop` (technical_debt): Technical debt score increased by 20.31 (19.40 -> 39.71).
- **[HIGH]** `hamvocke/spring-testing` (scorecard_dimension): Scorecard dimension 'dependency_health' dropped from B to C (-13.64).
- **[HIGH]** `hamvocke/spring-testing` (scorecard_dimension): Scorecard dimension 'security' dropped from A to F (-100.00).
- **[HIGH]** `hamvocke/spring-testing` (scorecard_overall): Overall scorecard grade dropped from C to F (-22.05).
- **[HIGH]** `hamvocke/spring-testing` (technical_debt): Technical debt score increased by 22.05 (21.65 -> 43.70).
- **[HIGH]** `kumarshaz/atruss-code-atlas` (scorecard_dimension): Scorecard dimension 'security' dropped from D to F (-63.00).
- **[HIGH]** `kumarshaz/atruss-code-atlas` (scorecard_overall): Overall scorecard grade dropped from D to F (-12.79).
- **[CRITICAL]** `kumarshaz/atruss-code-atlas` (secret): New CRITICAL secret ATRUSS-SEC-004 in exports/latest/reports/getsentry-spotlight-analysis.json.
- **[CRITICAL]** `kumarshaz/atruss-code-atlas` (secret): New CRITICAL secret ATRUSS-SEC-004 in exports/latest/reports/getsentry-spotlight-analysis.json.
- **[CRITICAL]** `kumarshaz/atruss-code-atlas` (secret): New CRITICAL secret ATRUSS-SEC-004 in exports/latest/reports/home-assistant-operating-system-analysis.json.
- **[CRITICAL]** `kumarshaz/atruss-code-atlas` (secret): New CRITICAL secret ATRUSS-SEC-004 in exports/latest/reports/keycloak-terraform-provider-keycloak-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/bitwarden-directory-connector-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/bitwarden-directory-connector-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/getsentry-snuba-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/getsentry-symbolicator-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-agento11y-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-agento11y-report.md.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-agento11y-report.md.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-alloy-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-alloy-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-beyla-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-beyla-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-beyla-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-gcx-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-gcx-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-grafana-ansible-collection-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-grafana-ansible-collection-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-grafana-ansible-collection-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-grafana-ansible-collection-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-grafana-foundation-sdk-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-helm-charts-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-helm-charts-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-loki-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-loki-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-traces-drilldown-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-traces-drilldown-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/grafana-traces-drilldown-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (secret): New HIGH secret ATRUSS-SEC-005 in exports/latest/reports/nextcloud-groupfolders-analysis.json.
- **[HIGH]** `kumarshaz/atruss-code-atlas` (technical_debt): Technical debt score increased by 12.79 (39.31 -> 52.10).
- **[HIGH]** `spring-projects/spring-petclinic` (scorecard_dimension): Scorecard dimension 'dependency_health' dropped from B to C (-9.00).
- **[HIGH]** `spring-projects/spring-petclinic` (scorecard_overall): Overall scorecard grade dropped from D to F (-9.35).
- **[HIGH]** `spring-projects/spring-petclinic` (technical_debt): Technical debt score increased by 9.35 (34.80 -> 44.15).

## Scorecard Transitions

- **Azure-Samples/todo-nodejs-mongo-terraform**: Overall `D` -> `F` (score delta `-3.58`, debt delta `+3.58`)
  - `dependency_health`: `A` -> `A` (`-2.54`)
  - `security`: `F` -> `F` (`-16.00`)
- **PostHog/posthog-elixir**: Overall `B` -> `D` (score delta `-18.14`, debt delta `+18.14`)
  - `dependency_health`: `A` -> `A` (`-3.57`)
  - `security`: `B` -> `F` (`-88.00`)
- **argoproj/notifications-engine**: Overall `C` -> `C` (score delta `-5.78`, debt delta `+5.78`)
  - `dependency_health`: `B` -> `B` (`-3.85`)
  - `security`: `F` -> `F` (`-26.00`)
- **dani-garcia/vaultwarden**: Overall `D` -> `D` (score delta `-0.22`, debt delta `+0.22`)
  - `code_quality`: `A` -> `A` (`+0.09`)
  - `dependency_health`: `A` -> `A` (`-1.59`)
- **discourse/rails_failover**: Overall `C` -> `D` (score delta `-10.05`, debt delta `+10.05`)
  - `dependency_health`: `A` -> `B` (`-13.64`)
  - `security`: `F` -> `F` (`-40.00`)
- **dotnet-architecture/eShopOnWeb**: Overall `C` -> `F` (score delta `-13.68`, debt delta `+13.68`)
  - `dependency_health`: `B` -> `C` (`-5.84`)
  - `security`: `D` -> `F` (`-64.00`)
- **dotnet/eShop**: Overall `F` -> `F` (score delta `-8.38`, debt delta `+8.38`)
  - `dependency_health`: `A` -> `A` (`-5.20`)
  - `security`: `F` -> `F` (`-38.00`)
- **getsentry/sentry-php**: Overall `C` -> `D` (score delta `-10.51`, debt delta `+10.51`)
  - `dependency_health`: `A` -> `A` (`-9.09`)
  - `pipeline_health`: `F` -> `F` (`+3.00`)
  - `security`: `F` -> `F` (`-48.00`)
- **github-samples/pets-workshop**: Overall `B` -> `D` (score delta `-20.31`, debt delta `+20.31`)
  - `dependency_health`: `A` -> `A` (`-2.09`)
  - `security`: `A` -> `F` (`-100.00`)
- **hamvocke/spring-testing**: Overall `C` -> `F` (score delta `-22.05`, debt delta `+22.05`)
  - `dependency_health`: `B` -> `C` (`-13.64`)
  - `security`: `A` -> `F` (`-100.00`)
- **kumarshaz/atruss-code-atlas**: Overall `D` -> `F` (score delta `-12.79`, debt delta `+12.79`)
  - `code_quality`: `F` -> `F` (`-8.00`)
  - `dependency_health`: `A` -> `A` (`-1.76`)
  - `maintainability`: `F` -> `F` (`-18.82`)
  - `pipeline_health`: `D` -> `A` (`+30.00`)
  - `security`: `D` -> `F` (`-63.00`)
- **nextcloud/docker**: Overall `B` -> `B` (score delta `+0.00`, debt delta `+0.00`)
- **spring-projects/spring-petclinic**: Overall `D` -> `F` (score delta `-9.35`, debt delta `+9.35`)
  - `dependency_health`: `B` -> `C` (`-9.00`)
  - `security`: `F` -> `F` (`-40.00`)
