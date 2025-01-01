# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import os
from pathlib import Path

import cv2


def load_images(dir: str) -> list:
    """Read images.

    Dir is the path to the image directory.
    The function returns a list with all frames.
    """
    dir = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images'
    image_paths = [Path(dir) / file for file in sorted(os.listdir(dir))]

    return [cv2.imread(str(path), cv2.IMREAD_UNCHANGED) for path in image_paths]
