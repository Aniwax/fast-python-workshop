#!/usr/bin/env python3

import numpy
import numba


# Note: there is no point to parallelize this Numpy code
@numba.njit
def approx_pi(n_attempts):
    points = numpy.random.rand(n_attempts, 2)
    n_hits = numpy.count_nonzero((points ** 2).sum(1) <= 1.0)
    return 4 * n_hits / n_attempts


if __name__ == "__main__":
    print(approx_pi(2_000_000))
