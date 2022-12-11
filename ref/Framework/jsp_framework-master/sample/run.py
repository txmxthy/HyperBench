import logging
from simulation import (JSProblem, JSSolution)
from simulation.solver import (GoogleORCPSolver)


def print_intermediate_solution(solution: JSSolution):
    logging.info(f'Makespan: {solution.makespan}')


if __name__ == '__main__':

    # ----------------------------------------
    # create problem from data
    # ----------------------------------------
    problem = JSProblem(benchmark='ft10')

    # ----------------------------------------
    # test built-in solver
    # ----------------------------------------
    # googl or-tools
    s = GoogleORCPSolver()

    # priority dispatching
    rules = ['spt', 'mopr', 'mwkr', 'hh', 'ihh']
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
