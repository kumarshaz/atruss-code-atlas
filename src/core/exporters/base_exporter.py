from abc import ABC, abstractmethod
from typing import Any


class BaseExporter(ABC):
    @abstractmethod
    def export_discovery(self, manifest: list[Any], output_path: str) -> None:
        pass

    @abstractmethod
    def export_pipeline(self, dag: Any, output_path: str) -> None:
        pass
