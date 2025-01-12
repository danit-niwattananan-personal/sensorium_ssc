# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Settings."""

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class SettingsDialog(QDialog):
    """Hier werden alle funktionen der Einstellungen beschrieben."""

    def __init__(self) -> None:
        """Hier wird das Fenster für die Einstellungen initializiert."""
        super().__init__()
        self.setWindowTitle('Einstellungen')
        self.setMinimumSize(300, 200)

        self.settings_layout = QVBoxLayout(self)

        self.label = QLabel('Example Setting:')
        self.input_field = QLineEdit(self)
        self.settings_layout.addWidget(self.label)
        self.settings_layout.addWidget(self.input_field)

        self.button_layout = QHBoxLayout()

        self.apply_button = QPushButton('Apply')
        self.apply_button.clicked.connect(self.apply_settings)
        self.button_layout.addWidget(self.apply_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.settings_layout.addLayout(self.button_layout)

    def apply_settings(self) -> None:
        """Speichert später die Einstellungen."""
        setting_value = self.input_field.text()
        print(f'Setting applied: {setting_value}')
        self.accept()


def open_settings_window() -> QDialog:
    """Hier werden alle Einstellungen kommen."""
    dialog = SettingsDialog()
    dialog.exec()
    return dialog
