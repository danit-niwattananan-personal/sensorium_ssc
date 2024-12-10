# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""dummy module."""

from sensorium.lidar_pointcloud.bin_to_ply import bin_to_ply_function


def test_bin_to_ply_function() -> None:
    """Dummy function."""
    assert bin_to_ply_function() == 1
