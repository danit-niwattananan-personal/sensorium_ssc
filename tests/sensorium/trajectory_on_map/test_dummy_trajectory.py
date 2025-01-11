# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Trajectory Visualization."""

from unittest.mock import mock_open, patch

from PySide6 import QtGui, QtWidgets

from sensorium.trajectory_on_map.dummy_trajectory import Trajectory


def test_draw_line() -> None:
    """Test if draw_line adds a QGraphicsLineItem when previous_point is not None."""
    # Mock file reading
    with patch(
        'pathlib.Path.open',
        mock_open(read_data='{"x": 0, "y": 0, "z": 0}\n{"x": 1, "y": 1, "z": 1}\n'),
    ):
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])  # Create QApplication
        widget = Trajectory()  # Create the widget

        widget.previous_point = [0, 0]
        print(widget.previous_point[0], widget.previous_point[1])

        widget.frame_number = 1
        widget.view = QtWidgets.QGraphicsView()
        widget.scene = QtWidgets.QGraphicsScene()
        widget.view.setScene(widget.scene)

        scale_factor = 1
        coords = widget.coordinates[:, :2] * scale_factor
        current_point = coords[widget.frame_number]
        print(current_point[0], current_point[1])

        widget.current_position_marker = widget.scene.addEllipse(
            0,
            0,
            0,
            0,
            QtGui.QPen(QtGui.QColor(255, 0, 0)),
            QtGui.QBrush(QtGui.QColor(255, 0, 0)),
        )

        widget.draw_line()

        items = widget.scene.items()
        print(items)

        assert len(items) > 0
        app.quit()
