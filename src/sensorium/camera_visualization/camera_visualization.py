# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera Visualization."""

import sys

import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    """."""

    def __init__(self) -> None:
        """."""
        super().__init__()
        self.img_directory = (
            r'C:\Users\wich_\Desktop\2011_09_26\2011_09_26_drive_0035_sync\image_00\data'
        )
        sample_img = cv2.imread(self.img_directory + '/' + '0000000000.png')
        height, width = sample_img.shape[:2]

        scale_factor = 0.5
        width = int(width * scale_factor)
        height = int(height * scale_factor)
        self.setWindowTitle('Video')
        self.setGeometry(100, 100, width, height)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)
        self.frame_number = 0

    def request_image_array(self) -> None:
        """."""

    def update_image(self) -> None:
        """."""
        pixmap = QPixmap(self.img_directory + '/' + f'{self.frame_number:010d}.png')
        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )
        )

        self.frame_number += 1


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
