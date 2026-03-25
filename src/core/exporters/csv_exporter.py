import csv
from typing import Any, List
from .base_exporter import BaseExporter

class CSVExporter(BaseExporter):
    def export_discovery(self, manifest: List[Any], output_path: str) -> None:
        if not manifest:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write("")
            return
            
        keys = manifest[0].model_dump().keys()
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for item in manifest:
                writer.writerow(item.model_dump())

    def export_pipeline(self, dag: Any, output_path: str) -> None:
        if not dag.nodes:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                f.write("")
            return
            
        keys = dag.nodes[0].model_dump().keys()
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for node in dag.nodes:
                writer.writerow(node.model_dump())
