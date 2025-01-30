# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Main engine for data processing which call unit loader functions."""

from pathlib import Path

import numpy as np
import yaml
from cv2.typing import MatLike
from numpy.typing import NDArray

import sensorium.data_processing.utils.io_data as semkitti_io
from sensorium.data_processing.camera.camera import load_single_img
from sensorium.data_processing.lidar_pointcloud.point_cloud import (
    read_labels_and_colors,
    read_point_cloud,
)
from sensorium.data_processing.trajectory.traj import get_framepos_from_list, parse_poses
from sensorium.data_processing.voxel_process.ssc_voxel_loader import (
    load_ssc_voxel,
    read_calib,
    vox2pix,
)


class BackendEngine:
    """Main engine for data processing which call unit loaders and unit processors."""

    def __init__(
        self,
        data_dir: str,
        *,
        verbose: bool = False,
        # **kwargs: dict,  # In case using config file to build the object
    ) -> None:
        """Initialize the BackendEngine.

        Args:
            data_dir: the kitti root directory from which path to individual data type is formed.
            verbose: whether to print debug messages.
        """
        # @Danit: Import and use the real loaders
        self.data_dir = data_dir
        self.verbose = verbose

        # @Danit: Declare all meta data attributes
        self.frequency = 10  # Hz
        self.voxel_origin = np.array((0, -25.6, -2))
        self.voxel_size = 0.2
        self.scene_size = (51.2, 51.2, 6.4)
        self.scene_dim = tuple(int(dim / self.voxel_size) for dim in self.scene_size)
        self.img_shape = (1220, 370)

        # Debugging variables
        self.problem_load_cam_2 = False
        self.problem_load_cam_3 = False
        self.problem_load_lidar_pc = False
        self.problem_load_lidar_label = False
        self.problem_load_trajectory = False
        self.problem_load_voxel = False

        # Initialize buffer memory. Don't use None to avoid type checking error.
        self.buf_mem = {
            'image_2': np.zeros((1,), dtype=np.uint8),
            'image_3': np.zeros((1,), dtype=np.uint8),
            'lidar_pc': np.zeros((3,), dtype=np.float32),
            'lidar_label': np.zeros((1,), dtype=np.uint32),
            'lidar_label_colors': np.zeros((4, 1), dtype=np.uint8),
            'trajectory': np.zeros((3, 1), dtype=np.float64),
        }

    def process_static_data(
        self,
        sequence_id: int | str,
    ) -> dict[str, str | list[NDArray[np.float64]] | NDArray[np.float64] | NDArray[np.bool_]]:
        """Process the data that takes long time, but only needs to be done once every sequence."""
        # Meta data
        sequence_id = f'{int(sequence_id):02d}'  # 2 digits, from 1 to '01'
        calib_file_path = str(Path(self.data_dir) / 'sequences' / sequence_id / 'calib.txt')
        poses_file_path = str(Path(self.data_dir) / 'sequences' / sequence_id / 'poses.txt')
        # Check if the file exists
        if not Path(calib_file_path).exists() or not Path(poses_file_path).exists():
            _error_msg = f"""Cannot go further without loading trajectory and voxel.
            calib.txt or poses.txt not found in the path:
            {calib_file_path}
            {poses_file_path}
            """
            raise FileNotFoundError(_error_msg)

        # Calculate all static data
        all_calibs = read_calib(calib_file_path)
        cam_intrinsic = all_calibs['P2']
        t_velo_2_cam = all_calibs['Tr']  # cam_pose
        cam_k = cam_intrinsic[:3, :3]
        # NOTE: This code takes way too long to calculate for every frame
        # Solution: calculate once and save it as attribute of class, or use a cache
        _, fov_mask, _ = vox2pix(
            t_velo_2_cam, cam_k, self.voxel_origin, self.img_shape, self.scene_size
        )

        # NOTE: the calib_file and calibration_file contains information about sequence_id
        poses = parse_poses(poses_file_path, all_calibs)

        return {
            'sequence_id': sequence_id,
            'fov_mask': fov_mask,
            't_velo_2_cam': t_velo_2_cam,
            'poses': poses,
        }

    def process(
        self,
        sequence_id: int | str,
        frame_id: int | str,
    ) -> dict[
        str,
        (
            str
            | list[float]
            | float
            | NDArray[np.float64]
            | NDArray[np.float32]
            | NDArray[np.bool_]
            | MatLike
            | None
        ),
    ]:
        """Call the loading methods of the loaders and pack them into a dict to be passed to COMM.

        Args:
            sequence_id: the id of the sequence folder
            frame_id: The id of the frame to be processed.

        Returns:
            data: data dict to be passed to COMM with keys <sensor_name> and value <sensor_data>
            the data dict should contain all data of ONLY that frame.
        """
        # Meta data
        start_frame_id = str(frame_id)
        start_frame_id = f'{frame_id:06d}'  # 6 digits, from 4070 to '004070'
        sequence_id = f'{int(sequence_id):02d}'  # 2 digits, from 1 to '01'

        # If the sequence_id is changed or static data is not available, reprocess static data
        try:
            is_seq_id_equal = sequence_id == self.static_data['sequence_id']  # type: ignore[has-type]
        except AttributeError:
            is_seq_id_equal = False

        if not is_seq_id_equal:
            if self.verbose:
                print('Will send data from buffer memory if file of current frame not found')
                print(f'Processing static data for sequence {sequence_id} at frame {frame_id} ...')
            self.static_data = self.process_static_data(sequence_id=sequence_id)

        # Load the image
        image_2_frame, image_3_frame = self._check_and_load_images(sequence_id, start_frame_id)

        # Load the lidar point cloud and panoptic ground truth
        lidar_pc, pc_labels, pc_label_colors = self._check_and_load_lidar(
            sequence_id, start_frame_id
        )

        # Load the trajectory
        try:
            trajectory_data_dict = get_framepos_from_list(
                self.static_data['poses'],  # type: ignore[arg-type]
                int(start_frame_id),
            )
            xyz = np.array(
                [trajectory_data_dict['x'], trajectory_data_dict['y'], trajectory_data_dict['z']]
            )
            self.buf_mem['trajectory'] = xyz
        except IndexError:
            self.problem_load_trajectory = True
            xyz = np.asarray(self.buf_mem['trajectory'])

        if self.verbose:
            print(f"""
            traj frame {start_frame_id} loaded successfully: {not self.problem_load_trajectory}
            x,y,z: {xyz}
            """)

        # Load the voxel
        sequence_path = str(Path(self.data_dir) / 'sequences')
        # Check if frame_id is divisible by 5
        try:
            self._check_arguments(frame_id=start_frame_id)
            # If yes, load the voxel
            try:  # Check if config file exists and load the voxel
                voxel_data = load_ssc_voxel(
                    sequence_path,
                    sequence_id,
                    start_frame_id,
                    semkitti_io.get_remap_lut(
                        str(Path(Path.cwd()) / 'configs' / 'vox_semantic_kitti.yaml')
                    ),
                )
                self.buf_mem['voxel'] = voxel_data
            except FileNotFoundError:
                self.problem_load_voxel = True
                voxel_data = np.asarray(self.buf_mem['voxel'])
                if self.verbose:
                    print(f"""
                    voxel frame {start_frame_id} loaded successfully: {not self.problem_load_voxel}
                    """)

        except ValueError:
            # If no, assign None to voxel_related data
            voxel_data = None

        if self.verbose:
            print('=' * 40)

        return {
            'frame_id': start_frame_id,  # for checking error after transmission
            'sequence_id': sequence_id,  # for checking error after transmission
            'timestamp': self.calculate_timestamp(start_frame_id),
            'image_2': image_2_frame,
            'image_3': image_3_frame,
            'lidar_pc': lidar_pc,
            'lidar_pc_labels': pc_labels,
            'lidar_pc_label_colors': pc_label_colors,
            'trajectory': xyz,
            'voxel': voxel_data,
            # NOTE: type: ignore[dict-item] might be required since process_static_data
            # has different item types
            'fov_mask': self.static_data['fov_mask'],  # type: ignore[dict-item]
            't_velo_2_cam': self.static_data['t_velo_2_cam'],  # type: ignore[dict-item]
        }

    def _check_and_load_images(
        self,
        sequence_id: str,
        frame_id: str,
    ) -> tuple[MatLike | None, MatLike | None]:
        """Check if the image file exists, and load the image if yes.

        Otherwise, use buffer memory.
        """
        # Load the image
        image_2_dir = Path(self.data_dir) / 'sequences' / sequence_id / 'image_2'
        image_3_dir = Path(self.data_dir) / 'sequences' / sequence_id / 'image_3'
        # Check if the image file exists. If yes, load the image and update buffer.
        # If no, use buffer memory.
        # NOTE: try-except does not work since opencv only issue warning, but not error
        if (Path(image_2_dir) / f'{frame_id}.png').exists():
            image_2_frame = load_single_img(str(image_2_dir), frame_id)
            self.buf_mem['image_2'] = image_2_frame
        else:
            self.problem_load_cam_2 = True
            image_2_frame = np.asarray(self.buf_mem['image_2'])

        if (Path(image_3_dir) / f'{frame_id}.png').exists():
            image_3_frame = load_single_img(str(image_3_dir), frame_id)
            self.buf_mem['image_3'] = image_3_frame
        else:
            self.problem_load_cam_3 = True
            image_3_frame = np.asarray(self.buf_mem['image_3'])

        if self.verbose:
            print(f"""
            img_2 frame {frame_id} loaded successfully: {not self.problem_load_cam_2}
            img_3 frame {frame_id} loaded successfully: {not self.problem_load_cam_3}
            """)
        return image_2_frame, image_3_frame

    def _check_and_load_lidar(
        self,
        sequence_id: str,
        frame_id: str,
    ) -> tuple[NDArray[np.float32], NDArray[np.uint32], NDArray[np.uint8]]:
        """Check if the lidar file exists, and load the lidar if yes.

        Otherwise, use buffer memory.
        """
        lidar_pc_path = str(
            Path(self.data_dir) / 'sequences' / sequence_id / 'velodyne' / f'{frame_id}.bin'
        )
        lidar_label_path = str(
            Path(self.data_dir) / 'sequences' / sequence_id / 'labels' / f'{frame_id}.label'
        )
        # Check if the file exists. If not, use buffer memory.
        try:
            lidar_pc = read_point_cloud(lidar_pc_path)
            self.buf_mem['lidar_pc'] = lidar_pc
        except FileNotFoundError:
            self.problem_load_lidar_pc = True
            lidar_pc = np.asarray(self.buf_mem['lidar_pc'])
        try:
            pc_labels, pc_label_colors = read_labels_and_colors(lidar_label_path)
            self.buf_mem['lidar_label'] = pc_labels
            self.buf_mem['lidar_label_colors'] = pc_label_colors
        except FileNotFoundError:
            self.problem_load_lidar_label = True
            pc_labels = np.asarray(self.buf_mem['lidar_label'])
            pc_label_colors = np.asarray(self.buf_mem['lidar_label_colors'])
        if self.verbose:
            print(f"""
            pc frame {frame_id} loaded successfully: {not self.problem_load_lidar_pc}
            label frame {frame_id} loaded successfully: {not self.problem_load_lidar_label}
            """)

        return lidar_pc, pc_labels, pc_label_colors

    def calculate_timestamp(
        self, frame_id: int | str | list[int] | list[str]
    ) -> float | list[float]:
        """Calculate the timestamp of the frame. # NOTE: Might move this to utils.

        Args:
            frame_id: The id (or ids) of the frame to be processed.

        Returns:
            timestamp: The timestamp of the frame.
        """
        if isinstance(frame_id, int | str):
            return float(int(frame_id) / self.frequency)
        return [float(int(f) / self.frequency) for f in frame_id]

    def spin(self) -> None:
        """Run the engine until the datastream ends, get interrupted, or new signal is received."""
        print('Spinning the engine...')  # To be implemented

    def _check_arguments(self, frame_id: int | str) -> None:
        """Check the arguments passed to the engine in case there is corruption during COMM."""
        if int(frame_id) % 5 != 0:
            _frame_id_error = 'Frame ID must be a multiple of 5 for SemanticKitti'
            raise ValueError(_frame_id_error)
        # Also check if sequence is in range 0 to 20
        # Check if path exists


def main() -> None:
    """Main function."""
    print('Loading config. Make sure you execute this script at directory root of project.')
    config_path = Path.cwd() / 'configs' / 'sensorium.yaml'
    with Path(config_path).open() as stream:
        backend_config = yaml.safe_load(stream)
    import time

    # Initialize the backend engine
    data_dir = backend_config['backend_engine']['data_dir']
    backend_engine = BackendEngine(data_dir=data_dir, verbose=True)

    # Load the first frame
    start_time = time.time()
    backend_engine.process(sequence_id=0, frame_id=0)
    print(f'Loaded data for sequence {0} and frame {0} ...')
    end_time = time.time()
    print(f'Time taken: {end_time - start_time:.4f} seconds')

    # Load another frame
    start_time = time.time()
    backend_engine.process(sequence_id=0, frame_id=5)
    print(f'Loaded data for sequence {0} and frame {5} ...')
    end_time = time.time()
    print(f'Time taken: {end_time - start_time:.4f} seconds')


if __name__ == '__main__':
    main()
