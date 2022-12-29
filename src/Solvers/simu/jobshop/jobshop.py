import fileinput
import json
import os
import random


def Jobs(path=None):
    with fileinput.input(files=path) as f:
        next(f)
        jobs = [[(int(machine), int(time)) for machine, time in zip(*[iter(line.split())] * 2)]
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

    tj = [0] * j
    tm = [0] * m

    ij = [0] * j

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

def schedule_to_gantt_json(jobs, schedule, price, instance):
    colors = ["tomato", "orange", "green", "gold", "royalblue", "violet", "gray", "cyan", "pink", "lime",
              "chocolate", "bisque", "teal", "salmon", "navy", "dimgray", "orchid", "turquoise",
              "darkturquoise", "rosybrown", "steelblue", "moccasin", "blue", "blueviolet", "plum"]

    j = len(jobs)
    m = len(jobs[0])

    tj = [0] * j
    tm = [0] * m

    ij = [0] * j

    machine_schedule = []
    # Reformat to a table to be able to sort by machine

    for job in schedule:
        machine, time = jobs[job][ij[job]]
        ij[job] += 1
        start = max(tj[job], tm[machine])
        end = start + time
        tj[job] = end
        tm[machine] = end

        machine_schedule.append((machine, start, end, job))


    json_dict = {
        "packages": [],
        "title": f"Simulated Annealing {instance}  Cost: {price} Slurm: {os.environ['RUN_KEY']}",
        "xlabel": "time",
        "xticks": []
    }

    # Sort
    machine_schedule.sort(key=lambda x: x[-1])



    for slot in machine_schedule:
        bar = {}
        bar['label'] = "Machine " + str(slot[0])
        bar['start'] = slot[1]
        bar['end'] = slot[2]
        bar['color'] = colors[slot[-1]]
        bar["legend"] = "Job " + str(slot[-1] + 1)
        json_dict["packages"].append(bar)

    json_str = json.dumps(json_dict)
    with open(os.environ["OUTPUT_DIR"] + f"/json/{os.environ['RUN_KEY']}_gantt.json", "w") as fp:
        fp.write(json_str)


def lowerBound(jobs):
    def lower0():
        return max(sum(time for _, time in job) for job in jobs)

    def lower1():
        mtimes = [0] * numMachines(jobs)

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
