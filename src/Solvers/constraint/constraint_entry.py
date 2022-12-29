#!/usr/bin/env python3
import os

from main import constraint_main

with open("constraint_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
print(f"Hello! This is Constraint Solver (Google OR) - Task {task_id}")

seed, instance = lines[task_id].split(',')

timeout = 20
constraint_main(seed=int(seed),
                timeout=int(timeout),
                instance=instance.strip())
