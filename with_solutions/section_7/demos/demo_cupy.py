# © 2020 ETH Zurich

import numpy as np
import cupy as cp

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
    # Create an array on the current GPU device
    points_gpu = cp.array(points)

    # Compute on the GPU
    p_2 = cp.einsum("ij,ij->i", points_gpu, points_gpu)
    x_2 = p_2[:, None]
    y_2 = p_2[None, :]
    x_y = points_gpu @ points_gpu.T
    distance_matrix_gpu = x_2 - 2 * x_y + y_2

    # Return the array to host memory
    distance_matrix_cpu = cp.asnumpy(distance_matrix_gpu)
    return distance_matrix_cpu
