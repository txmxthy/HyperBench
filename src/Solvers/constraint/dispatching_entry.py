#!/usr/bin/env python3
import os

from main import dispatching_main

with open("dispatching_inputs.txt", "r") as f:
    lines = f.readlines()

task_id = int(os.environ["RUN_KEY"])

print(f"Hello! This is Dispatching Rules - Task {task_id}")

seed, rules = lines[task_id].split(',')
rules = rules.split(':')
timeout = 60 * 5

datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
dispatching_main(datasets=datasets,
                 seed=int(seed),
                 rules=rules,
                 timeout=int(timeout))
