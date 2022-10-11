#!/usr/bin/env python3

from random import uniform

import numba


@numba.njit
def approx_pi(n_attempts):
    n_hits = 0

    for _ in range(n_attempts):
        x = uniform(-1.0, 1.0)
        y = uniform(-1.0, 1.0)
        if x ** 2 + y ** 2 <= 1.0:
            n_hits += 1
    return 4 * n_hits / n_attempts


@numba.njit(parallel=True)
def approx_pi_par(n_attempts):
    n_hits = 0

    for _ in numba.prange(n_attempts):
        x = uniform(-1.0, 1.0)
        y = uniform(-1.0, 1.0)
        if x ** 2 + y ** 2 <= 1.0:
            n_hits += 1
    return 4 * n_hits / n_attempts


if __name__ == "__main__":
    print(approx_pi(2_000_000))
    print(approx_pi_par(2_000_000))
