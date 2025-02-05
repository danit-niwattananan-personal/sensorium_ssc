# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test module for LiDAR visualization."""

import os
from unittest.mock import patch

import numpy as np
import pygfx as gfx  # type: ignore[import-untyped]
import pytest
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]
from wgpu.gui.qt import WgpuCanvas  # type: ignore[import-untyped]

from sensorium.visualization.lidar_visualization import PointcloudVis

MOCK_LIDAR_DATA = (np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]], dtype=np.float32), None)


@pytest.fixture
def pointcloud_vis(qtbot: QtBot) -> PointcloudVis:
    """Fixture to create and initialize a PointcloudVis instance.

    Args:
        qtbot: Pytest-qt fixture to handle Qt events.

    Returns:
        PointcloudVis: Instance of the PointcloudVis class
    """
    vis = PointcloudVis()
    qtbot.addWidget(vis)
    return vis


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_setup_canvas_initialization(pointcloud_vis: PointcloudVis) -> None:
    """Test the initialization of the canvas, renderer, scene, and camera.

    Args:
        pointcloud_vis: Instance of the PointcloudVis class.
    """
    pointcloud_vis.setup_scene()
    assert isinstance(pointcloud_vis.canvas, WgpuCanvas)
    assert isinstance(pointcloud_vis.renderer, gfx.WgpuRenderer)
    assert isinstance(pointcloud_vis.scene, gfx.Scene)
    assert isinstance(pointcloud_vis.camera, gfx.OrthographicCamera)


@pytest.mark.asyncio
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
async def test_update_scene(pointcloud_vis: PointcloudVis) -> None:
    """Test the update_scene method with mocked data.

    Args:
        pointcloud_vis: Instance of the PointcloudVis class.
        mock_positions: Numpy array of mock positions.
    """
    with patch(
        'sensorium.visualization.lidar_visualization.get_lidar_data', return_value=MOCK_LIDAR_DATA
    ):
        pointcloud_vis.setup_scene()

        mock_sizes = np.array([0.03, 0.03, 0.03], dtype=np.float32)
        await pointcloud_vis.update_scene(seq_id=0, frame_id=0)

        assert pointcloud_vis.pcd is not None
        expected_positions, _ = MOCK_LIDAR_DATA
        assert np.array_equal(pointcloud_vis.pcd.geometry.positions.data, expected_positions)
        assert np.array_equal(
            pointcloud_vis.pcd.geometry.colors.data,
            pointcloud_vis.load_colors_gradient(expected_positions),
        )
        assert np.array_equal(pointcloud_vis.pcd.geometry.sizes.data, mock_sizes)


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_animate(pointcloud_vis: PointcloudVis) -> None:
    """Test the animate_method to ensure the scene is rendered.

    Args:
        pointcloud_vis: Instance of the PointcloudVis class.
    """
    pointcloud_vis.setup_scene()
    pointcloud_vis.animate()
    assert pointcloud_vis.renderer is not None


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_load_colors_gradient() -> None:
    """Test the load_colors_gradient mehtod to ensure the right format.

    Args:
        mock_lidar_data: Numpy array of mock positions.
    """
    pointcloud_vis = PointcloudVis()
    positions, _ = MOCK_LIDAR_DATA
    colors = pointcloud_vis.load_colors_gradient(positions)
    assert colors.shape == (positions.shape[0], 3)
    assert np.all(colors[:, 0] == 1)
    assert np.all(colors[:, 2] == 0)
    assert colors[0, 1] > colors[1, 1] > colors[2, 1]
