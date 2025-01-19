# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Camera."""

from pathlib import Path

import cv2
import numpy as np
import pytest

# from sensorium.data_processing.camera.camera import load_images


def test_load_images(tmp_path: Path) -> None:
    """Test for the camera function."""
    height = 600
    width = 600

    # Creating the images
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
    temp_dir = tmp_path / 'temp_dir'
    temp_dir.mkdir()

    # Saving the images inside the temporary directory
    cv2.imwrite('imageRed.png', im_red)
    temp_red = temp_dir / 'imageRed.png'

    cv2.imwrite('imageBlue.png', im_blue)
    temp_blue = temp_dir / 'imageBlue.png'

    cv2.imwrite('imageGreen.png', im_green)
    temp_green = Path(temp_dir) / 'imageGreen.png'

    # Check if the temporary files exist
    # assert Path.exists(temp_red) == True
    # assert temp_file.is_file()

    # deleting temporary files (does not work for now.)
    Path.unlink(temp_red)


# load_images(temp_dir)
