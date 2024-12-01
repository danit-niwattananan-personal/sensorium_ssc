"""Test Hello."""
from data_processing.dummy_module_antonija import hello


def test_hello() -> None:
    """Test for Hello."""
    assert hello() == 'Hello!'
