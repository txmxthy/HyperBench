import csv
import logging
from jsp_fwk import (JSProblem, JSSolution)
from jsp_fwk.solver import (GoogleORCPSolver, PriorityDispatchSolver)


def print_intermediate_solution(solution: JSSolution):
    logging.info(f'Makespan: {solution.makespan}')


if __name__ == '__main__':
    maxTime = int(input("Input the max time in seconds for each instance:"))
    # ----------------------------------------
    # create problem from benchmark
    # ----------------------------------------
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
    for file in test_set:
        print("Solving:", file)
        problem = JSProblem(benchmark=file)

        s = GoogleORCPSolver(max_time=maxTime)

        # priority dispatching_rules
        # rules = ['spt', 'mopr', 'mwkr', 'hh', 'ihh']
        # s = PriorityDispatchSolver(rule=rules[-1])

        # ----------------------------------------
        # solve and result
        # ----------------------------------------
        s.solve(problem=problem, interval=2000, callback=print_intermediate_solution)
        s.wait()
        print('----------------------------------------')
        if s.status:
            print(f'Problem: {len(problem.jobs)} jobs, {len(problem.machines)} machines')
            print(f'Optimum: {problem.optimum}')
            print(f'Solution: {problem.solution.makespan}')
            print(f'Terminate successfully in {s.user_time} sec.')
        else:
            print(f'Solving process failed in {s.user_time} sec.')
        scores[file] = problem.solution.makespan
    print(scores)
    csv_columns = test_set

    csv_file = "scores.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(scores)
    except IOError:
        print("I/O error")