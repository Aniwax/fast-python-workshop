#!/usr/bin/env python3

from setuptools import setup, Extension

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [Extension(
    "pi",
    sources=["pi" + ext])]

if USE_CYTHON:
    extensions = cythonize(extensions)

setup(
    name='pi',
    ext_modules=extensions,
    zip_safe=False,
)
