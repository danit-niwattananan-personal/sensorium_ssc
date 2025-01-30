# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test the fusion module."""

import numpy as np
import pytest
from numba.core.dispatcher import Dispatcher  # type: ignore[import-untyped]

from sensorium.data_processing.voxel_process.fusion import TSDFVolume, rigid_transform


def test_tsdf_volume_initialization() -> None:
    """Test TSDF Volume initialization and attributes."""
    vol_bnds = np.array([[-3, 3], [-3, 3], [-3, 3]], dtype=np.float32)
    voxel_size = 0.1

    tsdf = TSDFVolume(vol_bnds, voxel_size)

    # Test initialization
    assert isinstance(tsdf._tsdf_vol_cpu, np.ndarray) # noqa: SLF001
    assert isinstance(tsdf._weight_vol_cpu, np.ndarray) # noqa: SLF001
    assert isinstance(tsdf._color_vol_cpu, np.ndarray) # noqa: SLF001
    assert tsdf._voxel_size == 0.1 # noqa: SLF001
    assert tsdf._trunc_margin == 5 * voxel_size # noqa: SLF001

def test_vox2world() -> None:
    """Test voxel to world coordinate conversion."""
    # Setup test data
    vol_origin = np.array([0., 0., 0.])
    vox_coords = np.array([[0, 0, 0], [1, 1, 1]], dtype=np.float32)
    vox_size = 0.1

    # Test method
    world_coords = TSDFVolume.vox2world(vol_origin, vox_coords, vox_size)

    # Check output
    assert world_coords.shape == (2, 3)
    assert world_coords.dtype == np.float32
    # First point should be at (0.05, 0.05, 0.05) due to default offset
    np.testing.assert_array_almost_equal(
        world_coords[0],
        np.array([0.05, 0.05, 0.05])
    )

def test_cam2pix() -> None:
    """Test camera to pixel coordinate conversion."""
    # Setup test data
    cam_pts = np.array([[0, 0, 1], [1, 1, 2]], dtype=np.float32)
    intr = np.array([
        [500, 0, 320],
        [0, 500, 240],
        [0, 0, 1]
    ], dtype=np.float64)

    # Test conversion
    pixels = TSDFVolume.cam2pix(cam_pts, intr)

    # Check output
    assert pixels.shape == (2, 2)
    assert pixels.dtype == np.int64
    # First point should project to principal point
    assert np.array_equal(pixels[0], np.array([320, 240]))

def test_rigid_transform() -> None:
    """Test rigid transformation of point cloud."""
    # Setup test data
    xyz = np.array([[1, 0, 0], [0, 1, 0]], dtype=np.float32)
    transform = np.array([
        [0, -1, 0, 1],
        [1, 0, 0, 2],
        [0, 0, 1, 3],
        [0, 0, 0, 1]
    ], dtype=np.float64)

    # Apply transformation
    transformed = rigid_transform(xyz, transform)

    # Check output
    assert transformed.shape == (2, 3)
    assert transformed.dtype == np.float32
    # Check if rotation and translation are correct
    expected = np.array([
        [1, 3, 3],
        [0, 2, 3]
    ], dtype=np.float32)
    assert np.array_equal(transformed, expected)

def test_invalid_volume_bounds() -> None:
    """Test TSDF Volume initialization with invalid bounds."""
    invalid_bounds = np.array([[-3, 3], [-3, 3]], dtype=np.float32)  # Missing z bounds
    with pytest.raises(AssertionError):
        TSDFVolume(invalid_bounds, 0.1)

def test_vox2world_with_custom_offsets() -> None:
    """Test voxel to world conversion with custom offsets."""
    vol_origin = np.array([0., 0., 0.])
    vox_coords = np.array([[0, 0, 0]], dtype=np.float32)
    vox_size = 0.1
    offsets = (0.0, 0.0, 0.0)

    world_coords = TSDFVolume.vox2world(vol_origin, vox_coords, vox_size, offsets)

    # With zero offsets, should be at origin
    assert np.array_equal(
        world_coords[0],
        np.array([0.0, 0.0, 0.0])
    )

def test_optimization() -> None:
    """Test whether the numba decorators are working."""
    # Test njit compilation
    assert isinstance(TSDFVolume.vox2world.__get__(None, TSDFVolume), Dispatcher)
    assert isinstance(TSDFVolume.cam2pix.__get__(None, TSDFVolume), Dispatcher)


