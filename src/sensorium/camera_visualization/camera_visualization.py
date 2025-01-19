# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera Visualization."""

import sys

import cv2  # noqa: F401
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
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
        scale_factor = 0.3
        width = int(self._width * scale_factor)
        height = int(self._height * scale_factor)
        self.setWindowTitle('Video')
        self.setGeometry(100, 100, width, height)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

    def show_image(self, frame_id: int) -> None:
        """."""
        pixmap = QPixmap(f'{self.img_directory}/{frame_id:010d}.png')

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
