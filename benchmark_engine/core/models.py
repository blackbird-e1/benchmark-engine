"""Data models for benchmark-engine."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class RuleType(str, Enum):
    """Defines how a metric should be benchmarked."""

    MAXIMUM = "maximum"
    MINIMUM = "minimum"
    RANGE = "range"
    TARGET = "target"


@dataclass
class MetricRule:
    """Defines the benchmark rule for a single metric."""

    name: str
    rule_type: RuleType

    minimum: Optional[float] = None
    maximum: Optional[float] = None
    target: Optional[float] = None
    tolerance: Optional[float] = None

    weight: float = 1.0


@dataclass
class BenchmarkInput:
    """Measured metric values supplied to the benchmark engine."""

    metrics: Dict[str, float]


@dataclass
class MetricResult:
    """Benchmark result for a single metric."""

    name: str
    value: float
    score: float
    weight: float

    status: str
    benchmark: str
    deviation: Optional[float] = None


@dataclass
class BenchmarkResult:
    """Overall benchmark result."""

    score: float
    metrics: Dict[str, MetricResult]