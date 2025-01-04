# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""APIs for reading semantic kitti data.

Code adapted from
https://github.com/astra-vision/MonoScene/blob/master/monoscene/data/semantic_kitti/io_data.py.
"""

from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray


def unpack(compressed: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """Given a bit encoded voxel grid, make a normal voxel grid out of it."""
    uncompressed = np.zeros(compressed.shape[0] * 8, dtype=np.uint8)
    uncompressed[::8] = compressed[:] >> 7 & 1
    uncompressed[1::8] = compressed[:] >> 6 & 1
    uncompressed[2::8] = compressed[:] >> 5 & 1
    uncompressed[3::8] = compressed[:] >> 4 & 1
    uncompressed[4::8] = compressed[:] >> 3 & 1
    uncompressed[5::8] = compressed[:] >> 2 & 1
    uncompressed[6::8] = compressed[:] >> 1 & 1
    uncompressed[7::8] = compressed[:] & 1

    return uncompressed


def read_semantickitti(
    path: str,
    dtype: np.dtype[np.uint8] | np.dtype[np.float32] | np.dtype[np.uint16],
    do_unpack: bool | None,
) -> NDArray[np.uint8] | NDArray[np.float32]:
    """Read the voxel data from supported file format.

    Args:
        path: path to the voxel data file.
        dtype: the data type of the voxel data.
        do_unpack: whether to unpack the voxel data.

    Returns:
        voxel_data: the voxel data.
    """
    bin_ = np.fromfile(path, dtype=dtype)  # Flattened array
    if do_unpack:
        bin_ = unpack(bin_.astype(np.uint8))
        return bin_.astype(np.uint8)  # Split returns to pass mypy
    return bin_.astype(np.float32)


def read_label_semantickitti(path: str) -> NDArray[np.float32]:
    """Return label values of semantic kitti.

    Args:
        path: path to the label file.

    Returns:
        label: label of semantic kitti.
    """
    return read_semantickitti(path, dtype=np.dtype(np.uint16), do_unpack=False).astype(np.float32)


def read_invalid_semantickitti(path: str) -> NDArray[np.uint8]:
    """Return invalid positions of semantic kitti.

    Args:
        path: path to the invalid file.

    Returns:
        invalid: invalid values of semantic kitti.
    """
    return read_semantickitti(path, dtype=np.dtype(np.uint8), do_unpack=True).astype(np.uint8)


def read_occluded_semantickitti(path: str) -> NDArray[np.uint8]:
    """Return occluded positions of semantic kitti.

    Args:
        path: path to the occluded file.

    Returns:
        occluded: occluded values of semantic kitti.
    """
    return read_semantickitti(path, dtype=np.dtype(np.uint8), do_unpack=True).astype(np.uint8)


def read_occupancy_semantickitti(path: str) -> NDArray[np.float32]:
    """Return occupancy array of semantic kitti.

    Args:
        path: path to the occupancy file.

    Returns:
        occupancy: occupancy values of semantic kitti.
    """
    return read_semantickitti(path, dtype=np.dtype(np.uint8), do_unpack=True).astype(np.float32)


def read_pointcloud_semantickitti(path: str) -> NDArray[np.float32]:
    """Return pointcloud semantic kitti with remissions (x, y, z, intensity).

    Args:
        path: path to the pointcloud file.

    Returns:
        pointcloud: pointcloud semantic kitti with remissions (x, y, z, intensity).
    """
    pointcloud = read_semantickitti(path, dtype=np.dtype(np.float32), do_unpack=False).astype(
        np.float32
    )
    return pointcloud.reshape((-1, 4))


def get_remap_lut(path: str) -> NDArray[np.int32]:
    """Get remap_lut to remap classes of semantic kitti to be 20 classes.

    Args:
        path: path to the semantic kitti config file.

    Returns:
        remap_lut: remap_lut to remap classes of semantic kitti to be 20 classes.
    """
    with Path(path).open() as stream:
        dataset_config = yaml.safe_load(stream)

    # make lookup table for mapping
    maxkey = max(dataset_config['learning_map'].keys())

    # +100 hack making lut bigger just in case there are unknown labels
    remap_lut = np.zeros((maxkey + 100), dtype=np.int32)
    remap_lut[list(dataset_config['learning_map'].keys())] = list(
        dataset_config['learning_map'].values()
    )

    # in completion we have to distinguish empty and invalid voxels.
    # Important: For voxels 0 corresponds to "empty" and not "unlabeled".
    remap_lut[remap_lut == 0] = 255  # map 0 to 'invalid'
    remap_lut[0] = 0  # only 'empty' stays 'empty'.

    return remap_lut


def get_cmap_semantickitti20() -> NDArray[np.uint8]:
    """Get the color map for visualizing voxels ofsemantic kitti 20 classes."""
    return np.array(
        [
            # Empty voxel has color [0  , 0  , 0, 255],
            [100, 150, 245, 255],
            [100, 230, 245, 255],
            [30, 60, 150, 255],
            [80, 30, 180, 255],
            [100, 80, 250, 255],
            [255, 30, 30, 255],
            [255, 40, 200, 255],
            [150, 30, 90, 255],
            [255, 0, 255, 255],
            [255, 150, 255, 255],
            [75, 0, 75, 255],
            [175, 0, 75, 255],
            [255, 200, 0, 255],
            [255, 120, 50, 255],
            [0, 175, 0, 255],
            [135, 60, 0, 255],
            [150, 240, 80, 255],
            [255, 240, 150, 255],
            [255, 0, 0, 255],
        ]
    ).astype(np.uint8)
