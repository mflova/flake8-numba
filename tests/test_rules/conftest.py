import ast
import os
import re
from collections.abc import Generator
from typing import Any

import pytest

from flake8_numba.rule import Error


@pytest.fixture
def node(file_name: str) -> ast.FunctionDef:
    """Node representing the ast conversion of the function.

    Args:
        file_name (str): File where the function is loaded.

    Returns:
        ast.FunctionDef: Node representing given function.
    """
    path = os.path.join(os.path.dirname(__file__), "data", file_name) + ".py"
    with open(path) as f:
        string = f.read()
    return ast.parse(string).body[0]  # type: ignore


@pytest.fixture
def errors(request: pytest.FixtureRequest) -> Generator[list[Error], None, None]:
    """Fixture used to perform extra checks over the code label."""
    errors: list[Error] = []
    yield errors
    check_name = re.search(r"test_(.*?)\[", request.node.name)
    if not check_name:
        raise ValueError("Test should be named `test_<CHECK>")

    check_name_str = check_name.group(1).lower()
    for error in errors:
        msg = (
            f"Name of the test {request.node.name} must match the check to be tested "
            f"{error.message[:6].lower()}. Ensure code is OK."
        )
        assert error.message.lower().startswith(check_name_str), msg


@pytest.fixture(autouse=True)
def _test_no_print_statements(
    capsys: pytest.CaptureFixture[Any],
) -> Generator[None, None, None]:
    """Verify that no print statements were added in any of these tests."""
    yield
    captured = capsys.readouterr()
    msg = "Print statements were detected for the checks."
    assert not captured.out, msg
    assert not captured.err, msg
