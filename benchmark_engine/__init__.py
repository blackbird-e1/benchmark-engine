"""Domain-agnostic benchmark engine."""

from typing import Dict

from .core.comparison import compare_metrics
from .core.models import (
    BenchmarkInput,
    BenchmarkResult,
    MetricRule,
    RuleType,
)
from .core.scoring import calculate_score


class BenchmarkEngine:
    def __init__(self, rules: Dict[str, MetricRule]):
        self.rules = rules

    def evaluate(
        self,
        benchmark_input: BenchmarkInput,
    ) -> BenchmarkResult:
        metric_results = compare_metrics(
            benchmark_input,
            self.rules,
        )

        score = calculate_score(metric_results)

        return BenchmarkResult(
            score=score,
            metrics=metric_results,
        )


__all__ = [
    "BenchmarkEngine",
    "BenchmarkInput",
    "BenchmarkResult",
    "MetricRule",
    "RuleType",
]