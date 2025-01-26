# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Alles für die Sequenzauswahl."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class ButtonPanel(QWidget):
    """Hier kann die Sequenz ausgewählt werden."""

    def __init__(self) -> None:
        """Initialiesierung."""
        super().__init__()

        # Layout für das Widget
        layout = QVBoxLayout(self)

        # Text über den Buttons
        self.info_label = QLabel('Such dir eine Sequenz aus', self)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.buttons = []
        for i in range(10):
            button = QPushButton(f'Sequenz {i}', self)
            button.setStyleSheet('background-color: lightgray; padding: 10px; border-radius: 15px;')
            button.clicked.connect(self.update_seq)
            self.buttons.append(button)
            layout.addWidget(button)

        self.setLayout(layout)

    def update_seq(self) -> None:
        """Updated die seq_id."""
        sender = self.sender()
        button_text = sender.text()  # type: ignore[attr-defined]
        button_number = int(button_text.split(' ')[1])
        print(f'Button {button_number} wurde gedrückt!')


if __name__ == '__main__':
    app = QApplication()
    window = ButtonPanel()
    window.show()
    app.exec()
