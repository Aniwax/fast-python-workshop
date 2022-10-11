#!/usr/bin/env python3
"""Euclidean distance example in 3 dimensional space"""

import numpy
from cython cimport boundscheck, wraparound
cimport numpy  # special compile-time information about the numpy module


DTYPE = numpy.double


# we dont optimize the setup part (just use numpy):
def setup_points(n):
    return numpy.indices((n, n, n), dtype=float).reshape((3, -1)).T


@boundscheck(False)
@wraparound(False)
def dist_matrix(numpy.ndarray points):
    if points.shape[1] != 3:
        raise ValueError("Only 3 dimensions supported")
    assert points.dtype == DTYPE
    cdef int n = points.shape[0]
    cdef numpy.ndarray rows = numpy.zeros([n, n], dtype=DTYPE)
    cdef int i, j

    # We first abuse the last row of rows to store the values of p[î]*p[i]:
    p_2 = rows[n-1, :]
    for i in range(n):
        p_2[i] = points[i, 0]**2 + points[i, 1]**2 + points[i, 2]**2
    # Then we compute the upper triangle of the matrix p[i]^2 + p[j]^2 -2 (p[i]*p[j])_ij
    for i in range(n):
        rows[i, i] = 0.  # diagonal is 0.
        for j in range(i+1, n):
            rows[i, j] = p_2[i] + p_2[j] - 2.*(points[i, 0] * points[j, 0]
                                               + points[i, 1] * points[j, 1]
                                               + points[i, 2] * points[j, 2])
    # Finally, we mirror the matrix and set rows[n-1][n-1] = 0.
    for i in range(n):
        for j in range(i):
            rows[i, j] = rows[j, i]
    rows[n-1, n-1] = 0.
    return rows


if __name__ == "__main__":
    M = dist_matrix(setup_points(10))
    print(M[:5, :5])
