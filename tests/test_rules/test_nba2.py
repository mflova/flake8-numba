import ast

import pytest

from flake8_numba.rules.nba2 import NBA205, NBA206, NBA207, NBA208


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_func_with_return_none", False),
        ("nba2/guvec_func_with_return", True),
        ("nba2/guvec_func_without_return", False),
        ("nba2/func", False),
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
        ("nba2/guvec", False),
        ("nba2/func", False),
        ("nba2/guvec_with_one_pos_arg", False),
        ("nba2/guvec_with_two_pos_args", False),
        ("nba2/guvec_with_second_arg_broken_parenthesis", True),
        ("nba2/guvec_with_second_arg_wrong_type", False),
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


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec", False),
        ("nba2/func", False),
        ("nba2/guvec_with_one_pos_arg", False),
        ("nba2/guvec_with_second_arg_wrong_type", True),
        ("nba2/guvec_with_second_arg_wrong_type2", True),
        ("nba2/guvec_with_two_pos_args", False),
    ],
)
def test_nba207(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA207.check(node))


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/func", False),
        ("nba2/guvec", True),
        ("nba2/guvec_with_one_pos_arg", True),
        ("nba2/guvec_with_two_pos_arg_wrong_type", True),
        ("nba2/guvec_with_two_pos_arg_wrong_type2", True),
        ("nba2/guvec_with_second_arg_wrong_type", True),
    ],
)
def test_nba208(file_name: str, expected_error: bool, node: ast.FunctionDef) -> None:
    """Test that the rule returns the expected outputs for different functions.

    Args:
        file_name (str): Name of the file that will be read from `data` folder.
        expected_error (bool): `True` if the rule is supposed to return an error for
            the function defined in `file_name`. `False` otherwise.
        node (ast.FunctionDef): Node describing the function from the txt file and
            parsed by ast
    """
    assert expected_error == bool(NBA208.check(node))
