import random

from scipy import stats
import seaborn as sns
import os
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from PIL.PngImagePlugin import PngInfo


def save_encoding(encoding):
    with open(f'{win_uni_dir()}\\encoding.json', 'w') as f:
        json.dump(encoding, f)


def load_encoding():
    with open(f'{win_uni_dir()}\\encoding.json', 'r') as f:
        encoding = json.load(f)
    return encoding


def get_one_to_many():
    # @TODO can check for duplicate keys to automatically create this list in future
    return ["dispatching_rules"]


def pretty_plot(alg, filepath, key, verbose=False):
    # Create some plots for the given instance
    # @TODO: Axis Scaling for number of X Vars
    # @TODO Key for GENETIC doesnt line up
    # Read the csv file

    df = pd.read_csv(filepath, names=key, skiprows=1)

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
        # file = f'{csv_path}{dataset_name}.csv'
        # d.to_csv(file, index=False)

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
        print(key)
        print("Warning: slurm not in key, adding it")
        add_slurm = True
        key.append("slurm")
        print(key)

    csv_dir = filepath + "results" + file_sep

    # Delete the files we create if the script has been run before
    # If it is prefixed with results keep it, if it is not, delete it
    files_to_del = [f for f in os.listdir(csv_dir)
                    if f.startswith('results-') is False
                    and f.startswith("batched") is False
                    and f.endswith('.csv')]

    for file in files_to_del:
        print(f"Deleting {len(files_to_del)} items: {files_to_del}")
        os.remove(csv_dir + file)

    # Get all files in the directory ending with .csv
    files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    print(f"Found {len(files)} files to unify")
    # instance, cost, seed, temp, cooldown, timeout
    # Iterate over files and add to a new file
    with open(f"{filepath}{file_sep}results.csv", "w") as results_file:
        for file in files:
            with open(f"{csv_dir}{file_sep}{file}", "r") as file:
                for line in file:
                    if add_slurm:
                        slurm = file.name.split("results-")[-1].split(".csv")[0]
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
        target = f"{filepath}\\results.csv"
        print(f"Sorting {target}")

        df = pd.read_csv(target, names=key)
        # Ensure cost is an int
        df['cost'] = df['cost'].astype(int)
        df.sort_values(by=key[0], inplace=True)

        df.to_csv(f"{filepath}/results_sorted.csv", index=False)

        # Delete old file
        os.remove(f"{filepath}/results.csv")

        # Removed: Create a separate file for each instance, overwriting if it exists

        # Copy the sorted file to the results directory
        command = f"copy {filepath}\\results_sorted.csv {win_uni_dir()}\\results_sorted_{alg}.csv"
        os.system(command)

    return key


def render_gantt_json(infile, destination, dupes, alg):
    # @TODO Max param for scaling can change by what you want to show.
    # Ie for dataset anim alg df['cost'].max() + 10 would be good,
    # But for comparing algorithms you want all algs max
    # max_cost = df['cost'].max() + 10

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

    raw_title = gantt_data["title"]
    try:

        prefix, slurm = raw_title.split("Slurm: ")
        name_ds, cost = prefix.split("Cost: ")
        cost = int(float(cost.strip()))
        title = f"{name_ds.strip()}: {cost} id: {slurm}"

        if len(dupes) > 1:
            title += f" copies: {len(dupes)}"
    except ValueError as v:
        print(f"Error parsing title: {raw_title} err: {v}")

    fig = px.timeline(df, x_start="Start", x_end="End", y="Machine", color="Color", labels="Job",
                      title=title)
    fig.update_yaxes(autorange="reversed")

    fig.layout.xaxis.type = 'linear'
    fig.layout.xaxis.range = [-10, df['End'].max() + 10]
    # fig.layout.xaxis.range = [min_cost, max_cost] # Disabled for now

    for d in fig.data:
        filt = df['Color'] == d.name
        d.name = str(df[filt]['Job'].values[0])
        d.x = df[filt]['Delta'].tolist()

    fig.update_xaxes(type='linear')
    fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up

    filename = f"{destination}/{cost}-gantt-{slurm}.png"

    # Attach the dupes

    # if file exists, delete it
    if os.path.exists(filename):
        os.remove(filename)
    try:
        fig.write_image(filename, format="png")
    except FileExistsError as e:
        print(f"File {filename} already exists")
        raise e

    # Write the dupes to the png files metadata
    # if len(dupes) > 1:
    #     # Get the image
    #     img = Image.open(filename)
    #     metadata = PngInfo()
    #     metadata.add_text("dupes", str(dupes))
    #     img.save(filename, "png", pnginfo=metadata)


def handle_one_to_many(path_prefix, algs):
    """
    To decode, the dict has a map of ints -> datasets
    The first 3 digits of the slurm col for encoded int are the dataset
    """

    def encode_dataset(n_codes):
        return set([random.randint(100, 999) for _ in range(n_codes)])

    encodings = {}
    for alg in algs:

        filename = f"\\results_sorted_{alg}.csv"
        filepath = path_prefix + filename

        # Pandas load
        df = pd.read_csv(filepath)
        # Rename slurm to batch
        df = df.rename(columns={"slurm": "batch"})
        df = df.assign(slurm=df['dataset'].astype('category').cat.codes)
        n_codes = len(df['slurm'].unique())
        codes = ()
        while len(codes) != n_codes:
            codes = encode_dataset(n_codes)

        df = df.assign(slurm=df['slurm'].map(dict(zip(df['slurm'].unique(), codes))))
        # Make a legend to map the dataset to the encoded dataset
        legend = dict(zip(df['slurm'], df['dataset']))
        legend = {str(k): v for k, v in legend.items()}
        df['slurm'] = (df['slurm'].astype(str) + df['batch'].astype(str))
        # Cast to int
        df['slurm'] = df['slurm'].astype(int)
        # Drop the batch column
        df = df.drop(columns=['batch'])
        # Save the encoding legend to the dict
        encodings[alg] = legend
        # Save the new csv
        df.to_csv(filepath, index=False)

    return encodings


def print_alg_stats(dir, algs):

    cross_solver_avg = pd.DataFrame()
    for alg in algs:
        # df results_sorted_{alg}.csv
        df = pd.read_csv(f"{dir}\\results_sorted_{alg}.csv")

        # Df stats (By Dataset)
        df_stats = df.groupby(['dataset']).agg({'cost': ['min', 'max', 'mean', 'median']})
        df_stats.to_latex(f"{dir}\\stats_{alg}.tex")

        # Overall
        # as a copy
        df_cross = df.copy()
        df_stats = df_cross.agg({'cost': ['min', 'max', 'mean', 'median']})
        # Rename cost to alg
        df_stats = df_stats.rename(columns={"cost": alg})
        # Add to the cross solver df
        cross_solver_avg = pd.concat([cross_solver_avg, df_stats], axis=1)

    print(cross_solver_avg)
    cross_solver_avg.to_latex(f"{dir}\\stats_cross.tex")

    #@TODO
    # Better pretty plots,
    # Wilcoxon
    # Scatter plots
    # Convergence (MAYBE)

    # Wilcoxon signed rank test
    # https://www.youtube.com/watch?v=iYFn1m4hFww
    # https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_nonparametric/bs704_nonparametric4.html
    # stats.wilcoxon(df, datasets, n_datasets, n_samples, seeds)

