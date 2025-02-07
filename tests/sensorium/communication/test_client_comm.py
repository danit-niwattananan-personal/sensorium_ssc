# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test module for client communication."""

import bz2
import gzip
import json
from collections.abc import AsyncGenerator

import numpy as np
import pytest
import pytest_asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol

from sensorium.communication import client_comm

FIXED_PORT = 8765


async def dummy_ws_handler(websocket: WebSocketServerProtocol) -> None:
    """Dummy WebSocket handler for testing client communication.

    Args:
        websocket: The WebSocket connection.
        _path: The URL path (unused).
    """
    async for message in websocket:
        request = json.loads(message)
        sensor_type = request.get('sensor_type')
        if sensor_type == 'camera2':
            dummy = np.full(client_comm.CAMERA2_SHAPE, 128, dtype=np.uint8)
            response = bz2.compress(dummy.tobytes())
        elif sensor_type == 'camera3':
            dummy = np.full(client_comm.CAMERA3_SHAPE, 64, dtype=np.uint8)
            response = bz2.compress(dummy.tobytes())
        elif sensor_type == 'lidar':
            dummy_pc = np.full((10, 3), 1.0, dtype=np.float32)
            dummy_labels = np.full((10, 1), 2.0, dtype=np.float32)
            combined = dummy_pc.tobytes() + b'__SPLIT__' + dummy_labels.tobytes()
            response = gzip.compress(combined)
        elif sensor_type == 'voxel':
            voxel = np.full(client_comm.VOXEL_SHAPE, 255, dtype=np.uint8)
            fov_mask = np.full(client_comm.FOV_MASK_SHAPE, fill_value=True, dtype=bool)
            t_velo_2_cam = np.full(client_comm.T_VELO_2_CAM_SHAPE, 3.14, dtype=np.float64)
            combined = (
                voxel.tobytes()
                + b'__SPLIT__'
                + fov_mask.tobytes()
                + b'__SPLIT__'
                + t_velo_2_cam.tobytes()
            )
            response = gzip.compress(combined)
        elif sensor_type == 'trajectory':
            trajectory = np.array([7.0, 8.0, 9.0], dtype=np.float64)
            response = trajectory.tobytes()
        else:
            response = b''
        await websocket.send(response)


@pytest_asyncio.fixture
async def dummy_server() -> AsyncGenerator[object, None]:
    """Fixture to start a dummy WebSocket server for testing client communication.

    Yields:
        The running dummy WebSocket server.
    """
    server = await websockets.serve(
        dummy_ws_handler,  # type: ignore[arg-type]
        '127.0.0.1',
        FIXED_PORT,
        max_size=2_097_152,
    )
    try:
        yield server
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.usefixtures('dummy_server')
@pytest.mark.asyncio
async def test_client_connect_disconnect() -> None:
    """Test that connect_client and disconnect_client correctly established."""
    await client_comm.connect_client('127.0.0.1', FIXED_PORT)
    assert client_comm._client_manager._client is not None  # noqa: SLF001
    await client_comm.disconnect_client()
    assert client_comm._client_manager._client is None  # noqa: SLF001


@pytest.mark.usefixtures('dummy_server')
@pytest.mark.asyncio
async def test_get_camera2_data() -> None:
    """Test get_camera2_data for correct request and decoding."""
    await client_comm.connect_client('127.0.0.1', FIXED_PORT)
    data = await client_comm.get_camera2_data(0, 0)
    expected = np.full(client_comm.CAMERA2_SHAPE, 128, dtype=np.uint8)
    assert np.array_equal(data, expected)
    await client_comm.disconnect_client()


@pytest.mark.usefixtures('dummy_server')
@pytest.mark.asyncio
async def test_get_camera3_data() -> None:
    """Test get_camera3_data for correct request and decoding."""
    await client_comm.connect_client('127.0.0.1', FIXED_PORT)
    data = await client_comm.get_camera3_data(0, 0)
    expected = np.full(client_comm.CAMERA3_SHAPE, 64, dtype=np.uint8)
    assert np.array_equal(data, expected)
    await client_comm.disconnect_client()


@pytest.mark.usefixtures('dummy_server')
@pytest.mark.asyncio
async def test_get_lidar_data() -> None:
    """Test get_lidar_data for correct request and decoding."""
    await client_comm.connect_client('127.0.0.1', FIXED_PORT)
    pc, labels = await client_comm.get_lidar_data(0, 0)
    expected_pc = np.full((10, 3), 1.0, dtype=np.float32)
    expected_labels = np.full((10, 1), 2.0, dtype=np.float32)
    assert np.array_equal(pc, expected_pc)
    assert np.array_equal(labels, expected_labels)
    await client_comm.disconnect_client()


@pytest.mark.usefixtures('dummy_server')
@pytest.mark.asyncio
async def test_get_voxel_data() -> None:
    """Test get_voxel_data for correct request and decoding."""
    await client_comm.connect_client('127.0.0.1', FIXED_PORT)
    voxel, fov_mask, t_velo_2_cam = await client_comm.get_voxel_data(0, 0)
    expected_voxel = np.full(client_comm.VOXEL_SHAPE, 255, dtype=np.uint8)
    expected_fov = np.full(client_comm.FOV_MASK_SHAPE, fill_value=True, dtype=bool)
    expected_t = np.full(client_comm.T_VELO_2_CAM_SHAPE, 3.14, dtype=np.float64)
    assert np.array_equal(voxel, expected_voxel)
    assert np.array_equal(fov_mask, expected_fov)
    assert np.array_equal(t_velo_2_cam, expected_t)
    await client_comm.disconnect_client()


@pytest.mark.usefixtures('dummy_server')
@pytest.mark.asyncio
async def test_get_trajectory_data() -> None:
    """Test get_trajectory_data for correct request and decoding."""
    await client_comm.connect_client('127.0.0.1', FIXED_PORT)
    data = await client_comm.get_trajectory_data(0, 0)
    expected = np.array([7.0, 8.0, 9.0], dtype=np.float64)
    assert np.array_equal(data, expected)
    await client_comm.disconnect_client()


def test_decode_camera2_data() -> None:
    """Test the decode_camera2_data function directly."""
    shape = client_comm.CAMERA2_SHAPE
    rng = np.random.default_rng()
    original = rng.integers(0, 256, size=shape, dtype=np.uint8)
    compressed = bz2.compress(original.tobytes())
    decoded = client_comm.decode_camera2_data(compressed)
    assert np.array_equal(decoded, original)


def test_decode_camera3_data() -> None:
    """Test the decode_camera3_data function directly."""
    shape = client_comm.CAMERA3_SHAPE
    rng = np.random.default_rng()
    original = rng.integers(0, 256, size=shape, dtype=np.uint8)
    compressed = bz2.compress(original.tobytes())
    decoded = client_comm.decode_camera3_data(compressed)
    assert np.array_equal(decoded, original)


def test_decode_lidar_data() -> None:
    """Test the decode_lidar_data function directly."""
    rng = np.random.default_rng()
    dummy_pc = rng.random((10, 3)).astype(np.float32)
    dummy_labels = rng.random((10, 1)).astype(np.float32)
    combined = dummy_pc.tobytes() + b'__SPLIT__' + dummy_labels.tobytes()
    compressed = gzip.compress(combined)
    decoded_pc, decoded_labels = client_comm.decode_lidar_data(compressed)
    assert np.array_equal(decoded_pc, dummy_pc)
    assert np.array_equal(decoded_labels, dummy_labels)


def test_decode_voxel_message() -> None:
    """Test the decode_voxel_message function directly."""
    rng = np.random.default_rng()
    voxel = rng.integers(0, 256, size=client_comm.VOXEL_SHAPE, dtype=np.uint8)
    fov_mask = rng.integers(0, 2, size=client_comm.FOV_MASK_SHAPE, dtype=bool)
    t_velo_2_cam = rng.random(client_comm.T_VELO_2_CAM_SHAPE).astype(np.float64)
    combined = (
        voxel.tobytes() + b'__SPLIT__' + fov_mask.tobytes() + b'__SPLIT__' + t_velo_2_cam.tobytes()
    )
    compressed = gzip.compress(combined)
    decoded_voxel, decoded_fov_mask, decoded_t_velo_2_cam = client_comm.decode_voxel_message(
        compressed
    )
    assert np.array_equal(decoded_voxel, voxel)
    assert np.array_equal(decoded_fov_mask, fov_mask)
    assert np.array_equal(decoded_t_velo_2_cam, t_velo_2_cam)


def test_decode_trajectory_data() -> None:
    """Test the decode_trajectory_data function directly."""
    rng = np.random.default_rng()
    trajectory = rng.random(client_comm.TRAJECTORY_DIM).astype(np.float64)
    raw = trajectory.tobytes()
    decoded = client_comm.decode_trajectory_data(raw)
    assert np.array_equal(decoded, trajectory)
