# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import os

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.engine.chooseframe import FrameDialog, SeqDialog
from sensorium.engine.visualization_gui import VisualisationGui


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_chooseframe(qtbot: QtBot) -> None:
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
    assert vizualisation.framenumber == 5

    assert not dialog.isVisible()

    dialog = FrameDialog(vizualisation)
    dialog.input_field.setText(str(100))
    assert dialog.input_field.text() == str(100)
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    assert vizualisation.framenumber == 5
    assert not dialog.isVisible()


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_chooseseq(qtbot: QtBot) -> None:
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
    assert vizualisation.seq_id == 5

    assert not dialog.isVisible()

    dialog = SeqDialog(vizualisation)
    dialog.input_field.setText(str(100))
    assert dialog.input_field.text() == str(100)
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    assert vizualisation.seq_id == 5
    assert not dialog.isVisible()

# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import os

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot  # type: ignore[import-untyped]

from sensorium.engine.chooseframe import FrameDialog, SeqDialog
from sensorium.engine.visualization_gui import VisualisationGui


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_chooseframe(qtbot: QtBot) -> None:
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
    assert vizualisation.framenumber == 5

    assert not dialog.isVisible()

    dialog = FrameDialog(vizualisation)
    dialog.input_field.setText(str(100))
    assert dialog.input_field.text() == str(100)
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    assert vizualisation.framenumber == 5
    assert not dialog.isVisible()

@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_chooseseq(qtbot: QtBot) -> None:
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
    assert vizualisation.seq_id == 5

    assert not dialog.isVisible()

    dialog = SeqDialog(vizualisation)
    dialog.input_field.setText(str(100))
    assert dialog.input_field.text() == str(100)
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # type: ignore[attr-defined]
    assert vizualisation.seq_id == 5
    assert not dialog.isVisible()
