import os
import random

import pandas as pd

from process_helpers.utilities.parallel_gantt_rendering import make_parallel_args, render_parallel_gantt
from process_helpers.utilities.plotting import unify_csvs, pretty_plot, win_uni_dir, win_root_dir, handle_one_to_many
from process_helpers.utilities.schedule_diff import get_unique_solutions_by_alg
from process_helpers.utilities.to_gif import to_gif

if __name__ == '__main__':
    # outdir = "/home/kali/PycharmProjects/Capstone/jobs/output/"
    outdir = "E:\\Capstone_Data\\"
    sim_dir = outdir + "sim_anneal/"
    tabu_dir = outdir + "tabu_search/"
    genetic_dir = outdir + "genetic/"
    constraint_dir = outdir + "constraint/"
    dispatch_dir = outdir + "dispatching_rules/"

    # Unified
    uni_path = "D:\\Projects\\Capstone\\Code\\jobs\\results\\output"

    # List dirs in output
    subdirs = os.listdir(outdir)
    # subdirs = ["tabu_search"]
    print(subdirs)

    keys = {
        "sim_anneal": ["dataset", "cost", "seed", "temp", "cooldown", "timeout", "slurm"],
        "tabu_search": ["dataset", "cost", "seed", "tabu_len", "nsteps", "hold", "timeout", "slurm"],
        "genetic": ["dataset", "cost", "seed", "pop_size", "ngen", "mut_rate", "cross_rate", "timeout"],
        "constraint": ["dataset", "seed", "cost", "timeout", "slurm"],
        "dispatching_rules": ["dataset", "seed", "cost", "slurm"]
    }

    for alg in subdirs:
        print(f"\nRunning for {alg}: Merging CSVs.")
        unify_csvs(outdir + alg, key=keys[alg], alg=alg)

    for alg in subdirs:
        print(f"\nRunning for {alg}: Creating boxplots.")
        # pretty_plot(alg=alg, filepath=f'{win_uni_dir()}\\results_sorted_{alg}.csv', key=keys[alg])

    # @TODO can check for duplicate keys to automatically create this list in future
    # Handle 1:Many slurm relations i.e. one slurm to test many datasets
    one_to_many = ["dispatching_rules"]
    encoding = handle_one_to_many(win_uni_dir(), one_to_many)

    for alg in subdirs:
        print(f"\nRunning for {alg}: Finding Unique Schedules")
        get_unique_solutions_by_alg(alg=alg, key=keys[alg], json_path=f'{outdir}{alg}\\json\\')

    # @TODO Table with summary statistics
    # @TODO PASS IN STATS SO THEY CAN BE RENDERED ON THE SAME SCALE
    # @TODO MAP SLURMS TO DISPATCHING RULES

    to_render = ['constraint', 'dispatching_rules', 'sim_anneal', 'tabu_search']
    # Warning - Genetic has MANY unique solutions

    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    args = make_parallel_args(algs=to_render,
                              datasets=datasets,
                              root_path=win_uni_dir(),
                              json_root=f'{outdir}',
                              encoding=encoding)

    render_parallel_gantt(args)

    # for alg in to_render:
    #     alg_dir = f'{win_uni_dir()}\\output\\{alg}\\'
    #
    #     for dataset in datasets:
    #         # D:\Projects\Capstone\Code\jobs\results\output\constraint\results\gif\img
    #         images_dir = f'{alg_dir}\\results\\gif\\img\\{dataset}\\'
    #         filename = f'{alg}_{dataset}.gif'
    #         to_gif(images_dir, alg_dir, filename)

    print("Done!")
