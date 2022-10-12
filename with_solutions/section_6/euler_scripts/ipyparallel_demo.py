import os
import pprint

import ipyparallel as ipp

n_engines = int(os.environ.get("SLURM_NTASKS", os.cpu_count()))

## Configure the ipython parallel cluster
cluster = ipp.Cluster(
    n=n_engines,
    controller_ip="*",
    engine_launcher_class="MPI",
    location="server.local",
)

## Start the ipython parallel cluster
cluster.start_cluster_sync()

## Connect a client to the cluster
client = cluster.connect_client_sync()

## Make sure all engines are connected
client.wait_for_engines(n=n_engines)

dview = client[:]


def summary(secs=1):
    import os
    import sys
    import time

    time.sleep(secs)

    return {
        "cwd": os.getcwd(),
        "python": sys.version,
        "hostname": os.uname().nodename,
        "pid": os.getpid(),
    }


ar = dview.apply(summary, 4)

## Future API
pprint.pprint(ar.result())

## Stop the cluster
cluster.stop_cluster_sync()
