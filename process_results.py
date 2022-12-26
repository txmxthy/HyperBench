import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



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


    # Create a boxplot for each seed


    # Create a boxplot for each parameter combination
    box_plotter(df, dir, instance, "Cost variance across seeds for " + instance, X="seed", Y="cost")
    box_plotter(df, dir, instance, "Cost variance across parameter combination for " + instance, X="param", Y="cost")


def box_plotter(df, dir, instance, name, X="param", Y="cost"):
    sns.boxplot(x=X, y=Y, data=df)
    # Rotate x labels
    plt.xticks(rotation=90)
    plt.title(name)
    plt.savefig(f"{dir}/{instance}_boxplot_{X}.png", bbox_inches='tight')
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





if __name__ == '__main__':
    dir = "/home/kali/PycharmProjects/Capstone/jobs/output/sim_anneal"
    key = "instance,cost,seed,temp,cooldown,timeout"
    unify_csvs(dir=dir, key=key)

    datasets = [f for f in os.listdir(dir) if f.startswith('results') is False and f.endswith('.csv')]
    for dataset in datasets:
        pretty_plots(instance=dataset, dir=dir, key=key)