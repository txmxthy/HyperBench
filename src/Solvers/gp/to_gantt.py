import json
import os


def generate_standardjss_gantt_json(table, csv_columns):
    colors = ["tomato", "orange", "green", "gold", "royalblue", "violet", "gray", "cyan", "pink", "lime",
              "chocolate", "bisque", "teal", "salmon", "navy", "dimgray", "orchid", "turquoise",
              "darkturquoise", "rosybrown", "steelblue", "moccasin", "blue", "blueviolet", "plum"]
    # CSV Columns: instance, cost, seed, tabu_len, nsteps, hold, timeout,
    instance, cost = csv_columns
    json_dict = {
        "packages": [],
        "title": f"GA {instance}  Cost: {cost} Slurm: {os.environ['RUN_KEY']}",
        "xlabel": "time",
        "xticks": []
    }
    mn = 0
    for m in table:
        mn += 1
        m.sort(key=lambda x: x[2])
        for slot in m:
            bar = {}
            bar['label'] = "Machine " + str(mn)
            bar['start'] = slot[0]
            bar['end'] = slot[1]
            bar['color'] = colors[slot[2]]
            bar["legend"] = "Job " + str(slot[2] + 1)
            # jobs_mark.append(s["job_id"]) # Old way of not trakcing jobs for labelling (reduce json size)
            json_dict["packages"].append(bar)
    json_str = json.dumps(json_dict)
    with open(os.environ["OUTPUT_DIR"] + f"/json/{os.environ['RUN_KEY']}_gantt.json", "w") as fp:
        fp.write(json_str)


def generate_flexible_gantt_json(filepath):
    """
    Gantt chart json format for parsing flexible output
    Job 7, arrives at 0.0, due at 0.0, weight is 1.0. It has 10 operations:
    [J7 O0-0, W4, T20.0]
    [J7 O1-0, W6, T86.0], [J7 O1-1, W2, T86.0]
    [J7 O2-0, W5, T21.0]
    [J7 O3-0, W8, T79.0]
    [J7 O4-0, W9, T62.0]
    [J7 O5-0, W2, T34.0]
    [J7 O6-0, W0, T27.0]
    [J7 O7-0, W1, T81.0]
    [J7 O8-0, W7, T30.0]
    [J7 O9-0, W3, T46.0]

    Job 2, arrives at 0.0, due at 0.0, weight is 1.0. It has 10 operations:
    [J2 O0-0, W1, T45.0]
    [J2 O1-0, W7, T46.0], [J2 O1-1, W9, T46.0]
    [J2 O2-0, W6, T22.0]
    [J2 O3-0, W2, T26.0]
    [J2 O4-0, W9, T38.0]
    [J2 O5-0, W0, T69.0]
    [J2 O6-0, W4, T40.0]
    [J2 O7-0, W3, T33.0]
    [J2 O8-0, W8, T75.0], [J2 O8-1, W3, T75.0]
    [J2 O9-0, W5, T96.0]
    """
    with open(filepath, "r") as f:
        lines = f.readlines()
    jobs = {}
    for line in lines:
        if line.startswith("Job"):
            comps = line.split(",")
            print(comps)
            job_name = comps[0]
            job_id = int(job_name.split(" ")[1])

            arrives = float(comps[1].split("at ")[1])
            due = float(comps[2].split("at ")[1])
            tmp = comps[3].split(". It has ")
            weight = float(tmp[0].split("weight is ")[1])
            nops = int(tmp[1].split(" operations:")[0])

            # print(f"job_id: {job_id}, due: {due}, weight: {weight}, nOps: {nops}")
            # Init key
            jobs[job_name] = {"id": job_id, "due": due, "weight": weight, "nOps": nops, "ops": {}}



        elif line.startswith("["):
            # Operations
            # - A single op has len 4 on a line
            comps = line.split(" ")
            print(comps)
            # nOptions = len(comps)//4
            # opts = {}
            # for option in range(0, nOptions):
            #     job_id =

            jobid = comps[0].split("[J")[1]
            op_opt = comps[1].split("-")
            op_id = op_opt[0]
            opt_id = op_opt[1].split(",")[0]
            workcenter = comps[2].split("W")[1].split(",")[0]






if __name__ == "__main__":
    generate_flexible_gantt_json("D:\\Projects\\Capstone\\Code\\src\\Solvers\\gp\\schedules\\1060.0.txt")
