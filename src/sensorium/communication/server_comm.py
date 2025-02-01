# sensorium/communication/server_comm.py

# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""This module handles connection for client mode."""

import asyncio
import json
from collections.abc import Callable

import numpy as np
import websockets
from websockets.legacy.server import WebSocketServerProtocol

from sensorium.data_processing.engine.backend_engine import BackendEngine

connected_clients: list[WebSocketServerProtocol] = []

data_directory = '/home/mehin/dummy pyt/kitti_dummy/dataset'
backend_engine = BackendEngine(data_dir=data_directory, verbose=True)

async def handle_client(websocket: WebSocketServerProtocol) -> None:
    """Handle client connections and data requests."""
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            try:
                request = json.loads(message)
                sensor_type = request.get('sensor_type')
                seq_id = int(request.get('seq_id', -1))
                frame_id = int(request.get('frame_id', -1))

                response = create_response(sensor_type, seq_id, frame_id)
                await websocket.send(response)         #encode
            except (ValueError, KeyError, TypeError) as e:
                error_msg = {'error': f'Invalid request: {e!s}'}
                await websocket.send(error_msg)
    finally:
        connected_clients.remove(websocket)


def create_response(sensor_type: str, seq_id: int, frame_id: int) -> bytes:
    """Fetch and format data from BackendEngine as raw bytes."""
    data = backend_engine.process(seq_id, frame_id)

    try:
        if sensor_type == 'camera2':
            image_2 = data.get('image_2')
            if isinstance(image_2, np.ndarray):
                return image_2.tobytes()
            msg = 'Invalid data type for image_2'
            raise ValueError(msg)

        if sensor_type == 'camera3':
            image_3 = data.get('image_3')
            if isinstance(image_3, np.ndarray):
                return image_3.tobytes()
            msg = 'Invalid data type for image_3'
            raise ValueError(msg)

        if sensor_type == 'lidar':
            lidar_pc = data.get('lidar_pc')
            pc_labels = data.get('lidar_pc_labels')
            if isinstance(lidar_pc, np.ndarray) and isinstance(pc_labels, np.ndarray):
                return lidar_pc.tobytes() + b'||' + pc_labels.tobytes()
            msg = 'Invalid data type for lidar_pc or lidar_pc_labels'
            raise ValueError(msg)

        if sensor_type == 'voxel':
            voxel = data.get('voxel')
            if isinstance(voxel, np.ndarray):
                return voxel.tobytes()
            msg = 'Invalid data type for voxel'
            raise ValueError(msg)

        if sensor_type == 'trajectory':
            trajectory = data.get('trajectory')
            if trajectory is not None and isinstance(trajectory, np.ndarray):
                return trajectory.tobytes()
            msg = 'Invalid trajectory data'
            raise ValueError(msg)

    except KeyError as e:
        msg = f"Missing data for sensor type '{sensor_type}': {e!s}"
        raise ValueError(msg) from e

    msg = f'Unknown sensor type: {sensor_type}'
    raise ValueError(msg)


async def start_server(port: int, stop_event: asyncio.Event) -> None:
    """Start the WebSocket server."""
    print(f'Starting server on ws://localhost:{port}')
    server = await websockets.serve(handle_client, 'localhost', port)

    try:
        await stop_event.wait()
    finally:
        server.close()
        await server.wait_closed()
        print('Server stopped.')


async def stop_server(stop_event: asyncio.Event) -> None:
    """Stop the WebSocket server."""
    stop_event.set()

    for client in connected_clients:
        await client.close()

    print('All clients disconnected, server stopped.')


def get_server_control_functions() -> tuple[Callable[[int], None], Callable[[], None]]:
    """Return functions to start and stop the server."""
    stop_event = asyncio.Event()

    running_tasks: list[asyncio.Task[None]] = []

    def start(port: int) -> None:
        """Start the server."""
        task: asyncio.Task[None] = asyncio.create_task(start_server(port, stop_event))
        task.add_done_callback(handle_task_exception)
        running_tasks.append(task)

    def stop() -> None:
        """Stop the server."""
        task: asyncio.Task[None] = asyncio.create_task(stop_server(stop_event))
        task.add_done_callback(handle_task_exception)
        running_tasks.append(task)

    def handle_task_exception(task: asyncio.Task[None]) -> None:
        """Handle exceptions raised by tasks."""
        try:
            task.result()
        except asyncio.CancelledError:
            print('Task was cancelled.')
        except ValueError as e:
            print(f'ValueError occurred: {e}')
        except KeyError as e:
            print(f'KeyError occurred: {e}')
        except Exception as e:
            print(f'Unhandled exception in task: {e!s}')
            raise

    return start, stop

