# Research: Atruss Astro Dashboard & CLI Renaming

## Topic 1: CLI Renaming Strategy
- **Decision:** Rename the entry point in `pyproject.toml` from `repo-analyzer` to `atruss`. Update all command decorator instances and help strings in `src/cli/main.py`.
- **Rationale:** Standard, deterministic way to change a Typer/setuptools CLI name. Requires users to re-run `pip install -e .` for the new entry point to be registered.
- **Alternatives considered:** Keeping an alias. Rejected because it violates the brand realignment goal of having zero instances of `repo-analyzer`.

## Topic 2: Astro Starlight Data Ingestion for JSON/YAML
- **Decision:** Use standard ESM imports for static JSON/YAML files (e.g., `import discoveryData from '../../exports/latest/discovery.json'`) within Astro components, or configure Astro Content Collections with `type: 'data'`.
- **Rationale:** Astro natively supports importing JSON, which allows us to build the Summary Dashboard (`AtlasSummary.astro`) seamlessly. Setting up a data collection is the most robust approach if the data schemas are strict.
- **Alternatives considered:** Fetching data client-side. Rejected because this is a static Docs-as-Code visualization; all data should be resolved at build time to adhere to the offline-capable principle in the Constitution.

## Topic 3: Linking Summary to Detailed Markdowns
- **Decision:** Place the generated markdown reports into `web/src/content/docs/reports/` (or configure the `srcDir` / symlinks). The summary dashboard will generate hyperlinked cards pointing to `/reports/[repo-name]/`.
- **Rationale:** Starlight automatically generates routes based on the file hierarchy in `src/content/docs/`. This requires zero custom routing logic.
- **Alternatives considered:** Building a custom Astro routing layer (`[slug].astro`). Rejected because Starlight already handles Markdown parsing, TOC generation, and sidebar navigation perfectly. We should leverage the framework, not fight it.
