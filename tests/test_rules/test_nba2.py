import ast
import os
from typing import Final

import pytest

from flake8_numba.rules.nba2 import NBA205, NBA206


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("guvec_func_with_return_none", False),
        ("guvec_func_with_return", True),
        ("guvec_func_without_return", False),
        ("func", False),
    ],
)
def test_nba205(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA205.check(node))


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("guvec", False),
        ("func", False),
        ("guvec_with_one_pos_arg", False),
        ("guvec_with_two_pos_args", False),
        ("guvec_with_second_arg_broken_parenthesis", True),
        ("guvec_with_second_arg_wrong_type", False),
    ],
)
def test_nba206(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA206.check(node))
