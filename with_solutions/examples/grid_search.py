#!/usr/bin/env python

import random
import requests
import time


# has to adapted for the course:
URL = "http://localhost:8777"


def random_search(n_attempts):
    best_score = None
    best_recipe = None

    for i in range(n_attempts):
        malt = random.uniform(0.1, 0.2)
        hops = random.uniform(0.01, 0.02)
        yeast = random.uniform(0.001, 0.005)
        temperature = random.uniform(40, 60)

        score = run_simulation(malt, hops, yeast, temperature)
        if best_score is None or score > best_score:
            best_score = score
            best_recipe = (malt, hops, yeast, temperature)

    return best_score, best_recipe


def grid_search(grid_size):

    best_score = None
    best_recipe = None

    recipes = []
    for i in range(grid_size):
        malt = grid_value(i, grid_size, 0.1, 0.2)

        for j in range(grid_size):
            hops = grid_value(j, grid_size, 0.01, 0.02)

            for k in range(grid_size):
                yeast = grid_value(k, grid_size, 0.001, 0.005)

                for l in range(grid_size):
                    temperature = grid_value(l, grid_size, 40, 60)

                    score = run_simulation(malt, hops, yeast, temperature)
                    if best_score is None or score > best_score:
                        best_score = score
                        best_recipe = (malt, hops, yeast, temperature)

    return best_score, best_recipe


def grid_value(i, grid_size, min_value, max_value):
    return i / (grid_size - 1) * (max_value - min_value) + min_value


def run_simulation(malt, hops, yeast, temperature):
    response = requests.get(
        URL, dict(malt=malt, hops=hops, yeast=yeast, temperature=temperature)
    )
    return float(response.text)


if __name__ == "__main__":
    started = time.time()
    print(random_search(30))
    print(grid_search(3))

    needed = time.time() - started
    throughput = (30 + 3 ** 4) / needed

    print(f"ran {throughput:.1f} simulations per second")
