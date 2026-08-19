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