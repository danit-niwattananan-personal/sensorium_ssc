# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Visualization of the Trajectory of the car."""

import json
from pathlib import Path

import numpy as np
from PySide6 import QtGui, QtWidgets

# from sensorium.launch.launch import get_traj_data # noqa: ERA001


class Trajectory(QtWidgets.QWidget):
    """."""

    def __init__(self) -> None:
        """Initialize the Trajectory widget."""
        super().__init__(None)
        self.resize(500, 500)
        self.view = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)

        self.frame_number = 0
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.trajectory_file_path = ''
        print(self.trajectory_file_path)

        self.previous_point = np.zeros(3)

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

    def draw_line(self, frame_id: int) -> None:
        """."""
        # coords = get_traj_data(frame_id, seq_id)# noqa: ERA001
        coords = self.get_coordinates()
        scale_factor = 1
        coords = coords * scale_factor
        current_point = coords[frame_id]
        if self.previous_point is not None:
            pen = QtGui.QPen(QtGui.QColor(100, 100, 200), 1)
            line = QtWidgets.QGraphicsLineItem(
                self.previous_point[0],
                self.previous_point[1],
                current_point[0],
                current_point[1],
            )
            line.setPen(pen)
            self.scene.addItem(line)

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

        self.previous_point = current_point
        self.frame_number += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Trajectory()
    window.trajectory_file_path = r'C:\Users\wich_\Desktop\trajectory.txt'
    window.show()
    app.exec()
