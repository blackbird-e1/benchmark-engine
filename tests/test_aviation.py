from benchmark_engine import BenchmarkEngine, BenchmarkInput
from benchmark_engine.adapters import AVIATION_RULES


def test_aviation_profile_contains_expected_metrics():
    assert set(AVIATION_RULES.keys()) == {
        "max_speed_knots",
        "max_bank_angle_deg",
        "max_descent_rate_fpm",
        "avg_throttle_percent",
    }


def test_aviation_profile_with_good_values():
    engine = BenchmarkEngine(AVIATION_RULES)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "max_speed_knots": 220,
                "max_bank_angle_deg": 25,
                "max_descent_rate_fpm": 1200,
                "avg_throttle_percent": 50,
            }
        )
    )

    assert result.score == 1.0


def test_aviation_profile_detects_high_bank_angle():
    engine = BenchmarkEngine(AVIATION_RULES)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "max_bank_angle_deg": 35,
            }
        )
    )

    metric = result.metrics["max_bank_angle_deg"]

    assert metric.score == 0.5
    assert metric.status == "ABOVE_LIMIT"
    assert metric.deviation == 5


def test_aviation_profile_detects_high_speed():
    engine = BenchmarkEngine(AVIATION_RULES)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "max_speed_knots": 275,
            }
        )
    )

    metric = result.metrics["max_speed_knots"]

    assert metric.score == 0.0
    assert metric.status == "ABOVE_LIMIT"
    assert metric.deviation == 25


def test_aviation_profile_detects_throttle_outside_range():
    engine = BenchmarkEngine(AVIATION_RULES)

    result = engine.evaluate(
        BenchmarkInput(
            metrics={
                "avg_throttle_percent": 90,
            }
        )
    )

    metric = result.metrics["avg_throttle_percent"]

    assert metric.score == 0.5
    assert metric.status == "ABOVE_RANGE"
    assert metric.deviation == 10