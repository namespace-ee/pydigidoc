import pytest

import pydigidoc


@pytest.fixture()
def lib():
    """Initialize and terminate pydigidoc around each test."""
    pydigidoc.initialize("pydigidoc-test")
    yield
    pydigidoc.terminate()
