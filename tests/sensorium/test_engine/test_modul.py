"""Test Hello."""
from sensorium.engine.dummy_modul import hello


def test_hello() -> None:
    """Test for Hello."""
    assert hello() == 'Hallo!'
