# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Server executable entry point."""

from __future__ import annotations

import time


def run() -> None:
    """Entry point function."""
    print('Hello server')
    time.sleep(5)


if __name__ == '__main__':
    run()
