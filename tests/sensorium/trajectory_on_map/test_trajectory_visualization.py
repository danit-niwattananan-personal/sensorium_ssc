# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Trajectory Visualization."""

from unittest.mock import mock_open, patch

import numpy as np
from PySide6 import QtGui, QtWidgets

from sensorium.visualization.trajectory_visualization import Trajectory


def test_draw_line() -> None:
    """."""
    with patch(
        'pathlib.Path.open',
        mock_open(read_data='{"x": 0, "y": 0, "z": 0}\n{"x": 1, "y": 1, "z": 1}\n'),
    ):
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        widget = Trajectory()

        widget.previous_point = np.array([0, 0], dtype=np.float64)

        widget.view = QtWidgets.QGraphicsView()
        widget.scene = QtWidgets.QGraphicsScene()
        widget.view.setScene(widget.scene)

        widget.current_position_marker = widget.scene.addEllipse(
            0,
            0,
            0,
            0,
            QtGui.QPen(QtGui.QColor(255, 0, 0)),
            QtGui.QBrush(QtGui.QColor(255, 0, 0)),
        )
        frame_id = 0
        widget.draw_line(frame_id)
        assert len(widget.scene.items()) == 2
    app.quit()
