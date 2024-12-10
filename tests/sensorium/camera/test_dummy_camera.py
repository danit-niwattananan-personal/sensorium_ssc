# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""dummy module."""

from sensorium.camera.dummy_camera import camera_function


def test_camera_function() -> None:
    """Dummy function."""
    assert camera_function() == 1
