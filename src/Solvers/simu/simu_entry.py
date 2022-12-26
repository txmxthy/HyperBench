#!/usr/bin/env python3
import os

from main import simu_main

with open("simu_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
print(f"Hello! This is Simulated Annealing - Task {task_id}")

seed, mode = lines[task_id-1].split(',')

timeout = 1200
simu_main(seed, mode, timeout)

