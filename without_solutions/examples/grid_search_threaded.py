#!/usr/bin/env python

import random
import time
from concurrent.futures import ThreadPoolExecutor

import requests


# has to be adapted for the courss:
URL = "http://localhost:8777"

N_THREADS = 150


def random_search(n_attempts):

    recipes = []

    for i in range(n_attempts):
        malt = random.uniform(0.1, 0.2)
        hops = random.uniform(0.01, 0.02)
        yeast = random.uniform(0.001, 0.005)
        temperature = random.uniform(40, 60)
        recipes.append((malt, hops, yeast, temperature))

    with ThreadPoolExecutor(N_THREADS) as executor:
        scores = list(executor.map(run_simulation, recipes))

    best_score = max(scores)
    position = scores.index(best_score)
    return best_score, recipes[position]


def grid_search(grid_size):

    recipes = []
    for i in range(grid_size):
        malt = grid_value(i, grid_size, 0.1, 0.2)

        for j in range(grid_size):
            hops = grid_value(j, grid_size, 0.01, 0.02)

            for k in range(grid_size):
                yeast = grid_value(k, grid_size, 0.001, 0.005)

                for l in range(grid_size):
                    temperature = grid_value(l, grid_size, 40, 60)

                    recipes.append((malt, hops, yeast, temperature))

    with ThreadPoolExecutor(N_THREADS) as executor:
        scores = list(executor.map(run_simulation, recipes))

    best_score = max(scores)
    position = scores.index(best_score)
    return best_score, recipes[position]


def grid_value(i, grid_size, min_value, max_value):
    return i / (grid_size - 1) * (max_value - min_value) + min_value


def run_simulation(recipe):
    malt, hops, yeast, temperature = recipe
    response = requests.get(
        URL, dict(malt=malt, hops=hops, yeast=yeast, temperature=temperature)
    )
    return float(response.text)


if __name__ == "__main__":
    started = time.time()

    print(random_search(2000))
    print(grid_search(8))

    needed = time.time() - started
    throughput = (2000 + 8 ** 4) / needed

    print(f"ran {throughput:.1f} simulations per second")
