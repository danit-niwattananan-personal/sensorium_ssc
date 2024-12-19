# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import cv2

"""load images"""


# folder_dir = 'dummy_data/kitti_sequence_00/images'
# for images in os.listdir(folder_dir):
#     if images.endswith('.png'):
#         im = cv2.imread(folder_dir, cv2.IMREAD_COLOR)
#         cv2.imshow('Window', im)
#         cv2.waitKey(3000)
#         cv2.destroyAllWindows()

# ______________________________________________
frame_length = 500  # change for faster/slower
im = cv2.imread('dummy_data/kitti_sequence_00/images/1.png', cv2.IMREAD_COLOR)
cv2.imshow('Image1', im)
cv2.waitKey(frame_length)
cv2.destroyAllWindows()

im = cv2.imread('dummy_data/kitti_sequence_00/images/2.png', cv2.IMREAD_COLOR)
cv2.imshow('Image2', im)
cv2.waitKey(frame_length)
cv2.destroyAllWindows()

im = cv2.imread('dummy_data/kitti_sequence_00/images/3.png', cv2.IMREAD_COLOR)
cv2.imshow('Image3', im)
cv2.waitKey(frame_length)
cv2.destroyAllWindows()

im = cv2.imread('dummy_data/kitti_sequence_00/images/4.png', cv2.IMREAD_COLOR)
cv2.imshow('Image4', im)
cv2.waitKey(frame_length)
cv2.destroyAllWindows()

im = cv2.imread('dummy_data/kitti_sequence_00/images/5.png', cv2.IMREAD_COLOR)
cv2.imshow('Image5', im)
cv2.waitKey(frame_length)
cv2.destroyAllWindows()

im = cv2.imread('dummy_data/kitti_sequence_00/images/6.png', cv2.IMREAD_COLOR)
cv2.imshow('Image6', im)
cv2.waitKey(0)  # wait for a key press to close the window
