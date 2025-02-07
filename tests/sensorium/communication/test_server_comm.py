# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test module for server communication."""

import bz2
import gzip

import numpy as np
import pytest
from numpy.typing import NDArray

from sensorium.communication import server_comm


def dummy_process_camera2(seq_id: int, frame_id: int) -> dict[str, NDArray[np.uint8]]:
    """Dummy backend process function for camera2.

    Args:
        seq_id: Sequence identifier.
        frame_id: Frame identifier.

    Returns:
        A dictionary containing a dummy 'image_2' NumPy array.
    """
    del seq_id, frame_id
    dummy_image: NDArray[np.uint8] = np.full((370, 1226, 3), 255, dtype=np.uint8)
    return {'image_2': dummy_image}


def dummy_process_camera3(seq_id: int, frame_id: int) -> dict[str, NDArray[np.uint8]]:
    """Dummy backend process function for camera3.

    Args:
        seq_id: Sequence identifier.
        frame_id: Frame identifier.

    Returns:
        A dictionary containing a dummy 'image_3' NumPy array.
    """
    del seq_id, frame_id
    dummy_image: NDArray[np.uint8] = np.full((370, 1226, 3), 100, dtype=np.uint8)
    return {'image_3': dummy_image}


def dummy_process_lidar(seq_id: int, frame_id: int) -> dict[str, NDArray[np.float32]]:
    """Dummy backend process function for lidar.

    Args:
        seq_id: Sequence identifier.
        frame_id: Frame identifier.

    Returns:
        A dictionary containing dummy 'lidar_pc' and 'lidar_pc_labels' arrays.
    """
    del seq_id, frame_id
    dummy_pc: NDArray[np.float32] = np.full((10, 3), 1.0, dtype=np.float32)
    dummy_labels: NDArray[np.float32] = np.full((10, 1), 2.0, dtype=np.float32)
    return {'lidar_pc': dummy_pc, 'lidar_pc_labels': dummy_labels}


def dummy_process_voxel(
    seq_id: int, frame_id: int
) -> dict[str, NDArray[np.uint8 | np.bool_ | np.float64]]:
    """Dummy backend process function for voxel.

    Args:
        seq_id: Sequence identifier.
        frame_id: Frame identifier.

    Returns:
        A dictionary containing dummy 'voxel', 'fov_mask', and 't_velo_2_cam' arrays.
    """
    del seq_id, frame_id
    voxel: NDArray[np.uint8] = np.full((256, 256, 32), 77, dtype=np.uint8)
    fov_mask: NDArray[np.bool_] = np.full((2097152,), fill_value=True, dtype=np.bool_)
    t_velo_2_cam: NDArray[np.float64] = np.full((4, 4), 3.14, dtype=np.float64)
    return {'voxel': voxel, 'fov_mask': fov_mask, 't_velo_2_cam': t_velo_2_cam}


def dummy_process_trajectory(seq_id: int, frame_id: int) -> dict[str, NDArray[np.float64]]:
    """Dummy backend process function for trajectory.

    Args:
        seq_id: Sequence identifier.
        frame_id: Frame identifier.

    Returns:
        A dictionary containing a dummy 'trajectory' array.
    """
    del seq_id, frame_id
    trajectory: NDArray[np.float64] = np.array([7.0, 8.0, 9.0], dtype=np.float64)
    return {'trajectory': trajectory}


def test_create_response_camera2(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_response correctly compresses and returns a response for camera2."""
    monkeypatch.setattr(server_comm.backend_engine, 'process', dummy_process_camera2)
    response = server_comm.create_response('camera2', 0, 0)
    decompressed = bz2.decompress(response)
    expected = np.full((370, 1226, 3), 255, dtype=np.uint8).tobytes()
    assert decompressed == expected


def test_create_response_camera3(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_response correctly compresses and returns a response for camera3."""
    monkeypatch.setattr(server_comm.backend_engine, 'process', dummy_process_camera3)
    response = server_comm.create_response('camera3', 0, 0)
    decompressed = bz2.decompress(response)
    expected = np.full((370, 1226, 3), 100, dtype=np.uint8).tobytes()
    assert decompressed == expected


def test_create_response_lidar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_response correctly compresses and returns a response for lidar."""
    monkeypatch.setattr(server_comm.backend_engine, 'process', dummy_process_lidar)
    response = server_comm.create_response('lidar', 0, 0)
    decompressed = gzip.decompress(response)
    parts = decompressed.split(b'__SPLIT__')
    assert len(parts) == 2
    expected_pc = np.full((10, 3), 1.0, dtype=np.float32).tobytes()
    expected_labels = np.full((10, 1), 2.0, dtype=np.float32).tobytes()
    assert parts[0] == expected_pc
    assert parts[1] == expected_labels


def test_create_response_voxel(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_response correctly compresses and returns a response for voxel."""
    monkeypatch.setattr(server_comm.backend_engine, 'process', dummy_process_voxel)
    response = server_comm.create_response('voxel', 0, 0)
    decompressed = gzip.decompress(response)
    parts = decompressed.split(b'__SPLIT__')
    assert len(parts) == 3
    expected_voxel = np.full((256, 256, 32), 77, dtype=np.uint8).tobytes()
    expected_fov = np.full((2097152,), fill_value=True, dtype=bool).tobytes()
    expected_t = np.full((4, 4), 3.14, dtype=np.float64).tobytes()
    assert parts[0] == expected_voxel
    assert parts[1] == expected_fov
    assert parts[2] == expected_t


def test_create_response_trajectory(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_response correctly returns a response for trajectory."""
    monkeypatch.setattr(server_comm.backend_engine, 'process', dummy_process_trajectory)
    response = server_comm.create_response('trajectory', 0, 0)
    expected = np.array([7.0, 8.0, 9.0], dtype=np.float64).tobytes()
    assert response == expected


def test_create_response_unknown_sensor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that create_response raises a ValueError for an unknown sensor type."""
    monkeypatch.setattr(server_comm.backend_engine, 'process', dummy_process_camera2)
    with pytest.raises(ValueError, match='Unknown sensor type'):
        server_comm.create_response('invalid_sensor', 0, 0)
