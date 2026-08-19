"""Core scoring logic for benchmark-engine."""
from typing import Dict

from .models import MetricResult


def calculate_score(
    metric_results: Dict[str, MetricResult],
) -> float:
    if not metric_results:
        return 0.0

    total_weight = sum(
        result.weight for result in metric_results.values()
    )

    if total_weight == 0:
        return 0.0

    weighted_score = sum(
        result.score * result.weight
        for result in metric_results.values()
    )

    return weighted_score / total_weight