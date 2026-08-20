"""Core comparison logic for benchmark-engine."""

from typing import Dict

from .models import BenchmarkInput, MetricRule, MetricResult, RuleType


def compare_metrics(
    benchmark_input: BenchmarkInput,
    rules: Dict[str, MetricRule],
) -> Dict[str, MetricResult]:
    results = {}

    for name, value in benchmark_input.metrics.items():
        if name not in rules:
            continue

        rule = rules[name]

        score, status, deviation, benchmark = _evaluate_rule(
            value,
            rule,
        )

        results[name] = MetricResult(
            name=name,
            value=value,
            score=score,
            weight=rule.weight,
            status=status,
            benchmark=benchmark,
            deviation=deviation,
        )

    return results


def _evaluate_rule(
    value: float,
    rule: MetricRule,
) -> tuple[float, str, float | None, str]:
    """Evaluate one metric against its benchmark rule."""

    if rule.rule_type == RuleType.MAXIMUM:
        score, status, deviation, benchmark = _evaluate_maximum(
            value,
            rule,
        )

    elif rule.rule_type == RuleType.MINIMUM:
        score, status, deviation, benchmark = _evaluate_minimum(
            value,
            rule,
        )

    elif rule.rule_type == RuleType.RANGE:
        score, status, deviation, benchmark = _evaluate_range(
            value,
            rule,
        )

    elif rule.rule_type == RuleType.TARGET:
        score, status, deviation, benchmark = _evaluate_target(
            value,
            rule,
        )

    else:
        raise ValueError(
            f"Unsupported rule type: {rule.rule_type}"
        )

    score = max(0.0, min(1.0, score))

    return score, status, deviation, benchmark


def _evaluate_maximum(
    value: float,
    rule: MetricRule,
) -> tuple[float, str, float, str]:
    if rule.maximum is None:
        raise ValueError(
            f"MAXIMUM rule '{rule.name}' requires maximum."
        )

    deviation = value - rule.maximum
    benchmark = f"<= {rule.maximum}"

    if value <= rule.maximum:
        return 1.0, "WITHIN_LIMIT", deviation, benchmark

    if rule.tolerance is None or rule.tolerance <= 0:
        return 0.0, "ABOVE_LIMIT", deviation, benchmark

    score = 1.0 - (deviation / rule.tolerance)

    return score, "ABOVE_LIMIT", deviation, benchmark


def _evaluate_minimum(
    value: float,
    rule: MetricRule,
) -> tuple[float, str, float, str]:
    if rule.minimum is None:
        raise ValueError(
            f"MINIMUM rule '{rule.name}' requires minimum."
        )

    deviation = value - rule.minimum
    benchmark = f">= {rule.minimum}"

    if value >= rule.minimum:
        return 1.0, "WITHIN_LIMIT", deviation, benchmark

    if rule.tolerance is None or rule.tolerance <= 0:
        return 0.0, "BELOW_LIMIT", deviation, benchmark

    score = 1.0 - (abs(deviation) / rule.tolerance)

    return score, "BELOW_LIMIT", deviation, benchmark


def _evaluate_range(
    value: float,
    rule: MetricRule,
) -> tuple[float, str, float, str]:
    if rule.minimum is None or rule.maximum is None:
        raise ValueError(
            f"RANGE rule '{rule.name}' requires minimum and maximum."
        )

    if rule.minimum > rule.maximum:
        raise ValueError(
            f"RANGE rule '{rule.name}' has minimum greater than maximum."
        )

    benchmark = f"{rule.minimum} - {rule.maximum}"

    if rule.minimum <= value <= rule.maximum:
        return 1.0, "WITHIN_RANGE", 0.0, benchmark

    if value < rule.minimum:
        deviation = value - rule.minimum
        distance = abs(deviation)
        status = "BELOW_RANGE"
    else:
        deviation = value - rule.maximum
        distance = abs(deviation)
        status = "ABOVE_RANGE"

    if rule.tolerance is None or rule.tolerance <= 0:
        return 0.0, status, deviation, benchmark

    score = 1.0 - (distance / rule.tolerance)

    return score, status, deviation, benchmark


def _evaluate_target(
    value: float,
    rule: MetricRule,
) -> tuple[float, str, float, str]:
    if rule.target is None:
        raise ValueError(
            f"TARGET rule '{rule.name}' requires target."
        )

    deviation = value - rule.target
    benchmark = f"target = {rule.target}"

    if value == rule.target:
        return 1.0, "ON_TARGET", deviation, benchmark

    if rule.tolerance is None or rule.tolerance <= 0:
        return 0.0, "OFF_TARGET", deviation, benchmark

    score = 1.0 - (
        abs(deviation) / rule.tolerance
    )

    return score, "OFF_TARGET", deviation, benchmark