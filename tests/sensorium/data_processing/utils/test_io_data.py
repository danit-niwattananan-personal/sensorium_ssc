# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test the IO data loading APIs."""

from pathlib import Path

import numpy as np

import sensorium.data_processing.utils.io_data as semkitti_io


def test_unpack() -> None:
    """Test the unpack function."""
    # Test with a single byte
    compressed = np.array([0b10110101], dtype=np.uint8)
    expected = np.array([1, 0, 1, 1, 0, 1, 0, 1], dtype=np.uint8)
    result = semkitti_io.unpack(compressed)
    np.testing.assert_array_equal(result, expected)

    # Test with multiple bytes
    compressed = np.array([0b11110000, 0b00001111], dtype=np.uint8)
    expected = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], dtype=np.uint8)
    result = semkitti_io.unpack(compressed)
    np.testing.assert_array_equal(result, expected)


def create_mock_data(
    path: str,
    dtype: np.dtype[np.uint8] | np.dtype[np.float32] | np.dtype[np.uint16],
) -> None:
    """Create a mock data file for testing."""
    data = np.array([0, 3, 6], dtype=dtype)
    data.tofile(path)


def test_read_semantickitti() -> None:
    """Test the read_semantickitti function."""
    dtypes = (np.uint16, np.uint8, np.float32)
    unpacks = (False, True, True)
    exts = ('.label', '.invalid', '.bin')

    for dtype, unpack, ext in zip(dtypes, unpacks, exts, strict=True):
        try:
            path = f'test_{dtype.__name__}{ext}'
            create_mock_data(path, dtype)  # type: ignore[arg-type]
            data = semkitti_io.read_semantickitti(path, dtype, unpack)  # type: ignore[arg-type]
            print(data)
            assert data.dtype in (np.float32, np.uint8)
            if not unpack:
                assert np.all(data == np.array([0, 3, 6], dtype=np.float32))
                assert data.dtype == np.float32
                assert data.shape == (3,)
            else:
                assert np.all(
                    data
                    == np.array(
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
                        dtype=np.uint8,
                    )
                )
                assert data.dtype == np.uint8
                assert data.shape == (24,)
        finally:
            Path(path).unlink()


# NOTE: read_label and read_invalid are already tested in test_voxel_loader.py
def test_read_occluded() -> None:
    """Test the read_occluded_semantickitti function."""
    try:
        create_mock_data('test_occluded.occluded', np.dtype(np.uint8))
        data = semkitti_io.read_occluded_semantickitti('test_occluded.occluded')
        assert data.dtype == np.uint8
        assert data.shape == (24,)
        assert np.all(
            data
            == np.array(
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
                dtype=np.uint8,
            )
        )
    finally:
        Path('test_occluded.occluded').unlink()


def test_read_occupancy() -> None:
    """Test the read_occupancy_semantickitti function."""
    try:
        create_mock_data('test_occupancy.occupancy', np.dtype(np.uint8))
        data = semkitti_io.read_occupancy_semantickitti('test_occupancy.occupancy')
        assert data.dtype == np.float32
        assert data.shape == (24,)
        assert np.all(
            data
            == np.array(
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
                dtype=np.float32,
            )
        )
    finally:
        Path('test_occupancy.occupancy').unlink()


def test_read_pointcloud() -> None:
    """Test the read_pointcloud_semantickitti function."""
    try:
        data = np.array([[0, 0, 0, 0], [1, 1, 1, 100], [2, 3, 4, 24]], dtype=np.float32)
        data.tofile('test_pointcloud.bin')
        read_data = semkitti_io.read_pointcloud_semantickitti('test_pointcloud.bin')
        assert read_data.dtype == np.float32
        assert read_data.shape == (3, 4)
        assert np.all(read_data == data)
    finally:
        Path('test_pointcloud.bin').unlink()


def test_get_cmap_semantickitti20() -> None:
    """Test the get_cmap_semantickitti20 function."""
    cmap = semkitti_io.get_cmap_semantickitti20()
    assert np.all(
        cmap
        == np.array(
            [
                [100, 150, 245, 255],
                [100, 230, 245, 255],
                [30, 60, 150, 255],
                [80, 30, 180, 255],
                [100, 80, 250, 255],
                [255, 30, 30, 255],
                [255, 40, 200, 255],
                [150, 30, 90, 255],
                [255, 0, 255, 255],
                [255, 150, 255, 255],
                [75, 0, 75, 255],
                [175, 0, 75, 255],
                [255, 200, 0, 255],
                [255, 120, 50, 255],
                [0, 175, 0, 255],
                [135, 60, 0, 255],
                [150, 240, 80, 255],
                [255, 240, 150, 255],
                [255, 0, 0, 255],
            ]
        ).astype(np.uint8)
    )


if __name__ == '__main__':
    test_unpack()
    test_read_semantickitti()
