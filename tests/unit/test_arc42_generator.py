from src.core.services.report_generator import generate_arc42_markdown


def test_arc42_generation():
    components = [
        {"name": "api_gateway", "type": "API_ROUTE", "dependencies": ["database"]},
        {"name": "database", "type": "DATA_ACCESS_LAYER", "dependencies": []}
    ]
    markdown = generate_arc42_markdown("TestRepo", components)

    assert "# Architecture: TestRepo" in markdown
    assert "## Building Block View" in markdown
    assert "```mermaid" in markdown
    assert "graph TD;" in markdown
    assert "api_gateway --> database" in markdown
