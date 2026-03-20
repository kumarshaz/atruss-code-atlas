

def generate_arc42_markdown(repo_name: str, components: list[dict]) -> str:
    """Generates an Arc42 compliant markdown string with Mermaid diagrams."""

    md = f"# Architecture: {repo_name}\n\n"
    md += "## Context\nAuto-generated architectural bounds extracted from AST.\n\n"
    md += "## Building Block View\n\n"

    md += "```mermaid\n"
    md += "graph TD;\n"

    if not components:
        md += "    Empty[No Architecture Components Detected]\n"

    edges = []
    nodes = []
    for c in components:
        node_name = c["name"]
        nodes.append(f"    {node_name}[{node_name} : {c.get('type')}]")
        for dep in c.get("dependencies", []):
            edges.append(f"    {node_name} --> {dep}")

    md += "\n".join(nodes) + "\n"
    if edges:
        md += "\n".join(set(edges)) + "\n"

    md += "```\n\n"
    md += "## Component Details\n"

    for c in components:
        md += f"- **{c['name']}** (`{c.get('file', 'unknown')}`): {c.get('type')}\n"

    return md
