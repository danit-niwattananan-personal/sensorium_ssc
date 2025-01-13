# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera Visualization."""

import sys

import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class CameraWidget(QMainWindow):
    """."""

    def __init__(self) -> None:
        """."""
        super().__init__()
        self.img_directory = (
            r'C:\Users\wich_\Desktop\2011_09_26\2011_09_26_drive_0035_sync\image_00\data'
        )
        sample_img = cv2.imread(self.img_directory + '/' + '0000000000.png')
        self._height, self._width = sample_img.shape[:2]

        self.setup_lable()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)
        self.frame_id = 0

    def request_image_array(
        self, frame_id: int, seg_id: int, data_mode: int
    ) -> tuple[int, int, int]:
        """."""
        return seg_id, frame_id, data_mode

    def setup_lable(self) -> None:
        """."""
        scale_factor = 0.3
        width = int(self._width * scale_factor)
        height = int(self._height * scale_factor)
        self.setWindowTitle('Video')
        self.setGeometry(100, 100, width, height)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

    def update_image(self) -> None:
        """."""
        pixmap = QPixmap(self.img_directory + '/' + f'{self.frame_id:010d}.png')
        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )
        )

        self.frame_id += 1

        if self.frame_id == 100:
            self.frame_id = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWidget()
    window.show()
    sys.exit(app.exec())
