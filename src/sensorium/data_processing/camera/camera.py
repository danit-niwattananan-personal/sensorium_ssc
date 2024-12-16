# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Camera."""

import cv2

# Trying OpenCV: object tracking
cap = cv2.VideoCapture(
    '/Users/antonijakrajcheva/Desktop/street.mp4'
)  # capture project that reads the frames from the video

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2()  # subtracts objects from a stable camera


while True:
    ret, frame = cap.read()

    # Object detectrion
    mask = object_detector.apply(frame)  # the mask makes everything we don't need black
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )  # extracting the boundaries of the white objects, i.e. the masks
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 400:
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    key = cv2.waitKey(30)
    if key == 27:
        break  # breaks the loop if we press 's' (27) on the keyboard

cap.release()
cv2.destroyAllWindows()
