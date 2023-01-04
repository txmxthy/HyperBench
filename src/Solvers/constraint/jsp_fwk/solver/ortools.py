import logging
import sys
from collections import (namedtuple, defaultdict)
from ortools.sat.python import cp_model
from ..common.exception import JSPException
from ..model.solver import JSSolver
from ..model.problem import JSProblem
from ..model.solution import JSSolution


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    '''Output intermediate solutions.

    https://github.com/google/or-tools/blob/stable/ortools/sat/doc/solver.md#printing-intermediate-solutions
    '''

    def __init__(self, variables: dict, problem: JSProblem, solution: JSSolution):
        '''Initialize with variable map: operation step -> OR-Tools variable.'''
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__problem = problem
        self.__solution = solution

    def on_solution_callback(self):
        '''Pass data back to domain class.'''
        # assign OR-Tools solution back to JSPSolution
        for op, var in self.__variables.items():
            op.update_start_time(self.Value(var.start))

        # update solution
        self.__problem.update_solution(self.__solution)

        # Check if early stop is requested.
        if self.__solution.early_termination:
            logging.info('Early Stop Identified.')
            self.StopSearch()


class GoogleORCPSolver(JSSolver):

    def __init__(self, name: str = None, max_time: int = None) -> None:
        '''Solve JSP with Google OR-Tools.

        Args:
            name (str, optional): Solver name.
            max_time (int, optional): Max solving time in seconds. Defaults to None, i.e. no limit.
        '''
        super().__init__(name)
        self.__max_time = max_time

    def do_solve(self, problem: JSProblem):
        '''Solve JSP with Google OR-Tools.

        https://developers.google.cn/optimization/scheduling/job_shop
        '''
        # Initialize an empty solution from problem
        solution = JSSolution(problem)

        # create model
        model, variables = self.__create_model(solution)

        # set solver
        solver = cp_model.CpSolver()

        # print parameter to stderr
        print(f"A1: Solver Catch SIGINT{solver.parameters.catch_sigint_signal}", file=sys.stderr)
        print(f"A2: Solver Threading{solver.parameters.num_workers}", file=sys.stderr)
        solver.parameters.catch_sigint_signal = True  # REQUIRED FOR SLURM/Parallel *Solvers*
        solver.parameters.num_workers = 1  # REQUIRED FOR SLURM/Parallel *Solvers*
        print(f"B1: Solver Catch SIGINT{solver.parameters.catch_sigint_signal}", file=sys.stderr)
        print(f"B2: Solver Threading {solver.parameters.catch_sigint_signal}", file=sys.stderr)
        if self.__max_time is not None:
            solver.parameters.max_time_in_seconds = self.__max_time  # set time limit

        solution_printer = VarArraySolutionPrinter(variables, problem, solution)
        status = solver.Solve(model, solution_callback=solution_printer)

        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            raise JSPException('No feasible solution found.')

    def __create_model(self, solution: JSSolution):
        '''Create Google OR-Tools model: variables, constraints and objective.'''
        # create the model: constraint programming
        model = cp_model.CpModel()

        # create variables
        variable = namedtuple('variable', 'start, end, interval')  # variable for a single operation
        max_time = sum(op.source.duration for op in solution.ops)  # upper bound of variables

        variables = {}  # all variables
        machine_intervals = defaultdict(list)  # interval variables assigned to same machine
        for op in solution.ops:
            source = op.source
            i = source.id
            start_var = model.NewIntVar(0, max_time, f'start-{i}')
            end_var = model.NewIntVar(0, max_time, f'end-{i}')
            interval_var = model.NewIntervalVar(start_var, source.duration, end_var, f'interval-{i}')
            variables[op] = variable(start=start_var, end=end_var, interval=interval_var)
            machine_intervals[source.machine].append(interval_var)

        # apply constraints
        # (1) no overlap for operations assigned to same machine
        for machine, interval_vars in machine_intervals.items():
            model.AddNoOverlap(interval_vars)

        # (2) operation sequence inside a job
        pre = None
        for op, var in variables.items():
            if pre and pre.source.job == op.source.job:
                pre_var = variables[pre]
                model.Add(pre_var.end <= var.start)
            pre = op

        # objective: makespan
        obj_var = model.NewIntVar(0, max_time, 'makespan')
        model.AddMaxEquality(obj_var, [variables[ops[-1]].end for job, ops in solution.job_ops.items()])
        model.Minimize(obj_var)

        return model, variables
