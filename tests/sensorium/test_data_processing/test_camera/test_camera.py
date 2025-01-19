# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Camera."""

from pathlib import Path

import cv2
import numpy as np
import pytest

from sensorium.data_processing.camera.camera import load_frame


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
    temp_green = temp_dir / 'imageGreen.png'

    # assert temp_red.is_file() //to check if the temporary file exists
    assert load_frame('temp_dir', 'imageRed.png') == cv2.imread(str(temp_red), cv2.IMREAD_UNCHANGED)

    # assert temp_blue.is_file()
    assert load_frame('temp_dir', 'imageBlue.png') == cv2.imread(
        str(temp_blue), cv2.IMREAD_UNCHANGED
    )

    # assert temp_green.is_file()
    assert load_frame('temp_dir', 'imageGreen.png') == cv2.imread(
        str(temp_green), cv2.IMREAD_UNCHANGED
    )


# code to delete temporary files?????
