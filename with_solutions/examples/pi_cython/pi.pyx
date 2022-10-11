#!/usr/bin/env python3
# distutils: language = c++
# distutils: extra_compile_args = -std=c++11
"""Monte Carlo computation of pi"""

from cython cimport boundscheck, wraparound
from random import uniform  # only used for random initial seed


cdef extern from "<random>" namespace "std":
    cdef cppclass random_device:
        random_device()  # we need to define this constructor to stack allocate classes in Cython
        random_device(unsigned int seed)  # not worrying about matching the exact int type for seed

    cdef cppclass uniform_real_distribution[T]:
        uniform_real_distribution()
        uniform_real_distribution(T a, T b)
        T operator()(random_device gen)


@boundscheck(False)
@wraparound(False)
def approx_pi(int n_attempts):
    cdef:
        random_device gen = random_device(5)
        uniform_real_distribution[double] dist = uniform_real_distribution[double](-1.0, 1.0)
        int n_hits = 0
        double x, y

    for _ in range(n_attempts):
        x = dist(gen)
        y = dist(gen)
        if x ** 2 + y ** 2 <= 1.0:
            n_hits += 1
    return 4. * n_hits / n_attempts
