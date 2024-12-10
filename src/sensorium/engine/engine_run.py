# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""GUI."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """MainWindow."""

    def __init__(self) -> None:
        """Aufbau der einzelnen Elemente des MainWindow."""
        super().__init__()
        self.setWindowTitle('Sensorium')
        self.setGeometry(100, 100, 800, 600)

        # Zentrale Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Hauptlayout
        main_layout = QHBoxLayout(central_widget)

        # Ordner
        self.left_column = QLabel('Ordner')
        self.left_column.setStyleSheet('background-color: lightgray; padding: 10px;')
        self.left_column.setFixedWidth(200)
        main_layout.addWidget(self.left_column)

        # Videoplayer
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        # Platzhalter-Label für Videoplayer
        placeholder = QLabel('Hier kommt der Videoplayer')
        placeholder.setAlignment(Qt.AlignCenter)  # type: ignore[attr-defined]
        right_layout.addWidget(placeholder, stretch=1)

        # Menüleiste
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menü: Einstellungen  # noqa: ERA001
        settings_menu = menu_bar.addMenu('Einstellungen')
        settings_action = QAction('Einstellungen öffnen', self)
        settings_action.setObjectName('action_settings')
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        # Menü: Server verbinden
        server_menu = menu_bar.addMenu('Server')
        server_connect = QAction('Mit Server verbinden', self)
        server_connect.triggered.connect(self.connect_server)
        server_disconnect = QAction('Verbindung trennen', self)
        server_disconnect.triggered.connect(self.disconnect_server)
        server_menu.addAction(server_connect)
        server_menu.addAction(server_disconnect)

        # Menü: Dateien vom Server anfragen
        ask_data_menu = menu_bar.addMenu('Dateien')
        ask_data_action = QAction('Dateien vom Server anfragen', self)
        ask_4_new_data = QAction('Dateien neu anfragen', self)
        ask_data_action.triggered.connect(self.ask_for_data)
        ask_4_new_data.triggered.connect(self.ask_for_data)
        ask_data_menu.addAction(ask_data_action)
        ask_data_menu.addAction(ask_4_new_data)

    def open_settings(self) -> None:
        """Hier wird später das fenster für die Einstellungen geöffnet."""
        print('Einstellungen geöffnet')

    def connect_server(self) -> None:
        """Hier wird später das Pop-Up für den Aufbau der Verbindung geöffnet."""
        print('Mit Server verbunden')

    def disconnect_server(self) -> None:
        """Hier wird später die Verbindung zum Server getrennt."""
        print('Verbindung zum Server getrennt')

    def ask_for_data(self) -> None:
        """Hier werden später die Ordner vom Server geladen."""
        print('Ordner laden')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
