.. image:: ../../../badges/master/pipeline.svg
   :target: ../../../-/commits/master
   :alt: pipeline status

.. image:: ../../../badges/master/coverage.svg
   :target: ../../../-/commits/master
   :alt: coverage report

.. image:: https://img.shields.io/badge/License-Apache_2.0-blue.svg
   :target: LICENSE
   :alt: License

=========
Sensorium
=========

A sensor network visualization tool tailored for Semantic Scene Completion (SSC) datasets used in autonomous driving applications.

Features
========
- Sensor data visualization with support for cameras and LiDAR point clouds
- Odometry ground truth and semantic voxel ground truth visualization
- Interactive 3D voxel visualization
- Dataset playback and timeline controls
- Switching between different scenes and sequences in a dataset
- Communication architecture for hosting sensor data on server and run visualization on client machine

Installation
===========

Prerequisites
------------
- uv Python package manager. Follow the official `uv documentation <https://docs.astral.sh/uv/getting-started/installation/#standalone-installer>` for installation instructions.
- conda might disrupt the environment during creating the .venv environment with uv. Please deactivate conda before running uv.

Setup
-----

1. Clone the repository and setup the dependencies with:

.. code-block:: bash

   uv sync

2. Download the dataset to be visualized. Currently (06.02.2025), the repository only supports the semantic kitti dataset. After downloading it, organize the data in the following manner:

.. code-block:: bash

   /path/to/dataset/
               └── sequences/
                        ├── 00/
                        │   ├── poses.txt
                        │   ├── calib.txt
                        │   ├── image_2/
                        │   ├── image_3/
                        │   ├── labels/
                        │   │     ├ 000000.label
                        │   │     └ 000001.label
                        |   ├── voxels/
                        |   |     ├ 000000.bin
                        |   |     ├ 000000.label
                        |   |     ├ 000000.occluded
                        |   |     ├ 000000.invalid
                        |   |     ├ 000001.bin
                        |   |     ├ 000001.label
                        |   |     ├ 000001.occluded
                        |   |     ├ 000001.invalid
                        │   └── velodyne/
                        │         ├ 000000.bin
                        │         └ 000001.bin
                        ├── 01/
                        ├── 02/
                        .
                        .
                        .
                        └── 21/

3. Declare the path to the dataset folder in the ``configs/sensorium.yaml`` file:

.. code-block:: yaml
   data_dir: /path/to/dataset

Usage
=====
Starting the Application
-----------

1. Launch the server with:

.. code-block:: bash

   uv run src/sensorium/launch/launch.py # use \ for windows paths
then select the server option and specify the port number through which data will be streamed. 

2. Launch the client with:

.. code-block:: bash

   uv run src/sensorium/launch/launch.py # use \ for windows paths
then select the client option and specify the server IP address and port number. If the server and client are running on the same machine, use ``localhost`` as the IP address.

3. After the connection is established, click ``Open Engine`` to start the visualization GUI windows. To start streaming, double-click the ``Play`` button.


Development
==========

Setup Development Environment
---------------------------
Clone the repository and setup your local checkout:

.. code-block:: bash
   uv sync

Testing
---------

The project uses pytest as its test runner, run the testsuite by simply invoking ``uv run pytest``.

Documentation
-------------------

Documentation is written with sphinx, to build the documentation from its source run sphinx-build:

.. code-block:: bash

   uv run sphinx-build -a docs public

The entrypoint to the local documentation build should be available under ``public/index.html``.

Issues
------

If you encounter any issues, please report them to the `issue tracker <https://gitlab.lrz.de/ldv/teaching/python/2024/b/-/issues>`.
