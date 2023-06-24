import pytest
import ast
import os


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
