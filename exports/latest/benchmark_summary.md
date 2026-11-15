# Atruss Code Atlas Benchmark Scorecard

- **Run ID**: `2026-11-15_05-24-40`
- **Mode**: `corpus` (seed `42`)
- **Window**: 2026-11-15T05:24:40Z -> 2026-11-15T05:24:40Z
- **Repositories Evaluated**: 372
- **Crash-Free Completion**: 320/372 (86.02%)
- **Classification Accuracy**: 273/320 (85.31%)
- **Pipeline Parse Rate**: 275/372 (73.92%)
- **Average Runtime / Repo**: 21.29s
- **SLA Compliance (<=180s)**: 320/372 (86.02%)
- **Anomalies Recorded**: 52

## Ecosystem Breakdown

| Ecosystem | Evaluated | Passed | Classification Match | Avg Runtime (s) |
| --- | ---: | ---: | ---: | ---: |
| .NET | 8 | 7 | 7/8 | 20.625s |
| Container / Helm / IaC | 54 | 54 | 32/54 | 15.0s |
| Elixir | 6 | 6 | 6/6 | 15.0s |
| Go | 51 | 49 | 44/51 | 16.765s |
| Java | 30 | 20 | 20/30 | 30.0s |
| JavaScript/TypeScript | 152 | 123 | 108/152 | 23.586s |
| PHP | 14 | 13 | 11/14 | 18.214s |
| Python | 34 | 28 | 27/34 | 22.941s |
| Ruby | 8 | 7 | 7/8 | 20.625s |
| Rust | 15 | 13 | 11/15 | 21.0s |

## Repository Results

| Repository | Expected | Detected | Framework | Workflows | Components | Status | Duration |
| --- | --- | --- | --- | ---: | ---: | --- | ---: |
| dotnet/eShop | .NET | .NET | Unknown | 4 | 124 | passed | 15.0s |
| dotnet-architecture/eShopOnWeb | .NET | .NET | Unknown | 2 | 38 | passed | 15.0s |
| github-samples/pets-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 6 | passed | 15.0s |
| Azure-Samples/todo-nodejs-mongo-terraform | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 23 | passed | 15.0s |
| jeffrafter/example-github-action-typescript | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 1 | passed | 15.0s |
| benchmark-action/github-action-benchmark | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 16 | 10 | passed | 15.0s |
| hamvocke/spring-testing | Java | Java | Unknown | 0 | 3 | passed | 15.0s |
| spring-projects/spring-petclinic | Java | Java | Unknown | 3 | 17 | passed | 15.0s |
| n8n-io/n8n | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| immich-app/immich | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 27 | 238 | passed | 15.0s |
| supabase/supabase | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| home-assistant/core | Python | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| grafana/grafana | JavaScript/TypeScript | Go | Unknown | 100 | 261 | passed | 15.0s |
| apache/superset | Python | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| dani-garcia/vaultwarden | Rust | Rust | Unknown | 9 | 67 | passed | 15.0s |
| pocketbase/pocketbase | Go | Go | Unknown | 1 | 251 | passed | 15.0s |
| twentyhq/twenty | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| go-gitea/gitea | Go | Go | Unknown | 13 | 251 | passed | 15.0s |
| appwrite/appwrite | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| laurent22/joplin | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 11 | 475 | passed | 15.0s |
| TryGhost/Ghost | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 25 | 2000 | passed | 15.0s |
| mastodon/mastodon | Ruby | Ruby | Unknown | 22 | 255 | passed | 15.0s |
| metabase/metabase | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| calcom/cal.diy | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 45 | 1928 | passed | 15.0s |
| discourse/discourse | Ruby | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/airflow | Python | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| RocketChat/Rocket.Chat | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| getsentry/sentry | Python | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| PostHog/posthog | Python | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| umami-software/umami | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 5 | 595 | passed | 15.0s |
| chatwoot/chatwoot | Ruby | Ruby | Unknown | 17 | 253 | passed | 15.0s |
| mattermost/mattermost | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 22 | 721 | passed | 15.0s |
| harness/harness | Go | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| directus/directus | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 18 | 437 | passed | 15.0s |
| keycloak/keycloak | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| nextcloud/server | PHP | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| langfuse/langfuse | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| medusajs/medusa | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| backstage/backstage | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| plausible/analytics | Elixir | Elixir | Unknown | 15 | 459 | passed | 15.0s |
| goharbor/harbor | Go | Go | Unknown | 11 | 5 | passed | 15.0s |
| grafana/loki | Go | Go | Unknown | 26 | 270 | passed | 15.0s |
| zulip/zulip | Python | Python | Unknown | 8 | 108 | passed | 15.0s |
| argoproj/argo-cd | Go | Go | Unknown | 17 | 280 | passed | 15.0s |
| saleor/saleor | Python | Python | Unknown | 22 | 97 | passed | 15.0s |
| bitwarden/server | .NET | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| argoproj/argo-workflows | Go | Go | Unknown | 18 | 294 | passed | 15.0s |
| triggerdotdev/trigger.dev | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| bitwarden/clients | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| formbricks/formbricks | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| nextcloud/all-in-one | PHP | PHP | Unknown | 31 | 68 | passed | 15.0s |
| getsentry/self-hosted | Container / Helm / IaC | Python | Unknown | 7 | 3 | passed | 15.0s |
| woodpecker-ci/woodpecker | Go | Go | Unknown | 0 | 266 | passed | 15.0s |
| supabase/realtime | Elixir | Elixir | Unknown | 22 | 253 | passed | 15.0s |
| home-assistant/operating-system | Python | Python | Unknown | 9 | 0 | passed | 15.0s |
| nextcloud/docker | Container / Helm / IaC | Container / Helm / IaC | Unknown | 2 | 8 | passed | 15.0s |
| home-assistant/frontend | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 23 | 75 | passed | 15.0s |
| grafana/mimir | Go | Go | Unknown | 19 | 306 | passed | 15.0s |
| nextcloud/desktop | Container / Helm / IaC | JavaScript/TypeScript | Unknown | 20 | 0 | passed | 15.0s |
| plausible/community-edition | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 1 | passed | 15.0s |
| pocketbase/js-sdk | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 19 | passed | 15.0s |
| medusajs/nextjs-starter-medusa | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 23 | passed | 15.0s |
| mattermost/mattermost-mobile | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| supabase/auth | Go | Go | Unknown | 5 | 250 | passed | 15.0s |
| RocketChat/Rocket.Chat.ReactNative | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| argoproj/argo-helm | Container / Helm / IaC | Python | Unknown | 10 | 297 | passed | 15.0s |
| keycloak/keycloak-quickstarts | Java | Java | Unknown | 6 | 60 | passed | 15.0s |
| supabase/supavisor | Elixir | Elixir | Unknown | 7 | 254 | passed | 15.0s |
| home-assistant/supervisor | Python | Python | Unknown | 8 | 27 | passed | 15.0s |
| owncloud/ocis | Go | Go | Unknown | 14 | 316 | passed | 15.0s |
| grafana/helm-charts | Container / Helm / IaC | Container / Helm / IaC | Unknown | 9 | 253 | passed | 15.0s |
| discourse/discourse_docker | Container / Helm / IaC | Ruby | Unknown | 3 | 12 | passed | 15.0s |
| n8n-io/n8n-hosting | Container / Helm / IaC | Container / Helm / IaC | Unknown | 6 | 189 | passed | 15.0s |
| saleor/storefront | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 6 | 313 | passed | 15.0s |
| goharbor/harbor-helm | Container / Helm / IaC | Go | Unknown | 5 | 4 | passed | 15.0s |
| keycloak/keycloak-containers | Container / Helm / IaC | Unknown | Unknown | 0 | 0 | passed | 15.0s |
| supabase/storage | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 8 | 130 | passed | 15.0s |
| saleor/saleor-dashboard | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 27 | 3152 | passed | 15.0s |
| zulip/zulip-desktop | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 1 | passed | 15.0s |
| bitwarden/self-host | Container / Helm / IaC | Container / Helm / IaC | Unknown | 6 | 2 | passed | 15.0s |
| saleor/saleor-platform | Container / Helm / IaC | Container / Helm / IaC | Unknown | 1 | 2 | passed | 15.0s |
| zulip/docker-zulip | Container / Helm / IaC | JavaScript/TypeScript | Unknown | 7 | 19 | passed | 15.0s |
| pocketbase/dart-sdk | Container / Helm / IaC | Unknown | Unknown | 0 | 0 | passed | 15.0s |
| PostHog/posthog-js | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| owncloud/web | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 10 | 54 | passed | 15.0s |
| mattermost/docker | Container / Helm / IaC | Container / Helm / IaC | Unknown | 2 | 5 | passed | 15.0s |
| TryGhost/Ghost-CLI | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 4 | passed | 15.0s |
| backstage/community-plugins | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 21 | 437 | passed | 15.0s |
| getsentry/relay | Rust | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| appwrite/console | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 8 | 1 | passed | 15.0s |
| goharbor/harbor-operator | Go | Go | Unknown | 8 | 362 | passed | 15.0s |
| RocketChat/Docker.Official.Image | Container / Helm / IaC | Container / Helm / IaC | Unknown | 3 | 5 | passed | 15.0s |
| open-runtimes/open-runtimes | PHP | JavaScript/TypeScript | Unknown | 3 | 98 | passed | 15.0s |
| backstage/charts | Container / Helm / IaC | Container / Helm / IaC | Unknown | 7 | 48 | passed | 15.0s |
| mattermost/mattermost-operator | Go | Go | Unknown | 4 | 179 | passed | 15.0s |
| drone-runners/drone-runner-kube | Go | Go | Unknown | 0 | 67 | passed | 15.0s |
| drone-runners/drone-runner-docker | Go | Go | Unknown | 0 | 52 | passed | 15.0s |
| TryGhost/ghost-docker | Container / Helm / IaC | Container / Helm / IaC | Unknown | 3 | 6 | passed | 15.0s |
| chatwoot/charts | Container / Helm / IaC | Container / Helm / IaC | Unknown | 2 | 11 | passed | 15.0s |
| PostHog/charts-clickhouse | Python | Python | Unknown | 15 | 137 | passed | 15.0s |
| PostHog/posthog-python | Python | Python | Unknown | 12 | 45 | passed | 15.0s |
| owncloud/ocis-charts | Container / Helm / IaC | Go | Unknown | 0 | 184 | passed | 15.0s |
| woodpecker-ci/helm | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 42 | passed | 15.0s |
| RocketChat/helm-charts | Container / Helm / IaC | Container / Helm / IaC | Unknown | 4 | 77 | passed | 15.0s |
| kumarshaz/atruss-code-atlas | Python | Python | Unknown | 3 | 30 | passed | 15.0s |
| apache/flink | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/skywalking | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/hadoop | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| n8n-io/self-hosted-ai-starter-kit | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 1 | passed | 15.0s |
| apache/pulsar | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| triggerdotdev/jsonhero-web | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 147 | passed | 15.0s |
| home-assistant/home-assistant.io | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| bitwarden/android | Java | Java | Unknown | 19 | 1 | passed | 15.0s |
| apache/shenyu | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| owncloud/core | PHP | PHP | Unknown | 0 | 250 | passed | 15.0s |
| getsentry/sentry-javascript | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 27 | 1558 | passed | 15.0s |
| apache/beam | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/iotdb | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/maka | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| supabase/supabase-js | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 17 | 44 | passed | 15.0s |
| owncloud/android | Java | Java | Unknown | 11 | 0 | passed | 15.0s |
| home-assistant/android | Java | Java | Unknown | 12 | 1 | passed | 15.0s |
| grafana/alloy | Go | Go | Unknown | 61 | 351 | passed | 15.0s |
| argoproj/argo-rollouts | Go | Go | Unknown | 13 | 299 | passed | 15.0s |
| supabase/pg_graphql | Rust | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/cloudstack | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/parquet-java | Java | Java | Unknown | 8 | 18 | passed | 15.0s |
| supabase/agent-skills | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 1 | passed | 15.0s |
| supabase/mcp | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 6 | 5 | passed | 15.0s |
| argoproj/argo-events | Go | Go | Unknown | 8 | 281 | passed | 15.0s |
| supabase/supabase-py | Python | Python | Unknown | 7 | 106 | passed | 15.0s |
| TryGhost/Casper | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 1 | passed | 15.0s |
| supabase/cli | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| apache/activemq | Java | Java | Unknown | 6 | 79 | passed | 15.0s |
| supabase/etl | Rust | Rust | Unknown | 16 | 270 | passed | 15.0s |
| mattermost/desktop | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 26 | 230 | passed | 15.0s |
| home-assistant/apps | Container / Helm / IaC | Container / Helm / IaC | Unknown | 4 | 3 | passed | 15.0s |
| grafana/grafana-zabbix | JavaScript/TypeScript | Go | Unknown | 7 | 69 | passed | 15.0s |
| apache/fluss | Java | Java | Unknown | 19 | 437 | passed | 15.0s |
| nextcloud/spreed | JavaScript/TypeScript | PHP | Unknown | 40 | 250 | passed | 15.0s |
| getsentry/sentry-python | Python | Python | Unknown | 23 | 84 | passed | 15.0s |
| argoproj/argocd-example-apps | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 54 | passed | 15.0s |
| grafana/beyla | Go | Go | Unknown | 31 | 208 | passed | 15.0s |
| mastodon/mastodon-android | Java | Java | Unknown | 4 | 0 | passed | 15.0s |
| getsentry/sentry-php | PHP | PHP | Unknown | 6 | 251 | passed | 15.0s |
| apache/auron | Rust | Java | Unknown | 18 | 232 | passed | 15.0s |
| getsentry/sentry-react-native | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 24 | 133 | passed | 15.0s |
| supabase/postgres | Container / Helm / IaC | Go | Unknown | 23 | 54 | passed | 15.0s |
| calcom/sans | Python | Python | Unknown | 0 | 0 | passed | 15.0s |
| mastodon/documentation | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 0 | passed | 15.0s |
| RocketChat/Rocket.Chat.Electron | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 178 | passed | 15.0s |
| nextcloud/vm | Container / Helm / IaC | PHP | Unknown | 6 | 1 | passed | 15.0s |
| getsentry/sentry-java | Java | Java | Unknown | 16 | 117 | passed | 15.0s |
| getsentry/sentry-laravel | PHP | PHP | Unknown | 4 | 141 | passed | 15.0s |
| zulip/zulip-mobile | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| n8n-io/nod | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| n8n-io/n8n-nodes-starter | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 1 | passed | 15.0s |
| PostHog/posthog.com | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| getsentry/skills | Python | Python | Unknown | 0 | 0 | passed | 15.0s |
| getsentry/sentry-go | Go | Go | Unknown | 6 | 235 | passed | 15.0s |
| chatwoot/chatwoot-mobile-app | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| nextcloud/mail | JavaScript/TypeScript | PHP | Unknown | 23 | 250 | passed | 15.0s |
| supabase/edge-runtime | Rust | JavaScript/TypeScript | Unknown | 6 | 131 | passed | 15.0s |
| getsentry/toolkit | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| keycloak/terraform-provider-keycloak | Go | Go | Unknown | 5 | 250 | passed | 15.0s |
| apache/camel-k | Go | Go | Unknown | 23 | 300 | passed | 15.0s |
| supabase/wrappers | Rust | Rust | Unknown | 8 | 144 | passed | 15.0s |
| zulip/zulip-terminal | Python | Python | Unknown | 2 | 0 | passed | 15.0s |
| supabase/supabase-kt | Java | Java | Unknown | 9 | 0 | passed | 15.0s |
| grafana/gcx | Go | Go | Unknown | 9 | 250 | passed | 15.0s |
| apache/wicket | Java | Java | Unknown | 1 | 41 | passed | 15.0s |
| TryGhost/docker-library-ghost | Container / Helm / IaC | Container / Helm / IaC | Unknown | 3 | 4 | passed | 15.0s |
| getsentry/sentry-dotnet | .NET | .NET | Unknown | 19 | 156 | passed | 15.0s |
| metabase/dataset-generator | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 12 | passed | 15.0s |
| argoproj/argoproj | Python | Python | Unknown | 0 | 0 | passed | 15.0s |
| keycloak/keycloak-nodejs-connect | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 30 | passed | 15.0s |
| getsentry/sentry-symfony | PHP | PHP | Unknown | 4 | 222 | passed | 15.0s |
| PostHog/posthog-foss | Python | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| nextcloud/photos | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 26 | 1 | passed | 15.0s |
| supabase/supabase-csharp | .NET | .NET | Unknown | 5 | 37 | passed | 15.0s |
| grafana/k8s-monitoring-helm | Container / Helm / IaC | Container / Helm / IaC | Unknown | 8 | 250 | passed | 15.0s |
| nextcloud/text | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| nextcloud/documentation | JavaScript/TypeScript | Python | Unknown | 19 | 0 | passed | 15.0s |
| discourse/logster | Ruby | Ruby | Unknown | 1 | 55 | passed | 15.0s |
| getsentry/spotlight | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 108 | passed | 15.0s |
| n8n-io/skills | Container / Helm / IaC | JavaScript/TypeScript | Unknown | 1 | 1 | passed | 15.0s |
| getsentry/symbolic | Rust | Rust | Unknown | 6 | 131 | passed | 15.0s |
| discourse/wp-discourse | PHP | PHP | Unknown | 4 | 95 | passed | 15.0s |
| langfuse/langfuse-python | Python | Python | Unknown | 9 | 32 | passed | 15.0s |
| bitwarden/sdk-sm | Rust | Rust | Unknown | 46 | 80 | passed | 15.0s |
| TryGhost/Starter | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 1 | passed | 15.0s |
| grafana/grafana-kiosk | Go | Go | Unknown | 5 | 38 | passed | 15.0s |
| nextcloud/richdocuments | JavaScript/TypeScript | PHP | Unknown | 22 | 179 | passed | 15.0s |
| TryGhost/express-hbs | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 20 | passed | 15.0s |
| directus/rstore | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 34 | passed | 15.0s |
| getsentry/symbolicator | Rust | Rust | Unknown | 10 | 154 | passed | 15.0s |
| twentyhq/favicon | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 8 | passed | 15.0s |
| supabase/dbdev | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 10 | 26 | passed | 15.0s |
| getsentry/warden | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 8 | 61 | passed | 15.0s |
| getsentry/junior | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| home-assistant/home-assistant-js-websocket | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 1 | passed | 15.0s |
| getsentry/snuba | Python | Python | Unknown | 15 | 180 | passed | 15.0s |
| zulip/python-zulip-api | Python | Python | Unknown | 2 | 10 | passed | 15.0s |
| backstage/mkdocs-monorepo-plugin | Python | Python | Unknown | 2 | 0 | passed | 15.0s |
| grafana/alloy-scenarios | Python | Python | Unknown | 3 | 10 | passed | 15.0s |
| TryGhost/action-deploy-theme | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 1 | passed | 15.0s |
| supabase/supabase-grafana | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 5 | passed | 15.0s |
| nextcloud/forms | JavaScript/TypeScript | PHP | Unknown | 22 | 151 | passed | 15.0s |
| supabase/pg_net | Python | Python | Unknown | 1 | 0 | passed | 15.0s |
| nextcloud/groupfolders | PHP | PHP | Unknown | 24 | 243 | passed | 15.0s |
| apache/cayenne | Java | Java | Unknown | 4 | 25 | passed | 15.0s |
| backstage/community | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 1 | passed | 15.0s |
| langfuse/skills | Python | JavaScript/TypeScript | Unknown | 2 | 1 | passed | 15.0s |
| argoproj/notifications-engine | Go | Go | Unknown | 1 | 84 | passed | 15.0s |
| nextcloud/twofactor_totp | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 18 | 1 | passed | 15.0s |
| bitwarden/directory-connector | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 11 | 72 | passed | 15.0s |
| home-assistant/docker | Container / Helm / IaC | Python | Unknown | 4 | 0 | passed | 15.0s |
| bitwarden/mcp-server | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 7 | 1 | passed | 15.0s |
| argoproj/argoproj-deployments | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 93 | passed | 15.0s |
| medusajs/examples | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 72 | passed | 15.0s |
| langfuse/langfuse-k8s | Container / Helm / IaC | Container / Helm / IaC | Unknown | 5 | 67 | passed | 15.0s |
| mastodon/joinmastodon | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 5 | 27 | passed | 15.0s |
| home-assistant/cli | Go | Go | Unknown | 5 | 192 | passed | 15.0s |
| keycloak/keycloak-community | JavaScript/TypeScript | Ruby | Unknown | 0 | 0 | passed | 15.0s |
| grafana/grafana-foundation-sdk | PHP | Java | Unknown | 8 | 17 | passed | 15.0s |
| medusajs/medusa-eats | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 61 | passed | 15.0s |
| grafana/ai-sdk | Go | Go | Unknown | 8 | 255 | passed | 15.0s |
| mattermost/mattermost-plugin-agents | Go | Go | Unknown | 10 | 437 | passed | 15.0s |
| argoproj/argo-ui | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 6 | 102 | passed | 15.0s |
| argoproj/rollouts-demo | Go | Go | Unknown | 0 | 43 | passed | 15.0s |
| medusajs/docker-medusa | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 3 | passed | 15.0s |
| grafana/grafana-ansible-collection | Python | Python | Unknown | 10 | 0 | passed | 15.0s |
| TryGhost/ActivityPub | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 8 | 66 | passed | 15.0s |
| medusajs/medusa-agent-skills | JavaScript/TypeScript | Unknown | Unknown | 2 | 0 | passed | 15.0s |
| bitwarden/agent-access | Rust | Rust | Unknown | 4 | 76 | passed | 15.0s |
| medusajs/medusa-starter-default | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 3 | passed | 15.0s |
| PostHog/wizard | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 9 | 356 | passed | 15.0s |
| mattermost/mattermost-helm | Container / Helm / IaC | Container / Helm / IaC | Unknown | 2 | 125 | passed | 15.0s |
| nextcloud/files_mindmap | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 7 | 1 | passed | 15.0s |
| mastodon/chart | Container / Helm / IaC | Container / Helm / IaC | Unknown | 1 | 35 | passed | 15.0s |
| bitwarden/passkeys-index | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 2 | passed | 15.0s |
| backstage/demo | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 5 | 15 | passed | 15.0s |
| nextcloud/user_oidc | PHP | PHP | Unknown | 16 | 111 | passed | 15.0s |
| apache/camel-spring-boot | Java | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| PostHog/duckgres | Go | Go | Unknown | 13 | 322 | passed | 15.0s |
| backstage/software-templates | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 6 | passed | 15.0s |
| mattermost/mattermost-plugin-github | Go | JavaScript/TypeScript | Unknown | 5 | 12 | passed | 15.0s |
| keycloak/keycloak-benchmark | Java | Java | Unknown | 30 | 73 | passed | 15.0s |
| langfuse/langfuse-js | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 7 | 154 | passed | 15.0s |
| apache/airflow-site | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 1 | passed | 15.0s |
| mastodon/mastodon-api | Ruby | Ruby | Unknown | 1 | 74 | passed | 15.0s |
| langfuse/mcp-server-langfuse | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 1 | passed | 15.0s |
| triggerdotdev/apihero | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 232 | passed | 15.0s |
| calcom/sans-ui | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 1 | passed | 15.0s |
| appwrite/templates | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 18 | passed | 15.0s |
| RocketChat/EmbeddedChat | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 6 | 129 | passed | 15.0s |
| goharbor/harbor-cli | Go | Go | Unknown | 2 | 254 | passed | 15.0s |
| medusajs/dtc-starter | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 48 | passed | 15.0s |
| bitwarden/ai-plugins | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 7 | 6 | passed | 15.0s |
| saleor/apps | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| chatwoot/ai-agents | Ruby | Ruby | Unknown | 2 | 79 | passed | 15.0s |
| mattermost/mattermost-plugin-gitlab | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 12 | passed | 15.0s |
| mattermost/mattermost-plugin-starter-template | Go | Go | Unknown | 3 | 17 | passed | 15.0s |
| nextcloud/notifications | JavaScript/TypeScript | PHP | Unknown | 26 | 77 | passed | 15.0s |
| langfuse/oss-llmops-stack | Container / Helm / IaC | JavaScript/TypeScript | Unknown | 0 | 4 | passed | 15.0s |
| goharbor/terraform-provider-harbor | Go | Go | Unknown | 4 | 99 | passed | 15.0s |
| mattermost/mattermost-plugin-calls | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 5 | 311 | passed | 15.0s |
| bitwarden/passwordless-server | .NET | .NET | Unknown | 8 | 83 | passed | 15.0s |
| nextcloud/activity | JavaScript/TypeScript | PHP | Unknown | 29 | 124 | passed | 15.0s |
| RocketChat/Rocket.Chat.js.SDK | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 4 | passed | 15.0s |
| mattermost/mattermost-plugin-boards | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 6 | 95 | passed | 15.0s |
| TryGhost/SDK | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 16 | passed | 15.0s |
| n8n-io/n8n-docker-caddy | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 1 | passed | 15.0s |
| home-assistant/companion.home-assistant | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 1 | passed | 15.0s |
| nextcloud/serverinfo | JavaScript/TypeScript | PHP | Unknown | 22 | 167 | passed | 15.0s |
| harness/harness-skills | Python | Python | Unknown | 1 | 0 | passed | 15.0s |
| grafana/agento11y | Go | Go | Unknown | 13 | 281 | passed | 15.0s |
| TryGhost/Source | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 1 | passed | 15.0s |
| triggerdotdev/examples | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 56 | passed | 15.0s |
| plausible/ecto_ch | Elixir | Elixir | Unknown | 1 | 54 | passed | 15.0s |
| nextcloud/viewer | Container / Helm / IaC | Unknown | Unknown | 4 | 0 | passed | 15.0s |
| nextcloud/twofactor_gateway | PHP | PHP | Unknown | 19 | 237 | passed | 15.0s |
| owncloud/richdocuments | JavaScript/TypeScript | PHP | Unknown | 6 | 47 | passed | 15.0s |
| saleor/macaw-ui | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| bitwarden/sdk-internal | Rust | Rust | Unknown | 25 | 257 | passed | 15.0s |
| discourse/rails_failover | Ruby | Ruby | Unknown | 1 | 51 | passed | 15.0s |
| backstage/mkdocs-techdocs-core | Python | Python | Unknown | 6 | 0 | passed | 15.0s |
| mastodon/fediverse_auxiliary_service_provider_specifications | Container / Helm / IaC | Unknown | Unknown | 0 | 0 | passed | 15.0s |
| harness/mcp-server | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 25 | passed | 15.0s |
| mattermost/mattermost-plugin-zoom | Go | JavaScript/TypeScript | Unknown | 4 | 6 | passed | 15.0s |
| mattermost/mattermost-plugin-jira | Go | JavaScript/TypeScript | Unknown | 3 | 11 | passed | 15.0s |
| nextcloud/files_pdfviewer | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| nextcloud/user_saml | PHP | PHP | Unknown | 15 | 93 | passed | 15.0s |
| grafana/cog | Go | Go | Unknown | 4 | 250 | passed | 15.0s |
| appwrite/sdk-for-cli | Go | Go | Unknown | 1 | 252 | passed | 15.0s |
| keycloak/keycloak-oauth-sig | Container / Helm / IaC | Go | Unknown | 1 | 8 | passed | 15.0s |
| nextcloud/unsplash | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 1 | passed | 15.0s |
| mattermost/mattermost-plugin-playbooks | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 274 | passed | 15.0s |
| PostHog/ai-plugin | Python | Python | Unknown | 2 | 1 | passed | 15.0s |
| goharbor/acceleration-service | Go | Go | Unknown | 6 | 49 | passed | 15.0s |
| keycloak/keycloak-js | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 3 | passed | 15.0s |
| bitwarden/sm-action | Rust | Rust | Unknown | 3 | 3 | passed | 15.0s |
| TryGhost/knex-migrator | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 1 | passed | 15.0s |
| grafana/tempo-operator | Go | Go | Unknown | 13 | 300 | passed | 15.0s |
| zulip/zulip-archive | Python | Python | Unknown | 2 | 0 | passed | 15.0s |
| appwrite/sdk-for-go | Go | Go | Unknown | 1 | 250 | passed | 15.0s |
| mattermost/mattermost-plugin-demo | Go | JavaScript/TypeScript | Unknown | 2 | 156 | passed | 15.0s |
| zulip/zulipbot | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 2 | passed | 15.0s |
| PostHog/posthog-android | Java | Java | Unknown | 10 | 3 | passed | 15.0s |
| home-assistant/builder | Container / Helm / IaC | Container / Helm / IaC | Unknown | 3 | 1 | passed | 15.0s |
| triggerdotdev/docker | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 3 | passed | 15.0s |
| zulip/zulip-js | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 1 | passed | 15.0s |
| saleor/saleor-app-template | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 12 | passed | 15.0s |
| discourse/discourse-activity-pub | Ruby | Ruby | Unknown | 2 | 250 | passed | 15.0s |
| directus/mcp | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 1 | passed | 15.0s |
| immich-app/base-images | Container / Helm / IaC | Container / Helm / IaC | Unknown | 6 | 2 | passed | 15.0s |
| plausible/ch | Elixir | Elixir | Unknown | 1 | 38 | passed | 15.0s |
| TryGhost/gscan | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 50 | passed | 15.0s |
| TryGhost/Edition | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 1 | passed | 15.0s |
| goharbor/community | Container / Helm / IaC | Unknown | Unknown | 1 | 0 | passed | 15.0s |
| grafana/grafana-csv-datasource | JavaScript/TypeScript | Go | Unknown | 5 | 11 | passed | 15.0s |
| plausible/wordpress | PHP | PHP | Unknown | 3 | 227 | passed | 15.0s |
| medusajs/gatsby-starter-medusa | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 5 | passed | 15.0s |
| chatwoot/chatwoot-react-native-widget | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 2 | passed | 15.0s |
| discourse/discourse-mcp | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 2 | passed | 15.0s |
| PostHog/skills | Python | Python | Unknown | 2 | 1 | passed | 15.0s |
| home-assistant/version | Container / Helm / IaC | Unknown | Unknown | 1 | 0 | passed | 15.0s |
| keycloak/keycloak-client | Java | Java | Unknown | 7 | 15 | passed | 15.0s |
| directus/vue-split-panel | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 1 | passed | 15.0s |
| langfuse/langfuse-java | Java | Java | Unknown | 3 | 1 | passed | 15.0s |
| PostHog/context-mill | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 9 | 228 | passed | 15.0s |
| appwrite/mcp | Python | Python | Unknown | 5 | 17 | passed | 15.0s |
| appwrite/playground-for-python | Python | Python | Unknown | 0 | 0 | passed | 15.0s |
| appwrite/playground-for-android | Java | Java | Unknown | 1 | 0 | passed | 15.0s |
| medusajs/medusa-express-nextjs | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 4 | passed | 15.0s |
| grafana/grafana-plugin-sdk-rust | Rust | Rust | Unknown | 3 | 33 | passed | 15.0s |
| TryGhost/migrate | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 40 | passed | 15.0s |
| n8n-io/n8n-heroku | Container / Helm / IaC | Container / Helm / IaC | Unknown | 0 | 1 | passed | 15.0s |
| grafana/traces-drilldown | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 13 | 54 | passed | 15.0s |
| saleor/cli | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 5 | 2 | passed | 15.0s |
| langfuse/langfuse-cli | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 4 | 1 | passed | 15.0s |
| mattermost/mattermost-load-test-ng | Go | Go | Unknown | 1 | 218 | passed | 15.0s |
| bitwarden/passwordless-client-js | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 6 | passed | 15.0s |
| PostHog/posthog-elixir | Elixir | Elixir | Unknown | 8 | 92 | passed | 15.0s |
| grafana/unused | Go | Go | Unknown | 2 | 50 | passed | 15.0s |
| RocketChat/rocketchat-compose | Container / Helm / IaC | Container / Helm / IaC | Unknown | 1 | 28 | passed | 15.0s |
| langfuse/langfuse-terraform-aws | Container / Helm / IaC | Container / Helm / IaC | Unknown | 3 | 24 | passed | 15.0s |
| langfuse/langfuse-workshop | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 5 | passed | 15.0s |
| bitwarden/helm-charts | Container / Helm / IaC | Container / Helm / IaC | Unknown | 13 | 65 | passed | 15.0s |
| PostHog/posthog-rs | Rust | Rust | Unknown | 9 | 146 | passed | 15.0s |
| home-assistant/contributors.home-assistant.io | JavaScript/TypeScript | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| mattermost/mattermost-plugin-wrangler | Go | JavaScript/TypeScript | Unknown | 3 | 3 | passed | 15.0s |
| plausible/website | JavaScript/TypeScript | Ruby | Unknown | 1 | 1 | passed | 15.0s |
| keycloak/keycloak-k8s-resources | Container / Helm / IaC | Unknown | Unknown | 0 | 0 | passed | 15.0s |
| umami-software/zen | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 0 | 293 | passed | 15.0s |
| medusajs/b2b-starter | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 151 | passed | 15.0s |
| woodpecker-ci/autoscaler | Go | Go | Unknown | 0 | 92 | passed | 15.0s |
| metabase/agent-skills | Container / Helm / IaC | Unknown | Unknown | 0 | 0 | passed | 15.0s |
| n8n-io/task-runner-launcher | Go | Go | Unknown | 3 | 30 | passed | 15.0s |
| bitwarden/f-droid | Go | Unknown | Unknown | 0 | 0 | timeout | 60.0s |
| PostHog/posthog-go | Go | Go | Unknown | 11 | 208 | passed | 15.0s |
| mattermost/mattermost-plugin-google-calendar | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 13 | passed | 15.0s |
| saleor/app-sdk | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 7 | passed | 15.0s |
| triggerdotdev/schema-infer | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 1 | passed | 15.0s |
| bitwarden/passwordless-dotnet | .NET | .NET | Unknown | 1 | 17 | passed | 15.0s |
| TryGhost/gctools | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 1 | 1 | passed | 15.0s |
| bitwarden/key-connector | .NET | .NET | Unknown | 6 | 31 | passed | 15.0s |
| goharbor/go-client | Go | Go | Unknown | 2 | 250 | passed | 15.0s |
| PostHog/hoglake | Java | Java | Unknown | 16 | 57 | passed | 15.0s |
| grafana/alloy-modules | Container / Helm / IaC | JavaScript/TypeScript | Unknown | 6 | 1 | passed | 15.0s |
| home-assistant/services.home-assistant.io | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 3 | 1 | passed | 15.0s |
| TryGhost/nodecmsguide | JavaScript/TypeScript | JavaScript/TypeScript | Unknown | 2 | 4 | passed | 15.0s |
