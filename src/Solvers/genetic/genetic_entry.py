#!/usr/bin/env python3
import os

from main import genetic_main

with open("genetic_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
print(f"Hello! This is Tabu Search - Task {task_id}")

seed, pop, gen, mut, cross, dataset = lines[task_id].split(',')
timeout = 60 * 5

genetic_main(instance=dataset.strip(),
             seed=int(seed),
             pop_size=int(pop),
             ngen=int(gen),
             mut_rate=float(mut),
             cross_rate=float(cross),
             timeout=int(timeout))
