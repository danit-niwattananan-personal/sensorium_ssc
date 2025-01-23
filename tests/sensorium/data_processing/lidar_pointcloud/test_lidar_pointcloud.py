# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Pointcloud Server Functions."""

from pathlib import Path

import numpy as np

from sensorium.data_processing.lidar_pointcloud.point_cloud import (
    get_cmap,
    read_labels,
    read_labels_and_colors,
    read_point_cloud,
)


def create_mock_pointcloud_file(file_path: str) -> None:
    """Create a mock point cloud file for testing."""
    pointcloud_data = np.array(
        [
            [1.0, 2.0, 3.0, 0.5],
            [4.0, 5.0, 6.0, 1.0],
        ],
        dtype=np.float32,
    )
    pointcloud_data.tofile(file_path)


def create_mock_label_file(file_path: str) -> None:
    """Create a mock label file for testing."""
    labels = np.array([10, 20, 30], dtype=np.uint16)
    labels.tofile(file_path)


def create_mock_label_file_with_colors(file_path: str) -> None:
    """Create a mock label file with uint32 labels for testing."""
    labels = np.array([10, 11, 13, 40], dtype=np.uint32)
    labels.tofile(file_path)


# Tests
def test_read_point_cloud() -> None:
    """Test the read_point_cloud function."""
    test_file = 'pointcloud_test.bin'
    create_mock_pointcloud_file(test_file)

    point_cloud = read_point_cloud(test_file)

    assert point_cloud.shape == (2, 3)
    assert np.allclose(point_cloud, [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    Path(test_file).unlink()


def test_read_labels() -> None:
    """Test the read_labels function."""
    test_file = 'labels_test.label'
    create_mock_label_file(test_file)

    labels = read_labels(test_file)

    assert labels.shape == (3,)
    assert np.all(labels == [10, 20, 30])

    Path(test_file).unlink()


def test_get_cmap() -> None:
    """Test the get_cmap function."""
    cmap = get_cmap()

    assert isinstance(cmap, dict)
    assert 10 in cmap
    assert cmap[10] == [245, 150, 100]  # car
    assert 40 in cmap
    assert cmap[40] == [255, 0, 255]  # road


def test_read_labels_and_colors() -> None:
    """Test the read_labels_and_colors function."""
    test_file = 'labels_colors_test.label'
    create_mock_label_file_with_colors(test_file)

    labels, label_colors = read_labels_and_colors(test_file)

    assert labels.shape == (4,)
    assert np.all(labels == [10, 11, 13, 40])

    expected_colors = [
        [245, 150, 100],  # car
        [245, 230, 100],  # bicycle
        [250, 80, 100],  # bus
        [255, 0, 255],  # road
    ]
    assert label_colors.shape == (4, 3)
    assert np.all(label_colors == expected_colors)

    Path(test_file).unlink()


if __name__ == '__main__':
    test_read_point_cloud()
    test_read_labels()
    test_get_cmap()
    test_read_labels_and_colors()
    print('All tests passed.')
