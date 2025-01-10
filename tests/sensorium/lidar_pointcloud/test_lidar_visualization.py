# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""dummy module."""

import pytest

from sensorium.lidar_pointcloud.lidar_visualization import PointcloudVis


@pytest.fixture
def pointcloud() -> PointcloudVis:
    """."""
    return PointcloudVis()


def test_jump_forwards(pointcloud: PointcloudVis) -> None:
    """."""
    initial_frame = pointcloud.frame_number
    pointcloud.jump_forwards()
    assert pointcloud.frame_number == initial_frame + 10
