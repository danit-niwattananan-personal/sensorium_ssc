"""Semantic Voxel Loader."""
from torch.utils.data import DataLoader

class SSCVoxelLoader(DataLoader):
    """Semantic Voxel Loader. Inherited mostly from PyTorch DataLoader."""
    def __init__(
        self,
        data_dir: str,
        sequence_id: str,
        frame_id: int | list[int | str],
        frequency: float = 1.0,
    ):
        super().__init__(data_dir, sequence_id, frame_id, frequency)
        # TODO: Implement the loader
        self.data_dir = data_dir
        self.sequence_id = sequence_id
        self.frame_id = frame_id
        self.frequency = frequency

    
