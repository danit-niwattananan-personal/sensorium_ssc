# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Voxel Visualization class."""

import os

os.environ['ETS_TOOLKIT'] = 'qt'
import sys

import numpy as np
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from traits.api import Dict, HasTraits, Instance, on_trait_change
from traitsui.api import Item, View

from sensorium.communication.client_comm import get_voxel_data
from sensorium.visualization.helper import draw_semantic_voxel


class VoxelVisualization(HasTraits):
    """Voxel Visualization class."""

    scene = Instance(MlabSceneModel, ())
    data = Dict()  # type: ignore[var-annotated]

    @on_trait_change('scene.activated')  # type: ignore[misc]
    def update_plot(self) -> None:
        """Load the new data and draw the new voxel."""
        draw_semantic_voxel(
            voxels=self.data['voxel'],
            cam_pose=self.data['t_velo_2_cam'],
            vox_origin=np.array([0, -25.6, -2]),
            fov_mask=self.data['fov_mask'],
            scene=self.scene,  # type: ignore[arg-type]
        )

    view = View(
        Item('scene', editor=SceneEditor(scene_class=MayaviScene), show_label=False),
        resizable=True,  # need this to resize with the parent widget
    )


# NOTE: QMainWindow doesn't work with our settings, so we use QWidget instead
class VoxelWidget(QWidget):
    """Mayavi PyQt wrapper for voxel visualization window."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the voxel widget."""
        super().__init__(parent)
        self.frame_number = 0
        self.setWindowTitle('Voxel Ground Truth')

        # Create the main widget
        self.layout_window = QVBoxLayout(self)
        self.layout_window.setContentsMargins(0, 0, 0, 0)
        self.layout_window.setSpacing(0)

    async def update_scene(self, seq_id: int, frame_id: int) -> None:
        """Update the scene with the new image and show to the user."""
        # First check the frame_id is valid
        if frame_id % 5 != 0:
            self.frame_number += 1
            return
        try:
            voxel, fov_mask, t_velo_2_cam = await get_voxel_data(seq_id, frame_id)
        except ValueError as e:
            print(f'Error getting voxel data: {e}')
            return

        data = {
            'voxel': voxel,
            'fov_mask': fov_mask,
            't_velo_2_cam': t_velo_2_cam,
        }

        self.visualization = VoxelVisualization(data=data)

        # Clean up the previous UI and scene
        if hasattr(self, 'ui'):
            self.layout_window.removeWidget(self.ui)  # type: ignore[has-type]
            self.ui.deleteLater()  # type: ignore[has-type]
            if self.visualization.scene.scene_editor is not None:  # type: ignore[union-attr]
                self.visualization.scene.scene_editor = None  # type: ignore[union-attr]

        # Remove the figure
        self.visualization.scene.mlab.clf()  # type: ignore[union-attr]

        # Update the scene and add it to the layout
        self.ui = self.visualization.edit_traits(
            parent=self, kind='subpanel', context=self.visualization
        ).control
        self.layout_window.addWidget(self.ui)
        self.ui.setParent(self)

        # Update the frame number
        self.frame_number += 1


def main() -> None:
    """Main function."""
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    window = VoxelWidget()
    window.show()
    sys.exit(app.exec())  # type: ignore[union-attr]


if __name__ == '__main__':
    main()
