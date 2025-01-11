# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import os
from pathlib import Path

import cv2
from cv2.typing import MatLike

dir1 = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images/'
desired_frame = '02.png'


def load_frame(directory: str, desired: str) -> list[MatLike]:
    """Read only one desired frame and return it in a list."""
    image_paths = [Path(directory) / file for file in sorted(os.listdir(directory))]
    msg = 'Error'

    for path in image_paths:
        if path.match(desired):
            return [cv2.imread(str(path), cv2.IMREAD_UNCHANGED)]
    raise RuntimeError(msg)


# Initialize function in the following way:
load_frame(dir1, desired_frame)
