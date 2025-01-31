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
        loaded_image_2_new, loaded_image_3_new = engine._check_and_load_images( # noqa: SLF001
            sequence_id='99',
            frame_id='222222'
        )
        assert np.allclose(loaded_image_2_new, engine.buf_mem['image_2']) # type: ignore[arg-type]
        assert np.allclose(loaded_image_3_new, engine.buf_mem['image_3']) # type: ignore[arg-type]
        assert engine.problem_load_cam_2
        assert engine.problem_load_cam_3
    finally:
        shutil.rmtree(data_dir)

def test_check_and_load_lidar_no_file(capsys: pytest.CaptureFixture[str]) -> None:
    """Method must use buffer memory if lidar files don't exist and print out correct message."""
    # images don't exist
    engine = BackendEngine(data_dir='test', verbose=True)

    loaded_lidar_pc, loaded_lidar_label, loaded_lidar_label_colors = engine._check_and_load_lidar( # noqa: SLF001
        sequence_id='99',
        frame_id='111111'
    )

    # The data should be from the initialized buffer memory
    assert isinstance(loaded_lidar_pc, np.ndarray)
    assert isinstance(loaded_lidar_label, np.ndarray)
    assert isinstance(loaded_lidar_label_colors, np.ndarray)
    assert loaded_lidar_pc.dtype == np.float32
    assert loaded_lidar_label.dtype == np.uint32
    assert loaded_lidar_label_colors.dtype == np.uint8
    assert np.allclose(loaded_lidar_pc, np.zeros((3,)))
    assert np.allclose(loaded_lidar_label, np.zeros((1,)))
    assert np.allclose(loaded_lidar_label_colors, np.zeros((4, 1)))
    assert np.allclose(loaded_lidar_pc, engine.buf_mem['lidar_pc']) # type: ignore[arg-type]
    assert np.allclose(loaded_lidar_label, engine.buf_mem['lidar_label']) # type: ignore[arg-type]
    assert np.allclose(loaded_lidar_label_colors, engine.buf_mem['lidar_label_colors']) # type: ignore[arg-type]

    # Check the printing out
    assert engine.problem_load_lidar_pc
    assert engine.problem_load_lidar_label
    captured = capsys.readouterr()
    expected_output = """
            pc frame 111111 loaded successfully: False
            label frame 111111 loaded successfully: False
            """

    assert captured.out.strip() == expected_output.strip()

def create_mock_lidar_file(path: str) -> None:
    """Create a mock lidar file for testing."""
    pointcloud_data = np.array(
        [
            [1.0, 2.0, 3.0, 0.5],
            [4.0, 5.0, 6.0, 1.0],
        ],
        dtype=np.float32,
    )
    pointcloud_data.tofile(path)

def create_mock_label_file(path: str) -> None:
    """Create a mock label file for testing."""
    labels = np.array([10, 20, 30], dtype=np.uint32)
    labels.tofile(path)

def test_check_and_load_lidar_exist() -> None:
    """Method must load lidar if it exists, otherwise use buffer memory."""
    try:
        data_dir = str(Path.cwd() / 'tmp')
        lidar_pc_path = Path(data_dir) / 'sequences' / '99' / 'velodyne'
        lidar_label_path = Path(data_dir) / 'sequences' / '99' / 'labels'
        if not lidar_pc_path.exists():
            lidar_pc_path.mkdir(parents=True)
        if not lidar_label_path.exists():
            lidar_label_path.mkdir(parents=True)
        create_mock_lidar_file(str(lidar_pc_path / '111111.bin'))
        create_mock_label_file(str(lidar_label_path / '111111.label'))
        engine = BackendEngine(data_dir=data_dir)

        loaded_lidar_pc, loaded_lidar_label, loaded_label_colors = engine._check_and_load_lidar( # noqa: SLF001
            sequence_id='99',
            frame_id='111111'
        )
        assert isinstance(loaded_lidar_pc, np.ndarray)
        assert isinstance(loaded_lidar_label, np.ndarray)
        assert isinstance(loaded_label_colors, np.ndarray)
        assert loaded_lidar_pc.shape == (2, 3)

        assert loaded_lidar_label.shape == (3,)
        assert loaded_label_colors.shape == (3, 3)
        assert loaded_lidar_pc.dtype == np.float32
        assert loaded_lidar_label.dtype == np.uint32
        assert loaded_label_colors.dtype == np.uint8

        # Loaded image is correct, and buffer memory is updated
        assert np.allclose(loaded_lidar_pc, np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]))
        assert np.allclose(loaded_lidar_label, np.array([10, 20, 30]))
        assert np.allclose(loaded_label_colors, np.array([
            [245, 150, 100],
            [255, 0, 0],
            [30, 30, 255],

        ]))
        assert np.allclose(loaded_lidar_pc, engine.buf_mem['lidar_pc']) # type: ignore[arg-type]
        assert np.allclose(loaded_lidar_label, engine.buf_mem['lidar_label']) # type: ignore[arg-type]
        assert np.allclose(loaded_label_colors, engine.buf_mem['lidar_label_colors']) # type: ignore[arg-type]
        assert not engine.problem_load_lidar_pc
        assert not engine.problem_load_lidar_label

        # If load another frame that doesn't exist, should get the buffer memory value
        loaded_pc_new, loaded_label_new, loaded_label_colors_new = engine._check_and_load_lidar( # noqa: SLF001
            sequence_id='99',
            frame_id='222222'
        )
        assert np.allclose(loaded_pc_new, engine.buf_mem['lidar_pc']) # type: ignore[arg-type]
        assert np.allclose(loaded_label_new, engine.buf_mem['lidar_label']) # type: ignore[arg-type]
        assert np.allclose(loaded_label_colors_new, engine.buf_mem['lidar_label_colors']) # type: ignore[arg-type]
        assert engine.problem_load_lidar_pc
        assert engine.problem_load_lidar_label
    finally:
        shutil.rmtree(data_dir)

def test_spin_engine() -> None:
    """Engine must spin until the end of the data, get interrupted, or new signal is received."""
    pr_str = """Engine must be able to spin until the end of the data, or get interrupted,
    or new signal is received."""
    print(pr_str)
