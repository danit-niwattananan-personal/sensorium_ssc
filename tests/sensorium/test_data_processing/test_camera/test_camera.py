# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Camera."""

import os

import cv2

from sensorium.data_processing.camera.camera import load_images

# def test_load_images(tmp_path: Path) -> None:
#     im = cv2.imread('dummy_data/kitti_sequence_00/images/1.png', cv2.IMREAD_COLOR)
#     tmp_path = cv2.imwrite('im', )


# # for testing that the function works:
# def iterate(list1) -> list:
#     """Simple function for iteration through list."""
#     yield from list1

# for val in iterate(load_images(dir1)):
#     frame_length = 300
#     cv2.imshow('Camera', val)
#     cv2.waitKey(frame_length)


# def test_camera_function() -> None:
#     """Test for camera."""
#     dir1 = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images'
#     for file in sorted(os.listdir(dir1)):
#         assert image_paths == [Path(dir1) / file]
#         assert load_images(dir1) == [
#             cv2.imread(str(path), cv2.IMREAD_UNCHANGED) for path in [Path(dir1) / file]
#       ]
