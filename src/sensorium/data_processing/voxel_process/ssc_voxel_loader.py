"""Semantic Voxel Loader."""

from numpy import ndarray
from torch.utils.data import Dataset


class SSCVoxelLoader(Dataset[ndarray]):
    """Semantic Voxel Loader. Inherited mostly from PyTorch DataLoader."""

    def __init__(
        self,
        data_dir: str,
        sequence_id: str,
        frame_id: int | list[int | str],
        frequency: float = 1.0,
    ) -> None:
        """Initialize the Semantic Voxel Loader.

        Args:
            data_dir: The directory to the data.
            sequence_id: The sequence id.
            frame_id: The frame id.
            frequency: The frequency.
        """
        super().__init__(data_dir, sequence_id, frame_id, frequency)
        # @Danit: Implement the loader
        self.data_dir = data_dir
        self.sequence_id = sequence_id
        self.frame_id = frame_id
        self.frequency = frequency
