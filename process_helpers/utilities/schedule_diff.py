import glob
import json
import os
from multiprocessing import Pool

import pandas as pd
from PIL import Image

from process_helpers.utilities.plotting import render_gantt_json, uni_dir, win_uni_dir, get_one_to_many

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


def flat_check(jsondir, slurms, dataset, makespan, slurm_encoded):
    """
    Much faster way to check for unique schedules
    """
    # Make a temp directory, Create a file named after the makespan,
    # For each slurm, load the json, and save each end time on a line seperated by commas

    os.makedirs(f"{jsondir}\\temp", exist_ok=True)
    with open(f"{jsondir}\\temp\\{makespan}.csv", "w") as f:

        slurms_sub = slurms
        if slurm_encoded:
            slurms = [str(slurm)[3:] for slurm in slurms]

        for i, slurm in enumerate(slurms):
            # if it is encoded then we drop the first 3 chars which are the dataset

            # Check slurm to prevent  cannot convert float NaN to integer
            # if slurm is float nan

            try:
                slurm = int(slurm)
            except ValueError:
                print(f"ValueError: {slurm} is not an integer")

            json_path = f"{jsondir}{(slurm)}_gantt.json"
            if "constraint" in jsondir or "dispatching" in jsondir:
                json_path = f"{jsondir}\\{dataset}-{int(slurm)}_gantt.json"

            with open(json_path, 'r') as j:
                json_data = json.load(j)
                for package in json_data["packages"]:
                    f.write(f"{package['end']},")
                f.write(f'{slurms_sub[i]}\n')

    # Read all lines
    # Pandas unique read csv
    df = pd.read_csv(f"{jsondir}\\temp\\{makespan}.csv", header=None)

    # Factorize the dataframe apart from the last column which is kept
    slurms = df.iloc[:, -1]
    all_slurms_list = [str(slurm) for slurm in slurms.tolist()]

    df = df.iloc[:, :-1].apply(lambda x: pd.factorize(x)[0])

    # Write the factorized dataframe to a csv
    df.to_csv(f"{jsondir}\\temp\\{makespan}_factorized.csv", index=False, header=False)

    # Put the slurms back in
    df["slurm"] = slurms
    # Slurms list

    # IF all but the last column (slurm) are the same then they are the same schedule
    # Track the unique schedules
    # - drop any repeats but store the slurm of the dropped one in a dict with the key being the slurm of the kept one

    schedules_to_ids = {}

    for i, row in df.iterrows():

        # Make the row hashable, and exclude the slurm column
        row = row[:-1]
        # Hash
        key = hash(tuple(row))

        slurm = df["slurm"][i]
        # If key is not in dict then add it
        if key not in schedules_to_ids.keys():
            schedules_to_ids[key] = str(slurm)
        else:
            schedules_to_ids[key] += f",{slurm}"

    slurm_map = {}
    for row, slurms in schedules_to_ids.items():
        if "," in slurms:
            ids = slurms.split(",")
            key = ids[0]
            matches = ids[1:]
            slurm_map[key] = matches
        else:
            slurm_map[slurms] = []
            # If there is only one slurm then it is not a duplicate

    # for k, v in slurm_map.items():
    #     print(f"{k} : {v}")

    # Stats

    unique_slurms = list(slurm_map.keys())
    duplicate_slurms = [slurm for slurm in all_slurms_list if slurm not in unique_slurms]

    # print(f"Unique Slurms: {(unique_slurms)}")
    # print(f"Duplicate Slurms: {(duplicate_slurms)}")
    #
    # print(f"Unique: {len(unique_slurms)}, Duplicates: {len(duplicate_slurms)}")

    # Delete file
    os.remove(f"{jsondir}\\temp\\{makespan}.csv")

    return slurm_map, duplicate_slurms


def check_json(jsondir, slurms, alg, dataset, n=0, makespan=None):
    """
    Pass in a list of schedule ids and return a list of unique schedules from that list
    """
    slurm_encoded = False
    if alg in get_one_to_many():
        slurm_encoded = True

    if makespan is None:
        return check_nth_job(jsondir, slurms, dataset, n)
    else:
        return flat_check(jsondir, slurms, dataset, makespan, slurm_encoded)

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
    # Keep only the rows with the same dataset
    df = df[df["dataset"] == dataset]

    # Total Rows
    makespans = df["cost"].value_counts()

    single_appearance = makespans[makespans == 1]
    multi_appearance = makespans[makespans > 1]
    single_slurms = df[df["cost"].isin(single_appearance.index)]["slurm"]
    # print(f"Found {len(single_appearance)} costs that only appear once")

    multi_slurms = df[df["cost"].isin(multi_appearance.index)]["slurm"]
    # print(f"Found {len(multi_slurms)} costs that appear more than once")
    # Print makespan and schedule id with appearance count
    targets = df[df["slurm"].isin(multi_slurms)]
    # print(df[df["slurm"].isin(multi_slurms)]["cost"].value_counts())

    # Store dict of makespan to a list of schedule ids
    makespan_to_slurms = {}
    for index, makespan in targets.iterrows():
        if makespan["cost"] not in makespan_to_slurms:
            makespan_to_slurms[makespan["cost"]] = []
        makespan_to_slurms[makespan["cost"]].append(makespan["slurm"])

    found_u = []
    found_dupes = []
    slurms_dicts_list = []
    jsondir = json_path

    n_rows = len(makespan_to_slurms)
    print(f"\nFound {n_rows} makespans that appear more than once for {dataset} {alg}")
    for makespan in makespan_to_slurms:

        slurm_map, dupes = check_json(jsondir=jsondir,
                                      slurms=makespan_to_slurms[makespan],
                                      alg=alg,
                                      dataset=dataset,
                                      makespan=makespan
                                      )

        uniques = slurm_map.keys()
        # Convert to ints
        uniques = [int(x) for x in uniques]
        print(f"\tMakespan: {makespan} - {len(makespan_to_slurms[makespan])} "
              f"instances with {len(uniques)}/{len(dupes)} uniques/dupes")
        slurms_dicts_list.append(slurm_map)
        found_u.extend(uniques)
        if len(dupes) > 0:
            dupes = [int(x) for x in dupes]
            found_dupes.extend(dupes)

    # SUMARY
    print(f"\n{dataset} {alg} - SUMMARY")
    print(f"Selected {len(found_u)} unique schedules")

    # Stats
    print(f"Found {len(single_slurms)} uniques from makespan, "
          f"{len(found_u)} from json and {len(found_dupes)} duplicates")

    # Combine unique from sources into one df

    # Make a copy of df with the elements where the slurm is in single_slurms
    dfA = df.copy()
    dfB = df.copy()

    single = dfA[dfA["slurm"].isin(single_slurms)]
    jsons = dfB[dfB["slurm"].isin(found_u)]
    print(f"Found {len(single)} unique from makespan and {len(jsons)} from json")

    unique = pd.concat([single, jsons], ignore_index=True)
    unique = unique.sort_values(by=["cost"])

    # Flatten the list of dicts into a single dict
    slurms_dict = {}
    for dictionary in slurms_dicts_list:
        slurms_dict.update(dictionary)

    # Put the makespan found slurms into the slurms dict
    for slurm in single_slurms:
        slurms_dict[slurm] = []

    # Ensure all keys are strings
    slurms_dict = {str(k): v for k, v in slurms_dict.items()}

    # Get only the ids as a list
    unique_ids = unique["slurm"].tolist()
    return unique_ids, slurms_dict


def get_unique_solutions_by_alg(alg, key, json_path):
    root_path = win_uni_dir()
    alg_path = root_path + "output\\" + alg + "\\"

    csv_path = alg_path + "results\\"
    gif_path = root_path + "results\\"
    unique_sol_ids = f"{alg_path}unique_solution_ids.txt"  # Shared betwixt all datasets
    # Delete file if it exists
    if os.path.exists(unique_sol_ids):
        os.remove(unique_sol_ids)

    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    for dataset in datasets:
        file = f'{win_uni_dir()}results_sorted_{alg}.csv'

        # For indvidual files
        # cols = key.copy()
        # if "timeout" in cols:
        #     cols.remove("timeout")

        # df = pd.read_csv(file, names=cols, skiprows=1)
        #
        # print(df.head())
        # input("Press Enter to continue...")

        # Try ids as dict unique to duplicates
        # when writing to a file each line is a new schedule and the first one is the selected one
        ids, dupes = isolate_same_schedule(file, key, json_path, dataset, alg)
        print(dupes.keys())
        # Save IDs to file
        with open(unique_sol_ids, "a") as f:
            for item in ids:
                matches = dupes[str(item)]
                # Format matches like csv
                matches = ",".join(matches)
                f.write(f'{item}:{matches}\n')
        print(f"Saved {len(ids)} unique solutions to {unique_sol_ids}")



if __name__ == "__main__":
    get_unique_solutions_by_alg("genetic")
