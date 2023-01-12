import json
import os
import random
import shutil
from time import sleep

import pandas as pd
from scipy.stats import wilcoxon

from process_helpers.utilities.parallel_gantt_rendering import make_parallel_args, render_parallel_gantt
from process_helpers.utilities.plotting import unify_csvs, win_uni_dir, win_root_dir, handle_one_to_many, \
    get_one_to_many, save_encoding, load_encoding, print_alg_stats, pretty_plot
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

"""
perform willcoxon test on all algs and datasets
"""
def calc_wilcoxon(algs):
    print(algs)
    # print(datasets)
    # columns = alg, dataset,seed,cost,slurm, p-value
    df = pd.DataFrame(columns=['alg', 'dataset', 'seed', 'cost', 'slurm', 'p-value'])
    for alg in algs:
        filepath=f'{win_uni_dir()}\\results_sorted_{alg}.csv'
        if os.path.exists:
            df_alg = pd.read_csv(filepath, header=0)
            # first line is the header
            # df_alg.columns = df_alg.iloc[0]
            df_alg = df_alg[1:]
            df_alg = df_alg.reset_index(drop=True)
            df_alg['alg'] = alg
            df_alg['p-value'] = 0

            df = df.append(df_alg[df.columns])


    print(df)
    # calc wilcoxon for each algorithm compared with all other algorithms for each dataset
    wilcoxon_df = pd.DataFrame(columns=['alg1', 'alg2', 'dataset', 'p-value'])
    for alg1 in df['alg'].unique():
        wilcoxon_df_inner = pd.DataFrame(columns=['alg2', 'dataset', 'p-value'])
        for alg2 in df['alg'].unique():
            # check alg1 != alg2 and haven't already calculated
            if alg1 != alg2:
                for dataset in df['dataset'].unique():

                    # get all costs for alg1 and alg2
                    alg1_costs = df[(df['alg'] == alg1) & (df['dataset'] == dataset)]['cost']
                    alg2_costs = df[(df['alg'] == alg2) & (df['dataset'] == dataset)]['cost']

                    alg1_costs = random.sample(list(alg1_costs), min(len(alg1_costs), len(alg2_costs)))
                    alg2_costs = random.sample(list(alg2_costs), min(len(alg1_costs), len(alg2_costs)))

                    # if x - y == 0 for all x,y in alg1_costs and alg2_costs, p value is 1
                    if all(x == y for x, y in zip(alg1_costs, alg2_costs)):
                        p = 1
                    # print(alg1_costs)
                    # print(alg2_costs)
                    # perform wilcoxon test
                    else:
                        stat, p = wilcoxon(alg1_costs, alg2_costs)
                    # print('Statistics=%.3f, p=%.3f' % (stat, p))
                    # interpret
                    alpha = 0.05

                        # print('Same distribution (fail to reject H0)')


                        # print('Different distribution (reject H0)')
                        # add to df
                    # round p value to 3 decimal places
                    if p > alpha:
                        p = str(p) + ' (same distribution)'
                    wilcoxon_df_inner = wilcoxon_df_inner.append({'alg2': alg2, 'dataset': dataset, 'p-value': p},
                                                                ignore_index=True)
        # new dataframe where alg2 column in wilcoxon_df_inner is the column names, the index is the dataset, and the values are the p-values
        wilcoxon_df_inner_new = wilcoxon_df_inner.pivot(index='dataset', columns='alg2', values='p-value')
        wilcoxon_df_inner_new.to_csv(f'{win_uni_dir()}\\results_wilcoxon_{alg1}.csv', index=True)
        # convert df_inner_new into latex table
        latex = wilcoxon_df_inner_new.to_latex()
        # print(latex)
        # save latex table
        with open(f'{win_uni_dir()}\\results_wilcoxon_{alg1}.txt', 'w') as f:
            f.write(latex)
        wilcoxon_df_inner['alg1'] = alg1
        wilcoxon_df = wilcoxon_df.append(wilcoxon_df_inner[wilcoxon_df.columns])
    print(wilcoxon_df)
    # remove duplicates, including alg1==alg2, alg2==alg1
    # wilcoxon_df = wilcoxon_df.drop_duplicates(subset=['alg1', 'alg2', 'dataset'], keep='first')
    # remove instances where a
    wilcoxon_df.to_csv(f'{win_uni_dir()}\\results_wilcoxon.csv', index=False)







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
        "dispatching_rules": ["dataset", "seed", "cost", "rules", "n_rules", "slurm"]
    }

    # Warning - Genetic has MANY unique solutions
    # to_render = ['constraint']
    to_reunify = ['sim_anneal', 'tabu_search', 'constraint']
    to_render = ['constraint', 'dispatching_rules', 'sim_anneal', 'tabu_search']

    # Disabled as we have got this already - dispatching is quite finnicky
    # for alg in to_reunify:
    #     print(f"Reunifying {alg}")
    #     unify_csvs(outdir + alg, key=keys[alg], alg=alg)

    # calc_wilcoxon(algs={key: keys[key] for key in to_render})
    calc_wilcoxon(algs=keys)

    # # # Handle 1:Many slurm relations i.e. one slurm to test many datasets
    # one_to_many = get_one_to_many()
    # encoding = handle_one_to_many(win_uni_dir(), one_to_many)
    # if encoding is not None:
    #     save_encoding(encoding)
    # encoding = load_encoding()
    #
    # # Find and record unique schedules and track repeats: See unique-solutions-ids.txt
    # for alg in to_render:
    #     get_unique_solutions_by_alg(alg=alg, key=keys[alg], json_path=f'{outdir}{alg}\\json\\')
    #
    # parallel_rendering_args = make_parallel_args(algs=to_render,
    #                                              datasets=datasets,
    #                                              root_path=win_uni_dir(),
    #                                              json_root=f'{outdir}',
    #                                              encoding=encoding)
    #
    # # Delete the old gif directory if it is in to_render
    # make_gantt_charts(to_render,
    #                   parallel_rendering_args,
    #                   delete_old=True)
    #
    # # Turn gantt charts into gifs
    # gantt_gif_by_alg_dataset(to_render, datasets)
    #
    # # Combine Gifs in a few ways:
    # # 1. All datasets for an alg
    # # 2. All algs for a dataset
    # # 3. All algs for all datasets
    # # 4. Best gantt for each alg for each dataset
    # combined_gif_by_alg(to_render)
    # # Table stats
    #
    # print_alg_stats(results_path, to_render)
    #
    # print("Done!")
    # # @TODO Table with summary statistics
    # # @TODO PASS IN STATS SO THEY CAN BE RENDERED ON THE SAME SCALE
    # # @TODO MAP SLURMS TO DISPATCHING RULES


if __name__ == '__main__':
    main()
