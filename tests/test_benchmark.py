from benchmark_engine import (
    BenchmarkEngine,
    BenchmarkInput,
    MetricRule,
)
import pytest

def test_basic_benchmark():
    rules = {
        "accuracy": MetricRule(
            name="accuracy",
            minimum=0,
            maximum=100,
            weight=1,
        ),
        "consistency": MetricRule(
            name="consistency",
            minimum=0,
            maximum=100,
            weight=1,
        ),
    }

    engine = BenchmarkEngine(rules)

    data = BenchmarkInput(
        metrics={
            "accuracy": 80,
            "consistency": 90,
        }
    )

    result = engine.evaluate(data)

    assert result.score == pytest.approx(0.85)


def test_metric_is_clamped():
    rules = {
        "accuracy": MetricRule(
            name="accuracy",
            minimum=0,
            maximum=100,
        )
    }

    engine = BenchmarkEngine(rules)

    data = BenchmarkInput(
        metrics={
            "accuracy": 120,
        }
    )

    result = engine.evaluate(data)

    assert result.metrics["accuracy"].score == 1.0

def test_weighted_metrics():
    rules = {
        "accuracy": MetricRule(
            name="accuracy",
            minimum=0,
            maximum=100,
            weight=2,
        ),
        "consistency": MetricRule(
            name="consistency",
            minimum=0,
            maximum=100,
            weight=1,
        ),
    }

    engine = BenchmarkEngine(rules)

    data = BenchmarkInput(
        metrics={
            "accuracy": 80,
            "consistency": 50,
        }
    )

    result = engine.evaluate(data)

    assert result.score == pytest.approx((0.8 * 2 + 0.5) / 3)

def test_metric_is_clamped_below_minimum():
    rules = {
        "accuracy": MetricRule(
            name="accuracy",
            minimum=0,
            maximum=100,
        )
    }

    engine = BenchmarkEngine(rules)

    data = BenchmarkInput(
        metrics={
            "accuracy": -20,
        }
    )

    result = engine.evaluate(data)

    assert result.metrics["accuracy"].score == 0.0

def test_result_contains_all_metrics():
    rules = {
        "accuracy": MetricRule(
            name="accuracy",
            minimum=0,
            maximum=100,
        ),
        "consistency": MetricRule(
            name="consistency",
            minimum=0,
            maximum=100,
        ),
    }

    engine = BenchmarkEngine(rules)

    data = BenchmarkInput(
        metrics={
            "accuracy": 80,
            "consistency": 90,
        }
    )

    result = engine.evaluate(data)

    assert set(result.metrics.keys()) == {
        "accuracy",
        "consistency",
    }

def test_empty_input_returns_zero_score():
    rules = {
        "accuracy": MetricRule(
            name="accuracy",
            minimum=0,
            maximum=100,
        )
    }

    engine = BenchmarkEngine(rules)

    data = BenchmarkInput(metrics={})

    result = engine.evaluate(data)

    assert result.score == 0.0