import csv
import os

from jobshop import *


def simu_main(seed=None, mode=None, timeout=None):
    files = (os.listdir(os.getcwd() + "/instances"))
    print(files)

    if seed is None:
        seed = int(input("seed: "))

    if mode is None:
        mode = input("mode: ")

    if timeout is None:
        timeout = int(input("timeout [30]: ") or 30)

    scores = {}

    for file in files:
        jobs = Jobs('instances/' + file)

        m = len(jobs[0])
        j = len(jobs)
        print("Chosen file:", file)
        print("Number of machines:", m)
        print("Number of jobs:", j)
        printJobs(jobs)

        cost, solution = simulatedAnnealingSearch(jobs, maxTime=timeout, T=int(200), termination=int(10),
                                                  halting=int(10),
                                                  mode='random', decrease=float(0.8))

        printSchedule(jobs, solution)

        scores[file] = cost
    print(scores)
    csv_columns = files

    csv_file = f"{os.environ['OUTPUT_DIR']}/scores-{os.environ['SLURM_ARRAY_TASK_ID']}.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(scores)
    except IOError:
        print("I/O error")


if __name__ == '__main__':
    simu_main()
