# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Visualization of the LiDAR pointcloud scene."""

import time
from pathlib import Path

import numpy as np
import pygfx as gfx
import yaml
from PySide6 import QtCore, QtWidgets
from wgpu.gui.qt import WgpuCanvas


class PointcloudVis(QtWidgets.QWidget):
    """Widget for visualizing and controlling the LiDAR pointcloud scene."""

    def __init__(self) -> None:
        """Initialize the PointcloudVis class."""
        super().__init__(None)
        self.resize(640, 480)

        self.pcd = None
        self.frame_number = 0
        self.is_animating = False
        self.waiting_for_new_file = False

        self.directory = ''
        self.label_directory = ''
        self.config_file = ''

        self.setup_gui()
        self.setup_canvas()
        self.setup_timers_and_watcher()

        self.frame_count = 0

        self.start_time = time.time()

    def setup_gui(self) -> None:
        """."""
        self.button = QtWidgets.QPushButton('Load next frame', self)
        self.button.clicked.connect(self.load_next_frame)
        self.animate_button = QtWidgets.QPushButton('Animation (On/Off)', self)
        self.animate_button.clicked.connect(self.toggle_animation)
        self.forward_button = QtWidgets.QPushButton('Jump Forwards', self)
        self.forward_button.clicked.connect(self.jump_forwards)
        self.backward_button = QtWidgets.QPushButton('Jump Backwards', self)
        self.backward_button.clicked.connect(self.jump_backwards)
        self.status_bar = QtWidgets.QStatusBar(self)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.button)
        layout.addWidget(self.animate_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.backward_button)
        layout.addWidget(self.status_bar)

    def setup_canvas(self) -> None:
        """."""
        self.canvas = WgpuCanvas(parent=self)
        self.layout().addWidget(self.canvas)
        self.renderer = gfx.WgpuRenderer(self.canvas)
        self.scene = gfx.Scene()
        self.camera = gfx.OrthographicCamera(100, 100)
        self.canvas.request_draw(self.animate)

        layout = self.layout()
        layout: QtWidgets.QVBoxLayout = self.layout()
        if layout is not None:
            layout.addWidget(self.canvas, 1)

    def setup_timers_and_watcher(self) -> None:
        """Set up timers and file system watcher."""
        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.load_next_frame)
        self.animation_timer.setInterval(100)

        self.file_watcher = QtCore.QFileSystemWatcher(self)
        self.file_watcher.directoryChanged.connect(self.directory_changed)

    def get_colormap(self) -> dict[int, list[float]]:
        """."""
        with Path(self.config_file).open('r', encoding='utf-8') as file:
            data: dict = yaml.safe_load(file)
            color_map: dict[int, list[float]] = data['color_map']
        return color_map

    def load_positions(self) -> np.ndarray[tuple[int, ...], np.float32]:
        """Loads the coordinates for the positions of the points from one .bin file."""
        path = f'{self.directory}/{self.frame_number:06d}.bin'
        points = np.fromfile(path, dtype=np.float32).reshape(-1, 4)
        return points[:, :3]

    def load_colors(self) -> np.ndarray[tuple[int, ...], np.float32]:
        """."""
        path = f'{self.label_directory}/{self.frame_number:06d}.label'
        ids = np.fromfile(path, dtype=np.uint32)
        semantic_ids = ids & 0xFFFF
        color_map = self.get_colormap()
        max_class_id = max(color_map.keys()) + 1
        color_map_array = np.zeros((max_class_id, 3), dtype=np.float32)

        for key, value in color_map.items():
            color_map_array[key] = value
        return np.asarray(color_map_array[semantic_ids], dtype=np.float32)

    def jump_forwards(self) -> None:
        """Skip 10 frames forwards."""
        self.frame_number += 10
        self.update_scene()

    def jump_backwards(self) -> None:
        """Skip 10 frames backwards."""
        self.frame_number -= 10
        self.update_scene()

    def load_next_frame(self) -> None:
        """."""
        self.frame_number += 1
        self.update_scene()

    def toggle_animation(self) -> None:
        """."""
        self.is_animating = not self.is_animating
        if self.is_animating:
            self.animation_timer.start()
        else:
            self.animation_timer.stop()

    def update_scene(self) -> None:
        """."""
        if Path(f'{self.directory}/{self.frame_number:06d}.bin').exists():
            positions = self.load_positions()
            colors = self.load_colors()
            sizes = np.full((positions.shape[0],), 0.03, dtype=np.float32)
            positions = np.ascontiguousarray(positions)
            colors = np.ascontiguousarray(colors)
            sizes = np.ascontiguousarray(sizes)
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
            self.status_bar.showMessage(f'Frame: {self.frame_number}')
            # calculating FPS for testing
            self.frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time >= 5.0:
                fps = self.frame_count / elapsed_time
                print(f'FPS: {fps:.2f} Frame:{self.frame_number}')
                self.frame_count = 0
                self.start_time = current_time
        elif self.is_animating:
            self.toggle_animation()
            self.waiting_for_new_file = True

    def directory_changed(self) -> None:
        """."""
        if (
            not self.is_animating
            and self.waiting_for_new_file
            and Path(f'{self.directory}/{self.frame_number:06d}.bin').exists()
        ):
            self.toggle_animation()
            self.waiting_for_new_file = False

    def animate(self) -> None:
        """."""
        self.renderer.render(self.scene, self.camera)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    pointcloud = PointcloudVis()
    pointcloud.config_file = r'C:\Users\wich_\Desktop\semantic-kitti-all.yaml'
    pointcloud.directory = r'C:\Users\wich_\Desktop\velodyne\00'
    pointcloud.label_directory = r'C:\Users\wich_\Desktop\data_odometry_labels\00\labels'
    pointcloud.file_watcher.addPath(str(pointcloud.directory))
    pointcloud.show()
    app.exec()
