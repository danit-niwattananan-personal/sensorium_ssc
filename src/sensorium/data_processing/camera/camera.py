# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import cv2

"""load images"""

im = cv2.imread(
    '/Users/antonijakrajcheva/Desktop/kitti_dummy_camera/kitti_sequence_00/images/1.png',
    cv2.IMREAD_COLOR,
)
cv2.imshow('Image1', im)
cv2.waitKey(5000)
