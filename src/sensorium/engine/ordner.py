# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Alles für die Sequenzauswahl."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

from sensorium.engine.visualization_gui import VisualisationGui


class ButtonPanel(QWidget):
    """Hier kann die Sequenz ausgewählt werden."""

    def __init__(self, videoplayer: VisualisationGui) -> None:
        """Initialiesierung."""
        super().__init__()
        self.videoplayer = videoplayer
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.info_label = QLabel('Such dir eine Sequenz aus', self)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        for i in range(16):
            button = QPushButton(f'Sequenz {i}', self)
            button.setStyleSheet("""
                QPushButton {
                    background-color: lightgray;
                    padding: 10px;
                    border-radius: 10px;
                    border: 1px solid transparent;
                }

                QPushButton:hover {
                    background-color: lightblue;
                    border: 1px solid #0066cc;
                }

                QPushButton:pressed {
                    background-color: lightgray;
                    border: 1px solid gray;
                }
            """)
            button.clicked.connect(self.update_seq)
            layout.addWidget(button)

        self.setLayout(layout)

    def update_seq(self) -> None:
        """Updated die seq_id."""
        sender = self.sender()
        button_text = sender.text()  # type: ignore[attr-defined]
        button_number = int(button_text.split(' ')[1])
        print(f'Button {button_number} wurde gedrückt!')
        if self.videoplayer.seq_id != button_number:
            self.videoplayer.seq_id = button_number
            self.videoplayer.framenumber = 0
            self.videoplayer.update_frame(0)


if __name__ == '__main__':
    app = QApplication()
    videoplayer = VisualisationGui()
    window = ButtonPanel(videoplayer)
    window.show()
    app.exec()
