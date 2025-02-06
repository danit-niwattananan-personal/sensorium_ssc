# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""This module handles connection for client mode."""

import asyncio
import bz2
import gzip
import json
from typing import TYPE_CHECKING

import numpy as np
import websockets
from numpy.typing import NDArray
from websockets.exceptions import WebSocketException

if TYPE_CHECKING:
    from websockets.legacy.client import WebSocketClientProtocol


class ClientManager:
    """Manages the WebSocket connection and data requests."""

    def __init__(self) -> None:
        """Initialize ClientManager."""
        self._client: WebSocketClientProtocol | None = None
        self.sem = asyncio.Semaphore(1)

    async def connect(self, ip: str, port: int) -> None:
        """Establish a connection to the server."""
        uri = f'ws://{ip}:{port}'
        try:
            print(f'Connecting to {uri}...')
            self._client = await websockets.connect(uri, max_size=2_097_152)  # type: ignore[assignment]
            print('Client connected.')
        except WebSocketException as e:
            msg = f'Failed to connect to {uri}: {e!s}'
            raise ConnectionError(msg) from e

    async def disconnect(self) -> None:
        """Close the WebSocket connection."""
        if self._client:
            try:
                await self._client.close()
                self._client = None
                print('Client disconnected.')
            except WebSocketException as e:
                print(f'Error while disconnecting: {e!s}')
        else:
            print('No active connection to disconnect.')

    async def send_request(self, sensor_type: str, sequence_id: int, frame_id: int) -> bytes:
        """Send a request to the server and fetch the data."""
        if not self._client:
            msg = 'Client is not connected.'
            raise ConnectionError(msg)

        request_message = json.dumps(
            {'sensor_type': sensor_type, 'seq_id': sequence_id, 'frame_id': frame_id}
        )

        try:
            print(f'Sending request: {request_message}')
            await self._client.send(request_message)
            print('Request sent.')
            response = await self._client.recv()
            print('Response received.')
            if isinstance(response, str):
                response = response.encode()

        except WebSocketException as e:
            msg = f'Communication error: {e!s}'
            raise RuntimeError(msg) from e
        else:
            return response

    async def get_data(
        self, sensor_type: str, sequence_id: int, frame_id: int, result: dict[str, bytes]
    ) -> None:
        """Fetch data for a specific sensor."""
        async with self.sem:
            result['data'] = await self.send_request(sensor_type, sequence_id, frame_id)


_client_manager = ClientManager()


async def connect_client(ip: str, port: int) -> None:
    """Establish a client connection."""
    await _client_manager.connect(ip, port)


async def disconnect_client() -> None:
    """Disconnect the client."""
    await _client_manager.disconnect()


CAMERA2_SHAPE = (370, 1226, 3)  # resolution for camera2
CAMERA3_SHAPE = (370, 1226, 3)  # resolution for camera3
LIDAR_POINT_DIM = 3
LIDAR_LABEL_DIM = 1
VOXEL_SHAPE = (256, 256, 32)
FOV_MASK_SHAPE = (2097152,)  # (256, 256, 32)
T_VELO_2_CAM_SHAPE = (4, 4)
TRAJECTORY_DIM = 3


def decode_camera2_data(raw_data: bytes) -> NDArray[np.uint8]:
    """Decode raw bytes into a numpy array for camera2."""
    decompressed_data = bz2.decompress(raw_data)
    return np.frombuffer(decompressed_data, dtype=np.uint8).reshape(CAMERA2_SHAPE)


def decode_camera3_data(raw_data: bytes) -> NDArray[np.uint8]:
    """Decode raw bytes into a numpy array for camera3."""
    decompressed_data = bz2.decompress(raw_data)
    return np.frombuffer(decompressed_data, dtype=np.uint8).reshape(CAMERA3_SHAPE)


def decode_lidar_data(raw_data: bytes) -> tuple[NDArray[np.float32], NDArray[np.float32]]:
    """Decode raw bytes into point cloud and labels."""
    decompressed_data = gzip.decompress(raw_data)
    print(f'Raw lidar data length: {len(raw_data)}')
    print(f"Occurrences of b'__SPLIT__': {raw_data.count(b'__SPLIT__')}")
    split_data = decompressed_data.split(b'__SPLIT__')
    print(f'Split data length: {len(split_data)}')
    if len(split_data) != 2:
        msg = f'Unexpected data format. Expected 2 parts, got {len(split_data)}.'
        raise ValueError(msg)
    lidar_pc_bytes, label_bytes = split_data
    lidar_pc = np.frombuffer(lidar_pc_bytes, dtype=np.float32).reshape(-1, LIDAR_POINT_DIM)
    labels = np.frombuffer(label_bytes, dtype=np.float32).reshape(-1, LIDAR_LABEL_DIM)
    return lidar_pc, labels


def decode_voxel_message(
    raw_data: bytes,
) -> tuple[NDArray[np.uint8], NDArray[np.bool_], NDArray[np.float64]]:
    """Decode raw bytes into voxel data, fov_mask, and cam_pose."""
    decompressed_data = gzip.decompress(raw_data)
    split_data = decompressed_data.split(b'__SPLIT__')
    if len(split_data) != 3:
        msg = f'Unexpected voxel message format. Expected 3 parts, got {len(split_data)}.'
        raise ValueError(msg)
    voxel_bytes, fov_mask_bytes, t_velo_2_cam_bytes = split_data
    voxel = np.frombuffer(voxel_bytes, dtype=np.uint8).reshape(VOXEL_SHAPE)
    fov_mask = np.frombuffer(fov_mask_bytes, dtype=np.bool_).reshape(FOV_MASK_SHAPE)
    t_velo_2_cam = np.frombuffer(t_velo_2_cam_bytes, dtype=np.float64).reshape(T_VELO_2_CAM_SHAPE)
    return voxel, fov_mask, t_velo_2_cam


def decode_trajectory_data(raw_data: bytes) -> NDArray[np.float64]:
    """Decode raw bytes into a numpy array for trajectory."""
    return np.frombuffer(raw_data, dtype=np.float64).reshape(TRAJECTORY_DIM)


async def get_camera2_data(sequence_id: int, frame_id: int) -> NDArray[np.uint8]:
    """Fetch and decode camera2 data."""
    result: dict[str, bytes] = {}
    await _client_manager.get_data('camera2', sequence_id, frame_id, result)
    return decode_camera2_data(result['data'])


async def get_camera3_data(sequence_id: int, frame_id: int) -> NDArray[np.uint8]:
    """Fetch and decode camera3 data."""
    result: dict[str, bytes] = {}
    await _client_manager.get_data('camera3', sequence_id, frame_id, result)
    return decode_camera3_data(result['data'])


async def get_lidar_data(
    sequence_id: int, frame_id: int
) -> tuple[NDArray[np.float32], NDArray[np.float32]]:
    """Fetch and decode lidar data."""
    result: dict[str, bytes] = {}
    await _client_manager.get_data('lidar', sequence_id, frame_id, result)
    return decode_lidar_data(result['data'])


async def get_voxel_data(
    sequence_id: int, frame_id: int
) -> tuple[NDArray[np.uint8], NDArray[np.bool_], NDArray[np.float64]]:
    """Fetch and decode voxel data (including fov_mask and cam_pose)."""
    result: dict[str, bytes] = {}
    await _client_manager.get_data('voxel', sequence_id, frame_id, result)
    return decode_voxel_message(result['data'])


async def get_trajectory_data(sequence_id: int, frame_id: int) -> NDArray[np.float64]:
    """Fetch and decode trajectory data."""
    result: dict[str, bytes] = {}
    await _client_manager.get_data('trajectory', sequence_id, frame_id, result)
    return decode_trajectory_data(result['data'])
