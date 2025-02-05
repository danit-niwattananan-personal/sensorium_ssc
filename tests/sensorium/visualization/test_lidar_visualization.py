# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test module for LiDAR visualization."""

import os

import numpy as np
import pygfx as gfx  # type: ignore[import-untyped]
import pytest
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]
from wgpu.gui.qt import WgpuCanvas  # type: ignore[import-untyped]

from sensorium.visualization.lidar_visualization import PointcloudVis


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


@pytest.fixture
def mock_positions() -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
    """Fixture to create mock data for testing.

    Args:
        None.

    Returns:
        np.ndarray: Numpy array of mock positions.
    """
    return np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]], dtype=np.float32)


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_setup_canvas_initialization(pointcloud_vis: PointcloudVis) -> None:
    """Test the initialization of the canvas, renderer, scene, and camera.

    Args:
        pointcloud_vis: Instance of the PointcloudVis class.

    Returns:
        None.
    """
    pointcloud_vis.setup_canvas()
    assert isinstance(pointcloud_vis.canvas, WgpuCanvas)
    assert isinstance(pointcloud_vis.renderer, gfx.WgpuRenderer)
    assert isinstance(pointcloud_vis.scene, gfx.Scene)
    assert isinstance(pointcloud_vis.camera, gfx.OrthographicCamera)


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_update_scene(
    pointcloud_vis: PointcloudVis, mock_positions: np.ndarray[tuple[int, ...], np.dtype[np.float32]]
) -> None:
    """Test the update_scene method with mocked data.

    Args:
        pointcloud_vis: Instance of the PointcloudVis class.
        mock_positions: Numpy array of mock positions.

    Returns:
        None.
    """
    pointcloud_vis.setup_canvas()
    frame_id = 0
    mock_sizes = np.array([0.03, 0.03, 0.03], dtype=np.float32)
    pointcloud_vis.update_scene(frame_id, mock_positions)

    assert pointcloud_vis.pcd is not None
    assert np.array_equal(pointcloud_vis.pcd.geometry.positions.data, mock_positions)
    assert np.array_equal(
        pointcloud_vis.pcd.geometry.colors.data, pointcloud_vis.load_colors_gradient(mock_positions)
    )
    print(pointcloud_vis.pcd.geometry.sizes.data)
    assert np.array_equal(pointcloud_vis.pcd.geometry.sizes.data, mock_sizes)


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_animate(pointcloud_vis: PointcloudVis) -> None:
    """Test the animate_method to ensure the scene is rendered.

    Args:
        pointcloud_vis: Instance of the PointcloudVis class.

    Returns:
        None.
    """
    pointcloud_vis.setup_canvas()
    pointcloud_vis.animate()
    assert pointcloud_vis.renderer is not None


def test_load_colors_gradient(
    mock_positions: np.ndarray[tuple[int, ...], np.dtype[np.float32]],
) -> None:
    """Test the load_colors_gradient mehtod to ensure the right format.

    Args:
        mock_positions: Numpy array of mock positions.

    Returns:
        None.
    """
    vis = PointcloudVis()
    colors = vis.load_colors_gradient(mock_positions)
    assert colors.shape == (mock_positions.shape[0], 3)
    assert np.all(colors[:, 0] == 1)
    assert np.all(colors[:, 2] == 0)
    assert colors[0, 1] > colors[1, 1] > colors[2, 1]
