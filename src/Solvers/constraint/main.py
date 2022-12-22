import src.util as util

if __name__ == '__main__':
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



