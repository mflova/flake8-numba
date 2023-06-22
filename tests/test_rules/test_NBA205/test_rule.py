import ast
import os
from typing import Final

import pytest

from flake8_numba.rules.nba2 import NBA205


class TestRule:
    DATA_DIR: Final = "data"
    """Directory where data lies."""

    @pytest.fixture
    def node(self, file_name: str) -> ast.FunctionDef:
        """Node representing the ast conversion of the function.

        Args:
            file_name (str): File where the function is loaded.

        Returns:
            ast.FunctionDef: Node representing given function.
        """
        path = os.path.join(os.path.dirname(__file__), self.DATA_DIR, file_name) + ".py"
        with open(path) as f:
            string = f.read()
        return ast.parse(string).body[0]  # type: ignore

    @pytest.mark.parametrize(
        "file_name, expected_error",
        [
            ("guvec_func_with_return_none", False),
            ("guvec_func_with_return", True),
            ("guvec_func_without_return", False),
            ("non_guvec_func", False),
        ],
    )
    def test_rule(
        self, file_name: str, expected_error: bool, node: ast.FunctionDef
    ) -> None:
        """Test that the rule returns the expected outputs for different functions.

        Args:
            file_name (str): Name of the file that will be read from `data` folder.
            expected_error (bool): `True` if the rule is supposed to return an error for
                the function defined in `file_name`. `False` otherwise.
            node (ast.FunctionDef): Node describing the function from the txt file and
                parsed by ast
        """
        assert expected_error == bool(NBA205.check(node))
