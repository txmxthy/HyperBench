import csv
import os

import numpy

from jobshop import *


def simu_main(seed=None, temp=None, cooldowwn=None, timeout=None, instance=None):
    files = (os.listdir(os.getcwd() + "/instances"))
    print(files)
    # Print params
    print(f"Seed: {seed}, Instance: {instance}, Temp: {temp}, Cooldown: {cooldowwn}, Timeout: {timeout}")


    if seed is None:
        seed = int(input("seed: ") or 0)

    # Set the seed
    random.seed(seed)
    numpy.random.seed(seed)

    if temp is None:
        temp = int(input("temp: ") or 200)
    if cooldowwn is None:
        cooldowwn = float(input("cooldown: ") or 0.8)
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

    (cost, solution), timedOut = simulatedAnnealingSearch(jobs,
                                                          maxTime=timeout,
                                                          T=int(temp),
                                                          termination=int(10),
                                                          halting=int(10),
                                                          mode='random',
                                                          decrease=float(cooldowwn))

    printSchedule(jobs, solution)
    print("TEST:" + str(cost), "Timed Out?" + str(timedOut))
    # @Todo Solutions are not being saved (Output is saved)

    csv_columns = instance, cost, seed, temp, cooldowwn, timeout

    csv_file = f"{os.environ['OUTPUT_DIR']}/results-{os.environ['SLURM_ARRAY_TASK_ID']}.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            # for data in csv_columns:
            #     writer.writerow(data)

    except IOError:
        print("I/O error")




if __name__ == '__main__':
    simu_main()
    print("Done")
