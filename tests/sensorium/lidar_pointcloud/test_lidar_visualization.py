# # Copyright 2024  Projektpraktikum Python.
# # SPDX-License-Identifier: Apache-2.0
"""dummy module."""

import os
from unittest.mock import patch

import numpy as np
import pygfx as gfx  # type: ignore[import-untyped]
import pytest
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]
from wgpu.gui.qt import WgpuCanvas  # type: ignore[import-untyped]

from sensorium.lidar_pointcloud.lidar_visualization import PointcloudVis


@pytest.fixture
def pointcloud_vis() -> PointcloudVis:
    """Fixture to create a PointcloudVis instance."""
    return PointcloudVis()


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_setup_canvas_initialization(qtbot: QtBot, pointcloud_vis: PointcloudVis) -> None:
    """Test setup_canvas method."""
    qtbot.addWidget(pointcloud_vis)
    pointcloud_vis.setup_canvas()
    assert isinstance(pointcloud_vis.canvas, WgpuCanvas)
    assert isinstance(pointcloud_vis.renderer, gfx.WgpuRenderer)
    assert isinstance(pointcloud_vis.scene, gfx.Scene)
    assert isinstance(pointcloud_vis.camera, gfx.OrthographicCamera)


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_update_scene(qtbot: QtBot, pointcloud_vis: PointcloudVis) -> None:
    """Test update_scene method."""
    qtbot.addWidget(pointcloud_vis)
    pointcloud_vis.setup_canvas()
    frame_id = 0
    mock_positions = np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]], dtype=np.float32)

    with patch.object(
        pointcloud_vis, 'load_positions', return_value=mock_positions
    ) as mock_load_positions:
        pointcloud_vis.update_scene(frame_id)
        mock_load_positions.assert_called_once_with(frame_id)
        frame_id += 1
        pointcloud_vis.update_scene(frame_id)
