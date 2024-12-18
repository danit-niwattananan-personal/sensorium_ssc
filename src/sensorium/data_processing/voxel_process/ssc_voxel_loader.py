# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Semantic Voxel Loader."""

import numpy as np
from numpy.typing import NDArray
from torch.utils.data import Dataset


class SSCVoxelLoader(Dataset[NDArray[np.float32]]):
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
        # @Danit: Implement the loader
        self.data_dir = data_dir
        self.sequence_id = sequence_id
        self.frame_id = frame_id
        self.frequency = frequency
