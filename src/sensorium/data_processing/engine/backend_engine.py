# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Main engine for data processing which call unit loader functions."""

import os
from pathlib import Path


class BackendEngine:
    """Main engine for data processing which call unit loaders and unit processors."""

    def __init__(
        self,
        data_dir: str,
        sequence_id: int,
        # **kwargs: dict,  # In case using config file to build the object
    ) -> None:
        """Initialize the BackendEngine.

        Args:
            data_dir: the kitti root directory from which path to individual data type is formed.
            sequence_id: the sequence user wants to visualize from frontend.
        """
        # @Danit: Import and use the real loaders
        self.data_dir = data_dir
        self.sequence_id = sequence_id

        # @Danit: Declare all meta data attributes
        self.frequency = 10  # Hz

    def process(self, frame_id: int | str) -> dict[str, list[int] | list[float] | float | None]:
        """Call the loading methods of the loaders and pack them into a dict to be passed to COMM.

        Args:
            frame_id: The id of the frame to be processed.

        Returns:
            data: data dict to be passed to COMM with keys <sensor_name> and value <sensor_data>
            the data dict should contain all data of ONLY that frame.
        """
        # Meta data
        start_frame_id = str(frame_id)
        start_frame_id = f'{frame_id:06d}'  # 6 digits, from 4070 to '004070'
        sequence_id = str(self.sequence_id)
        sequence_id = f'{sequence_id:02d}'  # 2 digits, from 1 to '01'

        self.files = [
            f.split('_')[0]  # Get only base frame_id (e.g. '000000' from '000000_1_1')
            for f in os.listdir(Path(self.data_dir) / sequence_id / str(frame_id))
            if (curr_frame_id := int(f.split('_')[0])) >= int(start_frame_id)
        ]
        # The data itself in dict format
        frame_ids = []
        for _ in self.files:
            frame_ids.append(curr_frame_id)
            # Load the data
            cam_data = None  # self.cam_loader.load(curr_frame_id)
            lidar_pc_data = None  # self.lidar_pc_loader.load(curr_frame_id)
            trajectory_data = None  # self.trajectory_loader.load(curr_frame_id)
            voxel_data = None  # self.voxel_loader.load(curr_frame_id)

        return {
            'frame_id': frame_ids,
            'timestamp': self.calculate_timestamp(frame_ids),
            'cam': cam_data,
            'lidar_pc': lidar_pc_data,
            'trajectory': trajectory_data,
            'voxel': voxel_data,
        }

    def calculate_timestamp(
        self, frame_id: int | str | list[int] | list[str]
    ) -> float | list[float]:
        """Calculate the timestamp of the frame. # NOTE: Might move this to utils.

        Args:
            frame_id: The id (or ids) of the frame to be processed.

        Returns:
            timestamp: The timestamp of the frame.
        """
        if isinstance(frame_id, int | str):
            return float(int(frame_id) / self.frequency)
        return [float(int(f) / self.frequency) for f in frame_id]

    def collate_dictoflists(self, data: dict[str, list[dict[str, float]]]) -> None:
        """Collate data into a single list of dicts instead of dict of lists.

        Args:
            data: The data to be collated.

        Returns:
            collated_data: The collated data.

        Raises:
            AssertionError: If the length of the data is not equal to the length of frame_id.
        """
        for k, v in data.items():
            assert len(v) == len(
                data['frame_id']
            ), f'The length of {k} is not equal to the length of frame_id'
        # to be implemented
        print('Collating data...')

    def spin(self) -> None:
        """Run the engine until the datastream ends, get interrupted, or new signal is received."""
        print('Spinning the engine...')  # To be implemented

    def _check_arguments(self, frame_id: int | str) -> None:
        """Check the arguments passed to the engine in case there is corruption during COMM."""
        print('Checking arguments...')  # To be implemented
        if int(frame_id) % 5 != 0:
            _frame_id_error = 'Frame ID must be a multiple of 5 for SemanticKitti'
            raise ValueError(_frame_id_error)
        # Also check if sequence is in range 0 to 20
        # Check if path exists
