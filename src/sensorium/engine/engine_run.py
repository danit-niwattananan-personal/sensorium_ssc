# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Beschreibung der Gui des Clients."""

import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QMainWindow,
    QMenuBar,
    QVBoxLayout,
    QWidget,
)

from sensorium.engine.chooseframe import choose_frame, choose_seq_id
from sensorium.engine.ordner import ButtonPanel
from sensorium.engine.settings import open_settings_window
from sensorium.engine.visualization_gui import VisualisationGui


class MainWindow(QMainWindow):
    """Code für das Hauptfenster."""

    def __init__(self) -> None:
        """Aufbau der einzelnen Elemente des MainWindow."""
        super().__init__()
        self.setWindowTitle('Sensorium')
        self.setGeometry(300, 200, 1130, 600)
        self.setMinimumSize(1130, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        right_layout = QVBoxLayout()

        self.videoplayer = VisualisationGui()

        self.left_column = ButtonPanel(self.videoplayer)
        self.left_column.setFixedWidth(200)
        main_layout.addWidget(self.left_column)
        right_layout.addWidget(self.videoplayer, stretch=1)
        main_layout.addLayout(right_layout)

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        settings_menu = menu_bar.addMenu('Einstellungen')
        settings_action = QAction('Einstellungen öffnen', self)
        settings_action.setObjectName('action_settings')
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        ask_data_menu = menu_bar.addMenu('Frame/Sequenz_ID wählen')
        ask_4_frame = QAction('Spezielle Framenummer laden', self)
        ask_4_seq_id = QAction('Spezielle Sequenz_ID laden', self)
        ask_4_frame.triggered.connect(self.ask_for_frame)
        ask_4_seq_id.triggered.connect(self.ask_for_seq)
        ask_data_menu.addAction(ask_4_frame)
        ask_data_menu.addAction(ask_4_seq_id)

    def open_settings(self) -> QDialog:
        """Hier werden die Einstellungen geöffnet."""
        print('Einstellungen geöffnet')
        return open_settings_window(self.videoplayer)


    def ask_for_frame(self) -> None:
        """Load current Frame."""
        print('Ordner laden')
        choose_frame(self.videoplayer)

    def ask_for_seq(self) -> None:
        """Load current Frame."""
        print('Ordner laden')
        choose_seq_id(self.videoplayer)


if __name__ == '__main__':
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    window = MainWindow()
    window.show()
    app.exec()  # type: ignore[union-attr]
