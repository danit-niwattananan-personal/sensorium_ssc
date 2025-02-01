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
    """Fixture to create and initialize a PointcloudVis instance."""
    vis = PointcloudVis()
    qtbot.addWidget(vis)
    return vis


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_setup_canvas_initialization(pointcloud_vis: PointcloudVis) -> None:
    """Test the initialization of the canvas, renderer, scene, and camera."""
    pointcloud_vis.setup_canvas()
    assert isinstance(pointcloud_vis.canvas, WgpuCanvas)
    assert isinstance(pointcloud_vis.renderer, gfx.WgpuRenderer)
    assert isinstance(pointcloud_vis.scene, gfx.Scene)
    assert isinstance(pointcloud_vis.camera, gfx.OrthographicCamera)


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_update_scene(pointcloud_vis: PointcloudVis) -> None:
    """Test the update_scene method with mocked data."""
    pointcloud_vis.setup_canvas()
    frame_id = 0
    mock_positions = np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]], dtype=np.float32)
    mock_sizes = np.array([0.03, 0.03], dtype=np.float32)
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
    """Test the animate method to ensure the scene is rendered."""
    pointcloud_vis.setup_canvas()
    pointcloud_vis.animate()
    assert pointcloud_vis.renderer is not None
