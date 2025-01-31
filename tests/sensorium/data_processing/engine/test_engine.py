# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Test the backend engine. To be implemented."""

import shutil
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from sensorium.data_processing.engine.backend_engine import BackendEngine


def test_create_engine() -> None:
    """Engine must be instantiated with correct attributes."""
    engine = BackendEngine(data_dir='test')
    assert engine.data_dir == 'test'
    assert not engine.verbose

    assert engine.frequency == 10
    assert np.allclose(engine.voxel_origin, np.array((0, -25.6, -2)))
    assert engine.voxel_size == 0.2
    assert engine.scene_size == (51.2, 51.2, 6.4)
    assert engine.scene_dim == (256, 256, 32)
    assert engine.img_shape == (1220, 370)

    assert not engine.problem_load_cam_2
    assert not engine.problem_load_cam_3
    assert not engine.problem_load_lidar_pc
    assert not engine.problem_load_lidar_label
    assert not engine.problem_load_trajectory
    assert not engine.problem_load_voxel

    assert isinstance(engine.buf_mem, dict)
    keys2check = [
        'image_2', 'image_3', 'lidar_pc', 'lidar_label', 'lidar_label_colors', 'trajectory'
    ]
    for key in keys2check:
        assert key in engine.buf_mem
        assert isinstance(engine.buf_mem[key], np.ndarray)


def test_process_static_data_nofile() -> None:
    """Method must raise FileNotFoundError if files are not found."""
    engine = BackendEngine(data_dir='test')
    check_msg = 'Cannot go further without loading trajectory and voxel.'
    with pytest.raises(FileNotFoundError, match=check_msg):
        engine.process_static_data(1)

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

def create_mock_pose_file(file_path: str) -> None:
    """Create a mock poses file for testing."""
    with Path(file_path).open('w') as f:
        f.write('1 0 0 1 0 1 0 2 0 0 1 3\n')
        f.write('1 0 0 4 0 1 0 5 0 0 1 6\n')

def test_return_static_data() -> None:
    """Method must return correct data format, values and types."""
    try:
        data_dir = str(Path.cwd() / 'tmp')
        sequence_path = Path(data_dir) / 'sequences' / '99'
        if not sequence_path.exists():
            sequence_path.mkdir(parents=True)
        calib_file = str(sequence_path / 'calib.txt')
        pose_file = str(sequence_path / 'poses.txt')
        create_mock_calib_file(calib_file)
        create_mock_pose_file(pose_file)

        engine = BackendEngine(data_dir=data_dir)
        result = engine.process_static_data(99)

        assert isinstance(result, dict)
        assert 'sequence_id' in result
        assert result['sequence_id'] == '99'

        assert 'fov_mask' in result
        assert result['fov_mask'].shape == np.prod(engine.scene_dim)  # type: ignore[union-attr]
        assert result['fov_mask'].dtype == np.bool_  # type: ignore[union-attr]

        assert 't_velo_2_cam' in result
        assert result['t_velo_2_cam'].shape == (4, 4)  # type: ignore[union-attr]
        assert result['t_velo_2_cam'].dtype == np.float64  # type: ignore[union-attr]
        assert np.allclose(result['t_velo_2_cam'], np.eye(4))

        assert 'poses' in result
        assert len(result['poses']) == 2
        assert result['poses'][0].shape == (4, 4)  # type: ignore[union-attr]
        assert result['poses'][0].dtype == np.float64  # type: ignore[union-attr]
        assert np.allclose(result['poses'][0], np.array([
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1]
        ]))
        assert result['poses'][1].shape == (4, 4)  # type: ignore[union-attr]
        assert result['poses'][1].dtype == np.float64  # type: ignore[union-attr]
        assert np.allclose(result['poses'][1], np.array([
            [1, 0, 0, 4],
            [0, 1, 0, 5],
            [0, 0, 1, 6],
            [0, 0, 0, 1]
        ]))
    finally:
        Path(calib_file).unlink()
        Path(pose_file).unlink()
        shutil.rmtree(data_dir)

def create_mock_image_files(path: str, option: int = 0) -> None:
    """Create mock 3-channel image file for testing."""
    array = np.arange(27) if option == 0 else np.arange(-27, 0)
    array = array.reshape(3, 3, 3)
    array = array[:, :, ::-1] # Reverse the order of the channels to counteract PIL's default BGR
    data = Image.fromarray(array.astype(np.uint8))
    data.save(path)

def test_check_and_load_images(capsys: pytest.CaptureFixture[str]) -> None:
    """Method must load images if they exist, otherwise use buffer memory."""
    # images don't exist
    engine = BackendEngine(data_dir='test', verbose=True)
    loaded_image_2, loaded_image_3 = engine._check_and_load_images( # noqa: SLF001
        sequence_id='99',
        frame_id='111111'
    )
    # The data should be from the initialized buffer memory
    assert isinstance(loaded_image_2, np.ndarray)
    assert isinstance(loaded_image_3, np.ndarray)
    assert loaded_image_2.dtype == np.uint8
    assert loaded_image_3.dtype == np.uint8
    assert np.allclose(loaded_image_2, np.zeros((1,)))
    assert np.allclose(loaded_image_3, np.zeros((1,)))
    assert np.allclose(loaded_image_2, engine.buf_mem['image_2']) # type: ignore[arg-type]
    assert np.allclose(loaded_image_3, engine.buf_mem['image_3']) # type: ignore[arg-type]

    # Check the printing out
    assert engine.problem_load_cam_2
    assert engine.problem_load_cam_3
    captured = capsys.readouterr()
    expected_output = """
            img_2 frame 111111 loaded successfully: False
            img_3 frame 111111 loaded successfully: False
            """
    assert captured.out.strip() == expected_output.strip()

    # Both images exist
    try:
        data_dir = str(Path.cwd() / 'tmp')
        image2_path = Path(data_dir) / 'sequences' / '99' / 'image_2'
        image3_path = Path(data_dir) / 'sequences' / '99' / 'image_3'
        if not image2_path.exists():
            image2_path.mkdir(parents=True)
        if not image3_path.exists():
            image3_path.mkdir(parents=True)
        create_mock_image_files(str(image2_path / '111111.png'))
        create_mock_image_files(str(image3_path / '111111.png'))
        engine = BackendEngine(data_dir=data_dir)
        loaded_image_2, loaded_image_3 = engine._check_and_load_images( # noqa: SLF001
            sequence_id='99',
            frame_id='111111'
        )
        assert isinstance(loaded_image_2, np.ndarray)
        assert isinstance(loaded_image_3, np.ndarray)
        assert loaded_image_2.shape == (3, 3, 3)
        assert loaded_image_3.shape == (3, 3, 3)
        # Loaded image is correct, and buffer memory is updated
        assert np.allclose(loaded_image_2, np.arange(27).reshape(3, 3, 3))
        assert np.allclose(loaded_image_3, np.arange(27).reshape(3, 3, 3))
        assert np.allclose(loaded_image_2, engine.buf_mem['image_2']) # type: ignore[arg-type]
        assert np.allclose(loaded_image_3, engine.buf_mem['image_3']) # type: ignore[arg-type]
        assert not engine.problem_load_cam_2
        assert not engine.problem_load_cam_3

        # If load another frame that doesn't exist, should get the buffer memory value
        loaded_image_2, loaded_image_3 = engine._check_and_load_images( # noqa: SLF001
            sequence_id='99',
            frame_id='222222'
        )
        assert np.allclose(loaded_image_2, engine.buf_mem['image_2']) # type: ignore[arg-type]
        assert np.allclose(loaded_image_3, engine.buf_mem['image_3']) # type: ignore[arg-type]
        assert engine.problem_load_cam_2
        assert engine.problem_load_cam_3
    finally:

        shutil.rmtree(data_dir)


def test_spin_engine() -> None:
    """Engine must spin until the end of the data, get interrupted, or new signal is received."""
    pr_str = """Engine must be able to spin until the end of the data, or get interrupted,
    or new signal is received."""
    print(pr_str)
