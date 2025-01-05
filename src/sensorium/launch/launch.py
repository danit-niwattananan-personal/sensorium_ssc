# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""This module provides the launch window for selecting server or client mode."""

import sys
from pathlib import Path

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class LaunchWindow(QMainWindow):
    """Main window to select server or client mode."""

    def __init__(self) -> None:
        """Initialize the main window for selecting server or client. Sets up the GUI layout."""
        super().__init__()
        self.setWindowTitle('WebSocket File Transfer')
        self.setGeometry(300, 300, 400, 200)

        self.main_layout = QVBoxLayout()
        self.label = QLabel('Select Role:')
        self.main_layout.addWidget(self.label)

        self.server_button = QPushButton('Server')
        self.client_button = QPushButton('Client')
        self.server_button.clicked.connect(self.server_mode)
        self.client_button.clicked.connect(self.client_mode)
        self.main_layout.addWidget(self.server_button)
        self.main_layout.addWidget(self.client_button)

        self.input_label = QLabel('')
        self.main_layout.addWidget(self.input_label)

        self.input_field1 = QLineEdit()
        self.input_field2 = QLineEdit()
        self.main_layout.addWidget(self.input_field1)
        self.main_layout.addWidget(self.input_field2)
        self.input_field1.hide()
        self.input_field2.hide()

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_process)
        self.main_layout.addWidget(self.start_button)

        self.comment_box = QTextEdit()
        self.comment_box.setReadOnly(True)
        self.main_layout.addWidget(self.comment_box)

        self.open_engine_button = QPushButton('Open Engine')
        self.open_engine_button.setVisible(False)
        self.open_engine_button.clicked.connect(self.open_engine)
        self.main_layout.addWidget(self.open_engine_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.mode: str = ''
        self.process: QProcess = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_output)


    def log(self, message: str) -> None:
        """Log messages to the comment box."""
        self.comment_box.append(message)

    def server_mode(self) -> None:
        """Set up the input fields for server mode."""
        self.mode = 'server'
        self.input_label.setText('Enter Port Number:')
        self.input_field1.setPlaceholderText('Port Number')
        self.input_field1.show()
        self.input_field2.hide()

    def client_mode(self) -> None:
        """Set up the input fields for client mode."""
        self.mode = 'client'
        self.input_label.setText('Enter IP Address and Port:')
        self.input_field1.setPlaceholderText('IP Address')
        self.input_field2.setPlaceholderText('Port Number')
        self.input_field1.show()
        self.input_field2.show()

    def start_process(self) -> None:
        """Start server or client based on user input."""
        current_dir = Path(__file__).parent.resolve()
        server_script = current_dir / '..' / 'communication' / 'server_comm.py'
        client_script = current_dir / '..' / 'communication' / 'client_comm.py'

        if self.mode == 'server':
            port = self.input_field1.text()
            if port.isdigit():
                self.log(f'Starting server on port {port}')
                self.process.start('python', [str(server_script), port])
                if True:  # connection approval should be implemented
                    self.open_engine_button.setVisible(True)
        elif self.mode == 'client':
            ip = self.input_field1.text()
            port = self.input_field2.text()
            if port.isdigit():
                self.log(f'Connectiong to a server at {ip} on port {port}')
                self.process.start('python', [str(client_script), ip, port])
                if True:  # connection approval should be implemented
                    self.open_engine_button.setVisible(True)

    def read_output(self) -> None:
        """Read output from the process and log it."""
        output_data = self.process.readAllStandardOutput().data()
        if isinstance(output_data, bytes | bytearray):
            output = output_data.decode('utf-8')
            self.log(output)

    def open_engine(self) -> None:
        """Launch the engine GUI."""
        current_dir = Path(__file__).parent.resolve()
        engine_script = current_dir / '..' / 'engine' / 'engine_run.py'
        self.log('Opening engine...')
        self.process.start('python', [str(engine_script)])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LaunchWindow()
    window.show()
    sys.exit(app.exec())
