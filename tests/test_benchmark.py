from benchmark_engine import (
    BenchmarkEngine,
    BenchmarkInput,
    MetricRule,
    RuleType,
)
import pytest


def test_minimum_rule():
    rules = {
        "airspeed": MetricRule(
            name="airspeed",
            rule_type=RuleType.MINIMUM,
            minimum=120,
            tolerance=20,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "airspeed": 140,
            }
        )
    )

    assert result.metrics["airspeed"].score == 1.0
    assert result.metrics["airspeed"].status == "WITHIN_LIMIT"


def test_minimum_rule_below_limit():
    rules = {
        "airspeed": MetricRule(
            name="airspeed",
            rule_type=RuleType.MINIMUM,
            minimum=120,
            tolerance=20,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "airspeed": 110,
            }
        )
    )

    assert result.metrics["airspeed"].score == pytest.approx(0.5)
    assert result.metrics["airspeed"].status == "BELOW_LIMIT"
    assert result.metrics["airspeed"].deviation == -10


def test_minimum_rule_reaches_zero_at_tolerance():
    rules = {
        "airspeed": MetricRule(
            name="airspeed",
            rule_type=RuleType.MINIMUM,
            minimum=120,
            tolerance=20,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "airspeed": 100,
            }
        )
    )

    assert result.metrics["airspeed"].score == 0.0
    assert result.metrics["airspeed"].status == "BELOW_LIMIT"
    assert result.metrics["airspeed"].deviation == -20


def test_maximum_rule():
    rules = {
        "bank_angle": MetricRule(
            name="bank_angle",
            rule_type=RuleType.MAXIMUM,
            maximum=30,
            tolerance=10,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "bank_angle": 25,
            }
        )
    )

    assert result.metrics["bank_angle"].score == 1.0
    assert result.metrics["bank_angle"].status == "WITHIN_LIMIT"


def test_maximum_rule_above_limit():
    rules = {
        "bank_angle": MetricRule(
            name="bank_angle",
            rule_type=RuleType.MAXIMUM,
            maximum=30,
            tolerance=10,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "bank_angle": 35,
            }
        )
    )

    assert result.metrics["bank_angle"].score == pytest.approx(0.5)
    assert result.metrics["bank_angle"].status == "ABOVE_LIMIT"
    assert result.metrics["bank_angle"].deviation == 5


def test_maximum_rule_reaches_zero_at_tolerance():
    rules = {
        "bank_angle": MetricRule(
            name="bank_angle",
            rule_type=RuleType.MAXIMUM,
            maximum=30,
            tolerance=10,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "bank_angle": 40,
            }
        )
    )

    assert result.metrics["bank_angle"].score == 0.0
    assert result.metrics["bank_angle"].status == "ABOVE_LIMIT"
    assert result.metrics["bank_angle"].deviation == 10


def test_range_rule_inside_range():
    rules = {
        "altitude": MetricRule(
            name="altitude",
            rule_type=RuleType.RANGE,
            minimum=28000,
            maximum=32000,
            tolerance=2000,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "altitude": 30000,
            }
        )
    )

    assert result.metrics["altitude"].score == 1.0
    assert result.metrics["altitude"].status == "WITHIN_RANGE"


def test_range_rule_below_range():
    rules = {
        "altitude": MetricRule(
            name="altitude",
            rule_type=RuleType.RANGE,
            minimum=28000,
            maximum=32000,
            tolerance=2000,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "altitude": 27000,
            }
        )
    )

    assert result.metrics["altitude"].score == pytest.approx(0.5)
    assert result.metrics["altitude"].status == "BELOW_RANGE"
    assert result.metrics["altitude"].deviation == -1000


def test_range_rule_above_range():
    rules = {
        "altitude": MetricRule(
            name="altitude",
            rule_type=RuleType.RANGE,
            minimum=28000,
            maximum=32000,
            tolerance=2000,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "altitude": 33000,
            }
        )
    )

    assert result.metrics["altitude"].score == pytest.approx(0.5)
    assert result.metrics["altitude"].status == "ABOVE_RANGE"
    assert result.metrics["altitude"].deviation == 1000


def test_range_rule_reaches_zero_below_range():
    rules = {
        "altitude": MetricRule(
            name="altitude",
            rule_type=RuleType.RANGE,
            minimum=28000,
            maximum=32000,
            tolerance=2000,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "altitude": 26000,
            }
        )
    )

    assert result.metrics["altitude"].score == 0.0
    assert result.metrics["altitude"].status == "BELOW_RANGE"


def test_range_rule_reaches_zero_above_range():
    rules = {
        "altitude": MetricRule(
            name="altitude",
            rule_type=RuleType.RANGE,
            minimum=28000,
            maximum=32000,
            tolerance=2000,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "altitude": 34000,
            }
        )
    )

    assert result.metrics["altitude"].score == 0.0
    assert result.metrics["altitude"].status == "ABOVE_RANGE"


def test_target_rule():
    rules = {
        "descent_rate": MetricRule(
            name="descent_rate",
            rule_type=RuleType.TARGET,
            target=1000,
            tolerance=200,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "descent_rate": 1000,
            }
        )
    )

    assert result.metrics["descent_rate"].score == 1.0
    assert result.metrics["descent_rate"].status == "ON_TARGET"


def test_target_rule_missed():
    rules = {
        "descent_rate": MetricRule(
            name="descent_rate",
            rule_type=RuleType.TARGET,
            target=1000,
            tolerance=200,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "descent_rate": 1100,
            }
        )
    )

    assert result.metrics["descent_rate"].score == pytest.approx(0.5)
    assert result.metrics["descent_rate"].status == "OFF_TARGET"
    assert result.metrics["descent_rate"].deviation == 100


def test_target_rule_reaches_zero_at_tolerance():
    rules = {
        "descent_rate": MetricRule(
            name="descent_rate",
            rule_type=RuleType.TARGET,
            target=1000,
            tolerance=200,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "descent_rate": 1200,
            }
        )
    )

    assert result.metrics["descent_rate"].score == 0.0
    assert result.metrics["descent_rate"].status == "OFF_TARGET"
    assert result.metrics["descent_rate"].deviation == 200


def test_weighted_metrics():
    rules = {
        "bank_angle": MetricRule(
            name="bank_angle",
            rule_type=RuleType.MAXIMUM,
            maximum=30,
            tolerance=10,
            weight=2,
        ),
        "airspeed": MetricRule(
            name="airspeed",
            rule_type=RuleType.MINIMUM,
            minimum=120,
            tolerance=20,
            weight=1,
        ),
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "bank_angle": 35,
                "airspeed": 110,
            }
        )
    )

    assert result.score == pytest.approx(0.5)


def test_empty_input_returns_zero_score():
    rules = {
        "bank_angle": MetricRule(
            name="bank_angle",
            rule_type=RuleType.MAXIMUM,
            maximum=30,
            tolerance=10,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(metrics={})
    )

    assert result.score == 0.0


def test_result_contains_benchmark_information():
    rules = {
        "bank_angle": MetricRule(
            name="bank_angle",
            rule_type=RuleType.MAXIMUM,
            maximum=30,
            tolerance=10,
        )
    }

    engine = BenchmarkEngine(rules)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "bank_angle": 35,
            }
        )
    )

    metric = result.metrics["bank_angle"]

    assert metric.benchmark == "<= 30"
    assert metric.deviation == 5
    assert metric.status == "ABOVE_LIMIT"
    assert metric.score == pytest.approx(0.5)