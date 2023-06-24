import ast

import pytest

from flake8_numba.rules.nba1 import NBA101


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba1/func", False),
        ("nba1/vec_with_one_return", False),
        ("nba1/vec_with_two_returns", True),
    ],
)
def test_nba101(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA101.check(node))
