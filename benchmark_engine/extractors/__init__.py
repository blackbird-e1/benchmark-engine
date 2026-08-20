"""Data extraction interfaces for benchmark-engine."""

from .aviation import AviationExtractor
from .base import BaseExtractor

__all__ = [
    "AviationExtractor",
    "BaseExtractor",
]