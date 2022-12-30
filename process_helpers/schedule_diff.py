import glob
import json
import os
import time

import pandas as pd
from PIL import Image

from process_helpers.utilities.plotting import render_gantt_json

DEBUG = False


def rprint(text, depth, alert=False):
    if not DEBUG:
        return
    prefix = " " * depth
    if alert:
        print(f"{'!' * depth}")
        print(f"{text}")
        print(f"{'!' * depth}")

    else:
        print(f"{prefix}{text}")


def check_json(jsondir, schedule_ids, n=0):
    """
    Pass in a list of schedule ids and return a list of unique schedules from that list
    """
    return check_nth_job(jsondir, schedule_ids, n)

    # If the times are different then they are not the same schedule,


def check_nth_job(jsondir, schedule_ids, n=0):
    unique = []
    duplicate = []

    nth_job_end = {}
    for schedule_id in schedule_ids:
        json_path = jsondir + str(schedule_id) + "_gantt.json"
        with open(json_path, 'r') as f:
            json_data = json.load(f)
            # add to dict with key if key exist else create
            if json_data["packages"][n]["end"] not in nth_job_end:
                nth_job_end[json_data["packages"][n]["end"]] = []
            nth_job_end[json_data["packages"][n]["end"]].append(schedule_id)

    for end_time in nth_job_end:
        # If multiple end at the same time they could still be the same

        if len(nth_job_end[end_time]) == 1:
            # print(f"Found unique schedule {nth_job_endtime[key]}")
            # This is a unique schedule

            schedule = nth_job_end[end_time][0]
            unique.append(schedule)
            # print(f"{schedule} cleared in {n + 1} checks.")

        elif len(nth_job_end[end_time]) > 1:
            # Check if the next node is in bounds of json_data["packages"]
            # If it is then check the end time of that node
            length = len(json_data["packages"])

            if n + 1 < length:

                rprint(f"duplicate end time ({end_time}) found: {nth_job_end[end_time]}", n + 1)
                u, d = check_nth_job(jsondir, nth_job_end[end_time], n + 1)
                unique.extend(u)
                duplicate.extend(d)
            else:
                # Reached the end without finding a different end time:: Schedule is the same
                rprint(f"Reached end of schedule without finding a different end time: {nth_job_end[end_time]}", n + 1,
                       alert=True)
                duplicate.extend(schedule_ids)

    return unique, duplicate


def isolate_same_schedule(path, cols):
    """
    Read schedule data to identify unique schedules on a dataset merged csv file
    """
    df = pd.read_csv(path, names=cols)
    # Total Rows
    makespans = df["cost"].value_counts()

    single_appearance = makespans[makespans == 1]
    multi_appearance = makespans[makespans > 1]
    single_schedule_ids = df[df["cost"].isin(single_appearance.index)]["schedule_id"]
    print(f"Found {len(single_appearance)} costs that only appear once")

    multi_schedule_ids = df[df["cost"].isin(multi_appearance.index)]["schedule_id"]
    print(f"Found {len(multi_schedule_ids)} costs that appear more than once")
    # Print makespan and schedule id with appearance count
    targets = df[df["schedule_id"].isin(multi_schedule_ids)]
    # print(df[df["schedule_id"].isin(multi_schedule_ids)]["cost"].value_counts())

    # Store dict of makespan to a list of schedule ids
    makespan_to_schedule_ids = {}
    for index, row in targets.iterrows():
        if row["cost"] not in makespan_to_schedule_ids:
            makespan_to_schedule_ids[row["cost"]] = []
        makespan_to_schedule_ids[row["cost"]].append(row["schedule_id"])

    found_u = []

    found_d = []
    found_dupes = []
    jsondir = "/home/kali/PycharmProjects/Capstone/jobs/output/genetic/json/"
    for row in makespan_to_schedule_ids:
        print("\nMakespan: ", row)
        print(
            f"{len(makespan_to_schedule_ids[row])} instances share this makespan.")  # {makespan_to_schedule_ids[row]}")
        uniques, dupes = check_json(jsondir=jsondir, schedule_ids=makespan_to_schedule_ids[row])
        print(f"Found {len(uniques)} unique schedules and {len(dupes)} duplicate schedules")
        print("_" * 50)
        found_u.extend(uniques)
        if len(dupes) > 0:
            print(f"Duplicate schedules: {dupes}")
            # Select
            # pick one of the duplicates to keep and ignore others in the list @TODO assign schedules their own id
            found_d.append(dupes[0])
            found_dupes.extend(dupes)

    # SUMARY
    print(f"Found {len(found_u)} unique schedules and {len(found_d)} duplicate schedules")

    # Stats
    print(f"Found {len(single_schedule_ids)} unique schedules from makespan")
    print(f"Found {len(found_u)} unique schedules from json")
    print(
        f"Found {len(found_dupes)} duplicate schedules from json with {len(found_d)} unique taken schedules from json")

    # Combine unique from sources into one df
    single = df[df["schedule_id"].isin(single_schedule_ids)]  # From makespan
    jsons = df[df["schedule_id"].isin(found_u)]  # Unique from json
    jsond = df[df["schedule_id"].isin(found_d)]  # Duplicate from json

    # Combine into one df
    unique = pd.concat([single, jsons, jsond])

    print(f"Found {len(unique)} unique schedules from makespan and json")
    # Sort by makespan
    unique = unique.sort_values(by=["cost"])
    print(unique.head())
    # Get only the ids as a list
    unique_ids = unique["schedule_id"].tolist()
    return unique_ids


def to_gif(img_path, gif_path, filename):
    frames = []
    path = img_path + "*.png"
    imgs = glob.glob(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(gif_path + filename, format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)

def render_gantts(dataset, alg_dir, ids):
    """
    Identify unique schedules and create a gif for the given dataset
    """

    print("\nCreating Gantt GIF for: " + dataset)
    # If there are no unique schedules then we can't make a gif
    if len(ids) == 0:
        print(f"\tNo unique schedules found for {dataset}")
        return

    img_path = f"{alg_dir}img/gif/{dataset}/"

    print(f"img_path: {img_path}")

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    print("TEST")
    n = len(ids)
    for i, slurm in enumerate(ids):
        time.sleep(0.1)
        progress = int(i / n * 50)
        print(f'running {i + 1} of {n} {progress * "."}', end='\r', flush=True)
        json_path = f"{alg_dir}/json/{slurm}_gantt.json"
        render_gantt_json(infile=json_path, destination=img_path, subdir=True)

    # Return output path
    return img_path



def render(alg):
    root_path = "/home/kali/PycharmProjects/Capstone/jobs/"
    alg_path = root_path + "output/" + alg + "/"

    csv_path = alg_path + "results/"
    gif_path = root_path + "results/"


    # datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    datasets = ["abz5"]
    for dataset in datasets:
        key = "instance,cost,seed,pop_size,ngen,mut_rate,cross_rate,timeout"
        cols = key.split(",") + ["schedule_id"]
        ids = isolate_same_schedule(csv_path + dataset + ".csv", cols)
        img_path = render_gantts(dataset, alg_path, ids)
        to_gif(img_path, gif_path, f"{alg}_{dataset}.gif")


if __name__ == "__main__":
    render("genetic")
