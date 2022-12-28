import os
import random


def generate_tabu_search_params(datasets, timeout):
    """
    Essentially a grid search over the parameters of the simulated annealing algorithm.
    """

    # Set the parameters
    seeds = 30  # Set to the number of verification runs
    tabu_length = [2, 3, 4, 6, 8]  # https://iopscience.iop.org/article/10.1088/1742-6596/1235/1/012047/pdf
    max_steps = [1000]
    longest_hold = [500, 1000]
    # Generate the param file (Exclude anywhere longest_hold > max_steps)

    with open("tabu_param.txt", "w") as param_file:
        # Write the header
        param_file.write("seed,tabu_length,max_steps,longest_hold")
        # Write the parameters
        for i in range(seeds):
            # Generate a random seed
            seed = random.randint(0, 1000000)
            for tabu in tabu_length:
                for steps in max_steps:
                    for hold in longest_hold:
                        if hold > steps:
                            continue
                        for dataset in datasets:
                            param_file.write(f"\n{seed},{tabu},{steps},{hold},{dataset}")

    #   Close
    param_file.close()
    total_runs = seeds * len(tabu_length) * len(datasets)

    valid_params = [(x, y) for x in longest_hold for y in max_steps if x <= y]
    print(valid_params)
    print(len(valid_params))

    total_runs = total_runs * len(valid_params)



    print("Param file generated for Tabu Search" + f" ({total_runs} runs) with timeout of {timeout} seconds")
    return total_runs


def generate_simulated_annealing_params(datasets, timeout):
    """
    Essentially a grid search over the parameters of the simulated annealing algorithm.
    """

    # Set the parameters
    seeds = 30  # Set to the number of verification runs
    initial_temp = [100, 200]
    cooldown = [0.5, 0.8, 0.9]
    # Generate the param file
    with open("simu_param.txt", "w") as param_file:
        # Write the header
        param_file.write("seed,initial_temp,cooldown")
        # Write the parameters
        for i in range(seeds):
            # Generate a random seed
            seed = random.randint(0, 1000000)
            for temp in initial_temp:
                for cool in cooldown:
                    for dataset in datasets:
                        param_file.write(f"\n{seed},{temp},{cool},{dataset}")

    #   Close
    param_file.close()
    total_runs = seeds * len(initial_temp) * len(cooldown) * len(datasets)
    print("Param file generated for Simulated Annealing" + f" ({total_runs} runs) with timeout of {timeout} seconds")
    return total_runs


def generate_genetic_algorithm_params(datasets, timeout):
    """
    Essentially a grid search over the parameters of the ga params
    genetic_main(instance=None, seed=None, pop_size=None, ngen=None, mut_rate=None, cross_rate=None, timeout=None):
    """
    print(os.getcwd())
    # Set the parameters
    seeds = 30  # Set to the number of verification runs
    pop_size = [100, 200, 300, 500, 1000]
    ngen = [5000]
    mut_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    cross_rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # Generate the param file
    with open("process_helpers/genetic_param.txt", "w") as param_file:
        # Write the header
        param_file.write("seed,pop_size,ngen,mut_rate,cross_rate")
        # Write the parameters
        for i in range(seeds):
            # Generate a random seed
            seed = random.randint(0, 1000000)
            for pop in pop_size:
                for gen in ngen:
                    for mut in mut_rate:
                        for cross in cross_rate:
                            # Check cross and mut dont exceed 1
                            if cross + mut > 1:
                                continue
                            for dataset in datasets:
                                param_file.write(f"\n{seed},{pop},{gen},{mut},{cross},{dataset}")

    #   Close
    param_file.close()
    # Count lines in the file
    with open("process_helpers/genetic_param.txt") as f:
        total_runs = sum(1 for _ in f) - 1
    print("Param file generated for Genetic Algorithm" + f" ({total_runs} runs) with timeout of {timeout} seconds")
    # print the full path of the param file
    print("Param file path: " + os.path.abspath("../genetic_param.txt"))

    return total_runs

def calculate_runtime(total_runs, timeout):
    """
    Calculate the runtime of the algorithm
    """
    worst_case = total_runs * timeout
    # Format into hours, minutes, seconds
    hours = worst_case // 3600
    minutes = (worst_case % 3600) // 60
    seconds = (worst_case % 3600) % 60
    print(f"Worst Case runtime: {hours} hours, {minutes} minutes, {seconds} seconds")
    parallels = [10, 50, 100, 200, 300, 500, 1000]
    for parallel in parallels:
        hours = (worst_case / parallel) // 3600
        minutes = ((worst_case / parallel) % 3600) // 60
        seconds = ((worst_case / parallel) % 3600) % 60
        print(f"For {parallel} parallel instances: - {hours} hours, {minutes} minutes, {seconds} seconds")


if __name__ == '__main__':
    """
    Generate a param file to pass arguments to the jobshop solver on SLURM grid cluster
    - Removed abz8, la05, ft06
    """
    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    timeout_s = 60

    # total_runs = generate_simulated_annealing_params(datasets, timeout_s)
    total_runs = generate_genetic_algorithm_params(datasets, timeout_s)
    calculate_runtime(total_runs, timeout_s)