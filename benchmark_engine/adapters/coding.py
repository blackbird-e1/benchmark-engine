"""Coding benchmark profile for benchmark-engine.

This profile defines simple, deterministic benchmarks for
a small Python calculator implementation.
"""

from typing import Dict

from ..core.models import MetricRule, RuleType


CODING_RULES: Dict[str, MetricRule] = {
    "function_count": MetricRule(
        name="function_count",
        rule_type=RuleType.MINIMUM,
        minimum=4,
        tolerance=1,
        weight=1.0,
    ),
    "operation_count": MetricRule(
        name="operation_count",
        rule_type=RuleType.MINIMUM,
        minimum=4,
        tolerance=1,
        weight=1.0,
    ),
    "has_division": MetricRule(
        name="has_division",
        rule_type=RuleType.TARGET,
        target=1,
        tolerance=0,
        weight=1.0,
    ),
    "has_error_handling": MetricRule(
        name="has_error_handling",
        rule_type=RuleType.TARGET,
        target=1,
        tolerance=0,
        weight=1.0,
    ),
    "line_count": MetricRule(
        name="line_count",
        rule_type=RuleType.MAXIMUM,
        maximum=40,
        tolerance=10,
        weight=1.0,
    ),
}