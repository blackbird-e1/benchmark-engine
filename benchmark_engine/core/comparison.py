"""Core comparison logic for benchmark-engine."""
from typing import Dict

from .models import BenchmarkInput, MetricRule, MetricResult


def compare_metrics(
    benchmark_input: BenchmarkInput,
    rules: Dict[str, MetricRule],
) -> Dict[str, MetricResult]:
    results = {}

    for name, value in benchmark_input.metrics.items():
        if name not in rules:
            continue

        rule = rules[name]

        if rule.maximum == rule.minimum:
            score = 1.0
        else:
            score = (value - rule.minimum) / (
                rule.maximum - rule.minimum
            )

        score = max(0.0, min(1.0, score))

        results[name] = MetricResult(
            name=name,
            value=value,
            score=score,
            weight=rule.weight,
        )

    return results