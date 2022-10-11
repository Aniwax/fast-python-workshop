#!/usr/bin/env python3

from numpy import get_include as _numpy_get_include
from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [Extension(
    "euclidean_distance",
    sources=["euclidean_distance" + ext],
    include_dirs=[_numpy_get_include()])]

if USE_CYTHON:
    extensions = cythonize(extensions)

setup(
    name='euclidean_distance',
    ext_modules=extensions,
    zip_safe=False,
    install_requires=["numpy"]
)
