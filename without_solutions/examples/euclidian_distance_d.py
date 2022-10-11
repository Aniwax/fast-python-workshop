#!/usr/bin/env python3
"""Euclidean distance example in d-dimensional space"""


def setup_points(n, d=100_000):
    # create n points in d-dim for testing
    points = []
    for i in range(0, d * n, d):
        points.append(tuple(1 + float(i // (j+1)) for j in range(d)))
    return points


def dist_squared(a, b):
    s = 0
    d = len(a)
    for i in range(d):
        s += (a[i] - b[i]) ** 2
    return s


def dist_matrix(points, dist_func=dist_squared):
    # compute distance matrix using given `dist_func`
    rows = []
    for p in points:
        row = []
        for q in points:
            row.append(dist_func(p, q))
        rows.append(row)
    return rows


if __name__ == "__main__":
    M = dist_matrix(setup_points(10))
    for row in M[:5]:
        print(row[:5])
