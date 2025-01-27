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

from sensorium.engine.visualization_gui import VisualisationGui


class SettingsDialog(QDialog):
    """Hier werden alle funktionen der Einstellungen beschrieben."""

    def __init__(self, visualisation: VisualisationGui) -> None:
        """Hier wird das Fenster für die Einstellungen initializiert."""
        super().__init__()
        self.setWindowTitle('Einstellungen')
        self.setMinimumSize(300, 200)
        self.visualisation = visualisation
        self.settings_layout = QVBoxLayout(self)

        self.label = QLabel('Max Frame:')
        self.input_field = QLineEdit(self)
        self.input_field.setText(str(self.visualisation.maxframe))
        self.settings_layout.addWidget(self.label)
        self.settings_layout.addWidget(self.input_field)

        self.speed_label = QLabel('Fps:')
        self.speed_input = QLineEdit(self)
        self.speed_input.setText(str(self.visualisation.fps))
        self.settings_layout.addWidget(self.speed_label)
        self.settings_layout.addWidget(self.speed_input)

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
        maxframe = self.input_field.text()
        print(f'Setting applied: {maxframe}')
        maxframe_int = int(maxframe)
        self.visualisation.maxframe = maxframe_int
        self.visualisation.slider.setRange(0, maxframe_int)

        fps = self.speed_input.text()
        self.next_frame_time = int(1000 / int(fps))
        self.visualisation.next_frame_time = self.next_frame_time
        x = self.visualisation.framenumber
        y = self.visualisation.seq_id
        self.visualisation.frame_label.setText(f'Frame: {x}, Sequence: {y} und FPS: {int(fps)}')
        self.accept()


def open_settings_window(visualisation: VisualisationGui) -> QDialog:
    """Hier werden alle Einstellungen kommen."""
    dialog = SettingsDialog(visualisation)
    dialog.exec()
    return dialog
