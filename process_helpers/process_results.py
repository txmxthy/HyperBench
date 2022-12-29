import os

from process_helpers.utilities.plotting import alg_gantts, alg_merge_boxes

if __name__ == '__main__':

    outdir = "/home/kali/PycharmProjects/Capstone/jobs/output/"
    sim_dir = outdir + "sim_anneal/"
    tabu_dir = outdir + "tabu_search/"
    genetic_dir = outdir + "genetic/"

    hardcoded_Test="/home/kali/PycharmProjects/Capstone/src/Solvers/constraint/outputs/"
    alg_gantts(hardcoded_Test, hardcoded_Test)



    # # Box Plots and CSV magic
    # key = "instance,cost,seed,temp,cooldown,timeout"
    # alg_merge_boxes("SA", sim_dir + "results/", key)
    #
    # key = "instance,cost,seed,tabu_length,max_steps,longest_hold,timeout"
    # alg_merge_boxes("TA", tabu_dir + "results/", key)

    # # Gantt Charts
    # candidates = tabu_dir + "json/"
    # alg_gantts(candidates, tabu_dir)
    #
    # candidates = genetic_dir + "json/"
    # alg_gantts(candidates, genetic_dir)