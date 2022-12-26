from .jobshop import *

import math
import random
import time


def getNeigbors(state, mode="normal"):
    allNeighbors = []

    for i in range(len(state) - 1):
        neighbor = state[:]
        if mode == "normal":
            swapIndex = i + 1
        elif mode == "random":
            swapIndex = random.randrange(len(state))
        neighbor[i], neighbor[swapIndex] = neighbor[swapIndex], neighbor[i]
        allNeighbors.append(neighbor)

    return allNeighbors


def simulatedAnnealing(jobs, T, termination, halting, mode, decrease):
    """
    Simulated Annealing
    :param jobs: list of jobs
    :param T: initial temperature
    :param termination: number of iterations in each temperature
    :param halting: number of halting iterations
    :param mode: mode of neighbor generation
    :param decrease: cooldown factor
    """
    numberOfJobs = len(jobs)
    numberOfMachines = len(jobs[0])

    state = randomSchedule(numberOfJobs, numberOfMachines)

    for i in range(halting):
        T = decrease * float(T)

        for k in range(termination):
            actualCost = cost(jobs, state)

            for n in getNeigbors(state, mode):
                nCost = cost(jobs, n)
                if nCost < actualCost:
                    state = n
                    actualCost = nCost
                else:
                    probability = math.exp(-nCost / T)
                    if random.random() < probability:
                        state = n
                        actualCost = nCost

    return actualCost, state


def simulatedAnnealingSearch(jobs, maxTime=None, T=200, termination=10, halting=10, mode="random", decrease=0.8):
    """
    Simulated Annealing Search
    :param jobs: list of jobs
    :param maxTime: maximum time to run the algorithm  (in seconds) per
    :param T: initial temperature
    :param termination: number of iterations in each temperature
    :param halting: number of halting iterations
    :param mode: mode of neighbor generation
    :param decrease: cooldown factor
    :return: best cost and best schedule
    """
    numExperiments = 1

    solutions = []
    best = 10000000

    t0 = time.time()
    totalExperiments = 0

    j = len(jobs)
    m = len(jobs[0])
    rs = randomSchedule(j, m)

    while True:
        try:
            start = time.time()

            for i in range(numExperiments):
                cost, schedule = simulatedAnnealing(jobs, T=T, termination=termination, halting=halting, mode=mode,
                                                    decrease=decrease)

                if cost < best:
                    best = cost
                    solutions.append((cost, schedule))

            totalExperiments += numExperiments

            if maxTime and time.time() - t0 > maxTime:
                raise OutOfTime("Time is over")

            t = time.time() - start
            if t > 0:
                print("Best:", best, "({:.1f} Experiments/s, {:.1f} s)".format(
                    numExperiments / t, time.time() - t0))

            if t > 4:
                numExperiments //= 2
                numExperiments = max(numExperiments, 1)
            elif t < 1.5:
                numExperiments *= 2

        except (KeyboardInterrupt, OutOfTime) as e:
            timedOut = isinstance(e, OutOfTime)

            print()
            print("================================================")
            print("Best solution:")
            print(solutions[-1][1])
            print("Found in {:} experiments in {:.1f}s".format(totalExperiments, time.time() - t0))

            if timedOut:
                print("Time is over")

            return solutions[-1], timedOut
