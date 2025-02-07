# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test module for Camera visualization."""

from unittest.mock import patch

import numpy as np
import pytest
import qimage2ndarray  # type: ignore[import-untyped]
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.visualization.camera_visualization import CAMERA2_SHAPE, CameraWidget

MOCK_CAMERA_DATA = np.zeros(np.prod(CAMERA2_SHAPE), dtype=np.uint8)


@pytest.mark.asyncio
async def test_show_image(qtbot: QtBot) -> None:
    """Test show_image method of CameraWidget.

    Args:
        qtbot: Pytest-qt fixture to handle Qt events.
    """
    with patch(
        'sensorium.visualization.camera_visualization.get_camera2_data',
        return_value=MOCK_CAMERA_DATA,
    ):
        widget = CameraWidget(camera_id='camera2')
        qtbot.addWidget(widget)

        await widget.show_image(seq_id=0, frame_id=0)

        pixmap = widget.label.pixmap()
        assert not pixmap.isNull()
        assert (pixmap.height(), pixmap.width()) == CAMERA2_SHAPE[:2]

        # qimage2ndarray extenion used to convert QImage to a numpy array
        img_array = qimage2ndarray.rgb_view(pixmap.toImage())
        assert img_array.shape == CAMERA2_SHAPE

        widget = CameraWidget(camera_id='invalid_camera')
        qtbot.addWidget(widget)

        with pytest.raises(ValueError, match='Invalid camera_id'):
            await widget.show_image(seq_id=0, frame_id=0)
