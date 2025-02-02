# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""."""

import asyncio
import sys
import time
from pathlib import Path

import yaml
from PySide6 import QtCore
from PySide6.QtGui import QResizeEvent
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

from sensorium.data_processing.engine.backend_engine import BackendEngine
from sensorium.visualization.camera_visualization import CameraWidget
from sensorium.visualization.lidar_visualization import PointcloudVis
from sensorium.visualization.trajectory_visualization import Trajectory
from sensorium.visualization.voxel_widget import VoxelWidget


class VisualisationGui(QMainWindow):
    """Main GUI that embeds all widgets."""

    def __init__(self) -> None:
        """Initialize the GUI."""
        super().__init__()
        self.setGeometry(0, 0, 1300, 910)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.grid_layout = QGridLayout()
        controlbar = QHBoxLayout()

        self._read_config()
        self._init_variables()
        self._setup_widgets()
        self.frame_label = QLabel(
            f'Frame: {self.framenumber}, Sequence: {self.seq_id} und FPS: {self.fps}'  # type: ignore[has-type]
        )
        main_layout.addWidget(self.frame_label)

        self.button_minus10 = QPushButton('-10 Frames')
        self.button_minus10.clicked.connect(lambda: asyncio.create_task(self.update_frame(-10)))
        controlbar.addWidget(self.button_minus10)

        self.button_minus1 = QPushButton('-1 Frame')
        self.button_minus1.clicked.connect(lambda: asyncio.create_task(self.update_frame(-1)))
        controlbar.addWidget(self.button_minus1)

        self.button_play_stop = QPushButton('Play')
        self.button_play_stop.clicked.connect(lambda: asyncio.create_task(self.toggle_play_stop()))
        controlbar.addWidget(self.button_play_stop)

        self.button_plus1 = QPushButton('+1 Frame')
        self.button_plus1.clicked.connect(lambda: asyncio.create_task(self.update_frame(1)))
        controlbar.addWidget(self.button_plus1)

        self.button_plus10 = QPushButton('+10 Frames')
        self.button_plus10.clicked.connect(lambda: asyncio.create_task(self.update_frame(10)))
        controlbar.addWidget(self.button_plus10)

        self._grid_layout()
        main_layout.addLayout(self.grid_layout)

        self.slider = QSlider(QtCore.Qt.Horizontal)  # type: ignore[attr-defined]
        self.slider.setRange(0, self.maxframe)  # type: ignore[has-type]
        self.slider.setValue(0)
        self.slider.valueChanged.connect(lambda: asyncio.create_task(self.set_frame_slider()))
        main_layout.addWidget(self.slider)
        main_layout.addLayout(controlbar)

        self.animation_timer.stop()  # type: ignore[has-type]
        self.loading_frame = False
        self._update_scene_lock = asyncio.Lock()

    def _init_variables(self) -> None:
        """Initialize the variables to reduce number of lines in init method."""
        self.maxframe = int(self.config['frontend_engine']['max_frame'])
        self.framenumber = 0
        self.play_en = False
        self.seq_id = 0
        self.next_frame_time = int(self.config['frontend_engine']['next_frame_time'])
        self.fps = int(1000 / self.next_frame_time)
        self.loading_frame = False

    def _setup_widgets(self) -> None:
        """Setup the widgets."""
        # Initialize data loader
        self.backend_engine = BackendEngine(data_dir=self.config['backend_engine']['data_dir'])

        self._setup_camera_widget()
        self.grid_layout.addLayout(self.camera, 0, 0)

        self.pointcloud = PointcloudVis()
        self.grid_layout.addWidget(self.pointcloud, 0, 1)

        self.trajectory = Trajectory()
        self.trajectory.trajectory_file_path = Path(
            self.config['frontend_engine_rw']['trajectory_dir']
        )
        self.grid_layout.addWidget(self.trajectory, 1, 0)

        self.voxel = VoxelWidget()
        self.grid_layout.addWidget(self.voxel, 1, 1)

        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.timer_callback)
        self.animation_timer.setInterval(self.next_frame_time)

    async def set_frame_slider(self) -> None:
        """Sets the Frame if slider is moved."""
        self.framenumber = self.slider.value()
        self.frame_label.setText(
            f'Frame: {self.framenumber}, Sequence: {self.seq_id} und FPS: {self.fps}'
        )
        if self.play_en is True:
            await self.load_frame(self.seq_id, self.framenumber)

    def _grid_layout(self) -> None:
        """Sets the layout of the grid_layout."""
        self.grid_layout.setColumnMinimumWidth(0, 300)
        self.grid_layout.setColumnMinimumWidth(1, 500)
        self.grid_layout.setRowMinimumHeight(0, 400)
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
        self.camera2 = CameraWidget(camera_id='camera2')  # left
        self.camera3 = CameraWidget(camera_id='camera3')  # right
        self.label2 = QLabel('Left camera')
        self.label3 = QLabel('Right camera')
        self.camera = QVBoxLayout()
        self.camera.addWidget(self.camera2)
        self.camera.addWidget(self.label2)
        self.camera.addWidget(self.camera3)
        self.camera.addWidget(self.label3)

    async def update_frame(self, frame: int) -> None:
        """Erhöht und senkt die Framenummer."""
        self.framenumber += frame
        self.framenumber = max(self.framenumber, 0)
        self.framenumber = min(self.framenumber, self.maxframe)
        self.frame_label.setText(
            f'Frame: {self.framenumber}, Sequence: {self.seq_id} und FPS: {self.fps}'
        )
        if self.framenumber == self.maxframe:
            self.framenumber = 0
        self.slider.setValue(self.framenumber)
        if self.play_en is True:
            await self.load_frame(self.seq_id, self.framenumber)

    async def toggle_play_stop(self) -> None:
        """Funktion die dem Play Button eine Funktion gibt."""
        self.play_en = not self.play_en
        if self.play_en:
            self.button_play_stop.setText('Play')
            self.animation_timer.stop()
        else:
            self.button_play_stop.setText('Stop')
            self.animation_timer.start()

    async def update_scene(self) -> None:
        """Ladet neue Bilder."""
        async with self._update_scene_lock:
            await self.load_frame(self.seq_id, self.framenumber)
            await self.update_frame(1)

    async def load_frame(self, seq_id: int, frame_id: int) -> None:
        """Ladet aktuelle Bilder."""
        if self.loading_frame:
            return
        self.loading_frame = True

        print(f'[{time.time()}] process_frame started for frame {self.framenumber}')

        try:
            await asyncio.gather(
                self.camera2.show_image(seq_id, frame_id),
                self.camera3.show_image(seq_id, frame_id),
                self.trajectory.draw_line(seq_id, frame_id),
                self.pointcloud.update_scene(seq_id, frame_id),
                self.voxel.update_scene(seq_id, frame_id),
            )
        except (RuntimeError, ValueError) as e:
            print(f'Error in process_frame: {e}')

        self.loading_frame = False

    def timer_callback(self) -> None:
        """Callback function for the timer."""
        if not self._update_scene_lock.locked():
            asyncio.create_task(self.update_scene())  # noqa: RUF006
        else:
            print('Update in progress; skipping new update.')

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        """If Window size changes, change Widget size."""
        new_size = event.size()
        print(f'{new_size}')
        self.camera2.setGeometry(0, 0, int(new_size.width() / 2), int(new_size.height() / 4 - 10))
        self.camera2.label.setGeometry(
            0, 0, int(new_size.width() / 2), int(new_size.height() / 4 - 10)
        )
        self.camera3.setGeometry(0, 0, int(new_size.width() / 2), int(new_size.height() / 4 - 10))
        self.camera3.label.setGeometry(
            0, 0, int(new_size.width() / 2), int(new_size.height() / 4 - 10)
        )
        self.load_frame(self.seq_id, self.framenumber)
        return super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    window = VisualisationGui()
    window.show()
    app.exec()  # type: ignore[union-attr]
