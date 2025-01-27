# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""."""

import sys
from pathlib import Path

import yaml
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from sensorium.visualization.camera_visualization import CameraWidget
from sensorium.visualization.lidar_visualization import PointcloudVis
from sensorium.visualization.trajectory_visualization import Trajectory
from sensorium.visualization.voxel_widget import VoxelWidget


class VisualisationGui(QMainWindow):
    """Main GUI that embeds all widgets."""

    def __init__(self) -> None:
        """Initialize the GUI."""
        super().__init__()
        self.setGeometry(0, 0, 900, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.maxframe = 10
        main_layout = QVBoxLayout(central_widget)

        self.grid_layout = QGridLayout()
        controlbar = QHBoxLayout()

        self._init_variables()
        self._read_config()

        self._setup_camera_widget()
        self.grid_layout.addLayout(self.camera, 0, 0)

        self.pointcloud = PointcloudVis()
        self.pointcloud.directory = Path(self.config['frontend_engine_rw']['pointcloud_dir'])
        self.grid_layout.addWidget(self.pointcloud, 0, 1)

        self.trajectory = Trajectory()
        self.trajectory.trajectory_file_path = Path(
            self.config['frontend_engine_rw']['trajectory_dir']
        )
        self.grid_layout.addWidget(self.trajectory, 1, 0)

        self.voxel = VoxelWidget()
        self.grid_layout.addWidget(self.voxel, 1, 1)

        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.update_scene)
        self.animation_timer.setInterval(self.next_frame_time)

        self.frame_label = QLabel(
            f'Frame: {self.framenumber}, Sequence: {self.seq_id} und FPS: {self.fps}'
        )
        main_layout.addWidget(self.frame_label)

        self.button_minus10 = QPushButton('-10 Frames')
        self.button_minus10.clicked.connect(lambda: self.update_frame(-10))
        controlbar.addWidget(self.button_minus10)

        self.button_minus1 = QPushButton('-1 Frame')
        self.button_minus1.clicked.connect(lambda: self.update_frame(-1))
        controlbar.addWidget(self.button_minus1)

        self.button_play_stop = QPushButton('Play')
        self.button_play_stop.clicked.connect(self.toggle_play_stop)
        controlbar.addWidget(self.button_play_stop)

        self.button_plus1 = QPushButton('+1 Frame')
        self.button_plus1.clicked.connect(lambda: self.update_frame(1))
        controlbar.addWidget(self.button_plus1)

        self.button_plus10 = QPushButton('+10 Frames')
        self.button_plus10.clicked.connect(lambda: self.update_frame(10))
        controlbar.addWidget(self.button_plus10)

        self._grid_layout()
        main_layout.addLayout(self.grid_layout)

        self.slider = QSlider(QtCore.Qt.Horizontal)  # type: ignore[attr-defined]
        self.slider.setRange(0, self.maxframe)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(lambda: self.set_frame_slider())
        main_layout.addWidget(self.slider)
        main_layout.addLayout(controlbar)

        self.animation_timer.stop()

    def _init_variables(self) -> None:
        """Initialize the variables to reduce number of lines in init method."""
        self.framenumber = 0
        self.play_en = False
        self.seq_id = 0
        self.next_frame_time = 1000
        self.fps = int(1000 / self.next_frame_time)

    def set_frame_slider(self) -> None:
        """Sets the Frame if slider is moved."""
        self.framenumber = self.slider.value()
        self.frame_label.setText(
            f'Frame: {self.framenumber}, Sequence: {self.seq_id} und FPS: {self.fps}'
        )

    def _grid_layout(self) -> None:
        """self.grid_layout."""
        self.grid_layout.setColumnMinimumWidth(0, 300)
        self.grid_layout.setColumnMinimumWidth(1, 500)
        self.grid_layout.setRowMinimumHeight(0, 230)
        self.grid_layout.setRowMinimumHeight(1, 400)

        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 0)

    def _read_config(self) -> None:
        """Read the config file for path findings during runtime data reading."""
        config_path = Path.cwd() / 'configs' / 'sensorium.yaml'
        with Path(config_path).open() as stream:
            self.config = yaml.safe_load(stream)

    def _setup_camera_widget(self) -> None:
        """Setup the camera widget."""
        self.camera1 = CameraWidget()
        self.camera1.img_directory = self.config['frontend_engine_rw']['img2_dir']
        self.camera2 = CameraWidget()
        self.camera2.img_directory = self.config['frontend_engine_rw']['img3_dir']

        self.camera = QVBoxLayout()
        self.camera.addWidget(self.camera2)
        self.camera.addWidget(self.camera1)

    def update_frame(self, frame: int) -> None:
        """Erhöht und senkt die Framenummer."""
        self.framenumber += frame
        self.framenumber = max(self.framenumber, 0)
        self.framenumber = min(self.framenumber, self.maxframe)
        self.frame_label.setText(
            f'Frame: {self.framenumber}, Sequence: {self.seq_id} und FPS: {self.fps}'
        )
        if self.framenumber == 100:
            self.framenumber = 0
        self.slider.setValue(self.framenumber)

    def toggle_play_stop(self) -> None:
        """Funktion die dem Play Button eine Funktion gibt."""
        self.play_en = not self.play_en
        if self.play_en:
            self.button_play_stop.setText('Play')
            self.animation_timer.stop()
        else:
            self.button_play_stop.setText('Stop')
            self.animation_timer.start()

    def update_scene(self) -> None:
        """Ladet neue Bilder."""
        self.camera1.show_image(self.framenumber)
        self.camera2.show_image(self.framenumber)
        self.trajectory.draw_line(self.framenumber)
        self.pointcloud.update_scene(self.framenumber)
        self.voxel.update_scene(self.framenumber, self.seq_id)
        self.update_frame(1)


if __name__ == '__main__':
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    window = VisualisationGui()
    window.show()
    app.exec()  # type: ignore[union-attr]
