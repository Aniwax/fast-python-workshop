import os
import pprint
import sys
import time
import platform

time.sleep(30)

res = {
    "cwd": os.getcwd(),
    "python": sys.version,
    "hostname": platform.node(),
    "pid": os.getpid(),
    "os.cpu_count() ": os.cpu_count(),
    "SLURM_CPUS_PER_TASK": int(os.environ["SLURM_CPUS_PER_TASK"]),
}

pprint.pprint(res)
