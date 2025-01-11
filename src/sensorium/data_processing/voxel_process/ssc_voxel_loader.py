# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Functional Semantic Voxel loading APIs.

Code partly from Monoscene
https://github.com/astra-vision/MonoScene/blob/master/monoscene/data/semantic_kitti/preprocess.py
"""

from pathlib import Path

import numpy as np
from numpy.typing import NDArray

import sensorium.data_processing.utils.io_data as semkitti_io

from . import fusion


def load_ssc_voxel(
    sequence_path: str,
    sequence_id: str,
    frame_id: str,
    remap_lut: NDArray[np.int32],
) -> NDArray[np.uint8]:
    """Load a SINGLE SSC voxel data from the given path.

    Args:
        sequence_path: path to the sequence directory.
        sequence_id: the sequence id.
        frame_id: the frame id.
        remap_lut: the remap Numpy array to remap the label to training format.

    Returns:
        voxel: the voxel data.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    # Make sure that frame_id does not have extension scale
    frame_id = frame_id.split('_')[0]

    # Construct the path
    label_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.label'
    invalid_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.invalid'

    # Check if path exists
    if not label_path.exists() or not invalid_path.exists():
        _path_error = f'File {label_path} or {invalid_path} not found'
        raise FileNotFoundError(_path_error)

    # Load using API
    label = semkitti_io.read_label_semantickitti(str(label_path))
    invalid = semkitti_io.read_invalid_semantickitti(str(invalid_path))

    # Remap the label
    label = remap_lut[label.astype(np.uint16)].astype(np.float32)
    label[np.isclose(invalid, 1)] = 255  # Setting unknown voxels marked by invalid mask to 255
    return label.reshape((256, 256, 32)).astype(np.uint8)


def read_calib(calib_path: str) -> dict[str, NDArray[np.float64]]:
    """Load the camera intrinsic and extrinsic matrices."""
    calib_data = {}
    with Path(calib_path).open() as f:
        for line in f:
            if line == '\n':
                break
            key, value = line.strip().split(':', 1)
            calib_data[key] = np.array([float(v) for v in value.split()])

    ret = {}
    ret['P2'] = calib_data['P2'].reshape(3, 4)  # 3x4 projection matrix for left camera
    ret['Tr'] = np.identity(4)
    ret['Tr'][:3, :4] = calib_data['Tr'].reshape(3, 4)
    return ret


def vox2pix(
    cam_e: NDArray[np.float64],
    cam_k: NDArray[np.float64],
    vol_origin: NDArray[np.float64],
    img_shape: tuple[int, int],
    scene_size: tuple[float, float, float],
) -> tuple[NDArray[np.int64], NDArray[np.bool_], NDArray[np.float32]]:
    """Compute the 2D projection of voxels centroids.

    Args:
        cam_e: (4, 4)
            transformation from camera to lidar coordinate in case of SemKITTI
        cam_k: (3, 3)
            camera intrinsics
        vol_origin: (3,)
            lidar(SemKITTI) cooridnates of the voxel at index (0, 0, 0)
        img_shape: (image width, image height)
        scene_size: (3,)
            scene size in meter: (51.2, 51.2, 6.4) for SemKITTI

    Returns:
        projected_pix: (N, 2)
            Projected 2D positions of voxels
        fov_mask: (N,)
            Voxels mask indice voxels inside image's FOV
        pix_z: (N,)
            Voxels' distance to the sensor in meter
    """
    # Set the meta data
    vox_size = 0.2
    # Compute the x, y, z bounding of the scene in meter
    vol_bnds = np.zeros((3, 2))
    vol_bnds[:, 0] = vol_origin
    vol_bnds[:, 1] = vol_origin + np.array(scene_size)

    # Compute the voxels centroids in lidar cooridnates
    vol_dim = np.ceil((vol_bnds[:, 1] - vol_bnds[:, 0]) / vox_size).copy(order='C').astype(int)
    xv, yv, zv = np.meshgrid(range(vol_dim[0]), range(vol_dim[1]), range(vol_dim[2]), indexing='ij')
    vox_coords = (
        np.concatenate([xv.reshape(1, -1), yv.reshape(1, -1), zv.reshape(1, -1)], axis=0)
        .astype(int)
        .T
    )

    # Project voxels' centroid from lidar coordinates to camera coordinates
    cam_pts = fusion.TSDFVolume.vox2world(vol_origin, vox_coords, vox_size)
    cam_pts = fusion.rigid_transform(cam_pts, cam_e)

    # Project camera coordinates to pixel positions
    projected_pix = fusion.TSDFVolume.cam2pix(cam_pts, cam_k)
    pix_x, pix_y = projected_pix[:, 0], projected_pix[:, 1]

    # Eliminate pixels outside view frustum
    pix_z = cam_pts[:, 2]
    img_w, img_h = img_shape
    fov_mask = np.logical_and(
        pix_x >= 0,
        np.logical_and(
            pix_x < img_w, np.logical_and(pix_y >= 0, np.logical_and(pix_y < img_h, pix_z > 0))
        ),
    ).astype(np.bool_)

    return projected_pix, fov_mask, pix_z
