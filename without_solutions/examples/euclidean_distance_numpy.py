#!/usr/bin/env python3
"""Euclidean distance example in 3 dimensional space"""

import numpy


def setup_points(n):
    return numpy.indices((n, n, n), dtype=float).reshape((3, -1)).T


def dist_matrix(points):
    # To avoid computing the same multiple times, use:
    # <x-y, x-y> = <x,x> -2 <x,y> + <y,y>
    # The following is a more efficient way of writing (points**2).sum(1):
    p_2 = numpy.einsum('ij,ij->i', points, points)
    x_2 = p_2[:, None]
    y_2 = p_2[None, :]
    x_y = points @ points.T  # @ is matrix multiplication
    return x_2 - 2 * x_y + y_2


if __name__ == "__main__":
    M = dist_matrix(setup_points(10))
    print(M[:5, :5])
