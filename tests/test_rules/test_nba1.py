import ast

import pytest

from flake8_numba.rule import Error
from flake8_numba.rules.nba1 import NBA101


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba1/func", False),
        ("nba1/vec_with_one_return", False),
        ("nba1/vec_with_two_returns", True),
    ],
)
def test_nba101(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA101().check(node, errors)
    assert expected_error == bool(errors)
