# © 2020 ETH Zurich

from numba import cuda
import numpy as np


@cuda.jit
def distance_matrix(points: np.array, result: np.array) -> None:
    """
    Computes the Euclidean distance matrix for the given points (naive CUDA implementation).
    It assumes that the CUDA grid and the distance matrix have the same shape.

    :param points: A matrix where each column represents the coordinates of a point.
    :param result: The Euclidean distance matrix.
    """
    number_of_points = points.shape[0]
    dimension = points.shape[1]

    assert result.shape[0] == number_of_points and result.shape[1] == number_of_points
    assert (
        cuda.gridDim.x == number_of_points
        and cuda.gridDim.y == number_of_points
        and cuda.gridDim.z == 1
    )

    row, col = cuda.grid(2)

    x = points[row]
    y = points[col]

    squared_distance = 0.0
    for index in range(0, dimension):
        squared_distance += (x[index] - y[index]) ** 2

    result[row][col] = squared_distance
