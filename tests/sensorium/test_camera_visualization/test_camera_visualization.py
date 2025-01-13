# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
# """Camera Visualization."""

# from unittest.mock import Mock, patch

# from PySide6.QtCore import Qt
# from PySide6.QtGui import QPixmap

# from sensorium.camera_visualization.camera_visualization import CameraWidget


# def test_update_image() -> None:
#     """."""
#     camera_widget = CameraWidget()
#     with patch('PySide6.QtGui.QPixmap') as mock_pixmap:
#         pixmap = Mock()
#         pixmap.scaled.return_value = pixmap
#         mock_pixmap.return_value = pixmap
#         camera_widget.update_image()
#         pixmap.scaled.assert_called_once_with(
#             camera_widget.label.width(),
#             camera_widget.label.height(),
#             Qt.AspectRatioMode.KeepAspectRatio,
#         )
#     assert camera_widget.label.setPixmap.call_count == 1


import sys
from unittest.mock import Mock, patch

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from sensorium.camera_visualization.camera_visualization import (
    CameraWidget,
)


# @pytest.fixture
# def start_application() -> QApplication:
#     """Fixture zum Erstellen und Initialisieren des MainWindow."""
#     return QApplication([])


def test_update_image() -> None:
    """."""
    app = QApplication([])
    # start_application
    camera_widget = CameraWidget()

    with patch('sensorium.camera_visualization.camera_visualization.QPixmap') as mock_pixmap:
        mock_pixmap_instance = Mock()
        mock_pixmap.return_value = mock_pixmap_instance
        mock_pixmap_instance.scaled.return_value = mock_pixmap_instance

        camera_widget.update_image()

        mock_pixmap.assert_called_once_with(
            camera_widget.img_directory + '/' + f'{camera_widget.frame_number - 1:010d}.png'
        )
        mock_pixmap_instance.scaled.assert_called_once_with(
            camera_widget.label.width(),
            camera_widget.label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )
    app.shutdown()
