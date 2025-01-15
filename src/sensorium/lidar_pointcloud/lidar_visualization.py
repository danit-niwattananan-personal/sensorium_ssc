# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Visualization of the LiDAR pointcloud scene."""

import time
from pathlib import Path
from typing import cast

import numpy as np
import pygfx as gfx  # type: ignore[import-untyped]
import yaml
from PySide6 import QtWidgets
from wgpu.gui.qt import WgpuCanvas  # type: ignore[import-untyped]

# from sensorium.launch.launch import get_lidar_data  # noqa: ERA001


class PointcloudVis(QtWidgets.QWidget):
    """Widget for visualizing and controlling the LiDAR pointcloud scene."""

    def __init__(self) -> None:
        """Initialize the PointcloudVis class."""
        super().__init__(None)
        self.resize(640, 480)
        self.directory = r'C:\Users\wich_\Desktop\velodyne\00'
        self.pcd = None
        self.frame_number = 0
        self.is_animating = False
        self.waiting_for_new_file = False

        self.label_directory = ''
        self.config_file = ''

        self.setup_canvas()

        self.frame_count = 0

        self.start_time = time.time()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

    def setup_canvas(self) -> None:
        """."""
        self.canvas = WgpuCanvas(parent=self)
        self.renderer = gfx.WgpuRenderer(self.canvas)
        self.scene = gfx.Scene()
        self.camera = gfx.OrthographicCamera(100, 100)
        self.canvas.request_draw(self.animate)
        layout = self.layout()
        self.canvas.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding
        )
        if layout is not None:
            layout.addWidget(self.canvas)

    def get_colormap(self) -> dict[str, list[float]]:
        """."""
        with Path(self.config_file).open('r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return cast(dict[str, list[float]], data['color_map'])

    def load_positions(self, frame_id: int) -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
        """Loads the coordinates for the positions of the points from one .bin file."""
        path = f'{self.directory}/{frame_id:06d}.bin'
        points = np.fromfile(path, np.float32).reshape(-1, 4)
        return points[:, :3]

    def load_colors_gradient(
        self, positions: np.ndarray[tuple[int, ...], np.dtype[np.float32]]
    ) -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
        """Creates a gradient color map based on the z-values of the points.

        Args:
            positions:np.ndarray[tuple[int, ...], np.dtype[np.float32]]: Array with the coordinates
            of the points. Needed to assign the colors based on the z-valuse.

        Returns:
            np.ndarray[tuple[int, ...], np.dtype[np.float32]]: Array withe rbg values of the points.
        """
        z_values = positions[:, 2]
        z_min = np.percentile(z_values, 10)
        z_max = np.percentile(z_values, 90)
        z_values_clipped = np.clip(z_values, z_min, z_max)
        normalized_z = (z_values_clipped - z_min) / (z_max - z_min)
        colors = np.zeros((len(normalized_z), 3), dtype=np.float32)

        colors[:, 0] = 1  # red
        colors[:, 1] = 0.80 - normalized_z  # green
        colors[:, 2] = 0  # blue
        return colors

    def load_colors_ground_truth(self) -> np.ndarray[tuple[int, ...], np.dtype[np.float32]]:
        """."""
        path = f'{self.label_directory}/{self.frame_number:06d}.label'
        ids = np.fromfile(path, dtype=np.uint32)
        semantic_ids = ids & 0xFFFF
        color_map = self.get_colormap()
        max_class_id = int(max(color_map.keys())) + 1
        color_map_array = np.zeros((max_class_id, 3), dtype=np.float32)

        for key, value in color_map.items():
            color_map_array[int(key)] = value
        return np.asarray(color_map_array[semantic_ids], dtype=np.float32)

    def update_scene(self, frame_id: int) -> None:
        """Method to update the scene with the current frame."""
        if Path(f'{self.directory}/{frame_id:06d}.bin').exists():  #
            # positions, colors = get_lidar_data(frame_id, seq_id)  # noqa: ERA001
            positions = np.ascontiguousarray(self.load_positions(frame_id), dtype=np.float32)
            colors = np.ascontiguousarray(self.load_colors_gradient(positions), dtype=np.float32)
            sizes = np.ascontiguousarray(
                np.ones(positions.shape[0], dtype=np.float32) * 0.03, dtype=np.float32
            )
            positions = gfx.Buffer(positions, force_contiguous=True)
            colors = gfx.Buffer(colors, force_contiguous=True)
            sizes = gfx.Buffer(sizes, force_contiguous=True)
            if self.pcd is not None:
                self.pcd.geometry.positions = positions
                self.pcd.geometry.colors = colors
                self.pcd.geometry.sizes = sizes
            else:
                self.pcd = gfx.Points(
                    gfx.Geometry(positions=positions, sizes=sizes, colors=colors),
                    gfx.PointsMaterial(color_mode='vertex', size_mode='vertex'),
                )
                self.scene.add(self.pcd)
            self.canvas.update()
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time >= 5.0:
                fps = self.frame_count / elapsed_time
                print(f'FPS: {fps:.2f} Frame:{self.frame_number}')
                self.frame_count = 0
                self.start_time = current_time
        elif self.is_animating:
            self.waiting_for_new_file = True

    def directory_changed(self) -> None:
        """."""
        if (
            not self.is_animating
            and self.waiting_for_new_file
            and Path(f'{self.directory}/{self.frame_number:06d}.bin').exists()
        ):
            self.waiting_for_new_file = False

    def animate(self) -> None:
        """."""
        self.frame_count += 1
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    pointcloud = PointcloudVis()
    pointcloud.config_file = r'C:\Users\wich_\Desktop\semantic-kitti-all.yaml'
    pointcloud.directory = r'C:\Users\wich_\Desktop\velodyne\00'
    pointcloud.label_directory = r'C:\Users\wich_\Desktop\data_odometry_labels\00\labels'
    pointcloud.show()
    app.exec()
