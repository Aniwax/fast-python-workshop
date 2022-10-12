# © 2020 ETH Zurich

from numba import njit
import numpy as np


@njit
def distance_matrix(points: np.array, result: np.array) -> None:
    """
    Computes the Euclidean distance matrix for the given points (naive Numba implementation).

    :param points: A matrix where each column represents the coordinates of a point.
    :param result: The Euclidean distance matrix.
    """
    number_of_points = points.shape[0]

    assert result.shape[0] == number_of_points and result.shape[1] == number_of_points

    for row in range(number_of_points):
        x = points[row]
        for col in range(number_of_points):
            y = points[col]
            result[row][col] = ((x - y) ** 2).sum()
