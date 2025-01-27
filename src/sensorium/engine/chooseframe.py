# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Load Frame by number or load sequenze by number."""

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from sensorium.engine.visualization_gui import VisualisationGui


class FrameDialog(QDialog):
    """Choose your frame."""

    def __init__(self, visualisation: VisualisationGui) -> None:
        """Build Gui forframeloader."""
        super().__init__()
        self.setWindowTitle('Wähle dein Frame')
        self.setMinimumSize(300, 200)
        self.visualisation = visualisation
        self.settings_layout = QVBoxLayout(self)

        self.label = QLabel('Schreibe deine Framenummer rein:')
        self.input_field = QLineEdit(self)
        self.input_field.setText(str(self.visualisation.framenumber))
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
        frame = self.input_field.text()
        print(f'Setting applied: {frame}')
        frame_int = int(frame)
        self.visualisation.framenumber = frame_int

        x = self.visualisation.framenumber
        y = self.visualisation.seq_id
        fps = int(1000 / self.visualisation.next_frame_time)
        self.visualisation.frame_label.setText(f'Frame: {x}, Sequence: {y} und FPS: {int(fps)}')
        self.visualisation.slider.setValue(self.visualisation.framenumber)
        self.accept()


def choose_frame(visualisation: VisualisationGui) -> QDialog:
    """Hier werden alle Einstellungen kommen."""
    dialog = FrameDialog(visualisation)
    dialog.exec()
    return dialog


class SeqDialog(QDialog):
    """Choose your frame."""

    def __init__(self, visualisation: VisualisationGui) -> None:
        """Build Gui forframeloader."""
        super().__init__()
        self.setWindowTitle('Wähle dein Sequenz')
        self.setMinimumSize(300, 200)
        self.visualisation = visualisation
        self.settings_layout = QVBoxLayout(self)

        self.label = QLabel('Schreibe deine Sequenznummer rein:')
        self.input_field = QLineEdit(self)
        self.input_field.setText(str(self.visualisation.seq_id))
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
        seq_id = self.input_field.text()
        print(f'Setting applied: {seq_id}')
        seq_id_int = int(seq_id)
        seq_id_int = min(seq_id_int, 9)
        self.visualisation.seq_id = seq_id_int

        x = self.visualisation.framenumber
        y = self.visualisation.seq_id
        fps = int(1000 / self.visualisation.next_frame_time)
        self.visualisation.frame_label.setText(f'Frame: {x}, Sequence: {y} und FPS: {int(fps)}')
        self.visualisation.slider.setValue(self.visualisation.framenumber)
        self.accept()


def choose_seq_id(visualisation: VisualisationGui) -> QDialog:
    """Hier werden alle Einstellungen kommen."""
    dialog = SeqDialog(visualisation)
    dialog.exec()
    return dialog
