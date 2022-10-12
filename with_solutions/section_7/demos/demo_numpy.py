# © 2020 ETH Zurich

import numpy as np

try:
    profile
except NameError:
    profile = lambda f: f


@profile
def distance_matrix(points: np.array) -> np.array:
    """
    Returns the Euclidean distance matrix for the given points.
    Computes this matrix using numpy.
    """
    p_2 = np.einsum("ij,ij->i", points, points)
    x_2 = p_2[:, None]
    y_2 = p_2[None, :]
    x_y = points @ points.T
    return x_2 - 2 * x_y + y_2
