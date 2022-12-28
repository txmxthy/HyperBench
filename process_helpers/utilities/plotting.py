import seaborn as sns
import os
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def alg_merge_boxes(alg, filepath, key):
    print("Merging CSVs for Boxplots: " + alg)

    unify_csvs(filepath, key=key)

    datasets = [f for f in os.listdir(filepath) if f.startswith('results') is False and f.endswith('.csv')]
    for dataset in datasets:
        pretty_plots(instance=dataset, target_dir=filepath, key=key, alg=alg)

    pretty_plots(instance="results_sorted.csv", target_dir=filepath, key=key, alg=alg, verbose=True)



def pretty_plots(instance, target_dir, key, alg, verbose=False):
    # Create some plots for the given instance

    # Box and whisker plot: Cost variance across seed for each parameter combination

    # Load the file
    cols = key.split(",")
    path = f"{target_dir}/{instance}"
    df = pd.read_csv(path, names=cols)

    # Unique timeouts
    timeouts = df["timeout"].unique()
    # drop timeout column
    df = df.drop(columns=['timeout'])

    ### Create a new column for the parameter combination ###

    if alg == "SA":
        df['param'] = df['temp'].astype(str) + "-" + df['cooldown'].astype(str)

    elif alg == "TA":
        df['param'] = df['tabu_length'].astype(str) + "-" + df['max_steps'].astype(str) + "-" + df[
            'longest_hold'].astype(
            str)

    # Boxplot for overall performance with all seeds combined
    box_plotter(df, target_dir, instance, alg + "Cost variance across seeds for " + instance, X="seed", Y="cost")
    box_plotter(df, target_dir, instance, alg + "Cost variance across parameter combination for " + instance, X="param",
                Y="cost")

    # Box plot with a seperate box for each dataset (instance)
    if verbose:
        box_plotter(df, target_dir, "Overall variance across datasets", alg + "Overall variance across datasets" + instance, X="instance",
                    Y="cost")



def alg_gantts(candidates, filepath):
    files = [f for f in os.listdir(candidates) if f.endswith('.json')]
    for file in files:
        render_gantt_json(file=candidates + file, outdir=filepath)


def box_plotter(df, target_dir, instance, name, X="param", Y="cost",):
    #@TODO Make sure scale is the same across all plots (y axis) so that they can be compared
    result_dir = os.getcwd() + "/jobs/results/" + target_dir.split("/")[-3]
    sns.boxplot(x=X, y=Y, data=df)
    # Rotate x labels
    plt.xticks(rotation=90)
    plt.title(name)
    plt.savefig(f"{result_dir}/{instance}_boxplot_{X}.png", bbox_inches='tight')
    plt.clf()


def unify_csvs(filepath, key):
    print("Unifying csvs")
    print("Trying for dir " + filepath.split("/")[-3])
    # Delete the files we create if the script has been run before
    # If it is prefixed with results keep it, if it is not, delete it
    for file in os.listdir(filepath):
        if file.startswith("results-"):
            continue
        elif file.endswith(".csv"):
            os.remove(f"{filepath}/{file}")

    # Get all files in the directory ending with .csv
    files = [f for f in os.listdir(filepath) if f.endswith('.csv')]
    # instance, cost, seed, temp, cooldown, timeout
    # Iterate over files and add to a new file
    with open(f"{filepath}/results.csv", "w") as results_file:
        for file in files:
            with open(f"{filepath}/{file}", "r") as file:
                for line in file:
                    results_file.write(line)
    # Sort rows by instance
    os.system(f"sort -t, -k1,1 {filepath}/results.csv > {filepath}/results_sorted.csv")

    # Delete old file
    os.remove(f"{filepath}/results.csv")

    # Create a separate file for each instance, overwriting if it exists
    os.system(f"awk -F, '{{print > \"{filepath}/\"$1\".csv\"}}' {filepath}/results_sorted.csv")
    result_dir = os.getcwd() + "/jobs/results/" + filepath.split("/")[-3]

    # Copy the sorted file to the results directory
    os.system(f"cp {filepath}/results_sorted.csv {result_dir}/results_sorted.csv")


def render_gantt_json(file, outdir):
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
    # Read the name of the file
    name = file.split("/")[-1].split(".")[0]
    slurm = name.split("_")[0]

    fig.write_image(outdir + "/img/gantt-" + slurm + ".png", format="png")
