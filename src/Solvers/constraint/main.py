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


def constraint_main(instance, timeout):
    algorithm = ['Google Or Tools']
    dataset = [instance]

    parameters = {"timeout": timeout}

    util.run_algorithms(algorithm, dataset, parameters)



# No. Rules   Description                     Type
# ----------------------------------------------------
# 1   FIFO    First In First Out              Static
# 2   LIFO    Last In First Out               Static
# 3   SPT     Shortest Processing Time        Static
# 4   LPT     Longest Processing Time         Static
# 5   SPS     Shortest Process Sequence       Static
# 6   LPS     Longest Process Sequence        Static
# 7   STPT    Shortest Total Processing Time  Static
# 8   LTPT    Longest Total Processing Time   Static
# 9   ECT     Earliest Creation Time          Dynamic
# 10  LCT     Longest Creation Time           Dynamic
# 11  SWT     Shortest Waiting Time           Dynamic
# 12  LWT     Longest Waiting Time            Dynamic
# 13  LTWR    Least Total Work Remaining      Dynamic
# 14  MTWR    Most Total Work Remaining       Dynamic
#
# These rules are based on 3 static parameters:
#
# - Processing Time       : Time required to complete an operation on a specific machine.
# - Process Sequence      : Total count of operations to complete a job.
# - Total Processing Time : Total time required to complete a job.
#
# and 3 dynamic parameters depending on the passage of time:
#
# - Creation Time         : The time when an operation arriving at a machine.
# - Waiting Time          : The time that an operation spent when waiting in the queue line on machine.
# - Total Work Remaining  : The time for a job to complete the remaining operations.


def dispatching_main(instance, timeout, rules):
    algorithm = ['Dispatching Rules']
    dataset = [instance]
    parameters = {"timeout": timeout,
                  "rules": rules}

    util.run_algorithms(algorithm, dataset, parameters)


if __name__ == '__main__':
    # main()
    # constraint_main('abz5', 60)
    dispatching_main('abz5', 60, ['spt', 'mopr', 'mwkr', 'hh', 'ihh'])