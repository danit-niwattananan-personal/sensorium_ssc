# Copyright 2024 Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test camera visualization."""

import numpy as np
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.visualization.camera_visualization import (
    CameraWidget,
)


def test_show_image(qtbot: QtBot) -> None:
    """Test the show_image method of CameraWidget."""
    height, width, channels = 375, 1242, 3
    rng = np.random.default_rng()
    mock_image = rng.integers(0, 255, size=(height, width, channels), dtype=np.uint8)
    widget = CameraWidget()
    qtbot.addWidget(widget)

    widget.show_image(mock_image)
