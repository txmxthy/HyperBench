import csv
import os
import time
import random
import copy
import json
import matplotlib.pyplot as plt
import pandas as pd


class Job:

    def __init__(self, job_constraint, job_id, machines):  # 初始化一个Job模板
        self.id = job_id  # 本job的id
        self.order = []  # 记录本job要求的machine先后顺序
        self.handle_time = []  # 记录本job在各个machine需要执行的时间
        # import pdb; pdb.set_trace()
        for i in range(len(job_constraint) // 2):
            self.order.append(machines[job_constraint[i * 2]])
            self.handle_time.append(job_constraint[i * 2 + 1])
        self.current_operation = 0  # 记录本job当前正在等待完工的操作号
        self.current_duration = self.handle_time[0]  # 记录本job当前正在等待执行的操作需要的时间
        self.isDone = False  # 记录本job是否执行完了所有的操作

    def reset_job(self, job_constraint, machines):  # 设置Job属性
        self.current_operation = 0  # 记录本job当前正在等待完工的操作号
        self.current_duration = self.handle_time[0]  # 记录本job当前正在等待执行的操作需要的时间
        self.isDone = False  # 记录本job是否执行完了所有的操作

    def goto_next_machine(self, current_time):  # job去其下一个操作所对应的机器中等待，返回该机器对象。如果所有工序已经执行完毕则将isDone置为True返回None
        if self.current_operation == len(self.order) - 1:
            self.isDone = True
            return None
        else:
            self.current_operation = self.current_operation + 1
            self.current_duration = self.handle_time[self.current_operation]
            self.order[self.current_operation].wait_queue.append(self)  # 将本job投入到下一个machine的队列中，如果该machine处于关闭状态则将其启动。
            if not self.order[self.current_operation].running:  # 启动机器
                self.order[self.current_operation].turn_on_machine(current_time)
            return self.order[self.current_operation]


class Machine:

    def __init__(self, priority: [int], machine_id):
        self.id = machine_id  # 本机器的id
        self.priority = priority  # 处理优先级
        self.wait_queue = []  # 等待处理的job队列
        self.running = False  # 机器是否正在运行
        self.current_job = None  # 正在操作的job对象
        self.finish_time = 0  # 完工时间点，也即machine下一次空闲的时间点
        self.schedule_table = []  # 本机器的调度表-结构：[{"job_id":*, "start":*, "end":*}, {...}, {...}]

    def reset_machine(self, priority: [int]):
        self.priority = priority  # 处理优先级
        self.wait_queue = []  # 等待处理的job队列
        self.running = False  # 机器是否正在运行
        self.current_job = None  # 正在操作的job对象
        self.finish_time = 0  # 完工时间点，也即machine下一次空闲的时间点

    def goto_next_job(self, current_time):  # 完成正在加工的job，从已有job队列中拿出优先级最高的job进行处理，并更新完工时间点,返回本次处理完的job对象。如果队列为空则关闭机器
        finish_job = self.current_job  # 完成正在加工的job
        # import pdb; pdb.set_trace()
        self.wait_queue.remove(finish_job)  # 将该job移除
        # 将本job的调度放入调度表
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

    def turn_on_machine(self, current_time):  # 启动机器, 启动成功返回True，失败返回False
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


# 数据结构-JSP问题对象
class JSPAns:

    def __init__(self, m, n, jobs_map: [[int]],
                 ans_map: [[int]]):  # 针对一个m个machines，n个jobs的JSP问题，随机初始化一个解,jobs_map为jobs要求的执行顺序
        '''
        解的形式：
        [[0,1,2],[2,1,0],[1,0,2],...] map[m][n]表示m机器处理njob的优先级,值越高表示越越优先
        '''
        # 问题输入
        self.machine_num = m
        self.job_num = n
        self.jobs = []
        self.machines = []
        self.current_time = 0  # 初始时间点为0
        self.ans_map = ans_map
        self.ans_value = -1
        '''
        # 初始化一个随机解,并以此初始化m个machine对象
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
        # 生成m个machine
        for x in ans_map:
            machine = Machine(x, len(self.machines))
            self.machines.append(machine)
        # 生成n个job对象
        for constraint in jobs_map:
            job = Job(constraint, len(self.jobs), self.machines)
            self.jobs.append(job)
        # 初始化machine的wait队列以及一些状态
        for job in self.jobs:
            job.order[0].wait_queue.append(job)
        for machine in self.machines:
            machine.turn_on_machine(self.current_time)
        # 求解适值
        self.ans_value = self.calculate_end_time()
        '''
        # 初始化当前解的适值，已知的最优解，最优解的适值
        self.current_ans_value = self.calculate_end_time()
        self.best_ans = self.current_ans
        self.best_ans_value = self.current_ans_value
        '''
        # 甘特图可选颜色
        self.colors = ["tomato", "orange", "green", "gold", "royalblue", "violet", "gray", "cyan", "pink", "lime",
                       "chocolate", "bisque", "teal", "salmon", "navy", "dimgray", "orchid", "turquoise",
                       "darkturquoise", "rosybrown", "steelbule", "moccasin", "blue", "buleviolet", "plum"]

    def machine_on_running(self):  # 以列表的形式返回当前正在运行的机器
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
                first_machine = running_machines[0]  # 最早完工的机器
                for machine in running_machines:
                    if machine.finish_time < first_machine.finish_time:
                        first_machine = machine
                self.current_time = first_machine.finish_time  # 将当前时间更新为最早完工时间
                finish_job = first_machine.goto_next_job(self.current_time)  # 机器推进到下一个job
                finish_job.goto_next_machine(self.current_time)  # 刚完工的job推进到下一个机器
            else:
                break
        return self.current_time

    def generate_gantt_json(self):
        json_dict = {
            "packages": [],
            "title": "GANTT",
            "xlabel": "time",
            "xticks": []
        }
        jobs_mark = []
        for m in self.machines:
            for s in m.schedule_table:
                bar = {}
                bar['label'] = "Machine " + str(m.id)
                bar['start'] = s["start"]
                bar['end'] = s["end"]
                bar['color'] = self.colors[s["job_id"]]
                if s["job_id"] not in jobs_mark:
                    bar["legend"] = "Job " + str(s["job_id"])
                    jobs_mark.append(s["job_id"])
                json_dict["packages"].append(bar)
        json_str = json.dumps(json_dict)
        with open("./ganttBar.json", "w") as fp:
            fp.write(json_str)


# 禁忌搜索工具包
class TabuSearch:

    def __init__(self, jobs_map, tabu_len, tabu_obj="machine-job-job"):  # 传入禁忌表长度，禁忌对象，问题模型，初始化禁忌表
        self.tabu_list = ["" for _ in range(tabu_len)]
        self.jobs_map = jobs_map  # 问题模型
        self.best_ans = None  # 目前找到的最优
        self.tabu_obj = tabu_obj

    def __tabu_object(self, machine_id, job1_id, job2_id):  # 返回禁忌对象字符串
        if self.tabu_obj == "machine":  # 禁忌机器
            return [str(machine_id)]
        elif self.tabu_obj == "job":  # 禁忌工件
            return str(job1_id), str(job2_id)
        elif self.tabu_obj == "machine-job":  # 禁忌机器-工件二元组
            return str(machine_id) + "-" + str(job1_id), str(machine_id) + "-" + str(job2_id)
        else:  # 禁忌机器-工件1-工件2三元组
            return str(machine_id) + "-" + str(job1_id) + "-" + str(job2_id), str(machine_id) + "-" + str(
                job2_id) + "-" + str(job1_id)

    def update_tabu(self, machine_id, job1_id, job2_id):  # 更新禁忌表内容
        tabu_obj = self.__tabu_object(machine_id, job1_id, job2_id)
        for obj in tabu_obj:
            self.tabu_list.pop(0)
            self.tabu_list.append(obj)

    def check_tabu(self, machine_id, job1_id, job2_id):  # 检查某个搜索所到的邻居是否被禁忌
        tabu_obj = self.__tabu_object(machine_id, job1_id, job2_id)
        for obj in tabu_obj:
            if obj in self.tabu_list: return False  # 如果本次搜索的方向在禁忌表中，返回False
        return True  # 不在禁忌表中，返回True，说明该邻居不被禁忌

    def jsp_random_initial_ans(self, machine_num, job_num) -> [
        [int]]:  # 返回JSP问题的大小为machine_num*job_num的一个随机解，返回一个JSPAns对象
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

    def jsp_neighbor_generator(self, current_ans_map: [[int]], m, n):  # 返回一个邻居生成器
        # 每次随机选一个机器交换两个工件的顺序。返回这个解同时返回，本次搜的方向（machine_id，Job1.id, Job2.id）
        while True:
            neighbor = copy.deepcopy(current_ans_map)
            random.seed(time.time())
            machine_id = random.randint(0, m - 1)
            job1_id, job2_id = tuple(random.sample(range(n), 2))
            neighbor[machine_id][job1_id], neighbor[machine_id][job2_id] = neighbor[machine_id][job2_id], \
                                                                           neighbor[machine_id][job1_id]
            yield neighbor, machine_id, job1_id, job2_id

    def jsp_update_ans(self, current_ans, m, n, k):  # current_ans是JSPAns对象，从当前解中找k个邻居更新当前解，返回更新后的当前解对象
        ng = self.jsp_neighbor_generator(current_ans.ans_map, m, n)
        neighbor_best_tabu = None  # 邻居中被禁的最优解
        nbt_mid = nbt_j1id = nbt_j2id = -1
        neighbor_best_no_tabu = None  # 邻居中没被禁的最优解
        nbnt_mid = nbnt_j1id = nbnt_j2id = -1
        neighbor_worst_tabu = None  # 邻居中被禁的最差解
        nwt_mid = nwt_j1id = nwt_j2id = -1
        count = 0
        for neighbor, machine_id, job1_id, job2_id in ng:
            new_ans = JSPAns(m, n, self.jobs_map, neighbor)
            if self.check_tabu(machine_id, job1_id, job2_id):  # 不在禁忌表中
                # print("neighbor", count, " not in tabu", "with value", new_ans.ans_value)
                if neighbor_best_no_tabu:
                    if neighbor_best_no_tabu.ans_value > new_ans.ans_value:
                        neighbor_best_no_tabu = new_ans
                        nbnt_mid, nbnt_j1id, nbnt_j2id = machine_id, job1_id, job2_id
                else:
                    neighbor_best_no_tabu = new_ans
                    nbnt_mid, nbnt_j1id, nbnt_j2id = machine_id, job1_id, job2_id
            else:  # 在禁忌表中
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
        update_ans = None  # 更新后的解
        if not neighbor_best_no_tabu:  # 如果没有不被禁的解，则所有邻居都被禁了
            if neighbor_best_tabu.ans_value < self.best_ans.ans_value:
                update_ans = neighbor_best_tabu
                machine_id, job1_id, job2_id = nbt_mid, nbt_j1id, nbt_j2id
                # print("update to tabu_best neighbor")
            else:
                update_ans = neighbor_worst_tabu
                machine_id, job1_id, job2_id = nwt_mid, nwt_j1id, nwt_j2id
                # print("update to tabu_worst neighbor")
        elif not neighbor_best_tabu:  # 如果没有被禁的解，则所有邻居都允许
            update_ans = neighbor_best_no_tabu
            machine_id, job1_id, job2_id = nbnt_mid, nbnt_j1id, nbnt_j2id
            # print("update to not_tabu_best neighbor")
        elif neighbor_best_no_tabu.ans_value > neighbor_best_tabu.ans_value:  # 如果既有被禁的也有不被禁的解且被禁的解是所有邻居中最优
            if neighbor_best_tabu.ans_value < self.best_ans.ans_value:
                update_ans = neighbor_best_tabu
                machine_id, job1_id, job2_id = nbt_mid, nbt_j1id, nbt_j2id
                # print("update to tabu_best neighbor")
            else:
                update_ans = neighbor_best_no_tabu
                machine_id, job1_id, job2_id = nbnt_mid, nbnt_j1id, nbnt_j2id
                # print("update to not_tabu_best neighbor")
        else:  # 不被禁的最优解是所有邻居中的最优，则选择此解
            update_ans = neighbor_best_no_tabu
            machine_id, job1_id, job2_id = nbnt_mid, nbnt_j1id, nbnt_j2id
            # print("update to not_tabu_best neighbor")
        # 更新目前最好的解以及tabu表
        if update_ans.ans_value < self.best_ans.ans_value:
            print("New Best Found:", update_ans.ans_value)
            self.best_ans = update_ans
        self.update_tabu(machine_id, job1_id, job2_id)
        return update_ans  # 返回更新后的解


if __name__ == "__main__":
    # get the full path of the directory "instance:
    files = (os.listdir(os.getcwd() + "/instances"))
    maxTime = float(input("Input the max time in seconds for each instance:"))

    scores = {}
    for file in files:
        print("file:", file)
        jobs_map = []
        with open(os.getcwd() + "/instances/" + file, "r") as f:
            n, m = tuple([int(x) for x in f.readline().split()])  # n是job数，m是machine数
            for line in f:
                jobs_map.append([int(x) for x in line.split()])
            print(m, n)
            print(jobs_map)
        ts = TabuSearch(jobs_map, 100)
        current_ans = ts.jsp_random_initial_ans(m, n)
        total_steps = 1000  # 最大迭代次数
        neighbor_num = m * n
        longest_hold = 1000  # longest_hold后未发现更优的，则退出迭代
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
        scores[file] = ts.best_ans.ans_value
        ts.best_ans.generate_gantt_json()  # 获取绘制甘特图的json文件
        plt.plot(best_value_record[:-longest_hold + 50])  # 绘制搜索的过程
        plt.show()
        # Close the file
        f.close()
    print(scores)
    csv_columns = files


    csv_file = "scores.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(scores)
    except IOError:
        print("I/O error")