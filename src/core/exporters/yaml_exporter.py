import yaml
from typing import Any, List
from .base_exporter import BaseExporter

class YAMLExporter(BaseExporter):
    def export_discovery(self, manifest: List[Any], output_path: str) -> None:
        data = [item.model_dump() for item in manifest]
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    def export_pipeline(self, dag: Any, output_path: str) -> None:
        data = dag.model_dump()
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False)
