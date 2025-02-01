# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Trajectory Visualization."""

import numpy as np
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.visualization.trajectory_visualization import Trajectory


def test_draw_line(qtbot: QtBot) -> None:
    """."""
    mock_data = np.array([1, 1, 1], dtype=np.float64)
    widget = Trajectory()
    qtbot.addWidget(widget)

    widget.previous_point = np.array([0, 0, 0], dtype=np.float32)

    widget.draw_line(xyz=mock_data, frame_id=1, sequence_id=0)

    assert len(widget.scene.items()) == 2

    current_marker = widget.scene.items()[0]
    assert isinstance(current_marker, QtWidgets.QGraphicsEllipseItem)
    assert current_marker.rect().center() == QtCore.QPointF(1, -1)

    line = widget.scene.items()[1]
    assert isinstance(line, QtWidgets.QGraphicsLineItem)
    assert line.line().p1() == QtCore.QPointF(0, 0)
    assert line.line().p2() == QtCore.QPointF(1, -1)
