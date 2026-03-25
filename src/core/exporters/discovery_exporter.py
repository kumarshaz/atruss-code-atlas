import json
import csv
import yaml
from pathlib import Path
from src.core.utils.export_manager import ExportManager
from src.models.discovery import DiscoveryManifestItem

class DiscoveryArchiver:
    def __init__(self, manager: ExportManager):
        self.manager = manager

    def export(self, items: list[DiscoveryManifestItem]) -> None:
        """
        Exports the strict dynamic payloads to CSV, JSON, and YAML formats natively 
        inside the `exports/{timestamp}/repos/` directory.
        """
        dicts = [item.to_dict() for item in items]
        
        # 1. JSON
        json_path = self.manager.get_path("repos", "repositories.json")
        envelope = {
            "count": len(dicts),
            "items": dicts
        }
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(envelope, jf, indent=2)

        # 2. YAML
        yaml_path = self.manager.get_path("repos", "repositories.yaml")
        with open(yaml_path, "w", encoding="utf-8") as yf:
            yaml.dump(envelope, yf, default_flow_style=False, sort_keys=False)

        # 3. CSV
        csv_path = self.manager.get_path("repos", "repositories.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as cf:
            if not dicts:
                # Default mock headers if completely empty
                fields = list(DiscoveryManifestItem.__annotations__.keys())
            else:
                fields = list(dicts[0].keys())

            writer = csv.DictWriter(cf, fieldnames=fields)
            writer.writeheader()
            for d in dicts:
                writer.writerow(d)
