# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Trajectory Visualization."""

from typing import cast
from unittest.mock import patch

import numpy as np
import pytest
from numpy.typing import NDArray
from PySide6 import QtCore, QtWidgets
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.visualization.trajectory_visualization import Trajectory


def mock_get_traj(seq_id: int, frame_id: int) -> NDArray[np.float64]:
    """Mock get_trajectory_data function form client_comm.

    Args:
        seq_id: Sequence number.
        frame_id: Frame number.

    Returns:
        The mock data for the given frame_id.
    """
    _ = seq_id
    mock_data = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]], dtype=np.float64)
    data = mock_data[frame_id]
    return cast(NDArray[np.float64], data)


@pytest.mark.asyncio
async def test_draw_line(qtbot: QtBot) -> None:
    """Test draw_line method of Trajectory widget.

    Args:
        qtbot: Fixture to interact with widget.

    Returns:
        None.
    """
    with patch(
        'sensorium.visualization.trajectory_visualization.get_trajectory_data',
        side_effect=mock_get_traj,
    ):
        widget = Trajectory()
        qtbot.addWidget(widget)

        await widget.draw_line(seq_id=0, frame_id=0)

        assert len(widget.scene.items()) == 1

        marker = widget.scene.items()[0]
        assert isinstance(marker, QtWidgets.QGraphicsEllipseItem)
        assert marker.rect().center() == QtCore.QPointF(0, 0)

        await widget.draw_line(seq_id=0, frame_id=1)

        assert len(widget.scene.items()) == 2

        marker = widget.scene.items()[0]
        assert isinstance(marker, QtWidgets.QGraphicsEllipseItem)
        assert marker.rect().center() == QtCore.QPointF(1, -1)

        line = widget.scene.items()[1]
        assert isinstance(line, QtWidgets.QGraphicsLineItem)
        assert line.line().p1() == QtCore.QPointF(0, 0)
        assert line.line().p2() == QtCore.QPointF(1, -1)

        await widget.draw_line(seq_id=0, frame_id=2)
        assert len(widget.scene.items()) == 3

        marker = widget.scene.items()[0]
        assert isinstance(marker, QtWidgets.QGraphicsEllipseItem)
        assert marker.rect().center() == QtCore.QPointF(2, -2)

        line = widget.scene.items()[1]
        assert isinstance(line, QtWidgets.QGraphicsLineItem)
        assert line.line().p1() == QtCore.QPointF(1, -1)
        assert line.line().p2() == QtCore.QPointF(2, -2)

        widget.last_frame = 100
        await widget.draw_line(seq_id=0, frame_id=2)

        assert len(widget.scene.items()) == 3

        marker = widget.scene.items()[0]
        assert isinstance(marker, QtWidgets.QGraphicsEllipseItem)
        assert marker.rect().center() == QtCore.QPointF(2, -2)

        await widget.draw_line(seq_id=1, frame_id=0)

        assert len(widget.scene.items()) == 1

        marker = widget.scene.items()[0]
        assert isinstance(marker, QtWidgets.QGraphicsEllipseItem)
        assert marker.rect().center() == QtCore.QPointF(0, -0)

        expected_previous_point = np.array([0, 0, 0], dtype=np.float64)
        assert np.array_equal(widget.previous_point, expected_previous_point)
        assert widget.last_frame == 0
        assert widget.current_sequence_id == 1
