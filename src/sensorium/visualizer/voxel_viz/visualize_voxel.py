# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Functional Semantic Voxel visualization APIs."""

import numpy as np
from numpy.typing import NDArray


def visualize_semantic_voxel(
    voxel: NDArray[np.uint8],
) -> None:
    """Visualize a semantic voxel."""
    vox_origin = np.array([0, -25.6, -2])
    print(f'The voxel origin is {vox_origin}.')
    print(f'The voxel size is {voxel.shape}.')
