"""Lidar pointcloud loader."""

from numpy import ndarray
from torch.utils.data import Dataset


# o3d.geometry.PointCloud did not pass Mypy since it can't generate stubs
class LidarPCLoader(Dataset[ndarray]):
    """Lidar pointcloud loader. Inherited mostly from PyTorch Dataset."""

    def __init__(
        self,
        data_dir: str,
        sequence_id: str,
        frame_id: int | list[int | str],
        frequency: float = 10.0,
    ) -> None:
        """Initialize the LidarPCLoader.

        Args:
            data_dir: The directory to the data.
            sequence_id: The sequence ID.
            frame_id: The frame ID.
            frequency: The frequency of the data.
        """
        # @Danit: Implement the loader
        self.data_dir = data_dir
        self.sequence_id = sequence_id
        self.frame_id = frame_id
        self.frequency = frequency
