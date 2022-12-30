import glob
import os
from PIL import Image
import pandas as pd

from process_helpers.utilities.plotting import alg_gantts, alg_merge_boxes, render_gantt_json


def gantt_gif_by_dataset(dataset, key, target_dir):
    """
    Identify unique schedules and create a gif for the given dataset
    """

    print("\nCreating Gantt GIF for: " + dataset)
    unique_schedule_ids = None
    csv_path = f"{target_dir}/results/{dataset}.csv"
    # Columns
    cols = key.split(",") + ["schedule_id"]
    # Load the file
    ids = unique_slurm_ids(cols, csv_path)

    # If there are no unique schedules then we can't make a gif
    if len(ids) == 0:
        print(f"\tNo unique schedules found for {dataset}")
        return

    #
    # Create folders
    # {target_dir}/gif/{dataset}/
    # If {target_dir}/gif/{dataset}/ does not exist, create it
    img_path = f"{target_dir}/img/gif/{dataset}/"

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    for slurm in ids:
        json_path = f"{target_dir}json/{slurm}_gantt.json"
        render_gantt_json(file=json_path, outdir=img_path, img_subdir=False)

    # Create the gif

    frames = []
    path = img_path + "*.png"
    imgs = glob.glob(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(target_dir + dataset, format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)


def unique_slurm_ids(cols, csv_path):
    df = pd.read_csv(csv_path, names=cols)
    # Total Rows
    total_rows = len(df.index)
    # Count how often each cost appears
    makespans = df["cost"].value_counts()
    # print(makespans)
    # Keep the makespans that appear only once
    single_appearance = makespans[makespans == 1]
    # print(f"Found {len(single_appearance)} costs that only appear once")
    # print(f"\t\t{total_rows - len(single_appearance)} appear more than once")
    # Get the schedule ids where the cost is in the unique_makespans
    unique_schedule_ids = df[df["cost"].isin(single_appearance.index)]["schedule_id"]
    # print(unique_schedule_ids)
    # @TODO, look at the other schedules to find remaining unique schedules
    # Could json dump the "Packages part of the json
    return unique_schedule_ids


def animated_gantt(target_dir, key):
    """
    Make a gif to show each unique gantt chart
    """

    # To create the animation we need to identify unique schedules
    # if a schedule is the same then it will have the same makespan. but not all makespans are the same schedule.
    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    for dataset in datasets:
        gantt_gif_by_dataset(dataset, key, target_dir)

    # Create the frames
    frames = []
    path = target_dir + "img/gif/*/*.png"
    imgs = glob.glob(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(target_dir + "ALL.gif", format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)


if __name__ == '__main__':
    outdir = "/home/kali/PycharmProjects/Capstone/jobs/output/"
    sim_dir = outdir + "sim_anneal/"
    tabu_dir = outdir + "tabu_search/"
    genetic_dir = outdir + "genetic/"
    constraint_dir = outdir + "constraint/"
    dispatch_dir = outdir + "dispatching_rules/"

    # # Box Plots and CSV magic
    # key = "instance,cost,seed,temp,cooldown,timeout"
    # alg_merge_boxes("SA", sim_dir + "results/", key)
    #
    # key = "instance,cost,seed,tabu_length,max_steps,longest_hold,timeout"
    # alg_merge_boxes("TA", tabu_dir + "results/", key)

    # Genetic
    key = "instance,cost,seed,pop_size,ngen,mut_rate,cross_rate,timeout"
    # alg_merge_boxes("GA", genetic_dir + "results/", key)
    animated_gantt(genetic_dir, key)

    # # # Gantt Charts
    # alg_gantts(tabu_dir + "json/", tabu_dir)
    #
    # alg_gantts(genetic_dir + "json/", genetic_dir)

    # alg_gantts(constraint_dir + "json/", constraint_dir)

    # alg_gantts(sim_dir + "json/", sim_dir)

    # Animated Different Gantt Charts

    #@TODO
    # Table of results for each algorithm
    # Terminal output and latex table

    print("Done!")
