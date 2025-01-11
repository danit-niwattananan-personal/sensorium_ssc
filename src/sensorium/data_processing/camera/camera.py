# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import os
from pathlib import Path

import cv2
from cv2.typing import MatLike


def load_frame(directory: str, desired: str) -> list[MatLike]:
    """Read only one desired frame and return it in a list."""
    image_paths = [Path(directory) / file for file in sorted(os.listdir(directory))]
    msg = 'Error'

    for path in image_paths:
        if path.match(desired):
            return [cv2.imread(str(path), cv2.IMREAD_UNCHANGED)]
    raise RuntimeError(msg)


def load_single_img(directory: str, frame_id: str) -> MatLike:
    """Read only one desired frame and return it in a list."""
    img_path = str(Path(directory) / f'{frame_id}.png')
    return cv2.imread(img_path, cv2.IMREAD_UNCHANGED)


# Initialize function in the following way:
if __name__ == '__main__':
    dir1 = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images/'
    desired_frame = '02.png'
    load_frame(dir1, desired_frame)
