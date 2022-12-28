import csv
import os
import time
import random
import copy
import json
from pprint import pprint

import numpy as np
import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
import plotly as py
import plotly.figure_factory as ff
from pandas import DataFrame


class Job:

    def __init__(self, job_constraint, job_id, machines):  # Initialize a Job template
        self.id = job_id  # The id of this job
        self.order = []  # Record the sequence of machines required by this job
        self.handle_time = []  # Record the time this job needs to execute in each machine
        # import pdb; pdb.set_trace()
        for i in range(len(job_constraint) // 2):
            self.order.append(machines[job_constraint[i * 2]])
            self.handle_time.append(job_constraint[i * 2 + 1])
        self.current_operation = 0  # Record the number of the job that is currently waiting to be completed
        self.current_duration = self.handle_time[
            0]  # Record the time required for the operation that this job is currently waiting to execute
        self.isDone = False  # Record whether the job has completed all operations

    def reset_job(self, job_constraint, machines):  # Set Job properties
        self.current_operation = 0  # Record the number of the job that is currently waiting to be completed
        self.current_duration = self.handle_time[
            0]  # Record the time required for the operation that this job is currently waiting to execute
        self.isDone = False  # Record whether the job has completed all operations

    def goto_next_machine(self,
                          current_time):  # The job waits in the machine corresponding to its next operation, and returns the machine object. If all processes have been executed, set is Done to True and return None
        if self.current_operation == len(self.order) - 1:
            self.isDone = True
            return None
        else:
            self.current_operation = self.current_operation + 1
            self.current_duration = self.handle_time[self.current_operation]
            self.order[self.current_operation].wait_queue.append(
                self)  # Put this job into the queue of the next machine, and start it if the machine is shut down.
            if not self.order[self.current_operation].running:  # start the machine
                self.order[self.current_operation].turn_on_machine(current_time)
            return self.order[self.current_operation]


class Machine:

    def __init__(self, priority: [int], machine_id):
        self.id = machine_id  # id of this machine
        self.priority = priority  # processing priority
        self.wait_queue = []  # queue of jobs waiting to be processed
        self.running = False  # is the machine running
        self.current_job = None  # The job object being operated on
        self.finish_time = 0  # Completion time point, that is, the time point when the machine is next idle
        self.schedule_table = []  # Schedule table for this machine - structure: [{"job_id":, "start":, "end":}, {...}, {...}]

    def reset_machine(self, priority: [int]):
        self.priority = priority  # processing priority
        self.wait_queue = []  # queue of jobs waiting to be processed
        self.running = False  # Is the machine running
        self.current_job = None  # The job object being operated on
        self.finish_time = 0  # Completion time point, that is, the time point when the machine is next idle

    def goto_next_job(self,
                      current_time):  # Complete the job being processed, take the job with the highest priority from the existing job queue for processing, update the completion time point, and return the job object that has been processed this time. shut down the machine if the queue is empty
        finish_job = self.current_job  # Complete the job being processed
        # import pdb; pdb.set_trace()
        self.wait_queue.remove(finish_job)  # remove the job
        # Put the scheduling of this job into the scheduling table
        schedule = {"job_id": finish_job.id, "start": self.finish_time - finish_job.current_duration,
                    "end": self.finish_time}
        self.schedule_table.append(schedule)
        if not self.wait_queue:
            self.running = False
        else:
            self.current_job = self.wait_queue[0]
            for job in self.wait_queue:
                if self.priority[self.current_job.id] < self.priority[job.id]:
                    self.current_job = job
            # import pdb; pdb.set_trace()
            self.finish_time = current_time + self.current_job.current_duration
        return finish_job

    def turn_on_machine(self,
                        current_time):  # Start the machine, return True if the startup is successful, and return False if it fails
        if not self.wait_queue:
            self.running = False
        else:
            self.running = True
            self.current_job = self.wait_queue[0]
            for job in self.wait_queue:
                if self.priority[self.current_job.id] < self.priority[job.id]:
                    self.current_job = job
            self.finish_time = current_time + self.current_job.current_duration
        return self.running


# Data Structure - JSP Question Object
class JSPAns:

    def __init__(self, m, n, jobs_map: [[int]],
                 ans_map: [[
                     int]]):  # For a JSP problem with m machines and n jobs, randomly initialize a solution, and the jobs map is the execution order required by the jobs
        '''
      The solution is of the form:
        [[0,1,2],[2,1,0],[1,0,2],...] map[m][n] indicates the priority of m machine processing njob, the higher the value, the better higher priority
        '''
        # question input
        self.machine_num = m
        self.job_num = n
        self.jobs = []
        self.machines = []
        self.current_time = 0  # The initial time point is 0
        self.ans_map = ans_map
        self.ans_value = -1
        '''
        # Initialize a random solution, and use it to initialize m machine objects
        # random.seed(time.time())
        x = list(range(n))
        self.current_ans = []
        for i in range(m):
            # import pdb; pdb.set_trace()
            random.shuffle(x)
            self.current_ans.append(x[:])
            machine = Machine(x[:], i)
            self.machines.append(machine)
        '''
        # Generate m machines
        for x in ans_map:
            machine = Machine(x, len(self.machines))
            self.machines.append(machine)
        # Generate n job objects
        for constraint in jobs_map:
            job = Job(constraint, len(self.jobs), self.machines)
            self.jobs.append(job)
        # Initialize the machine's wait queue and some states
        for job in self.jobs:
            job.order[0].wait_queue.append(job)
        for machine in self.machines:
            machine.turn_on_machine(self.current_time)
        # Find the fitness value
        self.ans_value = self.calculate_end_time()
        '''
        # Initialize the fitness value of the current solution, the known optimal solution, and the fitness value of the optimal solution
        self.current_ans_value = self.calculate_end_time()
        self.best_ans = self.current_ans
        self.best_ans_value = self.current_ans_value
        '''
        # Gantt chart optional colors
        self.colors = ["tomato", "orange", "green", "gold", "royalblue", "violet", "gray", "cyan", "pink", "lime",
                       "chocolate", "bisque", "teal", "salmon", "navy", "dimgray", "orchid", "turquoise",
                       "darkturquoise", "rosybrown", "steelblue", "moccasin", "blue", "blueviolet", "plum"]

    def machine_on_running(self):  # Returns the currently running machines as a list
        running_machines = []
        for machine in self.machines:
            if machine.running:
                running_machines.append(machine)
        return running_machines

    def calculate_end_time(self):
        while True:
            running_machines = self.machine_on_running()
            # import pdb; pdb.set_trace()
            if running_machines:
                first_machine = running_machines[0]  # FIRST COMPLETED MACHINE
                for machine in running_machines:
                    if machine.finish_time < first_machine.finish_time:
                        first_machine = machine
                self.current_time = first_machine.finish_time  # Update current time to earliest finish time
                finish_job = first_machine.goto_next_job(self.current_time)  # The machine advances to the next job
                finish_job.goto_next_machine(
                    self.current_time)  # The job just completed is advanced to the next machine
            else:
                break
        return self.current_time

    def generate_gantt_json(self, csv_columns):
        # CSV Columns: instance, cost, seed, tabu_len, nsteps, hold, timeout,
        instance, cost, seed, tabu_len, nsteps, hold, timeout = csv_columns
        json_dict = {
            "packages": [],
            "title": f"{instance}  Cost: {cost} Slurm: {os.environ['SLURM_ARRAY_TASK_ID']}",
            "xlabel": "time",
            "xticks": []
        }
        # jobs_mark = []
        for m in self.machines:
            for s in m.schedule_table:
                bar = {}
                bar['label'] = "Machine " + str(m.id)
                bar['start'] = s["start"]
                bar['end'] = s["end"]
                bar['color'] = self.colors[s["job_id"]]
                bar["legend"] = "Job " + str(s["job_id"])
                # jobs_mark.append(s["job_id"]) # Old way of not trakcing jobs for labelling (reduce json size)
                json_dict["packages"].append(bar)
        json_str = json.dumps(json_dict)
        with open(os.environ["OUTPUT_DIR"] + f"/json/{instance}_gantt.json", "w") as fp:
            fp.write(json_str)


# Taboo Search Toolkit
class TabuSearch:

    def __init__(self, jobs_map, tabu_len,
                 tabu_obj="machine-job-job"):  # Pass in the taboo table length, taboo object, problem model, and initialize the taboo table
        self.tabu_list = ["" for _ in range(tabu_len)]
        self.jobs_map = jobs_map  # problemModel
        self.best_ans = None  # The best found so far
        self.tabu_obj = tabu_obj

    def __tabu_object(self, machine_id, job1_id, job2_id):  # Returns the taboo object string
        if self.tabu_obj == "machine":  # TABOO MACHINE
            return [str(machine_id)]
        elif self.tabu_obj == "job":  # Taboo artifact
            return str(job1_id), str(job2_id)
        elif self.tabu_obj == "machine-job":  # Forbidden Machine-Workpiece Binary
            return str(machine_id) + "-" + str(job1_id), str(machine_id) + "-" + str(job2_id)
        else:  # Forbidden Machine-Artifact 1-Artifact 2 triplet
            return str(machine_id) + "-" + str(job1_id) + "-" + str(job2_id), str(machine_id) + "-" + str(
                job2_id) + "-" + str(job1_id)

    def update_tabu(self, machine_id, job1_id, job2_id):  # Update Taboo Table Contents
        tabu_obj = self.__tabu_object(machine_id, job1_id, job2_id)
        for obj in tabu_obj:
            self.tabu_list.pop(0)
            self.tabu_list.append(obj)

    def check_tabu(self, machine_id, job1_id, job2_id):  # Checks if a searched neighbor is taboo
        tabu_obj = self.__tabu_object(machine_id, job1_id, job2_id)
        for obj in tabu_obj:
            if obj in self.tabu_list: return False  # If the direction of this search is in the taboo table, return False
        return True  # Not in the taboo table, return True, indicating that the neighbor is not taboo

    def jsp_random_initial_ans(self, machine_num, job_num) -> [
        [
            int]]:  # Returns a random solution of the JSP problem whose size is machine numjob num, returns a JSP Ans object
        ans_map = []
        random.seed(time.time())
        x = list(range(job_num))
        for _ in range(machine_num):
            random.shuffle(x)
            ans_map.append(x[:])
        self.m = machine_num
        self.n = job_num
        initial_ans = JSPAns(self.m, self.n, self.jobs_map, ans_map)
        self.best_ans = initial_ans
        return initial_ans

    def jsp_neighbor_generator(self, current_ans_map: [[int]], m, n):  # returns a neighbor generator
        # Each time a machine is randomly selected to exchange the order of the two workpieces. Return this solution and return the direction of this search (machine_id, Job1.id, Job2.id)
        while True:
            neighbor = copy.deepcopy(current_ans_map)
            random.seed(time.time())
            machine_id = random.randint(0, m - 1)
            job1_id, job2_id = tuple(random.sample(range(n), 2))
            neighbor[machine_id][job1_id], neighbor[machine_id][job2_id] = neighbor[machine_id][job2_id], \
                                                                           neighbor[machine_id][job1_id]
            yield neighbor, machine_id, job1_id, job2_id

    def jsp_update_ans(self, current_ans, m, n,
                       k):  # current ans is a JSP Ans object, find k neighbors from the current solution to update the current solution, and return the updated current solution object
        ng = self.jsp_neighbor_generator(current_ans.ans_map, m, n)
        neighbor_best_tabu = None  # Optimal solution banned in neighbors
        nbt_mid = nbt_j1id = nbt_j2id = -1
        neighbor_best_no_tabu = None  # The optimal solution that is not banned in the neighborhood
        nbnt_mid = nbnt_j1id = nbnt_j2id = -1
        neighbor_worst_tabu = None  # worstSolutionBannedInNeighborhood
        nwt_mid = nwt_j1id = nwt_j2id = -1
        count = 0
        for neighbor, machine_id, job1_id, job2_id in ng:
            new_ans = JSPAns(m, n, self.jobs_map, neighbor)
            if self.check_tabu(machine_id, job1_id, job2_id):  # NOT IN TABOO LIST
                # print("neighbor", count, " not in tabu", "with value", new_ans.ans_value)
                if neighbor_best_no_tabu:
                    if neighbor_best_no_tabu.ans_value > new_ans.ans_value:
                        neighbor_best_no_tabu = new_ans
                        nbnt_mid, nbnt_j1id, nbnt_j2id = machine_id, job1_id, job2_id
                else:
                    neighbor_best_no_tabu = new_ans
                    nbnt_mid, nbnt_j1id, nbnt_j2id = machine_id, job1_id, job2_id
            else:  # IN TABOO LIST
                # print("neighbor", count, "in tabu", "with value", new_ans.ans_value)
                if neighbor_best_tabu:
                    if neighbor_best_tabu.ans_value > new_ans.ans_value:
                        neighbor_best_tabu = new_ans
                        nbt_mid, nbt_j1id, nbt_j2id = machine_id, job1_id, job2_id
                else:
                    neighbor_best_tabu = new_ans
                    nbt_mid, nbt_j1id, nbt_j2id = machine_id, job1_id, job2_id
                if neighbor_worst_tabu:
                    if neighbor_worst_tabu.ans_value < new_ans.ans_value:
                        neighbor_worst_tabu = new_ans
                        nwt_mid, nwt_j1id, nwt_j2id = machine_id, job1_id, job2_id
                else:
                    neighbor_worst_tabu = new_ans
                    nwt_mid, nwt_j1id, nwt_j2id = machine_id, job1_id, job2_id
            count = count + 1
            if count == k: break
        update_ans = None  # updatedSolution
        if not neighbor_best_no_tabu:  # If there is no unbanned solution, all neighbors are banned
            if neighbor_best_tabu.ans_value < self.best_ans.ans_value:
                update_ans = neighbor_best_tabu
                machine_id, job1_id, job2_id = nbt_mid, nbt_j1id, nbt_j2id
                # print("update to tabu_best neighbor")
            else:
                update_ans = neighbor_worst_tabu
                machine_id, job1_id, job2_id = nwt_mid, nwt_j1id, nwt_j2id
                # print("update to tabu_worst neighbor")
        elif not neighbor_best_tabu:  # If there are no forbidden solutions, all neighbors are allowed
            update_ans = neighbor_best_no_tabu
            machine_id, job1_id, job2_id = nbnt_mid, nbnt_j1id, nbnt_j2id
            # print("update to not_tabu_best neighbor")
        elif neighbor_best_no_tabu.ans_value > neighbor_best_tabu.ans_value:  # If there are both forbidden and non-banned solutions and the forbidden solution is the best among all neighbors
            if neighbor_best_tabu.ans_value < self.best_ans.ans_value:
                update_ans = neighbor_best_tabu
                machine_id, job1_id, job2_id = nbt_mid, nbt_j1id, nbt_j2id
                # print("update to tabu_best neighbor")
            else:
                update_ans = neighbor_best_no_tabu
                machine_id, job1_id, job2_id = nbnt_mid, nbnt_j1id, nbnt_j2id
                # print("update to not_tabu_best neighbor")
        else:  # The optimal solution that is not forbidden is the optimal solution among all neighbors, then choose this solution
            update_ans = neighbor_best_no_tabu
            machine_id, job1_id, job2_id = nbnt_mid, nbnt_j1id, nbnt_j2id
            # print("update to not_tabu_best neighbor")
        # Update the current best solution and tabu table
        if update_ans.ans_value < self.best_ans.ans_value:
            print("New Best Found:", update_ans.ans_value)
            self.best_ans = update_ans
        self.update_tabu(machine_id, job1_id, job2_id)
        return update_ans  # RETURNS THE UPDATED SOLUTION


def tabu_main(seed=None, tabu_len=None, nsteps=None, hold=None, timeout=None, instance=None):
    if seed is None:
        seed = int(input("seed: ") or 0)

        # Set the seed
    random.seed(seed)
    np.random.seed(seed)

    if tabu_len is None:
        tabu_len = int(input("len: ") or 3)
    if nsteps is None:
        nsteps = float(input("steps: ") or 500)

    if hold is None:
        hold = int(input("hold: ") or 100)

    if timeout is None:
        timeout = int(input("timeout: ") or 20)

    if instance is None:
        instance = str(input("instance: ") or "abz5")

    # @todo CURRENT SPOT: WORK ON THIS: loading in the instance and settings :)
    # get the full path of the directory "instance:
    instance_prefix = os.getcwd() + "/instances/"
    file = instance
    maxTime = float(timeout)

    print("file:", file)
    jobs_map = []
    with open(instance_prefix + file, "r") as f:
        n, m = tuple([int(x) for x in f.readline().split()])  # n is the number of jobs, m is the number of machines
        for line in f:
            jobs_map.append([int(x) for x in line.split()])
        print(m, n)
        print(jobs_map)

    ts = TabuSearch(jobs_map, 100)
    current_ans = ts.jsp_random_initial_ans(m, n)
    total_steps = 1000  # The maximum number of iterations
    neighbor_num = m * n
    longest_hold = 1000  # If no better one is found after the longest hold, exit the iteration
    hold_cnt = 0
    last_best = 0
    best_value_record = []
    t0 = time.time()
    for i in range(total_steps):

        # print("-----------------------------", "step", i, "-----------------------------")
        current_ans = ts.jsp_update_ans(current_ans, m, n, neighbor_num)
        # print("current value:", current_ans.ans_value)
        # print("best in history:", ts.best_ans.ans_value)
        if last_best == ts.best_ans.ans_value:
            hold_cnt += 1
        else:
            hold_cnt = 0
        last_best = ts.best_ans.ans_value
        best_value_record.append(last_best)
        if hold_cnt == longest_hold:
            break

        if maxTime and time.time() - t0 > maxTime:
            print("Time out!")
            break

    print("tabu_list:", ts.tabu_list)
    print("best_ans:", ts.best_ans.ans_value)
    cost = ts.best_ans.ans_value

    csv_columns = instance, cost, seed, tabu_len, nsteps, hold, timeout
    ts.best_ans.generate_gantt_json(csv_columns)  # Get the json file for drawing the Gantt chart
    plt.plot(best_value_record[:-longest_hold + 50])  # Mapping the search process
    plt.title(f"Tabu Search Convergence (Slurm: {os.environ['SLURM_ARRAY_TASK_ID']})")
    plt.savefig(f"{os.environ['OUTPUT_DIR']}/img/convergence-{os.environ['SLURM_ARRAY_TASK_ID']}.png")
    # Close the file
    f.close()



    csv_file = f"{os.environ['OUTPUT_DIR']}/results-{os.environ['SLURM_ARRAY_TASK_ID']}.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            # for data in csv_columns:
            #     writer.writerow(data)

    except IOError:
        print("I/O error")

    render_gantt_json(instance)


def render_gantt_json(instance):
    file = os.environ["OUTPUT_DIR"] + f"/json/{os.environ['SLURM_ARRAY_TASK_ID']}_gantt.json"
    with open(file, "r") as f:
        gantt_data = json.load(f)

    list_of_dicts = []
    for job in gantt_data["packages"]:
        d = {"Machine": job["label"],
             "Start": job["start"],
             "End": job["end"],
             "Color": job["color"],
             "Job": job["legend"]}

        list_of_dicts.append(d)

    df = pd.DataFrame(list_of_dicts)
    df['Delta'] = df['End'] - df['Start']

    fig = px.timeline(df, x_start="Start", x_end="End", y="Machine", color="Color", labels="Job",
                      title=gantt_data["title"])
    fig.update_yaxes(autorange="reversed")
    fig.layout.xaxis.type = 'linear'
    for d in fig.data:
        filt = df['Color'] == d.name
        d.name = str(df[filt]['Job'].values[0])
        d.x = df[filt]['Delta'].tolist()

    fig.update_xaxes(type='linear')
    fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
    fig.write_image(os.environ["OUTPUT_DIR"] + "/img/gantt-" + os.environ['SLURM_ARRAY_TASK_ID'] + ".png")


if __name__ == "__main__":
    tabu_main()
