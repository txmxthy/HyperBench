import os

from process_helpers.to_gif import minimal_animated_gantt
from process_helpers.utilities.plotting import alg_gantts, alg_merge_boxes, render_gantt_json, unify_csvs

if __name__ == '__main__':
    outdir = "/home/kali/PycharmProjects/Capstone/jobs/output/"
    sim_dir = outdir + "sim_anneal/"
    tabu_dir = outdir + "tabu_search/"
    genetic_dir = outdir + "genetic/"
    constraint_dir = outdir + "constraint/"
    dispatch_dir = outdir + "dispatching_rules/"

    # List dirs in output
    subdirs = os.listdir(outdir)
    print(subdirs)

    keys = {"sim_anneal": "instance,cost,seed,temp,cooldown,timeout,slurm",
            "tabu_search": "instance,cost,seed,tabu_len,nsteps,hold,timeout,slurm",
            "genetic": "instance,cost,seed,pop_size,ngen,mut_rate,cross_rate,timeout",
            "constraint": "dataset,seed,cost,slurm",
            "dispatching_rules": "dataset,seed,cost,slurm"}

    for alg in subdirs:
        print(f"\nRunning for {alg}: Merging CSVs.")
        unify_csvs(outdir+alg+"/", key=keys[alg], alg=alg)


    # # Box Plots and CSV magic
    # key = "instance,cost,seed,temp,cooldown,timeout"
    # alg_merge_boxes("SA", sim_dir + "results/", key)
    #
    # key = "instance,cost,seed,tabu_length,max_steps,longest_hold,timeout"
    # alg_merge_boxes("TA", tabu_dir + "results/", key)

    # Genetic
    # key = "instance,cost,seed,pop_size,ngen,mut_rate,cross_rate,timeout"
    # alg_merge_boxes("GA", genetic_dir + "results/", key)
    # minimal_animated_gantt(genetic_dir, key)

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
