#!/usr/bin/env python3
"""Euclidean distance example in 3 dimensional space"""

from scipy.spatial.distance import cdist
import numpy


def setup_points(n):
    return numpy.indices((n, n, n), dtype=float).reshape((3, -1)).T


def dist_matrix(points):
    return cdist(points, points, 'sqeuclidean')


if __name__ == "__main__":
    M = dist_matrix(setup_points(10))
    print(M[:5, :5])
