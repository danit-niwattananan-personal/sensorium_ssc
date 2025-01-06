# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Pointcloud Server Functions."""

import numpy as np
from numpy.typing import NDArray


def read_point_cloud(path: str) -> NDArray[np.float32]:
    """Reads point cloud data from a .bin file in the Semantic KITTI format.

    Args:
        path (str): The path to the .bin file containing point cloud data.

    Returns:
        np.ndarray: A numpy array of shape (N, 3) where N is the number of points,
                    and each point has the format [x, y, z].
    """
    # Read the .bin file which contains [x, y, z, intensity] for each point (float32)
    point_cloud = np.fromfile(path, dtype=np.float32)

    # Reshape the array to have 4 columns (x, y, z, intensity)
    point_cloud = point_cloud.reshape(-1, 4)

    # Extract only the x, y, z coordinates (first 3 columns)

    return point_cloud[:, :3]


def read_labels(path: str) -> NDArray[np.uint16]:
    """Reads ground truth labels from a .label file in the Semantic KITTI format.

    Args:
        path (str): The path to the .label file containing the label data.

    Returns:
        np.ndarray: A numpy array of shape (N,) where N is the number of points,
                    and each entry is a label (uint16) corresponding to a class.
    """
    # Read the .label file which contains the labels for each point (uint16)

    return np.fromfile(path, dtype=np.uint16)


def get_cmap() -> dict[int, list[int]]:
    """Returns the color map for the provided classes in the dataset."""
    
    # color map (BGR format)
    return {
        0: [0, 0, 0],  # unlabeled
        1: [0, 0, 255],  # outlier
        10: [245, 150, 100],  # car
        11: [245, 230, 100],  # bicycle
        13: [250, 80, 100],  # bus
        15: [150, 60, 30],  # motorcycle
        16: [255, 0, 0],  # on-rails
        18: [180, 30, 80],  # truck
        20: [255, 0, 0],  # other-vehicle
        30: [30, 30, 255],  # person
        31: [200, 40, 255],  # bicyclist
        32: [90, 30, 150],  # motorcyclist
        40: [255, 0, 255],  # road
        44: [255, 150, 255],  # parking
        48: [75, 0, 75],  # sidewalk
        49: [75, 0, 175],  # other-ground
        50: [0, 200, 255],  # building
        51: [50, 120, 255],  # fence
        52: [0, 150, 255],  # other-structure
        60: [170, 255, 150],  # lane-marking
        70: [0, 175, 0],  # vegetation
        71: [0, 60, 135],  # trunk
        72: [80, 240, 150],  # terrain
        80: [150, 240, 255],  # pole
        81: [0, 0, 255],  # traffic-sign
        99: [255, 255, 50],  # other-object
        252: [245, 150, 100],  # moving-car
        253: [200, 40, 255],  # moving-bicyclist
        254: [30, 30, 255],  # moving-person
        255: [90, 30, 150],  # moving-motorcyclist
        256: [255, 0, 0],  # moving-on-rails
        257: [250, 80, 100],  # moving-bus
        258: [180, 30, 80],  # moving-truck
        259: [255, 0, 0],  # moving-other-vehicle
}

def read_labels_and_colors(path: str) -> tuple[NDArray[np.uint32], NDArray[np.uint8]]:
    """Reads .label file and returns the label IDs and their corresponding colors.

    Args:
        path (str): The path to the .label file.

    Returns:
        tuple: A tuple containing:
             - labels (np.ndarray): A numpy array of label IDs.
             - label_colors (np.ndarray): A numpy array of the corresponding BGR colors.
    """
    labels = np.fromfile(path, dtype=np.uint32)  # Read labels as uint32
    cmap = get_cmap()  # Retrieve the color map as a dictionary

    # Map labels to colors, defaulting to black `[0, 0, 0]` if label is missing
    label_colors = np.array([cmap.get(label, [0, 0, 0]) for label in labels], dtype=np.uint8)

    return labels, label_colors  # Return labels and their BGR color values

