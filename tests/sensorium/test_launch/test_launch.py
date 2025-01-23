# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test module for launch."""

import pytest
from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]

from sensorium.launch.launch import LaunchWindow


@pytest.fixture
def window() -> LaunchWindow:
    """Fixture to create a LaunchWindow instance."""
    return LaunchWindow()


def test_launch_window_geometry(qtbot: QtBot, window: LaunchWindow) -> None:
    """Test to verify LaunchWindow geometry."""
    qtbot.addWidget(window)
    assert window.x() == 300
    assert window.y() == 300
    assert window.width() == 400
    assert window.height() == 200
