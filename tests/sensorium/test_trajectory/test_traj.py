# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
import numpy as np

from sensorium.trajectory.traj import parse_calibration, parse_poses, prepare_trajectory



"""Test trajectory server functionality."""


def test_parse_calibration() -> None:
    """Test calibration parsing."""
    # Create a temporary calibration file
    calib_file = 'test_calib.txt'
    with open(calib_file, 'w') as f:
        f.write('Tr: 1.0 0.0 0.0 0.5 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0\n')

    # Parse calibration file
    calib = parse_calibration(calib_file)
    expected_matrix = np.array(
        [
            [1.0, 0.0, 0.0, 0.5],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    # Check result
    np.testing.assert_array_almost_equal(calib['Tr'], expected_matrix, decimal=5)


def test_parse_poses() -> None:
    """Test pose parsing and transformation."""
    # Create temporary calibration and poses files
    calib_file = 'test_calib.txt'
    poses_file = 'test_poses.txt'
    with open(calib_file, 'w') as f:
        f.write('Tr: 1.0 0.0 0.0 0.5 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0\n')
    with open(poses_file, 'w') as f:
        f.write('1.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0\n')
        f.write('0.0 -1.0 0.0 2.0 1.0  0.0 0.0 0.0 0.0 0.0 1.0 0.0\n')

    # Parse poses
    calibration = parse_calibration(calib_file)
    poses = parse_poses(poses_file, calibration)

    # Expected results
    expected_pose_1 = np.array(
        [
            [1.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )
    expected_pose_2 = np.array(
        [
            [0.0, -1.0, 0.0, 1.5],
            [1.0, 0.0, 0.0, 0.5],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    # Assertions
    np.testing.assert_array_almost_equal(poses[0], expected_pose_1, decimal=5)
    np.testing.assert_array_almost_equal(poses[1], expected_pose_2, decimal=5)


def test_prepare_trajectory() -> None:
    """Test trajectory preparation from calibration and poses."""
    # Create temporary calibration and poses files
    calib_file = 'test_calib.txt'
    poses_file = 'test_poses.txt'
    with open(calib_file, 'w') as f:
        f.write('Tr: 1.0 0.0 0.0 0.5 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0\n')
    with open(poses_file, 'w') as f:
        f.write('1.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0\n')
        f.write('0.0 -1.0 0.0 2.0 1.0  0.0 0.0 0.0 0.0 0.0 1.0 0.0\n')

    # Prepare trajectory
    trajectory = prepare_trajectory(calib_file, poses_file)

    # Expected result
    expected_trajectory = [
        {'x': 1.0, 'y': 0.0, 'z': 0.0},
        {'x': 1.5, 'y': 0.5, 'z': 0.0},
    ]

    # Assertions
    assert (
        trajectory == expected_trajectory
    ), f'Expected {expected_trajectory}, got {trajectory}'
