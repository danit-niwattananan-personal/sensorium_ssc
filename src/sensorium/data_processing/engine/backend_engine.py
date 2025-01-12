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
from sensorium.data_processing.trajectory.traj import get_position_at_frame
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

    def process(
        self,
        sequence_id: int | str,
        frame_id: int | str,
    ) -> dict[
        str,
        str | list[float] | float | NDArray[np.float32] | NDArray[np.bool_] | MatLike | None,
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

        # Load the image
        image_2_dir = Path(self.data_dir) / 'sequences' / sequence_id / 'image_2'
        image_3_dir = Path(self.data_dir) / 'sequences' / sequence_id / 'image_3'
        image_2_frame = load_single_img(str(image_2_dir), start_frame_id)
        image_3_frame = load_single_img(str(image_3_dir), start_frame_id)
        if self.verbose:
            print('Images loaded')

        # Load the lidar point cloud and panoptic ground truth
        lidar_pc_path = str(
            Path(self.data_dir) / 'sequences' / sequence_id / 'velodyne' / f'{start_frame_id}.bin'
        )
        lidar_label_path = str(
            Path(self.data_dir) / 'sequences' / sequence_id / 'labels' / f'{start_frame_id}.label'
        )
        lidar_pc = read_point_cloud(lidar_pc_path)
        pc_labels, pc_label_colors = read_labels_and_colors(lidar_label_path)
        if self.verbose:
            print('Lidar point cloud loaded')

        # Load the trajectory
        # NOTE: the calib_file and calibration_file contains information about sequence_id
        calib_file_path = str(Path(self.data_dir) / 'sequences' / sequence_id / 'calib.txt')
        poses_file_path = str(
            Path(self.data_dir) / 'sequences' / sequence_id / 'poses_single_frame.txt'
        )
        trajectory_data_dict = get_position_at_frame(
            calib_file_path, poses_file_path, int(start_frame_id)
        )
        xyz = np.array(
            [trajectory_data_dict['x'], trajectory_data_dict['y'], trajectory_data_dict['z']]
        )
        if self.verbose:
            print(f'Trajectory loaded with x,y,z: {xyz}')

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
            except FileNotFoundError as e:
                _error_msg = """Make sure that 1) data exists, 2) execute this file from the root
                directory of project, 3) the config file is in b/config/vox_semantic_kitti.yaml"""
                raise ImportError(_error_msg) from e
            all_calibs = read_calib(calib_file_path)
            cam_intrinsic = all_calibs['P2']
            t_velo_2_cam = all_calibs['Tr']  # cam_pose
            cam_k = cam_intrinsic[:3, :3]
            # NOTE: This code takes way too long to calculate for every frame
            # Solution: calculate once and save it as attribute of class, or use a cache
            _, fov_mask, _ = vox2pix(
                t_velo_2_cam, cam_k, self.voxel_origin, self.img_shape, self.scene_size
            )

        except ValueError:
            # If no, assign None to voxel_related data
            voxel_data = None
            fov_mask = None
            t_velo_2_cam = None

        if self.verbose:
            print('Voxel loaded')

        return {
            'frame_id': start_frame_id,
            'timestamp': self.calculate_timestamp(start_frame_id),
            'image_2': image_2_frame,
            'image_3': image_3_frame,
            'lidar_pc': lidar_pc,
            'lidar_pc_labels': pc_labels,
            'lidar_pc_label_colors': pc_label_colors,
            'trajectory': xyz,
            'voxel': voxel_data,
            'fov_mask': fov_mask,
            't_velo_2_cam': t_velo_2_cam,
        }

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

    def collate_dictoflists(self, data: dict[str, list[dict[str, float]]]) -> None:
        """Collate data into a single list of dicts instead of dict of lists.

        Args:
            data: The data to be collated.

        Returns:
            collated_data: The collated data.

        Raises:
            AssertionError: If the length of the data is not equal to the length of frame_id.
        """
        for k, v in data.items():
            assert len(v) == len(
                data['frame_id']
            ), f'The length of {k} is not equal to the length of frame_id'
        # to be implemented
        print('Collating data...')

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

    start_time = time.time()
    data_dir = backend_config['backend_engine']['data_dir']
    backend_engine = BackendEngine(data_dir=data_dir)
    backend_engine.process(sequence_id=0, frame_id=0)
    print(f'Loaded data for sequence {0} and frame {0} ...')
    end_time = time.time()
    print(f'Time taken: {end_time - start_time} seconds')


if __name__ == '__main__':
    main()
