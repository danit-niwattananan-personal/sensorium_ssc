# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Trajectory Server Functions."""

import numpy as np
from numpy.linalg import inv
from numpy.typing import NDArray
from typing import List, Dict, Mapping


def parse_calibration(filename: str) -> Mapping[str, NDArray[np.float64]]:
    """
    Parse the calibration file to extract the transformation matrix.

    Args:
        filename (str): Path to the calibration file.

    Returns:
        dict: Calibration matrices as 4x4 numpy arrays.
    """
    calib = {}
    with open(filename) as calib_file:
        for line in calib_file:
            key, content = line.strip().split(':')
            values = [float(v) for v in content.strip().split()]
            pose = np.zeros((4, 4), dtype=np.float64)
            if key == 'Tr':
                pose[0, 0:4] = values[0:4]
                pose[1, 0:4] = values[4:8]
                pose[2, 0:4] = values[8:12]
                pose[3, 3] = 1.0
            calib[key] = pose
    return calib


def parse_poses(filename: str, calibration: Mapping[str, NDArray[np.float64]]) -> List[NDArray[np.float64]]:
    """
    Parse the poses file and transform the poses using calibration data.

    Args:
        filename (str): Path to the poses file.
        calibration (dict): Calibration data from parse_calibration.

    Returns:
        list: List of poses as 4x4 numpy arrays.
    """
    poses = []
    tr = calibration['Tr']
    tr_inv = np.linalg.inv(tr)

    with open(filename) as file:
        for line in file:
            values = [float(v) for v in line.strip().split()]
            pose = np.zeros((4, 4), dtype=np.float64)
            pose[0, 0:4] = values[0:4]
            pose[1, 0:4] = values[4:8]
            pose[2, 0:4] = values[8:12]
            pose[3, 3] = 1.0
            # Transform pose to global coordinates
            global_pose = np.matmul(tr_inv, np.matmul(pose, tr))
            poses.append(global_pose)
    return poses


def prepare_trajectory(calib_file: str, poses_file: str) -> List[Dict[str, float]]:
    """
    Parse calibration and poses to generate a trajectory list.

    Args:
        calib_file (str): Path to the calibration file.
        poses_file (str): Path to the poses file.

    Returns:
        list: List of trajectory points as dictionaries with (x, y, z).
    """
    # Parse files
    calibration = parse_calibration(calib_file)
    poses = parse_poses(poses_file, calibration)

    # Extract (x, y, z) from the 4x4 pose matrices
    trajectory = [{'x': pose[0, 3], 'y': pose[1, 3], 'z': pose[2, 3]} for pose in poses]

    return trajectory


def save_trajectory(trajectory: List[Dict[str, float]]) -> None:
    """
    Placeholder for saving the trajectory data.

    Args:
        trajectory (list): The trajectory data to save.
    """
    pass





