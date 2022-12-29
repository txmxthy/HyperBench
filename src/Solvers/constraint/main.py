import os

import util


def main():
    """
    Old Local Running Method I wrote to begin with
    """
    # Select Algorithms
    Algorithms = util.get_algorithms()  # ✔️
    print("Selected Algorithms:" + str(Algorithms))
    # Select Datasets
    Datasets = util.get_datasets()  # ✔️

    # Run Algorithms
    # Approach:
    # Create algorithm object , job object, machine object, task object
    # The algorithm object will have a method to run the algorithm and return the schedule
    # The job object will have a method to get the start time and end time of the job
    # The machine object will have a method to get the start time and end time of the machine

    util.run_algorithms(Algorithms, Datasets)


def constraint_main(seed, instance, timeout):
    dataset = [instance]
    parameters = {"seed": seed,
                  "timeout": timeout}

    util.run_algorithms(['Google Or Tools'], dataset, parameters)


def dispatching_main(seed, datasets, timeout, rules):
    parameters = {"seed": seed,
                  "timeout": timeout,
                  "rules": rules}

    util.run_algorithms(['Dispatching Rules'], datasets, parameters)



if __name__ == '__main__':
    # main()
    os.system("SLURM_ARRAY_TASK_ID=1 OUTPUT_DIR=/home/kali/PycharmProjects/Capstone/jobs/output/constraint RUN_KEY=3 python3 constraint_entry.py")
    # constraint_main(30,'abz5', 60)
    # dispatching_main(20, 'abz5', 60, ['mopr', 'mwkr', 'hh', 'ihh'])
