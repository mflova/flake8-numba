import ast
import os
from typing import Final

import pytest

from flake8_numba import Error, Rule

THIS_DIR: Final = os.path.dirname(__file__)
"""Directory where this script lies."""

FILE_PATH: Final = os.path.join(THIS_DIR, "data", "regression.py")
"""Path to the file to be tested."""


@pytest.fixture
def ast_nodes() -> list[ast.FunctionDef]:
    with open(FILE_PATH, "r") as f:
        source_code = f.read()
    ast_module = ast.parse(source_code, filename=FILE_PATH)
    return [node for node in ast.walk(ast_module) if isinstance(node, ast.FunctionDef)]


def test_regression(ast_nodes: list[ast.FunctionDef]) -> None:
    """Test all rules in `regression.py` collection."""
    for node in ast_nodes:
        errors: list[Error] = []
        for rule in Rule.all_rules:
            status = rule.check(node, errors)
            if not status:
                err_msg = f"{type(rule).__name__} was triggered: {errors[-1]}."
                assert status, err_msg
