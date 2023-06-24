import ast

import pytest

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
def test_nba006(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA006.check(node))


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
def test_nba007(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA007.check(node))
