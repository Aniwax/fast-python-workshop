#!/usr/bin/env python3
"""Euclidean distance example in 3 dimensional space"""

import numpy
import numba


def setup_points(n):
    return numpy.indices((n, n, n), dtype=float).reshape((3, -1)).T


@numba.njit(cache=True, fastmath=True)
def dist_matrix(points):
    # To avoid computing the same multiple times, use:
    # <x-y, x-y> = <x,x> -2 <x,y> + <y,y>
    # Numba does not support `numpy.einsum`
    p_2 = (points**2).sum(1)
    # Numba does not support numpy slicing w/ None, use expand_dims instead
    x_2 = numpy.expand_dims(p_2, 1)
    y_2 = numpy.expand_dims(p_2, 0)
    x_y = points @ points.T  # @ is matrix multiplication
    return x_2 - 2 * x_y + y_2


if __name__ == "__main__":
    M = dist_matrix(setup_points(10))
    print(M[:5, :5])
