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
    calib_data = {}
    with Path(filename).open() as f:
        for line in f:
            if line == '\n':
                break
            key, value = line.strip().split(':', 1)
            calib_data[key] = np.array([float(v) for v in value.split()])

    ret = {}
    ret['P2'] = calib_data['P2'].reshape(3, 4)  # 3x4 projection matrix for left camera
    ret['Tr'] = np.identity(4)
    ret['Tr'][:3, :4] = calib_data['Tr'].reshape(3, 4)
    return ret


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

            pose = np.zeros((4, 4))
            pose[0, 0:4] = values[0:4]
            pose[1, 0:4] = values[4:8]
            pose[2, 0:4] = values[8:12]
            pose[3, 3] = 1.0

            poses.append(tr_inv @ (pose @ tr))

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

    error_message = f"""Frame Index out of range. Frame index: {frame_index},
    number of frames: {len(poses)}
    """

    # Ensure the requested frame index is valid
    if frame_index < 0 or frame_index >= len(poses):
        raise IndexError(error_message)

    # Extract the (x, y, z) coordinates for the requested frame
    pose = poses[frame_index]
    return {'x': pose[0, 3], 'y': pose[1, 3], 'z': pose[2, 3]}

def get_framepos_from_list(poses: list[NDArray[np.float64]], frame_index: int) -> dict[str, float]:
    """Retrieve the (x, y, z) position for a specific frame from a pre-computed list of poses.

    Args:
        poses (list[NDArray[np.float64]]): List of poses as 4x4 numpy arrays.
        frame_index (int): The frame number for which to get the position.

    Returns:
        dict: A dictionary containing {'x': float, 'y': float, 'z': float}.
    """
    error_message = f"""Frame Index out of range. Frame index: {frame_index},
    number of frames: {len(poses)}
    """

    # Ensure the requested frame index is valid
    if frame_index < 0 or frame_index >= len(poses):
        raise IndexError(error_message)

    # Extract the (x, y, z) coordinates for the requested frame
    pose = poses[frame_index]
    return {'x': pose[0, 3], 'y': pose[1, 3], 'z': pose[2, 3]}
