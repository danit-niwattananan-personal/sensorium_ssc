# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Hello."""

from __future__ import annotations
from sensorium.trajectory.trajectory_code import say_hello


def test_say_hello():
    assert (
        say_hello() == "Hello, World!"
    ), "The function did not return the expected output."


if __name__ == "__main__":
    test_say_hello()
    print("All tests passed!")
