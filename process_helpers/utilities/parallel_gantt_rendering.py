import os
from multiprocessing import Pool
from tqdm.auto import tqdm
from process_helpers.utilities.plotting import render_gantt_json


def use_args(x):
    dataset = x[0]
    target = x[1]
    idn = x[2]
    json_path = x[3]

    img_path = f"{target}\\results\\gif\\img\\{dataset}\\"
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    json_file = f"{json_path}\\{idn}_gantt.json"
    render_gantt_json(infile=json_file, destination=img_path)

def render_gantt_in_parallel(algs, datasets, root_path, json_path):

    print(f"Algs {algs}, Datasets {datasets}, Root {root_path}, JSON {json_path}")

    args = []

    for alg in algs:

        alg_path = f'{root_path}{alg}'
        for dataset in datasets:
            # D:\Projects\Capstone\Code\jobs\results\output\genetic\unique_solution_ids.txt
            # D:\\Projects\\Capstone\\Code\\jobs\\results\\genetic\\unique_solution_ids.txt
            with open(f"{alg_path}\\unique_solution_ids.txt", "r") as f:
                for idn in f.read().splitlines():
                    args.append((dataset, alg_path, idn, json_path))

    pool = Pool(processes=6)
    r = list(tqdm(pool.imap(use_args, args), total=len(args)))




if __name__ == '__main__':
    print("Rendering Gantt Charts")
    datasets = ["abz5"]
    algs = ["genetic"]
    root_path = "/home/kali/PycharmProjects/Capstone/jobs/"
    render_gantt_in_parallel(algs, datasets, root_path)
