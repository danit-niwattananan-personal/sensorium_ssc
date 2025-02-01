# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera Visualization."""

import sys
from pathlib import Path

import cv2  # noqa: F401
import numpy as np
from cv2.typing import MatLike
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class CameraWidget(QMainWindow):
    """."""

    def __init__(self) -> None:
        """."""
        super().__init__()
        self.img_directory = ''
        # sample_img = cv2.imread(self.img_directory + '/' + '0000000000.png')  # noqa: ERA001
        self._height, self._width = 375, 1242
        self.setup_lable()

    def setup_lable(self) -> None:
        """."""
        scale_factor = 0.8
        # width = int(self._width * scale_factor)
        width = self._width
        height = int(self._height * scale_factor)
        self.setWindowTitle('Video')
        self.setGeometry(100, 100, width, height) # NOTE: make it scalable
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

    def show_image(self, image_data: MatLike) -> None:
        """."""
        image = np.ascontiguousarray(image_data)
        rgb_array = np.ascontiguousarray(image[..., ::-1])
        height, width, channels = rgb_array.shape
        bytes_per_line = channels * width
        qimage = QImage(
            rgb_array.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(qimage)

        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWidget()
    window.img_directory = (
        r'C:\Users\wich_\Desktop\2011_09_26\2011_09_26_drive_0035_sync\image_00\data'
    )
    window.show()
    sys.exit(app.exec())
