# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Module to convert .bin files into .ply files for pointcloud visualization."""

import os
from pathlib import Path

import numpy as np


def validate_path(bin_file_path: str, ply_file_path: str) -> None:
    """Raises error if .bin file cannot be opened or .ply cannot be saved.

    Args:
        bin_file_path: path to .bin file that should be opened.
        ply_file_path: path to .ply file that should be saved.

    Returns: None.

    Exception:
        FileNotFoundError: File with the path bin_file_path did not exist.
        PermissionError: Directory was not writable.
        FileExistsError: File with the path ply_file_path did already exits.
    """
    if not Path.exists(bin_file_path):
        msg = f"No such file or directory: '{bin_file_path}'"
        raise FileNotFoundError(msg)
    directory = Path.dirname(ply_file_path)
    if directory and not os.access(directory, os.W_OK):
        msg = f"Directory '{directory}' is not writable."
        raise PermissionError(msg)
    if Path.exists(ply_file_path):
        msg = f"File '{ply_file_path}' already exists."
        raise FileExistsError(msg)


def bin_to_ply(bin_file_path: str, ply_file_path: str) -> None:
    """Converts a .bin file to a .ply file.

    Args:
        bin_file_path: path to .bin file that should be opened.
        ply_file_path: path to .ply file that should be saved.

    Returns: None.
    """
    with Path(bin_file_path).open('rb') as f:
        bin_data = f.read()
    points = np.frombuffer(bin_data, dtype=np.float32).reshape(-1, 4).copy()
    with Path(ply_file_path).open('w') as ply_file:
        header = '\n'.join(
            [
                'ply',
                'format ascii 1.0',
                f'element vertex {len(points)}',
                'property float x',
                'property float y',
                'property float z',
                'property float intensity',
                'end_header',
            ]
        )
        ply_file.write(header + '\n')
        for point in points:
            ply_file.write(' '.join(map(str, point)) + '\n')


if __name__ == '__main__':
    bin_file_path = input('.bin file path:')
    ply_file_path = input('.ply file path:')
    bin_to_ply(bin_file_path, ply_file_path)
    with Path.open(ply_file_path) as f:
        print(f.read(1000))
