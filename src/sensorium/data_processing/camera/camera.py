# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import os

import cv2


def load_images() -> None:
    """Load images."""
    frame_length = 500  # change for faster/slower
    dir1 = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/'
    'camera/dummy_data/kitti_sequence_00/images/'

    image_paths = [os.path.join(dir1, file) for file in sorted(os.listdir(dir1))]

    for path in image_paths:
        im = cv2.imread(path, cv2.IMREAD_COLOR)
        cv2.imshow('Camera', im)
        cv2.waitKey(frame_length)


load_images()
