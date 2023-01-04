import os

from process_helpers.utilities.parallel_gantt_rendering import render_gantt_in_parallel
from process_helpers.utilities.plotting import unify_csvs, pretty_plot, win_uni_dir, win_root_dir
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
    print(subdirs)

    keys = {
        "sim_anneal": ["dataset", "cost", "seed", "temp", "cooldown", "timeout", "slurm"],
        "tabu_search": ["dataset", "cost", "seed", "tabu_len", "nsteps", "hold", "timeout", "slurm"],
        "genetic": ["dataset", "cost", "seed", "pop_size", "ngen", "mut_rate", "cross_rate", "timeout"],
        "constraint": ["dataset", "seed", "cost", "timeout", "slurm"],
        "dispatching_rules": ["dataset", "seed", "cost", "slurm"]
    }



    for alg in subdirs:
        pass
    #     print(f"\nRunning for {alg}: Merging CSVs.")
    #     keys[alg] = unify_csvs(outdir + alg, key=keys[alg], alg=alg)
    #
    # # test = ["tabu_search"]
    # #keys["genetic"].append("slurm")
    #
    # for alg in subdirs:
    #     print(f"\nRunning for {alg}: Creating boxplots.")
    #     pretty_plot(alg=alg, filepath=f'{win_uni_dir()}\\results_sorted_{alg}.csv', key=keys[alg])
    #     @TODO: Should do get unique solutions by problem rather than dataset. Label the solvers that got the same solution.
    #     get_unique_solutions_by_alg(alg=alg, key=keys[alg], json_path=f'{outdir}{alg}\\json\\')

    # @TODO Table with summary statistics
    # @TODO PASS IN STATS SO THEY CAN BE RENDERED ON THE SAME SCALE
    # @TODO MAP SLURMS TO DISPATCHING RULES
    datasets = ['ft10', 'abz7', 'ft20', 'abz9', 'la04', 'la03', 'abz6', 'la02', 'abz5', 'la01']
    render_gantt_in_parallel(algs=subdirs,
                             datasets=datasets,
                             root_path=f"{win_uni_dir()}\\output\\",
                             json_path=f'{outdir}genetic\\json\\')

    # @TODO STATISTICAL SIGNIFICANCE TESTS

    print("Done!")
