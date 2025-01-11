# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Trajectory Server Functions."""

from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def parse_calibration(filename: str) -> dict[str, NDArray[np.float64]]:
    """Parse the calibration file to extract the transformation matrix.

    Args:
        filename (str): Path to the calibration file.

    Returns:
        dict: Calibration matrices as 4x4 numpy arrays.
    """
    calib = {}
    with Path(filename).open() as calib_file:
        for line in calib_file:
            key, content = line.strip().split(':')
            calib[key] = np.array([float(x) for x in content.split()])
    return calib


def parse_poses(
    filename: str, calibration: dict[str, NDArray[np.float64]]
) -> list[NDArray[np.float64]]:
    """Parse the poses file and transform the poses using calibration data.

    Args:
        filename (str): Path to the poses file.
        calibration (dict): Calibration data from parse_calibration.

    Returns:
        list: List of poses as 4x4 numpy arrays.
    """
    poses = []
    tr = calibration['Tr']
    tr_inv = np.linalg.inv(tr)

    with Path(filename).open() as file:
        for line in file:
            values = [float(v) for v in line.strip().split()]
            pose = np.array(values).reshape(4, 4)
            poses.append(np.dot(tr_inv, pose))
    return poses


def get_position_at_frame(calib_file: str, poses_file: str, frame_index: int) -> dict[str, float]:
    """Retrieve the (x, y, z) position for a specific frame.

    Args:
        calib_file (str): Path to the calibration file.
        poses_file (str): Path to the poses file.
        frame_index (int): The frame number for which to get the position.

    Returns:
        dict: A dictionary containing {'x': float, 'y': float, 'z': float}.
    """
    # Load calibration and poses
    calibration = parse_calibration(calib_file)
    poses = parse_poses(poses_file, calibration)

    # Ensure the requested frame index is valid
    if frame_index < 0 or frame_index >= len(poses):
        raise IndexError('Frame index out of range.')

    # Extract the (x, y, z) coordinates for the requested frame
    pose = poses[frame_index]
    return {'x': pose[0, 3], 'y': pose[1, 3], 'z': pose[2, 3]}
