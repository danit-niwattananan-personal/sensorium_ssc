# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMenuBar
from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]

from sensorium.engine.engine_run import MainWindow
from sensorium.engine.settings import SettingsDialog


@pytest.fixture
def setup_window() -> tuple[QApplication, MainWindow]:
    """Fixture zum Erstellen und Initialisieren des MainWindow."""
    app = QApplication([])
    window = MainWindow()
    return app, window


def test_main_window_initialization(setup_window: tuple[QApplication, MainWindow]) -> None:
    """Testet die grundlegende Initialisierung des MainWindow."""
    app, window = setup_window
    try:
        assert window.windowTitle() == 'Sensorium'

        assert window.width() == 800
        assert window.height() == 600

        assert window.centralWidget() is not None

        assert isinstance(window.left_column, QLabel)
        assert window.left_column.text() == 'Ordner'

        menu_bar = window.menuBar()
        assert isinstance(menu_bar, QMenuBar)
    finally:
        app.shutdown()


def test_menu_bar(setup_window: tuple[QApplication, MainWindow]) -> None:
    """Testet die Menüleiste."""
    app, window = setup_window
    window.connect_server()
    window.disconnect_server()
    window.ask_for_data()
    app.shutdown()


def test_open_settings_window(qtbot: QtBot) -> None:
    """Testet das Einstellungsfenster mit pytest-qt."""
    dialog = SettingsDialog()
    dialog.show()
    qtbot.waitExposed(dialog)

    input_field = dialog.findChild(QLineEdit)
    assert input_field is not None

    assert dialog.apply_button is not None
    assert dialog.cancel_button is not None

    qtbot.mouseClick(dialog.apply_button, Qt.LeftButton)
    assert not dialog.isVisible()

    dialog = SettingsDialog()
    dialog.show()
    qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)
    assert not dialog.isVisible()
