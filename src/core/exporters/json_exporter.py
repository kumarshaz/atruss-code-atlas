import json
from typing import Any, List
from .base_exporter import BaseExporter

class JSONExporter(BaseExporter):
    def export_discovery(self, manifest: List[Any], output_path: str) -> None:
        data = [item.model_dump() for item in manifest]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def export_pipeline(self, dag: Any, output_path: str) -> None:
        data = dag.model_dump()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
