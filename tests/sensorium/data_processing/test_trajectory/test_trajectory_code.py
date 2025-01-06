# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Hello."""

from sensorium.data_processing.trajectory.trajectory_code import hello


def test_hello() -> None:
    """Test sayy hello."""
    assert hello() == 'Hello!'
