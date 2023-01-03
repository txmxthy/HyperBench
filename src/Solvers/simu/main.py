import csv
import os

import numpy

from jobshop import *


def simu_main(seed=None, temp=None, cooldown=None, timeout=None, instance=None):
    files = (os.listdir(os.getcwd() + "/instances"))
    print(files)
    # Print params
    print(f"Seed: {seed}, Instance: {instance}, Temp: {temp}, Cooldown: {cooldown}, Timeout: {timeout}")

    if seed is None:
        seed = int(input("seed: ") or 0)

    # Set the seed
    random.seed(seed)
    numpy.random.seed(seed)

    if temp is None:
        temp = int(input("temp: ") or 200)
    if cooldown is None:
        cooldown = float(input("cooldown: ") or 0.8)
    if timeout is None:
        timeout = int(input("timeout: ") or 5)

    scores = {}

    # for file in files:

    jobs = Jobs('instances/' + instance)

    m = len(jobs[0])
    j = len(jobs)
    print("Chosen file:", instance)
    print("Number of machines:", m)
    print("Number of jobs:", j)
    printJobs(jobs)
    
    #//@TODO ADD TERMINATION AND HALTING TO PARAMS https://scialert.net/fulltext/?doi=jas.2009.662.670https://scialert.net/fulltext/?doi=jas.2009.662.670
    (cost, solution), timedOut = simulatedAnnealingSearch(jobs,
                                                          maxTime=timeout,
                                                          T=int(temp),
                                                          termination=int(10),
                                                          halting=int(10),
                                                          mode='random',
                                                          decrease=float(cooldown))

    # printSchedule(jobs, solution)
    print("Cost:" + str(cost), "Timed Out: " + str(timedOut))
    schedule_to_gantt_json(jobs, solution, cost, instance)

    csv_columns = instance, cost, seed, temp, cooldown, timeout,os.environ['SLURM_ARRAY_TASK_ID']

    csv_file = f"{os.environ['OUTPUT_DIR']}/csv/results-{os.environ['SLURM_ARRAY_TASK_ID']}.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
    except IOError:
        print("I/O error")


if __name__ == '__main__':
    simu_main()
    print("Done")
