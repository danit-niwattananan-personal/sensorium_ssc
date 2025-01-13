# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""."""

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

from sensorium.camera_visualization.camera_visualization import CameraWidget  # noqa: F401
from sensorium.lidar_pointcloud.lidar_visualization import PointcloudVis  # noqa: F401
from sensorium.trajectory_on_map.trajectory_visualization import Trajectory  # noqa: F401


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

        self.framenumber = 1
        self.play_en = False

        # self.camera = CameraWidget()  # noqa: ERA001
        # grid_layout.addWidget(camera, 0, 0)  # noqa: ERA001

        # self.pointcloud = PointcloudVis()  # noqa: ERA001
        # grid_layout.addWidget(pointcloud, 0, 1)  # noqa: ERA001
        # pointcloud.toggle_animation()  # noqa: ERA001

        # self.trajectory = Trajectory()  # noqa: ERA001
        # grid_layout.addWidget(trajectory, 1, 0)  # noqa: ERA001

        # self.placeholder = QLabel('Platzhalter')  # noqa: ERA001
        # grid_layout.addWidget(placeholder, 1, 1)  # noqa: ERA001

        widget1 = QLabel('Widget 1')
        widget2 = QLabel('Widget 2')
        widget3 = QLabel('Widget 3')
        widget4 = QLabel('Widget 4')

        grid_layout.addWidget(widget1, 0, 0)
        grid_layout.addWidget(widget2, 0, 1)
        grid_layout.addWidget(widget3, 1, 0)
        grid_layout.addWidget(widget4, 1, 1)

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

        button_plus10 = QPushButton('+10 Frame')
        button_plus10.clicked.connect(lambda: self.update_frame(10))
        controlbar.addWidget(button_plus10)

        main_layout.addLayout(grid_layout)
        main_layout.addLayout(controlbar)

        self.update_scene()

    def update_frame(self, frame: int) -> None:
        """Erhöht und senkt die Framenummer."""
        self.framenumber += frame
        self.framenumber = max(self.framenumber, 1)
        self.frame_label.setText(f'Frame: {self.framenumber}')

    def toggle_play_stop(self) -> None:
        """Funktion die dem Play Button eine Funktion gibt."""
        self.play_en = not self.play_en
        if self.play_en:
            self.button_play_stop.setText('Stop')
        else:
            self.button_play_stop.setText('Play')
            self.update_scene()

    def update_scene(self) -> None:
        """Ladet neue Bilder."""
        # load_worked = false  # noqa: ERA001
        # if self.play_en:
        # load_worked = CameraWidget.update_image(self.camera, self.framenumber)  # noqa: ERA001
        # load_worked = load_worked or Trajectory.draw_line(self.trajectory, self.framenumber)  # noqa: E501, ERA001
        # load_worked = load worked or PointcloudVis.update_scene(self.pointcloud, self.framenumber)
        # load_worked = load worked or self.placeholder.setText(f'Das ist der neue frame: {frame}')
        # if load_worked:
        # self.update_frame(1)  # noqa: ERA001
        # update_scene(self)  # noqa: ERA001
        # else
        # CameraWidget.update_image(self.camera, self.framenumber)  # noqa: ERA001
        # Trajectory.draw_line(self.trajectory, self.framenumber)  # noqa: ERA001
        # PointcloudVis.update_scene(self.pointcloud, self.framenumber)  # noqa: ERA001
        # self.placeholder.setText(f'Das ist der neue frame: {frame}')  # noqa: ERA001


if __name__ == '__main__':
    app = QApplication([])
    window = VisualisationGui()
    window.show()
    app.exec()
