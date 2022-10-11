#!/usr/bin/env python3

import numpy
import numexpr


def setup_points(n):
    return numpy.indices((n, n, n), dtype=float).reshape((3, -1)).T


def dist_matrix(points):
    # numexpr is for point wise operation, not for vector dot operations.
    # Therefore first use the first step of the numpy example
    p_2 = numpy.einsum('ij,ij->i', points, points)
    x_2 = p_2[:, None]
    y_2 = p_2[None, :]
    x_y = points @ points.T  # @ is matrix multiplication
    return numexpr.evaluate("x_2 - 2*x_y + y_2")


if __name__ == "__main__":
    M = dist_matrix(setup_points(10))
    print(M[:5, :5])
