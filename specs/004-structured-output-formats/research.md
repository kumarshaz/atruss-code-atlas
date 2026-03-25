# Phase 0: Outline & Research

## Needs Clarification Resolutions

**Unknown**: Best practices for serializing nested Pipeline DAGs to CSV.
- **Decision**: For CSV pipeline visualization output, we will flatten the DAG into an Edge List format `(source_node, target_node, dependency_type)` alongside a Node List `(node_id, job_name, status)`. If a single CSV is forced, we default to the Node List.
- **Rationale**: CSV cannot natively represent deeply nested trees/DAGs. An adjacency or edge list is the standard structural representation of graphs in flat files.
- **Alternatives considered**: JSON-encoding the nested dependencies within a single CSV column (rejected as it defeats the purpose of choosing CSV for plain structural readability).

**Unknown**: YAML and JSON Generation Libraries.
- **Decision**: Utilize standard library `json` for JSON generation. Utilize `pyyaml` (already present in `requirements.txt`) for YAML export.
- **Rationale**: Keeps dependencies minimal while ensuring robust and deterministic serialization. `pyyaml`'s `SafeDumper` ensures no arbitrary object execution vulnerabilities.
- **Alternatives considered**: Relying strictly on Pydantic's internal serializers. We will use Pydantic `model_dump()` combined with standard json/yaml to ensure separation of concerns.

**Unknown**: Validation Strategy.
- **Decision**: Unit and integration tests will strictly validate the JSON and YAML structures against expected structural schemas. No strict schema validation will occur at runtime to maintain the < 3 minutes execution constraint.
- **Rationale**: Aligns with the user's clarification to "Validate only in CI/testing, not at runtime."
- **Alternatives considered**: Runtime JSONSchema validation using `jsonschema` (rejected due to user preference for performance).
