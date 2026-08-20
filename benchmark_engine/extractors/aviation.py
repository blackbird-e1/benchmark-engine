"""Aviation telemetry extractor for benchmark-engine."""

from statistics import mean
from typing import Mapping, Sequence

from benchmark_engine.core.models import BenchmarkInput

from .base import BaseExtractor


class AviationExtractor(BaseExtractor):
    """
    Convert raw aviation telemetry into benchmarkable metrics.

    Expected input keys:

        speed_knots
        bank_angle_deg
        descent_rate_fpm
        throttle_percent

    The extractor intentionally contains only data preparation logic.
    Benchmark thresholds and scoring remain inside the benchmark engine.
    """

    REQUIRED_FIELDS = (
        "speed_knots",
        "bank_angle_deg",
        "descent_rate_fpm",
        "throttle_percent",
    )

    def extract(
        self,
        data: Mapping[str, Sequence[float]],
    ) -> BenchmarkInput:
        """Extract aviation metrics from raw telemetry."""

        self._validate_input(data)

        metrics = {
            "max_speed_knots": max(data["speed_knots"]),
            "max_bank_angle_deg": max(
                abs(value) for value in data["bank_angle_deg"]
            ),
            "max_descent_rate_fpm": max(
                data["descent_rate_fpm"]
            ),
            "avg_throttle_percent": mean(
                data["throttle_percent"]
            ),
        }

        return BenchmarkInput(metrics=metrics)

    def _validate_input(
        self,
        data: Mapping[str, Sequence[float]],
    ) -> None:
        """Validate that the required telemetry is available."""

        for field in self.REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(
                    f"Missing required aviation telemetry: '{field}'"
                )

            if not data[field]:
                raise ValueError(
                    f"Aviation telemetry field '{field}' is empty"
                )