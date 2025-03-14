# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import asyncio
import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.engine.visualization_gui import VisualisationGui


@pytest.fixture
def _event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Asyncio event loop is running."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_visualitsation_gui(qtbot: QtBot) -> None:
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
    await asyncio.sleep(0)


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_update_frame() -> None:
    """Testet update_frame."""
    config_path = Path.cwd() / 'configs' / 'sensorium.yaml'
    config_content = await asyncio.to_thread(config_path.read_text)
    config = yaml.safe_load(config_content)
    max_frame = config['frontend_engine']['max_frame']
    visualisation = VisualisationGui()
    visualisation.framenumber = 1
    await visualisation.update_frame(1)
    assert visualisation.framenumber == 2
    await visualisation.update_frame(-10)
    assert visualisation.framenumber == 0
    await visualisation.update_frame(max_frame + 1)
    assert visualisation.framenumber == 0


@pytest.mark.usefixtures('_event_loop')
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
        patch(
            'sensorium.engine.visualization_gui.VisualisationGui.update_frame'
        ) as mock_update_frame,
        patch('sensorium.visualization.voxel_widget.VoxelWidget.update_scene') as mock_update_voxel,
    ):
        await visualisation.update_scene()
        mock_update_camera.assert_called_with(0, 1)
        mock_update_trajectory.assert_called_once_with(0, 1)
        mock_update_pointcloud.assert_called_once_with(0, 1)
        mock_update_voxel.assert_called_once_with(0, 1)
        mock_update_frame.assert_called_once_with(1)


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_load_frame(qtbot: QtBot) -> None:
    """Testet load_frame."""
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
        patch('sensorium.visualization.voxel_widget.VoxelWidget.update_scene') as mock_update_voxel,
    ):
        await visualisation.load_frame(0, 1)
        mock_update_camera.assert_called_with(0, 1)
        mock_update_trajectory.assert_called_once_with(0, 1)
        mock_update_pointcloud.assert_called_once_with(0, 1)
        mock_update_voxel.assert_called_once_with(0, 1)


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_set_frame_slider(qtbot: QtBot) -> None:
    """Testet set_frame_slider."""
    visualisation = VisualisationGui()
    qtbot.addWidget(visualisation)
    visualisation.framenumber = 30
    await visualisation.set_frame_slider()
    assert visualisation.framenumber == visualisation.slider.value()
    visualisation.slider.setValue(50)
    await asyncio.sleep(0.1)
    assert visualisation.framenumber == 50


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_toggle_play_stop(qtbot: QtBot) -> None:
    """Testet toggle_play_stop."""
    visualisation = VisualisationGui()
    qtbot.addWidget(visualisation)
    visualisation.play_en = True
    await visualisation.toggle_play_stop()
    assert visualisation.play_en is False
    assert visualisation.button_play_stop.text() == 'Stop'
    assert visualisation.animation_timer.isActive()
    qtbot.mouseClick(visualisation.button_play_stop, Qt.LeftButton)  # type: ignore[attr-defined]
    await asyncio.sleep(0.1)
    assert visualisation.play_en is True
    assert visualisation.button_play_stop.text() == 'Play'
    assert not visualisation.animation_timer.isActive()
