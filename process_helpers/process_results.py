import os

from process_helpers.utilities.plotting import unify_csvs, pretty_plot, win_uni_dir

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

    # keys = {"sim_anneal": "instance,cost,seed,temp,cooldown,timeout,slurm",
    #         "tabu_search": "instance,cost,seed,tabu_len,nsteps,hold,timeout,slurm",
    #         "genetic": "instance,cost,seed,pop_size,ngen,mut_rate,cross_rate,timeout",
    #         "constraint": "dataset,seed,cost,slurm",
    #         "dispatching_rules": "dataset,seed,cost,slurm"}

    keys = {
        "sim_anneal": ["dataset", "cost", "seed", "temp", "cooldown", "timeout", "slurm"],
        "tabu_search": ["dataset", "cost", "seed", "tabu_len", "nsteps", "hold", "timeout", "slurm"],
        "genetic": ["dataset", "cost", "seed", "pop_size", "ngen", "mut_rate", "cross_rate", "timeout"],
        "constraint": ["dataset", "seed", "cost", "timeout", "slurm"],
        "dispatching_rules": ["dataset", "seed", "cost", "slurm"]
    }

    test = ["sim_anneal"]

    # for alg in subdirs:
    #     print(f"\nRunning for {alg}: Merging CSVs.")
    #     keys[alg] = unify_csvs(outdir + alg, key=keys[alg], alg=alg)

    for alg in subdirs:
        print(f"\nRunning for {alg}: Creating boxplots.")
        pretty_plot(alg=alg, filepath=f'{win_uni_dir()}\\results_sorted_{alg}.csv', key=keys[alg])

    # # # Gantt Charts
    # alg_gantts(tabu_dir + "json/", tabu_dir)
    #
    # alg_gantts(genetic_dir + "json/", genetic_dir)

    # alg_gantts(constraint_dir + "json/", constraint_dir)

    # alg_gantts(sim_dir + "json/", sim_dir)

    # Animated Different Gantt Charts

    # @TODO
    # Table of results for each algorithm
    # Terminal output and latex table

    print("Done!")
