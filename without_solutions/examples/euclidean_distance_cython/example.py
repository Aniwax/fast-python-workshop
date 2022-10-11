#!/usr/bin/env python3

import numpy
from euclidean_distance import dist_matrix, setup_points


def dist_matrix_numpy(points):  # numpy as a reference
    p_2 = numpy.einsum('ij,ij->i', points, points)
    x_2 = p_2[:, None]
    y_2 = p_2[None, :]
    x_y = points @ points.T  # @ is matrix multiplication
    return x_2 - 2 * x_y + y_2


if __name__ == "__main__":
    points = setup_points(10)
    M = dist_matrix(points)
    assert (M == dist_matrix_numpy(points)).all()
    print(M[:5, :5])
