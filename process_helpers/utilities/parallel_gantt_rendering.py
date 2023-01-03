import os
from multiprocessing import Pool
from tqdm import tqdm
from process_helpers.utilities.plotting import render_gantt_json


def print_args(x):
    dataset = x[0]
    alg_dir = x[1]
    id = x[2]

    img_path = f"{alg_dir}img/gif/{dataset}/"
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    json_path = f"{alg_dir}/json/{id}_gantt.json"
    render_gantt_json(infile=json_path, destination=img_path)

def run_in_parallel():
    args = []


    datasets = ["abz5"]
    algs = ["genetic"]
    for alg in algs:
        alg_path = root_path + "output/" + alg + "/"
        for dataset in datasets:
            with open(f"{alg_path}unique_solution_ids.txt", "r") as f:
                for id in f.read().splitlines():
                    args.append((dataset, root_path + "output/" + alg + "/", id))

    pool = Pool(processes=4)
    r = list(tqdm(pool.imap(print_args, args), total=len(args)))


if __name__ == '__main__':
    print("Rendering Gantt Charts")
    root_path = "/home/kali/PycharmProjects/Capstone/jobs/"
    run_in_parallel()
