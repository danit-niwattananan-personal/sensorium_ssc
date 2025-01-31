# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test the semantic voxel loader and their APIs."""

import shutil
from pathlib import Path

import numpy as np
import pytest
import yaml

import sensorium.data_processing.utils.io_data as semkitti_io
from sensorium.data_processing.voxel_process.ssc_voxel_loader import (
    load_ssc_voxel,
    read_calib,
    vox2pix,
)

# Global config
config_path = Path.cwd() / 'configs' / 'sensorium.yaml'
with Path(config_path).open() as stream:
    config = yaml.safe_load(stream)
data_dir = str(Path.cwd() / 'tmp')
sequence_path = str(Path(data_dir) / 'sequences')
sequence_id = '99'
frame_id = '111110'
label_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.label'
invalid_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.invalid'


@pytest.mark.parametrize(
    ('sequence_path', 'sequence_id', 'frame_id'),
    [
        ('test_sequence', '00', '000000'),  # Incorrect sequence_path
        (sequence_path, '1000', '000000'),  # Incorrect sequence_id
        (sequence_path, '00', '11'),  # Incorrect frame_id
    ],
)
def test_file_not_found(sequence_path: str, sequence_id: str, frame_id: str) -> None:
    """The loader must raise FileNotFoundError if the file from given arguments is not found."""
    with pytest.raises(FileNotFoundError):
        load_ssc_voxel(sequence_path, sequence_id, frame_id, np.array([]))


def create_mock_voxel_files(label_path: str, invalid_path: str) -> None:
    """Create a mock voxel files for testing."""
    generator = np.random.default_rng(seed=12345)

    # Label data can only have values declared in configs/vox_semantic_kitti.yaml in labels
    with Path(Path.cwd() / 'configs' / 'vox_semantic_kitti.yaml').open() as stream:
        dataset_config = yaml.safe_load(stream)
    possible_labels = list(dataset_config['learning_map'].keys())
    label_data = generator.choice(
        np.array(possible_labels),
        size=int(np.prod(config['semantic_kitti']['grid_dims'])),
    )
    label_data = label_data.astype(np.uint16)
    label_data.tofile(label_path)

    # Invalid data can only have values 0 and 1
    invalid_data = generator.choice(
        np.array([0, 1]),
        size=262144,
    )
    invalid_data = invalid_data.astype(np.uint8)
    invalid_data.tofile(invalid_path)


def test_return_voxel_data() -> None:
    """The loader must return the data in correct type, shape, and value range."""
    # First, create the data
    try:
        if not Path(label_path).parent.exists():
            Path(label_path).parent.mkdir(parents=True)
        create_mock_voxel_files(str(label_path), str(invalid_path))

        # Then, load the data
        voxel_data = load_ssc_voxel(
            sequence_path,
            sequence_id,
            frame_id,
            semkitti_io.get_remap_lut(
                str(Path(Path.cwd()) / 'configs' / 'vox_semantic_kitti.yaml')
            ),
        )

        # Check the conditions
        assert voxel_data.dtype == np.uint8
        assert voxel_data.shape == tuple(config['semantic_kitti']['grid_dims'])
        assert np.all(np.isin(voxel_data, config['semantic_kitti']['voxel_class_ids']))

    # Clean up
    finally:
        if Path(data_dir).exists():
            shutil.rmtree(data_dir)


def create_mock_calib_file(file_path: str) -> None:
    """Create a mock calibration file for testing."""
    contents = [
        'P0: 1 0 0 0 0 1 0 0 0 0 1 0',
        'P1: 1 0 0 0 0 1 0 0 0 0 1 0',
        'P2: 1 0 0 0 0 1 0 0 0 0 1 0',
        'P3: 1 0 0 0 0 1 0 0 0 0 1 0',
        'Tr: 1 0 0 0 0 1 0 0 0 0 1 0',
        '',
        'Extra: 1 2 3 4 5 6 7 8 9 10 11 12',
    ]
    with Path(file_path).open('w') as f:
        f.write('\n'.join(contents))


def test_reading_calib_file() -> None:
    """The parsed calibration must return dict with correct keys and values in correct type."""
    try:
        create_mock_calib_file(str(Path(Path.cwd()) / 'calib_test.txt'))
        calib_data = read_calib(str(Path(Path.cwd()) / 'calib_test.txt'))
        # Check data type, and keys
        assert isinstance(calib_data, dict)
        keys_to_test = ['P2', 'Tr']
        for key in keys_to_test:
            assert key in calib_data
            assert isinstance(calib_data[key], np.ndarray)
            assert calib_data[key].dtype == np.float64

        # Check whether line break works
        assert 'Extra' not in calib_data

        # Check shapes and values
        assert calib_data['P2'].shape == (3, 4)
        assert calib_data['Tr'].shape == (4, 4)
        assert np.allclose(calib_data['Tr'], np.eye(4))
    finally:
        Path(str(Path(Path.cwd()) / 'calib_test.txt')).unlink()


def test_vox_to_pix() -> None:
    """The vox2pix must return the correct pixel coordinates, camera fox_mask, and pixel depth.

    The voxel positions are given by the transform, cam intrinsics, and scene/img size.
    """
    cam_e = np.eye(4)
    cam_k = np.array(
        [
            [718.856, 0, 607.1928],
            [0, 718.856, 185.2157],
            [0, 0, 1],
        ]
    )
    vol_origin = np.array([0, -25.6, -2])
    img_shape = (1220, 370)
    scene_size = (51.2, 51.2, 6.4)

    projected_pix, fov_mask, pix_z = vox2pix(cam_e, cam_k, vol_origin, img_shape, scene_size)

    # Check output types and shapes
    assert isinstance(projected_pix, np.ndarray)
    assert isinstance(fov_mask, np.ndarray)
    assert isinstance(pix_z, np.ndarray)
    assert projected_pix.shape[1] == 2  # [N, 2] shape
    assert fov_mask.shape[0] == projected_pix.shape[0]  # [N, ] shape
    assert pix_z.shape == fov_mask.shape  # [N, ] shape
    assert fov_mask.shape[0] == np.prod(config['semantic_kitti']['grid_dims'])  # N = num_all_voxels

    # Check the camera fov mask
    assert fov_mask.dtype == np.bool_
    valid_pixels = projected_pix[fov_mask]
    assert np.all(valid_pixels[:, 0] >= 0)  # x coordinates
    assert np.all(valid_pixels[:, 0] < img_shape[0])
    assert np.all(valid_pixels[:, 1] >= 0)  # y coordinates
    assert np.all(valid_pixels[:, 1] < img_shape[1])

    # Check the pixel depth
    assert pix_z.dtype == np.float32
    assert np.all(pix_z[fov_mask] >= 0)
    assert np.all(pix_z[fov_mask] < 100)  # cam should not have depth beyond 100m
