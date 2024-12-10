# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QMenuBar

from sensorium.engine.engine_run import MainWindow


@pytest.fixture
def setup_window() -> tuple[QApplication, MainWindow]:
    """Fixture zum Erstellen und Initialisieren des MainWindow."""
    app = QApplication([])  # Erstellen einer QApplication-Instanz
    window = MainWindow()  # Erstellen eines MainWindow
    return app, window


def test_main_window_initialization(setup_window: tuple[QApplication, MainWindow]) -> None:
    """Testet die grundlegende Initialisierung des MainWindow."""
    app , window = setup_window

    # Überprüfen des Fenstertitels
    assert window.windowTitle() == 'Sensorium'

    # Überprüfen der Fenstergröße
    assert window.width() == 800
    assert window.height() == 600

    # Überprüfen, ob das zentrale Widget vorhanden ist
    assert window.centralWidget() is not None

    # Überprüfen, ob die linke Spalte existiert und den richtigen Text hat
    assert isinstance(window.left_column, QLabel)
    assert window.left_column.text() == 'Ordner'

    # Überprüfen, ob die Menüleiste vorhanden ist
    menu_bar = window.menuBar()
    assert isinstance(menu_bar, QMenuBar)
    app.shutdown()
