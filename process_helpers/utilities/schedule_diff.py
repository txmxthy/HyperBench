import glob
import json
import os
from multiprocessing import Pool

import pandas as pd
from PIL import Image

from process_helpers.utilities.plotting import render_gantt_json, uni_dir, win_uni_dir

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


def flat_check(jsondir, slurms, dataset, makespan):
    """
    Much faster way to check for unique schedules
    """
    # Make a temp directory, Create a file named after the makespan,
    # For each slurm, load the json, and save each end time on a line seperated by commas

    os.makedirs(f"{jsondir}\\temp", exist_ok=True)
    with open(f"{jsondir}\\temp\\{makespan}.csv", "w") as f:
        for slurm in slurms:
            json_path = f"{jsondir}{int(slurm)}_gantt.json"
            if "constraint" in jsondir or "dispatching" in jsondir:
                json_path = f"{jsondir}\\{dataset}-{int(slurm)}_gantt.json"

            with open(json_path, 'r') as j:
                json_data = json.load(j)
                for package in json_data["packages"]:
                    f.write(f"{package['end']},")
                f.write(f'{slurm}\n')

    # Read all lines
    # Pandas unique read csv
    df = pd.read_csv(f"{jsondir}\\temp\\{makespan}.csv", header=None)

    # Factorize the dataframe apart from the last column which is kept
    slurms = df.iloc[:, -1]
    df = df.iloc[:, :-1].apply(lambda x: pd.factorize(x)[0])

    # Count unique rows
    # unique = df.drop_duplicates().shape[0] - 1 # We count as  unique only if it appears once
    # duplicate = df.shape[0] - unique
    # print(f"Unique: {unique}, Duplicate: {duplicate}")

    # Put the slurms back in
    df["slurm"] = slurms

    # Drop duplicates again (Ignore the slurm column when checking for duplicates, but drop it if its row is a duplicate)
    df = df.drop_duplicates(subset=df.columns[:-1], keep="first")

    uniques = df["slurm"].tolist()
    duplicates = [slurm for slurm in slurms if slurm not in uniques]

    # write
    # df.to_csv(f"{jsondir}\\temp\\{makespan}_factorized.csv", index=False, header=False)

    # Delete file
    os.remove(f"{jsondir}\\temp\\{makespan}.csv")

    return uniques, duplicates


def check_json(jsondir, slurms, dataset, n=0, makespan=None, alg=None):
    """
    Pass in a list of schedule ids and return a list of unique schedules from that list
    """
    if makespan is None:
        return check_nth_job(jsondir, slurms, dataset, n)
    else:
        return flat_check(jsondir, slurms, dataset, makespan)

    # If the times are different then they are not the same schedule,


def check_nth_job(jsondir, slurms, dataset, n=0):
    unique = []
    duplicate = []

    nth_job_end = {}
    for slurm in slurms:
        # If constraint or dispatching in path then switch jsobpath variable
        json_path = f"{jsondir}{slurm}_gantt.json"
        if "constraint" in jsondir or "dispatching" in jsondir:
            json_path = f"{jsondir}\\{dataset}-{slurm}_gantt.json"

        # json_path = f"{jsondir}{dataset}-{slurm}_gantt.json"
        with open(json_path, 'r') as f:
            json_data = json.load(f)
            # add to dict with key if key exist else create
            if json_data["packages"][n]["end"] not in nth_job_end:
                nth_job_end[json_data["packages"][n]["end"]] = []
            nth_job_end[json_data["packages"][n]["end"]].append(slurm)

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
                u, d = check_nth_job(jsondir, nth_job_end[end_time], dataset, n + 1)
                unique.extend(u)
                duplicate.extend(d)
            else:
                # Reached the end without finding a different end time:: Schedule is the same
                rprint(f"Reached end of schedule without finding a different end time: {nth_job_end[end_time]}", n + 1,
                       alert=True)
                duplicate.extend(slurms)

    return unique, duplicate


def isolate_same_schedule(path, cols, json_path, dataset, alg):
    """
    Read schedule data to identify unique schedules on a dataset merged csv file
    """
    df = pd.read_csv(path, names=cols, skiprows=1)
    # Total Rows
    makespans = df["cost"].value_counts()

    single_appearance = makespans[makespans == 1]
    multi_appearance = makespans[makespans > 1]
    single_slurms = df[df["cost"].isin(single_appearance.index)]["slurm"]
    print(f"Found {len(single_appearance)} costs that only appear once")

    multi_slurms = df[df["cost"].isin(multi_appearance.index)]["slurm"]
    print(f"Found {len(multi_slurms)} costs that appear more than once")
    # Print makespan and schedule id with appearance count
    targets = df[df["slurm"].isin(multi_slurms)]
    # print(df[df["slurm"].isin(multi_slurms)]["cost"].value_counts())

    # Store dict of makespan to a list of schedule ids
    makespan_to_slurms = {}
    for index, row in targets.iterrows():
        if row["cost"] not in makespan_to_slurms:
            makespan_to_slurms[row["cost"]] = []
        makespan_to_slurms[row["cost"]].append(row["slurm"])

    found_u = []

    found_d = []
    found_dupes = []
    jsondir = json_path
    for row in makespan_to_slurms:
        print("\nMakespan: ", row)
        print(
            f"{len(makespan_to_slurms[row])} instances share this makespan.")  # {makespan_to_slurms[row]}")
        uniques, dupes = check_json(jsondir=jsondir,
                                    slurms=makespan_to_slurms[row],
                                    dataset=dataset,
                                    makespan=row,
                                    alg=alg)
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
    print(f"Found {len(single_slurms)} unique schedules from makespan")
    print(f"Found {len(found_u)} unique schedules from json")
    print(
        f"Found {len(found_dupes)} duplicate schedules from json with {len(found_d)} unique taken schedules from json")

    # Combine unique from sources into one df
    single = df[df["slurm"].isin(single_slurms)]  # From makespan
    jsons = df[df["slurm"].isin(found_u)]  # Unique from json
    jsond = df[df["slurm"].isin(found_d)]  # Duplicate from json

    # Combine into one df
    unique = pd.concat([single, jsons, jsond])

    print(f"Found {len(unique)} unique schedules from makespan and json")
    # Sort by makespan
    unique = unique.sort_values(by=["cost"])
    # Get only the ids as a list
    unique_ids = unique["slurm"].tolist()
    return unique_ids


def get_unique_solutions_by_alg(alg, key, json_path):


    root_path = win_uni_dir()
    alg_path = root_path + "output\\" + alg + "\\"

    csv_path = alg_path + "results\\"
    gif_path = root_path + "results\\"

    # datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    datasets = ["abz5"]
    for dataset in datasets:
        file = f'{csv_path}{dataset}.csv'
        cols = key.copy()
        if "timeout" in cols:
            cols.remove("timeout")

        # df = pd.read_csv(file, names=cols, skiprows=1)
        #
        # print(df.head())
        # input("Press Enter to continue...")

        ids = isolate_same_schedule(file, cols, json_path, dataset, alg)

        # Save IDs to file
        with open(f"{alg_path}unique_solution_ids.txt", "w") as f:
            for item in ids:
                f.write("%s" % item + "\n")


if __name__ == "__main__":
    get_unique_solutions_by_alg("genetic")
