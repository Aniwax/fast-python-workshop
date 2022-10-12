#!/usr/bin/env python3

# © 2020 ETH Zurich

import numpy as np
import timeit
import json
import pathlib
import typing

import demo_numba_cpu
import demo_numba_gpu
import demo_cupy
import demo_numpy


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


def save_measurements_as_json_file(
    data: typing.Dict[int, typing.Dict[str, float]], file_name: pathlib.Path
) -> None:
    """
    Writes the provided data to a new JSON file at file_name.
    """
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=2)


def run_benchmark(number_of_points: int, iterations: int) -> typing.Dict[str, float]:
    """
    Runs the benchmarks (CPU and GPU) for the given number_of_points. Each call is repeated iterations times.
    The function returns a dictionary with two keys ('cpu' and 'gpu') and the associated average measured time.
    """

    points = create_random_points(number_of_points)

    result_cpu = create_zero_distance_matrix(number_of_points)
    timer_cpu = timeit.Timer(
        stmt=lambda: demo_numba_cpu.distance_matrix(points, result_cpu),
    )

    result_gpu = create_zero_distance_matrix(number_of_points)
    timer_gpu = timeit.Timer(
        stmt=lambda: demo_numba_gpu.distance_matrix[
            (number_of_points, number_of_points), (1, 1)
        ](points, result_gpu),
    )

    result_numpy = create_zero_distance_matrix(number_of_points)
    timer_numpy = timeit.Timer(
        stmt=lambda: np.copyto(result_numpy, demo_numpy.distance_matrix(points)),
    )

    result_cupy = create_zero_distance_matrix(number_of_points)
    timer_cupy = timeit.Timer(
        stmt=lambda: np.copyto(result_cupy, demo_cupy.distance_matrix(points)),
    )

    result = {
        "gpu": timer_gpu.timeit(iterations) / iterations,
        "cpu": timer_cpu.timeit(iterations) / iterations,
        "numpy": timer_numpy.timeit(iterations) / iterations,
        "cupy": timer_cupy.timeit(iterations) / iterations,
    }

    assert np.linalg.norm(result_cpu - result_gpu) < 1.0e-12
    assert np.linalg.norm(result_cpu - result_numpy) < 1.0e-12
    assert np.linalg.norm(result_cpu - result_cupy) < 1.0e-12
    return result


def main() -> None:
    """
    Runs the benchmarks for a range of given points and writes them to a JSON file "measurements.json".
    """
    measurements = {}
    iterations = 1000

    for number_of_points in range(1, 800, 2 ** 3):
        print(
            f"Running benchmark for {number_of_points} points ({iterations} iterations)..."
        )
        measurements[number_of_points] = run_benchmark(number_of_points, iterations)

    save_measurements_as_json_file(measurements, pathlib.Path("measurements.json"))


if __name__ == "__main__":
    main()
