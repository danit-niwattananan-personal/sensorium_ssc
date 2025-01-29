# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test the semantic voxel loader and their APIs."""
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
    sequence_path = str(Path(config['backend_engine']['data_dir']) / 'sequences')
    sequence_id = '00'
    frame_id = '111110'
    label_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.label'
    invalid_path = Path(sequence_path) / sequence_id / 'voxels' / f'{frame_id}.invalid'

@pytest.mark.parametrize(
    ('sequence_path', 'sequence_id', 'frame_id'),
    [
        ('test_sequence', '00', '000000'), # Incorrect sequence_path
        (sequence_path, '1000', '000000'), # Incorrect sequence_id
        (sequence_path, '00', '11'), # Incorrect frame_id
    ],
)
def test_file_not_found(sequence_path: str, sequence_id: str, frame_id: str) -> None:
    """The loader must raise FileNotFoundError if the file from given arguments is not found."""
    with pytest.raises(FileNotFoundError):
        load_ssc_voxel(sequence_path, sequence_id, frame_id, np.array([]))

def create_mock_voxel_files(label_path: str, invalid_path: str) -> None:
    """Create a mock voxel file for testing."""
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
        assert np.all(voxel_data.all() in config['semantic_kitti']['voxel_class_ids'])

    # Clean up
    finally:
        Path(label_path).unlink()
        Path(invalid_path).unlink()


def test_ssc_voxel_loader_with_invalid_data() -> None:
    """Semantic voxel loader must raise an error if the data is not in correct format."""
    print('Semantic voxel loader must raise an error if the data is not in correct format.')


def test_ssc_voxel_loader_with_invalid_frame_id() -> None:
    """Loader must raise an error if the frame_id is not in correct forma (divisible by 5)."""
    print('Loader must raise an error if the frame_id is not in correct forma (divisible by 5).')
