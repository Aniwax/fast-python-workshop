#!/usr/bin/env python3

import numpy
from euclidean_distance import dist_matrix


def setup_points(n):
    # here .copy() is important, as the c extension will only see the
    # underlaying contiguous array (C would not see the .T)
    return numpy.indices((n, n, n), dtype=float).reshape((3, -1)).T.copy()


def dist_matrix_numpy(points):  # numpy as a reference
    p_2 = numpy.einsum('ij,ij->i', points, points)
    x_2 = p_2[:, None]
    y_2 = p_2[None, :]
    x_y = points @ points.T  # @ is matrix multiplication
    return x_2 - 2 * x_y + y_2


if __name__ == "__main__":
    pts = setup_points(10)
    N = pts.shape[0]
    out = numpy.empty((N, N), dtype=float)
    M = dist_matrix(pts, out)
    assert (M == dist_matrix_numpy(pts)).all()
    print(M[:5, :5])
