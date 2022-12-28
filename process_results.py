import seaborn as sns
import os
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def pretty_plots(instance, dir, key):
    # Create some plots for the given instance

    # Box and whisker plot: Cost variance across seed for each parameter combination

    # Load the file
    cols = key.split(",")
    path = f"{dir}/{instance}"
    df = pd.read_csv(path, names=cols)

    # Unique timeouts
    timeouts = df["timeout"].unique()
    # drop timeout column
    df = df.drop(columns=['timeout'])

    # Create a new column for the parameter combination
    df['param'] = df['temp'].astype(str) + "-" + df['cooldown'].astype(str)

    plt.figure()

    # Boxplot for overall performance with all seeds combined
    box_plotter(df, dir, instance, "Overall performance", X="param", Y="cost")

    # Create a boxplot for each
    box_plotter(df, dir, instance, "Cost variance across seeds for " + instance, X="seed", Y="cost")
    box_plotter(df, dir, instance, "Cost variance across parameter combination for " + instance, X="param", Y="cost")


def box_plotter(df, dir, instance, name, X="param", Y="cost"):
    result_dir = os.getcwd() + "/jobs/results/" + dir.split("/")[-1]
    sns.boxplot(x=X, y=Y, data=df)
    # Rotate x labels
    plt.xticks(rotation=90)
    plt.title(name)
    plt.savefig(f"{result_dir}/{instance}_boxplot_{X}.png", bbox_inches='tight')
    plt.clf()


def unify_csvs(dir, key):
    # Delete the files we create if the script has been run before
    # If it is prefixed with results keep it, if it is not, delete it
    for file in os.listdir(dir):
        if file.startswith("results-"):
            continue
        elif file.endswith(".csv"):
            os.remove(f"{dir}/{file}")

    # Get all files in the directory ending with .csv
    files = [f for f in os.listdir(dir) if f.endswith('.csv')]
    # instance, cost, seed, temp, cooldown, timeout
    # Iterate over files and add to a new file
    with open(f"{dir}/results.csv", "w") as results_file:
        for file in files:
            with open(f"{dir}/{file}", "r") as file:
                for line in file:
                    results_file.write(line)
    # Sort rows by instance
    os.system(f"sort -t, -k1,1 {dir}/results.csv > {dir}/results_sorted.csv")

    # Delete old file
    os.remove(f"{dir}/results.csv")

    # Create a separate file for each instance, overwriting if it exists
    os.system(f"awk -F, '{{print > \"{dir}/\"$1\".csv\"}}' {dir}/results_sorted.csv")
    result_dir = os.getcwd() + "/jobs/results/" + dir.split("/")[-1]

    # Copy the sorted file to the results directory
    os.system(f"cp {dir}/results_sorted.csv {result_dir}/results_sorted.csv")


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


if __name__ == '__main__':

    outdir = "/home/kali/PycharmProjects/Capstone/jobs/output/"
    sim_dir = outdir + "sim_anneal/"
    tabu_dir = outdir + "tabu_search/"


    ### SIMULATED ANNEALING ###
    # key = "instance,cost,seed,temp,cooldown,timeout"
    # unify_csvs(dir=sim_dir, key=key)
    #
    # datasets = [f for f in os.listdir(sim_dir) if f.startswith('results') is False and f.endswith('.csv')]
    # for dataset in datasets:
    #     pretty_plots(instance=dataset, dir=sim_dir, key=key)
    #
    # # pretty_plots(instance="results_sorted.csv", dir=dir, key=key)

    ### TABU SEARCH GANTT ###
    # for file in os.listdir(tabu_dir + "{DATE}/json/"):
    candidates = tabu_dir + "json/"

    files = [f for f in os.listdir(candidates) if f.endswith('.json')]
    for file in files:
        render_gantt_json(file=candidates + file, outdir=tabu_dir)
