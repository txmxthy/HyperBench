import random

def generate_tabu_search_params(datasets, timeout):
    """
    Essentially a grid search over the parameters of the simulated annealing algorithm.
    """

    # Set the parameters
    seeds = 30 # Set to the number of verification runs
    tabu_length = [5, 10, 15, 20]



def generate_simulated_annealing_params(datasets, timeout):
    """
    Essentially a grid search over the parameters of the simulated annealing algorithm.
    """

    # Set the parameters
    seeds = 30 # Set to the number of verification runs
    initial_temp = [100, 200]
    cooldown = [0.5, 0.8, 0.9]
    # Generate the param file
    with open("param.txt", "w") as param_file:
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

    total_runs = generate_simulated_annealing_params(datasets, timeout_s)
    calculate_runtime(total_runs, timeout_s)