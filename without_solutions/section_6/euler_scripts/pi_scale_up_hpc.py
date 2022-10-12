import os
import time
from concurrent.futures import ProcessPoolExecutor
from random import uniform


def approx_pi(n_attempts):
    n_hits = 0
    for _ in range(n_attempts):
        x = uniform(-1.0, 1.0)
        y = uniform(-1.0, 1.0)
        if x ** 2 + y ** 2 <= 1.0:
            n_hits += 1
    return n_hits


def main():
    num_points = 2_000_000

    num_workers = int(os.environ.get("SLURM_NTASKS", os.cpu_count()))

    num_points_worker = [int(num_points / num_workers) for _ in range(num_workers)]
    num_points = sum(num_points_worker)

    started = time.time()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(approx_pi, num_points_worker)
    duration = time.time() - started
    print("The estimates value of Pi is: {}".format(sum(results) * 4 / num_points))
    print(f"Execution time: {duration:.3f}s using {num_workers=}")


if __name__ == "__main__":
    main()
