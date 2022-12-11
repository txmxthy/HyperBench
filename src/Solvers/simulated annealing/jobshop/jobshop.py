import fileinput
import random

def Jobs(path=None):
    with fileinput.input(files=path) as f:
        next(f)
        jobs = [[(int(machine), int(time)) for machine, time in zip(*[iter(line.split())]*2)]
                    for line in f if line.strip()]
    return jobs

def printJobs(jobs):
    print(len(jobs), len(jobs[0]))
    for job in jobs:
        for machine, time in job:
            print(machine, time, end=" ")
        print()


def cost(jobs, schedule):
    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j
    tm = [0]*m

    ij = [0]*j

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1

        start = max(tj[i], tm[machine])
        end = start + time
        tj[i] = end
        tm[machine] = end

    return max(tm)


def costPartial(jobs, partialSchedule):
    return cost(jobs, normalizeSchedule(partialSchedule))

def normalizeSchedule(jobs, partialSchedule):
    j = len(jobs)
    m = len(jobs[0])

    occurences = [0] * j
    normalizedSchedule = []

    for t in partialSchedule:
        if occurences[t] < m:
            normalizedSchedule.append(t)
            occurences[t] += 1
        else:
            pass

    for t, count in enumerate(occurences):
        if count < m:
            normalizedSchedule.extend([t] * (m - count))

    return normalizedSchedule

class OutOfTime(Exception):
    pass

def randomSchedule(j, m):
    schedule = [i for i in list(range(j)) for _ in range(m)]
    random.shuffle(schedule)
    return schedule



def printSchedule(jobs, schedule):
    def format_job(time, jobnr):
        if time == 1:
            return '#'
        if time == 2:
            return '[]'

        js = str(jobnr)

        if 2 + len(js) <= time:
            return ('[{:^' + str(time - 2) + '}]').format(jobnr)

        return '#' * time

    j = len(jobs)
    m = len(jobs[0])

    tj = [0]*j
    tm = [0]*m

    ij = [0]*j

    output = [""] * m

    for i in schedule:
        machine, time = jobs[i][ij[i]]
        ij[i] += 1
        start = max(tj[i], tm[machine])
        space = start - tm[machine]
        end = start + time
        tj[i] = end
        tm[machine] = end

        output[machine] += ' ' * space + format_job(time, i)

    print("")
    print("Optimal Schedule: ")
    [print("Machine ", idx, ":", machine_schedule) for idx, machine_schedule in enumerate(output)]
    print("")
    print("Optimal Schedule Length: ", max(tm))


def lowerBound(jobs):
    def lower0():
        return max(sum(time for _, time in job) for job in jobs)
    def lower1():
        mtimes = [0]*numMachines(jobs)

        for job in jobs:
            for machine, time in job:
                mtimes[machine] += time

        return max(mtimes)

    return max(lower0(), lower1())


def numMachines(jobs):
    return len(jobs[0])


def numJobs(jobs):
    return len(jobs)


def shuffle(x, start=0, stop=None):
    if stop is None or stop > len(x):
        stop = len(x)

    for i in reversed(range(start + 1, stop)):
        j = random.randint(start, i)
        x[i], x[j] = x[j], x[i]