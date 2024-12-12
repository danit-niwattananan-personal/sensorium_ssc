"""Main engine for data processing which call unit loaders and unit processors."""

from pathlib import Path

from torch.utils.data import DataLoader, Dataset


class BackendEngine(DataLoader):
    """Main engine for data processing which call unit loaders and unit processors."""

    def __init__(
        self,
        cam_loader: Dataset,
        lidar_pc_loader: Dataset,
        trajectory_loader: Dataset,
        voxel_loader: Dataset,
        # **kwargs: dict,  # In case using config file to build the object
    ) -> None:
        """Initialize the BackendEngine.

        Args:
            cam_loader: The camera dataset.
            lidar_pc_loader: The lidar pointcloud dataset.
            trajectory_loader: The trajectory dataset.
            voxel_loader: The voxel dataset.
        """
        # @Danit: Import and use the real loaders
        self.cam_loader = cam_loader
        self.lidar_pc_loader = lidar_pc_loader
        self.trajectory_loader = trajectory_loader
        self.voxel_loader = voxel_loader

        # @Danit: Declare all meta data attributes
        self.frequency = 10  # Hz

    def process(self, frame_id: int | str) -> dict:
        """Call the loading methods of the loaders and pack them into a dict to be passed to COMM.

        Args:
            frame_id: The id of the frame to be processed.

        Returns:
            data: data dict to be passed to COMM with keys <sensor_name> and value <sensor_data>
            the data dict should contain all data of ONLY that frame.
        """
        # Meta data
        start_frame_id = int(frame_id)
        start_frame_id = f'{frame_id:06d}'  # 6 digits, from 4070 to 004070
        self.files = [
            f
            for f in Path(self.data_dir) / self.sequence_id / str(frame_id)
            if (curr_frame_id := int(f.name)) >= start_frame_id
        ]
        # The data itself in dict format
        frame_ids = []
        for _ in self.files:
            frame_ids.append(curr_frame_id)
            cam_data = self.cam_loader.load(curr_frame_id)
            lidar_pc_data = self.lidar_pc_loader.load(curr_frame_id)
            trajectory_data = self.trajectory_loader.load(curr_frame_id)
            voxel_data = self.voxel_loader.load(curr_frame_id)

        return {
            'frame_id': frame_ids,
            'timestamp': self.calculate_timestamp(frame_ids),
            'cam': cam_data,
            'lidar_pc': lidar_pc_data,
            'trajectory': trajectory_data,
            'voxel': voxel_data,
        }

    def calculate_timestamp(self, frame_id: int | str | list[int | str]) -> float:
        """Calculate the timestamp of the frame. # NOTE: Might move this to utils.

        Args:
            frame_id: The id (or ids) of the frame to be processed.

        Returns:
            timestamp: The timestamp of the frame.
        """
        if isinstance(frame_id, int | str):
            return float(int(frame_id) / self.frequency)
        return [float(int(f) / self.frequency) for f in frame_id]

    def collate_fn(self, data: dict[str, list[dict]]) -> list[dict]:
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
        return [
            {
                'frame_id': data['frame_id'][i],
                'timestamp': data['timestamp'][i],
                'cam': data['cam'][i],
                'lidar_pc': data['lidar_pc'][i],
                'trajectory': data['trajectory'][i],
                'voxel': data['voxel'][i],
            }
            for i in range(len(data['frame_id']))
        ]

    def spin(self) -> None:
        """Run the engine until the datastream ends, get interrupted, or new signal is received."""
        print('Spinning the engine...')  # To be implemented
