# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test module for launch."""

import pytest
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.launch.launch import LaunchWindow


@pytest.fixture
def window(qtbot: QtBot) -> LaunchWindow:
    """Create and show a LaunchWindow instance.

    Args:
        qtbot (QtBot): The pytest-qt bot instance.

    Returns:
        LaunchWindow: The instantiated launch window.
    """
    launch = LaunchWindow()
    qtbot.addWidget(launch)
    launch.show()
    return launch


def test_server_mode_setup(window: LaunchWindow) -> None:
    """Test the server_mode GUI.

    Args:
        window (LaunchWindow): The launch window fixture.

    Returns:
        None
    """
    window.server_mode()
    assert window.mode == 'server'
    assert window.input_label.text() == 'Enter Port Number:'
    assert not window.ip_field.isVisible()
    assert window.port_field.isVisible()


def test_client_mode_setup(window: LaunchWindow) -> None:
    """Test the client_mode GUI.

    Args:
        window (LaunchWindow): The launch window fixture.

    Returns:
        None
    """
    window.client_mode()
    assert window.mode == 'client'
    assert window.input_label.text() == 'Enter IP Address and Port:'
    assert window.ip_field.isVisible()
    assert window.port_field.isVisible()
