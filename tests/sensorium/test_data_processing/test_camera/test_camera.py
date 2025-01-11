# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Camera."""

import os
from pathlib import Path

import cv2
import numpy as np

# from sensorium.data_processing.camera.camera import load_images


def test_load_images(tmp_path: Path) -> None:
    """Test for the camera function."""
    height = 600
    width = 600

    # creating the images
    im_red = np.zeros((height, width, 3), np.uint8)
    im_red[:, :, 0] = 0
    im_red[:, :, 1] = 0
    im_red[:, :, 2] = 255

    im_blue = np.zeros((height, width, 3), np.uint8)
    im_blue[:, :, 0] = 255
    im_blue[:, :, 1] = 0
    im_blue[:, :, 2] = 0

    im_green = np.zeros((height, width, 3), np.uint8)
    im_green[:, :, 0] = 0
    im_green[:, :, 1] = 255
    im_green[:, :, 2] = 0

    # Using tmp_path to create a temporary directory
    temp_dir = tmp_path / 'my_temp_dir'
    temp_dir.mkdir()

    # pathlib.Path.mkdir(target_dir)

    # Saving the images inside the temporary directory
    file = cv2.imwrite('imageRed.png', im_red)
    temp_red = os.path.join(temp_dir, file)

    temp_blue = Path(temp_dir) / cv2.imwrite('imageBlue.png', im_blue)

    temp_green = Path(temp_dir) / cv2.imwrite('imageGreen.png', im_green)

    # Check if the temporary files exist
    assert temp_red.is_file()
    assert temp_blue.is_file()
    assert temp_green.is_file()

    # load_images(temp_dir)


# for file_path in Path.cwd().glob("*.txt"):
#     new_path = Path("archive") / file_path.name
#     file_path.rename(new_path)
# >>> Path.home().joinpath("python", "scripts", "test.py")
