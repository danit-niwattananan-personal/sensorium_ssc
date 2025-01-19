# Copyright 2024 Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test camera visualization."""

from unittest.mock import Mock, patch

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.visualization.camera_visualization import (
    CameraWidget,
)


def test_show_image(qtbot: QtBot) -> None:
    """Test the show_image method of CameraWidget."""
    mock_img = np.zeros((375, 1242, 3), dtype=np.uint8)
    with patch('cv2.imread', return_value=mock_img):
        camera_widget = CameraWidget()
        qtbot.addWidget(camera_widget)
        frame_id = 0

        with patch('sensorium.visualization.camera_visualization.QPixmap') as mock_pixmap:
            mock_pixmap_instance = Mock(spec=QPixmap)
            mock_pixmap_instance.scaled.return_value = QPixmap()
            mock_pixmap.return_value = mock_pixmap_instance

            camera_widget.show_image(frame_id)

            mock_pixmap_instance.scaled.assert_called_once_with(
                camera_widget.label.width(),
                camera_widget.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )
