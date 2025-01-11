# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""First function function  reads and shows each frame individually.

Second function  reads and shows all frames in a loop.

Left for testing. Should be later removed.

"""

import os
from pathlib import Path

import cv2
import numpy as np


def camera() -> None:
    """Testing creation of image that is only red."""
    height = 600
    width = 600
    im_red = np.zeros((height, width, 3), np.uint8)
    im_red[:, :, 0] = 0
    im_red[:, :, 1] = 0
    im_red[:, :, 2] = 255

    cv2.imshow(' Image', im_red)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


camera()


def camera_function() -> None:
    """A function that reads and showseach frame individually."""
    frame_length = 200  # change for faster/slower

    im = cv2.imread('dummy_kitti/images/02.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image2', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    # Using cv2.imwrite() method for saving the image in the current folder
    filename = 'Frame2.jpg'
    cv2.imwrite(filename, im)

    im = cv2.imread('dummy_kitti/images/03.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image3', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/04.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image4', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/05.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image5', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/06.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image6', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/07.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image7', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/08.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image8', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/09.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image9', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/10.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image10', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_kitti/images/11.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image11', im)
    cv2.waitKey(0)  # wait for a key press to close the window


camera_function()


def load_images() -> None:
    """Load images."""
    frame_length = 300  # change for faster/slower
    dir1 = '/Users/antonijakrajcheva/b/src/sensorium/data_processing/camera/dummy_kitti/images'
    image_paths = [Path(dir1) / file for file in sorted(os.listdir(dir1))]

    for path in image_paths:
        im = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        cv2.imshow('Camera', im)
        cv2.waitKey(frame_length)


load_images()
