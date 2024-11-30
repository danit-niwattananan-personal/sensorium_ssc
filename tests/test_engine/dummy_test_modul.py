"""Test Hello."""
from engine.dummy_modul import hello


def test_hello() -> None:
    """Test for Hello."""
    assert hello() == 'Hallo!'
