"""Data models for benchmark-engine."""
from dataclasses import dataclass
from typing import Dict


@dataclass
class MetricRule:
    name: str
    minimum: float
    maximum: float
    weight: float = 1.0


@dataclass
class BenchmarkInput:
    metrics: Dict[str, float]


@dataclass
class MetricResult:
    name: str
    value: float
    score: float
    weight: float


@dataclass
class BenchmarkResult:
    score: float
    metrics: Dict[str, MetricResult]