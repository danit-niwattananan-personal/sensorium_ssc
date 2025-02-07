# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test für die Sequenzauswahl."""

import asyncio
import os
from collections.abc import Generator
from unittest.mock import patch

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.engine.ordner import ButtonPanel
from sensorium.engine.visualization_gui import VisualisationGui


@pytest.fixture
def _event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Asyncio event loop is running."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_ordner(qtbot: QtBot) -> None:
    """Testet ordner."""
    vizualisation = VisualisationGui()
    ordner = ButtonPanel(vizualisation)
    qtbot.add_widget(ordner)
    with patch('sensorium.engine.ordner.ButtonPanel.update_seq') as mock_update_seq:
        qtbot.mouseClick(ordner.button, Qt.LeftButton)  # type: ignore[attr-defined]
        await asyncio.sleep(0)
        mock_update_seq.assert_called_once()


@pytest.mark.usefixtures('_event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_update_seq(qtbot: QtBot) -> None:
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
        await asyncio.sleep(0)
        assert vizualisation.seq_id == 15
        assert vizualisation.framenumber == 0
        mock_update_frame.assert_called_once_with(0)
