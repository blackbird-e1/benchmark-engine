from benchmark_engine import BenchmarkEngine, BenchmarkInput
from benchmark_engine.adapters import AVIATION_RULES


def main():
    engine = BenchmarkEngine(AVIATION_RULES)

    benchmark_input = BenchmarkInput(
        metrics={
            "max_speed_knots": 220,
            "max_bank_angle_deg": 25,
            "max_descent_rate_fpm": 1200,
            "avg_throttle_percent": 50,
        }
    )

    result = engine.evaluate(benchmark_input)

    print(f"Overall score: {result.score:.2f}")

    for name, metric in result.metrics.items():
        print(
            f"{name}: "
            f"value={metric.value}, "
            f"score={metric.score:.2f}, "
            f"status={metric.status}, "
            f"benchmark={metric.benchmark}"
        )


if __name__ == "__main__":
    main()