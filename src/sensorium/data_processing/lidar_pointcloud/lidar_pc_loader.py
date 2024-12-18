"""Lidar pointcloud loader."""

from pathlib import Path

import open3d as o3d  # type: ignore[import-untyped] # Ignore mypy stubs not found


# o3d.geometry.PointCloud did not pass Mypy since it can't generate stubs
def load_lidar_pc(
    data_dir: str, sequence_id: str, frame_id: int | list[int | str]
) -> o3d.geometry.PointCloud:
    """Load the lidar pointcloud."""
    # @Dimitar: Implement the loader and conversion .bin -> .ply
    pcd_path = Path(data_dir) / sequence_id / 'velodyne' / f'{frame_id}.bin'
    # Must convert to ply first
    return o3d.io.read_point_cloud(pcd_path)
