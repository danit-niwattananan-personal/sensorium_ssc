# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import os
from pathlib import Path

import cv2


def load_images(dir):  # noqa: A002, ANN001, ANN201
    """Read images.

    Dir is the path to the image directory.
    The function returns a list with all frames.
    """
    dir = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images'  # noqa: A001
    image_paths = [Path(dir) / file for file in sorted(os.listdir(dir))]

    return [cv2.imread(str(path), cv2.IMREAD_UNCHANGED) for path in image_paths]


# for testing that the function works:
def iterate(list):
    yield from list


dir = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images'  # noqa: A001
frame_length = 300

for val in iterate(load_images(dir)):
    cv2.imshow('Camera', val)
    cv2.waitKey(frame_length)
