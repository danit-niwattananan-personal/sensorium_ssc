# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""This module provides the launch window for selecting server or client mode."""

import asyncio
import sys
from typing import TYPE_CHECKING

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
from qasync import QEventLoop  # type: ignore[import-untyped]

from sensorium.communication.client_comm import connect_client, disconnect_client
from sensorium.communication.server_comm import get_server_control_functions
from sensorium.engine.engine_run import MainWindow

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class LaunchWindow(QMainWindow):
    """Main window to select server or client mode."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle('Communication')
        self.setGeometry(300, 300, 400, 200)

        self.main_layout = QVBoxLayout()
        self.setup()

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.start_server_func: Callable[[int], None] | None
        self.stop_server_func: Callable[[], Awaitable[None]] | None
        self.start_server_func, self.stop_server_func = get_server_control_functions()  # type: ignore[assignment]

    def setup(self) -> None:
        """Sets up the GUI layout for selecting server or client."""
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

        self.ip_field = QLineEdit()
        self.port_field = QLineEdit()
        self.main_layout.addWidget(self.ip_field)
        self.main_layout.addWidget(self.port_field)
        self.ip_field.hide()
        self.port_field.hide()

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.start_process)
        self.main_layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton('Disconnect')
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.clicked.connect(self.disconnect_client)
        self.main_layout.addWidget(self.disconnect_button)

        self.stop_server_button = QPushButton('Stop server')
        self.stop_server_button.setEnabled(False)
        self.stop_server_button.clicked.connect(self.stop_server)
        self.main_layout.addWidget(self.stop_server_button)

        self.comment_box = QTextEdit()
        self.comment_box.setReadOnly(True)
        self.main_layout.addWidget(self.comment_box)

        self.open_engine_button = QPushButton('Open Engine')
        self.open_engine_button.setVisible(False)
        self.open_engine_button.clicked.connect(self.open_engine)
        self.main_layout.addWidget(self.open_engine_button)

        self.mode: str = ''
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)

    def log(self, message: str) -> None:
        """Log messages to the comment box."""
        self.comment_box.append(message)

    def server_mode(self) -> None:
        """Set up the input fields for server mode."""
        self.mode = 'server'
        self.input_label.setText('Enter Port Number:')
        self.ip_field.setPlaceholderText('Port Number')
        self.ip_field.hide()
        self.port_field.show()

    def client_mode(self) -> None:
        """Set up the input fields for client mode."""
        self.mode = 'client'
        self.input_label.setText('Enter IP Address and Port:')
        self.ip_field.setPlaceholderText('IP Address')
        self.port_field.setPlaceholderText('Port Number')
        self.ip_field.show()
        self.port_field.show()

    def start_process(self) -> None:
        """Start the server or client process based on user input."""
        if self.mode == 'server':
            self.start_server()
        elif self.mode == 'client':
            self.start_client()

    def start_server(self) -> None:
        """Start server."""
        port = self.port_field.text()
        if port.isdigit():
            self.log(f'Starting server on port {port}')
            if callable(self.start_server_func):
                server_task: asyncio.Task = asyncio.create_task(self.start_server_func(int(port)))
                self.current_task = server_task
                self.stop_server_button.setEnabled(True)
                self.connect_button.setEnabled(False)
            else:
                self.log('Error: Server start function is not callable or available.')
        else:
            self.log('Invalid port number. Please enter a valid number.')

    def stop_server(self) -> None:
        """Stop the server."""
        if callable(self.stop_server_func):
            self.log('Stopping server...')
            stop_task: asyncio.Task = asyncio.create_task(self.stop_server_func())
            self.current_task = stop_task
            self.stop_server_button.setEnabled(False)
            self.connect_button.setEnabled(True)
            self.log('Server stopped.')
        else:
            self.log('Error: Server stop function is not callable or available.')

    def start_client(self) -> None:
        """Start client."""
        ip = self.ip_field.text()
        port = self.port_field.text()
        if port.isdigit():
            self.log(f'Connecting to server at {ip}:{port}')
            client_task = asyncio.create_task(connect_client(ip, int(port)))
            self.current_task = client_task
            self.open_engine_button.setVisible(True)
            self.disconnect_button.setEnabled(True)
            self.connect_button.setEnabled(False)
        else:
            self.log('Invalid port number. Please enter a valid number.')

    def disconnect_client(self) -> None:
        """Disconnect the client."""
        self.log('Disconnecting client.')
        disconnect_task = asyncio.create_task(disconnect_client())
        self.current_task = disconnect_task
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.log('Client disconnected.')


    def read_output(self) -> None:
        """Read output from the process and log it."""
        output_data = self.process.readAllStandardOutput().data()
        if isinstance(output_data, bytes | bytearray):
            output = output_data.decode('utf-8')
            self.log(output)

    def open_engine(self) -> None:
        """Launch the engine GUI."""
        self.log('Opening engine...')
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = LaunchWindow()
    window.show()

    with loop:
        loop.run_forever()
