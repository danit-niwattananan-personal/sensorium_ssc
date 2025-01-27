# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test Camera."""

import os
from pathlib import Path

import cv2
import numpy as np
import pytest

from sensorium.data_processing.camera.camera import load_frame


def test_load_images(tmp_path: Path) -> None:
    """Test for the camera function.

    Right now it tests the camera function that only loads one frame. Should be later changed.
    """
    height = 600
    width = 600

    # Creating the images (test data)
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

    # Create a temporary file paths within the temporary directory (tmp_path)
    temp_file_path_1 = tmp_path / 'imageRed.png'
    cv2.imwrite(temp_file_path_1, im_red)

    temp_file_path_2 = tmp_path / 'imageBlue.png'
    cv2.imwrite(temp_file_path_2, im_blue)

    temp_file_path_3 = tmp_path / 'imageGreen.png'
    cv2.imwrite(temp_file_path_3, im_green)

    # Assert that the files were created in the temporary directory
    assert temp_file_path_1.exists()
    assert temp_file_path_2.exists()
    assert temp_file_path_3.exists()

    # read the test data with opencv
    test_data_red = cv2.imread(str(temp_file_path_1), cv2.IMREAD_UNCHANGED)
    test_data_blue = cv2.imread(str(temp_file_path_2), cv2.IMREAD_UNCHANGED)
    test_data_green = cv2.imread(str(temp_file_path_3), cv2.IMREAD_UNCHANGED)

    # Assert that the data from the function matches the test data
    assert load_frame(tmp_path, temp_file_path_1) == test_data_red
    assert load_frame(tmp_path, temp_file_path_2) == test_data_green
    assert load_frame(tmp_path, temp_file_path_3) == test_data_blue

    # os.remove(temp_dir)
