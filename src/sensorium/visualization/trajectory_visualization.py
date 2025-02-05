# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Visualization of the Trajectory of the car."""

import json
from pathlib import Path

import numpy as np
from PySide6 import QtGui, QtWidgets

from sensorium.communication.client_comm import get_trajectory_data


class Trajectory(QtWidgets.QWidget):
    """Widget for visualizing the trajectory of the car."""

    def __init__(self) -> None:
        """Initializes the Trajectory widget.

        Returns:
            None.
        """
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
        self.current_sequence_id = 0

        self.current_position_marker = self.scene.addEllipse(
            0,
            0,
            0,
            0,
            QtGui.QPen(QtGui.QColor(255, 0, 0)),
            QtGui.QBrush(QtGui.QColor(255, 0, 0)),
        )

    def get_coordinates(self) -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
        """Get the coordinates from a trajectory.json or .txt file.

        Returns:
            An Array of the coordinates of the trajectory.

        Note: This function is not used in the current implementation.
        It is for testing on a local machine without the server.
        """
        with Path(self.trajectory_file_path).open() as f:
            coord_dict = [json.loads(line.strip()) for line in f]
        x = np.array([coord['x'] for coord in coord_dict])
        y = np.array([coord['y'] for coord in coord_dict])
        z = np.array([coord['z'] for coord in coord_dict])
        return np.column_stack((x, y, z))

    async def draw_line(self, seq_id: int, frame_id: int) -> None:
        """Visualizing the Trajectory of the car.

        Draws a line between the points pf the previous time frame and the current time frame
        and updates a marker representing the current position of the car
        relative to the starting point.

        Args:
            seq_id: The sequence number.
            frame_id: The frame number.

        Returns:
            None.
        """
        # If sequence is changed, reset the previous point anc clear all lines
        is_sequence_changed = seq_id != self.current_sequence_id
        if is_sequence_changed:
            self.current_sequence_id = seq_id
            self.previous_point = np.zeros(3)
            self.last_frame = 0
            self.scene.clear()
        scale_factor = 1
        coords = await get_trajectory_data(seq_id, frame_id)
        current_point = coords * scale_factor
        current_point[1] = -current_point[1]  # Mirror the y axis
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

        if self.current_position_marker and not is_sequence_changed:
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

        self.current_sequence_id = seq_id


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Trajectory()
    window.trajectory_file_path = Path(r'C:\Users\wich_\Desktop\trajectory.txt')
    window.show()
    app.exec()
