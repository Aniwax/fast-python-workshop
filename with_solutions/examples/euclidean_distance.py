#!/usr/bin/env python3
"""Euclidean distance example in 3 dimensional space"""


def setup_points(n):
    # create n points in 3d for testing
    points = []
    for i in range(0, 3 * n, 3):
        points.append((float(i), 1 + float(i // 2), 1 + float(i // 3)))
    return points


def dist_squared(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def dist_matrix(points):
    rows = []
    for p in points:
        row = []
        for q in points:
            row.append(dist_squared(p, q))
        rows.append(row)
    return rows


if __name__ == "__main__":
    M = dist_matrix(setup_points(1000))
    for row in M[:5]:
        print(row[:5])
