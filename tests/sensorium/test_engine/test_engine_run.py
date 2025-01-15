# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test GUI."""

# import pytest  # noqa: ERA001
# from PySide6.QtCore import Qt  # noqa: ERA001
# from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QMenuBar  # noqa: ERA001
# from pytestqt.qtbot import QtBot  # type:ignore[import-untyped]  # noqa: ERA001

# from sensorium.engine.engine_run import MainWindow  # noqa: ERA001
# from sensorium.engine.settings import SettingsDialog  # noqa: ERA001


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


# def test_open_settings_window(qtbot: QtBot) -> None:
#     """Testet das Einstellungsfenster mit pytest-qt."""
#     dialog = SettingsDialog()  # noqa: ERA001
#     dialog.show()  # noqa: ERA001
#     qtbot.waitExposed(dialog)  # noqa: ERA001

#     input_field = dialog.findChild(QLineEdit)  # noqa: ERA001
#     assert input_field is not None

#     assert dialog.apply_button is not None
#     assert dialog.cancel_button is not None

#     qtbot.mouseClick(dialog.apply_button, Qt.LeftButton)  # noqa: ERA001
#     assert not dialog.isVisible()  # noqa: ERA001

#     dialog = SettingsDialog()  # noqa: ERA001
#     dialog.show()  # noqa: ERA001
#     qtbot.mouseClick(dialog.cancel_button, Qt.LeftButton)  # noqa: ERA001
#     assert not dialog.isVisible()  # noqa: ERA001
