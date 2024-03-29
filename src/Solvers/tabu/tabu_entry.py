#!/usr/bin/env python3
import os

from main import tabu_main

with open("tabu_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["RUN_KEY"])
print(f"Hello! This is Tabu Search - Task {task_id}")

seed, tabu_length, steps, hold, instance = lines[task_id].split(',')

timeout = 60*5
tabu_main(seed=int(seed),
          tabu_len=int(tabu_length),
          nsteps=float(steps),
          timeout=int(timeout),
          hold=int(hold),
          instance=instance.strip())
