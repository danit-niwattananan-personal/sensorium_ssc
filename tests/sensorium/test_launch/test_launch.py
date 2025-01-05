# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test module for launch."""

import pytest
from PySide6.QtWidgets import QApplication

from sensorium.launch.launch import LaunchWindow


@pytest.fixture
def app() -> QApplication:
    """Fixture to create a QApplication instance."""
    if not QApplication.instance():
        return QApplication([])
    return QApplication.instance()


@pytest.fixture
def window() -> LaunchWindow:
    """Fixture to create a LaunchWindow instance."""
    return LaunchWindow()


def test_launch_window_geometry(window: LaunchWindow) -> None:
    """Test to verify LaunchWindow geometry."""
    assert window.x() == 300
    assert window.y() == 300
    assert window.width() == 400
    assert window.height() == 200
