# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

from unittest.mock import patch

import pytest  # noqa: F401
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMenuBar  # noqa: F401
from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]

from sensorium.engine.engine_run import MainWindow  # noqa: F401
from sensorium.engine.settings import SettingsDialog
from sensorium.engine.visualization_gui import VisualisationGui

# @pytest.fixture
# def setup_window() -> tuple[QApplication, MainWindow]:
#     """Fixture zum Erstellen und Initialisieren des MainWindow."""
#     app = QApplication([])  # noqa: ERA001
#     window = MainWindow()  # noqa: ERA001
#     return app, window  # noqa: ERA001


# def test_main_window_initialization(setup_window: tuple[QApplication, MainWindow]) -> None:
#     """Testet die grundlegende Initialisierung des MainWindow."""
#     app, window = setup_window  # noqa: ERA001

#     assert window.windowTitle() == 'Sensorium'  # noqa: ERA001

#     assert window.width() == 800  # noqa: ERA001
#     assert window.height() == 600  # noqa: ERA001

#     assert window.centralWidget() is not None  # noqa: ERA001

#     assert isinstance(window.left_column, QLabel)  # noqa: ERA001
#     assert window.left_column.text() == 'Ordner'  # noqa: ERA001

#     menu_bar = window.menuBar()  # noqa: ERA001
#     assert isinstance(menu_bar, QMenuBar)  # noqa: ERA001
#     app.shutdown()  # noqa: ERA001


# def test_menu_bar(setup_window: tuple[QApplication, MainWindow]) -> None:
#     """Testet die Menüleiste."""
#     app, window = setup_window  # noqa: ERA001
#     window.connect_server()  # noqa: ERA001
#     window.disconnect_server()  # noqa: ERA001
#     window.ask_for_data()  # noqa: ERA001
#     app.shutdown()  # noqa: ERA001


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


def test_update_frame(qtbot: QtBot) -> None:
    """Testet das Einstellungsfenster mit pytest-qt."""
    visualisation = VisualisationGui()
    qtbot.add_widget(visualisation)
    with patch(
        'sensorium.engine.visualization_gui.VisualisationGui.update_frame'
    ) as mock_update_frame:
        qtbot.mouseClick(visualisation.button_minus10, Qt.LeftButton)
        mock_update_frame.assert_called_with(-10)
