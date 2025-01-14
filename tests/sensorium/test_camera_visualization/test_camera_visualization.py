# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test camera visualization."""

from unittest.mock import Mock, patch

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from sensorium.camera_visualization.camera_visualization import (
    CameraWidget,
)


def test_show_image() -> None:
    """."""
    app = QApplication([])
    mock_img = np.zeros((375, 1242, 3), dtype=np.uint8)
    try:
        with patch('cv2.imread', return_value=mock_img):
            camera_widget = CameraWidget()
            camera_widget.frame_id = 99
            with patch(
                'sensorium.camera_visualization.camera_visualization.QPixmap'
            ) as mock_pixmap:
                mock_pixmap_instance = Mock(spec=QPixmap)
                mock_pixmap_instance.scaled.return_value = QPixmap()
                mock_pixmap.return_value = mock_pixmap_instance

                camera_widget.show_image()
                assert camera_widget.frame_id == 0
                mock_pixmap_instance.scaled.assert_called_once_with(
                    camera_widget.label.width(),
                    camera_widget.label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
                camera_widget.show_image()
                assert camera_widget.frame_id == 1

    finally:
        app.shutdown()
