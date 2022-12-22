#!/usr/bin/env python3
import os

from main import simu_main

lines: list[str] = []
with open("simu_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
seed, mode = lines[task_id].split(',')

timeout = 1200
simu_main(seed, mode, timeout)

