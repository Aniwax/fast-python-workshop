#!/usr/bin/env python3
"""
To only compile the C extension inplace:
python setup.py build_ext --inplace
"""

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    raise RuntimeError('setuptools is required')
try:
    from numpy import get_include as _numpy_get_include
except ImportError:
    raise RuntimeError('numpy is required')

setup(name="euclidean_distance",
      version="1.0",
      packages=find_packages(),
      package_dir={"euclidean_distance": "."},
      description="Euclidean distance example in 3 dimensional space",
      keywords=[],
      install_requires=["numpy"],
      setup_requires=["numpy"],
      classifiers=[],
      python_requires=">=3.5",
      ext_package="euclidean_distance",
      ext_modules=[Extension('euclidean_distance',
                             sources=["euclidean_distance.c"],
                             include_dirs=[_numpy_get_include()])]
      )
