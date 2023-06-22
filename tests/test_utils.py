from flake8_numba import utils
import ast
import pytest


class TestHasReturnValue:
    @pytest.mark.parametrize(
        "function, has_return_value",
        [
            (
                """
def func():
    return 2
""",
                True,
            ),
            (
                """
def func():
    return
""",
                False,
            ),
            (
                """
def func():
    pass
""",
                False,
            ),
        ],
    )
    def test_has_reutrn_value(self, function: str, has_return_value: bool) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            function (str): Function defined as a string
            has_return_value (bool): Expected output of the function.
        """
        tree = ast.parse(function)
        func = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)][0]

        assert has_return_value == utils.has_return_value(func)[0]


class TestIsDecoratedWith:
    @pytest.mark.parametrize(
        "function, expected_output",
        [
            (
                """
@numba.guvectorize
def func():
    ...
""",
                True,
            ),
            (
                """
@nb.guvectorize
def func():
    ...
""",
                True,
            ),
            (
                """
@guvectorize
def func():
    pass
""",
                True,
            ),
            (
                """
@vectorize
def func():
    ...
""",
                False,
            ),
            (
                """
def func():
    ...
""",
                False,
            ),
        ],
    )
    def test_is_decorated_with(self, function: str, expected_output: bool) -> None:
        """Test that for multiple given functions, the function returns the expected value.

        Args:
            function (str): Function defined as a string
            expected_output(bool): Expected output of the function to be tested.
        """
        tree = ast.parse(function)
        func = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)][0]

        assert expected_output == utils.is_decorated_with("guvectorize", func)
