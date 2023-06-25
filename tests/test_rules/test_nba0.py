import ast

import pytest

from flake8_numba.rule import Error
from flake8_numba.rules.nba0 import NBA006, NBA007


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba0/func", False),
        ("nba0/vec_in_bound_method", True),
        ("nba0/guvec_in_bound_method", True),
        ("nba0/guvec_with_no_args", False),
        ("nba0/guvec_with_matching_signatures", False),
    ],
)
def test_nba006(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA006().check(node, errors)
    assert expected_error == bool(errors)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba0/func", False),
        ("nba0/guvec_with_first_arg_wrong_type", True),
        ("nba0/vec_with_first_arg_wrong_type", True),
        ("nba0/vec_with_matching_signatures", False),
        ("nba0/guvec_with_matching_signatures", False),
    ],
)
def test_nba007(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA007().check(node, errors)
    assert expected_error == bool(errors)
