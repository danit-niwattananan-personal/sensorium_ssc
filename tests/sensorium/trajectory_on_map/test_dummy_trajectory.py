# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""dummy module."""

from sensorium.trajectory_on_map.dummy_trajectory import trajectory_function


def test_trajectory_function() -> None:
    """Dummy function."""
    assert trajectory_function() == 1
