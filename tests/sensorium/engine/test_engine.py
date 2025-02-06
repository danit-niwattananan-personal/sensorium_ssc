# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import asyncio
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]

from sensorium.engine.visualization_gui import VisualisationGui


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


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_update_frame() -> None:
    """Testet update_frame."""
    # Load the config for max_frame
    config_path = Path.cwd() / 'configs' / 'sensorium.yaml'
    config_content = await asyncio.to_thread(config_path.read_text)
    config = yaml.safe_load(config_content)
    max_frame = config['frontend_engine']['max_frame']

    # Test if the frame number is increased by 1
    visualisation = VisualisationGui()
    visualisation.framenumber = 1
    await visualisation.update_frame(1)
    assert visualisation.framenumber == 2

    # Test if the frame number is set to 0 if it is less than 0
    await visualisation.update_frame(-10)
    assert visualisation.framenumber == 0

    # Test if the frame number is set to 0 if it is greater than max_frame
    await visualisation.update_frame(max_frame + 1)
    assert visualisation.framenumber == 0


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_update_scene(qtbot: QtBot) -> None:
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
        await visualisation.update_scene()
        mock_update_camera.assert_called_with(1)
        mock_update_trajectory.assert_called_with(1)
        mock_update_pointcloud.assert_called_with(1)
