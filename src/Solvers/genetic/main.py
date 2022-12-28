import csv
import os
from alg.utils import readFilePairs
from alg.jspGA import genetic


def genetic_main(instance=None, seed=None, pop_size=None, ngen=None, mut_rate=None, cross_rate=None, timeout=None):
    target = None
    # Print the location of this file
    path = os.path.dirname(os.path.abspath(__file__))
    path += "/cases/"
    files = os.listdir(path)
    print(files)


    if pop_size is None:
        pop_size = int(input('Please input the size of population (default: 30): ') or 30)

    if ngen is None:
        ngen = int(input('Please input the number of generations (default: 100): ') or 100)

    if mut_rate is None:
        mut_rate = float(input('Please input the mutation rate (default: 0.1): ') or 0.1)
    if cross_rate is None:
        cross_rate = float(input('Please input the crossover rate (default: 0.1): ') or 0.1)
    if seed is None:
        seed = int(input('Please input the seed (default: 0): ') or 0)
    if timeout is None:
        timeout = int(input('Please input the timeout (default: 60): ') or 60)
    if instance not in files or instance is None:
        instance = "abz5"


    times, machines, n = readFilePairs("cases/" + instance)

    cost = genetic(times, machines, n, pop_size, ngen, mut_rate, target, maxTime=timeout, instance=instance)


    csv_columns = instance, cost, seed, pop_size, ngen, mut_rate, cross_rate, timeout

    csv_file = f"{os.environ['OUTPUT_DIR']}/results-{os.environ['SLURM_ARRAY_TASK_ID']}.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

    except IOError:
        print("I/O error")


if __name__ == '__main__':
    genetic_main()