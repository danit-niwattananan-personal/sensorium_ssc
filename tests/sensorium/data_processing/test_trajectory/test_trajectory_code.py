# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Trajectory Server Functions."""

from sensorium.data_processing.trajectory.traj import (
    parse_calibration,
    parse_poses,
    get_position_at_frame,
    get_framepos_from_list,
)
import numpy as np
from pathlib import Path


# Mock data for testing
def create_mock_calibration_file(file_path):
    with open(file_path, 'w') as f:
        f.write('P2: 1 0 0 0 0 1 0 0 0 0 1 0\n')
        f.write('Tr: 1 0 0 0 0 1 0 0 0 0 1 0\n')


def create_mock_poses_file(file_path):
    with open(file_path, 'w') as f:
        f.write('1 0 0 1 0 1 0 2 0 0 1 3\n')
        f.write('1 0 0 4 0 1 0 5 0 0 1 6\n')


# Tests
def test_parse_calibration():
    test_file = 'calib_test.txt'
    create_mock_calibration_file(test_file)

    result = parse_calibration(test_file)

    assert 'P2' in result
    assert 'Tr' in result
    assert result['P2'].shape == (3, 4)
    assert np.allclose(result['Tr'], np.eye(4))

    Path(test_file).unlink()


def test_parse_poses():
    calib_file = 'calib_test.txt'
    poses_file = 'poses_test.txt'
    create_mock_calibration_file(calib_file)
    create_mock_poses_file(poses_file)

    calibration = parse_calibration(calib_file)
    poses = parse_poses(poses_file, calibration)

    assert len(poses) == 2
    assert poses[0].shape == (4, 4)
    assert poses[1].shape == (4, 4)

    Path(calib_file).unlink()
    Path(poses_file).unlink()


def test_get_position_at_frame():
    calib_file = 'calib_test.txt'
    poses_file = 'poses_test.txt'
    create_mock_calibration_file(calib_file)
    create_mock_poses_file(poses_file)

    position = get_position_at_frame(calib_file, poses_file, 0)
    assert position == {'x': 1.0, 'y': 2.0, 'z': 3.0}

    position = get_position_at_frame(calib_file, poses_file, 1)
    assert position == {'x': 4.0, 'y': 5.0, 'z': 6.0}

    try:
        get_position_at_frame(calib_file, poses_file, 2)
        assert False, 'Expected an IndexError for out-of-range frame index'
    except IndexError:
        pass

    Path(calib_file).unlink()
    Path(poses_file).unlink()


def test_get_framepos_from_list():
    poses = [
        np.array([[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1, 3], [0, 0, 0, 1]]),
        np.array([[1, 0, 0, 4], [0, 1, 0, 5], [0, 0, 1, 6], [0, 0, 0, 1]]),
    ]

    position = get_framepos_from_list(poses, 0)
    assert position == {'x': 1.0, 'y': 2.0, 'z': 3.0}

    position = get_framepos_from_list(poses, 1)
    assert position == {'x': 4.0, 'y': 5.0, 'z': 6.0}

    try:
        get_framepos_from_list(poses, 2)
        assert False, 'Expected an IndexError for out-of-range frame index'
    except IndexError:
        pass


if __name__ == '__main__':
    test_parse_calibration()
    test_parse_poses()
    test_get_position_at_frame()
    test_get_framepos_from_list()
    print('All tests passed.')
