import seaborn as sns
import os
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def pretty_plot(alg, filepath, key, verbose=False):
    # Create some plots for the given instance
    # @TODO: Axis Scaling for number of X Vars
    # @TODO Key for GENETIC doesnt line up
    # Read the csv file
    print("Key: " + str(key))
    df = pd.read_csv(filepath, names=key, skiprows=1)
    print(df.head(3))

    root_path = win_uni_dir()
    alg_path = root_path + "output\\" + alg + "\\"
    csv_path = alg_path + "results\\"

    plots = ["seed"]
    # Get the unique datasets
    datasets = df["dataset"].unique()

    if "timeout" in key:
        timeouts = df["timeout"].unique()
        df = df.drop(columns=['timeout'])
        # Uncomment for multiple manual timeouts (not just early stopping)
        # if len(timeouts) > 1:
        #     plots.append("timeout")
        # else:
        #     df = df.drop(columns=['timeout'])

    # Handle plot types and create a new column for the parameter combinations

    standard = ["dataset", "cost", "seed", "slurm"]
    params = [col for col in df.columns if col not in standard]
    if len(params) > 0:
        plots.append("param")

    prefix = f'{win_root_dir()}\\jobs\\results\\output\\{alg}'
    # Make the directory if it doesn't exist
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    # Create a plot for each dataset
    for dataset in datasets:
        d = df[df["dataset"] == dataset].copy()
        dataset_name = d["dataset"].unique()[0]

        # Save it as a csv for later
        file = f'{csv_path}{dataset_name}.csv'
        d.to_csv(file, index=False)

        # Only handle if unique/multiple timeouts exist for the same data
        d['param'] = d[params].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
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


def win_uni_dir():
    return win_root_dir() + "\\jobs\\results\\"


def root_dir():
    """
    Dir above jobs
    """
    return os.getcwd()[0:os.getcwd().index("Capstone") + len("Capstone")]


def uni_dir():
    return root_dir() + "/jobs/results/"


def box_plotter(df, prefix, alg, dataset, X, Y):
    # @TODO Make sure scale is the same across all plots (y axis) so that they can be compared
    title = "{}: {} variance across {} for {}".format(alg, Y, X, dataset)
    # print("Rendering Boxplot: " + title)
    # if len(df[X].unique()) > 10:
    #     print("Warning, lots of X values, you should handle this better")

    sns.boxplot(x=X, y=Y, data=df)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.savefig(prefix + f"\\{dataset}_boxplot_{X}.png", bbox_inches='tight')
    plt.clf()


def unify_csvs(filepath, key, alg=None, add_slurm=False):
    file_sep = None
    if os.name == 'nt':
        file_sep = "\\"
    else:
        file_sep = "/"
    filepath += file_sep

    if "slurm" not in key:
        add_slurm = True
        key.append("slurm")

    csv_dir = filepath + "results" + file_sep

    print("Unifying path:" + csv_dir)
    # Delete the files we create if the script has been run before
    # If it is prefixed with results keep it, if it is not, delete it
    files_to_del = [f for f in os.listdir(csv_dir)
                    if f.startswith('results-') is False
                    and f.startswith("batched") is False
                    and f.endswith('.csv')]
    print(f"Deleting {len(files_to_del)} items: {files_to_del}")
    for file in files_to_del:
        # delete
        os.remove(csv_dir + file)

    # Get all files in the directory ending with .csv
    files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    print(f"Found {len(files)} files to unify")
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

    # IF os is windows

    if os.name != 'nt':
        # Linux
        # Use Command Line tools
        # Sort rows by instance
        os.system(f"sort -t, -k1,1 {filepath}/results.csv > {filepath}/results_sorted.csv")

        # Delete old file
        os.remove(f"{filepath}/results.csv")

        # Removed: Create a separate file for each instance, overwriting if it exists
        # os.system(f"awk -F, '{{print > \"{filepath}/\"$1\".csv\"}}' {filepath}/results_sorted.csv")

        # Copy the sorted file to the results directory
        result_dir = root_dir() + "/jobs/results/" + filepath.split("/")[-3]

        os.system(f"cp {filepath}/results_sorted.csv {result_dir}/results_sorted_{alg}.csv")

    else:
        # Windows
        # Use Python tools
        # Sort rows by instance
        df = pd.read_csv(f"{filepath}/results.csv", names=key)

        df.sort_values(by=key[0], inplace=True)

        df.to_csv(f"{filepath}/results_sorted.csv", index=False)

        # Delete old file
        os.remove(f"{filepath}/results.csv")

        # Removed: Create a separate file for each instance, overwriting if it exists

        # Copy the sorted file to the results directory
        command = f"copy {filepath}\\results_sorted.csv {win_uni_dir()}\\results_sorted_{alg}.csv"
        os.system(command)

    return key


def render_gantt_json(infile, destination, subdir=False):
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
    name = infile.split("\\")[-1].split(".")[0]
    slurm = name.split("_")[0]

    cost = gantt_data["title"].split("Cost: ")[-1]
    cost = cost.split(" ")[0]
    filename = f"{destination}/{cost}-gantt-{slurm}.png"

    # if file exists, delete it
    if os.path.exists(filename):
        os.remove(filename)

    fig.write_image(filename, format="png")
