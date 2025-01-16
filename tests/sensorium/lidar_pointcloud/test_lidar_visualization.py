# # Copyright 2024  Projektpraktikum Python.
# # SPDX-License-Identifier: Apache-2.0
"""dummy module."""

from unittest.mock import patch

import numpy as np
import pygfx as gfx  # type: ignore[import-untyped]
import pytest
from PySide6 import QtWidgets
from wgpu.gui.qt import WgpuCanvas  # type: ignore[import-untyped]

from sensorium.lidar_pointcloud.lidar_visualization import PointcloudVis


@pytest.fixture
def app() -> QtWidgets.QApplication:
    """."""
    return QtWidgets.QApplication([])


@pytest.fixture
def pointcloud_vis() -> PointcloudVis:
    """Fixture to create a PointcloudVis instance."""
    with patch('wgpu.gui.qt.get_alt_x11_display', return_value=1):
        return PointcloudVis()


def test_setup_canvas_initialization(
    app: QtWidgets.QApplication, pointcloud_vis: PointcloudVis
) -> None:
    """Test setup_canvas method."""
    # Patch die Funktion und erhalte das Mock-Objekt

    # Initialisiere das Canvas
    pointcloud_vis.setup_canvas()
    assert isinstance(pointcloud_vis.canvas, WgpuCanvas)
    assert isinstance(pointcloud_vis.renderer, gfx.WgpuRenderer)
    assert isinstance(pointcloud_vis.scene, gfx.Scene)
    assert isinstance(pointcloud_vis.camera, gfx.OrthographicCamera)

    # App sauber herunterfahren
    app.shutdown()
    app.quit()


def test_update_scene(app: QtWidgets.QApplication, pointcloud_vis: PointcloudVis) -> None:
    """Test update_scene method."""
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

    app.shutdown()
    app.quit()
