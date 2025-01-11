# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0

"""Helper functions for voxel visualization."""

import mayavi
from mayavi import mlab

try:
    engine = mayavi.engine
except NameError:
    from mayavi.api import Engine

    engine = Engine()
    engine.start()
import numpy as np
from numpy.typing import NDArray

import sensorium.data_processing.utils.io_data as semkitti_io


def position_scene_view(scene: mlab.figure.scene, view: int = 1) -> None:
    """Rotate the scene to a specific view.

    Available views:
    0. Default view with camera frustum facing the south west direction
    1. Camera frustum facing the north east direction like PaSCo
    Code adapted from PaSCo https://github.com/astra-vision/PaSCo/blob/main/scripts/visualize.py
    """
    if view == 0:
        pass  # Default mayavi isometric view, do nothing.
    elif view == 1:
        scene.x_minus_view()
        scene.camera.position = [-54.665532379571125, -43.712070618513835, 93.7371444096225]
        scene.camera.focal_point = [25.49999923631549, 25.49999923631549, 1.9999999515712261]
        scene.camera.view_angle = 30.0
        scene.camera.view_up = [0.5442689178381115, 0.3685077360527552, 0.7536400954995723]
        scene.camera.clipping_range = [81.66754657666122, 214.0287975774116]
        scene.camera.compute_view_plane_normal()
        scene.render()


def get_grid_coords(dims: list[int], resolution: float) -> NDArray[np.float32]:
    """Get the grid coordinates of the voxel.

    Args:
        dims: the dimensions of the grid [x, y, z] (i.e. [256, 256, 32])
        resolution: the size of the voxel

    Returns:
        coords_grid: the center coordinates of the voxels in the grid
    """
    g_xx = np.arange(0, dims[0] + 1)
    g_yy = np.arange(0, dims[1] + 1)
    g_zz = np.arange(0, dims[2] + 1)

    # Obtaining the grid with coords...
    xx, yy, zz = np.meshgrid(g_xx[:-1], g_yy[:-1], g_zz[:-1])
    coords_grid = np.array([xx.flatten(), yy.flatten(), zz.flatten()]).T
    coords_grid = coords_grid.astype(float)
    coords_grid = (coords_grid * resolution) + resolution / 2

    temp = np.copy(coords_grid)
    temp[:, 0] = coords_grid[:, 1]
    temp[:, 1] = coords_grid[:, 0]
    return np.copy(temp)


def draw_semantic_voxel(
    voxels: NDArray[np.uint8] | NDArray[np.float32] | None,
    cam_pose: NDArray[np.float32],
    vox_origin: NDArray[np.float32],
    fov_mask: NDArray[np.bool_],
    figure: mlab.figure = None,
) -> mlab.figure:
    """Draw a semantic voxel. Code adapted from Symphonies.

    Args:
        voxels: the voxel data
        cam_pose: the camera's extrinsic matrix relative to lidar
        vox_origin: the origin coordinate of the voxel
        fov_mask: the field of view mask
        figure: the mayavi figure
    """
    # Set meta data of the voxel
    img_size = (1220, 370)  # for SemanticKITTI dataset.
    f = 707.0912  # for SemanticKITTI dataset.
    voxel_size = 0.2
    d = 7  # 7m - determine the size of the mesh representing the camera
    view = 1  # choose viewing mode defined in position_scene_view function

    # Check the input voxel
    if voxels is None:
        _e_msg = 'No voxel passed to draw_semantic_voxel function'
        raise ValueError(_e_msg)

    if figure is None:
        figure = mlab.figure(size=(1400, 1400), bgcolor=(1, 1, 1), engine=engine)

    # Compute the coordinates of the mesh representing camera
    x = d * img_size[0] / (2 * f)
    y = d * img_size[1] / (2 * f)
    tri_points = np.array(
        [
            [0, 0, 0],
            [x, y, d],
            [-x, y, d],
            [-x, -y, d],
            [x, -y, d],
        ]
    )
    tri_points = np.hstack([tri_points, np.ones((5, 1))])
    tri_points = (np.linalg.inv(cam_pose) @ tri_points.T).T
    x = tri_points[:, 0] - vox_origin[0]
    y = tri_points[:, 1] - vox_origin[1]
    z = tri_points[:, 2] - vox_origin[2]
    triangles = [
        (0, 1, 2),
        (0, 1, 4),
        (0, 3, 4),
        (0, 2, 3),
    ]

    # Compute the voxels coordinates
    grid_coords = get_grid_coords([voxels.shape[0], voxels.shape[1], voxels.shape[2]], voxel_size)
    # Attach the predicted class to every voxel
    grid_coords = np.vstack([grid_coords.T, voxels.reshape(-1)]).T.astype(np.float32)
    # Get the voxels inside FOV
    fov_grid_coords = grid_coords[fov_mask, :]
    # Get the voxels outside FOV
    outfov_grid_coords = grid_coords[~fov_mask, :]
    # Draw the camera
    mlab.triangular_mesh(
        x,
        y,
        z,
        triangles,
        representation='wireframe',
        color=(0, 0, 0),
        line_width=10,
        figure=figure,
    )

    colors = semkitti_io.get_cmap_semantickitti20()

    outfov_colors = colors.copy()
    outfov_colors[:, :3] = outfov_colors[:, :3] // 3 * 2

    for i, grid_coords in enumerate((fov_grid_coords, outfov_grid_coords)):
        # Remove empty and unknown voxels
        voxels = grid_coords[(grid_coords[:, 3] > 0) & (grid_coords[:, 3] < 255)]
        plt_plot = mlab.points3d(
            voxels[:, 0],
            voxels[:, 1],
            voxels[:, 2],
            voxels[:, 3],
            colormap='viridis',
            scale_factor=voxel_size - 0.05 * voxel_size,
            figure=figure,
            mode='cube',
            opacity=1.0,
            vmin=1,
            vmax=19,
        )
        position_scene_view(figure.scene, view)

        plt_plot.glyph.scale_mode = 'scale_by_vector'
        plt_plot.module_manager.scalar_lut_manager.lut.table = colors if i == 0 else outfov_colors

    plt_plot.scene.camera.zoom(1.3)

    return figure
