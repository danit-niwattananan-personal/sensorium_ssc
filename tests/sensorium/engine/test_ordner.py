# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test für die Sequenzauswahl."""

import os
from unittest.mock import patch

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]

from sensorium.engine.ordner import ButtonPanel
from sensorium.engine.visualization_gui import VisualisationGui


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_ordner(qtbot: QtBot) -> None:
    """Testet ordner."""
    vizualisation = VisualisationGui()
    ordner = ButtonPanel(vizualisation)
    qtbot.addWidget(ordner)

    with patch('sensorium.engine.ordner.ButtonPanel.update_seq') as mock_update_seq:
        qtbot.mouseClick(ordner.button, Qt.LeftButton)  # type: ignore[attr-defined]
        mock_update_seq.assert_called_once()


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_update_seq(qtbot: QtBot) -> None:
    """Testet ordner."""
    vizualisation = VisualisationGui()
    ordner = ButtonPanel(vizualisation)
    qtbot.add_widget(ordner)

    with patch(
        'sensorium.engine.visualization_gui.VisualisationGui.update_frame'
    ) as mock_update_frame:
        vizualisation.seq_id = 4
        vizualisation.framenumber = 10
        qtbot.mouseClick(ordner.button, Qt.LeftButton)  # type: ignore[attr-defined]
        assert vizualisation.seq_id == 9
        assert vizualisation.framenumber == 0
        mock_update_frame.assert_called_once_with(0)
