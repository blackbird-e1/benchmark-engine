"""Python code extractor for benchmark-engine."""

import ast
from typing import Mapping

from benchmark_engine.core.models import BenchmarkInput

from .base import BaseExtractor


class CodingExtractor(BaseExtractor):
    """
    Extract simple, deterministic metrics from Python source code.

    The extractor does not score the code.
    It only converts source code into benchmarkable metrics.
    """

    def extract(self, data: str) -> BenchmarkInput:
        """Extract benchmark metrics from Python source code."""

        if not data or not data.strip():
            raise ValueError("Python source code cannot be empty")

        try:
            tree = ast.parse(data)
        except SyntaxError as error:
            raise ValueError("Invalid Python source code") from error

        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        operations = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.BinOp)
        ]

        has_division = any(
            isinstance(node.op, (ast.Div, ast.FloorDiv))
            for node in operations
        )

        has_error_handling = any(
            isinstance(node, ast.Try)
            for node in ast.walk(tree)
        )

        line_count = len(data.splitlines())

        metrics = {
            "function_count": len(functions),
            "operation_count": len(operations),
            "has_division": int(has_division),
            "has_error_handling": int(has_error_handling),
            "line_count": line_count,
        }

        return BenchmarkInput(metrics=metrics)