"""Base interfaces for benchmark data extractors."""

from abc import ABC, abstractmethod
from typing import Any

from benchmark_engine.core.models import BenchmarkInput


class BaseExtractor(ABC):
    """Base interface for converting raw data into benchmark input."""

    @abstractmethod
    def extract(self, data: Any) -> BenchmarkInput:
        """Convert raw data into BenchmarkInput."""
        raise NotImplementedError