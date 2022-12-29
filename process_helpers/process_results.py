import os

from process_helpers.utilities.plotting import alg_gantts, alg_merge_boxes

if __name__ == '__main__':
    outdir = "/home/kali/PycharmProjects/Capstone/jobs/output/"
    sim_dir = outdir + "sim_anneal/"
    tabu_dir = outdir + "tabu_search/"
    genetic_dir = outdir + "genetic/"
    constraint_dir = outdir + "constraint/"
    dispatch_dir = outdir + "dispatching/"

    # # Box Plots and CSV magic
    # key = "instance,cost,seed,temp,cooldown,timeout"
    # alg_merge_boxes("SA", sim_dir + "results/", key)
    #
    # key = "instance,cost,seed,tabu_length,max_steps,longest_hold,timeout"
    # alg_merge_boxes("TA", tabu_dir + "results/", key)

    # # # Gantt Charts
    # alg_gantts(tabu_dir + "json/", tabu_dir)
    #
    # alg_gantts(genetic_dir + "json/", genetic_dir)

    alg_gantts(constraint_dir + "json/", constraint_dir)

    print("Done!")
