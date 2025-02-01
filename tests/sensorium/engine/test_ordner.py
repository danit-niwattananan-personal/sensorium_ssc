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
def test_update_scene(qtbot: QtBot) -> None:
    """Testet update_scene."""
    vizualisation = VisualisationGui()
    ordner = ButtonPanel(vizualisation)

    qtbot.addWidget(ordner)
    with patch('sensorium.engine.ordner.ButtonPanel.update_seq') as mock_update_seq:
        qtbot.mouseClick(ordner.button, Qt.LeftButton) # type: ignore[attr-defined]
        mock_update_seq.assert_called_once()


