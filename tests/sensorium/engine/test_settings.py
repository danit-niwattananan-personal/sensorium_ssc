# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import os

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.engine.settings import SettingsDialog
from sensorium.engine.visualization_gui import VisualisationGui


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_open_settings_window(qtbot: QtBot) -> None:
    """Testet das Einstellungsfenster mit pytest-qt."""
    vizualisation = VisualisationGui()
    dialog = SettingsDialog(vizualisation)
    qtbot.add_widget(vizualisation)

    assert dialog.speed_input is not None
    assert dialog.input_field is not None
    assert dialog.apply_button is not None
    assert dialog.cancel_button is not None

    dialog.input_field.setText(str(100))
    dialog.speed_input.setText(str(10))
    assert dialog.input_field.text() == str(100)
    assert dialog.speed_input.text() == str(10)

    qtbot.mouseClick(dialog.apply_button, Qt.LeftButton)  # type: ignore[attr-defined]
    assert vizualisation.fps == 10
    assert vizualisation.next_frame_time == 100
    assert vizualisation.maxframe == 100

    assert not dialog.isVisible()

    dialog = SettingsDialog(vizualisation)

    dialog.input_field.setText(str(10))
    dialog.speed_input.setText(str(1))

    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    assert vizualisation.fps == 10
    assert vizualisation.maxframe == 100
    assert not dialog.isVisible()
