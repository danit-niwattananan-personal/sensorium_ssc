.. image:: ../../../badges/master/pipeline.svg
   :target: ../../../-/commits/master
   :alt: pipeline status

.. image:: ../../../badges/master/coverage.svg
   :target: ../../../-/commits/master
   :alt: coverage report


=========
Sensorium
=========

A sensor network visualization tool.


Getting started
===============

Setup
-----

Clone the repository and setup your local checkout:

.. code-block:: bash

   uv sync

Entrypoints
-----------

The configuration in ``pyproject.toml`` defines two entrypoints, one for server and client each. They execute the run functions in the top-level server and client modules from the sensorium package. Launch via:

.. code-block:: bash

   uv run sensorium-server
   uv run sensorium-client

Run tests
---------

The project uses pytest as its test runner, run the testsuite by simply invoking ``uv run pytest``.

Build documentation
-------------------

Documentation is written with sphinx, to build the documentation from its source run sphinx-build:

.. code-block:: bash

   uv run sphinx-build -a docs public

The entrypoint to the local documentation build should be available under ``public/index.html``.
