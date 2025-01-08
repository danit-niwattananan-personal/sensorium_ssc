# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import os
from pathlib import Path

import cv2
from cv2.typing import MatLike

dir1 = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images'


def load_images(directory: str) -> list[MatLike]:
    """Read images.

    Dir is the path to the image directory.
    The function returns a list with all frames.
    """
    image_paths = [Path(directory) / file for file in sorted(os.listdir(directory))]

    return [cv2.imread(str(path), cv2.IMREAD_UNCHANGED) for path in image_paths]
