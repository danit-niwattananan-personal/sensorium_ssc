# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Voxel Visualization class."""

import sys
from pathlib import Path

import numpy as np
import yaml
from cv2.typing import MatLike
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget

from sensorium.data_processing.engine.backend_engine import BackendEngine
from sensorium.visualizer.voxel_viz.helper import draw_semantic_voxel


class VoxelWidget(QMainWindow):
    """Mayavi PyQt wrapper for voxel visualization window."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """."""
        super().__init__(parent)

        # First, get all necessary data. Must change this to call COMM func instead
        config_path = Path.cwd() / 'configs' / 'sensorium.yaml'
        with Path(config_path).open() as stream:
            backend_config = yaml.safe_load(stream)
        backend_engine = BackendEngine(data_dir=backend_config['backend_engine']['data_dir'])
        data = backend_engine.process(sequence_id=0, frame_id=0)

        voxel_img = draw_semantic_voxel(
            voxels=data['voxel'],  # type: ignore[arg-type]
            cam_pose=data['t_velo_2_cam'],  # type: ignore[arg-type]
            vox_origin=np.array([0, -25.6, -2]),
            fov_mask=data['fov_mask'],  # type: ignore[arg-type]
        )
        height, width = voxel_img.shape[:2]

        scale_factor = 0.5
        width = int(width * scale_factor)
        height = int(height * scale_factor)
        self.setWindowTitle('Voxel Ground Truth')
        self.setGeometry(100, 100, width, height)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_scene)
        self.timer.start(100)
        self.frame_number = 0

    def update_scene(self, img: MatLike) -> None:
        """Update the scene with the new image and show to the user."""
        pixmap = QPixmap(img)
        self.label.setPixmap(
            pixmap.scaled(
                self.label.width(),
                self.label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )
        )

        self.frame_number += 1


def main() -> None:
    """Main function."""

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance
    window = VoxelWidget()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
