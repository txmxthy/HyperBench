import json
import os

import plotly.figure_factory as ff
import datetime
import numpy as np
import random


def generate_gantt_json(table, csv_columns):
    colors = ["tomato", "orange", "green", "gold", "royalblue", "violet", "gray", "cyan", "pink", "lime",
              "chocolate", "bisque", "teal", "salmon", "navy", "dimgray", "orchid", "turquoise",
              "darkturquoise", "rosybrown", "steelblue", "moccasin", "blue", "blueviolet", "plum"]
    # CSV Columns: instance, cost, seed, tabu_len, nsteps, hold, timeout,
    instance, cost = csv_columns
    json_dict = {
        "packages": [],
        "title": f"GA {instance}  Cost: {cost} Slurm: {os.environ['SLURM_ARRAY_TASK_ID']}",
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
    with open(os.environ["OUTPUT_DIR"] + f"/json/{os.environ['SLURM_ARRAY_TASK_ID']}_gantt.json", "w") as fp:
        fp.write(json_str)

def printTable(table):
    i = 1
    print("TABLE: ")
    for row in table:
        # Key: (start, end, job_id)
        print("M%s: %s" %(i, row))
        i += 1

# Replaced to export to json and render off grid (Loading chrome on grid is slow)
# def plotResult(table, maxValue):
#
#     # Dump the table to console
#
#     df = []
#     mn = 0
#     colors = []
#     for m in table:
#         mn += 1
#         m.sort(key=lambda x: x[2])
#         for slot in m:
#             start_time=str(datetime.timedelta(seconds=slot[0]))
#             end_time=str(datetime.timedelta(seconds=slot[1]))
#             today = datetime.date.today()
#             entry = dict(
#                 Task='Machine-{0}'.format(mn),
#                 Start="{0} {1}".format(today, start_time),
#                 Finish="{0} {1}".format(today, end_time),
#                 duration=slot[1] - slot[0],
#                 Resource='Job {0}'.format(slot[2] + 1)
#                 )
#             df.append(entry)
#
#             #Generate random colors
#             if(len(colors) < len(m)):
#                 a = min(255 - ( slot[2] * 10 ), 255)
#                 b = min(slot[2] * 10, 255)
#                 c = min(255, int(random.random() * 255))
#                 colors.append("rgb({0}, {1}, {2})".format(a, b, c))
#
#     #In order to see the line ordered by integers and not by dates we need to generate the dateticks manually
#     #we create 11 linespaced numbers between 0 and the maximum value
#     num_tick_labels = np.linspace(start = 0, stop = maxValue, num = 11, dtype = int)
#     date_ticks = ["{0} {1}".format(today, str(datetime.timedelta(seconds=int(x)))) for x in num_tick_labels]
#
#     fig = ff.create_gantt(df,colors=colors, index_col='Resource', group_tasks=True, show_colorbar=True, showgrid_x=True, title='Job shop Schedule')
#     fig.layout.xaxis.update({
#         'tickvals' : date_ticks,
#         'ticktext' : num_tick_labels
#         })
#     fig.show()
