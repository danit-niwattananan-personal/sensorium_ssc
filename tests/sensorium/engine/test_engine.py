# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import os
from unittest.mock import patch

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit
from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]

from sensorium.engine.settings import SettingsDialog
from sensorium.engine.visualization_gui import VisualisationGui


def test_open_settings_window(qtbot: QtBot) -> None:
    """Testet das Einstellungsfenster mit pytest-qt."""
    dialog = SettingsDialog()
    dialog.show()
    qtbot.waitExposed(dialog)

    input_field = dialog.findChild(QLineEdit)
    assert input_field is not None

    assert dialog.apply_button is not None
    assert dialog.cancel_button is not None

    qtbot.mouseClick(dialog.apply_button, Qt.LeftButton)
    assert not dialog.isVisible()

    dialog = SettingsDialog()
    dialog.show()
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)
    assert not dialog.isVisible()


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_visualitsation_gui(qtbot: QtBot) -> None:
    """Testet die funktionen der Visualisation GUI."""
    visualisation = VisualisationGui()
    qtbot.add_widget(visualisation)
    with patch(
        'sensorium.engine.visualization_gui.VisualisationGui.update_frame'
    ) as mock_update_frame:
        qtbot.mouseClick(visualisation.button_minus10, Qt.LeftButton)  # type: ignore[attr-defined]
        mock_update_frame.assert_called_with(-10)

        qtbot.mouseClick(visualisation.button_minus1, Qt.LeftButton)  # type: ignore[attr-defined]
        mock_update_frame.assert_called_with(-1)

        qtbot.mouseClick(visualisation.button_plus1, Qt.LeftButton)  # type: ignore[attr-defined]
        mock_update_frame.assert_called_with(1)

        qtbot.mouseClick(visualisation.button_plus10, Qt.LeftButton)  # type: ignore[attr-defined]
        mock_update_frame.assert_called_with(10)


def test_update_frame() -> None:
    """Testet update_frame."""
    visualisation = VisualisationGui()
    visualisation.framenumber = 1
    visualisation.update_frame(1)
    assert visualisation.framenumber == 2

    visualisation.update_frame(-10)
    assert visualisation.framenumber == 0

    visualisation.update_frame(450)
    assert visualisation.framenumber == 10


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_update_scene(qtbot: QtBot) -> None:
    """Testet update_scene."""
    visualisation = VisualisationGui()
    qtbot.addWidget(visualisation)
    visualisation.framenumber = 1
    with (
        patch(
            'sensorium.visualization.camera_visualization.CameraWidget.show_image'
        ) as mock_update_camera,
        patch(
            'sensorium.visualization.trajectory_visualization.Trajectory.draw_line'
        ) as mock_update_trajectory,
        patch(
            'sensorium.visualization.lidar_visualization.PointcloudVis.update_scene'
        ) as mock_update_pointcloud,
    ):
        visualisation.update_scene()
        mock_update_camera.assert_called_with(1)
        mock_update_trajectory.assert_called_with(1)
        mock_update_pointcloud.assert_called_with(1)
