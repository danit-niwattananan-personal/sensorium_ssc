# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Client executable tests."""

from __future__ import annotations

from unittest.mock import patch

# ohne "src." bekomme ich die Fehlermedlung:
# "Cannot find implementation or library stub for module named "sensorium.server"Mypy".
# In Ihrer Präsentation meinten Sie glaube ich, dass man das nicht so machen sollte.
# Wie würde man den Fehler also richtig beheben?
from src.sensorium.client import run


def test_entrypoint() -> None:
    """Test entrypoint is a callable."""
    assert callable(run)


def test_calls_sleep() -> None:
    """Test entrypoint calls sleep."""
    with patch('time.sleep') as sleep_mock:
        run()
        sleep_mock.assert_called_once_with(5)
