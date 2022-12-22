from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from src.data.script.load_instance import load_instance
from src.Solvers.constraint.jsp_fwk import JSSolution, JSProblem
from src.Solvers.constraint.jsp_fwk.solver import PriorityDispatchSolver, GoogleORCPSolver


def print_header(text):
    """
    Print the header for the section centered on the screen.
    :param text: The text to print in the header.
    """
    print('\n' + '=' * (len(text) + 2) + '\n' + text + '\n' + '=' * (len(text) + 2) + '\n')


def get_algorithms():
    """
    Allow user to select which algorithms to run individually or as a whole.
    :return: A list of selected Job Shop Scheduling algorithms.
    @TODO - Add tuning for additional selection - i.e. adding dispatching rules, etc.
    @TODO - Put real data here
    """

    # Get user input from terminal to select algorithms from a check box.
    all_algorithms = ['Google Or Tools', 'Dispatching Rules']
    print_header('Select Algorithms')
    # Get selection
    selected_algorithms = []
    for algorithm in all_algorithms:
        if input(f'{algorithm}? (y/n) ') == 'y':
            selected_algorithms.append(algorithm)
        # Skip case for testing
    return selected_algorithms


def load(dataset):
    """
    Load a dataset from the data folder.
    :param dataset:
    :return:
    """
    try:
        path, optimum = load_instance(dataset)
        print("Loaded dataset: " + dataset + " with optimum: " + str(optimum))
        return [path, optimum]
    except Exception as e:
        print(e)
        return [None, None]


def get_datasets():
    """
    Allow the user to select which datasets to run by source, individually, or as a whole.
    :return: A map of instance codes to optimal solutions for makespan
    """

    # Datasets collected by https://github.com/tamy0612
    # Five instances donated as ABZ5-9 due to Adams et al. [1].
    # Three instances donated as FT06, FT10 and FT20 due to Fisher and Thompson [2].
    # Forty instances donated as LA01-40 due to Lawrence [3].
    # Ten instances donated as ORB01-10 due to Applegate and Cook [4].
    # Twenty instances donated as SWV01-20 due to Storer et al. [5].
    # Four instances donated as yn1-4 due to Yamada and Nakano [6].
    # Eighty instances donated as ta01-80 due to Taillard [7].

    # Key map prefixes to sources
    # Source, [Prefix, Span]
    sources = {'Adams et Al.': ['abz', '5-9'],
               'Fisher and Thompson': ['ft', '06,10,20'],
               'Lawrence': ['la', '01-40'],
               'Applegate and Cook': ['orb', '01-10'],
               'Storer et al.': ['swv', '1-20'],
               'Yamada and Nakano': ['yn', '1-4'],
               'Taillard': ['ta', '01-80']}

    print_header('Select Datasets')

    # Select specific datasets
    selected_datasets = []
    while True:
        if input(f'Select specific dataset(s) (y) or test-set (n)? (y/n) ') == 'y':
            code = input(f'Input exact dataset code: ')
            # Get Optimum
            path, optimum = load(code)
            if optimum is None:
                print(f'Dataset {code} not found.')
                continue
            selected_datasets.append(code)
        else:
            test_set = [
                "abz5",
                "abz6",
                "abz7",
                "abz8",
                "abz9",
                "ft06",
                "ft10",
                "ft20",
                "la01",
                "la02",
                "la03",
                "la04",
                "la05"]
            scores = {}
            for dataset in test_set:
                path, optimum = load(dataset)
                if optimum is None:
                    print(f'Dataset {dataset} not found.')
                    continue
                scores[dataset] = optimum
            print(scores)
            selected_datasets.append(test_set)
            return selected_datasets


    # Get user input from terminal to select datasets from a check box.

    for source in sources:
        if input(f'{source}? (y/n) ') == 'y':

            # Get prefix
            prefix = sources[source][0]
            # Get each instance
            case = sources[source][1]
            if '-' in case:  # Range
                span = case.split('-')
                start = int(span[0])
                end = int(span[1])
                for i in range(start, end + 1):
                    # Handle 0 padding
                    non_padded = ('abz', 'yn')
                    if i < 10 and prefix not in non_padded:
                        code = prefix + '0' + str(i)
                    else:
                        code = prefix + str(i)
                    path, optimum = load(code)
                    selected_datasets.append(code)
            else:  # Singular
                for instance in case.split(','):
                    code = prefix + instance
                    path, optimum = load(code)
                    selected_datasets.append(code)

    print(f'Selected {len(selected_datasets)} datasets.')
    return selected_datasets



def run_algorithms(Algorithms, Datasets):
    """
    Run the selected algorithms on the selected datasets.
    :param Algorithms: A list of strings representing the algorithms to run.
    :param Datasets: A map of dataset code to [file path, optimal solution]
    # @TODO - Add support for multiple algorithms
    """
    for dataset in Datasets:
        problem = JSProblem(benchmark=dataset)
        # Structural pattern match for the algorithms
        for alg in Algorithms:
            if alg == 'Google Or Tools':
                solver = GoogleORCPSolver()
                do_solve(problem, solver)
            elif alg == 'Dispatching Rules':
                rules = ['spt', 'mopr', 'mwkr', 'hh', 'ihh']
                solver = PriorityDispatchSolver(rule=rules[-1])
                do_solve(problem, solver)
            else:
                print(f'Algorithm {alg} not found.')
                continue


def do_solve(problem, solver):
    # @TODO only solve if there is not already a solution recorded
    solver.solve(problem=problem, interval=2000, callback=print_intermediate_solution)
    solver.wait()
    print('----------------------------------------')
    if solver.status:
        print(f'Problem: {len(problem.jobs)} jobs, {len(problem.machines)} machines')
        print(f'Optimum: {problem.optimum}')
        print(f'Solution: {problem.solution.makespan}')
        print(f'Terminate successfully in {solver.user_time} sec.')
        # Add to file if not already in file
        with open('data/outputs/results.csv', 'r+') as f:
            # Headers are Dataset, Algorithm, Optimum, Solution, Time
            # If there is not an entry for this dataset and algorithm, add it
            if not any(line.startswith(f'{problem.name},{solver.name}') for line in f):
                f.write(f'{problem.name},{solver.name},{problem.optimum},{problem.solution.makespan},{solver.user_time}\n')
    else:
        print(f'Solving process failed in {solver.user_time} sec.')


def print_intermediate_solution(solution: JSSolution):
    logging.info(f'Makespan: {solution.makespan}')


def compare_algorithms(Algorithms, Datasets):
    return None


def estimate_runtime(Algorithms, Datasets):
    calculate_combinations(Datasets)
    return None


def calculate_combinations(Dataset):
    return None


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


