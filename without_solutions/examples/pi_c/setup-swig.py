#!/usr/bin/env python3
"""
To only compile the C extension inplace:
python setup.py build_ext --inplace
"""

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    raise RuntimeError('setuptools is required')

setup(name="pi_swig",
      version="1.0",
      packages=find_packages(),
      package_dir={"pi_swig": "."},
      description="Pi",
      python_requires=">=3.5",
      ext_modules=[Extension(
          '_pi_swig',
          sources=["approx_pi.c", "pi_swig_wrap.c"])]
      )
