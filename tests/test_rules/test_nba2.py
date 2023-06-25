import ast

import pytest

from flake8_numba.rule import Error
from flake8_numba.rules.nba2 import (
    NBA201,
    NBA202,
    NBA203,
    NBA204,
    NBA205,
    NBA206,
    NBA207,
    NBA208,
    NBA211,
)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_with_matching_signatures", False),
        ("nba2/guvec_with_missmatching_signatures", True),
        ("nba2/guvec_with_missmatching_signatures2", True),
    ],
)
def test_nba201(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA201().check(node, errors)
    assert expected_error == bool(errors)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_with_matching_signatures", False),
        ("nba2/guvec_with_missmatching_signatures3", True),
    ],
)
def test_nba202(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA202().check(node, errors)
    assert expected_error == bool(errors)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_with_constants_in_signature", False),
        ("nba2/guvec_with_undefined_symbols_in_signature", True),
        ("nba2/guvec_with_one_pos_arg", False),
        ("nba2/guvec_with_two_pos_args", False),
        ("nba2/func", False),
    ],
)
def test_nba203(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA203().check(node, errors)
    assert expected_error == bool(errors)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_with_constants_in_signature", True),
        ("nba2/guvec_with_undefined_symbols_in_signature", False),
        ("nba2/guvec_with_one_pos_arg", False),
        ("nba2/guvec_with_two_pos_args", False),
        ("nba2/func", False),
    ],
)
def test_nba204(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA204().check(node, errors)
    assert expected_error == bool(errors)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_func_with_return_none", False),
        ("nba2/guvec_func_with_return", True),
        ("nba2/guvec_func_without_return", False),
        ("nba2/func", False),
    ],
)
def test_nba205(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA205().check(node, errors)
    assert expected_error == bool(errors)


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
def test_nba206(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA206().check(node, errors)
    assert expected_error == bool(errors)


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
def test_nba207(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA207().check(node, errors)
    assert expected_error == bool(errors)


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
def test_nba208(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA208().check(node, errors)
    assert expected_error == bool(errors)


@pytest.mark.parametrize(
    "file_name, expected_error",
    [
        ("nba2/guvec_with_two_pos_args", False),
        ("nba2/guvec_with_missing_commas", True),
    ],
)
def test_nba211(
    file_name: str, expected_error: bool, node: ast.FunctionDef, errors: list[Error]
) -> None:
    """Test that the rule returns the expected outputs for different functions."""
    NBA211().check(node, errors)
    assert expected_error == bool(errors)
