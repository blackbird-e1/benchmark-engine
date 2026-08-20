"""Aviation adapter for benchmark-engine.

This adapter is intentionally thin: domain-specific data preparation belongs here,
while benchmark methodology remains inside benchmark_engine.core.
"""
"""Aviation benchmark profile for benchmark-engine.

This module contains aviation-specific benchmark rules.
Benchmark methodology remains inside benchmark_engine.core.
"""

from typing import Dict

from ..core.models import MetricRule, RuleType


AVIATION_RULES: Dict[str, MetricRule] = {
    "max_speed_knots": MetricRule(
        name="max_speed_knots",
        rule_type=RuleType.MAXIMUM,
        maximum=250,
        tolerance=25,
        weight=1.0,
    ),
    "max_bank_angle_deg": MetricRule(
        name="max_bank_angle_deg",
        rule_type=RuleType.MAXIMUM,
        maximum=30,
        tolerance=10,
        weight=1.0,
    ),
    "max_descent_rate_fpm": MetricRule(
        name="max_descent_rate_fpm",
        rule_type=RuleType.MAXIMUM,
        maximum=1500,
        tolerance=500,
        weight=1.0,
    ),
    "avg_throttle_percent": MetricRule(
        name="avg_throttle_percent",
        rule_type=RuleType.RANGE,
        minimum=20,
        maximum=80,
        tolerance=20,
        weight=1.0,
    ),
}