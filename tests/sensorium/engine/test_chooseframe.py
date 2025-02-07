# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import asyncio
import os
from collections.abc import Generator

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.engine.chooseframe import FrameDialog, SeqDialog
from sensorium.engine.visualization_gui import VisualisationGui


@pytest.fixture
def _event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Asyncio event loop is running."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.mark.usefixtures('event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_chooseframe(qtbot: QtBot) -> None:
    """Testet das chooseframe Fenster mit pytest-qt."""
    vizualisation = VisualisationGui()
    dialog = FrameDialog(vizualisation)
    qtbot.add_widget(vizualisation)

    assert dialog.input_field is not None
    assert dialog.apply_button is not None
    assert dialog.cancel_button is not None

    dialog.input_field.setText(str(5))
    assert dialog.input_field.text() == str(5)

    qtbot.mouseClick(dialog.apply_button, Qt.LeftButton)  # type: ignore[attr-defined]
    await asyncio.sleep(0.1)
    assert vizualisation.framenumber == 5

    assert not dialog.isVisible()

    dialog = FrameDialog(vizualisation)
    dialog.input_field.setText(str(100))
    assert dialog.input_field.text() == str(100)
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    await asyncio.sleep(0.1)
    assert vizualisation.framenumber == 5
    assert not dialog.isVisible()


@pytest.mark.usefixtures('event_loop')
@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
@pytest.mark.asyncio
async def test_chooseseq(qtbot: QtBot) -> None:
    """Testet das chooseframe Fenster mit pytest-qt."""
    vizualisation = VisualisationGui()
    dialog = SeqDialog(vizualisation)
    qtbot.add_widget(vizualisation)

    assert dialog.input_field is not None
    assert dialog.apply_button is not None
    assert dialog.cancel_button is not None

    dialog.input_field.setText(str(5))
    assert dialog.input_field.text() == str(5)

    qtbot.mouseClick(dialog.apply_button, Qt.LeftButton)  # type: ignore[attr-defined]
    await asyncio.sleep(0.1)
    assert vizualisation.seq_id == 5

    assert not dialog.isVisible()

    dialog = SeqDialog(vizualisation)
    dialog.input_field.setText(str(100))
    assert dialog.input_field.text() == str(100)
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    await asyncio.sleep(0.1)
    assert vizualisation.seq_id == 5
    assert not dialog.isVisible()
