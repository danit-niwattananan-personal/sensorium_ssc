# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera Visualization."""

import sys

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from sensorium.communication.client_comm import get_camera2_data, get_camera3_data

CAMERA2_SHAPE = (375, 1242, 3)
CAMERA3_SHAPE = (375, 1242, 3)


class CameraWidget(QMainWindow):
    """Widget fo Visualizing camera data."""

    def __init__(self, camera_id: str) -> None:
        """Initializes the Camera Widget."""
        super().__init__()
        self.img_directory = ''
        self.camera_id = camera_id
        self._height, self._width = 375, 1242
        self.setup_lable()

    def setup_lable(self) -> None:
        """Setup up the lable required to display the image."""
        scale_factor = 1
        width = self._width
        height = int(self._height * scale_factor)
        self.setWindowTitle('Video')
        self.setGeometry(100, 100, width, height)  # NOTE: make it scalable
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

    async def show_image(self, seq_id: int, frame_id: int) -> None:
        """Creates an image from the raw data of the according frame and shows it in the label.

        Args:
            seq_id: Sequence number.
            frame_id: Frame number.
        """
        if self.camera_id == 'camera2':
            raw_data = await get_camera2_data(seq_id, frame_id)
            image = raw_data.reshape(CAMERA2_SHAPE).astype(np.uint8)
        elif self.camera_id == 'camera3':
            raw_data = await get_camera3_data(seq_id, frame_id)
            image = raw_data.reshape(CAMERA3_SHAPE).astype(np.uint8)
        else:
            message = 'Invalid camera_id'
            raise ValueError(message)

        image = np.ascontiguousarray(image)
        rgb_array = np.ascontiguousarray(image[..., ::-1])
        height, width, channels = rgb_array.shape
        bytes_per_line = channels * width
        qimage = QImage(
            rgb_array.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
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
    window = CameraWidget(camera_id='camera2')
    window.img_directory = (
        r'C:\Users\wich_\Desktop\2011_09_26\2011_09_26_drive_0035_sync\image_00\data'
    )
    window.show()
    sys.exit(app.exec())
