import os
import pprint
import sys
import time

from dask.distributed import Client
from dask_mpi import initialize

n_workers = int(os.environ.get("SLURM_NTASKS", os.cpu_count())) - 2

## memory in bytes on Euler
mem = (
    1024 * 1024 * int(os.environ["SLURM_MEM_PER_CPU"])
    if os.environ.get("SLURM_MEM_PER_CPU")
    else "auto"
)

# Run within MPI env
initialize(nthreads=1, memory_limit=mem, local_directory="~/dask-mpi-workers")

## Configure and start the cluster
client = Client()

## Make sure all engines are connected
client.wait_for_workers(n_workers=n_workers)


def summary(secs=1):
    time.sleep(secs)

    return {
        "cwd": os.getcwd(),
        "python": sys.version,
        "hostname": os.uname().nodename,
        "pid": os.getpid(),
    }


futures = client.map(summary, range(n_workers + 2))
results = client.gather(futures)
pprint.pprint(results)
