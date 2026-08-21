from benchmark_engine import BenchmarkEngine
from benchmark_engine.adapters.coding import CODING_RULES
from benchmark_engine.extractors.coding import CodingExtractor


REFERENCE_CALCULATOR = """
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
"""


def test_coding_extractor_extracts_reference_metrics():
    extractor = CodingExtractor()

    result = extractor.extract(REFERENCE_CALCULATOR)

    assert result.metrics["function_count"] == 4
    assert result.metrics["operation_count"] == 4
    assert result.metrics["has_division"] == 1
    assert result.metrics["has_error_handling"] == 1


def test_reference_calculator_passes_coding_benchmark():
    extractor = CodingExtractor()
    engine = BenchmarkEngine(CODING_RULES)

    benchmark_input = extractor.extract(REFERENCE_CALCULATOR)
    result = engine.evaluate(benchmark_input)

    assert result.score == 1.0


def test_simple_incomplete_calculator_scores_lower():
    code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""

    extractor = CodingExtractor()
    engine = BenchmarkEngine(CODING_RULES)

    benchmark_input = extractor.extract(code)
    result = engine.evaluate(benchmark_input)

    assert result.score < 1.0


def test_coding_extractor_rejects_empty_code():
    extractor = CodingExtractor()

    try:
        extractor.extract("")
        assert False
    except ValueError as error:
        assert "empty" in str(error).lower()


def test_coding_extractor_rejects_invalid_python():
    extractor = CodingExtractor()

    invalid_code = """
def broken(
"""

    try:
        extractor.extract(invalid_code)
        assert False
    except ValueError as error:
        assert "invalid" in str(error).lower()
        