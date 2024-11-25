# Copyright 2024  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Sphinx config."""

# ruff: noqa: INP001

project = 'Sensorium'
copyright = '2024, Projektpraktikum Python'  # noqa: A001
author = 'Projectpraktikum Python'

autoapi_python_use_implicit_namespaces = True
autodoc_typehints = 'description'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

html_theme = 'sphinx_rtd_theme'
