#!/usr/bin/env python3

# © 2020 ETH Zurich

import numpy as np
import sys

import demo_numpy
import demo_cupy


def create_zero_distance_matrix(matrix_size: int) -> np.array:
    """
    Returns a square matrix of size matrix_size x matrix_size filled with zeros.
    """
    return np.zeros((matrix_size, matrix_size))


def create_random_points(number_of_points: int) -> np.array:
    """
    Returns number_of_points random points in 3D space.
    """
    return np.random.rand(number_of_points, 3)


def main(n: int):
    print("Running number of points: ", n)
    points = create_random_points(n)
    for _ in range(5000):
        result_numpy = demo_numpy.distance_matrix(points)
        result_cupy = demo_cupy.distance_matrix(points)

        assert np.linalg.norm(result_numpy - result_cupy) < 1e-12


if __name__ == "__main__":
    main(int(sys.argv[1]))
