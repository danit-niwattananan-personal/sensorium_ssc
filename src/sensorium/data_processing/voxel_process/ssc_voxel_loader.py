# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Functional Semantic Voxel loading APIs.

Code partly from Monoscene
https://github.com/astra-vision/MonoScene/blob/master/monoscene/data/semantic_kitti/preprocess.py
"""

from pathlib import Path

import numpy as np
from numpy.typing import NDArray

import sensorium.data_processing.utils.io_data as semkitti_io


def load_ssc_voxel(
    sequence_path: str,
    sequence_id: str,
    frame_id: str,
    remap_lut: NDArray[np.int32],
) -> NDArray[np.uint8]:
    """Load a SINGLE SSC voxel data from the given path.

    Args:
        sequence_path: path to the sequence directory.
        sequence_id: the sequence id.
        frame_id: the frame id.
        remap_lut: the remap Numpy array to remap the label to training format.

    Returns:
        voxel: the voxel data.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    # Make sure that frame_id does not have extension scale
    frame_id = frame_id.split('_')[0]

    # Construct the path
    label_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.bin'
    invalid_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.invalid'

    # Check if path exists
    if not label_path.exists() or not invalid_path.exists():
        _path_error = f'File {label_path} or {invalid_path} not found'
        raise FileNotFoundError(_path_error)

    # Load using API
    label = semkitti_io.read_label_semantickitti(str(label_path))
    invalid = semkitti_io.read_label_semantickitti(str(invalid_path))

    # Remap the label
    label = remap_lut[label.astype(np.uint16)].astype(np.float32)
    label[np.isclose(invalid, 1)] = 255  # Setting unknown voxels marked by invalid mask to 255
    return label.reshape((256, 256, 32)).astype(np.uint8)
