# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Visualization of the Trajectory of the car."""

import json
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PySide6 import QtGui, QtWidgets

# from sensorium.launch.launch import LaunchWindow  # noqa: ERA001


class Trajectory(QtWidgets.QWidget):
    """."""

    # def __init__(self, launch_window: LaunchWindow) -> None:
    def __init__(self) -> None:
        """Initialize the Trajectory widget."""
        super().__init__(None)
        self.resize(500, 500)
        # self.launch_window = launch_window  # noqa: ERA001
        self.view = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.trajectory_file_path = Path()
        print(self.trajectory_file_path)

        self.previous_point = np.zeros(3)
        self.last_frame = 0

        self.current_position_marker = self.scene.addEllipse(
            0,
            0,
            0,
            0,
            QtGui.QPen(QtGui.QColor(255, 0, 0)),
            QtGui.QBrush(QtGui.QColor(255, 0, 0)),
        )

    def get_coordinates(self) -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
        """."""
        with Path(self.trajectory_file_path).open() as f:
            coord_dict = [json.loads(line.strip()) for line in f]
        x = np.array([coord['x'] for coord in coord_dict])
        y = np.array([coord['y'] for coord in coord_dict])
        z = np.array([coord['z'] for coord in coord_dict])
        return np.column_stack((x, y, z))

    # def get_traj_data(
    #     self, frame_id: int, seq_id: int
    # ) -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
    #     """."""
    #     data_list = self.launch_window.get_traj_data(frame_id, seq_id)  # noqa: ERA001
    #     x = data_list['x']  # noqa: ERA001
    #     y = data_list['y']  # noqa: ERA001
    #     z = data_list['z']  # noqa: ERA001
    #     return np.column_stack((x, y, z))  # noqa: ERA001

    def draw_line(self, xyz: NDArray[np.float64], frame_id: int) -> None:
        """."""
        scale_factor = 1
        current_point = xyz * scale_factor
        current_point[1] = -current_point[1] # Mirror the y axis
        if self.previous_point is not None and frame_id == self.last_frame + 1:
            pen = QtGui.QPen(QtGui.QColor(100, 100, 200), 1)
            line = QtWidgets.QGraphicsLineItem(
                self.previous_point[0],
                self.previous_point[1],
                current_point[0],
                current_point[1],
            )
            line.setPen(pen)
            self.scene.addItem(line)
        self.previous_point = current_point
        self.last_frame = frame_id

        if self.current_position_marker:
            self.scene.removeItem(self.current_position_marker)

        circle_radius = 2
        self.current_position_marker = self.scene.addEllipse(
            current_point[0] - circle_radius,
            current_point[1] - circle_radius,
            circle_radius * 2,
            circle_radius * 2,
            QtGui.QPen(QtGui.QColor(255, 0, 0)),
            QtGui.QBrush(QtGui.QColor(255, 0, 0)),
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Trajectory()
    window.trajectory_file_path = Path(r'C:\Users\wich_\Desktop\trajectory.txt')
    window.show()
    app.exec()
