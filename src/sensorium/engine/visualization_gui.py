# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""."""

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from sensorium.visualization.camera_visualization import CameraWidget
from sensorium.visualization.lidar_visualization import PointcloudVis
from sensorium.visualization.trajectory_visualization import Trajectory


class VisualisationGui(QMainWindow):
    """Main GUI that embeds all widgets."""

    def __init__(self) -> None:
        """."""
        super().__init__()
        self.setGeometry(0, 0, 1200, 800)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        grid_layout = QGridLayout()
        controlbar = QHBoxLayout()

        self.framenumber = 0
        self.play_en = False
        self.seq_id = 0

        self.camera = CameraWidget()
        grid_layout.addWidget(self.camera, 0, 0)

        self.pointcloud = PointcloudVis()
        grid_layout.addWidget(self.pointcloud, 0, 1)

        self.trajectory = Trajectory()
        grid_layout.addWidget(self.trajectory, 1, 0)

        self.placeholder = QLabel('Platzhalter')
        grid_layout.addWidget(self.placeholder, 1, 1)

        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.update_scene)
        self.animation_timer.setInterval(1)

        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        self.frame_label = QLabel(f'Frame: {self.framenumber}')
        main_layout.addWidget(self.frame_label)

        button_minus10 = QPushButton('-10 Frames')
        button_minus10.clicked.connect(lambda: self.update_frame(-10))
        controlbar.addWidget(button_minus10)

        button_minus1 = QPushButton('-1 Frame')
        button_minus1.clicked.connect(lambda: self.update_frame(-1))
        controlbar.addWidget(button_minus1)

        self.button_play_stop = QPushButton('Play')
        self.button_play_stop.clicked.connect(self.toggle_play_stop)
        controlbar.addWidget(self.button_play_stop)

        button_plus1 = QPushButton('+1 Frame')
        button_plus1.clicked.connect(lambda: self.update_frame(1))
        controlbar.addWidget(button_plus1)

        button_plus10 = QPushButton('+10 Frames')
        button_plus10.clicked.connect(lambda: self.update_frame(10))
        controlbar.addWidget(button_plus10)

        main_layout.addLayout(grid_layout)
        main_layout.addLayout(controlbar)

        self.update_scene()
        self.animation_timer.start()

    def update_frame(self, frame: int) -> None:
        """Erhöht und senkt die Framenummer."""
        self.framenumber += frame
        self.framenumber = max(self.framenumber, 0)
        self.framenumber = min(self.framenumber, 100)
        self.frame_label.setText(f'Frame: {self.framenumber}')
        if self.framenumber == 100:
            self.framenumber = 0

    def toggle_play_stop(self) -> None:
        """Funktion die dem Play Button eine Funktion gibt."""
        self.play_en = not self.play_en
        if self.play_en:
            self.button_play_stop.setText('Play')
            window.animation_timer.stop()
        else:
            self.button_play_stop.setText('Stop')
            window.animation_timer.start()

    def update_scene(self) -> None:
        """Ladet neue Bilder."""
        CameraWidget.show_image(self.camera, self.framenumber)
        Trajectory.draw_line(self.trajectory, self.framenumber)
        PointcloudVis.update_scene(self.pointcloud, self.framenumber)
        self.placeholder.setText(f'Das ist der neue Frame: {self.framenumber}')
        self.update_frame(1)


if __name__ == '__main__':
    app = QApplication([])
    window = VisualisationGui()
    window.show()
    app.exec()
