# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Hello."""


from PySide6.QtWidgets import QApplication

from sensorium.engine.engine_run import MainWindow


def setup_window() -> tuple[QApplication, MainWindow]:
    """Fixture zum Erstellen des MainWindow."""
    app = QApplication([])
    window = MainWindow()
    return app, window

def test_main_window_initialization(setup_window: tuple[QApplication, MainWindow]) -> None:
    """Testet, ob das MainWindow korrekt initialisiert wird."""
    _, window = setup_window

    # Prüft den Fenstertitel
    assert window.windowTitle() == 'Sensorium'

    # Prüft die Größe des Fensters
    assert window.width() == 800
    assert window.height() == 600

    # Prüft, ob das zentrale Widget gesetzt wurde
    assert window.centralWidget() is not None

    # Prüft, ob die linke Spalte den richtigen Text hat
    assert window.left_column.text() == 'Ordner'


