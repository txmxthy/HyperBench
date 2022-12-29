#!/usr/bin/env python3
import os

from main import simu_main

with open("simu_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
print(f"Hello! This is Simulated Annealing - Task {task_id}")

seed, inital_temp, cooldown, instance = lines[task_id].split(',')

timeout = 10
simu_main(seed=int(seed),
          temp=int(inital_temp),
          cooldown=float(cooldown),
          timeout=int(timeout),
          instance=instance.strip())

