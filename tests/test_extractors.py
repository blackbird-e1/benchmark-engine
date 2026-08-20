from benchmark_engine.extractors import AviationExtractor


def test_aviation_extractor():
    extractor = AviationExtractor()

    result = extractor.extract(
        {
            "speed_knots": [180, 220, 250],
            "bank_angle_deg": [-10, 20, -35, 15],
            "descent_rate_fpm": [500, 900, 1200, 1500],
            "throttle_percent": [40, 50, 60],
        }
    )

    assert result.metrics["max_speed_knots"] == 250
    assert result.metrics["max_bank_angle_deg"] == 35
    assert result.metrics["max_descent_rate_fpm"] == 1500
    assert result.metrics["avg_throttle_percent"] == 50


def test_aviation_extractor_rejects_missing_field():
    extractor = AviationExtractor()

    try:
        extractor.extract(
            {
                "speed_knots": [180, 220],
                "bank_angle_deg": [10, 20],
                "descent_rate_fpm": [500, 1000],
            }
        )
        assert False
    except ValueError as error:
        assert "throttle_percent" in str(error)


def test_aviation_extractor_rejects_empty_field():
    extractor = AviationExtractor()

    try:
        extractor.extract(
            {
                "speed_knots": [],
                "bank_angle_deg": [10, 20],
                "descent_rate_fpm": [500, 1000],
                "throttle_percent": [40, 50],
            }
        )
        assert False
    except ValueError as error:
        assert "speed_knots" in str(error)