# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test für den Aufbau der GUI."""

import os
from unittest.mock import patch

import pytest

from sensorium.engine.engine_run import MainWindow


@pytest.mark.skipif(bool(os.getenv('CI')), reason='no windowing system available in CI')
def test_mainwindow() -> None:
    """Testet das Mainwindow."""
    window = MainWindow()

    with (
        patch.object(window, 'open_settings') as mock_open_settings,
        patch.object(window, 'ask_for_frame') as mock_ask_for_frame,
        patch.object(window, 'ask_for_seq') as mock_ask_for_seq,
    ):
        window.settings_action.trigger()
        window.ask_4_frame.trigger()
        window.ask_4_seq_id.trigger()

        mock_open_settings.assert_called_once()
        mock_ask_for_frame.assert_called_once()
        mock_ask_for_seq.assert_called_once()

