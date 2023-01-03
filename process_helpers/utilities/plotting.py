import seaborn as sns
import os
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def pretty_plot(alg, filepath, key, verbose=False):
    # Create some plots for the given instance

    # Read the csv file
    df = pd.read_csv(filepath, names=key)

    # Split into list of dataframes by dataset Using list comprehension

    # Get the unique datasets
    datasets = df["dataset"].unique()

    # Create a plot for each dataset
    for dataset in datasets:
        d = df[df["dataset"] == dataset].copy()
        dataset_name = d["dataset"].unique()[0]
        # Only handle if unique/multiple timeouts exist for the same data
        if "timeout" in key:
            timeouts = d["timeout"].unique()
            d = d.drop(columns=['timeout'])
            if len(timeouts) > 1:
                # Raise unimplemented error
                raise NotImplementedError("Multiple timeouts not implemented for plotting same data")

        # Create a new column for the parameter combination
        standard = ["dataset", "cost", "seed", "slurm"]
        # Combine the remaining columns into a single column "param"
        params = [col for col in d.columns if col not in standard]
        d['param'] = d[params].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)

        prefix = f'{win_root_dir()}\\jobs\\results\\output\\{alg}'
        # Make the directory if it doesn't exist
        if not os.path.exists(prefix):
            os.makedirs(prefix)

        plots = ["seed", "param"]
        for plot in plots:
            box_plotter(d, prefix, alg, dataset_name, plot, "cost")


def alg_gantts(candidates, filepath):
    files = [f for f in os.listdir(candidates) if f.endswith('.json')]
    for file in files:
        render_gantt_json(file=candidates + file, outdir=filepath)


def win_root_dir():
    """
    Dir above jobs
    """
    return os.getcwd()[0:os.getcwd().index("Code") + len("Code")]


def root_dir():
    """
    Dir above jobs
    """
    return os.getcwd()[0:os.getcwd().index("Capstone") + len("Capstone")]


def box_plotter(df, prefix, alg, dataset, X, Y):
    # @TODO Make sure scale is the same across all plots (y axis) so that they can be compared
    title = "{}: {} variance across {} for {}".format(alg, Y, X, dataset)
    sns.boxplot(x=X, y=Y, data=df)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.savefig(prefix + f"\\{dataset}_boxplot_{X}.png", bbox_inches='tight')
    plt.clf()


def unify_csvs(filepath, key, alg=None, add_slurm=False):
    if "slurm" not in key:
        add_slurm = True

    csv_dir = filepath + "results/"
    print("Unifying csvs")
    print("Trying for dir " + filepath.split("/")[-3])
    print("Full path:" + csv_dir)
    # Delete the files we create if the script has been run before
    # If it is prefixed with results keep it, if it is not, delete it
    files_to_del = [f for f in os.listdir(csv_dir) if f.startswith('results-') is False and f.endswith('.csv')]
    print(files_to_del)

    for file in files_to_del:
        # delete
        os.remove(csv_dir + file)

    # Get all files in the directory ending with .csv
    files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    # instance, cost, seed, temp, cooldown, timeout
    # Iterate over files and add to a new file
    with open(f"{filepath}/results.csv", "w") as results_file:
        for file in files:
            with open(f"{csv_dir}/{file}", "r") as file:
                for line in file:
                    if add_slurm:
                        slurm = file.name.split("/results-")[-1].split(".csv")[0]
                        line = line.strip() + "," + slurm + "\n"
                    else:
                        line = line.strip() + "\n"
                    results_file.write(line)

    # Sort rows by instance
    os.system(f"sort -t, -k1,1 {filepath}/results.csv > {filepath}/results_sorted.csv")

    # Delete old file
    os.remove(f"{filepath}/results.csv")

    # Create a separate file for each instance, overwriting if it exists
    os.system(f"awk -F, '{{print > \"{filepath}/\"$1\".csv\"}}' {filepath}/results_sorted.csv")
    result_dir = root_dir() + "/jobs/results/" + filepath.split("/")[-3]

    # Copy the sorted file to the results directory
    os.system(f"cp {filepath}/results_sorted.csv {result_dir}/results_sorted.csv")

    # If alg is specified output to the unified dir
    if alg is not None:
        # Copy the sorted file to the results directory for the unified dir
        os.system(f"cp {filepath}/results_sorted.csv {result_dir}/results_sorted_{alg}.csv")

    return key.append("slurm") if add_slurm else key


def render_gantt_json(infile, destination, subdir=False):
    print("Rendering gantt chart for " + infile)
    with open(infile, "r") as f:
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
    name = infile.split("/")[-1].split(".")[0]
    slurm = name.split("_")[0]

    cost = gantt_data["title"].split("Cost: ")[-1]
    cost = cost.split(" ")[0]
    filename = f"{destination}/{cost}-gantt-{slurm}.png"

    fig.write_image(filename, format="png")
