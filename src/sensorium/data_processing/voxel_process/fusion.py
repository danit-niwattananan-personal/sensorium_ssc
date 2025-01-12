# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

r"""Adapted from https://github.com/andyzeng/tsdf-fusion-python/blob/master/fusion.py.

@inproceedings{zeng20163dmatch,
    title={3DMatch: Learning Local Geometric Descriptors from RGB-D Reconstructions},
    author={Zeng, Andy and Song, Shuran and Nie{\ss}ner, Matthias and Fisher, Matthew and Xiao,
    Jianxiong and Funkhouser, Thomas},
    booktitle={CVPR},
    year={2017}
}

Code adapted from Symphonies. Remove GPU C++ code.
"""

import numpy as np
from numba import njit, prange
from numpy.typing import NDArray


class TSDFVolume:
    """Volumetric TSDF Fusion of RGB-D Images."""

    def __init__(self, vol_bnds: NDArray[np.float32], voxel_size: float) -> None:
        """Constructor.

        Args:
          vol_bnds (ndarray): An ndarray of shape (3, 2). Specifies the
            xyz bounds (min/max) in meters.
          voxel_size (float): The volume discretization in meters.
        """
        vol_bnds = np.asarray(vol_bnds)
        assert vol_bnds.shape == (3, 2), '[!] `vol_bnds` should be of shape (3, 2).'

        # Define voxel volume parameters
        self._vol_bnds = vol_bnds
        self._voxel_size = float(voxel_size)
        self._trunc_margin = 5 * self._voxel_size  # truncation on SDF
        self._color_const = 256 * 256

        # Adjust volume bounds and ensure C-order contiguous
        self._vol_dim = (
            np.ceil((self._vol_bnds[:, 1] - self._vol_bnds[:, 0]) / self._voxel_size)
            .copy(order='C')
            .astype(int)
        )
        self._vol_bnds[:, 1] = self._vol_bnds[:, 0] + self._vol_dim * self._voxel_size
        self._vol_origin = self._vol_bnds[:, 0].copy(order='C').astype(np.float32)

        # Initialize pointers to voxel volume in CPU memory
        self._tsdf_vol_cpu = np.zeros(self._vol_dim).astype(np.float32)
        # for computing the cumulative moving average of observations per voxel
        self._weight_vol_cpu = np.zeros(self._vol_dim).astype(np.float32)
        self._color_vol_cpu = np.zeros(self._vol_dim).astype(np.float32)

        # Get voxel grid coordinates
        xv, yv, zv = np.meshgrid(
            range(self._vol_dim[0]), range(self._vol_dim[1]), range(self._vol_dim[2]), indexing='ij'
        )
        self.vox_coords = (
            np.concatenate([xv.reshape(1, -1), yv.reshape(1, -1), zv.reshape(1, -1)], axis=0)
            .astype(int)
            .T
        )

    @staticmethod
    @njit(parallel=True)  # type: ignore[misc]
    def vox2world(
        vol_origin: NDArray[np.float64],
        vox_coords: NDArray[np.float32],
        vox_size: float,
        offsets: tuple[float, float, float] = (0.5, 0.5, 0.5),
    ) -> NDArray[np.float32]:
        """Convert voxel grid coordinates to world coordinates."""
        vol_origin = vol_origin.astype(np.float32)
        vox_coords = vox_coords.astype(np.float32)
        cam_pts = np.empty_like(vox_coords, dtype=np.float32)
        for i in prange(vox_coords.shape[0]):
            for j in range(3):
                cam_pts[i, j] = vol_origin[j] + vox_size * vox_coords[i, j] + vox_size * offsets[j]
        return cam_pts

    @staticmethod
    @njit(parallel=True)  # type: ignore[misc]
    def cam2pix(
        cam_pts: NDArray[np.float32],
        intr: NDArray[np.float64],
    ) -> NDArray[np.int64]:
        """Convert camera coordinates to pixel coordinates."""
        intr = intr.astype(np.float32)
        fx, fy = intr[0, 0], intr[1, 1]
        cx, cy = intr[0, 2], intr[1, 2]
        pix = np.empty((cam_pts.shape[0], 2), dtype=np.int64)
        for i in prange(cam_pts.shape[0]):
            pix[i, 0] = int(np.round((cam_pts[i, 0] * fx / cam_pts[i, 2]) + cx))
            pix[i, 1] = int(np.round((cam_pts[i, 1] * fy / cam_pts[i, 2]) + cy))
        return pix


def rigid_transform(
    xyz: NDArray[np.float32],
    transform: NDArray[np.float64],
) -> NDArray[np.float32]:
    """Applies a rigid transform to an (N, 3) pointcloud."""
    xyz_h = np.hstack([xyz, np.ones((len(xyz), 1), dtype=np.float32)])
    xyz_t_h = np.dot(transform, xyz_h.T).T
    return np.astype(xyz_t_h[:, :3], np.float32)  # this format to suppress mypy
