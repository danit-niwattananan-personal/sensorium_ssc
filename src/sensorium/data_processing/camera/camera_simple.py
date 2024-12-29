# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""A function that reads and shows each frame individually.

Left for testing. Should be later removed.
"""

import cv2


def camera_function() -> None:
    """A function that reads and showseach frame individually."""
    frame_length = 100  # change for faster/slower

    im = cv2.imread('dummy_data/images/02.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image2', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/03.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image3', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/04.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image4', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/05.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image5', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/06.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image6', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/07.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image7', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/08.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image8', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/09.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image9', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/10.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image10', im)
    cv2.waitKey(frame_length)
    cv2.destroyAllWindows()

    im = cv2.imread('dummy_data/images/11.png', cv2.IMREAD_COLOR)
    cv2.imshow('Image11', im)
    cv2.waitKey(0)  # wait for a key press to close the window


camera_function()
