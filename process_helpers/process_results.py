import json
import os
import random
import shutil
from time import sleep

import pandas as pd

from process_helpers.utilities.parallel_gantt_rendering import make_parallel_args, render_parallel_gantt
from process_helpers.utilities.plotting import unify_csvs, pretty_plot, win_uni_dir, win_root_dir, handle_one_to_many, \
    get_one_to_many, save_encoding, load_encoding, print_alg_stats
from process_helpers.utilities.schedule_diff import get_unique_solutions_by_alg
from process_helpers.utilities.to_gif import to_gif, merge_gifs


def make_gantt_charts(to_render, args, delete_old=False):
    if delete_old:
        for alg in to_render:
            alg_path = f'{win_uni_dir()}\\output\\{alg}\\results\\gif\\'
            if os.path.exists(alg_path):
                shutil.rmtree(alg_path)
            while os.path.exists(alg_path):
                sleep(1)
            print(f"Deleted {alg_path}")

    render_parallel_gantt(args)


def gantt_gif_by_alg_dataset(to_render, datasets):
    for alg in to_render:
        alg_path = f'{win_uni_dir()}\\output\\{alg}\\results\\gif\\'
        if not os.path.exists(alg_path + "base\\"):
            os.makedirs(alg_path + "base\\")
        for dataset in datasets:
            images_dir = f'{alg_path}img\\{dataset}\\'
            filename = f'{alg}_{dataset}.gif'
            to_gif(images_dir, alg_path + "base\\", filename)


def combined_gif_by_alg(to_render):
    for alg in to_render:
        alg_path = f'{win_uni_dir()}\\output\\{alg}\\results\\gif\\'
        files = os.listdir(alg_path + "base\\")
        gifs = [f for f in files if f.endswith('.gif')]
        merge_gifs(alg_path, gifs, f'{alg}_dataset_merged.gif')


def main():
    outdir = "E:\\Capstone_Data\\"
    results_path = "D:\\Projects\\Capstone\\Code\\jobs\\results"
    uni_path = f"{results_path}\\output"
    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    subdirs = os.listdir(outdir)

    keys = {
        "sim_anneal": ["dataset", "cost", "seed", "temp", "cooldown", "timeout", "slurm"],
        "tabu_search": ["dataset", "cost", "seed", "tabu_len", "nsteps", "hold", "timeout", "slurm"],
        "genetic": ["dataset", "cost", "seed", "pop_size", "ngen", "mut_rate", "cross_rate", "timeout"],
        "constraint": ["dataset", "seed", "cost", "timeout", "slurm"],
        "dispatching_rules": ["dataset", "seed", "cost", "slurm"]
    }

    # Warning - Genetic has MANY unique solutions
    # to_render = ['constraint']
    to_render = ['constraint', 'dispatching_rules', 'sim_anneal', 'tabu_search']

    # Disabled as we have got this already
    # for alg in to_render:
    #     unify_csvs(outdir + alg, key=keys[alg], alg=alg)

    for alg in to_render:
        pretty_plot(alg=alg, filepath=f'{win_uni_dir()}\\results_sorted_{alg}.csv', key=keys[alg])

    # # Handle 1:Many slurm relations i.e. one slurm to test many datasets
    one_to_many = get_one_to_many()
    encoding = handle_one_to_many(win_uni_dir(), one_to_many)
    if encoding is not None:
        save_encoding(encoding)
    encoding = load_encoding()

    # Find and record unique schedules and track repeats: See unique-solutions-ids.txt
    for alg in to_render:
        get_unique_solutions_by_alg(alg=alg, key=keys[alg], json_path=f'{outdir}{alg}\\json\\')

    parallel_rendering_args = make_parallel_args(algs=to_render,
                                                 datasets=datasets,
                                                 root_path=win_uni_dir(),
                                                 json_root=f'{outdir}',
                                                 encoding=encoding)

    # Delete the old gif directory if it is in to_render
    make_gantt_charts(to_render,
                      parallel_rendering_args,
                      delete_old=True)

    # Turn gantt charts into gifs
    gantt_gif_by_alg_dataset(to_render, datasets)

    # Combine Gifs in a few ways:
    # 1. All datasets for an alg
    # 2. All algs for a dataset
    # 3. All algs for all datasets
    # 4. Best gantt for each alg for each dataset
    combined_gif_by_alg(to_render)
    # Table stats

    print_alg_stats(results_path, to_render)

    print("Done!")
    # @TODO Table with summary statistics
    # @TODO PASS IN STATS SO THEY CAN BE RENDERED ON THE SAME SCALE
    # @TODO MAP SLURMS TO DISPATCHING RULES


if __name__ == '__main__':
    main()
